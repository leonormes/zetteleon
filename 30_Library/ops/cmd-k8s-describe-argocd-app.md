---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
prerequisites:
  - [[cmd-ssh-bastion-tunnel]]
tags: #atomic #kubectl #argocd
---

# Describe ArgoCD Application

## 🎯 Intent
Inspect the detailed status, metadata, and recent events of a specific ArgoCD application to identify why it is failing.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)
- [ ] Bastion host

---

## ⚡ Action

```bash
kubectl describe application <app_name> -n argocd
```

### Placeholders
- `<app_name>` — Name of the ArgoCD application

---

## ✅ Verification
Look for:
- `Status.Sync.Status`: Should be `Synced`
- `Events`: Check for `FailedSync` or `SyncError`
- `Operation State.Message`: Detailed error message from the last sync attempt

---

## 🔗 Related
- [[cmd-k8s-get-argocd-apps]]
- [[cmd-k8s-get-argocd-controller-logs]]
