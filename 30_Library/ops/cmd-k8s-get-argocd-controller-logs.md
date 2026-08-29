---
created: 2026-02-16T11:46:04+00:00
hop_level: local
modified: 2026-08-29T09:36:47+00:00
permalink: llmeon/30-library/ops/cmd-k8s-get-argocd-controller-logs
requires_tunnel: true
tags: [argocd, atomic, kubectl]
target_service: argocd
title: cmd-k8s-get-argocd-controller-logs
tool: kubectl
---

## Get ArgoCD Application Controller Logs

### 🎯 Intent

View the logs of the application controller to diagnose synchronization issues, authentication failures, or cluster connection problems.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
kubectl logs -n argocd statefulset/argocd-application-controller --tail=100
```

#### Filtered for Application

```bash
kubectl logs -n argocd statefulset/argocd-application-controller --tail=200 | grep -E "<app_name>|authentication|Access denied"
```

#### Placeholders

- `<app_name>`—Name of the application to filter logs for

---

### ✅ Verification

Look for:

- `authentication required`: Indicates repository credential issues.
- `Failed to load target state`: Network or Git access issues.

---

### 🔗 Related

- [[cmd-k8s-describe-argocd-app]]
