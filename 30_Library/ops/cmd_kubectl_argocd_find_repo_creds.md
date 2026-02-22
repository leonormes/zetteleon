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

# Find ArgoCD Repository Template Secrets

## 🎯 Intent
Locate all Kubernetes Secrets in the `argocd` namespace that are tagged as URL template credentials (`secret-type=repo-creds`). These secrets implicitly match any repository URL that begins with the specified URL template and take precedence over exact-match `repository` secrets.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repo-creds -o json | \
  jq '.items[] | select(.data.url) | {name: .metadata.name, url: (.data.url | @base64d)}'
```

---

## ✅ Verification
- Expected Output: A stream of JSON objects containing `name` and decoded `url`. Find secrets whose URL acts as a prefix for your registry.

## 💥 Failure Mode Analysis
- **Symptom:** You have a valid `repository` secret but authentication is still failing.
  - **Fix:** A stale `repo-creds` secret might be taking precedence. This command helps identify the offending overrides.

---

## 🔗 Related
- [[cmd_kubectl_argocd_find_repo_secrets]]
- [[cmd_kubectl_argocd_get_secret_creds]]
