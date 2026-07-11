---
created: 2026-02-21 15:05:07+00:00
hop_level: local
modified: 2026-07-04 10:50:42+00:00
permalink: llmeon/30-library/ops/cmd-argocd-get-resources
requires_tunnel: true
tags:
- argocd
- atomic
- resources
- triage
target_service: argocd
title: cmd_argocd_get_resources
tool: argocd
prodos:
  kind: ops
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
