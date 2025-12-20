---
aliases: []
confidence: 
created: 2025-07-01T05:54:36Z
epistemic: 
id: TFC Service Principle for Azure
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: TFC Service Principle for Azure
type:
uid: 
updated: 
version:
---

## 1. Purpose and Creation

The Service Principal is a non-human identity that Terraform Cloud uses to authenticate with your Azure subscription and perform automated infrastructure deployments. It needs to be created in your Azure tenant before the Terraform deployment can begin.

The general steps for its creation involve:

- Navigating to Microsoft Entra ID (formerly Azure Active Directory) within the Azure tenant.
- Going to "App registrations" and selecting "Add".
- Naming the Service Principal, typically something descriptive like "FITFILE Terraform Cloud Provisioner".
- Registering the application.
- Creating a new client secret for it, usually with a recommended default lifetime (e.g., 6 months).

## 2. Required Credentials for Terraform Cloud

After creation, specific credentials from the Service Principal are needed to configure the Terraform Cloud workspace. These are known as Azure Resource Manager (ARM) keys and must be set as environment variables within the Terraform Cloud workspace:

- `ARM_CLIENT_ID`: This is the Application (client) ID of the enterprise application/Service Principal. This is the *only* ARM key that should not be marked as sensitive in Terraform Cloud, allowing its value to be visible.
- `ARM_ACCESS_KEY`: This is the Secret_id of the client secret you created for the Service Principal in the Azure tenant. This variable must be marked as sensitive.
- `ARM_CLIENT_SECRET`: This is the actual Value of the client secret you created in the Azure tenant. This variable must also be marked as sensitive.

These keys enable Terraform to authenticate successfully with Azure using the Service Principal's identity.

## 3. Required Azure Role Assignments

For the Service Principal to have the necessary permissions to create and manage Azure resources, it must be assigned specific roles within the Azure Subscription. The assignment process involves navigating to the subscription's "Access control" (IAM) section and adding new role assignments:

- `Contributor` Role: The Service Principal requires `Contributor` access to the Subscription. This role grants broad permissions to create, manage, and delete resources within the subscription, which is essential for Terraform's provisioning tasks.
- `User Access Administrator` Role: An additional role assignment of `User Access Administrator` is required for the Service Principal on the subscription. This is a critical permission that allows the Service Principal to:
- Assign specific roles to identities, which is necessary for the AKS cluster identity to function correctly.
- Specifically, a condition should be configured under this role to constrain it to the `Network Contributor` role. This allows the Service Principal (and by extension, the AKS cluster identity it configures) to manage network resources as needed.

Without these precise role assignments, Terraform deployments can fail due to insufficient permissions, as evidenced by errors such as `InvalidAuthenticationTokenTenant` or `SubscriptionNotEnabledEncryptionAtHost`.

## Summary of Service Principal Requirements

- Created as an App Registration in Microsoft Entra ID.
- Credentials (`ARM_CLIENT_ID`, `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET`) configured as sensitive environment variables in Terraform Cloud (except for `ARM_CLIENT_ID`).
- Assigned `Contributor` role on the target Azure Subscription.
- Assigned `User Access Administrator` role on the target Azure Subscription, with a condition that specifically allows it to assign the `Network Contributor` role for the AKS cluster's identity.

In our previous discussion, we covered the basic requirements for the Service Principal, including the need for `Contributor` and `User Access Administrator` roles. Now, let's dive deeper into how we can refine these permissions to adhere more strictly to the principle of least privilege, leveraging the detailed information in the `azure-aks.pdf` document.

### Understanding the Service Principal's Role

The Service Principal is an application identity used by Terraform Cloud to authenticate with your Azure subscription. It acts as a non-human user, allowing Terraform to programmatically create and manage Azure resources.

For Terraform Cloud to use this Service Principal, it requires specific credentials to be configured as sensitive environment variables within the workspace:

- `ARM_CLIENT_ID`: The Application (client) ID of the Service Principal. This is the only one that doesn't need to be marked as sensitive.
- `ARM_ACCESS_KEY`: The Secret_id of the client secret. This must be sensitive.
- `ARM_CLIENT_SECRET`: The Value of the client secret. This must also be sensitive.

### Refining Permissions for Least Privilege

The goal of least privilege is to grant only the permissions absolutely necessary to perform a given task, and no more. For a Terraform Cloud Service Principal deploying AKS, this involves distinguishing between permissions needed to create and operate the cluster and permissions required by the AKS cluster's own managed identity to interact with other Azure services.

#### 1. Permissions for the Terraform Cloud Service Principal (The Identity *Creating* and *Operating* the Cluster)

Initially, the "FITFILE Azure Deployment - Customer Checklist" recommends assigning the `Contributor` role to the Service Principal. While `Contributor` grants broad permissions to manage all resources, which simplifies initial setup, it's not aligned with least privilege.

The `azure-aks.pdf` provides a more granular list of permissions needed by "the identity creating and operating the cluster". To achieve least privilege, instead of a blanket `Contributor` role, you should consider creating a custom Azure role definition that includes only these specific actions.

Here's a breakdown of the *more refined* permissions for the Terraform Cloud Service Principal:

- Compute-Related Permissions: These are essential for managing virtual machines (VMs), disks, and related components that make up the AKS nodes:
  - `Microsoft.Compute/diskEncryptionSets/read`: To read disk encryption set IDs.
  - `Microsoft.Compute/proximityPlacementGroups/write`: For updating proximity placement groups.
  - `Microsoft.Compute/disks/`: For configuring Azure Disks.
  - `Microsoft.Compute/virtualMachines/`: For managing virtual machines. This likely includes `Microsoft.Compute/virtualMachines/extensions/` and `Microsoft.Compute/virtualMachines/powerOff/action`.
  - `Microsoft.Compute/locations/vmSizes/read`: To find information about virtual machine sizes for volume limits.
  - `Microsoft.Compute/locations/operations/read`: To find information about virtual machine operations.
- Network-Related Permissions: Necessary for configuring virtual networks, load balancers, and network interfaces:
  - `Microsoft.Network/virtualNetworks/joinLoadBalancer/action`: Required to configure IP-based Load Balancer Backend Pools.
  - `Microsoft.Network/networkInterfaces/`: For managing network interfaces.
  - `Microsoft.Network/virtualNetworks/` and `Microsoft.Network/virtualNetworks/subnets/`: For managing virtual networks and subnets. More specifically, if using a custom VNet, you'd need `Microsoft.Network/virtualNetworks/subnets/read` and `Microsoft.Network/virtualNetworks/subnets/join/action`.
- Managed Identity Permissions: Crucial for enabling the AKS cluster to use its own managed identity for Azure resource access (recommended over Service Principals for AKS cluster identity):
  - `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action`: This is needed by the identity creating the cluster to assign user-assigned managed identities to resources (like the AKS nodes).
- AKS Cluster Management Permissions:
  - `Microsoft.ContainerService/managedClusters/`: This is a broad permission for creating users and operating the AKS cluster itself. While still broad, it's specific to the AKS resource type.
- Resource Management Permissions: For managing resource groups and subscriptions:
  - `Microsoft.Resources/subscriptions/providers/read`: To read providers.
  - `Microsoft.Resources/subscriptions/resourcegroups/`: For managing resource groups.
- Monitoring-Related Permissions: For configuring Log Analytics workspaces and Container Insights:
  - `Microsoft.OperationalInsights/workspaces/sharedkeys/read`.
  - `Microsoft.OperationalInsights/workspaces/read`.
  - `Microsoft.OperationsManagement/solutions/write`.
  - `Microsoft.OperationsManagement/solutions/read`: Required to create and update Log Analytics workspaces and Azure monitoring for containers.
- Role Assignment Permissions (for assigning roles to the AKS Cluster Identity):
  - `User Access Administrator` role with a specific condition: The "FITFILE Azure Deployment - Customer Checklist" explicitly states that "Another role assignment needs to be added to allow the service principal to assign a specific role for the aks cluster identity". This role is `User Access Administrator` on the subscription, with a condition to constrain it to the `Network Contributor` role. This is critical because the AKS cluster's managed identity requires `Network Contributor` access on the virtual network and API server subnet for its operations, especially in AKS Automatic with custom VNets. The Service Principal needs permission to *assign* this role.

#### 2. Permissions for the AKS Cluster's Own Managed Identity

Once the AKS cluster is deployed by your Service Principal, the cluster itself will use a managed identity to interact with other Azure services. This is distinct from the Service Principal that deployed it, and managed identities are the recommended approach for the cluster's runtime operations due to automatic credential management.

The `azure-aks.pdf` details the permissions needed by the "AKS cluster identity":

- `Microsoft.ContainerService/managedClusters/`: General operations related to the managed cluster.
- `Microsoft.Network/loadBalancers/`: For configuring the load balancer for Kubernetes services.
- `Microsoft.Compute/disks/`: For configuring Azure Disks.
- `Microsoft.Storage/storageAccounts/`: For configuring storage accounts for AzureFile or AzureDisk.
- `Microsoft.Network/routeTables/`: For configuring route tables and routes for nodes.
- `Microsoft.Compute/virtualMachines/read` and `Microsoft.Compute/virtualMachines/write`: For finding information about VMs and attaching Azure Disks.
- `Microsoft.Compute/virtualMachineScaleSets/`: For managing VM scale sets, including adding/deleting VMs and associating with load balancers.
- `Microsoft.Network/networkInterfaces/read`: To search internal IPs and load balancer backend address pools.
- `Microsoft.Compute/snapshots/`: For configuring snapshots for AzureDisk.

Additionally, specifically for AKS Automatic clusters with custom virtual networks, the cluster identity requires the `Network Contributor` built-in role assignment on the API server subnet and the virtual network to support Node Auto Provisioning.

### Summary of Least Privilege for the Terraform Cloud Service Principal

To truly maintain least privilege for your Terraform Cloud Service Principal, you should:

1. Create a Custom Role for Terraform Cloud Service Principal: Instead of the broad `Contributor` role, define a custom Azure role that includes *only* the specific `Microsoft.Compute`, `Microsoft.Network`, `Microsoft.Resources`, `Microsoft.ManagedIdentity`, `Microsoft.ContainerService`, `Microsoft.OperationalInsights`, and `Microsoft.OperationsManagement` permissions listed above for "Identity creating and operating the cluster".
2. Assign `User Access Administrator` with Condition: Assign the `User Access Administrator` role to the Service Principal, but ensure it's conditioned to only allow assignment of the `Network Contributor` role (or other specific roles) to the AKS cluster's managed identity on relevant resources. This precise control minimizes the Service Principal's ability to arbitrarily grant permissions across your subscription.

By doing this, you ensure that the Terraform Cloud Service Principal has only the necessary permissions to provision and configure the AKS cluster and its dependencies, without having overly broad access to other resources or the ability to grant arbitrary roles.
