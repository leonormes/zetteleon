---
aliases: []
confidence: 
created: 2025-01-03T12:44:50Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Phase 1 Tooling Configuration
type:
uid: 
updated: 
version:
---

## FitFile Platform Deployment Guide - Phase 1 Tooling Configuration

### Overview

This guide covers the first phase of deploying the FitFile platform: configuring the central services tooling. This phase establishes the foundational components needed for authentication, secret management, and monitoring. All subsequent deployment phases will build upon these configurations.

### Prerequisites

Before beginning the tooling configuration, ensure you have the following:

1. Access to the following services:
   - HashiCorp Cloud Platform (HCP) Portal
   - Auth0 Management Console
   - GitLab Account with access to FitFile repositories
   - Terraform Cloud Account

2. Required software installed locally:
   - tfenv and terraform with correct version
   - rust (nightly version required for UDE CLI)
   - git

3. Local environment setup:

```bash
# Create a working date directory
mkdir fitfile_deployment
cd fitfile_deployment
   
# Clone required repositories 
git clone https://gitlab.com/fitfile/ude-cli
git clone https://gitlab.com/fitfile/terraform-infrastructure/production/central-services
```

### Step 1: Generate Deployment Key

The deployment key is a crucial identifier used consistently across all infrastructure components.

1. Navigate to the central-services repository:

```bash
cd central-services
```

2. Run the shortname generator script:

```bash
chmod +x ./short_name.sh
   ./short_name.sh
```

3. When prompted:
   - Enter the full name of the customer
   - Enter the deployment environment (Dev, Prod)
   - Save the generated deployment key for use throughout the process

4. Record the deployment key in the deployment database:
   Navigate to: <https://fitfile.atlassian.net/wiki/spaces/FITFILE/database/1839071273>

### Step 2: Configure Vault Resources

1. Navigate to the Vault configuration directory:

   ```bash
   cd central-services/hcp/vault
   ```

2. Edit the locals.tf file to add the new deployment:

   ```hcl
   "<your-deployment-key>" = {
     secrets = tomap({
       "application" = {},
       "spicedb" = {},
       "cloudflare" = {}, # only if using cloudflare
       "monitoring" = {}, # for grafana credentials
     })
   }
   ```

3. Commit and push the changes:

   ```bash
   git add locals.tf
   git commit -m "feat: add vault secrets for <deployment-key>"
   git push
   ```

4. Apply the Terraform changes:
   - Navigate to Terraform Cloud
   - Find the run triggered by your push
   - Review and approve the plan

### Step 3: Populate Vault Secrets

1. Access the Vault UI:
   - Go to <https://portal.cloud.hashicorp.com/>
   - Select the ops-project
   - Navigate to Vault Dedicated
   - Click on vault-cluster
   - Generate an admin token
   - Click on the "Public" web access link

2. Navigate to deployments/\<your-deployment-key\> namespace
3. Configure application secrets:

   ```json
   {
     "auth0_client_id": "",
     "auth0_client_secret": "",
     "auth0_audience": "",
     "auth0_frontend_client_id": "",
     "auth0_frontend_client_secret": "",
     "mongodb_password": "<generated-secure-password>",
     "mongodb_username": "root",
     "mongodb_replica_set_key": "<generated-64-char-alphanumeric>",
     "postgresql_password": "<generated-secure-password>",
     "postgresql_username": "postgres",
     "s3_access_key_id": "ffadmin",
     "s3_secret_access_key": "<generated-secure-password>",
     "ude_key": "<generated-from-ude-cli>",
     "spicedb_pre_shared_key": "<from-central-or-generated>"
   }
   ```

4. Configure spicedb secrets:

   ```json
   {
     "postgresql_password": "<generated-secure-password>",
     "postgresql_username": "postgres",
     "spicedb_preshared_key": "<same-as-in-application-secrets>"
   }
   ```

5. If using Cloudflare, configure cloudflare secrets:

   ```json
   {
     "api_token": "<generated-from-cloudflare-portal>"
   }
   ```

### Step 4: Generate UDE Secret

1. Navigate to the ude-cli directory:

   ```bash
   cd ../../ude-cli
   ```

2. Install Rust nightly:

   ```bash
   rustup install nightly
   ```

3. Generate the UDE key:

   ```bash
   cargo run -- key-gen
   ```

4. Copy the generated key and add it to the vault application secrets under the "ude_key" field

### Step 5: Configure Auth0

1. Navigate to the Auth0 configuration:

   ```bash
   cd ../central-services/auth0/prod  # or auth0/non-prod for non-production
   ```

2. Edit locals.tf to add the new tenant:

```hcl
   "<your-deployment-key>" = {
     tenant_name = "<display-name>"
     api_name = "<api-display-name>"
     api_audience = "https://<tenant-host-address>"
     enabled_apis =
     whitelist_api_audience_for_login_redirect = true
   }
```

3. Update main.tf if needed:

```hcl
   additional_logout_redirect_urls =
   additional_web_origins =
```

4. Apply the changes:

```bash
   git add .
   git commit -m "feat: add auth0 configuration for <deployment-key>"
   git push
```

5. Get the client credentials from Terraform output:

```bash
   terraform output -json
```

6. Update Vault application secrets with the Auth0 credentials:
   - Add client_id and client_secret to the application secrets
   - Add webapp_application_client_credential values

### Step 6: Configure Grafana

1. Navigate to the Grafana configuration:

```bash
   cd ../grafana
```

2. Edit locals.tf:

```hcl
   locals {
     deployments = tomap({
       "<your-deployment-key>" = {
         stack = local.prod_stack  # or local.non_prod_stack if not production
       }
     })
   }
```

3. Apply the changes and get the output:

```bash
   terraform output -json
```

4. Update the monitoring secrets in Vault with the Grafana credentials:

```json
   {
     "prometheus_host": "<from-terraform-output>",
     "prometheus_username": "<from-terraform-output>",
     "prometheus_password": "<from-terraform-output>",
     "loki_host": "<from-terraform-output>",
     "loki_username": "<from-terraform-output>",
     "loki_password": "<from-terraform-output>",
     "tempo_host": "<from-terraform-output>:443",
     "tempo_username": "<from-terraform-output>",
     "tempo_password": "<from-terraform-output>"
   }
```

### Verification

After completing all steps, verify:

1. All secrets are properly populated in Vault
2. Auth0 application is created and configured
3. Grafana monitoring stack is configured
4. UDE key is generated and stored
5. All changes are committed and pushed to version control

### Troubleshooting

If you encounter issues:

1. Check the Terraform Cloud logs for detailed error messages
2. Verify all secrets are properly formatted JSON
3. Ensure all generated passwords meet minimum requirements (length, complexity)
4. Confirm all required access tokens are still valid
5. Verify network connectivity to all services

### Next Steps

Once the tooling configuration is complete, proceed to Phase 2: Infrastructure Deployment. All secrets and configurations set up in this phase will be used by the infrastructure deployment process.
