*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jan 23, 2026 - 1:47 PM*
---
You're looking in the **wrong place**! The ACR credentials aren't stored in Vault's **KV secrets engine** — they're **dynamically generated** by Vault's **Azure secrets engine**.

---

## Where the ACR Credentials Actually Come From

Based on your infrastructure, the `fitfile-image-pull-secret` is created by Vault Secrets Operator (VSO) using:

```yaml
Mount: azure                    # ← Azure secrets engine (not KV)
Namespace: admin/central        # ← Central shared namespace
Path: creds/acr-pull           # ← Dynamic credential generator
```

This is a **dynamic secret** — Vault generates short-lived Azure Service Principal credentials **on-demand** and automatically rotates them.

---

## Why You're Getting 403 Errors

You're trying to access `admin/secrets/` (a KV mount), but:
1. There's **no KV secrets engine** mounted at `admin/secrets/`
2. Your token doesn't have permissions for that path anyway
3. ACR credentials live in the **Azure engine** at `admin/central/azure/creds/acr-pull`

---

## Diagnosis Commands (Run These)

### 1. Check if VSO Can Read from the Azure Engine
```bash
export VAULT_ADDR="https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200"

# See what's mounted in the central namespace
vault secrets list -namespace=admin/central

# Try to generate a fresh ACR credential (this will fail if auth is broken)
vault read -namespace=admin/central azure/creds/acr-pull
```

### 2. Check the VaultDynamicSecret Resource Status
```bash
# Find the VaultDynamicSecret that creates the image pull secret
kubectl get vaultdynamicsecret -A | grep -i "image-pull\|acr"

# Get detailed status (replace namespace if needed)
kubectl -n argocd describe vaultdynamicsecret argocd-pull
```

**Look for:**
- `SecretSynced` events (good)
- `VaultClientError` events (auth broken)
- `SecretLease` status with `renewable: true`

### 3. Verify the Secret Content is Fresh
```bash
# Check when the secret was last updated
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.metadata.creationTimestamp}'

# Decode and check the username (should be a GUID-like Service Principal ID)
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' \
  | base64 -d | jq -r '.auths["fitfileregistry.azurecr.io"].username'
```

---

## The Real Problem (Based on Your Errors)

Your `acr-test` pod is still getting **401 Unauthorized** from ACR. This means:

1. ✅ The secret exists in Kubernetes
2. ✅ The pod is configured to use it
3. ❌ **The credentials inside the secret are expired/invalid**

This happens when:
- VSO failed to refresh the secret before the Azure SP credentials expired
- The VaultDynamicSecret wasn't created in the `spicedb` namespace
- The credentials were rotated in Azure but VSO hasn't synced yet

---

## Quick Fix: Force VSO to Regenerate the Secret

```bash
# Delete the stale secret
kubectl -n spicedb delete secret fitfile-image-pull-secret

# Trigger VSO to recreate it (if VaultDynamicSecret exists)
kubectl get vaultdynamicsecret -A | grep -i spicedb

# If it doesn't exist, copy the working one from argocd
kubectl -n argocd get vaultdynamicsecret argocd-pull -o json \
  | jq '.metadata.namespace="spicedb" | del(.metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .metadata.managedFields)' \
  | kubectl apply -f -
```

Then restart the test pod:
```bash
kubectl -n spicedb delete pod acr-test --force --grace-period=0
kubectl -n spicedb run acr-test \
  --image=fitfileregistry.azurecr.io/bitnami/os-shell:12-debian-12-r24 \
  --restart=Never \
  --overrides='{"spec":{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}}'
```

---

**Run these commands and paste the output** — specifically the `vault secrets list -namespace=admin/central` and the `vaultdynamicsecret` status. That will tell us if VSO can even talk to Vault's Azure engine.