---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
tags: [atomic, argocd, diff, triage]
---

# Diff ArgoCD Application

## 🎯 Intent
Compares the desired state in Git with the live state in the Kubernetes cluster to identify specific drifts.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
argocd app diff <APP_NAME>
```

### Placeholders
- `<APP_NAME>` — The name of the ArgoCD application.

---

## ✅ Verification
- Review the output for `+` (added) or `-` (removed) fields.
- If output is empty, the states are perfectly aligned.

---

## 🧠 Failure Modes
- `ComparisonError`: Indicates an issue rendering manifests or connection issues with the cluster.

---

## 🔗 Related
- [[cmd_argocd_get_app]]
- [[kb_argocd_sync_failure_causes]]