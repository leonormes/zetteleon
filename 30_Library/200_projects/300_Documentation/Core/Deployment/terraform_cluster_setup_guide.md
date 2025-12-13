---
aliases: []
confidence: 
created: 2024-10-30T14:37:49Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: terraform_cluster_setup_guide
type:
uid: 
updated: 
version:
---

## Terraform_Cluster_Setup_Guide

- Azure Tenant
- Azure Subscription in the tenant
- Azure Subscription has registered the use of Resource Providers

### Register Resource Providers in Subscription

Resource providers can be identified by the resources that need them on this page:

1. Navigate to the subscription
2. In the side panel, click on Resource Providers
3. Register the following (one-by-one)
    1. Microsoft.ContainerService - for Kubernetes Service
    2. Microsoft.ManagedIdentity - for kubernetes managed identities
    3. Microsoft.Network - for networking infrastructure
    4. Microsoft.Storage - for storage accounts

## Process

### Configure Auth0

As we use Auth0 for our identity tokens, we need to configure Auth0 to know about the new

1. Login to your azure tenant and copy the tenant_id. navigate to Microsoft Entra ID, and go to overview. Also get the subscription id
2. Pull this repo:
3. cd to environments/fitfile/prod/auth0/main.tf
4. Add a new ffnode application and register it by making the following changes:
5. Commit and push and run the pipeline in
6. This should create a new application in auth0:

    We will need the client_id and client_secret later when we create the terraform variables.

7. Git clone the fitfile-development repository (this may be fitfile-production if it is a production deployment)
8. Open the create_new_cluster.sh script in the root, and modify the terraform project key:
9. Run the script to generate the cluster. The name must be conform to the following regular expression

```sh
./new_cluster_called.sh <cluster-name>
```

    This should create the Terraform workspace within the project - YOU MAY NEED TO CREATE THE PROJECT FIRST if it doesn’t already exist

    Once complete you will have a new folder with the name of the cluster you provided to the script

10. CD into the cluster-name’d folder. Go to providers.tf and modify the tenant_id on line 18 and 22, and subscription_id on line 23:
11. Back in Azure portal Create Enterprise Application
12. This creates an app registration. You can navigate to this and create a certificate/secret:
13. Create new secret. Recommended default lifetime of the secret is 6 months, but depends on policy of customer.
14. Go to the workspace, and go to variable. Create 2 new terraform variables:
    1. application_secrets_map:

```json
{
auth0_client_id = "", // use the Auth0 client id from before
auth0_client_secret = "", // use the Auth0 client secret from before
auth0_frontend_client_id = "", // use existing FITFILE SPA application client id
auth0_frontend_client_secret = "", // use existing FITFILE SPA application client secret
cli_auth0_client_id = "", // Not needed - do not need to fill
cli_auth0_client_secret = "", // Not needed - do not need to fill
mesh_client_cert = "", // Not needed for environments that don't need optout
mesh_client_key = "", // Not needed for environments that don't need optout
mesh_hash_secret = "", // Not needed for environments that don't need optout
mesh_mailbox_password = "", // Not needed for environments that don't need optout
mongodb_password = "", // randomly generate secure password
mongodb_username = "root", // we don't have platformers users yet!
postgresql_password = "", // randomly generate secure password
postgresql_username = "postgres", // we don't have platformers users yet!
rabbitmq_password = "", // randomly generate secure password
rabbitmq_username = "ffadmin", // we don't have platformers users yet!
s3_access_key_id = "", // randomly generate secure password
s3_secret_access_key = ""ffadmin, // we don't have platformers users yet!
sleuth_api_key = "", // Not needed
spicedb_pre_shared_key = "" // This may be different based on whether you use centralised spicedb or not. If centralised, get it from vault from admin/fitfile/production/spicedb_secrets. Otherwise, get from spicedb_secrets you will create
}
```

2. spicedb_secrets (only needed if not using centralised spicedb

```sh
{
postgresql_password = "", // randomly generate secure password
postgresql_username = "postgres",
spicedb_preshared_key = "" // radonly generated and shared within application_secrets
}
```

3. cloudflare_issuer_api_token (only need if we haven’t moved this to a reusable variable set)!

Should look something like this:

15. Create a new Variable set in Terraform Cloud
Login, Go to Settings → Variable Sets

16. Add to the variable set the following. Set all the following to environment variables and set all bar the client_id as sensitive (this restricts them from showing in the UI)
- ARM_ACCESS_KEY == Secret_id of the secret you created in the azure tenant
- ARM_CLIENT_SECRET == Value of the secret you created in azure tenant
- ARM_CLIENT_ID == the application id of the enterprise application
- You will also want to add the CLOUDFLARE_API_TOKEN. (hopefully by the time you are using this, the token is in its own variable set which can be reused across terraform projects/workspaces

17. Add the new variable set and the following existing variable sets to the project and/or workspace
18. Your New Variable Set
19. FITFILE Vault Configuration
20. Now go back to the fitfile-development repo and within your cluster folder, run:

```sh
terraform plan
```

19. Now run

```sh
terraform apply
```

20. Once finished, the cluster should be created with ArgoCD deployed. Because we used a workaround for error number 4, by commenting out the aks_to_acr_role resource block from the main.tf file, we need to manually injected an ACR secret.

## Errors Encountered

1. We had to :

```sh
Error: creating Kubernetes Cluster (Subscription: "35e4be95-fb89-4da6-89c6-f102c04517e8"
│ Resource Group Name: "fitfile-cloud-ollie-rg"
│ Kubernetes Cluster Name: "fitfile-cloud-ollie-aks-cluster"): performing CreateOrUpdate: Put "https://management.azure.com/subscriptions/35e4be95-fb89-4da6-89c6-f102c04517e8/resourceGroups/fitfile-cloud-ollie-rg/providers/Microsoft.ContainerService/managedClusters/fitfile-cloud-ollie-aks-cluster?api-version=2023-06-02-preview": The Resource Provider was not registered
│
│ Resource Providers (APIs) in Azure need to be registered before they can be used - however the Resource
│ Provider was not registered, and calling the API returned the following error:
│
│ The subscription is not registered to use namespace 'Microsoft.ContainerService'. See https://aka.ms/rps-not-found  for how to register subscriptions. >
│
│ The Azure Provider by default will automatically register certain Resource Providers at launch-time,
│ whilst it's possible to opt-out of this (which you may have done)
│
│ Please ensure that this Resource Provider is properly registered, you can do this using the Azure CLI
│ for example to register the Resource Provider "Some.ResourceProvider" is registered run:
│
│ > az provider register --namespace "Some.ResourceProvider"
│
│ Resource Providers can take a while to register, you can check the status by running:
│
│ > az provider show --namespace "Some.ResourceProvider" --query "registrationState"
│
│ Once this outputs "Registered" the Resource Provider is available for use and you can re-run Terraform.
│
│
│   with module.aks.azurerm_kubernetes_cluster.main,
│   on .terraform/modules/aks/main.tf line 13, in resource "azurerm_kubernetes_cluster" "main":
│   13: resource "azurerm_kubernetes_cluster" "main" {
```

2. Limited number of vCores allowed in subscription:

```sh
module.aks.azurerm_kubernetes_cluster.main: Creating...
╷
│ Error: creating Kubernetes Cluster (Subscription: "35e4be95-fb89-4da6-89c6-f102c04517e8"
│ Resource Group Name: "fitfile-cloud-ollie-rg"
│ Kubernetes Cluster Name: "fitfile-cloud-ollie-aks-cluster"): performing CreateOrUpdate: unexpected status 400 with response: {
│   "code": "QuotaExceeded",
│   "details": null,
│   "message": "Preflight validation check for resource(s) for container service fitfile-cloud-ollie-aks-cluster in resource group MC_fitfile-cloud-ollie-rg_fitfile-cloud-ollie-aks-cluster_uksouth failed. Message: Operation could not be completed as it results in exceeding approved Total Regional Cores quota. Additional details - Deployment Model: Resource Manager, Location: uksouth, Current Limit: 4, Current Usage: 0, Additional Required: 8, (Minimum) New Limit Required: 8. Setup Alerts when Quota reaches threshold. Learn more at https://aka.ms/quotamonitoringalerting . Submit a request for Quota increase at https://aka.ms/ProdportalCRP/#blade/Microsoft_Azure_Capacity/UsageAndQuota.ReactView/Parameters/%7B%22subscriptionId%22:%2235e4be95-fb89-4da6-89c6-f102c04517e8%22,%22command%22:%22openQuotaApprovalBlade%22,%22quotas%22:[%7B%22location%22:%22uksouth%22,%22providerId%22:%22Microsoft.Compute%22,%22resourceName%22:%22cores%22,%22quotaRequest%22:%7B%22properties%22:%7B%22limit%22:8,%22unit%22:%22Count%22,%22name%22:%7B%22value%22:%22cores%22%7D%7D%7D%7D]%7D by specifying parameters listed in the ‘Details’ section for deployment to succeed. Please read more about quota limits at https://docs.microsoft.com/en-us/azure/azure-supportability/regional-quota-requests. Details: ",
│   "subcode": ""
│  }
│ 
│   with module.aks.azurerm_kubernetes_cluster.main,
│   on .terraform/modules/aks/main.tf line 13, in resource "azurerm_kubernetes_cluster" "main":
│   13: resource "azurerm_kubernetes_cluster" "main" {
│ 
╵
Operation failed: failed running terraform apply (exit 1)
```

Solution: either increase vCore allowance in subscription, OR reduce VM sizes

```sh
module "aks" {
source  = "app.terraform.io/FITFILE-Platforms/aks/azure"
...

default_node_pool_max_count                   = 2
default_node_pool_min_count                   = 1
workflows_node_pool_max_count         = 1
}
```

3. EncryptionAtHost not enabled in subscription

```sh
│ Error: creating Kubernetes Cluster (Subscription: "35e4be95-fb89-4da6-89c6-f102c04517e8"
│ Resource Group Name: "fitfile-cloud-ollie-rg"
│ Kubernetes Cluster Name: "fitfile-cloud-ollie-aks-cluster"): performing CreateOrUpdate: unexpected status 400 with response: {
│   "code": "SubscriptionNotEnabledEncryptionAtHost",
│   "details": null,
│   "message": "Subscription does not enable EncryptionAtHost.",
│   "subcode": ""
│  }
│ 
│   with module.aks.azurerm_kubernetes_cluster.main,
│   on .terraform/modules/aks/main.tf line 13, in resource "azurerm_kubernetes_cluster" "main":
│   13: resource "azurerm_kubernetes_cluster" "main" {
│ 
╵
Operation failed: failed running terraform apply (exit 1)
```

Solution: Run this command using the azure CLI:

```sh
az feature register --namespace microsoft.compute --name EncryptionAtHost

Register-AzProviderFeature -FeatureName "EncryptionAtHost" -ProviderNamespace "Microsoft.Compute"
```

4. ACR cross-tenant access:

```sh
Error: loading Role Definition List: unexpected status 401 with error: InvalidAuthenticationTokenTenant: The access token is from the wrong issuer 'https://sts.windows.net/29e004ae-2eba-4db3-aa4b-986053570a0e/'. It must match the tenant 'https://sts.windows.net/45e73aa3-1ee9-47c0-ba25-54eda9da021a/' associated with this subscription. Please use the authority (URL) 'https://login.windows.net/45e73aa3-1ee9-47c0-ba25-54eda9da021a' to get the token. Note, if the subscription is transferred to another tenant there is no impact to the services, but information about new tenant could take time to propagate (up to an hour). If you just transferred your subscription and see this error message, please try back later.
with azurerm_role_assignment.aks_to_acr_role
on main.tf line 35, in resource "azurerm_role_assignment" "aks_to_acr_role":
resource "azurerm_role_assignment" "aks_to_acr_role" {
```

Solution: Create a private link between the 2 tenants

[https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-link](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-link)

1. I created a virtual network in the azure shared services subscription with default configuration
2. I created a private endpoint and link it to a record in a new private dns zone
3. Decided to stop here as I realised we can do something simpler. Just manually add the docker-pull secret to the k8s cluster…

### TODO

- Grafana agent configuration in terraform
- ACR private link and integration (less secure alternative is to deploy an ACR docker-pull secret via terraform. But for private clusters, we need this anyway - right now our ACR is public!!!)
- DONE - CreateNamespace=true sync policy on ArgoCD applications
- Automagically generate secrets
- Move Auth0 module under terraform to be able to create new applications, the secrets of which need to be passed to vault
- Add tenantId and subscriptionId as variable to the create new cluster script
- Modify script to use root fitfile module for maintainance, currently duplicates a lot of terraform code, which should be in a single module, only the config should change.
