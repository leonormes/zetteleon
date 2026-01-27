---
created: 2026-01-27T11:38:36+00:00
modified: 2026-01-27T12:24:36+00:00
---
# Vault Secrets: cuh-prod-1 Deployment

## KV Tree Structure for `/v1/admin/deployments/cuh-prod-1/secrets/data/`

```
deployments/cuh-prod-1/secrets/
├── application (20 keys)
│   ├── auth0_audience
│   ├── auth0_client_id
│   ├── auth0_client_secret
│   ├── auth0_frontend_client_id
│   ├── auth0_frontend_client_secret
│   ├── fitfile_tenant_pkcs8.key
│   ├── fitfile_tenant_public.crt
│   ├── mesh_client_cert
│   ├── mesh_client_key
│   ├── mesh_hash_secret
│   ├── mesh_mailbox_password
│   ├── mongodb_password
│   ├── mongodb_replica_set_key
│   ├── mongodb_username
│   ├── mutating_proxy_webhook_tls_crt
│   ├── mutating_proxy_webhook_tls_key
│   ├── postgresql_password
│   ├── postgresql_username
│   ├── s3_access_key_id
│   ├── s3_secret_access_key
│   ├── spicedb_pre_shared_key
│   └── ude_key
│
├── argo-workflows (2 keys)
│   ├── postgresql_password
│   └── postgresql_username
│
├── argocd (5 keys)
│   ├── admin_password
│   ├── gitlab_deploy_token_password
│   ├── gitlab_deploy_token_username
│   ├── server_secret_key
│   └── unhashed_admin_password
│
├── cloudflare (1 key)
│   └── api_token
│
├── hutch (7 keys)
│   ├── bunny_database_password
│   ├── bunny_database_username
│   ├── bunny_relay_password
│   ├── bunny_relay_username
│   ├── ca.pem
│   ├── intermediate.crt
│   └── root.crt
│
├── monitoring (9 keys)
│   ├── loki_host
│   ├── loki_password
│   ├── loki_username
│   ├── prometheus_host
│   ├── prometheus_password
│   ├── prometheus_username
│   ├── tempo_host
│   ├── tempo_password
│   └── tempo_username
│
├── spicedb (3 keys)
│   ├── postgresql_password
│   ├── postgresql_username
│   └── spicedb_preshared_key
│
└── thehyve (0 keys - empty)
```

## Policies Applied

### Current Token Policies
The `hcp-root` policy grants **full access** to all paths:

```hcl
path "*" {     
    capabilities = ["sudo","read","create","update","delete","list","patch","subscribe"]
    subscribe_event_types = ["*"]
}
```

### Capabilities for Each Secret Path
All secrets under `deployments/cuh-prod-1/secrets/` have **identical capabilities** due to the wildcard `hcp-root` policy:

- **Data path**: `create, delete, list, patch, read, subscribe, sudo, update`
- **Metadata path**: `create, delete, list, patch, read, subscribe, sudo, update`

### Other Relevant Policies in Namespace
The following policies exist in the `admin` namespace that could be assigned to other service accounts:

- **`argocd-secrets-lca-prd-2`**: Read-only access to `deployments/lca-prd-2/secrets/data/*`
- **`lca-prd-2-read`**: Read access to lca-prd-2 deployment secrets
- **`acr-reader`**: Azure Container Registry credentials access
- **`vso-auth-policy-operator`**: Vault Secrets Operator transit encryption access
- **`admin`**: System health checks and ACL policy management
- **`engine-policy`**: Secrets engine mounting capabilities
- **`tester`**: Limited test environment access

## Notes

- No specific restrictive policies exist for the `cuh-prod-1` deployment path
- Access is currently controlled only by the root-level `hcp-root` policy
- The `thehyve` secret exists but contains no keys
- Most secrets follow a pattern of storing database credentials and service authentication tokens
- The `application` secret is the most comprehensive, containing Auth0, MongoDB, PostgreSQL, S3, and SpiceDB credentials

## Metadata

- **Namespace**: `admin`
- **Path**: `deployments/cuh-prod-1/secrets/`
- **KV Version**: v2
- **Total Secrets**: 8 (7 with data, 1 empty)
- **Date Generated**: 2026-01-27

```json
{
"spicedb_pre_shared_key": "y9GZCGDNcetUGG3v2nmRKC1j3k3BBZu8",
"postgresql_password": "yAGywP1K2sCKqSVDqlef2Gcq",
"postgresql_username": "postgres"
}
```

```json
{ 
"gitlab_deploy_token_password": "gldt-reWkBa7YUDD2ua7dgMxJ", "gitlab_deploy_token_username": "gitlab+deploy-token-11028822", "grafana_admin_password": "2mdctzntXUbq2xJmzRxYis3g",
"loki_password": "2mdctzntXUbq2xJmzRxYis3g",
"mongodb_password": "LMNTZ2KlCv3ubVpMheIvLPSy",
"mongodb_replica_set_key": "LMNTZ2KlCv3ubVpMheIvLPSy",
"mongodb_username": "root",
"postgresql_password": "yAGywP1K2sCKqSVDqlef2Gcq",
"postgresql_username": "postgres", 
"prometheus_password": "2mdctzntXUbq2xJmzRxYis3g", 
"s3_access_key_id": "ffadmin", 
"s3_secret_access_key": "asFeEfEr4TyTx40jzESbudpxyGgakuSr", 
"spicedb_pre_shared_key": "y9GZCGDNcetUGG3v2nmRKC1j3k3BBZu8", 
"tempo_password": "2mdctzntXUbq2xJmzRxYis3g", 
"ude_key": "5d8e83dd3c53c9b14674d1dff5eda210350790251076cb34583f2c05a781f2c4", "vm_admin_password": "?FXkVNUB!KPpRJas" }
```