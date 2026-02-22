---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, sync, error, conditions]
---

# Get ArgoCD Application Failure Conditions

## 🎯 Intent
Show the overarching application conditions (e.g., `SyncError`, `ComparisonError`) and the specific degraded reasoning. This gets straight to the "Why did the sync fail?" without reading large YAML manifests.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{range .status.conditions[*]}{.type}{"  "}{.reason}{"  "}{.message}{"\n"}{end}'
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
- Expected Output: A clear message detailing the exact problem:
  ```text
  SyncError  Failed sync attempt...
  ComparisonError  helm registry login failed...
  ```

## 💥 Failure Mode Analysis
- **Symptom:** Blank output.
  - **Fix:** The application currently has no active error conditions. The `sync.status` may be `Synced` and `health.status` may be `Healthy`. Use [[cmd_kubectl_argocd_list_applications_table]] to verify its high-level state.
