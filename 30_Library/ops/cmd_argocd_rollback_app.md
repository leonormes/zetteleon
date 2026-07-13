---
created: 2026-02-21T15:05:08+00:00
hop_level: local
modified: 2026-07-13T08:52:59+00:00
permalink: llmeon/30-library/ops/cmd-argocd-rollback-app
requires_tunnel: true
tags: [argocd, atomic, recovery, rollback]
target_service: argocd
title: cmd_argocd_rollback_app
tool: argocd
---

## Rollback ArgoCD Application

### 🎯 Intent

Reverts the application state to a previous successful revision ID.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
argocd app rollback <APP_NAME> <REVISION_ID>
```

#### Placeholders

- `<APP_NAME>`—The name of the ArgoCD application.
- `<REVISION_ID>`—The specific ID or relative index (e.g., 0 for previous).

---

### ✅ Verification

```bash
argocd app get <APP_NAME>
```

---

### 🔗 Related

- [[cmd_argocd_sync_app]]
