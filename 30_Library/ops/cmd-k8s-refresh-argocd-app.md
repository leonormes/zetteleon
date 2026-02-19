---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
tags: #atomic #kubectl #argocd
---

# Force Hard Refresh of ArgoCD Application

## 🎯 Intent
Force ArgoCD to re-evaluate manifest generation from scratch, ignoring existing cached comparisons. This is different from a `sync`, as it triggers the `repo-server` logic.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
kubectl annotate application <APP_NAME> -n argocd argocd.argoproj.io/refresh=hard --overwrite
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{.status.conditions[0].message}' && echo
```
Expected signal:
- If success, message is empty or updated timestamp.
- If failure, error message updated (no longer says `(cached)`).

---

## 🔗 Related
- [[cmd-argocd-flush-cache]]
