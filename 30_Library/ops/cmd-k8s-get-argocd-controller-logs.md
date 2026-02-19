---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
tags: #atomic #kubectl #argocd
---

# Get ArgoCD Application Controller Logs

## 🎯 Intent
View the logs of the application controller to diagnose synchronization issues, authentication failures, or cluster connection problems.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
kubectl logs -n argocd statefulset/argocd-application-controller --tail=100
```

### Filtered for Application
```bash
kubectl logs -n argocd statefulset/argocd-application-controller --tail=200 | grep -E "<app_name>|authentication|Access denied"
```

### Placeholders
- `<app_name>` — Name of the application to filter logs for

---

## ✅ Verification
Look for:
- `authentication required`: Indicates repository credential issues.
- `Failed to load target state`: Network or Git access issues.

---

## 🔗 Related
- [[cmd-k8s-describe-argocd-app]]
