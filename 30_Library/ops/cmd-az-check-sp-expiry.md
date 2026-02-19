---
type: atomic_command
tool: az
hop_level: local
target_service: identity
tags: #atomic #azure #identity
---

# Check Service Principal Credential Expiry

## 🎯 Intent
Verify if the Service Principal (App ID) being used for ACR or other services has an expired secret or certificate.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (authenticated to AZ CLI)

---

## ⚡ Action

```bash
az ad app credential list --id "<APP_ID>" --output table
```

### Placeholders
- `<APP_ID>` — The Application (Client) ID of the Service Principal.

---

## ✅ Verification
Check the `EndDate` column. If it is in the past, the secret is expired and must be rotated in Azure AD and Vault.

---

## 🔗 Related
- [[pb-argocd-oci-auth-fail]]
