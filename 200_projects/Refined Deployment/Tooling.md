---
aliases: []
author:
confidence: 
created: 2025-09-28T02:56:47Z
description:
epistemic: 
id: Tooling
last_reviewed: 
modified: 2025-10-30T14:24:13Z
published:
purpose: 
review_interval: 
see_also: []
source: https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/Azure+-+Tooling
source_of_truth: []
status: 
tags: []
title: Tooling
type:
uid: 
updated: 
version:
---

## 1. Central Services and Prerequisites

Before initiating the tooling phase, certain prerequisites and software installations are necessary. These include setting up a workstation with `tfenv` and `terraform` (with the correct version), `azure-cli`, and `last-pass`. Essential repositories like "FITFILE development," "UDE CLI," and "Central Services" must be cloned.

A unique `deployment-key` (short name, e.g., "WM-Prod") is generated using a script (e.g., `short_name.sh` in Central Services) for each deployment and must be consistently used across the infrastructure. This key needs to be saved in a database.

## 2. Vault Configuration

Vault, specifically Hashicorp Vault, is a critical tool for secrets management.

- Creating Vault Resources: This step involves creating empty secrets in Vault.
- Within the `hcp/vault` directory of the Central Services repository, a new block needs to be added to the `deployments` variable.
- For new deployments, this typically includes secrets for "application," "spicedb," "cloudflare" (if used), "monitoring" (for Grafana credentials), and "argo-workflows" (for SSO configuration).
- Committing and pushing these changes triggers a Terraform plan and apply in Terraform Cloud, which a DevOps engineer must manually approve.
- Populating Secrets: After creation, these empty secrets must be populated.
- Access to the HashiCorp Cloud Platform (HCP) Portal and the "ops-project" is required. From there, an admin token is generated to log in to the Vault Dedicated instance.
- Secrets are populated within the `deployments/<deployment-name>` namespace in Vault. Each secret version must be created and populated with specific JSON data, ensuring comments are removed as Vault does not accept them.
- Application Secrets: Include `mongodb_password`, `mongodb_username` (root), `mongodb_replica_set_key`, `postgresql_password`, `postgresql_username` (Postgres), `s3_access_key_id` (ffadmin), `s3_secret_access_key`, and `ude_key`. Optional fields like `cli_auth0_client_id`, `cli_auth0_client_secret`, and `mesh_` related keys can be left blank if not required.
- Spicedb Secrets: Contain `postgresql_password`, `postgresql_username` (Postgres), and `spicedb_preshared_key`.
- Cloudflare Secrets: Required if Cloudflare is used as DNS, and consist of a `api_token` generated from the Cloudflare portal with "Edit DNS" permissions for the relevant zone.
- ArgoCD Secrets: Consist of `admin_password` (for break-glass account), `sso_azure_client_secret` (for ArgoCD Application in Microsoft Entra ID), and `gitlab_deploy_token_password` and `gitlab_deploy_token_username` (with `read_repository` role for GitLab access).
- Argo Workflows SSO Secrets: May include optional `argo_sso_client_id` and `argo_sso_client_secret` if an ingress is attached and SSO is desired, and required `postgresql_password` and `postgresql_username` for workflow archiving.

## 3. UDE Secret Generation

The UDE CLI repository is used to generate a unique key. This involves:

- Installing the nightly version of Rust.
- Running `cargo run -- key-gen` to generate the key. The resulting unique string is copied for use.

## 4. Auth0 Configuration

Auth0 manages application user identities and provides the authentication mechanism.

- The process involves configuring Auth0 to recognise the new deployment.
- The `auth0` directory (either `auth0/prod` or `auth0/non-prod`) within the Central Services repo is used.
- A new block for the `fitfile_tenant_applications` map is added to the `auth0/locals.tf` file, defining `tenant_name`, `api_name`, `api_audience` (which is the DNS record for the ingress controller), and `enabled_apis`.
- Additional `additional_logout_redirect_urls` and `additional_web_origins` (which can use wildcards) might be added to `main.tf`.
- After applying the Terraform changes, the `client_id` and `client_secret` (along with `webapp_application_client_credential` client_id and client_secret) from the Terraform output are retrieved. These values are then added to the `application` secret in Vault.

## 5. Grafana Configuration

Grafana is used for observability, specifically for logging (Loki), tracing (Tempo), and metrics (Prometheus).

- Within the `grafana` directory of the Central Services repo, a new key-value pair for the deployment is added to the `deployments` local variable in `locals.tf`, specifying the stack (e.g., `prod_stack` or `non_prod_stack`).
- After applying Terraform, the output (containing Prometheus, Loki, and Tempo `_host`, `_username`, and `_password` values) is used to populate the `monitoring` secret in Vault.

## Tooling in the Larger Azure Deployment Context

The "Tooling" phase is fundamental to the entire Azure deployment process. The information generated and configured during this phase (like the `deployment-key`, Vault secrets, Auth0 credentials, and Grafana configurations) directly feeds into subsequent stages:

- Infrastructure Deployment: Terraform Cloud, used for infrastructure deployment, relies on ARM keys (`ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET`) which are set as sensitive environment variables after being created in the tooling phase. The `deployment-key` is also crucial for naming workspaces and resources.
- Platform Deployment: The platform configuration, especially for a private cluster, depends on connecting to Vault for secrets (using `approles`) and GitLab for deployment configurations. The SSH Jumpbox, configured during infrastructure deployment, is used to access and further configure the platform elements, leveraging credentials and access setup in the tooling phase.
- Networking and Firewall Rules: The requirement for outbound firewall rules for various FITFILE central services (Vault, Auth0, Grafana, GitLab, Azure Container Registry, Microsoft Container Registry) is explicitly defined, showing the critical dependency between the configured tooling and the customer's network environment. Issues with these firewall rules can block key tooling processes, such as a VM's ability to install tools from package repositories or connect to Vault.
- Identity and Access Management: The creation of Service Principals with Contributor access and User Access Administrator roles, along with adding FITFILE DevOps users to the customer's Azure Tenant, are prerequisites that enable the tooling to interact with the Azure subscription.

The "Navigating Complex Cloud Deployments: Lessons Learned" document underscores the importance of a detailed technical pre-deployment checklist, which would encompass many of these tooling-related configurations. Issues like incorrect IP addressing, missing VNet peering, and unapplied firewall rules highlight why thorough upfront clarity on network architecture, firewall rules, and access permissions—all dependent on or affecting tooling connectivity—are essential. For instance, failures to register Resource Providers or insufficient vCPU quotas, which are typically identified during the early setup stages linked to tooling, can halt the deployment.

- 1 [Vault](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#Vault)
  - 1.1 [Create Vault Resources](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#Create-Vault-Resources)
  - 1.2 [Populate secrets](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#Populate-secrets-%5BinlineExtension%5D)
    - 1.2.1 [UDE secret generation](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#UDE-secret-generation)
- 2 [Auth0](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#Auth0)
- 3 [Grafana](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/#Grafana)

These tasks need to be performed by DevOps contributors who are responsible for the Central Services tooling.

The terraform for Central Services is found here: [Central Services](https://gitlab.com/fitfile/terraform-infrastructure/production/central-services)

This customer deploy will be referenced with what we are calling a deployment-key. This is the short name FITFILE uses for the specific customer everywhere in the infrastructure. Do not use the full name of the customer but something like WM-Prod. Make sure to keep this consistent where ever you use it. It is important!

## Vault

Complete

### Create Vault Resources

Complete

This just creates empty secrets on vault.

Inside the Central Services repository, cd to `hcp/vault`

1. [Central Services](https://gitlab.com/fitfile/terraform-infrastructure/production/central-services "https://gitlab.com/fitfile/terraform-infrastructure/production/central-services")
2. Within `locals.tf` add a new block to the `deployments` variable. The secret objects to create may differ with each deployment, but generally for new deployments it will look like this:
   `"<replace_with_deployment_key>"={secrets= tomap({"application"={}, "spicedb"={}, "cloudflare"={}, # only needed if using cloudflare"monitoring"={}, # for grafana creds"argo-workflows"={}, # for argo workflows sso configuration}) }`
3. Commit and push the change to trigger the terraform plan and apply in Terraform Cloud: [HCP Terraform](https://app.terraform.io/app/FITFILE-Platforms/workspaces/hcp-vault)
4. A DevOps engineer will need to manually press the apply button on the Run page
5. Once the run has complete, now we need to set up the secrets.

### Populate Secrets

Complete

At the time of writing this, SSO for the vault instance has not been set up, so the only way to login to vault is through the HCP portal: [HashiCorp Cloud Platform](https://portal.cloud.hashicorp.com/) and then navigating to the vault dedicated instance, and generating an admin token.

1. Login to HCP Portal: [HashiCorp Cloud Platform](https://portal.cloud.hashicorp.com/) and ensure you’re on the ops-project
   ![image-20240716-075957.png](https://media-cdn.atlassian.com/file/1566b503-ff89-487f-808d-c2371a65c0ad/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=443&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
2. Go to Vault Dedicated, then click on vault-cluster:
   ![image-20240716-080008.png](https://media-cdn.atlassian.com/file/24d33f5b-9b71-4985-a8ec-9745eaf0a543/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=335&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
3. Click on Generate admin token and then click on the “Public“ web access link, which will open a new browser tab
   ![image-20240716-080018.png](https://media-cdn.atlassian.com/file/ba97a26a-258d-4301-9e77-4c43d1f334fe/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=462&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
4. Paste the token into the “Sign in Vault” form
   ![image-20240716-080047.png](https://media-cdn.atlassian.com/file/fd8c28be-e2df-4b0c-b19c-7904d46a2860/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=483&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
5. Navigate to the `deployments/<deployment-name>` namespace
   ![image-20240716-084505.png](https://media-cdn.atlassian.com/file/b1666679-e348-43b7-a798-98c48b3fffab/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=846&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
6. Go to secrets engines and click on `secrets` - You should see the secrets we created in the previous step.
   ![image-20240716-084553.png](https://media-cdn.atlassian.com/file/822a6099-8eac-47e0-9da9-126dea265805/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=681&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
7. Create a new version of each secret and populate the json secrets:
   ![image-20240716-084638.png](https://media-cdn.atlassian.com/file/7b8be0d9-7dd5-4e3e-a34e-222efdac76a8/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=583&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760) ![image-20240716-084654.png](https://media-cdn.atlassian.com/file/e9d5c205-5bf1-4fe2-b0e4-9f93a8772579/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=210&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760) ![image-20240716-085107.png](https://media-cdn.atlassian.com/file/46ef0bc0-1bdf-419d-a232-f898369edba7/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=561&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
   **FOLLOW THE COMMENTS BESIDE EACH SECRET FOR HOW TO POPULATE THEM**
   VAULT DOES NOT EXCEPT JSON WITH COMMENTS AND SO WILL NOT SAVE UNTIL THEY ARE REMOVED
   1. application secrets:
      ``{"cli_auth0_client_id":"",// Leave blank - do not need to fill"cli_auth0_client_secret":"",// Leave blank - do not need to fill"mesh_client_cert":"",// Leave blank if optout not required"mesh_client_key":"",// Leave blank if optout not required"mesh_hash_secret":"",// Leave blank if optout not required"mesh_mailbox_password":"",// Leave blank if optout not required"mongodb_password":"",// generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)"mongodb_username":"root","mongodb_replica_set_key":"",// generate secure password (length: 64, alphanumeric only)"postgresql_password":"",// generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)"postgresql_username":"postgres","s3_access_key_id":"ffadmin","s3_secret_access_key":"",// generate secure password (min length 10, alphanumeric only)"ude_key":"",// generate from ude_cli using `key-gen` command. Needs to be same in all connected tenants"spicedb_pre_shared_key":""// This may be different based on whether you use centralised spicedb or not. If centralised, get it from vault from admin/fitfile/production/spicedb_secrets. Otherwise, get from spicedb_secrets you will create"fitfile_tenant_pkcs8.key":""// The private tenant pkcs8 signing key. See below"fitfile_tenant_public.crt":""// The public tenant signing key. See below}``
      \*To generate the fitfile_tenant signing keys, do the following:

      `mkdir <deployment-key> cd <deployment-key> openssl genrsa -out keypair.pem 4096 openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key openssl rsa -in keypair.pem -pubout -out publickey.crt`

      Put the `pkcs8.key` in the `fitfile_tenant_pkcs8.key` secret value, and the `publickey.crt` in the `fitfile_tenant_public.crt` value.

   2. spicedb secrets:
   3. cloudflare secrets (required if using cloudflare as DNS):
      Generate from Cloudflare portal → Account → API Tokens. Ensure it has Edit DNS for the [Home - FITFILE](http://fitfile.net/) zone. Name it appropriately, like `<deployment-name>-challenge-token`
      `{   "api_token": "" }`
   4. ArgoCD secrets:
      There are 3 parts to this secret
      \- The `admin_password` for the break glass account
      \- The `sso_azure_client_secret` for the ArgoCD Application in Microsoft Entra ID which governs access to this ArgoCD instance
      \- The `gitlab_deploy_token_password` and `gitlab_deploy_token_username` credentials with the `read_repository` role which allow ArgoCD to pull from our GitLab deployment repository. (See here for creating a deploy token: [Deploy tokens | GitLab Docs](https://docs.gitlab.com/user/project/deploy_tokens/) )

      `{"admin_password":"",// htpasswd -nbBC 10 "" <replace-me-with-password> | tr -d ':\n' | sed 's/$2y/$2a/'"gitlab_deploy_token_password":"","gitlab_deploy_token_username":"","sso_azure_client_secret":""}`

   5. Argo workflows SSO secrets.
      This is comprised of 2 parts:
      \- (Optional) `argo_sso_client_id` and `argo_sso_client_secret`. Only needed if an ingress is attached to Argo Workflows API and SSO is desired. The SSO outbound connection to our Azure tenant auth endpoint must be allowed by the customer. Argo Workflows is usually an internal API to the cluster and is not exposed by default. In this case, client authentication is used (meaning kubernetes auth is used). A user can still call the workflows API given the right level of access on their user, or they can assume a service account role which does have access.

      \- (Required) `postgresql_password` and `postgresql_username`. These are the credentials to the postgresql instance for argo workflows to archive workflows to. Currently we use the same credentials as the **application** secret uses, however, in future we’d like to create a scoped user during the postgresql init db script which is more limited to the argo workflows db in the server.

      `{"argo_sso_client_id":"","argo_sso_client_secret":"","postgresql_password":"",// The same as the application postgresql_password"postgresql_username":""// The same as the application postgresql_username}`

#### UDE Secret Generation

Complete

1. Checkout this repo: [UDE CLI](https://gitlab.com/fitfile/ude-cli)
2. Run this command:
   `rustup install nightly`
   This will install the nightly version of rust, required by the testing framework.
3. run `cargo run -- key-gen` - this will download dependencies, build the binary and run the keygen command.
4. Copy the final line of the output, which should be a unique string

Unable to render {include} The included page could not be found.

## Auth0

- Complete

Auth0 manages our application user identities and provides our authentication mechanism.

![image-20240716-085926.png](https://media-cdn.atlassian.com/file/40155b5d-c5cd-45cf-80db-10cc64aab756/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=557&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)

1. Go to the central services repo
2. cd to auth0 directory - either `auth0/prod` if it is a production deployment, or `auth0/non-prod` if it is non production.
3. Open the auth0/ [locals.tf](http://locals.tf/ "http://locals.tf/") file
   1. Add a new block to the `fitfile_tenant_applications` map
      tenant is something you make up.
      As an example, given deployment key `wm-dev-1` we used the name `WM Dev 1`. This is only every seen by us.
      api_audience must be the dns record for the ingress controller. In this example we created `resource "azurerm_private_dns_a_record" "ingress_controller_dns_record" {`
      and so this is the the one to use. Our deployments will have many different dns records and so this is something we find out in collaboration with the customer IT Team.
      enabled_apis is the list of partner audiences the machine can call with the given token.
4. You may need to add some configuration to the [main.tf](http://main.tf/ "http://main.tf/") file as well:
   Add the `additional_logout_redirect_urls` and `additional_web_origins` - these can use wildcards (`*`) on the subdomain.
   `additional_logout_redirect_urls` - is usually `https://<host>/fitfile`
   `additional_web_origins` - is usually `https//<host>`
5. Apply the terraform changes.
6. From the terraform output, grab the `client_id` and `client_secret` of the deployment. Also grab the `webapp_application_client_credential` client_id and client_secret as well.
   `terraform output -json`
7. You will need to add these values to the vault `application` secret for the deployment.
8. Follow these [steps](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1894744069&navigatingVersions=true# "https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1894744069&navigatingVersions=true#") to get to the secrets engine
9. Click on the **application** secret and click “create new version”
10. Add these new values in the json object secret
    `"auth0_client_id": "", // use the Auth0 client id from the Auth0 terraform output "auth0_client_secret": "", // use the Auth0 client secret from the Auth0 terraform output "auth0_audience": "", // use API Audience from the Auth0 terraform output "auth0_frontend_client_id": "", // use existing FITFILE SPA application client id from the Auth0 terraform output "auth0_frontend_client_secret": "", // use existing FITFILE SPA application client secret from the Auth0 terraform output`
11. Click save

## Grafana

Complete

1. Go to the central services repo
2. cd to grafana
3. Open the [locals.tf](http://locals.tf/ "http://locals.tf") file
4. Add a new key value pair to the “deployments” local variable
   `locals{  ... deployments= tomap({    ... "<replace-with-deployment-key>"={stack= local.prod_stack # or local.non_prod_stack if not production}})   ... }`
5. Apply terraform
6. Get the terraform output with:
   `terraform output -json`
   You will need to reference this output later
7. Follow these [steps](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839169559/# "#") to get to the secrets engine
8. Click on the `monitoring` secret and click “create new version”
9. Add the following values:
   `{   // Get from Central Services grafana module output   "prometheus_host": "",   "prometheus_username": "",   "prometheus_password": "", // The access policy token for this deployment   "loki_host": "",   "loki_username": "",   "loki_password": "", // The same access policy token for this deployment   "tempo_host": "", // Ensure you add the port :443 on the end   "tempo_username": "",   "tempo_password": "" // The same access policy token for this deployment }`
   ![image-20240716-090607.png](https://media-cdn.atlassian.com/file/8f58a2f6-62f6-417a-90bd-5fde8ccc484a/image/cdn?allowAnimated=true&client=79d9a90a-d0b1-4ba1-9c4d-7fda8295d8c2&collection=contentId-1839169559&height=526&max-age=2592000&mode=full-fit&source=mediaCard&token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3OWQ5YTkwYS1kMGIxLTRiYTEtOWM0ZC03ZmRhODI5NWQ4YzIiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpjb2xsZWN0aW9uOmNvbnRlbnRJZC0xODM5MTY5NTU5IjpbInJlYWQiXX0sImV4cCI6MTc1ODUzMzMwMSwibmJmIjoxNzU4NTMwNDIxLCJhYUlkIjoiNjMzYWUyYjlmZWRjNjE2OWFlZDhmNjAxIn0.abwMcW5QFNE6Ul7NAbqB0jSdkmFZOvpVpA4McTQ0ZII&width=760)
10. Save the secret

## Azure - Infrastructure (private): Overview

The "Infrastructure" phase is the second part of the four-stage Azure deployment process. Its primary goal is to create the necessary infrastructure in Azure, which includes networking, compute resources, and setting up developer access for the new deployment. Specifically for a private cluster in Azure, this phase sets up the Terraform infrastructure deployment. These tasks are performed by DevOps contributors who are also responsible for the Central Services tooling.

## Core Components and Process Steps

The deployment of private Azure infrastructure involves several key tools and steps:

### 1. Terraform Cloud Setup

Terraform Cloud is used to manage the infrastructure deployment and its continuous integration/continuous delivery (CI/CD).

- **Login and Project Creation**: DevOps contributors must log in to Terraform Cloud (HCP Terraform) and either select an existing project for the customer or create a new one.
- **Workspace Creation**: A workspace must be created within the project, named using a unique `deployment-key`. This key is a short name (e.g., "WM-Prod") used consistently across the infrastructure to identify the specific customer deployment.
- **Variable Configuration**: Essential Azure Resource Manager (ARM) keys must be added as environment variables to the Terraform Cloud workspace: `ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, and `ARM_CLIENT_SECRET`. All of these, except the client ID, should be marked as sensitive. Additionally, a randomly generated, secure `admin_password` (ideally 20+ characters) for the jumpbox must be added as a Terraform variable and saved securely (e.g., in LastPass).

### 2. GitLab Repository Setup

A new customer deployment repository is created in GitLab to isolate configuration and manage access.

- **Project Creation and Cloning**: DevOps engineers log into GitLab, navigate to the "Customers" group, and create a new blank project using the same `deployment-key` as the project name. The repository is then cloned locally.
- **File Initialization**: Initial Terraform files (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `providers.tf`, `.gitignore`) are created.
- **Terraform Configuration**:
- The Terraform Cloud configuration block (copied from the workspace) is pasted into `versions.tf`.
- The `azurerm` provider block is added to `providers.tf`, specifying `tenant_id` and `subscription_id`.
- An output block for `aks_cluster_outbound_ip_address` is added to `outputs.tf`.
- The `main.tf` file is populated with a module block, typically referencing the `private-infrastructure/azure` module from the Terraform module registry, ensuring the `deployment_key` and `admin_password` variables are passed.
- The `admin_password` variable is also declared in `variables.tf`.
- VM sizes for node pools (`additional_node_pool_vm_size`, `default_node_pool_vm_size`) can be overridden based on customer requirements, though smaller VM sizes are not recommended due to resource consumption by daemon set pods.
- The module configures the Kubernetes Cluster to use `loadBalancer` as the default outbound type, which assigns a public IP address for egress. Other outbound types like `userDefinedRouting` (for firewall), `managedNATGateway`, or `userAssignedNATGateway` (for NAT Gateway) can be specified if required.

### 3. Terraform Execution

Once the configuration is in place, Terraform commands are executed to deploy the infrastructure.

- **Authentication**: `terraform login` is run locally to obtain the necessary access token for Terraform Cloud.
- **Initialization and Apply**: `terraform init --upgrade` is run to initialize the working directory and download providers/modules. Then, `terraform apply` is executed, and the plan must be reviewed before confirming the deployment.
- **Output Retrieval**: After successful deployment, `terraform output` can be used to retrieve values like the `aks_cluster_outbound_ip_address` (if using `loadBalancer`) which might be needed for subsequent steps. For AWS infrastructure, `terraform output` provides the generated password for the `awsadmin` user to log in to the jumpbox.

### 4. Jumpbox Access and Verification

A critical part of the infrastructure deployment is setting up and verifying access to the Jumpbox, which acts as a secure access point to the private cluster.

- **Connecting to the Jumpbox**: For Azure, users connect to the `FITFILEJumpbox` VM via the Azure portal's serial console or RDP using `azadmin` as the login name and the `admin_password` set in Terraform. For AWS, `aws ssm start-session` is used to establish a session to the `FITFILEJumpbox` instance, followed by an RDP client connection to `localhost:55679`.
- **Tool Verification**: Once logged into the Jumpbox, it's essential to verify that `aws cli`, `terraform`, and `kubectl` are installed and working.
- **Azure CLI Configuration**: `az login` is performed on the Jumpbox to authenticate with Azure, selecting the correct customer subscription.
- **Kubernetes Credentials**: Credentials for the AKS cluster are downloaded and configured using `az aks get-credentials` (or `aws eks update-kubeconfig` for AWS). `kubectl get nodes` or `kubectl get pods -A` is then run to test connectivity to the cluster's API server.

## Prerequisites from the Customer's Perspective

The customer plays a crucial role in preparing their Azure Tenant and Subscription for the FITFILE deployment. These prerequisites directly enable the "Infrastructure (private)" phase to proceed smoothly.

- **Information Sharing**: The customer must share their Azure Tenant ID and Azure Subscription ID with FITFILE.
- **Resource Provider Registration**: Specific Resource Providers in the Azure Subscription must be registered. These include `Microsoft.ContainerService` (for Kubernetes Service), `Microsoft.ManagedIdentity` (for managed identities), `Microsoft.Network` (for networking), `Microsoft.Storage` (for storage accounts), and `Microsoft.Compute` (for virtual machines). An error during deployment occurred previously due to an unregistered Resource Provider.
- **Service Principal Creation**: A Service Principal (e.g., "FITFILE Terraform Cloud Provisioner") needs to be created in the Azure tenant with `Contributor` access to the Subscription. An additional role assignment of `User Access Administrator` is also required for the Service Principal to assign roles for the AKS cluster identity. The client ID, secret ID, and value of this Service Principal are then used as ARM keys in Terraform Cloud.
- **Encryption at Host**: Encryption at Host must be enabled on the subscription, which can take up to 20 minutes. An error was encountered when this was not enabled, leading to deployment failure.
- **Compute Quota**: The customer must ensure that the correct compute quota is registered in their Azure Subscription, as FITFILE's Terraform defaults to using memory-optimized Esv5 Series vCPUs, which may exceed default quotas. A "QuotaExceeded" error previously blocked deployment. Quota increases may be required and can take time.
- **FITFILE DevOps User Access**: A designated FITFILE DevOps user needs to be invited to the customer's Azure Tenant as a `Member` and assigned `Contributor` access to the subscription.

## Networking and Firewall Considerations

The infrastructure phase heavily involves configuring network components to allow communication for the cluster.

- **Virtual Network (VNet) and Subnets**: A VNet will be created with subnets for resources. This VNet will be peered to an existing CUH (customer) Shared Services vNet to route traffic. The address range must be provided to FITFILE for their Terraform script.
- **Route Tables**: Existing route tables in the Shared Services vNet are used to route traffic to the CUH on-premises network. A new route table is created in the FITFILE subscription's VNet to force traffic through the Shared Services FortiGate firewall.
- **Network Security Groups (NSGs)**: An NSG is applied to the FITFILE VNet's subnet to restrict inbound and outbound traffic.
- **Firewall Rules**: Outbound firewall rules are crucial for the FITFILE deployment to access central services like Auth0, Grafana, GitLab, Vault, and Azure Container Registry (ACR). Inbound rules are also needed for callback responses from services like Auth0. Incorrect or missing firewall rules were a significant problem, leading to blocked deployments and communication issues. It was found that traffic was routing to the Azure FortiGate but then going to the internet instead of the on-premise FortiGate. The resolution for this might involve configuring a proxy on the FITFILE VMs.
- **Private DNS**: FITFILE will deploy a private DNS zone, and Telefónica Tech will configure a DNS forwarder in the on-premises DNS to resolve FITFILE service IP addresses, allowing on-premises users to access FITFILE URLs (e.g., `app.privatelink.fitfile.net`).

## Challenges and Lessons Learned

Real-world deployments often encounter challenges that highlight the importance of thorough planning during the infrastructure phase.

- **Initial Access and Permissions**: Problems with `az login` hanging or session conflicts can impede initial access to the Jumpbox, preventing deployment progress.
- **Infrastructure Naming and IP Addressing**: Failing to adhere to customer-specified naming conventions (for Resource Groups, VNets, Route Tables, NSGs) and incorrect IP addressing for VNets and subnets (especially for AKS, which may require a larger range) lead to time-consuming teardowns and redeployments.
- **Network Connectivity and Firewall Rules**:
- **VNet Peering**: Critical VNet peering can be missing or inadvertently removed by subsequent Terraform redeployments, breaking network connectivity.
- **Outbound Routing**: Traffic may initially bypass required on-premise proxies, flowing directly to the internet, which is a security and compliance risk.
- **Firewall Blockage**: Even when routed correctly, traffic can be blocked if necessary firewall rules are not pre-emptively implemented, leading to delays due to formal change management processes (e.g., CAB). Troubleshooting can be complex due to protocols like ICMP being blocked by firewalls.
- **External Dependencies**: Delays can occur if requirements for user and other platform access (e.g., SDE) or on-premise database connectivity details (including authentication methods and security sign-off) are not established upfront. The ACR cross-tenant access issue required a private link or manual secret injection.

These issues underscore the need for a comprehensive technical pre-deployment checklist, clarity on roles and responsibilities, understanding of change management processes, and adopting modular Infrastructure as Code (IaC) with pre-flight checks.

## Central Services Setup for a New Customer

This guide consolidates the process from the multiple documents you provided, focusing on the "Tooling" and "Infrastructure" stages, which represent the core of the central services setup.

Phase 1: Prerequisites and Initial Setup

1. Workstation Setup:
   Ensure you have the following software installed: `tfenv`, `terraform` (correct version), `azure-cli`, and `last-pass`.
   Clone the `FITFILE development`, `UDE CLI`, and `Central Services` repositories.

2. Generate Deployment Key:
   In the `Central Services` repository, run the `./short_name.sh` script.
   When prompted, enter the full customer name and deployment environment (e.g., Dev, Prod).
   This will generate a unique `deployment-key` (e.g., `WM-Prod`). This key is crucial and must be used consistently throughout the entire process.
   Save this key securely.

Phase 2: Configure Central Services Tooling (Terraform Cloud & Vault)

1. Create Vault Resources:
   Navigate to the `hcp/vault` directory in the `Central Services` repository.
   In the `locals.tf` file, add a new block for the customer under the `deployments` variable, using the `deployment-key` you generated. This will define the necessary secret engines for the new customer in HashiCorp Vault.
   Commit and push the changes to trigger the Terraform plan in Terraform Cloud. A DevOps engineer will need to manually approve and apply the plan.

2. Populate Vault Secrets:
   Log in to the HashiCorp Cloud Platform (HCP) Portal.
   Navigate to the Vault cluster and then to the `deployments/<deployment-key>` namespace.
   Go to the `secrets` engine and create new versions for the `application`, `spicedb`, `cloudflare`, `ArgoCD`, and `argo-workflows` secrets.
   Populate the secrets with the required values, following the guidance and comments in the `Azure - Tooling` document. Use LastPass to generate secure passwords where required.

3. Configure Auth0:
   In the `Central Services` repo, navigate to the `auth0/prod` or `auth0/non-prod` directory, depending on the environment.
   In `auth0/locals.tf`, add a new block to the `fitfile_tenant_applications` map for the new customer, using the `deployment-key`.
   Define the `api_audience` (the DNS record for the ingress controller) and any other required parameters.
   Apply the Terraform changes and retrieve the `client_id` and `client_secret` from the output.
   Add these credentials to the `application` secret in Vault.

4. Configure Grafana:
   In the `Central Services` repo, go to the `grafana` directory.
   In `locals.tf`, add a new key-value pair for the new customer to the `deployments` local variable.
   Apply the Terraform changes and add the output values to the `monitoring` secret in Vault.

Phase 3: Deploy Azure Infrastructure

1. Create Terraform Cloud Workspace:
   Log in to Terraform Cloud.
   Create a new project or use an existing one for the customer.
   Create a new CLI-driven workspace within the project, naming it with the `deployment-key`.
   Add the necessary environment variables to the workspace: `ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET`, and the `admin_password` for the jumpbox. Ensure sensitive variables are marked as such.

2. Set up Customer GitLab Repository:
   In GitLab, navigate to the "Customers" group and create a new blank project, using the `deployment-key` as the project name.
   Clone the new repository locally.
   Create the following files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `providers.tf`, and `.gitignore`.
   Populate the files with the necessary Terraform configuration, as detailed in the "Azure - Infrastructure (private)" document. This includes the Terraform Cloud backend configuration, the `azurerm` provider block with the customer's tenant and subscription IDs, and the module block for the private infrastructure.

3. Deploy the Infrastructure:
   Run `terraform login` and authenticate with Terraform Cloud.
   Run `terraform init --upgrade`.
   Run `terraform apply` and review the plan carefully before confirming.
   Once the apply is complete, run `terraform output` to get the `aks_cluster_outbound_ip_address`. This will be needed for Vault.

## Canvas: FITFILE Node Deployment SOP

This document is a living Standard Operating Procedure (SOP) for deploying a new FITFILE customer node. Each section can be expanded with further detail.

---

### 🎯 **Stage 0: Prerequisites**

*(Details to be added here. This section will consolidate all setup requirements for both the customer and the DevOps engineer.)*

- **0.1 Customer Prerequisites** (AWS & Azure)
- **0.2 DevOps Engineer Prerequisites** (Workstation Setup)

---

### 🛠️ **Stage 1: Central Services Tooling**

This stage configures FITFILE's shared central services to support the new customer deployment.

#### **Step 1.1: Generate the Deployment Key**

The primary goal of this first step is to definitively establish the unique identifier for the deployment, known as the `deployment-key`. This key is essential for naming conventions across all infrastructure and GitOps tooling, and consistency is vital.

| Activity        | Details                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------- |
| **Goal**        | Generate a short, unique identifier (e.g., `MKUH-Prod`) to be used across all components.      |
| **Location**    | The DevOps engineer must navigate to their local clone of the **Central Services** repository. |
| **Script Used** | The `short_name.sh` script is executed.                                                        |

> **Next Steps:** Once this key is generated, it will be used to name resources like the Terraform Cloud Workspace and the GitLab repository. The next logical steps are to configure Auth0 and HashiCorp Vault.

#### **Step 1.2: Configure HashiCorp Vault**

*(This section is ready for iteration. Add details on how the `deployment-key` is used to create and populate secrets in Vault.)*

- **Goal**: Create the secret paths and approles in Vault for the new deployment.
- **Actions**:
  - Modify `locals.tf` in the `Central Services` repo.
  - Apply Terraform changes.
  - Log in to Vault UI and populate secrets.

#### **Step 1.3: Configure Auth0**

*(This section is ready for iteration. Add details on creating the Auth0 application and linking it back to the Vault secrets.)*

- **Goal**: Configure Auth0 for application user identity management.
- **Actions**:
  - Modify `locals.tf` in the `Central Services` repo.
  - Apply Terraform changes.
  - Update Vault with the new `client_id` and `client_secret`.

---

### ☁️ **Stage 2: Cloud Infrastructure**

*(This stage is ready for iteration. Detail the steps for deploying the core cloud resources for the customer.)*

- **Step 2.1: Create GitLab Repository**
- **Step 2.2: Configure Terraform Cloud Workspace**
- **Step 2.3: Populate Repository & Deploy Infrastructure (with AWS/Azure specifics)**
- **Step 2.4: Access & Verify the Jumpbox (with AWS/Azure specifics)**

---

### ⚙️ **Stage 3: Platform Deployment**

*(This stage is ready for iteration. Detail the steps performed from the jumpbox to install the GitOps platform.)*

- **Step 3.1: Jumpbox Preparation**
- **Step 3.2: Configure & Apply Platform Terraform**
- **Step 3.3: Manual Kubernetes Adjustments**

---

### 🚀 **Stage 4: Application Deployment**

*(This stage is ready for iteration. Detail the final GitOps-triggered application deployment.)*

- **Step 4.1: Prepare Helm Values**
- **Step 4.2: Commit & Push to Trigger GitOps Flow**
