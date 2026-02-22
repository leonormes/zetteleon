---
type: command
tool: kubectl
hop_level: local
target_service: deployment
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, kubectl, rollout, restart, pods]
---

# Rollout Restart Deployment

## 🎯 Intent
Force a Kubernetes deployment to terminate its current pods and spin up entirely new ones without altering the actual Deployment manifest configuration. Crucial when external dependencies (like an Auth0 scope misconfiguration or a Vault payload rotate) are fixed out-of-band and the application pods must pull the new state.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl rollout restart deployment <DEPLOYMENT_NAME> -n <NAMESPACE>
```

### Placeholders
- `<DEPLOYMENT_NAME>` — Name of the target Deployment.
- `<NAMESPACE>` — Target namespace.

---

## ✅ Verification
- `kubectl rollout status deployment <DEPLOYMENT_NAME> -n <NAMESPACE>`
- Or simply watch the pods terminate and recreate: `kubectl get pods -n <NAMESPACE> -w`

## 💥 Failure Mode Analysis
- **Symptom:** `error: the server doesn't have a resource type "deployment"`.
  - **Fix:** Your kubectl context might be borked, or you typed `deployments` when the server API strictly requires singular syntax depending on your shell alias. Check namespace existence and spellings.
