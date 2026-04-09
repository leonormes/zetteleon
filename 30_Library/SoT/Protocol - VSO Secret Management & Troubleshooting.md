---
aliases: [Secret Rotation Protocol, VSO Troubleshooting]
created: 2026-03-12T08:52:25+00:00
last_synthesis: 2026-04-05
modified: 2026-04-09T08:11:05+00:00
status: evergreen
tags: [aks, argocd, hcp-vault, kubernetes, protocol, secrets, vault, vso]
title: Protocol - VSO Secret Management & Troubleshooting
type: Protocol
updated: 2026-04-05
---

## Protocol - VSO Secret Management & Troubleshooting

### 1. The Mental Model: The High-Security Office

To understand Kubernetes secrets and certificate flows, visualize the system as a physical security operation rather than abstract cryptographic handshakes.

| Component | Physical Analogy | Description |
|:--- |:--- |:--- |
| Pod | The Employee | The entity needing access to a locked resource (e.g., database password). |
| Service Account | The ID Badge | The identity (JWT token) issued to the employee upon hiring. |
| VSO | The Trusted Courier | A high-clearance guard whose sole job is to fetch keys for employees. |
| HCP Vault | The Central Safe | The secure location where all master keys and secrets are stored. |
| K8s API / OIDC | The Notary | The authority that verifies if an ID badge (token) is genuine. |

#### The Flow (Secrets)

1. Request: You define a `VaultStaticSecret`. (You tell the Courier: "Get the DB key for this Pod.")
2. Proof: VSO grabs the Pod's Service Account Token. ("Here is the ID badge.")
3. Verification: Vault asks the K8s API: "Did you issue this badge to this specific Pod?"
4. Delivery: Once verified, Vault hands the key to VSO, who drops it into a standard K8s Secret.

#### The Flow (Certificates)

Similar to secrets, but the Pod generates a CSR (a blank passport with a photo). Vault checks the identity, applies its cryptographic stamp (Signature), and returns a valid TLS certificate.

---

### 2. Manual Verification (Bypassing the Black Box)

If the VSO operator is failing and the logs are ambiguous, perform the "Handshake" manually to isolate the failure point.

#### Step 1: Procure the "ID Badge" (K8s Token)

```bash
# 1. Create a test identity
kubectl create serviceaccount manual-vault-test -n <ns>
# 2. Generate a 1-hour token
export KUBE_TOKEN=$(kubectl create token manual-vault-test -n <ns>)
# 3. Inspect the badge (requires jq)
jq -R 'split(".") | .[1] | @base64d | fromjson' <<< $KUBE_TOKEN
```

#### Step 2: Perform the Handshake (Vault Login)

```bash
export VAULT_ADDR="https://<your-hcp-vault-url>:8200"
# Present the K8s token to Vault's kubernetes auth mount
curl -s --request POST \
  --data '{"jwt": "'"$KUBE_TOKEN"'", "role": "<your-vault-role>"}' \
  $VAULT_ADDR/v1/auth/kubernetes/login
```

_Success returns a `client_token`. Failure here indicates a K8s-to-Vault trust issue (JWT provider, CA, or Role mapping)._

#### Step 3: Fetch the Secret

```bash
export VAULT_TOKEN="<hvs.token-from-step-2>"
curl -s -H "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/secret/data/<path>
```

_Failure here indicates a Vault Policy issue (the identity is valid, but doesn't have `read` on the path)._

---

### 3. Core Components & Logic

The FITFILE platform uses HCP Vault as the Source of Truth. VSO synchronizes these into Kubernetes as native `Secret` objects.

- VaultAuth: Defines how VSO authenticates (ServiceAccount JWT or AppRole).
- VaultStaticSecret (VSS): Syncs KV (static) secrets.
- VaultDynamicSecret (VDS): Generates/syncs ephemeral credentials (e.g., Azure SPs for ACR).
- Reflector: Replicates secrets (like image pull secrets) from `argocd` to all application namespaces.

---

### 4. The "Overwrite" Golden Rule

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

1. VaultDynamicSecret / VaultStaticSecret (CR):

   ```bash
   kubectl describe <kind> <name> -n <ns>
   ```

   _Identify: Which VaultAuth is referenced? What is the Vault path?_

2. VaultAuth (Identity):

   ```bash
   kubectl describe vaultauth <auth-ref> -n <ns>
   ```

   _Identify: Is it using `method: kubernetes` or `appRole`? Which ServiceAccount or SecretRef is used?_

3. VaultConnection (Endpoint):

   ```bash
   kubectl describe vaultconnection <conn-ref> -n <ns>
   ```

   _Identify: Is the Vault address correct? Are the namespace headers accurate?_

4. Operator Logs (System):

   ```bash
   kubectl logs -n vault-secrets-operator-system deploy/vault-secrets-operator-controller-manager --tail=100
   ```

   _Look for: 403 (Policy error), 404 (Path error), or TLS handshake failures._

5. Vault-side Verification (CLI):

   ```bash
   export VAULT_NAMESPACE="<as-defined-in-vss>"
   vault secrets list
   vault policy read <policy-name>
   ```

   _Check: Does the path exist? Does the policy grant `read` (or `write` for dynamic) capabilities?_

#### Phase 2: Common Fixes

| Issue | Symptom | Fix |
|:--- |:--- |:--- |
| Stale Credentials | `401 Unauthorized` / `Invalid clientid` | Set `overwrite: true` in VDS/VSS and delete the K8s secret to force recreation. |
| Permission Denied | `Code: 403` in VSO logs | Check the Vault Policy attached to the role VSO is using (e.g., `lca-prd-2-read`). |
| Double Namespace | `404 Not Found` in Vault path | Check if `spec.namespace` is relative or absolute. Avoid double nesting like `admin/admin/…`. |
| ArgoCD Priority | Valid secret but ArgoCD fails | Find and delete manual `repo-creds` secrets overriding the VSO `repository` secret. |
| Startup Crash (.NET) | `User creation failed` / `Identity error` | Password Complexity: Ensure the Vault-stored password meets Microsoft Identity requirements (Upper, Lower, Num, Special). |

---

### 5. Force Refresh Protocol

If a secret is stuck or out of sync, follow this exact sequence:

1. Patch to Overwrite (if not already set):

   ```bash
   kubectl patch <kind> <name> -n <ns> --type='merge' -p '{"spec":{"destination":{"overwrite":true}}}'
   ```

2. The "Dummy Annotation" Trick (Bypass polling interval):
   Inject a timestamp to force an immediate reconciliation without deleting the secret.

   ```bash
   kubectl annotate <kind> <name> -n <ns> force-sync=$(date +%s) --overwrite
   ```

3. Delete K8s Secret (If patching fails):

   ```bash
   kubectl delete secret <secret-name> -n <ns>
   ```

4. Restart Consumer:

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
