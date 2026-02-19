# Playbook: Debugging VSO-Managed Kubernetes Secrets

> **When to use this:** A Kubernetes Secret managed by HashiCorp Vault Secrets Operator (VSO) is suspected to be stale, misconfigured, or causing authentication failures (e.g. `401 unauthorized` from a container registry).

---

## Phase 1: Identify the Secret's Origin

The goal is to determine **what created the secret** and **where in Vault it comes from**.

### 1.1 Full Secret Dump

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o yaml
```

This is the single most valuable command. Scan the output for:

- **`metadata.labels`** — look for `app.kubernetes.io/managed-by: hashicorp-vso` to confirm VSO ownership.
- **`metadata.ownerReferences`** — tells you the exact VSO Custom Resource (CR) that owns this secret and its `kind` (`VaultStaticSecret`, `VaultDynamicSecret`, or `VaultPKISecret`).
- **`metadata.annotations`** — look for `reflector.v1.k8s.emberstack.com/*` annotations indicating the secret is mirrored to other namespaces.

### 1.2 Check Owner References Directly

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.metadata.ownerReferences}' | jq .
```

| Field | Meaning |
|---|---|
| `kind: VaultDynamicSecret` | Vault generates short-lived credentials (e.g. Azure SP, AWS IAM) |
| `kind: VaultStaticSecret` | Vault stores a static KV secret |
| `kind: VaultPKISecret` | Vault issues a TLS certificate |
| Empty / missing | Secret was **not** created by VSO — investigate Helm, ArgoCD, or manual creation |

### 1.3 Check Labels

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.metadata.labels}' | jq .
```

VSO-managed secrets will have:

```json
{
  "app.kubernetes.io/component": "secret-sync",
  "app.kubernetes.io/managed-by": "hashicorp-vso",
  "app.kubernetes.io/name": "vault-secrets-operator"
}
```

### 1.4 Check Annotations

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.metadata.annotations}' | jq .
```

Look for clues about other controllers:

| Annotation prefix | Source |
|---|---|
| `secrets.hashicorp.com/*` | VSO |
| `reflector.v1.k8s.emberstack.com/*` | Ember Stack Reflector (mirrors secrets across namespaces) |
| `meta.helm.sh/release-name` | Helm |
| `argocd.argoproj.io/*` | ArgoCD |

---

## Phase 2: Inspect the VSO Custom Resource

Once you know the owning CR kind and name from Phase 1:

### 2.1 List All VSO CRs in the Namespace

```bash
kubectl get vaultstaticsecret,vaultdynamicsecret,vaultpkisecret -n <NAMESPACE>
```

### 2.2 Get the Full CR Spec

```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o yaml
```

Example:

```bash
kubectl get vaultdynamicsecret fitfile-image-pull -n argocd -o yaml
```

**Key fields to note in the spec:**

| Field | What it tells you |
|---|---|
| `spec.mount` | The Vault secrets engine mount path (e.g. `azure`, `kv`, `pki`) |
| `spec.namespace` | The Vault namespace (e.g. `admin/central`) |
| `spec.path` | The path within the mount (e.g. `creds/acr-pull`) |
| `spec.vaultAuthRef` | Which VSO VaultAuth CR is used to authenticate to Vault |
| `spec.destination.name` | The K8s Secret name VSO writes to |
| `spec.destination.overwrite` | **Critical:** `false` means VSO will NOT overwrite a manually edited secret |
| `spec.destination.transformation` | Templates used to reshape Vault data into the K8s Secret format |

### 2.3 Check CR Status (Lease Health)

```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o yaml | grep -A 30 "status:"
```

This shows:

- Current Vault lease ID
- Last renewal time
- Sync errors or failures
- Whether the secret is up to date

---

## Phase 3: Inspect the Secret Data

### 3.1 Decode the Secret

For `kubernetes.io/dockerconfigjson` type secrets:

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .
```

For `Opaque` type secrets:

```bash
# List all keys
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data}' | jq 'keys'

# Decode a specific key
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.data.<KEY>}' | base64 -d
```

### 3.2 Check Recent Events

```bash
kubectl events -n <NAMESPACE> --for secret/<SECRET_NAME>
```

> **Note:** Kubernetes events expire after ~1 hour by default. No events does **not** mean nothing happened — it means nothing happened *recently*.

---

## Phase 4: Common Failure — Stale Credentials After Manual Edit

### Symptoms

- `401 unauthorized` or `403 forbidden` errors from downstream services (e.g. container registries, databases).
- The VSO CR status shows no errors (it thinks everything is fine).
- The secret's `creationTimestamp` is older than expected for a dynamic secret.

### Root Cause

1. Vault issued dynamic credentials with a finite TTL.
2. Someone manually edited the K8s Secret (or it was modified by another controller).
3. The Vault lease expired, invalidating the old credentials in the upstream provider (e.g. Azure AD).
4. VSO attempted to sync fresh credentials but `spec.destination.overwrite: false` prevented the write.
5. The K8s Secret now contains expired credentials that will never be refreshed.

### Fix

**Step 1: Delete the secret so VSO recreates it with fresh credentials.**

```bash
kubectl delete secret <SECRET_NAME> -n <NAMESPACE>
```

Watch it come back:

```bash
kubectl get secret -n <NAMESPACE> -w | grep <SECRET_NAME>
```

VSO will detect its owned secret is missing and recreate it within seconds.

**Step 2: Prevent recurrence by enabling overwrite.**

```bash
kubectl patch <CR_KIND> <CR_NAME> -n <NAMESPACE> \
  --type='merge' \
  -p '{"spec":{"destination":{"overwrite":true}}}'
```

**Step 3: Verify the new credentials are valid.**

```bash
# Confirm new creationTimestamp
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.metadata.creationTimestamp}'

# For dockerconfigjson secrets — confirm new client_id
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq '.auths | to_entries[0].value.username'
```

---

## Phase 5: Reflector — Checking Mirrored Copies

If the source secret has Ember Stack Reflector annotations, it is automatically mirrored to other namespaces.

### 5.1 Check Which Namespaces Receive the Mirror

```bash
kubectl get secret <SECRET_NAME> -n <SOURCE_NAMESPACE> \
  -o jsonpath='{.metadata.annotations.reflector\.v1\.k8s\.emberstack\.com/reflection-auto-namespaces}'
```

### 5.2 Verify a Mirrored Copy Matches the Source

```bash
# Compare the data hash across namespaces
for ns in <NAMESPACE_1> <NAMESPACE_2> <NAMESPACE_3>; do
  echo -n "$ns: "
  kubectl get secret <SECRET_NAME> -n $ns \
    -o jsonpath='{.data}' 2>/dev/null | md5sum || echo "NOT FOUND"
done
```

> **Important:** When you delete and recreate the source secret (Phase 4), Reflector should automatically update all mirrored copies. Verify this with the command above after the fix.

---

## Quick Reference: Full Vault Path

When you need to tell someone "where does this secret come from in Vault," the answer is assembled from three CR fields:

```
{spec.namespace}/{spec.mount}/{spec.path}
```

Example: `admin/central/azure/creds/acr-pull`

---

## Checklist Summary

- [ ] Identified the owning VSO CR via `ownerReferences`
- [ ] Confirmed the Vault namespace, mount, and path
- [ ] Checked `spec.destination.overwrite` value
- [ ] Checked CR status for lease/sync errors
- [ ] Decoded and validated the secret data
- [ ] If stale: deleted the secret and confirmed VSO recreated it
- [ ] If stale: patched `overwrite: true` to prevent recurrence
- [ ] Verified mirrored copies (if Reflector is in use) are up to date
