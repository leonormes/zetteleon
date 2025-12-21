---
aliases: [FitFile Deployment Phase 1]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T15:43:17Z
purpose: To provide a detailed guide for Phase 1 of the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, foundation, phase1, tooling]
title: SoT - FitFile Deployment - Phase 1 - Foundation and Tooling
type: SoT
uid: 
updated: 
version: 1.0
---

## Phase 1: Foundation & Tooling

**Goal:** Establish the central identity, secrets, and monitoring control plane. This is the "Key to the Castle."

These tasks must be performed by DevOps contributors responsible for the Central Services tooling. The terraform configuration for Central Services can be found in the [Central Services repository](https://gitlab.com/fitfile/central-services).

### 1. Vault Configuration

#### Creating Vault Resources

First, we'll create empty secrets in vault:

1.  Navigate to the Central Services repository
2.  Change directory to `hcp/vault`
3. In `locals.tf`, add a new block to the deployments variable (e.g., for "wm-prod"):

```hcl
"wm-prod" = {
  secrets = tomap({
    "application" = {},
    "spicedb" = {},
    "cloudflare" = {}, # only needed if using cloudflare
    "monitoring" = {}, # for grafana creds
  })
}
```

4.  Commit and push the changes to trigger the terraform plan in [HCP Terraform](https://app.terraform.io/).
5.  A DevOps engineer must manually approve the apply on the Run page

#### Populating Vault Secrets

The customer deployment will be referenced using a deployment-key - a short name FITFILE uses consistently throughout the infrastructure. For example, use "WM-Prod" instead of the full customer name.

**Accessing Vault**

Currently, SSO is not configured for the vault instance. To access vault:

1.  Log into the HCP portal: <https://portal.cloud.hashicorp.com/>
2.  Navigate to the vault dedicated instance
3.  Generate an admin token

**Secret Configuration**

You'll need to create new versions of the following secrets:

**Application Secrets**

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

**SpiceDB Secrets**

```json
{
  "postgresql_password": "",  // Generate secure password (min length 10, alphanumeric)
  "postgresql_username": "postgres",
  "spicedb_preshared_key": ""  // Generated and shared within application_secrets
}
```

**Cloudflare Secrets (if Using Cloudflare as DNS)**

```json
{
  "api_token": ""  // Generate from Cloudflare portal with Edit DNS permissions
}
```

### 2. UDE Secret Generation

1.  Clone the repository: [https://gitlab.com/fitfile/ude-cli](https://gitlab.com/fitfile/ude-cli)
2.  Install the nightly version of rust:

```bash
rustup install nightly
```

3.  Run the key generation command:

```bash
cargo run -- key-gen
```

4.  Copy the final line of output (unique string) for use in the secrets

### 3. Auth0 Configuration

Auth0 manages application user identities and provides authentication. To configure:

1.  Navigate to the central services repository
2.  Change to the appropriate auth0 directory:
    -   `auth0/prod` for production deployments
    -   `auth0/non-prod` for non-production deployments
3. Edit `auth0/locals.tf` and add a new block to the `fitfile_tenant_applications` map. The tenant and API names are typically provided by the Project Manager. Example for `wm-prod`:

```hcl
"wm-prod" = {
  tenant_name = "West Midlands Production"
  api_name    = "FitFile API (WM-Prod)"
  api_audience = "https://api.westmidlands.fitfile.io"
  enabled_apis = ["<REPLACE>"]
  whitelist_api_audience_for_login_redirect = true # Set to true if deploying a web application
}
```

4. Update `main.tf` with additional configuration (after logging into the [Auth0 Dashboard](https://manage.auth0.com/)):
    - Set `additional_logout_redirect_urls` (usually `https://<host>/fitfile`)
    - Set `additional_web_origins` (usually `https//<host>`)
    - These can use wildcards () on the subdomain
5. Apply the terraform changes:

    ```bash
    terraform plan
    terraform apply
    ```

6. Once applied, collect the necessary outputs:

    ```bash
    terraform output -json
    ```

7. From the output, collect:
    - `client_id` and `client_secret`
    - `webapp_application_client_credential` values
8. Update the vault application secret with Auth0 values:

```json
{
  "auth0_client_id": "",  // Auth0 client id from terraform output
  "auth0_client_secret": "",  // Auth0 client secret from terraform output
  "auth0_audience": "",  // API Audience from terraform output
  "auth0_frontend_client_id": "",  // FITFILE SPA application client id
  "auth0_frontend_client_secret": ""  // FITFILE SPA application client secret
}
```

### 4. Grafana Setup

1.  In the central services' repository, navigate to the Grafana directory
2.  Edit `locals.tf` and add to the "deployments" variable. Example for `wm-prod`:

```hcl
locals {
  deployments = tomap({
    "<replace-with-deployment-key>" = {
      stack = local.prod_stack # or local.non_prod_stack if not production
    }
  })
}
```

3.  Apply terraform and get the output:

```bash
terraform output -json
```

4.  Update the monitoring secret in vault with:

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

### Verification

- [ ] **GitLab & Terraform Cloud:** Verify that the Terraform Cloud workspace for Central Services can successfully authenticate with GitLab and pull the repository contents.
- [ ] **Vault Secrets:** Log into the Vault UI and confirm that the new secrets for the deployment (e.g., `secret/fig/wm-prod/application`) have been created and populated correctly.
- [ ] **Auth0 Application:** Log into the Auth0 dashboard and verify that the new application, API, and associated permissions have been created as defined in the Terraform configuration.
- [ ] **Grafana Dashboards:** Log into Grafana and confirm that the new stack and associated data sources (Prometheus, Loki, Tempo) have been provisioned and are accessible.
- [ ] **IAM/RBAC Permissions:** Conduct a test to ensure that the permissions applied via Terraform grant the intended access and that there are no privilege escalation paths.
