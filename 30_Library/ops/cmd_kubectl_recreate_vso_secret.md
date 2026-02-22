---
type: command
tool: kubectl
service: vso
risk: high
tags: [vso, k8s, mutation, recovery]
---

# Recreate VSO Managed Secret

## 🎯 Intent
Forces VSO to recreate a secret with fresh credentials by deleting the current instance. Use this when credentials are stale or manually corrupted.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
# Delete the secret
kubectl delete secret <SECRET_NAME> -n <NAMESPACE>

# Watch for automatic recreation
kubectl get secret -n <NAMESPACE> -w | grep <SECRET_NAME>
```

### Placeholders
- `<SECRET_NAME>` — The name of the Kubernetes secret.
- `<NAMESPACE>` — The namespace.

---

## ✅ Verification
- Check the `creationTimestamp` of the new secret.

---

## 🧠 Failure Modes
- `Secret does not reappear`: Check VSO operator logs; the `VaultAuth` or `VaultConnection` may be failing.

---

## 🔗 Related
- [[cmd_kubectl_patch_vso_overwrite]]
- [[playbook_vso_secret_debugging]]