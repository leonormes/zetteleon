---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, appproject, describe, debug]
---

# Describe ArgoCD Application

## 🎯 Intent
Describe an ArgoCD application to view detailed sync error messages, the governing AppProject, and the source path fields. Critical for diagnosing registry access or AppProject source restrictions.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl describe application <APP_NAME> -n <NAMESPACE>
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application
- `<NAMESPACE>` — The namespace ArgoCD is installed in (usually `argocd`)

---

## ✅ Verification
- **Expected Output:** Look closely at `Status.Conditions` for `ComparisonError` messages, and the `Spec.Project` field to see which AppProject configures its boundaries.

## 💥 Failure Mode Analysis
- **Symptom:** `Error from server (NotFound): applications.argoproj.io "<APP_NAME>" not found`
  - **Fix:** Ensure you are in the correct cluster context and referencing the exact application name deployed in the ArgoCD namespace.
