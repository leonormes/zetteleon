---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
tags: [atomic, argocd, sync, mutation]
---

# Sync ArgoCD Application

## 🎯 Intent
Manually triggers a sync operation to apply the Git state to the cluster.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
argocd app sync <APP_NAME> --prune --retry-limit 3
```

### Placeholders
- `<APP_NAME>` — The name of the ArgoCD application.

---

## ✅ Verification

```bash
argocd app wait <APP_NAME>
```

Expected signal:
- Application reaches `Synced` status.

---

## 🧠 Failure Modes
- `Sync Failed`: Check for immutable field violations or admission webhook blocks.

---

## 🔗 Related
- [[cmd_argocd_rollback_app]]
- [[cmd_argocd_refresh_app]]