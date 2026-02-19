---
type: atomic_command
tool: kubectl
hop_level: local
target_service: vault-secrets-operator
requires_tunnel: true
tags: #atomic #kubectl #vault
---

# Force Vault Secret Rotation

## 🎯 Intent
Force the Vault Secrets Operator to immediately re-fetch secrets from Vault, bypassing the refresh interval. Useful when rotating Git tokens or updating credentials.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
kubectl annotate vaultstaticsecret <secret_name> -n argocd secrets.hashicorp.com/vault-force-rotation="$(date +%s)" --overwrite
```

### Placeholders
- `<secret_name>` — Name of the `VaultStaticSecret` resource

---

## ✅ Verification
```bash
kubectl get events -n argocd --sort-by='.lastTimestamp' -w | grep SecretRotated
```
Expected signal:
- `SecretRotated` event appearing for the target secret.

---

## 🔗 Related
- [[pb-argocd-sync-failure-triage]]
