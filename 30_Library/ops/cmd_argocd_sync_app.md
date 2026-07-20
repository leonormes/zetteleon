---
created: 2026-02-21T15:05:07+00:00
hop_level: local
modified: 2026-07-20T16:33:38+00:00
permalink: llmeon/30-library/ops/cmd-argocd-sync-app
requires_tunnel: true
tags: [argocd, atomic, mutation, sync]
target_service: argocd
title: cmd_argocd_sync_app
tool: argocd
---

## Sync ArgoCD Application

### 🎯 Intent

Manually triggers a sync operation to apply the Git state to the cluster.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
argocd app sync <APP_NAME> --prune --retry-limit 3
```

#### Placeholders

- `<APP_NAME>`—The name of the ArgoCD application.

---

### ✅ Verification

```bash
argocd app wait <APP_NAME>
```

Expected signal:

- Application reaches `Synced` status.

---

### 🧠 Failure Modes

- `Sync Failed`: Check for immutable field violations or admission webhook blocks.

---

### 🔗 Related

- [[cmd_argocd_rollback_app]]
- [[cmd_argocd_refresh_app]]
