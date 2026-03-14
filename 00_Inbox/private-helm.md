---
created: 2026-01-15T15:14:21+00:00
modified: 2026-03-14T11:10:50+00:00
title: private-helm
---

## Azure Platform Deployment Guide

### Deploy the Platform

By now, the infrastructure has been created and central tooling has been configured. The platform is deployed via the SSH jumpbox created previously.

#### 1. Prepare AppRoles

This involves sensitive HCL Terraform variables. You must retrieve these values from the HCP Vault workspace.

- Check out the central services repo and navigate to the `vault` directory.
- Run the following command, replacing `<replace-with-deployment-key>` with your specific deployment key:

```bash
terraform output json | jq-arg prefix "<replace-with-deployment-key>"

```

- Alternatively, use the improved script to output HCL directly:

```bash
terraform output json | jq-arg prefix "<replace-with-deployment-key>"' .deployments_approle_roles.value as $roles | .deployments_approle_secret_ids.value | to_entries | map(select(.key | startswith($prefix)) | if .key == $prefix then {key: "argocd", value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}} else {key: (.key | gsub("^" + $prefix + "\\.";"")), value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}} end ) | from_entries' > ./tmp.json && echo "jsondecode(file(\"./tmp.json\"))" | terraform console

```

- Note: Convert the JSON output to an HCL object. It is recommended to set browser dev tools to "offline" when using online converters to ensure secrets are not leaked.

#### 2. Connect to the SSH Jumpbox

Ensure you have "Contributor" permissions on the subscription.

1. Login to the Azure portal and switch to the customer's directory.
2. Navigate to the resource group (e.g., `wm-dev-1-rg`).
3. Select the FITFILEJumpbox VM and click Connect.
4. Select More ways to connect, then click Go to serial console.
5. If the console appears inactive, press Enter.
Login: Enter `azadmin` as the username.
Password: Use the `admin_password` value from the infrastructure deployment Terraform workspace.

#### 3. Configure Azure CLI and Cluster Access

1. Run `az login`.
2. Open a new browser tab, navigate to the provided link, and enter the code displayed in the terminal.
3. Select the customer subscription from the list once logged in.
4. Verify the correct tenant by running `az account show`.
5. In the Azure portal (different tab), navigate to the AKS cluster, click Connect, and copy the "Download cluster credentials" command.
6. Paste and run that command in the SSH jumpbox.
7. Test the connection by running `kubectl get nodes`.

#### 4. Prepare Deployment Variables

The jumpbox should contain `main.tf`, `vars.tfvars`, and `vars_setup.sh`.

1. Make the setup script executable: `chmod +x./vars_setup.sh`.
2. Copy the kube config to the tfvars file: `./vars_setup.sh < /home/azadmin/.kube/config`.
3. Confirm the population of cluster variables (certificate, key, host) using `cat vars.tfvars`.

#### 5. Prepare Helm Value Overrides

1. On your local machine, clone the deployment repository and check out the specific feature branch (e.g., `feature/FFAPP-3073…`).
2. Create a values file at `ffnodes/<customer>/<deployment-key>/values.yaml`.
3. Populate the `values.yaml` using the provided template, ensuring the `deploymentKey`, `baseURL`, `host`, and `defaultOrganisationAdminUserId` are correctly set.
4. Commit and push the changes to the feature branch.

#### 6. Populate Remaining Platform Variables

In the `vars.tfvars` file on the jumpbox, set the following:

approles: The HCL object generated in Step 1.

deployment_key: Set to your deployment key (e.g., `wm-dev-1`).

deployment_values_file_path: The relative path to the `values.yaml` created in Step 5.

argocd_host: The DNS record for the ArgoCD app.

aks_cluster_host: Found in `~/.kube/config` under `clusters.cluster.server`.

ingress_controller_ip_address: Must match the value in the infrastructure module config.

#### 7. Initialize and Apply Terraform

1. Run `terraform login` and follow the prompts to create an API token on `app.terraform.io`.
2. Paste the token into the SSH console.
3. Run `terraform init`.
4. Apply the configuration: `terraform apply -var-file="./vars.tfvars"`.
Post-Apply: Copy the `terraform.tfstate` file from the box and store it in a subdirectory within the GitLab deployment repo (do not store it in the root).

---

### Appendix

#### Cloudflare (Optional)

If using Cloudflare for DNS, add the records in `locals.tf` within the central services repository for the deployment key and ArgoCD.

#### Generating Secure Passwords

Per company policy, use the LastPass generator to create 64-character passwords including lowercase, uppercase, and numbers.

#### Creating Virtual Network Gateway

When creating a Virtual Network Gateway in Azure, ensure the following settings are used:

Gateway type: VPN or ExpressRoute (as required).

SKU: Standard.

Virtual network: aks.

Public IP address: Create new (e.g., `dev-access`).

Would you like me to help you format the specific `values.yaml` template mentioned in the instructions?
