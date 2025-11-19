---
aliases: []
confidence: 
created: 2025-11-19T09:07:06Z
epistemic: 
last_reviewed: 
modified: 2025-11-19T09:28:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: NNUH Deployment
type: 
uid: 
updated: 
---

- Gitlab repo
   - Some trouble with the GITLAB_TOKEN.
- Create the TFC workspace
## Deployment Plan: Azure AKS Private Cluster

### Phase 1: Prerequisites & Workstation Setup
**Reference:** `FITFILE-240628 - Azure Deployment Process`

Before touching Azure or Terraform, ensure your local environment is ready.

1.  **Install Software:**
    - `tfenv` and `terraform` (ensure version matches current standards, usually `>=1.9.0`).
    - `azure-cli`.
    - LastPass (for password generation).
2.  **Clone Repositories:**
    - `FITFILE development` (or production)
    - `UDE CLI`
    - `Central Services`
3.  **Generate Deployment Key:**
    - Navigate to `Central Services`.
    - Run `./short_name.sh`.
    - Input customer name and environment (e.g., Dev, Prod).
    - **Save the output.** This key (e.g., `wm-dev-1`) is used everywhere.

---

### Phase 2: Azure Tenant Preparation
**Reference:** `FITFILE-Deploy into a new Azure Tenant` & `Customer Checklist`

These steps are performed inside the Customer's Azure Portal.

#### 1. Resource Providers

Register the following providers in the target Subscription:

- `Microsoft.ContainerService`
- `Microsoft.ManagedIdentity`
- `Microsoft.Network`
- `Microsoft.Storage`
- `Microsoft.Compute`

#### 2. Access & Identity
1.  **Create Service Principal:**
    - App Registrations -> New Registration -> Name: `FITFILE Terraform Cloud Provisioner`.
    - Create a Client Secret. **Save Value and Secret ID**.
    - **Save Application (client) ID**.
2.  **Assign Roles (Subscription Level):**
    - **Contributor**: Assign to the Service Principal.
    - **User Access Administrator**: Assign to the Service Principal, but **add a condition**:
        - Constrain roles -> Assignable roles: Select only `Network Contributor`.
3.  **Invite DevOps User:**
    - Entra ID -> Users -> Invite External User.
    - Invite the FITFILE DevOps engineer.
    - Change User Type from "Guest" to "Member".
    - Assign `Contributor` role on the Subscription to this user.

#### 3. Infrastructure Limits
1.  **EncryptionAtHost:**
    - Run: `az feature register --namespace Microsoft.Compute --name EncryptionAtHost`.
    - Wait for registration, then propagate.
2.  **Compute Quotas:**
    - Subscription -> Usage & Quotas.
    - Filter for **Standard ESv5 Family vCPUs** (UK South).
    - Request quota increase (Min 10 vCPUs required).

---

### Phase 3: Central Services & Tooling
**Reference:** `FITFILE-Azure - Tooling`

Configure the central management plane to accept the new cluster.

#### 1. Vault Configuration
1.  Navigate to `Central Services/hcp/vault`.
2.  Edit `locals.tf`: Add the deployment block.

    ```hcl
    "<deployment_key>" = {
      secrets = tomap({
        "application" = {},
        "spicedb" = {},
        "cloudflare" = {},
        "monitoring" = {},
        "argo-workflows" = {},
      })
    }
    ```

3.  Commit, push, and apply in Terraform Cloud (HCP Terraform).
4.  **Populate Secrets:** Go to the Vault UI (`admin/deployments/<key>`) and populate:
    - `application`: DB passwords (generate secure strings), UDE key.
    - `spicedb`: Postgres creds.
    - `cloudflare`: API Token (Edit DNS permissions).
    - `argo-workflows`: SSO Client ID/Secret (if applicable).

#### 2. Auth0 Configuration
1.  Navigate to `Central Services/auth0/<env>`.
2.  Edit `locals.tf`: Add the new tenant configuration (API Identifier, Tenant Name).
3.  Apply via Terraform.
4.  **Capture Outputs:** Note `client_id` and `client_secret` from the output.
5.  **Update Vault:** Add these Auth0 credentials to the `application` secret in Vault created in step 3.1.

#### 3. Grafana Configuration
1.  Navigate to `Central Services/grafana`.
2.  Edit `locals.tf`: Add deployment key to `deployments` map.
3.  Apply via Terraform.
4.  **Update Vault:** Take the output (Prometheus/Loki/Tempo endpoints and users) and update the `monitoring` secret in Vault.

---

### Phase 4: Infrastructure Deployment
**Reference:** `FITFILE-Azure - Infrastructure (private)`

Deploy the actual Azure resources (VNet, AKS, Jumpbox).

#### 1. Terraform Cloud Setup
1.  Create a new Workspace in **FITFILE-Platforms** project. Name: `<deployment-key>`.
2.  **Configure Variables (Environment, Sensitive):**
    - `ARM_CLIENT_ID` (Service Principal ID)
    - `ARM_CLIENT_SECRET` (SP Secret Value)
    - `ARM_ACCESS_KEY` (SP Secret ID)
    - `ARM_SUBSCRIPTION_ID`
    - `ARM_TENANT_ID`
    - `TF_VAR_admin_password` (Generate a secure password for the Jumpbox).

#### 2. GitLab Repository Setup
1.  Create a new Private project in `fitfile/customers`. Name: `<deployment-key>`.
2.  Clone locally.
3.  Create files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `providers.tf`.
4.  **Versions.tf:** Configure the `cloud` block to point to the Workspace created above.
5.  **Main.tf:**

    ```hcl
    module "private-infrastructure" {
      source = "app.terraform.io/FITFILE-Platforms/private-infrastructure/azure"
      version = "<latest>"
      deployment_key = "<deployment-key>"
      admin_password = var.admin_password
    }
    ```

6.  **Outputs.tf:** Expose `aks_cluster_outbound_ip_address`.

#### 3. Deploy
1.  `terraform login`.
2.  `terraform init`.
3.  `terraform apply`.
4.  **Record the Output:** Note the `aks_cluster_outbound_ip_address` (required for allow-listing if the customer has a firewall).

---

### Phase 5: Platform Configuration
**Reference:** `FITFILE-Azure - Platform (private)`

Configure the software running inside the cluster via the Jumpbox.

#### 1. Generate AppRoles
1.  In `Central Services/hcp/vault`, run the `jq` script to extract Role IDs and Secret IDs for the new deployment.
2.  Convert the JSON output to HCL format (save this safely, you will need it for the Jumpbox).

#### 2. Connect to Jumpbox
1.  Azure Portal -> VM (`FITFILEJumpbox`) -> Serial Console.
2.  Login as `azadmin` using the `admin_password` set in Phase 4.
3.  Run `az login`.

#### 3. Jumpbox Configuration
1.  Run `./vars_setup.sh < /home/azadmin/.kube/config`.
    - *Verify:* `cat vars.tfvars` should show certificate data.
2.  **Populate `vars.tfvars`:** Edit the file on the Jumpbox to include:
    - `approles = { ... }` (The HCL object generated in step 5.1).
    - `deployment_key`.
    - `argocd_host` (e.g., `key-argocd.privatelink.fitfile.net`).
    - `ingress_controller_ip_address` (from infra module output).
3.  **Terraform Login:** Run `terraform login` on the Jumpbox (create a User Token in TFC settings if needed).

#### 4. Prepare Helm Overrides (Local Machine)
1.  Checkout the `Deployment` repository.
2.  Create file: `ffnodes/<customer>/<deployment-key>/values.yaml`.
3.  Populate using the template (Configure `namespace`, `deploymentkey`, `oauth`, `appConfig`).
4.  Commit and push to the `latest-release` branch (or feature branch if testing).

#### 5. Apply Platform (Jumpbox)
1.  On the Jumpbox: `terraform init`.
2.  `terraform apply -var-file="./vars.tfvars"`.

#### 6. Finalise
1.  **State Backup:** Copy the `terraform.tfstate` from the Jumpbox to a subdirectory in the Customer GitLab repository (created in Phase 4). **Do not put it in the root.**
2.  **DNS:** Ensure Cloudflare/DNS records are updated with the Ingress IP.
