---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
tags: [atomic, argocd, resources, triage]
---

# List Managed Resources

## 🎯 Intent
Lists all Kubernetes resources managed by the ArgoCD application along with their individual sync and health statuses.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
argocd app resources <APP_NAME>
```

### Placeholders
- `<APP_NAME>` — The name of the ArgoCD application.

---

## ✅ Verification
- Scan the `STATUS` and `HEALTH` columns for items that are not `Synced` or `Healthy`.

---

## 🔗 Related
- [[cmd_kubectl_get_events]]
- [[cmd_kubectl_get_pods]]