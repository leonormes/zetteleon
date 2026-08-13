---
created: 2026-02-22T16:56:46+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-08-13T10:53:54+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-describe-application
requires_tunnel: false
tags: [appproject, argocd, cmd, debug, describe]
target_service: argocd
title: cmd_kubectl_argocd_describe_application
tool: kubectl
---

## Describe ArgoCD Application

### 🎯 Intent

Describe an ArgoCD application to view detailed sync error messages, the governing AppProject, and the source path fields. Critical for diagnosing registry access or AppProject source restrictions.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl describe application <APP_NAME> -n <NAMESPACE>
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application
- `<NAMESPACE>`—The namespace ArgoCD is installed in (usually `argocd`)

---

### ✅ Verification

- Expected Output: Look closely at `Status.Conditions` for `ComparisonError` messages, and the `Spec.Project` field to see which AppProject configures its boundaries.

### 💥 Failure Mode Analysis

- Symptom: `Error from server (NotFound): applications.argoproj.io "<APP_NAME>" not found`
  - Fix: Ensure you are in the correct cluster context and referencing the exact application name deployed in the ArgoCD namespace.
