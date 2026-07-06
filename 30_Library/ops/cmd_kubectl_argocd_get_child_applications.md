---
created: 2026-02-22T17:01:23+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04T10:50:42+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-child-applications
requires_tunnel: false
status: active
tags: [app-of-apps, argocd, child, cmd]
target_service: argocd
title: cmd_kubectl_argocd_get_child_applications
tool: kubectl
type: command
---

## List ArgoCD Child Applications

### 🎯 Intent

Identify and list all child applications generated and tracked by an "app-of-apps" parent pattern. Parent apps can show as `Degraded` even when their own immediate manifests are healthy, precisely because one of their generated children is out of sync.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get application <PARENT_APP_NAME> -n argocd -o jsonpath='{range .status.resources[?(@.kind=="Application")]}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'
```

#### Placeholders

- `<PARENT_APP_NAME>`—Name of the Parent ArgoCD Application

---

### ✅ Verification

- Expected Output: A list of every child application and its sync/health status. Ensure none are `OutOfSync` or `Degraded`.

### 💥 Failure Mode Analysis

- Symptom: Blank output.
  - Fix: The target application is not an app-of-apps pattern. It does not spawn other `Application` Custom Resources.
