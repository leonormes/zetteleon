---
created: 2026-02-22 16:57:52+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04 10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-logs-repo-server
requires_tunnel: false
tags:
- argocd
- auth
- cmd
- helm
- logs
target_service: argocd
title: cmd_kubectl_argocd_logs_repo_server
tool: kubectl
prodos:
  kind: ops
  lifecycle: active
---


## Stream ArgoCD Repo-Server Auth Logs

### 🎯 Intent

Stream the logs from the active `argocd-repo-server` pods specifically filtering for authentication, registry, or helm resolution warnings and errors. Crucial during live validation of dependency fetching.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server --tail=50 -f \
  | grep -iE --line-buffered 'auth|401|login|registry|helm'
```

---

### ✅ Verification

- Expected Output: Warning or Information logs emitted anytime ArgoCD communicates with external Git or OCI endpoints during manifest generation.
- Hit `CTRL+C` to terminate the stream.

### 💥 Failure Mode Analysis

- Symptom: `No resources found` or silent output despite known sync activity.
  - Fix: The pod label (`app.kubernetes.io/name=argocd-repo-server`) might be styled differently in this cluster distribution. Use `kubectl get pods -n argocd --show-labels` to find the correct selector.
