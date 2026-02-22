---
type: command
tool: kubectl
hop_level: local
target_service: secret
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, kubectl, secrets, jsonpath, decode]
---

# Decode Specific Secret JSON Key

## 🎯 Intent
Decode a specific JSON payload assigned to a single key (like `auth.json`) embedded inside a Kubernetes secret using jsonpath, bypassing the need to decode the entire secret block conceptually.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

*Note the `\.` escaping required when jsonpath keys contain dots (like `auth.json`).*

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.auth\.json}' | base64 -d; echo
```

### Placeholders
- `<SECRET_NAME>` — Name of the Kubernetes secret.
- `<NAMESPACE>` — Target namespace.

---

## ✅ Verification
- Expected Output: The raw, decoded JSON payload corresponding to that single key, typically containing connection strings or API credentials.

## 💥 Failure Mode Analysis
- **Symptom:** Silent output or `error: jsonpath parse error`.
  - **Fix:** The key does not exist inside `.data`, or the escaping syntax `# ` is incorrect for your specific shell. You can also try `.data['auth.json']` notation if escaping fails.
