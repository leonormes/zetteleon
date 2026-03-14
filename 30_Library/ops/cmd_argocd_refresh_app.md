---
created: 2026-02-21T15:05:07+00:00
hop_level: local
modified: 2026-03-14T11:10:11+00:00
requires_tunnel: true
tags: [argocd, atomic, cache, refresh]
target_service: argocd
title: cmd_argocd_refresh_app
tool: argocd
type: atomic_command
---

## Hard Refresh ArgoCD Application

### 🎯 Intent

Forces ArgoCD to bypass its cache, re-download the Git repository, and re-calculate the comparison with the cluster.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
argocd app get <APP_NAME> --refresh --hard
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application

---

### ✅ Verification

- Observe the `Last Refresh` timestamp in the output to ensure it matches the current time.

---

### 🔗 Related

- [[cmd_argocd_get_app]]
- [[cmd_argocd_flush_cache]]
- [[playbook_argocd_oci_helm_dependency_troubleshooting]]
