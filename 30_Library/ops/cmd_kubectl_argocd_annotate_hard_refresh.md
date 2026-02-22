---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, refresh, cache, sync]
---

# Annotate Hard Refresh of ArgoCD Application

## 🎯 Intent
Force a hard refresh of an ArgoCD application strictly via Kubernetes annotations. This tells the Argo Controller to disregard the cached generator state and fully re-clone/re-evaluate the source manifests. Crucial when debugging GitOps drift or stale repository secrets.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl annotate application <APP_NAME> -n argocd argocd.argoproj.io/refresh=hard --overwrite
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
- The ArgoCD controller consumes this annotation almost instantly and removes it. To verify it worked, check the application conditions for a cleared "cached" error or view the latest operation state.
- Alternatively run a `kubectl get application <APP_NAME> -n argocd -w` while annotating.

## 💥 Failure Mode Analysis
- **Symptom:** Nothing happens; sync status remains identical and errors don't update.
  - **Fix:** If the `repo-server` pod is in a CrashLoop or uncontactable by the application-controller, the refresh request will hang or be silently ignored until connectivity is restored.
