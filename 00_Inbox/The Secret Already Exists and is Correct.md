---
created: 2026-01-23T14:01:20+00:00
modified: 2026-01-23T19:27:37+00:00
title: The Secret Already Exists and is Correct
---

## The Secret Already Exists and is Correct

You don't need to copy anything - the `VaultDynamicSecret` you created earlier **successfully generated the secret**. The error you're seeing is because `argocd-acr-pull-secret` is **not a Docker config secret** - it's an ArgoCD Helm repository secret with a different structure.

---

## The Real Problem: Old Pods Don't Have the Secret

Your pods are still failing because they were created **before** you patched the service accounts. Kubernetes doesn't automatically update running pods when you change their service account.

---

## Solution: Force Pod Recreation

Delete the old pods so they recreate with the updated service account (which now has `imagePullSecrets`):

```bash
# Delete all spicedb-related pods
kubectl -n spicedb delete pod -l app.kubernetes.io/name=spicedb --force --grace-period=0
kubectl -n spicedb delete pod spicedb-postgresql-0 --force --grace-period=0

# Delete the test pod too
kubectl -n spicedb delete pod acr-test --force --grace-period=0 2>/dev/null || true
```

Wait 10 seconds, then check:

```bash
kubectl -n spicedb get pods -w
```

---

## Verify the Credentials Are Actually Valid

While waiting for pods to recreate, test if the credentials in the secret actually work:

```bash
# Extract credentials and test
ACR_USER=$(kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq -r '.auths["fitfileregistry.azurecr.io"].username')
ACR_PASS=$(kubectl -n spicedb get secret fitfile-image-pull-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq -r '.auths["fitfileregistry.azurecr.io"].password')

echo "Testing credentials:"
echo "$ACR_PASS" | docker login fitfileregistry.azurecr.io -u "$ACR_USER" --password-stdin
```

**If the login fails with 401**, the Azure SP credentials have expired. In that case, delete the `VaultDynamicSecret` to force VSO to regenerate fresh credentials:

```bash
kubectl -n spicedb delete vaultdynamicsecret spicedb-acr-pull
kubectl -n spicedb delete secret fitfile-image-pull-secret

# Recreate it
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

# Wait 10 seconds for VSO to create it
sleep 10
kubectl -n spicedb get secret fitfile-image-pull-secret
```

---

**Run the pod deletion commands and paste the output of `kubectl -n spicedb get pods` after 30 seconds.** If pods still fail, paste the output of the `docker login` test command.
