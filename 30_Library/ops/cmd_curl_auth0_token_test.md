---
created: 2026-02-22T17:06:45+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-08-13T10:53:54+00:00
permalink: llmeon/30-library/ops/cmd-curl-auth0-token-test
requires_tunnel: false
tags: [auth0, cmd, curl, isolation, m2m, token]
target_service: auth0
title: cmd_curl_auth0_token_test
tool: curl
---

## Test Auth0 M2M Token Exchange via cURL

### 🎯 Intent

Execute a manual `curl` token exchange directly against an Auth0 tenant endpoint using specific Client credentials. This isolates the M2M authentication request completely from Kubernetes or application logic, proving definitively whether a client secret is authorized for the requested tenant and audience.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with internet access)

---

### ⚡ Action

```bash
curl --request POST --url "https://<AUTH0_TENANT>.auth0.com/oauth/token" \
  --header 'content-type: application/json' \
  --data '{"client_id":"<CLIENT_ID>", "client_secret":"<CLIENT_SECRET>", "audience":"https://<AUTH0_TENANT>.auth0.com/api/v2/", "grant_type":"client_credentials"}'
```

#### Placeholders

- `<AUTH0_TENANT>`—e.g. `fitfile-prod.eu` or `fitfile-test.eu`
- `<CLIENT_ID>`—Extracted from Kubernetes secret or Vault.
- `<CLIENT_SECRET>`—Extracted from Kubernetes secret or Vault.
- `audience`—Must match the intended audience exactly (often the Management API or a custom API identifier).

---

### ✅ Verification

- Expected Output: An HTTP `200 OK` response payload containing an `access_token` JWT.

### 💥 Failure Mode Analysis

- Symptom: `401 Unauthorized`.
  - Fix: The Client ID or Client Secret is completely incorrect. Check your copy/paste or Vault payload.
- Symptom: `403 Forbidden` or `access_denied` with reasoning about tenant/audience.
  - Fix: The credential pair is valid for _an_ Auth0 tenant, but not the one you just addressed in the URL. This signifies a classic tenant mismatch (e.g. Test credentials firing against the Prod endpoint).
