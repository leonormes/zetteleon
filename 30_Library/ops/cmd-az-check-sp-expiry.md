---
created: 2026-02-17 12:03:31+00:00
hop_level: local
modified: 2026-03-14 11:10:11+00:00
tags:
- atomic
- azure
- identity
target_service: identity
title: cmd-az-check-sp-expiry
tool: az
type: atomic_command
permalink: llmeon/30-library/ops/cmd-az-check-sp-expiry
---

## Check Service Principal Credential Expiry

### 🎯 Intent

Verify if the Service Principal (App ID) being used for ACR or other services has an expired secret or certificate.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (authenticated to AZ CLI)

---

### ⚡ Action

```bash
az ad app credential list --id "<APP_ID>" --output table
```

#### Placeholders

- `<APP_ID>`—The Application (Client) ID of the Service Principal.

---

### ✅ Verification

Check the `EndDate` column. If it is in the past, the secret is expired and must be rotated in Azure AD and Vault.

---

### 🔗 Related

- [[pb-argocd-oci-auth-fail]]