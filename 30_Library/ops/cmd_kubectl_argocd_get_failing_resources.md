---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, sync, drift, debug]
---

# Get ArgoCD Failing Resources

## 🎯 Intent
Print every individually tracked Kubernetes resource managed by an ArgoCD application and display its specific Sync and Health state. This is exactly how you find out *which* specific ConfigMap or Service is causing the parent application to show `OutOfSync`.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{range .status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
- Expected Output: A line-by-line list of resources. Look for `sync=OutOfSync` or `health=Degraded`.

## 💥 Failure Mode Analysis
- **Symptom:** `error: parse error: unclosed action` or output formatting groups together on one line.
  - **Fix:** Depending on the OS (Mac vs Linux), the `\n` carriage return inside `jsonpath` might need double escaping (`\\n`) or literal strings instead. 
