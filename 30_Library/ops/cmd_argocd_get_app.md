---
created: 2026-02-21T15:05:07+00:00
hop_level: local
modified: 2026-07-04T10:50:43+00:00
permalink: llmeon/30-library/ops/cmd-argocd-get-app
requires_tunnel: true
tags: [argocd, atomic, status, triage]
target_service: argocd
title: cmd_argocd_get_app
tool: argocd
type: atomic_command
---

## Get ArgoCD Application Status

### 🎯 Intent

Retrieves the current sync and health status of an ArgoCD application, including the last sync result and any high-level errors.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

Active requirements:

- [x] SSH tunnel active
- [x] ArgoCD login active

---

### ⚡ Action

```bash
argocd app get <APP_NAME>
```

#### Placeholders

- `<APP_NAME>`—The name of the ArgoCD application.

---

### ✅ Verification

```bash
argocd app get <APP_NAME> -o json | jq '{sync: .status.sync.status, health: .status.health.status}'
```

Expected signal:

- `sync`: "Synced"
- `health`: "Healthy"

---

### 🧠 Failure Modes

- `Permission Denied`: Check your ArgoCD CLI authentication (`argocd login`).
- `Application Not Found`: Verify the `<APP_NAME>` exists in the current ArgoCD context.

---

### 🔗 Related

- [[playbook_argocd_sync_failure_triage]]
- [[cmd_argocd_diff_app]]
