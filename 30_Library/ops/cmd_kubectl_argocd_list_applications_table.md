---
created: 2026-02-22T17:00:59+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04T10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-list-applications-table
requires_tunnel: false
status: active
tags: [argocd, cmd, health, list, sync]
target_service: argocd
title: cmd_kubectl_argocd_list_applications_table
tool: kubectl
type: command
---

## List ArgoCD Applications Table

### 🎯 Intent

Get a concise, tabular view of all ArgoCD Applications in a namespace, highlighting only their Name, Sync Status, and Health Status. This removes the clutter of standard `kubectl get apps` output.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status --no-headers
```

---

### ✅ Verification

- Expected Output:

  ```text
  payment-service-prod   Synced       Healthy
  ff-hie-test-34         OutOfSync    Degraded
  ```

### 💥 Failure Mode Analysis

- Symptom: Silent output.
  - Fix: Ensure you are actively targeting the namespace where ArgoCD Application CRs are deployed (commonly `argocd`, but could be a tenant namespace).
