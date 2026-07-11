---
created: 2026-02-16 11:46:04+00:00
hop_level: local
modified: 2026-07-04 10:50:44+00:00
permalink: llmeon/30-library/ops/cmd-k8s-get-argocd-apps
prerequisites:
- - - cmd-ssh-bastion-tunnel
requires_tunnel: true
tags:
- argocd
- atomic
- kubectl
target_service: argocd
title: cmd-k8s-get-argocd-apps
tool: kubectl
prodos:
  kind: ops
---


## List ArgoCD Applications

### 🎯 Intent

Get a high-level overview of all applications managed by ArgoCD, including their sync and health status.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)
- [ ] Bastion host
- [ ] Inside cluster

Active requirements:

- [x] KUBECONFIG set
- [x] SSH tunnel to cluster API active

---

### ⚡ Action

```bash
kubectl get applications -n argocd
```

#### Table View (Recommended)

```bash
kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status --no-headers
```

---

### ✅ Verification

Expected signal:

- List of applications with `Synced` and `Healthy` status.

---

### 🔗 Related

- [[cmd-k8s-describe-argocd-app]]
