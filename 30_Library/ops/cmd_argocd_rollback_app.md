---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
tags: [atomic, argocd, rollback, recovery]
---

# Rollback ArgoCD Application

## 🎯 Intent
Reverts the application state to a previous successful revision ID.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
argocd app rollback <APP_NAME> <REVISION_ID>
```

### Placeholders
- `<APP_NAME>` — The name of the ArgoCD application.
- `<REVISION_ID>` — The specific ID or relative index (e.g., 0 for previous).

---

## ✅ Verification

```bash
argocd app get <APP_NAME>
```

---

## 🔗 Related
- [[cmd_argocd_sync_app]]