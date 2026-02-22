---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, repo-server, config, volume]
---

# Get ArgoCD Repo-Server Deployment Config

## 🎯 Intent
Introspect the runtime configuration, environment variables, and volume mounts of the ArgoCD `repo-server` deployment. Primarily useful when checking how Docker configurations (`.dockerconfigjson`) or Helm registry settings map into the pod environment.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get deployment argocd-repo-server -n argocd -o yaml | grep -A 5 -i 'registry\|HELM_\|DOCKER'
kubectl get deployment argocd-repo-server -n argocd -o yaml | grep -A 10 'volumeMounts'
```

---

## ✅ Verification
- Expected Output: Configuration subsets from the deployment manifest containing lines indicating standard configurations or dynamically mounted config folders. If `HELM_CACHE_HOME` or injected TLS certificates are defined, they appear here.

## 💥 Failure Mode Analysis
- **Symptom:** Silent output.
  - **Fix:** The Deployment may have a different name in your cluster (e.g., `argo-cd-repo-server`). List the deployments and correct the name `kubectl get deploy -n argocd`.
