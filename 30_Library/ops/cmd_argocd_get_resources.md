---
created: 2026-02-21 15:05:07+00:00
hop_level: local
modified: 2026-03-14 11:10:11+00:00
requires_tunnel: true
tags:
- argocd
- atomic
- resources
- triage
target_service: argocd
title: cmd_argocd_get_resources
tool: argocd
type: atomic_command
permalink: llmeon/30-library/ops/cmd-argocd-get-resources
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