---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, credentials, secrets, debug]
---

# Find ArgoCD Repository Secrets

## 🎯 Intent
Locate all Kubernetes Secrets in the `argocd` namespace that are tagged as exact-match repository credentials (`secret-type=repository`). Decodes the URL to easily identify which registry they target.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository -o json | \
  jq '.items[] | select(.data.url) | {name: .metadata.name, url: (.data.url | @base64d)}'
```

---

## ✅ Verification
- Expected Output: A stream of JSON objects containing `name` and decoded `url`. Find the secret targeting your specific registry URL.

## 💥 Failure Mode Analysis
- **Symptom:** Blank output
  - **Fix:** There are no exact-match repository secrets. Check for template credentials using `repo-creds` instead.

---

## 🔗 Related
- [[cmd_kubectl_argocd_find_repo_creds]]
- [[cmd_kubectl_argocd_get_secret_creds]]
