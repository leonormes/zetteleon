---
created: 2026-02-16 11:46:04+00:00
hop_level: local
modified: 2026-03-14 11:10:11+00:00
prerequisites:
- - - cmd-ssh-bastion-tunnel
requires_tunnel: true
tags:
- argocd
- atomic
- kubectl
target_service: argocd
title: cmd-k8s-describe-argocd-app
tool: kubectl
type: atomic_command
permalink: llmeon/30-library/ops/cmd-k8s-describe-argocd-app
---

## Describe ArgoCD Application

### 🎯 Intent

Inspect the detailed status, metadata, and recent events of a specific ArgoCD application to identify why it is failing.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)
- [ ] Bastion host

---

### ⚡ Action

```bash
kubectl describe application <app_name> -n argocd
```

#### Placeholders

- `<app_name>`—Name of the ArgoCD application

---

### ✅ Verification

Look for:

- `Status.Sync.Status`: Should be `Synced`
- `Events`: Check for `FailedSync` or `SyncError`
- `Operation State.Message`: Detailed error message from the last sync attempt

---

### 🔗 Related

- [[cmd-k8s-get-argocd-apps]]
- [[cmd-k8s-get-argocd-controller-logs]]