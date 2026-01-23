*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jan 23, 2026 - 1:45 PM*
---
You're right—let's stop guessing and get the full diagnostic picture. Here's a **complete diagnostic runbook** that will tell us exactly what's wrong.

---

## **Part 1: What's Actually IN the Secret (and does it work)?**

### 1.1 Decode the Secret and Check Its Contents
```bash
# See what registry/username/password are in the secret
kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' \
  | base64 -d | jq '.'
```

**Expected output:** Should show `fitfileregistry.azurecr.io` with username/password.

---

### 1.2 Test if Those Credentials Actually Work
Extract the credentials and try to log in manually:
```bash
# Extract username and password
ACR_USER=$(kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq -r '.auths["fitfileregistry.azurecr.io"].username')
ACR_PASS=$(kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq -r '.auths["fitfileregistry.azurecr.io"].password')

echo "Username: $ACR_USER"
echo "Password: ${ACR_PASS:0:10}..." # Only show first 10 chars for safety

# Test login
echo "$ACR_PASS" | docker login fitfileregistry.azurecr.io -u "$ACR_USER" --password-stdin
```

**If this fails:** The credentials in the K8s secret are expired/wrong. Skip to **Part 4** to regenerate them.

---

## **Part 2: What's in Vault?**

### 2.1 List What Secrets Exist in Vault
```bash
export VAULT_ADDR="https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200"
export VAULT_NAMESPACE="admin"

# List secrets in the deployment namespace
vault kv list -namespace=admin/deployments/lca-prd-2 secrets/
```

### 2.2 Check if the ACR Credentials Are in Vault
```bash
# Check if there's a secret path for ACR/Docker registry
vault kv list -namespace=admin secrets/ | grep -i registry
vault kv list -namespace=admin secrets/ | grep -i docker
vault kv list -namespace=admin secrets/ | grep -i acr

# If you find a path (e.g., "common/fitfile-registry-reader"), read it:
vault kv get -namespace=admin secrets/common/fitfile-registry-reader
```

---

## **Part 3: What Permissions Does the Cluster Have?**

### 3.1 Check What Vault Auth Role Exists for `spicedb`
```bash
# List all roles in the JWT auth
vault list -namespace=admin auth/jwt-lca-prd-2/role

# Read the role config for spicedb (if it exists)
vault read -namespace=admin auth/jwt-lca-prd-2/role/spicedb-app
```

### 3.2 Check What That Role is Allowed to Read
```bash
# Check the policies attached to the role
POLICIES=$(vault read -namespace=admin auth/jwt-lca-prd-2/role/spicedb-app -format=json | jq -r '.data.token_policies[]')

# Read each policy
for policy in $POLICIES; do
  echo "=== Policy: $policy ==="
  vault policy read -namespace=admin "$policy"
done
```

### 3.3 Check What the `spicedb` Namespace Service Account Can Actually Access
```bash
# Generate a token from the cluster's perspective
ISS="$(kubectl get --raw /.well-known/openid-configuration | jq -r '.issuer')"
JWT="$(kubectl -n spicedb create token default --duration=10m --audience="$ISS")"

# Try to log in to Vault using that token
vault write -namespace=admin auth/jwt-lca-prd-2/login role=spicedb-app jwt="$JWT"

# If successful, test what paths you can read with that token
VAULT_TOKEN="<token from above>" vault kv get -namespace=admin/deployments/lca-prd-2 secrets/spicedb
```

---

## **Part 4: Fix – Regenerate ACR Credentials Directly from Azure**

If the credentials in Vault/K8s are stale, regenerate them from the source of truth (Azure):

```bash
ACR_NAME="fitfileregistry"

# Get fresh credentials from Azure
ACR_USER=$(az acr credential show -n "$ACR_NAME" --query username -o tsv)
ACR_PASS=$(az acr credential show -n "$ACR_NAME" --query 'passwords[0].value' -o tsv)

echo "Fresh credentials retrieved:"
echo "Username: $ACR_USER"
echo "Password: ${ACR_PASS:0:10}..."

# Test them
echo "$ACR_PASS" | docker login fitfileregistry.azurecr.io -u "$ACR_USER" --password-stdin
```

If that works, update the K8s secret:
```bash
kubectl -n spicedb delete secret fitfile-image-pull-secret

kubectl -n spicedb create secret docker-registry fitfile-image-pull-secret \
  --docker-server=fitfileregistry.azurecr.io \
  --docker-username="$ACR_USER" \
  --docker-password="$ACR_PASS"

# Patch all service accounts
kubectl -n spicedb patch serviceaccount default --type merge -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}'
kubectl -n spicedb patch serviceaccount spicedb --type merge -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}'
kubectl -n spicedb patch serviceaccount spicedb-postgresql --type merge -p '{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}'
```

Then delete and recreate the test pod:
```bash
kubectl -n spicedb delete pod acr-test --force --grace-period=0

kubectl -n spicedb run acr-test \
  --image=fitfileregistry.azurecr.io/bitnami/os-shell:12-debian-12-r24 \
  --restart=Never \
  --overrides='{"spec":{"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}]}}'
```

---

**Run these commands in order and paste the output.** This will show us:
1. If the secret content is wrong
2. If Vault has the right secrets
3. If the K8s→Vault auth path is broken
4. Whether we need to regenerate credentials from Azure