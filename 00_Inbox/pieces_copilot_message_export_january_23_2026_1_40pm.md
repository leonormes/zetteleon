*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jan 23, 2026 - 1:40 PM*
---
From your logs (latest at **2026-01-23 ~13:37**), `acr-test` is stuck in `ImagePullBackOff` pulling from `fitfileregistry.azurecr.io` — that’s almost always **image pull auth** (missing/incorrect `imagePullSecret`, or credentials no longer valid).

Below is a **copy/paste runbook** to (1) verify what’s wrong and (2) fix it.

---

## 0) Clean up the stuck test pod (so you get fresh events)
```bash
kubectl -n spicedb delete pod acr-test --force --grace-period=0 2>/dev/null || true
```

---

## 1) Verify the namespace has the image pull secret (and it targets the right registry)
```bash
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.type}{"\n"}'
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' \
  | base64 -d | jq -r '.auths | keys[]'
```

Expected:
- type: `kubernetes.io/dockerconfigjson`
- auth key includes: `fitfileregistry.azurecr.io`

If the secret is missing or doesn’t contain that registry hostname, fix it in **Step 3**.

---

## 2) Ensure the service account used by workloads references the secret
Check which SA your real pods use (example for spicedb deployment + postgres statefulset):
```bash
kubectl -n spicedb get pod -l app.kubernetes.io/name=spicedb -o jsonpath='{range .items[*]}{.metadata.name}{"  sa="}{.spec.serviceAccountName}{"\n"}{end}' 2>/dev/null || true
kubectl -n spicedb get pod spicedb-postgresql-0 -o jsonpath='sa={.spec.serviceAccountName}{"\n"}' 2>/dev/null || true
```

Now patch the relevant SAs (safe even if already set):
```bash
kubectl -n spicedb patch serviceaccount default --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}'

kubectl -n spicedb patch serviceaccount spicedb --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}' 2>/dev/null || true

kubectl -n spicedb patch serviceaccount spicedb-postgresql --type merge \
  -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}' 2>/dev/null || true
```

---

## 3) Fix the secret (two options)

### Option A (fast): copy the secret from a namespace where it works
You previously had it in `lca-prd-2` / `argocd` etc. Copy from `lca-prd-2` → `spicedb`:

```bash
kubectl -n lca-prd-2 get secret fitfile-image-pull-secret -o json \
| jq '
  .metadata.namespace="spicedb"
  | del(.metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .metadata.managedFields, .metadata.ownerReferences)
' \
| kubectl apply -f -
```

### Option B (authoritative): recreate it from Azure ACR credentials (fixes “creds rotated/expired”)
Set variables:
```bash
ACR_NAME="fitfileregistry"
ACR_SERVER="${ACR_NAME}.azurecr.io"
```

Get a fresh username/password from Azure (requires `az login` already working on the box you run it from):
```bash
ACR_USER="$(az acr credential show -n "$ACR_NAME" --query username -o tsv)"
ACR_PASS="$(az acr credential show -n "$ACR_NAME" --query 'passwords[0].value' -o tsv)"
```

Recreate the secret in `spicedb`:
```bash
kubectl -n spicedb delete secret fitfile-image-pull-secret 2>/dev/null || true

kubectl -n spicedb create secret docker-registry fitfile-image-pull-secret \
  --docker-server="$ACR_SERVER" \
  --docker-username="$ACR_USER" \
  --docker-password="$ACR_PASS"
```

---

## 4) Re-test image pulling in spicedb namespace
Create a fresh `acr-test` that explicitly uses the secret:
```bash
kubectl -n spicedb run acr-test \
  --image=fitfileregistry.azurecr.io/bitnami/os-shell:12-debian-12-r24 \
  --restart=Never \
  --overrides='{"spec":{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}}'
```

Watch + inspect events:
```bash
kubectl -n spicedb get pod acr-test -w
# in another terminal:
kubectl -n spicedb describe pod acr-test | sed -n '/Events:/,$p'
```

If it still 401s after Option B, that strongly suggests **ACR-side permissions / repo scope** (e.g., the credentials don’t have pull rights for that repository), and we should switch to checking ACR role assignments / tokens.

---

## 5) Kick ArgoCD workloads after the secret fix
Once `acr-test` pulls successfully, restart the real stuck pods:
```bash
kubectl -n spicedb delete pod -l app.kubernetes.io/name=spicedb
kubectl -n spicedb delete pod spicedb-postgresql-0
```

And force ArgoCD to re-evaluate:
```bash
kubectl -n argocd annotate application spicedb argocd.argoproj.io/refresh=hard --overwrite
```

---

If you paste the **full** `kubectl -n spicedb describe pod acr-test` event block *including the “Failed to pull image … 401 Unauthorized …” line* (right now your snippet only shows BackOff/Failed without the earlier reason), I can tell you whether we’re dealing with:
- missing/unused secret (K8s-side wiring), or
- wrong/expired credentials (secret content), or
- ACR permission/scope issue (Azure-side).