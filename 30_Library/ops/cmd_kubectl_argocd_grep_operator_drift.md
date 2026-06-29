---
created: 2026-02-22 17:01:33+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14 11:10:10+00:00
requires_tunnel: false
status: active
tags:
- argocd
- cmd
- drift
- metadata
- operator
target_service: argocd
title: cmd_kubectl_argocd_grep_operator_drift
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-grep-operator-drift
---

## Grep Resource for Operator Metadata Drift

### 🎯 Intent

Filter a live Kubernetes resource manifest to find unexpected metadata (annotations/labels) injected by external operators (like Cert-Manager or External-Secrets) which causes ArgoCD to perpetually report "drift" against the pure Git configuration in its repository.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get <KIND> -n <NAMESPACE> <NAME> -o yaml | grep -E -n 'annotations:|labels:|image:|env:|configMapRef:|secretRef:'
```

#### Placeholders

- `<KIND>`—The Kubernetes type (e.g., `Certificate`, `Deployment`, `Secret`).
- `<NAMESPACE>`—Target namespace.
- `<NAME>`—Name of the resource reporting anomalous drift.

---

### ✅ Verification

- Compare the output returned from the live cluster query against the raw YAML file in your Git repository. If extra labels or annotations exist natively on the cluster resource, that is the cause of the continuous drift.

### 💥 Failure Mode Analysis

- Symptom: The manifest matches Git perfectly but still shows `OutOfSync`.
  - Fix: An immutable field may be failing reconciliation entirely. Check the overarching application failure conditions using [[cmd_kubectl_argocd_get_failure_conditions]].