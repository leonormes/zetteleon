---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
tags: #atomic #kubectl #argocd #cache
---

# Nuclear ArgoCD Cache Flush

## 🎯 Intent
Forced restart of all ArgoCD control-plane components to clear "ghost" authentication caches in Redis and the controller memory. Use this when 401 errors persist after updating credentials.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
# Clear the Redis cache (the "brain")
kubectl delete pod -n argocd -l app.kubernetes.io/name=argocd-redis

# Restart the Controller (the "logic loop")
kubectl delete pod -n argocd -l app.kubernetes.io/name=argocd-application-controller

# Restart the Repo Server (the "executor")
kubectl delete pod -n argocd -l app.kubernetes.io/name=argocd-repo-server
```

---

## ✅ Verification
Expected signal:
- New pods reach `Running` and `1/1 Ready` status.
- Next sync attempt should use fresh credentials.

---

## 🔗 Related
- [[pb-argocd-oci-auth-fail]]
- [[cmd-k8s-refresh-argocd-app]]
