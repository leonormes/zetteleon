---
created: 2026-02-22T17:01:03+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-20T16:33:38+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-annotate-hard-refresh
requires_tunnel: false
tags: [argocd, cache, cmd, refresh, sync]
target_service: argocd
title: cmd_kubectl_argocd_annotate_hard_refresh
tool: kubectl
---

## Annotate Hard Refresh of ArgoCD Application

### 🎯 Intent

Force a hard refresh of an ArgoCD application strictly via Kubernetes annotations. This tells the Argo Controller to disregard the cached generator state and fully re-clone/re-evaluate the source manifests. Crucial when debugging GitOps drift or stale repository secrets.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl annotate application <APP_NAME> -n argocd argocd.argoproj.io/refresh=hard --overwrite
```

#### Placeholders

- `<APP_NAME>`—Name of the ArgoCD Application

---

### ✅ Verification

- The ArgoCD controller consumes this annotation almost instantly and removes it. To verify it worked, check the application conditions for a cleared "cached" error or view the latest operation state.
- Alternatively run a `kubectl get application <APP_NAME> -n argocd -w` while annotating.

### 💥 Failure Mode Analysis

- Symptom: Nothing happens; sync status remains identical and errors don't update.
  - Fix: If the `repo-server` pod is in a CrashLoop or uncontactable by the application-controller, the refresh request will hang or be silently ignored until connectivity is restored.
