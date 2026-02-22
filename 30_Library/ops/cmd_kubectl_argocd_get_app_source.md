---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, source, debug]
---

# Get ArgoCD Application Source

## 🎯 Intent
Extract the source configuration of an ArgoCD Application, specifically to confirm the Helm chart source or the OCI registry it is attempting to pull from.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{.spec.source}' | jq .
```

### Placeholders
- `<APP_NAME>` — Name of the ArgoCD Application

---

## ✅ Verification
- Expected Output: A JSON object detailing the `repoURL`, `targetRevision`, and `chart` or `path` fields. Look for `repoURL` pointing to an OCI registry to confirm the app pulls from it.

## 💥 Failure Mode Analysis
- **Symptom:** Blank output or `parse error: Invalid numeric literal`
  - **Fix:** Ensure `jq` is installed and the JSONPath expression is returning valid JSON.

---

## 🔗 Related
- [[cmd_kubectl_argocd_get_app_operation_state]]
