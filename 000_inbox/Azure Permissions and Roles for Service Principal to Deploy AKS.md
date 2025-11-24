---
aliases: []
confidence:
created: 2025-11-24T11:22:05Z
epistemic:
last_reviewed:
modified: 2025-11-24T11:31:46Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: Azure Permissions and Roles for Service Principal to Deploy AKS
type:
uid:
updated:
---

## Azure Permissions and Roles for Service Principal to Deploy AKS

Microsoft recommends using [Managed Identities over Service Principals for AKS clusters](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity). Service principals are in maintenance mode. Consider using managed identities for new deployments for improved security and ease of use.  

### 1. Overview

A service principal is an identity created within Microsoft Entra ID (formerly Azure Active Directory) that is used by applications, services, and automation tools to access Azure resources programmatically[1]. When deploying Azure Kubernetes Service (AKS), a service principal is required for the AKS control plane to dynamically create and manage other Azure resources on your behalf.

These resources include:

- Virtual Machines and Virtual Machine Scale Sets
- Load Balancers and Public IP Addresses
- Virtual Networks, Subnets, and Network Interfaces
- Managed Disks
- Access to Azure Container Registry (ACR)

The service principal acts as the identity for the AKS cluster's operational backend, enabling it to provision and manage the underlying infrastructure. While Microsoft now strongly advocates for the use of managed identities—which are created and managed by Azure and eliminate the need for credential management—service principals are still supported in AKS and remain a common choice in existing deployments or specific automation scenarios[1].

### 2. Required Azure Roles

For a service principal to successfully deploy and operate an AKS cluster, it must be assigned specific Azure RBAC roles. The minimum set of built-in roles required is as follows:

- **Contributor**: This role is the foundational requirement. It grants broad permissions to create, read, update, and delete (CRUD) most Azure resources.
    - **Minimum Scope**: Resource group level where the AKS cluster will be deployed.
    - **Required For**: Creating the AKS cluster resource itself, managed disks, virtual machine scale sets for agent nodes, load balancers, and other core infrastructure[2].
- **Network Contributor**: This role is required *only* if your AKS cluster uses a pre-existing virtual network (VNet) or subnet that resides in a different resource group than the AKS cluster.
    - **Scope**: The resource group containing the custom virtual network resources.
    - **Required For**: Allowing the AKS control plane to manage networking components like joining VMs to subnets, managing public IPs, and configuring network security groups when using advanced networking configurations[1].
- **AcrPull** (Azure Container Registry Pull): This role is required if your AKS workloads will deploy container images from a private Azure Container Registry (ACR).
    - **Scope**: The resource group or, preferably, the specific ACR resource.
    - **Required For**: Granting the service principal the necessary permissions to authenticate with and pull container images from ACR[1][3].
- **Managed Identity Operator**: This role is required if your AKS cluster will use Azure AD pod-managed identities (where individual pods are assigned managed identities for Azure access).
    - **Scope**: Resource group or subscription level.
    - **Required For**: Allowing the AKS control plane to assign managed identities to pods running within the cluster[3].

### 3. Specific Permissions

Beyond the assignment of entire roles, understanding the granular permissions is crucial for troubleshooting and security auditing. The required actions are derived from the roles listed above and AKS operational needs[2].

#### Resource Group Permissions

The **Contributor** role provides a wide array of permissions. Key actions the AKS control plane needs on the cluster's resource group include:

- `Microsoft.ContainerService/managedClusters/*` - Full control over AKS cluster lifecycle.
- `Microsoft.Compute/disks/*` - Create and manage managed disks for persistent volumes.
- `Microsoft.Compute/virtualMachineScaleSets/*` - Create and manage VM scale sets for the node pool.
- `Microsoft.Network/loadBalancers/*` - Provision and configure load balancers for services.
- `Microsoft.Network/publicIPAddresses/*` - Allocate public IP addresses.
- `Microsoft.Network/virtualNetworks/subnets/join/action` - Allow VMs in the scale set to be attached to a subnet.
- `Microsoft.OperationalInsights/workspaces/*` and `Microsoft.OperationsManagement/solutions/*` - Enable Azure Monitor for containers.
- `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action` - Assign managed identities to the AKS cluster's identity profile.

#### Virtual Network and Subnet Permissions

If the VNet is in a different resource group, the **Network Contributor** role grants these specific actions on that resource group:

- `Microsoft.Network/virtualNetworks/read` - Verify the existence and configuration of the target VNet.
- `Microsoft.Network/virtualNetworks/subnets/read` - Validate the configuration of the specified subnet.
- `Microsoft.Network/virtualNetworks/subnets/join/action` - Essential permission for the AKS cluster to place its node network interfaces into the custom subnet.
- `Microsoft.Network/routeTables/read` and `Microsoft.Network/routeTables/routes/write` - Manage routing for the cluster nodes.
- `Microsoft.Network/networkSecurityGroups/read` and `Microsoft.Network/networkSecurityGroups/write` - Allow the creation of security rules for the load balancer.

#### Azure Container Registry Permissions

For ACR access, the **AcrPull** role grants these specific actions on the ACR resource:

- `Microsoft.ContainerRegistry/registries/pull/action` - Authenticate to the registry and download (pull) container images.

#### Managed Identity Permissions

The **Managed Identity Operator** role grants these actions, which are necessary for pod identity scenarios:

- `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action` - Assign an existing user-assigned managed identity to a resource (in this case, a pod).
- `Microsoft.ManagedIdentity/userAssignedIdentities/read` - Retrieve the configuration of a managed identity.

### 4. Step-by-Step Assignment Instructions

This section provides clear instructions for assigning the necessary roles using the Azure Portal, Azure CLI, and PowerShell.

#### Azure Portal

1. Navigate to the **Resource Group** where your AKS cluster will be created.
2. Click on **Access control (IAM)**.
3. Click **Add** > **Add role assignment**.
4. In the **Role** tab, select **Contributor**.
5. Click **Next**.
6. In the **Members** tab, click **Select members**.
7. In the **Select members** pane, search for your service principal by its name or Application (Client) ID.
8. Select the service principal and click **Select**.
9. Click **Review + assign** and verify the details.
10. Click **Assign**.

To assign **Network Contributor** for a custom VNet in another resource group:

1. Navigate to the **Resource Group** containing the custom VNet.
2. Click on **Access control (IAM)**.
3. Click **Add** > **Add role assignment**.
4. Select the **Network Contributor** role.
5. Follow steps 6-10 above to assign the role to your service principal.

To assign **AcrPull** for an ACR:

1. Navigate directly to your **Azure Container Registry** resource.
2. Click on **Access control (IAM)**.
3. Click **Add** > **Add role assignment**.
4. Select the **AcrPull** role.
5. Follow steps 6-10 above to assign the role to your service principal.

#### Azure CLI Commands

{code:azurecli}

## (Optional) Create a New Service Principal for AKS

## This Command Will Output the appId (client ID) and Password (client secret)

az ad sp create-for-rbac --name myAKSServicePrincipal

## Assign the Contributor Role to the Service Principal at the Resource Group Scope

## Replace with the Service Principal's Client ID and with Your Target RG

az role assignment create  
--assignee  
--role "Contributor"  
--resource-group

## Assign the Network Contributor Role for Custom VNET Scenarios

## Replace and with Your Values

az role assignment create  
--assignee  
--role "Network Contributor"  
--scope "/subscriptions//resourceGroups/"

## Assign the AcrPull Role to Grant Image Pull Permissions

## Replace and with Your ACR's Details

az role assignment create  
--assignee  
--role "AcrPull"  
--scope "/subscriptions//resourceGroups//providers/Microsoft.ContainerRegistry/registries/"  
{code}

### PowerShell Commands

{code:powershell}

## (Optional) Create a New Service Principal

$sp = New-AzADServicePrincipal -DisplayName "myAKSServicePrincipal"  
Write-Output "Application ID: $($sp.ApplicationId)"

## The Password is a SecureString. If You Need the Plain Text (for e.g., CLI login), Convert it

## $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($sp.Secret)

## $plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

## Write-Output "Password: $plainPassword"

## Assign the Contributor Role at the Resource Group Level

New-AzRoleAssignment -ApplicationId $sp.ApplicationId `-ResourceGroupName "<resource-group-name>"`  
-RoleDefinitionName "Contributor"

## Assign the Network Contributor Role

New-AzRoleAssignment -ApplicationId $sp.ApplicationId `-Scope "/subscriptions/<subscription-id>/resourceGroups/<vnet-resource-group>"`  
-RoleDefinitionName "Network Contributor"

## Assign the AcrPull Role for Container Registry Access

New-AzRoleAssignment -ApplicationId $sp.ApplicationId `-Scope "/subscriptions/<subscription-id>/resourceGroups/<acr-resource-group>/providers/Microsoft.ContainerRegistry/registries/<acr-name>"`  
-RoleDefinitionName "AcrPull"  
{code}

### 5. Best Practices

{info:title=Principle of Least Privilege}  
Always grant the minimum permissions required for functionality. Avoid assigning broad, powerful roles like **Owner** to service principals. The security impact of a compromised credential with excessive permissions can be severe.  
{info}

- **Scope Limitations**
    - **Resource Group Scope**: Assign the **Contributor** role at the *resource group level*, never at the subscription level if possible. This limits the potential blast radius if the service principal is compromised[2].
    - **Fine-Grained ACR Access**: Scope **AcrPull** to the *specific ACR resource*, rather than the entire resource group or subscription.
    - **Network Group Isolation**: Limit the **Network Contributor** role to only the resource group that contains the custom VNet and related networking resources.
- **Service Principal Credential Management**
    - **Expiration Policies**: Set credential expiration. By default, service principal credentials are valid for one year and should be rotated[4].
    - **Use Certificates**: Prefer certificates over client secrets. Certificates are more secure and can have longer lifespans with non-repudiation.
    - **Secure Storage**: *Never* store service principal secrets in code or unsecured files. Use [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/) to store and manage client secrets or certificate keys.
    - **Regular Rotation**: Establish a process for regularly rotating credentials (e.g., every 90 days).
    - **Propagate Timing**: Remember that role assignments can take up to 60 minutes to propagate across Azure's infrastructure[1].
- **Migration to Managed Identities**
    - For all new AKS deployments, use managed identities. A system-assigned managed identity is created by default in new AKS clusters and is simpler and more secure[3].
    - Consider upgrading existing clusters to use managed identities to eliminate the need to manage service principal credentials altogether[1].
- **Auditing and Monitoring**
    - Enable **Azure Monitor for AKS** and **Azure Activity Logs** to audit all role assignments and operations performed by the service principal[2].
    - Set up **Azure Monitor Alerts** for unusual activities, such as failed authorization attempts or unexpected resource creation.

### 6. Troubleshooting

{warning:title=Common Permission-Related Errors}  
Always check the **Azure Activity Logs** and **AKS deployment logs** for specific, detailed error messages. Permission issues are a leading cause of deployment failure.  
{warning}

- **"Authorization failed" or "The client does not have authorization"**
    - **Solution**: This is the most common error. Verify that the **Contributor** role is assigned to the correct service principal and that the assignment is scoped to the resource group where the AKS cluster is being created. Be patient, as role assignments can take up to 60 minutes to take full effect across Azure's control plane[1].
- **"Failed to create network interface" or "Cannot join subnet"**
    - **Solution**: This error occurs when using a custom VNet in a separate resource group without proper permissions. Assign the **Network Contributor** role to the service principal for the resource group containing the VNet. Ensure the `Microsoft.Network/virtualNetworks/subnets/join/action` permission is granted[1].
- **"Cannot pull image from container registry"**
    - **Solution**: The service principal lacks pull access to the ACR. Assign the built-in **AcrPull** role on the service principal for the specific ACR resource. Double-check the scope in the role assignment[1].
- **Service principal credentials have expired**
    - **Symptom**: Errors during cluster creation or deployment indicating invalid credentials.
    - **Solution**: Check the credential expiration with the command:  
        `{code:azurecli}az ad app credential list --id <appId> --query "[].endDateTime" --output tsv{code}`  
        If expired, reset the credentials:  
        `{code:azurecli}az ad sp credential reset --name <appId>{code}`  
        Or, if using a client secret, create a new one via the Azure Portal. The default validity period is one year[4].
- **Role assignments are not taking effect**
    - **Solution**: Wait at least 60 minutes for propagation. Verify that the correct service principal **Application ID (appId)** was used in the role assignment, not the Object ID. Ensure there are no typos in the resource IDs and scopes[1].
- **"Operation failed with status: 'Bad Request' - The credentials in ServicePrincipalProfile were invalid"**
    - **Solution**: This often stems from Azure CLI caching old or incorrect credentials. Try clearing the Azure CLI cache or use `az login` with the service principal's client ID and secret again. Check if the service principal has been accidentally deleted or disabled in Microsoft Entra ID. Verify the service principal object exists with `az ad sp list --display-name <service-principal-name>`.

References:  
[1]: [https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal)  
[2]: [https://learn.microsoft.com/en-us/azure/aks/concepts-identity](https://learn.microsoft.com/en-us/azure/aks/concepts-identity)  
[3]: [https://learn.microsoft.com/en-us/azure/aks/use-managed-identity](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity)  
[4]: [https://learn.microsoft.com/en-us/azure/aks/update-credentials](https://learn.microsoft.com/en-us/azure/aks/update-credentials)  
[5]: [https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal)  
[6]: [https://learn.microsoft.com/en-us/answers/questions/2337883/aks-rbac-roles-clarification](https://learn.microsoft.com/en-us/answers/questions/2337883/aks-rbac-roles-clarification)  
[7]: [https://stackoverflow.com/questions/58245176/what-roles-does-a-serviceprincipal-need-to-create-aks-from-az-cli](https://stackoverflow.com/questions/58245176/what-roles-does-a-serviceprincipal-need-to-create-aks-from-az-cli)  
[8]: [https://florinloghiade.ro/aks-authorization-models-2/](https://florinloghiade.ro/aks-authorization-models-2/)  
[9]: [https://learn.microsoft.com/en-us/azure/aks/aks-desktop-permissions](https://learn.microsoft.com/en-us/azure/aks/aks-desktop-permissions)  
[10]: [https://docs.azure.cn/en-us/aks/use-managed-identity](https://docs.azure.cn/en-us/aks/use-managed-identity)  
[11]: [https://trendmicro.com/cloudoneconformity/knowledge-base/azure/AKS/enable-azure-rbac.html](https://trendmicro.com/cloudoneconformity/knowledge-base/azure/AKS/enable-azure-rbac.html)

Here is a comprehensive Confluence wiki page draft documenting **Azure permissions and roles required for a service principal to deploy Azure Kubernetes Service (AKS)**. This conforms to your structure, technical audience, and uses Confluence wiki markup.

---

h1. Azure AKS Deployment: Service Principal Roles & Permissions

---

h2. Overview

A *service principal* is an identity created for use with applications, services, and automation tools to access Azure resources securely. For AKS deployments, a service principal allows your infrastructure automation (IaC tools, CI/CD pipelines) to interact with Azure on behalf of users with defined permissions—critical for least-privilege cluster and network resource provisioning.

*Why specific permissions?*

- Service principals help automate AKS cluster creation and management.
- Precise roles/permissions are required to securely provision resources (e.g., VNets, containers, disks) and avoid broad access.

---

h2. Required Azure Roles

Below are the key Azure built-in roles necessary for AKS deployments via a service principal:

- *Contributor*: Full management access to all resources (except role assignment). Often scoped to a resource group.
- *Network Contributor*: Required if deploying AKS into custom VNets/subnets.
- *Azure Kubernetes Service Cluster User Role*: Enables interaction with AKS cluster resources.
- *AcrPull*/*AcrPush*: Required for Azure Container Registry access (if AKS pulls images from ACR).
- *Virtual Machine Contributor*: Needed if your cluster interacts with compute resources/disks directly.
- *Custom role(s)*: When least-privilege is desired, define custom roles limited to required resource actions.

Panel(title=Info)  
For security, never grant *Owner* role unless strictly necessary.  
EndPanel

---

h2. Specific Permissions

h3. Resource Group

- Read, create, delete, and modify AKS cluster and associated resources.
- Assign RBAC roles at resource group level for isolation.

h3. Virtual Network & Subnet

- *Network Contributor* on target subnet(s): Manages network interfaces, public IPs, routing, and security rules.
- For advanced setups, granular custom roles: e.g., only creation/attachment of NICs.

h3. Azure Container Registry (ACR)

- *AcrPull*: Pull container images.
- *AcrPush*: (if build agent needs to push images).

h3. Managed Identity (Alternatives)

- For workload identity integrations, assign *Managed Identity Operator* or define custom scopes.

Panel(title=Info)  
*Assign permissions at the narrowest required scope:* ideally at resource group or resource level, not at subscription.  
EndPanel

---

h2. Step-by-Step Assignment Instructions

h3. Using Azure Portal

## Go to *Azure Active Directory* > *App registrations* > Your Service Principal

## Assign Built-in Roles

text

`- Navigate to the target resource (resource group, VNet, ACR). - Go to *Access Control (IAM)* > *Add role assignment*. - Select the appropriate role (Contributor, Network Contributor, AcrPull). - Select your service principal as the assignee.`

Panel(title=Info)  
Changes may take up to 60 minutes to propagate.  
EndPanel

h3. Using Azure CLI

bash

`# Assign Contributor to resource group az role assignment create \   --assignee <appId> \  --role "Contributor" \  --scope /subscriptions/<subId>/resourceGroups/<rgName> # Assign Network Contributor to VNet subnet az role assignment create \   --assignee <appId> \  --role "Network Contributor" \  --scope /subscriptions/<subId>/resourceGroups/<rgName>/providers/Microsoft.Network/virtualNetworks/<vnetName>/subnets/<subnetName> # Assign AcrPull for ACR access az role assignment create \   --assignee <appId> \  --role "AcrPull" \  --scope /subscriptions/<subId>/resourceGroups/<rgName>/providers/Microsoft.ContainerRegistry/registries/<acrName>`

h3. Using PowerShell (optional)

powershell

``# Assign Contributor to resource group New-AzRoleAssignment -ApplicationId <appId> `   -RoleDefinitionName "Contributor" `  -Scope "/subscriptions/<subId>/resourceGroups/<rgName>"``

---

h2. Best Practices

- *Principle of Least Privilege*: Assign only the permissions necessary for AKS deployment and operation.
- *Scope limitations*: Prefer resource-group scope over subscription-wide roles.
- *Credential management*: Store service principal secrets in secure stores (Azure Key Vault).
- *Regular rotation*: Rotate secrets annually or sooner; monitor for expiration.
- *Audit & Logging*: Enable logging of service principal usage for traceability.

Panel(title=Warning)  
Do NOT use *Owner* role except for break-glass scenarios.  
EndPanel

---

h2. Troubleshooting

|Error|Likely Cause|Solution|
|---|---|---|
|"Bad Request: Invalid ServicePrincipalProfile credentials"|Expired or incorrect SPN secret|Use `az ad app credential list` to check expiry; rotate secrets or re-create SPN.|
|"AuthorizationFailed: does not have authorization to perform action ..."|Missing resource-specific role|Verify correct role assigned and at the correct scope (e.g., resource group, subnet).|
|Network provisioning errors|Missing Network Contributor role or wrong scope|Assign *Network Contributor* on relevant VNet/subnet resource.|
|Unable to pull images from ACR|SPN lacks AcrPull role on ACR|Assign *AcrPull* role to SPN for correct registry.|

Panel(title=Info)  
Always verify propagation and check Azure Activity Logs for permission errors.  
EndPanel

---

h2. References

- [Official: Use a service principal with AKS](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal)
- [Built-in Azure RBAC roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
- [AKS Best Practice Checks](https://kubebuddy.kubedeck.io/usage/aks-best-practice-checks/)

---

*This page is intended for DevOps engineers and Azure cloud administrators. For questions or updates, please contact the platform team or file a Confluence comment/request.*

---

Let me know if you want edits for custom role JSON examples, or want sections broken into child pages for easier knowledge base integration.

1. [https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal)
2. [https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal)
3. [https://confluence.atlassian.com/spaces/ENTERPRISE/pages/969535580/Running+Confluence+on+an+Azure+cluster](https://confluence.atlassian.com/spaces/ENTERPRISE/pages/969535580/Running+Confluence+on+an+Azure+cluster)
4. [https://stackoverflow.com/questions/58245176/what-roles-does-a-serviceprincipal-need-to-create-aks-from-az-cli](https://stackoverflow.com/questions/58245176/what-roles-does-a-serviceprincipal-need-to-create-aks-from-az-cli)
5. [https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-application](https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-application)
6. [https://triotechsystems.com/azure-devops-how-to-create-service-principal-for-acr-and-aks/](https://triotechsystems.com/azure-devops-how-to-create-service-principal-for-acr-and-aks/)
7. [https://stackoverflow.com/questions/75463812/creating-an-aks-cluster-with-kubernetes-rbac-and-ad-integration-using-a-service](https://stackoverflow.com/questions/75463812/creating-an-aks-cluster-with-kubernetes-rbac-and-ad-integration-using-a-service)
8. [https://learn.microsoft.com/en-us/answers/questions/5516237/aks-automatic-error-when-using-service-principal](https://learn.microsoft.com/en-us/answers/questions/5516237/aks-automatic-error-when-using-service-principal)
9. [https://www.jamessturtevant.com/posts/Deploying-AKS-with-least-privileged-service-principal/](https://www.jamessturtevant.com/posts/Deploying-AKS-with-least-privileged-service-principal/)
10. [https://learn.microsoft.com/en-us/azure/aks/](https://learn.microsoft.com/en-us/azure/aks/)
11. [https://learn.microsoft.com/en-us/azure/aks/concepts-identity](https://learn.microsoft.com/en-us/azure/aks/concepts-identity)
12. [https://learn.microsoft.com/en-us/azure/aks/manage-azure-rbac](https://learn.microsoft.com/en-us/azure/aks/manage-azure-rbac)
13. [https://www.007ffflearning.com/post/renewing-expired-aks-service-principal/](https://www.007ffflearning.com/post/renewing-expired-aks-service-principal/)
14. [https://intercept.cloud/en-gb/blogs/aks-security](https://intercept.cloud/en-gb/blogs/aks-security)
15. [https://community.atlassian.com/forums/Jira-questions/Azure-DevOps-for-Jira-using-a-service-principal/qaq-p/3093815](https://community.atlassian.com/forums/Jira-questions/Azure-DevOps-for-Jira-using-a-service-principal/qaq-p/3093815)
16. [https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
17. [https://docs.cambridgesemantics.com/anzo/v5.4/userdoc/aks-iam.htm](https://docs.cambridgesemantics.com/anzo/v5.4/userdoc/aks-iam.htm)
18. [https://github.com/hashicorp/terraform-provider-kubernetes/issues/1964](https://github.com/hashicorp/terraform-provider-kubernetes/issues/1964)
19. [https://kubebuddy.kubedeck.io/usage/aks-best-practice-checks/](https://kubebuddy.kubedeck.io/usage/aks-best-practice-checks/)
20. [https://www.youtube.com/watch?v=_JPZbNplWvc](https://www.youtube.com/watch?v=_JPZbNplWvc)

## Research Report on Permissions for Azure Kubernetes Service (AKS) Private Cluster Deployment

**DATE:** 2025-11-24

### 1. Overview: Service Principal Fundamentals and Permission Requirements for Private AKS

The deployment and management of Azure Kubernetes Service (AKS), particularly in a private configuration, relies on a sophisticated identity and access management framework. At the core of this framework are Azure service principals and managed identities, which act as the security context through which the AKS cluster interacts with other Azure resources. A service principal is an identity created for use with applications, hosted services, and automated tools to access Azure resources. It is the security identity of an application, defining what the application can and cannot do within a Microsoft Entra tenant. While service principals have historically been the standard, Azure now strongly recommends the use of **managed identities** for Azure resources. Managed identities provide Azure services with an automatically managed identity in Microsoft Entra ID, eliminating the need for developers to manage credentials like secrets or certificates.

The necessity for specific, and often extensive, permissions stems from the fundamental architecture of AKS. When an AKS cluster is provisioned, it is not a self-contained entity; it must dynamically create and manage a suite of underlying Azure infrastructure resources on behalf of the user. These resources typically reside in a separate, AKS-managed resource group known as the node resource group and include virtual machine scale sets (VMSS) for nodes, virtual networks (VNets), network interfaces (NICs), load balancers, public IP addresses, and managed disks for persistent storage. The identity assigned to the AKS cluster—whether a service principal or a managed identity—must be granted sufficient permissions to perform these lifecycle operations within the user's subscription.

For a **private AKS cluster**, the permission requirements become even more stringent and complex. In a private cluster, the Kubernetes API server, which serves as the control plane, is not exposed to the public internet. Instead, it is assigned a private IP address within a virtual network. This design significantly enhances security by ensuring that all network traffic between the cluster's node pools and the API server remains exclusively on the private network. This is typically achieved using Azure Private Link, which projects the API server into a private endpoint within the cluster's VNet, or through the more recent API Server VNet Integration feature, which injects the API server directly into a delegated subnet. This private architecture imposes additional permission requirements related to private networking, such as managing private endpoints, configuring private DNS zones to resolve the API server's private FQDN, and managing specific network security group (NSG) rules to control traffic flow. Without these precise permissions, the cluster nodes would be unable to communicate with the control plane, rendering the cluster non-functional.

### 2. Required Azure Roles

To facilitate the deployment and operation of a private AKS cluster, Azure provides several built-in Role-Based Access Control (RBAC) roles. Assigning these roles to the service principal or managed identity responsible for the cluster ensures it has the necessary authority to manage associated resources. While broad roles can be used, a granular approach is recommended for production environments.

The **Contributor** role is a high-privilege role that grants full access to manage all resources within its scope (such as a subscription or resource group), but it does not allow the assignment of roles to other identities. Assigning the Contributor role to an AKS service principal at the subscription level will certainly provide sufficient permissions for cluster deployment. However, this approach is overly permissive and directly contravenes the principle of least privilege, posing a significant security risk. It is generally discouraged for automated services in production environments.

A more secure and common requirement is the **Network Contributor** role. This role is essential for any AKS deployment that involves custom virtual network configurations, which is standard for private clusters. It grants the assigned identity permissions to manage most networking resources, including virtual networks, subnets, network interfaces, and load balancers. For a private AKS cluster, the cluster's identity must have the Network Contributor role assigned at the scope of the virtual network and its subnets. Specifically, when using the API Server VNet Integration feature, this role is required on both the primary cluster subnet and the dedicated API server subnet to allow the AKS service to inject the necessary components.

The **Private DNS Zone Contributor** role is another critical component for private AKS clusters. When a private cluster is created, AKS can automatically create a private DNS zone to handle the name resolution for the private API server endpoint. If an organization chooses to use a pre-existing or custom private DNS zone (for example, in a hub-and-spoke network topology), the cluster's identity must be granted the Private DNS Zone Contributor role on that specific DNS zone. This permission allows the AKS control plane to create and manage the necessary 'A' records that map the API server's fully qualified domain name (FQDN) to its internal IP address, enabling seamless communication from within the VNet.

In addition to these primary roles, other roles play a part in the broader AKS ecosystem. The **Azure Kubernetes Service Cluster Admin** role is a user-facing role that grants access to the `get-credentials` action with admin privileges, allowing a user to download the admin `kubeconfig` file and gain full administrative access to the Kubernetes API. This role is distinct from the permissions needed by the cluster's service principal to manage Azure infrastructure. Furthermore, Azure provides a set of roles specifically for Kubernetes authorization, such as **Azure Kubernetes Service RBAC Reader**, **Writer**, **Admin**, and **Cluster Admin**, which allow for fine-grained control over actions *within* the Kubernetes cluster via Azure RBAC, once the cluster is deployed.

### 3. Specific Permissions

Beyond the high-level built-in roles, a granular understanding of specific permission actions is crucial for implementing a least-privilege model. These permissions are required by the identity creating the cluster and the cluster's own managed identity to perform their respective functions.

**Resource Group Operations**: The AKS service needs to manage resources within the node resource group. While this is often handled by an internal AKS service identity, the identity deploying the cluster may need permissions to create the resource group itself if it does not already exist.

**Virtual Network and Subnet Management**: This is one of the most critical areas. The identity requires `Microsoft.Network/virtualNetworks/subnets/join/action` permission. This action is fundamental as it allows the virtual machine scale sets (for nodes) and the API server's private endpoint to have their network interfaces joined to the specified subnets. When using the API Server VNet Integration model, the API server subnet must be delegated to the `Microsoft.ContainerService/managedClusters` service, a configuration step that requires appropriate permissions on the VNet.

**Private Endpoint Creation and Management**: The cluster identity needs permissions to manage the private endpoint for the API server and the internal load balancers for Kubernetes services of type `LoadBalancer`. This includes actions like `Microsoft.Network/privateEndpoints/write`, `Microsoft.Network/loadBalancers/write`, `Microsoft.Network/loadBalancers/read`, and `Microsoft.Network/loadBalancers/delete`. If the cluster uses a standard load balancer with outbound rules, permissions such as `Microsoft.Network/publicIPAddresses/join/action` and `Microsoft.Network/publicIPPrefixes/join/action` are also necessary.

**Private DNS Zone Configuration**: To manage DNS records for the private API server, the identity needs permissions within the `Microsoft.Network/privateDnsZones` provider. The `Private DNS Zone Contributor` role encompasses these, but a custom role could be limited to `Microsoft.Network/privateDnsZones/A/write` and `Microsoft.Network/privateDnsZones/A/read` for the specific zone, providing more granular control. The identity also needs to link the private DNS zone to the virtual network, requiring `Microsoft.Network/privateDnsZones/virtualNetworkLinks/write`.

**Azure Container Registry (ACR) Integration**: For a private AKS cluster to pull container images from a private Azure Container Registry, the cluster's managed identity must be granted a role on the ACR instance. The built-in `AcrPull` role is the standard, least-privilege role for this purpose, granting only the permission to pull images from the registry. This integration is typically configured during cluster creation or update using the `--attach-acr` flag in the Azure CLI.

**Managed Identity Permissions**: The AKS cluster's own managed identity requires a specific set of permissions to operate the node resource group. These include, but are not limited to: `Microsoft.Compute/virtualMachineScaleSets/write`, `Microsoft.Compute/virtualMachineScaleSets/delete`, `Microsoft.Compute/virtualMachines/write`, `Microsoft.Network/networkInterfaces/write`, `Microsoft.Compute/disks/write`, and `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action`. These permissions allow the AKS control plane to scale node pools, update nodes, attach disks for persistent volumes, and manage networking for pods and services.

**Private Cluster-Specific Networking Requirements**: A private cluster's security posture depends on correctly configured network security groups (NSGs) and, potentially, an Azure Firewall for egress control. The identity managing the cluster must have permissions to create and modify NSGs (`Microsoft.Network/networkSecurityGroups/write`). Furthermore, specific traffic flows must be permitted. Communication between the API server subnet and the cluster node subnet is required on TCP ports 443 and 4443. If an Azure Firewall is used to lock down outbound traffic, rules must be created to allow essential egress for DNS (UDP 53), NTP for time synchronization (UDP 123), and access to required service tags like `AzureContainerRegistry`, `MicrosoftContainerRegistry`, and `AzureActiveDirectory`.

### 4. Step-by-Step Assignment Instructions

Assigning the necessary roles and permissions can be accomplished through the Azure Portal, Azure CLI, or PowerShell. Using managed identities is the recommended approach to avoid credential management.

#### Azure Portal UI Steps

1.  **Navigate to the Target Resource**: To assign a role, first navigate to the resource where the permission is needed. This could be a subscription, a resource group, a specific virtual network, or a private DNS zone.
2.  **Open Access Control (IAM)**: In the resource's navigation pane, select **Access control (IAM)**.
3.  **Add Role Assignment**: Click the **Add** button and select **Add role assignment**.
4.  **Select a Role**: On the Role tab, search for and select the required built-in role, such as **Network Contributor** or **Private DNS Zone Contributor**.
5.  **Select the Assignee**: Click **Next** to go to the Members tab. Select **Managed identity**. Choose the subscription where the identity resides and then select the specific user-assigned managed identity that will be used by the AKS cluster. If using a service principal, select **User, group, or service principal** and search for it by name.
6.  **Review and Assign**: Click **Review + assign** to complete the role assignment. The permission can take several minutes to propagate. Repeat this process for all required roles at their respective scopes.

#### Azure CLI Commands with Examples

The Azure CLI provides an efficient, scriptable method for managing role assignments.

1.  **Create a User-Assigned Managed Identity (if one doesn't exist):**

    ```bash
    # Define variables
    RESOURCE_GROUP="myResourceGroup"
    IDENTITY_NAME="myAksIdentity"

    # Create the identity
    az identity create --resource-group $RESOURCE_GROUP --name $IDENTITY_NAME
    ```

2.  **Assign Roles to the Managed Identity**: You will need the resource ID of the identity and the scope of the assignment.

    ```bash
    # Get the identity's principal ID and resource ID
    IDENTITY_PRINCIPAL_ID=$(az identity show --resource-group $RESOURCE_GROUP --name $IDENTITY_NAME --query "principalId" -o tsv)
    VNET_SCOPE=$(az network vnet show --resource-group $RESOURCE_GROUP --name myVnet --query "id" -o tsv)
    DNS_ZONE_SCOPE=$(az network private-dns zone show --resource-group $RESOURCE_GROUP --name "privatelink.eastus.azmk8s.io" --query "id" -o tsv)

    # Assign Network Contributor role to the VNet
    az role assignment create \
        --assignee-object-id $IDENTITY_PRINCIPAL_ID \
        --assignee-principal-type "ServicePrincipal" \
        --role "Network Contributor" \
        --scope $VNET_SCOPE

    # Assign Private DNS Zone Contributor role to the DNS zone
    az role assignment create \
        --assignee-object-id $IDENTITY_PRINCIPAL_ID \
        --assignee-principal-type "ServicePrincipal" \
        --role "Private DNS Zone Contributor" \
        --scope $DNS_ZONE_SCOPE
    ```

#### PowerShell Commands with Examples

PowerShell offers another powerful scripting interface for Azure management.

1.  **Create a User-Assigned Managed Identity:**

    ```powershell
    # Define variables
    $resourceGroupName = "myResourceGroup"
    $identityName = "myAksIdentity"

    # Create the identity
    $identity = New-AzUserAssignedIdentity -ResourceGroupName $resourceGroupName -Name $identityName
    ```

2.  **Assign Roles to the Managed Identity**:

    ```powershell
    # Get the scopes for the VNet and DNS Zone
    $vnetScope = (Get-AzVirtualNetwork -ResourceGroupName $resourceGroupName -Name "myVnet").Id
    $dnsZoneScope = (Get-AzPrivateDnsZone -ResourceGroupName $resourceGroupName -Name "privatelink.eastus.azmk8s.io").Id

    # Assign Network Contributor role
    New-AzRoleAssignment -ObjectId $identity.PrincipalId -RoleDefinitionName "Network Contributor" -Scope $vnetScope

    # Assign Private DNS Zone Contributor role
    New-AzRoleAssignment -ObjectId $identity.PrincipalId -RoleDefinitionName "Private DNS Zone Contributor" -Scope $dnsZoneScope
    ```

### 5. Best Practices

Adhering to security best practices is paramount when configuring permissions for a private AKS cluster to minimize the attack surface and prevent unauthorized access.

**Principle of Least Privilege**: This is the most important security principle. Always grant only the minimum permissions required for a service to perform its function. Avoid using broad roles like `Owner` or `Contributor` at a subscription scope for automated services like AKS. If the built-in roles are too permissive for your organization's security policies, create custom Azure roles that contain only the specific actions needed. For example, a custom role could be created that only allows the management of 'A' records within a specific private DNS zone, rather than granting full contributor access.

**Scope Limitations**: Permissions should always be assigned at the most granular scope possible. If an AKS cluster's managed identity only needs to manage networking within a single resource group, assign the `Network Contributor` role at that resource group's scope, not at the entire subscription's scope. This containment strategy limits the potential impact of a compromised identity, as its permissions are confined to a smaller set of resources.

**Service Principal Credential Management**: If service principals must be used instead of managed identities, their credentials (client secrets or certificates) must be managed securely. Secrets should be rotated regularly, following a defined schedule. Never hard-code credentials in application code, scripts, or configuration files. Instead, store them securely in Azure Key Vault and have the application or script retrieve them at runtime using a managed identity. This practice centralizes secret management and reduces the risk of accidental exposure.

**Private Cluster Security Considerations**: Beyond IAM, securing a private cluster involves a multi-layered approach. Use Azure Policy to enforce security standards across your AKS clusters, such as requiring private clusters to be enabled or restricting allowed container registries. Implement strict Network Security Group (NSG) rules to control traffic between the API server, node pools, and other network segments. For controlling outbound (egress) traffic from the cluster, use Azure Firewall to create explicit allow-lists for required endpoints, blocking all other outbound connections by default. Finally, enable and regularly review audit logs for both Azure Activity and the Kubernetes API server to monitor for suspicious or unauthorized activities.

### 6. Troubleshooting

Permission-related issues are a common source of failure during the deployment and operation of private AKS clusters. Understanding the typical errors and their solutions is key to effective troubleshooting.

**Error: `AuthorizationFailed`**: This is the most frequent permission error. The detailed error message usually indicates which identity (service principal or managed identity) failed to perform an action on a specific resource. The solution involves carefully reviewing the error to identify the missing permission and the target resource scope. Use the Azure CLI command `az role assignment list --assignee <principal-id> --all` to verify the current roles assigned to the identity. Then, assign the missing role (e.g., `Network Contributor`) at the correct scope (e.g., the virtual network or resource group).

**Error: `InvalidSubnet` or Subnet Delegation Failure**: During deployment, an error indicating an invalid subnet often points to a permission issue. This can occur if the subnet designated for the API server is not correctly delegated to the `Microsoft.ContainerService/managedClusters` service. It can also happen if the cluster's identity lacks the `Microsoft.Network/virtualNetworks/subnets/join/action` permission on the subnet, preventing it from attaching network interfaces. Verify both the subnet delegation and the role assignments for the cluster identity.

**DNS Resolution Failure for Private API Server**: If cluster nodes or external tools within the VNet fail to connect to the API server, the issue is often DNS-related. This manifests as an inability to resolve the private FQDN of the API server. First, ensure the Private DNS Zone is correctly linked to the cluster's virtual network. Second, confirm that the cluster's managed identity has the `Private DNS Zone Contributor` role on the zone, which allows it to create and update the necessary 'A' record. If the IP address of the private endpoint changes, AKS needs this permission to update the DNS record accordingly.

**Error: `Forbidden` from Kubernetes API**: If you can successfully authenticate to the cluster (e.g., via `az aks get-credentials`) but receive `Forbidden` errors when running `kubectl` commands (like `kubectl get pods`), the issue is typically with Kubernetes RBAC, not Azure IAM. This means your Microsoft Entra user or group does not have the appropriate Kubernetes `Role` or `ClusterRole` assigned via a `RoleBinding` or `ClusterRoleBinding`. If using Azure RBAC for Kubernetes, this means your user has not been assigned one of the "Azure Kubernetes Service RBAC" roles (e.g., Reader, Writer, Admin) at the cluster or namespace scope.

## References
1. [Create a private Azure Kubernetes Service (AKS) cluster - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/private-clusters)
2. [Identity concepts in Azure Kubernetes Service (AKS) - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/concepts-identity)
3. [Set up clusters from hosted Kubernetes providers - ranchermanager.docs.rancher.com](https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-clusters-in-rancher-setup/set-up-clusters-from-hosted-kubernetes-providers/aks)
4. [Minimum permission to create AKS cluster - stackoverflow.com](https://stackoverflow.com/questions/77500845/minimum-permission-to-create-aks-cluster)
5. [Private Cluster Nodes - trendmicro.com](https://www.trendmicro.com/cloudoneconformity/knowledge-base/azure/AKS/private-cluster-nodes.html)
6. [Use a service principal with Azure Kubernetes Service (AKS) - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal)
7. [Deploying AKS with least privileged service principal - jamessturtevant.com](https://www.jamessturtevant.com/posts/Deploying-AKS-with-least-privileged-service-principal/)
8. [Azure Kubernetes Services - when it is required to set AKS service principle on - stackoverflow.com](https://stackoverflow.com/questions/65954507/azure-kubernetes-services-when-it-is-required-to-set-aks-service-principle-on)
9. [Create and Update the Service Principal Key for Azure Kubernetes Service (AKS) - opsmx.com](https://www.opsmx.com/blog/create-and-update-the-service-principal-key-for-azure-kubernetes-service-aks/)
10. [How to grant a service principal access to AKS API when RBAC and AAD integration are enabled? - serverfault.com](https://serverfault.com/questions/963481/how-to-grant-a-service-principal-access-to-aks-api-when-rbac-and-aad-integration)
11. [Azure Private AKS with custom DNS - docs.cloudera.com](https://docs.cloudera.com/data-warehouse/cloud/azure-environments/topics/dw-azure-private-aks-custom-dns.html)
12. [Private DNS zone for private AKS cluster with custom vnet - github.com](https://github.com/Azure/AKS/issues/2185)
13. [DNS options for private Azure Kubernetes Service - baeke.info](https://baeke.info/2021/07/01/dns-options-for-private-azure-kubernetes-service/)
14. [Tutorial: Azure Private DNS - github.com](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/azure-private-dns.md)
15. [Create an Azure Kubernetes Service cluster with API Server VNet Integration - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/api-server-vnet-integration)
16. [A complete guide to building a private AKS cluster - github.com](https://github.com/paolosalvatori/private-aks-cluster)
17. [Quickstart: Deploy a private AKS Automatic cluster in a custom virtual network - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/automatic/quick-automatic-private-custom-network)
18. [privateDNS-and-AKS - github.com](https://github.com/gkaleta/privateDNS-and-AKS)
19. [Fully private AKS clusters without any public IPs — finally! - denniszielke.medium.com](https://denniszielke.medium.com/fully-private-aks-clusters-without-any-public-ips-finally-7f5688411184)
20. [Use Azure RBAC for Kubernetes Authorization - learn.microsoft.com](https://learn.microsoft.com/en-us/azure/aks/manage-azure-rbac)
21. [Policy - Azure Kubernetes Service (AKS) clusters should be private - azadvertizer.net](https://www.azadvertizer.net/azpolicyadvertizer/040732e8-d947-40b8-95d6-854c95024bf8.html)
