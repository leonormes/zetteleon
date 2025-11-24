---
aliases: []
confidence: 
created: 2025-11-24T11:22:05Z
epistemic: 
last_reviewed: 
modified: 2025-11-24T11:22:55Z
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
{info}

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
