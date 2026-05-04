# Deployment - Infrastructure (private) - FITFILE

- 1 [Terraform Cloud](#Terraform-Cloud)

- 2 [GitLab](#GitLab)

In this section, we will setup the terraform infrastructure deployment for a private cluster in Azure. Ensure you have completed the previous steps before beginning this one.

These tasks need to be performed by DevOps contributors who are responsible for the Central Services tooling.

This customer deploy will be referenced with what we are calling a deployment-key. This is the short name FITFILE uses for the specific ustomer everywhere in the infrastructure. Do not use the full name of the customer but something like WM-Prod. Make sure to keep this consistent where ever you use it. It is important

## Terraform Cloud

Next we need to create the workspace for the new deployment and setup the CI/CD.

1. Login to Terraform cloud: [HCP Terraform](https://app.terraform.io/app/FITFILE-Platforms/)

2. Select Projects in the sidebar, and click **New Project**, or reuse a project if it is for the same customer.

   

   

3. Create a Workspace within that project with the name as the <deployment-key>

   

   

4. Now we are going to add variables for the ARM keys. Ensure they are all **environment variables** and mark all bar the client id as sensitive.

   1. ARM_CLIENT_ID == the application id of the enterprise application/service principal

   2. ARM_ACCESS_KEY == Secret_id of the secret you created in the azure tenant

   3. ARM_CLIENT_SECRET == Value of the secret you created in azure tenant

5. We also need to add a variable for the admin password for the jumpbox we will create. This is a terraform variable called `admin_password`. This should be a randomly generated secure password. ideally 20+ characters long. You can generate it from LastPass password generator. **Make sure you save it in LastPass as you will need it later to login to the jumpbox!**

6. Go back to the overview, and copy the terraform config block:

## GitLab

We are going to create a new customer deployment repository in GitLab to isolate the configuration and manage access

1. Login to gitlab

2. Navigate to the Customers group: <https://gitlab.com/fitfile/customers>

3. Click New Project

4. Click Create blank project

5. For the project name, enter the same **deployment key** as before:

6. Click on Code drop down and copy the SSH key

7. Git clone locally. We suggest creating a “customers” folder to clone into.

8. cd into the cloned repo

9. Run this command to create comes files we will populate:

   `touch main.tf variables.tf outputs.tf versions.tf providers.tf .gitignore && echo ".tfstate\n.tfstate.\n.terraform/\nterraform.tfvars\n.tfvars" > .gitignore`

10. Paste the previously copied terraform block (form the workspace) into the [versions.tf](http://versions.tf/ "http://versions.tf") file. And add the following so your file looks like this (with a different workspace name)

   `terraform { cloud { organization = "FITFILE-Platforms" workspaces { name = "wm-dev-1" } } required_version = ">= 1.9.0" required_providers { azurerm = { source = "hashicorp/azurerm" version = "3.93.0" } } }`

11. In the [providers.tf](http://providers.tf/ "http://providers.tf") file, copy the following, replacing the tenant_id and subscription_id with the proper values.

   `provider "azurerm" { features { resource_group { prevent_deletion_if_contains_resources = false } } tenant_id = "9559219e-bc8b-44dc-9ac1-3f2d080a6875" subscription_id = "714b1dbd-8a9a-4d64-9397-53ed8c459bb3" skip_provider_registration = true }`

12. In the [outputs.tf](http://outputs.tf/ "http://outputs.tf") file, add the following block:

   `output "aks_cluster_outbound_ip_address" { value = module.private-infrastructure.load_balancer_outbound_ip }`

13. In the [main.tf](http://main.tf/ "http://main.tf") file, we will are going to populate a module block. We can get this code block from the module registry: <https://app.terraform.io/app/FITFILE-Platforms/registry/modules/private/FITFILE-Platforms/private-infrastructure/azure>

   `module "private-infrastructure" { source = "app.terraform.io/FITFILE-Platforms/private-infrastructure/azure" version = <latest_version> deployment_key = "wm-dev-1" # replace with your deployment key admin_password = var.admin_password }`

Make sure to get the current private-infrastructure module version and replace <latest_version> in the block.

If the customer does not want to use the ESv5 family of vCPUs, they can override the vm_sizes like so:

`module "private-infrastructure" { source = "app.terraform.io/FITFILE-Platforms/private-infrastructure/azure" version = <latest_version> deployment_key = "wm-dev-1" additional_node_pool_vm_size = "Standard_DS2_v2" default_node_pool_vm_size = "Standard_DS2_v2" admin_password = var.admin_password }`

We can set the `additional_node_pool_vm_size` and the `default_node_pool_vm_size` values to whatever they prefer, however, boxes with only 2cpus are not recommended as a large proportion of the available vCPU is consumed by daemon set pods which run on every node.

1. In the [variables.tf](http://variables.tf/ "http://variables.tf") file, we need to add the `admin_password` variable

   `variable "admin_password" { description = "The password for the jumpbox admin user" type = string sensitive = true }`

2. `terraform login` to get the token you need. This should take you to terraform cloud to get the access token. The CLI will prompt you through the experience.

3. Save the files, and then run `terrafrom init --upgrade`

4. Run `terraform apply` and check the plan before entering “yes” when prompted.

For now, the module configures the Kubernetes Cluster to use the [loadBalancer outboundType](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype#outbound-type-of-loadbalancer "https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype#outbound-type-of-loadbalancer"). This means the egress has an assigned public ip address.

Different customers may require different types here:

- `loadBalancer` - (default) assigns a public ip address for egress

- `userDefinedRouting` - used if you want the cluster behind a Firewall

- `managedNATGateway` and `userAssignedNATGateway` - if you want the cluster behind a NATGateway

1. Run `terraform output` to get the `aks_cluster_outbound_ip_address` if using loadBalancer for outbound traffic. We will add this to Vault in the next step.

Be the first to add a reaction



Source: <https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839202366/Deployment+-+Infrastructure+private>