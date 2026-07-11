---
created: 2026-02-21 15:05:07+00:00
hop_level: local
modified: 2026-07-04 10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-get-events
requires_tunnel: true
tags:
- atomic
- events
- kubectl
- triage
target_service: k8s
title: cmd_kubectl_get_events
tool: kubectl
prodos:
  kind: ops
---


## Get Namespace Events

### 🎯 Intent

Surfaces recent Kubernetes events to diagnose underlying resource issues like image pull errors or scheduling constraints.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get events -n <NAMESPACE> --sort-by='.lastTimestamp'
```

#### Placeholders

- `<NAMESPACE>`—target namespace

---

### ✅ Verification

- Look for `Warning` type events in the last 10–15 minutes.

---

### 🔗 Related

- [[cmd_kubectl_get_pods]]
- [[playbook_argocd_sync_failure_triage]]
