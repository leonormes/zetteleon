---
created: 2026-02-21 15:05:07+00:00
hop_level: local
modified: 2026-07-04 10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-get-pods
requires_tunnel: true
tags:
- atomic
- kubectl
- pods
- verification
target_service: k8s
title: cmd_kubectl_get_pods
tool: kubectl
prodos:
  kind: ops
---


## Get Pods Wide Output

### 🎯 Intent

Confirms pod status, node placement, and restart counts to verify deployment health.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get pods -n <NAMESPACE> -l <LABEL_SELECTOR> -o wide
```

#### Placeholders

- `<NAMESPACE>`—target namespace
- `<LABEL_SELECTOR>`—label filter (e.g., `app=my-service`)

---

### ✅ Verification

- `STATUS` should be `Running`.
- `RESTARTS` should be 0 or stable.

---

### 🔗 Related

- [[cmd_kubectl_get_events]]
