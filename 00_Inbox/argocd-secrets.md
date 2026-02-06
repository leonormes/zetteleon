---
created: 2026-02-05T19:55:23+00:00
modified: 2026-02-05T20:00:28+00:00
title: argocd-secrets
---

```json
{
  "admin_password": "", // htpasswd -nbBC 10 "" <replace-me-with-password> | tr -d ':
' | sed 's/$2y/$2a/'
  "gitlab_deploy_token_password": "",
  "gitlab_deploy_token_username": "",
  "sso_azure_client_secret": "",
  "server_secret_key": "", // openssl rand -base64 32
}
```
