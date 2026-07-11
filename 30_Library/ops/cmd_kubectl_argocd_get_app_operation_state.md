---
created: 2026-02-22 16:52:48+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04 10:50:42+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-app-operation-state
requires_tunnel: false
tags:
- argocd
- cmd
- debug
- error
- sync
target_service: argocd
title: cmd_kubectl_argocd_get_app_operation_state
tool: kubectl
prodos:
  kind: ops
  lifecycle: active
---


## Get ArgoCD Application Operation State

### 🎯 Intent

Retrieve the exact error message from the last synchronization attempt of an ArgoCD Application, specifically useful for debugging "Unknown" sync states or `ComparisonError`.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{.status.operationState.message}'
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application

---

### ✅ Verification

- Expected Output: A string containing the error message (e.g., `failed to login to registry… 401: unauthorized`). If empty, the application hasn't attempted a sync recently or doesn't have an operation state.

### 💥 Failure Mode Analysis

- Symptom: `error: the server doesn't have a resource type "application"`
  - Fix: Ensure you are targeting a cluster where ArgoCD is installed and you have RBAC permissions for the `argoproj.io/v1alpha1` group.

---

### 🔗 Related

- [[cmd_kubectl_argocd_get_app_source]]
