---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
tags: [atomic, argocd, cache, refresh]
---

# Hard Refresh ArgoCD Application

## 🎯 Intent
Forces ArgoCD to bypass its cache, re-download the Git repository, and re-calculate the comparison with the cluster.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
argocd app get <APP_NAME> --refresh --hard
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
- Observe the `Last Refresh` timestamp in the output to ensure it matches the current time.

---

## 🔗 Related
- [[cmd_argocd_get_app]]
- [[cmd_argocd_flush_cache]]
- [[playbook_argocd_oci_helm_dependency_troubleshooting]]