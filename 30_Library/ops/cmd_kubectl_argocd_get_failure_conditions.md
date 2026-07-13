---
created: 2026-02-22T17:01:20+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-13T08:53:00+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-failure-conditions
requires_tunnel: false
tags: [argocd, cmd, conditions, error, sync]
target_service: argocd
title: cmd_kubectl_argocd_get_failure_conditions
tool: kubectl
---

## Get ArgoCD Application Failure Conditions

### 🎯 Intent

Show the overarching application conditions (e.g., `SyncError`, `ComparisonError`) and the specific degraded reasoning. This gets straight to the "Why did the sync fail?" without reading large YAML manifests.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{range .status.conditions[*]}{.type}{"  "}{.reason}{"  "}{.message}{"\n"}{end}'
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application

---

### ✅ Verification

- Expected Output: A clear message detailing the exact problem:

  ```text
  SyncError  Failed sync attempt...
  ComparisonError  helm registry login failed...
  ```

### 💥 Failure Mode Analysis

- Symptom: Blank output.
  - Fix: The application currently has no active error conditions. The `sync.status` may be `Synced` and `health.status` may be `Healthy`. Use [[cmd_kubectl_argocd_list_applications_table]] to verify its high-level state.
