---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, restart, cache, credentials]
---

# Restart ArgoCD Repo Server

## 🎯 Intent
Restart the ArgoCD `repo-server` deployment. This forcibly flushes its in-memory cache of Git/Helm chart responses and forces it to re-read registry credentials from the Kubernetes Secrets API.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl rollout restart deployment argocd-repo-server -n argocd
kubectl rollout status deployment argocd-repo-server -n argocd
```

---

## ✅ Verification
- Expected Output: The rollout status should report `deployment "argocd-repo-server" successfully rolled out`.

## 💥 Failure Mode Analysis
- **Symptom:** `error: deployment "argocd-repo-server" not found`
  - **Fix:** Confirm you are in the correct cluster context and that the ArgoCD installation resides in the `argocd` namespace. Some installations use a different deployment name (like `argo-cd-repo-server`); use `kubectl get deploy -n argocd` to verify.

---

## 🔗 Related
- [[cmd_argocd_refresh_app]]
- [[playbook_argocd_vso_oci_registry_auth_failure]]
