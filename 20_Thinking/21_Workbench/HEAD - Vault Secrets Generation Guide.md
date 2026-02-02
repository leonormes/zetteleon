---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-01T20:52:31+00:00
status: processing
tags:
  - state/thinking
title: HEAD - Vault Secrets Generation Guide
type: head
updated:
uuid: cc0f2c94-c31e-468e-b100-87e3fa31b0c8
---

- Where are all the secrets configurations and usage spread across my code.
    - [x] Find the conflunce for the vault setup.
    - [ ] Find the secret assignments in the helm. ^2026-02-01T20-52-13
    - [📱 View in Todoist app](todoist://task?id=6fvV923M8X83WFwv) (Created: 📝 2026-02-01T20:52)
    - [ ] Check the clusters for where the secrets are
    - [ ] Check the vso docs for how to set it up
    - [ ] Check the LCA secrets implementation

## Vault Secrets Generation Guide

This guide outlines the process for creating and populating Vault resources for new customer deployments within the Central Services infrastructure.

---

### 1. Initial Resource Creation

Before populating values, you must create empty secret objects using Terraform.

1. Navigate to the repository: In the Central Services repository, go to `hcp/vault`.
2. Define the deployment: In `locals.tf`, add a new block to the `deployments` variable using the deployment-key (a short, consistent name like `WM-Prod`).
3. Template configuration:

    Terraform

```hcl
"<replace_with_deployment_key>" = {
  secrets = tomap({
    "application"    = {},
    "spicedb"        = {},
    "cloudflare"     = {}, # Only if using Cloudflare
    "monitoring"     = {}, # For Grafana credentials
    "argo-workflows" = {}, # For Argo Workflows SSO
  })
}
```

1. Apply changes: Commit and push to trigger the Terraform plan. A DevOps engineer must manually approve the apply in Terraform Cloud.

---

### 2. Accessing Vault

Currently, SSO is not enabled. Access is managed via the HashiCorp Cloud Platform (HCP) Portal.

1. Log in to the HCP Portal and select the `ops-project`.
2. Navigate to Vault Dedicated > vault-cluster.
3. Generate an Admin Token and open the Public web access link.
4. Sign in using the generated token and navigate to the `deployments/<deployment-key>` namespace.

---

### 3. Secret Population Logic

> Important: Vault does not accept JSON with comments. Remove all instructional comments before saving.

#### A. Application Secrets

Navigate to Secrets Engines > secrets and create a new version of the `application` secret.

|Key|Generation Logic / Source|
|---|---|
|`mongodb_password`|Secure alphanumeric password (min length 10).|
|`mongodb_replica_set_key`|Secure alphanumeric password (length 64).|
|`postgresql_password`|Secure alphanumeric password (min length 10).|
|`s3_secret_access_key`|Secure alphanumeric password (min length 10).|
|`ude_key`|Generated via UDE CLI: `cargo run key-gen`.|
|`spicedb_pre_shared_key`|If centralised, copy from `admin/fitfile/production/spicedb_secrets`.|
|`auth0_…`|Populated after Auth0 Terraform apply (see Auth0 section).|

Tenant Signing Keys:

To generate `fitfile_tenant_pkcs8.key` and `fitfile_tenant_public.crt`, run these commands locally:

```sh
`openssl genrsa -out keypair.pem 4096`
`openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key`
`openssl rsa -in keypair.pem -pubout -out publickey.crt`
```

#### B. SpiceDB Secrets

Populate the `spicedb` secret engine with:

- `postgresql_password`: Secure password (min 10 chars).
- `spicedb_preshared_key`: Must match the key used in Application secrets.

#### C. Monitoring (Grafana) Secrets

Navigate to the `monitoring` secret. Values are retrieved from the Central Services Grafana module output (`terraform output -json`).

- `prometheus_password`, `loki_password`, and `tempo_password` all use the same access policy token.
- Ensure `tempo_host` includes the port `:443`.

#### D. ArgoCD & Argo Workflows

- ArgoCD: Requires `admin_password` (hashed via `htpasswd`), GitLab deploy tokens for repository access, and Azure SSO client secrets.
- Argo Workflows: Primarily uses the same `postgresql` credentials as the main application.
