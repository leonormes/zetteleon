---
aliases: [Secret Rotation Protocol, VSO Troubleshooting]
created: 2026-03-12T09:00:00Z
modified: 2026-03-14T11:10:17+00:00
status: evergreen
tags: [argocd, kubernetes, protocol, secrets, vault, vso]
title: Protocol - VSO Secret Management & Troubleshooting
type: Protocol
updated: 2026-03-12
---

## Protocol - VSO Secret Management & Troubleshooting

### 1. Context & Architecture

The FITFILE platform uses HashiCorp Vault (HCP) as the Source of Truth for all secrets. The Vault Secrets Operator (VSO) synchronizes these into Kubernetes as native `Secret` objects.

#### Core Components

- VaultAuth: Defines how VSO authenticates to Vault (typically using Kubernetes ServiceAccount JWT or AppRole).
- VaultStaticSecret (VSS): Syncs KV (static) secrets from Vault.
- VaultDynamicSecret (VDS): Generates and syncs dynamic credentials (e.g., Azure Service Principals for ACR).
- Reflector: Replicates secrets (like image pull secrets) from a source namespace (e.g., `argocd`) to all application namespaces.

---

### 2. The "Overwrite" Golden Rule

CRITICAL: For any secret managed by VSO, especially dynamic ones, the specification MUST include:

```yaml
spec:
  destination:
    overwrite: true
```

Why? If `overwrite: false` (the default), VSO will create the secret once but will never update it. For dynamic secrets (ACR tokens), the Vault lease will rotate, but the Kubernetes secret will remain stuck with the expired credential, leading to `401 Unauthorized` errors.

---

### 3. ArgoCD & ACR Specifics

ArgoCD uses two types of secrets for ACR/Helm OCI:

1. Repository Secret (`argocd.argoproj.io/secret-type: repository`): Used for specific repo URLs.
2. Repo-Creds Secret (`argocd.argoproj.io/secret-type: repo-creds`): Acts as a template for multiple repos.

Priority Warning: In ArgoCD, `repo-creds` take priority over `repository` secrets. If a stale manual `repo-creds` exists, it will override a valid VSO-managed `repository` secret.

---

### 4. Troubleshooting Playbook

#### Phase 1: End-to-End Diagnostic Chain

If a secret is missing or failing to sync, trace the "wiring" in this exact order:

1. **VaultDynamicSecret / VaultStaticSecret (CR):**
   ```bash
   kubectl describe <kind> <name> -n <ns>
   ```
   *Identify: Which VaultAuth is referenced? What is the Vault path?*

2. **VaultAuth (Identity):**
   ```bash
   kubectl describe vaultauth <auth-ref> -n <ns>
   ```
   *Identify: Is it using `method: kubernetes` or `appRole`? Which ServiceAccount or SecretRef is used?*

3. **VaultConnection (Endpoint):**
   ```bash
   kubectl describe vaultconnection <conn-ref> -n <ns>
   ```
   *Identify: Is the Vault address correct? Are the namespace headers accurate?*

4. **Operator Logs (System):**
   ```bash
   kubectl logs -n vault-secrets-operator-system deploy/vault-secrets-operator-controller-manager --tail=100
   ```
   *Look for: 403 (Policy error), 404 (Path error), or TLS handshake failures.*

5. **Vault-side Verification (CLI):**
   ```bash
   export VAULT_NAMESPACE="<as-defined-in-vss>"
   vault secrets list
   vault policy read <policy-name>
   ```
   *Check: Does the path exist? Does the policy grant `read` (or `write` for dynamic) capabilities?*

#### Phase 2: Common Fixes

| Issue | Symptom | Fix |
|:--- |:--- |:--- |
| Stale Credentials | `401 Unauthorized` / `Invalid clientid` | Set `overwrite: true` in VDS/VSS and delete the K8s secret to force recreation. |
| Permission Denied | `Code: 403` in VSO logs | Check the Vault Policy attached to the role VSO is using (e.g., `lca-prd-2-read`). |
| Double Namespace | `404 Not Found` in Vault path | Check if `spec.namespace` is relative or absolute. Avoid double nesting like `admin/admin/…`. |
| ArgoCD Priority | Valid secret but ArgoCD fails | Find and delete manual `repo-creds` secrets overriding the VSO `repository` secret. |
| Startup Crash (.NET) | `User creation failed` / `Identity error` | **Password Complexity**: Ensure the Vault-stored password meets Microsoft Identity requirements (Upper, Lower, Num, Special). |

---

### 5. Force Refresh Protocol

If a secret is stuck or out of sync, follow this exact sequence:

1. **Patch to Overwrite** (if not already set):
   ```bash
   kubectl patch <kind> <name> -n <ns> --type='merge' -p '{"spec":{"destination":{"overwrite":true}}}'
   ```

2. **The "Dummy Annotation" Trick** (Bypass polling interval):
   Inject a timestamp to force an immediate reconciliation without deleting the secret.
   ```bash
   kubectl annotate <kind> <name> -n <ns> force-sync=$(date +%s) --overwrite
   ```

3. **Delete K8s Secret** (If patching fails):
   ```bash
   kubectl delete secret <secret-name> -n <ns>
   ```

4. **Restart Consumer**:
   ```bash
   kubectl rollout restart deployment <deployment-name> -n <ns>
   ```

---

### 6. Maintenance & Toil Reduction

- Cleanup: Regularly check for orphaned `VaultDynamicSecret` leases in Vault. If multiple VDS target the same SP, they can pile up hundreds of credentials.
- Single Source: Prefer using a single `VaultDynamicSecret` in the `argocd` namespace and use Reflector to push it to other namespaces, rather than creating identical VDS resources everywhere.

---

### 7. Audit & Documentation (The Wiki Builder)

Use these commands to generate a real-time "wiring diagram" of cluster secrets.

#### A. Map VSO Resources to Vault Paths
```bash
kubectl get vaultstaticsecrets,vaultdynamicsecrets -A \
  -o jsonpath='{range .items[*]}{.kind}{" | "}{.metadata.namespace}{" | "}{.metadata.name}{" | vaultAuthRef="}{.spec.vaultAuthRef}{" | vaultNS="}{.spec.namespace}{" | mount="}{.spec.mount}{" | path="}{.spec.path}{" | dest="}{.spec.destination.name}{"\n"}{end}' \
| sort
```

#### B. Map Namespace Authentication Methods
```bash
kubectl get vaultauth -A \
  -o jsonpath='{range .items[*]}{.metadata.namespace}{" | "}{.metadata.name}{" | method="}{.spec.method}{" | mount="}{.spec.mount}{" | vaultNS="}{.spec.namespace}{" | role="}{.spec.jwt.role}{" | sa="}{.spec.jwt.serviceAccount}{"\n"}{end}' \
| sort
```

#### C. Generate a Markdown Secrets Map
```bash
OUT="secrets-map-$(date +%F).md"
{
  echo "# Cluster Secrets Wiring Map"
  echo "Generated: $(date)"
  echo
  echo "## VaultAuth Strategy per Namespace"
  kubectl get vaultauth -A -o jsonpath='{range .items[*]}- {.metadata.namespace}: method={.spec.method}, mount={.spec.mount}, vaultNS={.spec.namespace}, role={.spec.jwt.role}, sa={.spec.jwt.serviceAccount}{"\n"}{end}' | sort
  echo
  echo "## VSO Managed Secrets (Creation Logic)"
  kubectl get vaultstaticsecrets,vaultdynamicsecrets -A -o jsonpath='{range .items[*]}- {.kind} `{.metadata.namespace}/{.metadata.name}` → dest=`{.spec.destination.name}` (type=`{.spec.destination.type}`), vaultNS=`{.spec.namespace}`, mount=`{.spec.mount}`, path=`{.spec.path}`, vaultAuthRef=`{.spec.vaultAuthRef}`{"\n"}{end}' | sort
} > "$OUT"
```
