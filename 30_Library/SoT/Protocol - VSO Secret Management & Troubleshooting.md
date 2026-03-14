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

#### Phase 1: Diagnostics

1. Check the VSO Custom Resource (CR):

   ```bash
   kubectl describe vaultdynamicsecret <name> -n <namespace>
   ```

   _Look for: `SecretSynced: True` or errors in Events (e.g., `VaultClientError`, `Permission Denied`)._

2. Verify the Kubernetes Secret Metadata:

   ```bash
   kubectl get secret <name> -n <namespace> -o yaml
   ```

   _Look for: `ownerReferences` (should point to VSO) and distinctive VSO annotations._

3. Check VSO Operator Logs:

   ```bash
   kubectl logs -n vault-secrets-operator-system -l app.kubernetes.io/name=vault-secrets-operator
   ```

#### Phase 2: Common Fixes

| Issue | Symptom | Fix |
|:--- |:--- |:--- |
| Stale Credentials | `401 Unauthorized` / `Invalid clientid` | Set `overwrite: true` in VDS/VSS and delete the K8s secret to force recreation. |
| Permission Denied | `Code: 403` in VSO logs | Check the Vault Policy attached to the role VSO is using (e.g., `lca-prd-2-read`). |
| Double Namespace | `404 Not Found` in Vault path | Check if `spec.namespace` is relative or absolute. Avoid double nesting like `admin/admin/…`. |
| ArgoCD Priority | Valid secret but ArgoCD fails | Find and delete manual `repo-creds` secrets overriding the VSO `repository` secret. |

---

### 5. Force Refresh Protocol

If a secret is stuck or out of sync, follow this exact sequence:

1. Patch to Overwrite:

   ```bash
   kubectl patch vaultdynamicsecret <name> -n <ns> --type='merge' -p '{"spec":{"destination":{"overwrite":true}}}'
   ```

2. Delete K8s Secret:

   ```bash
   kubectl delete secret <secret-name> -n <ns>
   ```

3. Trigger VSO Sync:

   ```bash
   kubectl annotate vaultdynamicsecret <name> -n <ns> force-sync=$(date +%s) --overwrite
   ```

4. Restart Consumer:

   ```bash
   kubectl rollout restart deployment <deployment-name> -n <ns>
   ```

---

### 6. Maintenance & Toil Reduction

- Cleanup: Regularly check for orphaned `VaultDynamicSecret` leases in Vault. If multiple VDS target the same SP, they can pile up hundreds of credentials.
- Single Source: Prefer using a single `VaultDynamicSecret` in the `argocd` namespace and use Reflector to push it to other namespaces, rather than creating identical VDS resources everywhere.
