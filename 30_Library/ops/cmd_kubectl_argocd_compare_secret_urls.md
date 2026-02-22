---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, credentials, diff, debug]
---

# Compare ArgoCD Repository Secret URLs

## 🎯 Intent
Compare the decoded `url` field of an ArgoCD repository secret. 
ArgoCD strictly matches the repository secret's `url` against the dependency URL inside `Chart.yaml`. Mismatches cause silent auth failures. This is highly useful when comparing a broken cluster against a working one.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
# Run this against the failing cluster, then run it against the working cluster to diff.
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.data.url}' | base64 -d && echo
```

### Placeholders
- `<SECRET_NAME>` — Name of the target Secret

---

## ✅ Verification
- Expected Output: A plaintext URL string like `https://myregistry.azurecr.io/helm` or `myregistry.azurecr.io`. 

## 💥 Failure Mode Analysis
- **Symptom:** The working cluster expects `myregistry.azurecr.io` but the failing cluster's secret specifies `oci://myregistry.azurecr.io`.
  - **Fix:** ArgoCD `repo-server` is failing string interpolation. Reconfigure the secret generation engine (or VSO manifest) to drop or add the scheme protocol as required.
