---
created: 2026-02-22T16:57:41+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-20T16:33:38+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-create-repo-creds-template
requires_tunnel: false
tags: [argocd, cmd, credentials, oci, template]
target_service: argocd
title: cmd_kubectl_argocd_create_repo_creds_template
tool: kubectl
---

## Create ArgoCD Repo-Creds Wildcard Template

### 🎯 Intent

Create a `Secret` containing registry credentials and tag it as `secret-type: repo-creds`. Unlike standard `repository` secrets, `repo-creds` act as wildcard credential templates that ArgoCD applies to any matching URL, which is specifically required during OCI sub-dependency resolution inside Git-sourced Applications.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
# Extract username/password from the exact-match repository secret
PASS=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n argocd -o jsonpath='{.data.password}' | base64 -d)
USER=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n argocd -o jsonpath='{.data.username}' | base64 -d)

# Write the new wildcard repo-creds template
cat <<EOF | kubectl apply -n argocd -f -
apiVersion: v1
kind: Secret
metadata:
  name: argocd-<REGISTRY_PREFIX>-repo-creds
  labels:
    argocd.argoproj.io/secret-type: repo-creds
type: Opaque
stringData:
  url: "<REGISTRY_URL>"
  username: "${USER}"
  password: "${PASS}"
  type: "helm"
  enableOCI: "true"
  ForceHttpBasicAuth: "true"
EOF
```

#### Placeholders

- `<REPOSITORY_SECRET_NAME>`—Name of the VSO-managed or valid source secret containing credentials.
- `<REGISTRY_URL>`—The base domain for string matching (e.g. `fitfileregistry.azurecr.io`).
- `<REGISTRY_PREFIX>`—String identifier for the name field (e.g. `fitfile`).

---

### ✅ Verification

```bash
kubectl get secret argocd-<REGISTRY_PREFIX>-repo-creds -n argocd -o yaml | grep "secret-type: repo-creds"
```

### 💥 Failure Mode Analysis

- Symptom: Validation errors applying the Secret via `kubectl apply`.
  - Fix: If bash variables are empty during extraction, ensure `<REPOSITORY_SECRET_NAME>` corresponds strictly to an existing `repository` secret in the `argocd` namespace.
