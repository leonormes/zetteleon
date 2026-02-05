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