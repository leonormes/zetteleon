*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jan 23, 2026 - 1:50 PM*
---
## Analysis: Your Vault & VSO Setup is Working Correctly

The good news: **Your infrastructure is healthy!**

✅ **Vault Azure Engine:** Generating fresh ACR credentials successfully  
✅ **VSO Authentication:** JWT auth working (`jwt-043880980a3209593d1880-admin/central`)  
✅ **Secret Sync:** `argocd-pull` has an active 12h lease with no errors  
✅ **Credential Validity:** The generated Service Principal credentials are valid

---

## The Real Problem: Namespace Distribution

The `spicedb` namespace pods are failing because **the image pull secret doesn't exist there**. Your VSO only created the secret in the `argocd` namespace (as `argocd-acr-pull-secret`).

---

## Solution: Create VaultDynamicSecret for SpiceDB Namespace

### Option A: Create a New VaultDynamicSecret (Recommended)

```bash
cat <<'YAML' | kubectl apply -f -
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: spicedb-acr-pull
  namespace: spicedb
spec:
  mount: azure
  namespace: admin/central
  path: creds/acr-pull
  vaultAuthRef: default
  renewalPercent: 67
  destination:
    create: true
    name: fitfile-image-pull-secret
    overwrite: false
    type: kubernetes.io/dockerconfigjson
    transformation:
      excludes:
        - ".*"
      templates:
        .dockerconfigjson:
          text: |
            {
              "auths": {
                "fitfileregistry.azurecr.io": {
                  "username": "{{get .Secrets "client_id"}}",
                  "password": "{{get .Secrets "client_secret"}}",
                  "auth": "{{printf "%s:%s" (get .Secrets "client_id") (get .Secrets "client_secret") | b64enc}}"
                }
              }
            }
YAML
```

### Option B: Quick Fix - Copy the Working Secret

```bash
# Copy the working secret from argocd to spicedb
kubectl -n argocd get secret argocd-acr-pull-secret -o json \
| jq '
  .metadata.namespace="spicedb"
  | .metadata.name="fitfile-image-pull-secret"
  | del(.metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .metadata.managedFields, .metadata.ownerReferences)
' \
| kubectl apply -f -
```

---

## Verify & Restart

### 1. Confirm the Secret Exists
```bash
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.type}'
# Should output: kubernetes.io/dockerconfigjson
```

### 2. Patch Service Accounts
```bash
kubectl -n spicedb patch serviceaccount default --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}'

kubectl -n spicedb patch serviceaccount spicedb --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}' 2>/dev/null || true

kubectl -n spicedb patch serviceaccount spicedb-postgresql --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}' 2>/dev/null || true
```

### 3. Delete the Failed Pods
```bash
kubectl -n spicedb delete pod spicedb-postgresql-0
kubectl -n spicedb delete pod -l app.kubernetes.io/name=spicedb
```

### 4. Force ArgoCD to Re-Sync
```bash
kubectl -n argocd annotate application spicedb argocd.argoproj.io/refresh=hard --overwrite
```

---

## Why This Happened

Your infrastructure uses **per-namespace VaultDynamicSecret resources**. The `argocd` namespace has one, but `spicedb` was deployed without creating its own. This is by design—VSO doesn't auto-distribute secrets across namespaces for security reasons.

**Option A** (creating a VaultDynamicSecret) is better because:
- Automatic 12h credential rotation
- Survives pod restarts
- Self-healing if secret gets deleted

**Option B** (copying) is faster but:
- Static credentials (no rotation)
- Requires manual updates
- Will break if the source secret rotates

---

Run **Option A** commands, then check the pod status:
```bash
kubectl -n spicedb get pods -w
```

The `ImagePullBackOff` should clear within 30 seconds. Let me know if you see any new errors!