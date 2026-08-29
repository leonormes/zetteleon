---
created: 2026-02-21T15:05:07+00:00
hop_level: local
modified: 2026-08-29T09:36:47+00:00
permalink: llmeon/30-library/ops/cmd-argocd-get-resources
requires_tunnel: true
tags: [argocd, atomic, resources, triage]
target_service: argocd
title: cmd_argocd_get_resources
tool: argocd
---

## List Managed Resources

### 🎯 Intent

Lists all Kubernetes resources managed by the ArgoCD application along with their individual sync and health statuses.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
argocd app resources <APP_NAME>
```

#### Placeholders

- `<APP_NAME>`—The name of the ArgoCD application.

---

### ✅ Verification

- Scan the `STATUS` and `HEALTH` columns for items that are not `Synced` or `Healthy`.

---

### 🔗 Related

- [[cmd_kubectl_get_events]]
- [[cmd_kubectl_get_pods]]
- [[cmd-argocd-get-sync-status]]
- [[Atomic Command Template]]
- [[cmd_argocd_get_app]]
- [[cmd_kubectl_argocd_get_failing_resources]]
- [[cmd_argocd_sync_app]]
