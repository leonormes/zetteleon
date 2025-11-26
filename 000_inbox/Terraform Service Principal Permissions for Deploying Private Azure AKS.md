---
aliases: []
confidence: 
created: 2025-11-24T13:16:59Z
epistemic: 
last_reviewed: 
modified: 2025-11-24T13:23:33Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Terraform Service Principal Permissions for Deploying Private Azure AKS
type: 
uid: 
updated: 
---

## Required Service Principal Permissions for Private AKS

**Minimum required permissions:**

|Scope|Role/Permission|Reason/Notes|
|---|---|---|
|Resource Group (AKS)|Contributor *or*|Create/Manage cluster and related resources|
||Azure Kubernetes Service Cluster Admin|Narrower, but only for AKS creation itself|
|Subnet (for nodepool)|Network Contributor|Manage subnet if it's not in same RG or scoped differently|
|Private DNS zone|Private DNS Zone Contributor|Needed for custom DNS (e.g. privatelink.*.azmk8s.io)|
|Azure Container Registry (if used)|AcrPull|Pull images from ACR (if enabled)|
|Other resources|Custom permissions|As needed (e.g. managed identity, storage, key vault, etc.)|

**For private AKS, extra focus is needed on the network and DNS permissions:**

- The SP **must** be able to create, link, and update private endpoints and private DNS zone records.
- If using custom DNS: role **Private DNS Zone Contributor** on the DNS zone.[learn.microsoft](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/error-codes/customprivatednszonemissingpermissions-error)​
- If using custom VNET/subnet: role **Network Contributor** on the subnet.[learn.microsoft](https://learn.microsoft.com/en-us/answers/questions/2129362/private-aks-provisioning-this-subnet-does-not-have)​

## Role Assignment Examples (CLI)

```sh
az role assignment create --assignee <appId> --role "Contributor" --scope /subscriptions/<sub>/resourceGroups/<rg>
az role assignment create --assignee <appId> --role "Network Contributor" --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<vnet>/subnets/<subnet>
az role assignment create --assignee <appId> --role "Private DNS Zone Contributor" --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/privateDnsZones/<zone>
```

---

## Key Notes

- **Contributor** at resource group level generally suffices for most deployments.
- For more restrictive setups, combine role assignments as above and add more roles for storage, Key Vault, etc. as needed.
- Managed identities are recommended for new clusters, but SPs are still valid.
- The SP **does not** require Owner-level permissions.
- These permissions are validated during deployment; if incorrect/missing, you’ll see errors about subnet, DNS zones, or resource provisioning.learn.microsoft+1​

## Microsoft Official References

- [Use a service principal with Azure Kubernetes Service (AKS)][learn.microsoft](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal)​
- [Create a private Azure Kubernetes Service (AKS) cluster][learn.microsoft](https://learn.microsoft.com/en-us/azure/aks/private-clusters)​
- [CustomPrivateDNSZoneMissingPermissions Error Code][learn.microsoft](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/error-codes/customprivatednszonemissingpermissions-error)​
- [Access and identity in Azure Kubernetes Services][learn.microsoft](https://learn.microsoft.com/en-us/azure/aks/concepts-identity)​

---

You **do NOT need to grant your Service Principal permissions to the Azure-managed "MC_" resource group** (the one Azure auto-creates for AKS control plane and infrastructure resources).

**Key points:**

- You create (and assign permissions for) the main resource group holding the AKS resource itself.
- **Azure itself** manages the "MC_\<resgroup>*\<aksname>*\<region>" managed resource group. The AKS resource provider has full control of this RG to operate/scale the cluster and manage infra.
- Your Service Principal only needs permission on the resource group you specify for the *AKS resource* (and any other supporting infrastructure you directly manage—e.g., VNETs, DNS, optionally custom node RG).
- **You should not, and cannot, directly manage or change resources in the MC_ resource group** except through supported AKS/Portal/API actions.kubernetes.anjikeesari+1​

*If deploying with Terraform, set your SP to Contributor on your RG and required subordinate resources; AKS will handle MC* group access under the hood._
