---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
tags: #atomic #kubectl #argocd
---

# Force Sync ArgoCD Application (kubectl)

## 🎯 Intent
Manually trigger a reconciliation (sync) of an application with its Git source using a kubectl patch. Use this when auto-sync is disabled or stuck.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
kubectl patch application <app_name> -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'
```

### Placeholders
- `<app_name>` — Name of the ArgoCD application

---

## ✅ Verification
```bash
kubectl get application <app_name> -n argocd -w
```
Expected signal:
- `SYNC STATUS` transitions to `Synced`

---

## 🔗 Related
- [[cmd-k8s-describe-argocd-app]]
