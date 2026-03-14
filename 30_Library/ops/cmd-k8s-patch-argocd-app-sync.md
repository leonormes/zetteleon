---
created: 2026-02-16T11:46:04+00:00
hop_level: local
modified: 2026-03-14T11:10:11+00:00
requires_tunnel: true
tags: [argocd, atomic, kubectl]
target_service: argocd
title: cmd-k8s-patch-argocd-app-sync
tool: kubectl
type: atomic_command
---

## Force Sync ArgoCD Application (kubectl)

### 🎯 Intent

Manually trigger a reconciliation (sync) of an application with its Git source using a kubectl patch. Use this when auto-sync is disabled or stuck.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
kubectl patch application <app_name> -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'
```

#### Placeholders

- `<app_name>`—Name of the ArgoCD application

---

### ✅ Verification

```bash
kubectl get application <app_name> -n argocd -w
```

Expected signal:

- `SYNC STATUS` transitions to `Synced`

---

### 🔗 Related

- [[cmd-k8s-describe-argocd-app]]
