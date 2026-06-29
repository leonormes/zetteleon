---
created: 2026-02-22 17:01:05+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14 11:10:10+00:00
requires_tunnel: false
status: active
tags:
- argocd
- cmd
- debug
- drift
- sync
target_service: argocd
title: cmd_kubectl_argocd_get_failing_resources
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-failing-resources
---

## Get ArgoCD Failing Resources

### 🎯 Intent

Print every individually tracked Kubernetes resource managed by an ArgoCD application and display its specific Sync and Health state. This is exactly how you find out _which_ specific ConfigMap or Service is causing the parent application to show `OutOfSync`.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{range .status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application

---

### ✅ Verification

- Expected Output: A line-by-line list of resources. Look for `sync=OutOfSync` or `health=Degraded`.

### 💥 Failure Mode Analysis

- Symptom: `error: parse error: unclosed action` or output formatting groups together on one line.
  - Fix: Depending on the OS (Mac vs Linux), the `\n` carriage return inside `jsonpath` might need double escaping (`\\n`) or literal strings instead.