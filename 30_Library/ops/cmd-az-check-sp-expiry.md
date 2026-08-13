---
created: 2026-02-17T12:03:31+00:00
hop_level: local
modified: 2026-08-13T10:53:53+00:00
permalink: llmeon/30-library/ops/cmd-az-check-sp-expiry
tags: [atomic, azure, identity]
target_service: identity
title: cmd-az-check-sp-expiry
tool: az
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
