---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, logs, auth, helm]
---

# Stream ArgoCD Repo-Server Auth Logs

## 🎯 Intent
Stream the logs from the active `argocd-repo-server` pods specifically filtering for authentication, registry, or helm resolution warnings and errors. Crucial during live validation of dependency fetching.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server --tail=50 -f \
  | grep -iE --line-buffered 'auth|401|login|registry|helm'
```

---

## ✅ Verification
- Expected Output: Warning or Information logs emitted anytime ArgoCD communicates with external Git or OCI endpoints during manifest generation.
- Hit `CTRL+C` to terminate the stream.

## 💥 Failure Mode Analysis
- **Symptom:** `No resources found` or silent output despite known sync activity.
  - **Fix:** The pod label (`app.kubernetes.io/name=argocd-repo-server`) might be styled differently in this cluster distribution. Use `kubectl get pods -n argocd --show-labels` to find the correct selector.
