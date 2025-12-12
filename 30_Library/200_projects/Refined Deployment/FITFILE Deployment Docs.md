---
aliases: []
confidence: 
created: 2025-07-01T05:13:38Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Deployment Docs
type:
uid: 
updated: 
version:
---

## FITFILE Infrastructure and Platform Deployment Dependency Graph

The FITFILE Azure deployment process is broadly split into four main parts: Tooling, Infrastructure, Platform, and Application. While the provided documents primarily detail Azure deployments, some sections also cover AWS, where noted.

### Phase 0: Initial Prerequisites & Customer Setup

This phase involves critical setup steps and agreements that must be completed before the core deployment begins.

## Customer-Side Azure Account Preparation

The customer provides their Azure Tenant ID and Azure Subscription ID to FITFILE.

Register Resource Providers: The customer navigates to their subscription and registers the following resource providers: `Microsoft.ContainerService` (for Kubernetes Service), `Microsoft.ManagedIdentity` (for Kubernetes managed identities), `Microsoft.Network` (for networking infrastructure), `Microsoft.Storage` (for storage accounts), and `Microsoft.Compute` (for virtual machines).

Create Service Principal: The customer creates a services for e principal (e.g., "FITFILE Terraform Cloud Provisioner") within Azure AD, generates a secret, and copies the `secret id`, `value`, and `Application (client) ID`.

Assign Service Principal Roles: The service principal must be assigned the `Contributor` role and the `User Access Administrator` role (with a condition to constrain to `Network Contributor` role) on the subscription. These credentials (`ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET`) are later used by FITFILE in Terraform Cloud.

Enable Encryption at Host: The customer must enable `Enabled to use cryptionAtHost` on their subscription using Azure CLI (`az feature register --namespace microsoft.compute --name EncryptionAtHost`). This can take up to 20 minutes.

Adjust Compute Quota: The customer needs to ensure sufficient vCPU quota (e.g., for `Standard ESv5 Family vCPUs` with a limit of 10) in the deployment region (e.g., UK South) to avoid `QuotaExceeded` errors.

Add FITFILE DevOps User: The customer invites the designated FITFILE user to their Azure Tenant, changing their user type from Guest to Member, and assigns them the `Contributor` role on the subscription.

Configure Outbound Firewall Rules (if applicable): If a firewall is in place, outbound rules must be added to allow the FITFILE deployment to access FITFILE central services (e.g., HashiCorp, Auth0, Grafana, GitLab, Microsoft registries).

## FITFILE Workstation Setup

Check for required software: `tfenv`, `terraform` (with correct version), `azure-cli`, `last-pass`.

Set up a deployment directory and clone necessary repositories: `FITFILE development`, `UDE CLI`, `Central Services`.

3. Generate Deployment Key:
   In the `Central Services` repository, run `./short_name.sh` to generate a `deployment-key` (a unique identifier for the deployment, e.g., WM-Prod), based on the full customer name and environment. This key must be saved and used consistently.

4. AWS Specific Prerequisites (if deploying to AWS):
   AWS Account & Service Account: An AWS Account to deploy to and a Terraform service account user assigned to the `terraform-policy` role definition are required. The document lists extensive `kms`, `iam`, `ec2`, `network-firewall`, `elasticloadbalancing`, `route53`, and `eks` permissions for this role.
   Install AWS CLI & Session Manager Plugin: Install the latest AWS CLI and the Session Manager Plugin, ensuring symlinks are added to a directory in your PATH.
   Create & Configure AWS Access Key: Create an access key for your users via the IAM portal and run `aws configure` from the command line using the generated `access key id` and `secret`.
   Install RDP Client: Install an RDP client (e.g., Windows App).
   Configure EKS API Permissions: Tell the EKS API that your user has permission to make API calls by creating an access entry, selecting your user from the IAM Principal ARN list, and adding the `AmazonEKSClusterAdminPolicy`.

### Phase 1: Tooling (Central Services Configuration)

These tasks are typically performed by DevOps contributors responsible for Central Services tooling.

1. Vault Setup:
   Create Vault Resources: Navigate to `Central Services/hcp/vault` and add a new block to the `deployments` variable in `locals.tf` to define the secrets needed for the new deployment (e.g., `application`, `spicedb`, `cloudflare` (optional), `monitoring`, `argo-workflows`).
   Commit and push this change to trigger a Terraform Cloud plan and apply, which a DevOps engineer must manually approve.
   Populate Secrets: Login to the HCP Portal, generate an admin token for the Vault Dedicated instance, and sign in. Navigate to the `deployments/<deployment-name>` namespace and populate the JSON secrets for `application`, `spicedb`, `cloudflare` (if used), `ArgoCD`, and `Argo Workflows SSO`.
   `application` secrets include `mongodb_password`, `mongodb_username`, `mongodb_replica_set_key`, `postgresql_password`, `postgresql_username`, `s3_access_key_id`, `s3_secret_access_key`, `ude_key`, and `spicedb_pre_shared_key`.
   `spicedb` secrets include `postgresql_password`, `postgresql_username`, and `spicedb_preshared_key`.
   `cloudflare` secrets require an `api_token` generated from the Cloudflare portal.
   `ArgoCD` secrets include `admin_password`, `gitlab_deploy_token_password`, `gitlab_deploy_token_username`, and `sso_azure_client_secret`.
   `Argo Workflows SSO` secrets include optional `argo_sso_client_id`, `argo_sso_client_secret`, and required `postgresql_password`, `postgresql_username`.

2. UDE Secret Generation:
   Checkout the `UDE CLI` repository and run `rustup install nightly` (if needed).
   Run `cargo run -- key-gen` and copy the generated unique string (`ude_key`), which will be used in the `application` secret in Vault.

3. Auth0 Configuration:
   Retrieve the Azure Tenant ID and Subscription ID from the Azure Portal.
   Pull the `FITFILE Infrastructure` repository and navigate to `environments/fitfile/prod/auth0/main.tf` (or `non-prod`).
   Add a new block to the `fitfile_tenant_applications` map in `auth0/locals.tf` to configure the new `ffnode` application, specifying `tenant_name`, `api_name`, `api_audience` (DNS record for the ingress controller), and `enabled_apis`.
   Potentially add `additional_logout_redirect_urls` and `additional_web_origins` to `main.tf`.
   Apply these Terraform changes (commit, push, and manually apply in GitLab.com). This creates a new application in Auth0.
   Obtain the `client_id` and `client_secret` from the Terraform output, along with `webapp_application_client_credential` client ID and secret.
   Add these `auth0_client_id`, `auth0_client_secret`, `auth0_audience`, `auth0_frontend_client_id`, and `auth0_frontend_client_secret` values to the `application` secret in Vault.

4. Grafana Configuration:
   Navigate to `Central Services/grafana` and open `locals.tf`.
   Add a new key-value pair for the deployment to the `deployments` local variable (e.g., `stack = local.prod_stack`).
   Apply Terraform changes.
   Get the Terraform output for Grafana (e.g., `prometheus_host`, `prometheus_username`, `prometheus_password`, `loki_host`, `loki_username`, `loki_password`, `tempo_host`, `tempo_username`, `tempo_password`).
   Add these values to the `monitoring` secret in Vault.

### Phase 2: Infrastructure Deployment

This phase focuses on creating the cloud infrastructure (networking, compute resources, developer access). It differs based on the cloud provider.

1. Common Terraform Cloud & GitLab Setup:
   Terraform Cloud Workspace: Login to Terraform Cloud, select/create a Project, and create a Workspace named as the `<deployment-key>`.
   GitLab Repository: Login to GitLab, navigate to the `Customers` group (or create it), and create a new blank project with the same `<deployment-key>`.
   Clone the newly created GitLab repository locally.
   Terraform Login: Run `terraform login` from your local machine to get an access token from Terraform Cloud.

2. Option A: Azure Infrastructure (private):
   Workspace Variables: Add the `ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET` (from Phase 0) as environment variables to the Terraform Cloud workspace, marking all but `ARM_CLIENT_ID` as sensitive. Also, add a `admin_password` variable (randomly generated and saved in LastPass) for the jumpbox.
   Local File Setup: Create `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `providers.tf`, and `.gitignore` locally.
   Populate `versions.tf` with the Terraform Cloud config block from the workspace.
   Add the AzureRM provider configuration to `providers.tf`, replacing `tenant_id` and `subscription_id` with the correct values.
   Add an output block for `aks_cluster_outbound_ip_address` to `outputs.tf`.
   Populate `main.tf` with the `private-infrastructure` module block, specifying `deployment_key`, `admin_password`, and the `<latest_version>`. Optional `vm_sizes` can be set here.
   Add the `admin_password` variable declaration to `variables.tf`.
   Terraform Execution: Run `terraform init --upgrade`. Then, run `terraform apply` and approve the plan.
   Retrieve Output: Run `terraform output` to get the `aks_cluster_outbound_ip_address`, which will be added to Vault later.
   Connect to Azure Jumpbox: Login to the Azure portal, find the `FITFILEJumpbox` VM, and connect via the serial console. Log in as `azadmin` with the `admin_password`.
   Configure AWS CLI on Jumpbox: Run `az login` on the Jumpbox and select the customer's subscription.
   Get AKS Credentials: From the Azure portal, navigate to the AKS cluster, copy the command for "Download cluster credentials," and run it in the Jumpbox's SSH session.
   Verify Cluster Connection: Run `kubectl get nodes` to test the credentials.
   Populate Platform Variables on Jumpbox: Make `vars_setup.sh` executable (`chmod +x ./vars_setup.sh`) and run it (`./vars_setup.sh < /home/azadmin/.kube/config`) to populate `vars.tfvars` with cluster details.

3. Option B: AWS Infrastructure (private):
   Workspace Variables: Add `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` as environment variables to the Terraform Cloud workspace, marking the key and secret as sensitive.
   Local Repo Setup: Check access to the `terraform-aws-eks-private` repository and use it as a template for the new AWS deployment.
   Template Modification: Modify the template based on customer requirements, including `VM sizes`, `Region`, and `VPC CIDR range`.
   Terraform Execution: Commit and push the changes to your repo; this should trigger a Terraform Cloud workspace "Run". Approve the plan and monitor its progress.
   Run `terraform init --upgrade`. Then, run `terraform apply` and approve the plan.
   Retrieve Output: Run `terraform output` to get the `generated_password` for the `awsadmin` user (jumpbox).
   Connect to AWS Jumpbox: Start an SSM session to the `FITFILEJumpbox` instance, port-forwarding to port 3389. Open a remote desktop app (e.g., Windows App) and connect to `localhost:55679` using the `generated_password`.
   Check Cloud-Init Status: Once logged into the jumpbox, open a terminal and run `cloud-init status --wait` to ensure the script finished successfully. Verify that `aws cli`, `terraform`, and `kubectl` are installed.
   Configure AWS CLI on Jumpbox: Follow the `aws-cli configure` commands to set up the AWS CLI with your access token.
   Get EKS Credentials: Run `aws eks update-kubeconfig --region <region> --name <cluster-name>` to get the EKS credentials.
   Verify Cluster Connection: Run `kubectl get pods -A` to check the connection to the cluster's API server.

### Phase 3: Platform Deployment

This phase involves configuring the GitOps tooling inside the cluster and secret injection.

1. Connect to Jumpbox & Git Setup:
   Connect to the Jumpbox (as performed in the Infrastructure phase).
   Generate an SSH key with `ssh-keygen -t rsa` on the Jumpbox and add the public key to your GitLab account.
   Clone the `Private Platform Template` repository to the Jumpbox.

2. Modify Platform Template Files:
   Edit `vars.tfvars` on the Jumpbox, populating values such as `vault_address`, `deployment_key`, `deployment_repo_values_file_path`, `argocd_host`, `approles` (obtained from Vault output), `ingress_controller_ip_address`, `aks_cluster_ca_certificate`, and `aks_cluster_host`.
   Modify the `providers` blocks in `main.tf` to correctly reference the Kubernetes, Helm, and Kubectl providers.

3. Platform Terraform Apply:
   Run `terraform apply -var-file=vars.tfvars`. Note: You are likely to get an error initially because `ingress-nginx` is requesting AWS/Azure to create the load balancer, which takes time. Monitor the load balancer provisioning in the cloud console, and once it's active, run `terraform apply` again.

4. Post-Infrastructure Manual Configurations (for EKS):
   Storage Account: Modify the default `StorageClass` object called "gp2" to set `storageclass.kubernetes.io/is-default-class` to "true" and `reclaimPolicy` to `Retain`. Use `kubectl edit storageclass gp2`.
   CoreDNS: Edit the CoreDNS configmap (`kubectl edit configmap coredns -n kube-system`) to add a rewrite rule for hostnames (e.g., `app.ff-sandbox.privatelink.fitfile.net` to `ingress-nginx-controller.ingress-nginx.svc.cluster.local`) to prevent hairpin routing. Then restart CoreDNS pods (`kubectl rollout restart deployment/coredns -n kube-system`).
   Modify Loadbalancer ARN (mentioned but no details provided).
   Monitor ArgoCD: Monitor ArgoCD on its designated host (e.g., `argocd.privatelink.fitfile.net`).

5. Prepare Helm Value Overrides (Local Machine):
   Back on your local machine, clone/checkout the deployment repository (e.g., `feature/FFAPP-3073-new-ffnode-chart-with-vault-secrets` branch).
   Create or edit the values file at `ffnodes/<customer>/<deployment-key>/values.yaml`.
   Edit the template inside the file to set `namespace`, `targetRevision` (e.g., `latest-release` or a feature branch), `certManager`, `baseURL`, `managementApiAudience`, `host`, `defaultOrganisationAdminUserId`, `frontend features`, `mongodb` `replicaCount`, `minio` `size`, and optionally `argoWorkflows` SSO configuration.
   Commit and push these changes to your deployment repository.

6. Prepare Remaining Platform Variables (on Jumpbox):
   Set the missing values in the `vars.tfvars` file on the Jumpbox VM.
   `approles`: Go to the `central-services` repo on your local machine (`hcp/vault` directory) and run `terraform output -json | jq --arg prefix "<deployment-key>" ...` to get the `approles` JSON output. Convert this JSON to an HCL object and paste it into `vars.tfvars`.
   Set `deployment_key`.
   Set `deployment_values_file_path` (e.g., `/ffnodes/fitfile/wm-dev-1/values.yaml`).
   Set `argocd_host` (e.g., `wm-dev-1-argocd.privatelink.fitfile.net`).
   Set `aks_cluster_host` from the `/home/azadmin/.kube/config` file (the `clusters.cluster.server` property).
   Set `ingress_controller_ip_address` to the same value chosen in the `fitfile-private-infrastructure` module config.

7. Final Platform Terraform Execution (on Jumpbox):
   Run `terraform login` on the Jumpbox. Create a new API token in Terraform Cloud settings and paste it into the waiting script on the Jumpbox.
   Run `terraform init`.
   Run `terraform apply -var-file="./vars.tfvars"`. If it fails, try again as it might be a timing issue.
   Terraform State File Management: Once applied, copy the `terraform.tfstate` file off the Jumpbox and store it in a subdirectory within the GitLab Customers deployment repo (not in the root to avoid conflicts with remote state).

### Phase 4: Application Configuration

This is the final step, where the application configuration is created and the GitOps flow takes over.

1. ArgoCD Takeover: ArgoCD, configured in the platform step, now manages the application deployment based on the GitOps flow and the `helm value overrides` committed in Phase 3.
2. Post-Deployment Cluster Configuration (Manual):
   Spicedb Relationships: Create project relationships in each node's `spicedb` (e.g., `project_data_partner`, `project_host`) using `zed relationship create` commands.
   Update Deployment Config `values.yaml`: Update the `fitConnectCode` and `fitConnectHosts` configuration in the `values.yaml` for both partner and host nodes. The first element in `fitConnectHosts` MUST be the local fitconnect to the node.
   MongoDB Configuration: Port-forward into the host node's MongoDB pod, open a `mongosh` terminal, and insert `Tenants` and `Connections` documents.
   Assign User Roles: To allow users to see data sources/sets, assign the `data_source_manager` or `dataset_manager` role in both the host and data partner tenants (e.g., using `zed relationship create` for the host node).

3. Cloudflare Configuration (Optional DNS):
   If using Cloudflare as DNS, open the `Central Services` repository, navigate to `cloudflare`, and add entries for the deployment key to the `records` property in `locals.tf`, including for ArgoCD if exposed.

---

## Critical Questions & Upfront Considerations to Prevent Blocks

Based on the provided documentation, especially the `CUH deployment status` and `Errors encountered` sections, here are crucial questions and points to sort out upfront to improve the deployment process:

### I. Customer & Account Prerequisites

Azure Resource Provider Registration: Has the customer confirmed all necessary Azure Resource Providers (`Microsoft.ContainerService`, `Microsoft.ManagedIdentity`, `Microsoft.Network`, `Microsoft.Storage`, `Microsoft.Compute`) are registered on their subscription before deployment starts?

Azure Compute Quota: Has the customer confirmed sufficient vCPU quota (e.g., for `Standard ESv5 Family vCPUs`) in the target region, or submitted a quota increase request if needed? What is the current limit, current usage, and additional required?

Azure Encryption at Host: Has `EncryptionAtHost` been enabled on the customer's subscription, and has its registration status been confirmed as "Registered"?

Azure ACR Cross-Tenant Access: If using Azure Container Registry (ACR), how will cross-tenant access be handled for private clusters? Will a private link be established, or will Docker pull secrets be manually injected? (The document notes that the ACR is public currently and a private link is needed for private clusters).

FITFILE DevOps User Access: Have the designated FITFILE DevOps engineers been added as `Contributor` to the customer's AWS Account or Azure Tenant/Subscription?

### II. Networking & Firewall Rules (Customer & Telefonica/CUH)

Outbound Allow List: If the customer has a firewall, have all necessary outbound rules for FITFILE central services and AKS Microsoft resources been explicitly added to their allow list?

Networking Setup to CUH On-Premise: What is the definitive status of the networking setup through Telefonica to the CUH on-premise network? Are the initial firewall rules (sent by FITFILE) implemented correctly by Telefonica?

Routing Between Firewalls: Has the routing issue between the Telefonica firewall and the CUH on-premise firewall been resolved? Is Telefonica forwarding traffic correctly to the CUH network?

Internet Proxy on FITFILE VMs: Is a proxy configuration required on the FITFILE VMs in Azure to resolve internet access issues (bypassing the CUH on-premise firewall)? What is the timeline for this change process, and what are the implications for future upgrades if resources bypass the firewall?

Domain Names for FITFILE APIs: What are the specific domain names CUH will expose for the FITFILE APIs? These are needed for configuring `fitConnectHosts` in the HIE node deployment config.

### III. Credentials & Data Access

SQL Database Credentials: What type of SQL credentials will CUH provide for the Bunny application and the FITFILE system to access OMOP and source data? (Initially, service account was discussed, but the application only works with username/password, which will be a CUH AD username and password post-review). Have these credentials been provided and verified?

MS SQL Server Connection Settings: What are the specific MS SQL Server connection settings required for the deployment configuration?

OMOP Data Source: Has the OMOP Data source been added to the project via an API call?

Auth0 User Provisioning: What is the status of fixing the Auth0 email engine? Are the users added to the Auth0 production tenant, and are there API calls to add them via the Serial Console of the Jumpbox?

GitLab Customers Group Link: The documentation mentions "Can't find link" for the GitLab Customers group. Is there an updated or correct link available?

### IV. Deployment Configuration & Automation

Terraform Module Versions: Which is the `<latest_version>` to use for the `private-infrastructure` module in Azure? How are we ensuring that the correct and latest module versions are consistently used across deployments?

DNS Entry Conflicts: Be aware that existing DNS entries in the customer's account can block Terraform from creating them. How will we pre-check for existing DNS entries to avoid `terraform apply` failures?

Manual Steps in Platform Deployment: Many steps in the Platform deployment are manual (e.g., SSH key generation, modifying `vars.tfvars` on jumpbox, copying `terraform.tfstate`). Are there plans to automate these manual file modifications and transfers to reduce human error and speed up deployment?

Vault Secret Generation: The current Vault process involves manual login and population of secrets using admin tokens, with JSON to HCL conversion. Are there plans to automate secret generation and injection to enhance security and efficiency?

Auth0 Module Automation: The Auth0 module is currently not under Terraform for creating new applications, requiring manual passing of secrets to Vault. Is there a plan to integrate this fully into Terraform?

CoreDNS and StorageClass Configurations: The CoreDNS rewrite and StorageClass modifications are manual post-apply steps. Can these be integrated into the Terraform deployment or a pre/post-hook script?

Load Balancer Provisioning: The `terraform apply` for platform may need to be run twice due to load balancer provisioning time. Can this be handled with `depends_on` or retries in a CI/CD pipeline?

---

This detailed breakdown should give you a clear understanding of the dependencies and potential blocking points. It highlights where pre-work, confirmation with the customer, or internal process improvements are needed.

Would you like me to elaborate on any specific step, or perhaps explore solutions for some of the identified blocking points? I can also quiz you on the deployment stages if you'd like to test your understanding!
