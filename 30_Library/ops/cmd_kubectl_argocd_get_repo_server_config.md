---
created: 2026-02-22T16:57:44+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-08-13T10:53:55+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-repo-server-config
requires_tunnel: false
tags: [argocd, cmd, config, repo-server, volume]
target_service: argocd
title: cmd_kubectl_argocd_get_repo_server_config
tool: kubectl
---

## Get ArgoCD Repo-Server Deployment Config

### 🎯 Intent

Introspect the runtime configuration, environment variables, and volume mounts of the ArgoCD `repo-server` deployment. Primarily useful when checking how Docker configurations (`.dockerconfigjson`) or Helm registry settings map into the pod environment.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get deployment argocd-repo-server -n argocd -o yaml | grep -A 5 -i 'registry\|HELM_\|DOCKER'
kubectl get deployment argocd-repo-server -n argocd -o yaml | grep -A 10 'volumeMounts'
```

---

### ✅ Verification

- Expected Output: Configuration subsets from the deployment manifest containing lines indicating standard configurations or dynamically mounted config folders. If `HELM_CACHE_HOME` or injected TLS certificates are defined, they appear here.

### 💥 Failure Mode Analysis

- Symptom: Silent output.
  - Fix: The Deployment may have a different name in your cluster (e.g., `argo-cd-repo-server`). List the deployments and correct the name `kubectl get deploy -n argocd`.

---

## Related

- [[cmd_kubectl_argocd_exec_cat_helm_registry_config]]
- [[cmd_kubectl_restart_argocd_repo_server]]
- [[cmd_kubectl_argocd_exec_helm_registry_login]]
- [[FITFILE Platform—ArgoCD + Helm Deployment Wiki]]
- [[cmd_kubectl_argocd_logs_repo_server]]
