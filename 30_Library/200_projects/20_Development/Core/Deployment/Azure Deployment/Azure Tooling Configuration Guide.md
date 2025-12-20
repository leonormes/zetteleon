---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: Azure Tooling Configuration Guide
type: 
uid: 
updated: 
version: 
---

## Overview

These tasks must be performed by DevOps contributors responsible for the Central Services tooling. The terraform configuration for Central Services can be found in the Central Services repository.

## Vault Configuration

### Creating Vault Resources

First, we'll create empty secrets in vault:

1. Navigate to the Central Services repository
2. Change directory to `hcp/vault`
3. In `locals.tf`, add a new block to the deployments variable:

```hcl
"<replace_with_deployment_key>" = {
  secrets = tomap({
    "application" = {},
    "spicedb" = {},
    "cloudflare" = {}, # only needed if using cloudflare
    "monitoring" = {}, # for grafana creds
  })
}
```

4. Commit and push the changes to trigger the terraform plan in Terraform Cloud: HCP Terraform
5. A DevOps engineer must manually approve the apply on the Run page

### Populating Vault Secrets

The customer deployment will be referenced using a deployment-key - a short name FITFILE uses consistently throughout the infrastructure. For example, use "WM-Prod" instead of the full customer name.

#### Accessing Vault

Currently, SSO is not configured for the vault instance. To access vault:

1. Log into the HCP portal: <https://portal.cloud.hashicorp.com/>
2. Navigate to the vault dedicated instance
3. Generate an admin token

#### Secret Configuration

You'll need to create new versions of the following secrets:

##### Application Secrets

```json
{
  "cli_auth0_client_id": "",  // Leave blank - not needed
  "cli_auth0_client_secret": "",  // Leave blank - not needed
  "mesh_client_cert": "",  // Leave blank if optout not required
  "mesh_client_key": "",  // Leave blank if optout not required
  "mesh_hash_secret": "",  // Leave blank if optout not required
  "mesh_mailbox_password": "",  // Leave blank if optout not required
  "mongodb_password": "",  // Generate secure password (min length 10, alphanumeric)
  "mongodb_username": "root",
  "mongodb_replica_set_key": "",  // Generate secure password (length: 64, alphanumeric)
  "postgresql_password": "",  // Generate secure password (min length 10, alphanumeric)
  "postgresql_username": "postgres",
  "s3_access_key_id": "ffadmin",
  "s3_secret_access_key": "",  // Generate secure password (min length 10, alphanumeric)
  "ude_key": "",  // Generate from ude_cli using key-gen command
  "spicedb_pre_shared_key": ""  // Get from centralized spicedb or create new
}
```

##### SpiceDB Secrets

```json
{
  "postgresql_password": "",  // Generate secure password (min length 10, alphanumeric)
  "postgresql_username": "postgres",
  "spicedb_preshared_key": ""  // Generated and shared within application_secrets
}
```

##### Cloudflare Secrets (if Using Cloudflare as DNS)

```json
{
  "api_token": ""  // Generate from Cloudflare portal with Edit DNS permissions
}
```

## UDE Secret Generation

1. Clone the repository: <https://gitlab.com/fitfile/ude-cli>
2. Install the nightly version of rust:

```bash
rustup install nightly
```

3. Run the key generation command:

```bash
cargo run -- key-gen
```

4. Copy the final line of output (unique string) for use in the secrets

## Auth0 Configuration

Auth0 manages application user identities and provides authentication. To configure:

1. Navigate to the central services repository
2. Change to the appropriate auth0 directory:
   - `auth0/prod` for production deployments
   - `auth0/non-prod` for non-production deployments

3. Edit `auth0/locals.tf` and add a new block to the `fitfile_tenant_applications` map:

```hcl
<replace-with-deployment-key> = {
  tenant_name = "<replace with tenant display name>"
  api_name = "<replace with tenant api display name>"
  api_audience = "https://<replace-with-tenant-host-address>"
  enabled_apis =
  whitelist_api_audience_for_login_redirect = true # Set to true if deploying a web application
}
```

4. Update `main.tf` with additional configuration:
   - Set `additional_logout_redirect_urls` (usually `https://<host>/fitfile`)
   - Set `additional_web_origins` (usually `https//<host>`)
   - These can use wildcards () on the subdomain

5. Apply the terraform changes:

   ```bash
   terraform output -json
   ```

6. From the output, collect:
   - client_id and client_secret
   - webapp_application_client_credential values

7. Update the vault application secret with Auth0 values:

```json
{
  "auth0_client_id": "",  // Auth0 client id from terraform output
  "auth0_client_secret": "",  // Auth0 client secret from terraform output
  "auth0_audience": "",  // API Audience from terraform output
  "auth0_frontend_client_id": "",  // FITFILE SPA application client id
  "auth0_frontend_client_secret": ""  // FITFILE SPA application client secret
}
```

## Grafana Setup

1. In the central services repository, navigate to the grafana directory
2. Edit `locals.tf` and add to the "deployments" variable:

```hcl
locals {
  deployments = tomap({
    "<replace-with-deployment-key>" = {
      stack = local.prod_stack # or local.non_prod_stack if not production
    }
  })
}
```

3. Apply terraform and get the output:

   ```bash
   terraform output -json
   ```

4. Update the monitoring secret in vault with:

```json
{
  "prometheus_host": "",
  "prometheus_username": "",
  "prometheus_password": "",  // Access policy token
  "loki_host": "",
  "loki_username": "",
  "loki_password": "",  // Same access policy token
  "tempo_host": "",  // Include port :443
  "tempo_username": "",
  "tempo_password": ""  // Same access policy token
}
```
