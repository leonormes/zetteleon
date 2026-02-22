---
type: command
tool: kubectl
hop_level: local
target_service: pod
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, kubectl, configmap, values, helm]
---

# Get Rendered ConfigMap Values

## 🎯 Intent
Inspect a deployment's ConfigMap and grep for specific strings (like `auth0` or `baseURL`) to extract the final rendered Helm values consumed by the pod. This exposes the "App Truth" vs the "Vault Truth".

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get configmap -n <NAMESPACE> <CONFIGMAP_NAME> -o yaml | grep -i '<SEARCH_TERM>' -n
```

### Placeholders
- `<NAMESPACE>` — Target namespace.
- `<CONFIGMAP_NAME>` — Name of the ConfigMap.
- `<SEARCH_TERM>` — The configuration key you suspect is wrong (e.g. `baseURL`, `auth0`, `host`).

---

## ✅ Verification
- Expected Output: The YAML line number and value injected by Helm. Compare this value to the environment credentials (e.g., if the URL says `PROD` but Vault serves `TEST` secrets, you found a parity mismatch).

## 💥 Failure Mode Analysis
- **Symptom:** Nothing returned.
  - **Fix:** The ConfigMap name is incorrect, or the value is injected via another mechanism (like raw Environment Variables on the Deployment manifest, rather than a ConfigMap). Use `kubectl get deploy` instead.
