---
title: pieces_copilot_message_export_july_16_2026_10_20am
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-16-2026-10-20am
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 16, 2026 - 10:20 AM*
---
## Deployment Permissions - FITFILE

```yaml
title: "Deployment Permissions - FITFILE"
source: "https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2240151566/Deployment+Permissions"
captured: "2026-07-16T10:13:18+01:00"
status: "processing"
tags:
  - "input"
type: "head"
```

### Raw Output / Content

## Deployment Permissions

### Permissions for the Terraform Cloud Service Principal (The Identity Creating and Operating the Cluster)

To achieve least privilege, instead of a blanket `Contributor` role, we should create a custom Azure role definition that includes only these specific actions.

Here's a breakdown of the permissions for the Terraform Cloud Service Principal:

- **Compute-Related Permissions**: essential for managing virtual machines (VMs), disks, and related components that make up the AKS nodes:
  - `Microsoft.Compute/diskEncryptionSets/read`: to read disk encryption set IDs.
  - `Microsoft.Compute/proximityPlacementGroups/write`: for updating proximity placement groups.
  - `Microsoft.Compute/disks/`: for configuring Azure Disks.
  - `Microsoft.Compute/virtualMachines/`: for managing virtual machines. This likely includes `Microsoft.Compute/virtualMachines/extensions/` and `Microsoft.Compute/virtualMachines/powerOff/action`.
  - `Microsoft.Compute/locations/vmSizes/read`: to find information about virtual machine sizes for volume limits.
  - `Microsoft.Compute/locations/operations/read`: to find information about virtual machine operations.
- **Network-Related Permissions**: necessary for configuring virtual networks, load balancers, and network interfaces:
  - `Microsoft.Network/virtualNetworks/joinLoadBalancer/action`: required to configure IP-based Load Balancer Backend Pools.
  - `Microsoft.Network/networkInterfaces/`: for managing network interfaces.
  - `Microsoft.Network/virtualNetworks/` and `Microsoft.Network/virtualNetworks/subnets/`: for managing virtual networks and subnets. More specifically, if using a custom VNet, you'd need `Microsoft.Network/virtualNetworks/subnets/read` and `Microsoft.Network/virtualNetworks/subnets/join/action`.
- **Managed Identity Permissions**: crucial for enabling the AKS cluster to use its own managed identity for Azure resource access (recommended over Service Principals for AKS cluster identity):
  - `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action`: needed by the identity creating the cluster to assign user-assigned managed identities to resources (like the AKS nodes).
- **AKS Cluster Management Permissions**:
  - `Microsoft.ContainerService/managedClusters/`: a broad permission for creating and operating the AKS cluster itself. While still broad, it's specific to the AKS resource type.
- **Resource Management Permissions**: for managing resource groups and subscriptions:
  - `Microsoft.Resources/subscriptions/providers/read`: to read providers.
  - `Microsoft.Resources/subscriptions/resourcegroups/`: for managing resource groups.
- **Monitoring-Related Permissions**: for configuring Log Analytics workspaces and Container Insights:
  - `Microsoft.OperationalInsights/workspaces/sharedkeys/read`.
  - `Microsoft.OperationalInsights/workspaces/read`.
  - `Microsoft.OperationsManagement/solutions/write`.
  - `Microsoft.OperationsManagement/solutions/read`: required to create and update Log Analytics workspaces and Azure monitoring for containers.
- **Role Assignment Permissions** (for assigning roles to the AKS Cluster Identity):
  - `User Access Administrator` role with a specific condition: the "FITFILE Azure Deployment - Customer Checklist" explicitly states that "another role assignment needs to be added to allow the service principal to assign a specific role for the AKS cluster identity." This role is `User Access Administrator` on the subscription, with a condition to constrain it to the `Network Contributor` role. This is critical because the AKS cluster's managed identity requires `Network Contributor` access on the virtual network and API server subnet for its operations, especially in AKS Automatic with custom VNets. The Service Principal needs permission to *assign* this role.

### Permissions for the AKS Cluster's Own Managed Identity

Once the AKS cluster is deployed by your Service Principal, the cluster itself will use a managed identity to interact with other Azure services. This is distinct from the Service Principal that deployed it, and managed identities are the recommended approach for the cluster's runtime operations due to automatic credential management.

The `azure-aks.pdf` details the permissions needed by the "AKS cluster identity":

- `Microsoft.ContainerService/managedClusters/`: general operations related to the managed cluster.
- `Microsoft.Network/loadBalancers/`: for configuring the load balancer for Kubernetes services.
- `Microsoft.Compute/disks/`: for configuring Azure Disks.
- `Microsoft.Storage/storageAccounts/`: for configuring storage accounts for AzureFile or AzureDisk.
- `Microsoft.Network/routeTables/`: for configuring route tables and routes for nodes.
- `Microsoft.Compute/virtualMachines/read` and `Microsoft.Compute/virtualMachines/write`: for finding information about VMs and attaching Azure Disks.
- `Microsoft.Compute/virtualMachineScaleSets/`: for managing VM scale sets, including adding/deleting VMs and associating with load balancers.
- `Microsoft.Network/networkInterfaces/read`: to search internal IPs and load balancer backend address pools.
- `Microsoft.Compute/snapshots/`: for configuring snapshots for AzureDisk.

Additionally, specifically for AKS Automatic clusters with custom virtual networks, the cluster identity requires the `Network Contributor` built-in role assignment on the API server subnet and the virtual network to support Node Auto Provisioning.

### Permissions for Private Backups (ZRS) — new section, added 2026-07-16

Deploying **fully private, zone-redundant (ZRS) backups** on top of an already-running cluster surfaces a gap the base Contributor role does not cover: **role delegation**. This section documents the specific request that was made for CUH and the actual, evidenced pattern behind it.

#### The core blocker

The `azure-aks-backup` Kubernetes extension installs its own Managed Service Identity (MSI) into the cluster. To let that MSI write backup data to the private blob container, Terraform must assign it **Storage Blob Data Contributor** on the backup storage account — an action gated by `Microsoft.Authorization/roleAssignments/write`. Contributor "can create resources but cannot delegate rights to them," so every apply hits:

> `403 Forbidden` on `Microsoft.Authorization/roleAssignments/write`

This is confirmed independently in two places in the CUH thread: the 2026-05-18 email to Alexis McKenna ("Technical Update: Required Terraform Permissions for CUH Private AKS Backups") and a later reply to Sean Donnelly on the same thread — both describe the identical mechanism.

#### The requested/granted permission

Two versions of the ask appear in the record, and the record shows the final, narrower version is what was actually sent and actioned:

- **Early draft (2026-05-18, to Alexis McKenna directly):** a straight upgrade to **RBAC Administrator** scoped to three resource groups — `rg-ff-uks-gp-net`, `pentest-1-backup-rg`, `pentest-1-backup-snapshots-rg`.
- **Final version sent to Sean Donnelly** (same thread, after Alexis looped Sean in on 2026-05-18/19): **RBAC Administrator + an Azure ABAC condition** restricting the SP to delegate *only* one role — **Storage Blob Data Contributor**, built-in role ID `ba92f5b4-2d11-453d-a403-e96b0029c9fe` — scoped to a *different* three-RG set: `rg-ff-uks-gp-net`, `rg-ff-uks-gp-backup`, `rg-ff-uks-gp-snapshot`.

**Unresolved discrepancy — flagging rather than guessing:** the RG names differ between the two emails in the same thread (`pentest-1-backup-rg`/`pentest-1-backup-snapshots-rg` vs. `rg-ff-uks-gp-backup`/`rg-ff-uks-gp-snapshot`). Both are verbatim from LTM tool output, so this isn't a transcription error on my part — it looks like the RG naming itself shifted between the sandbox/pentest environment and the production CUH environment as the request was finalized. If you're pasting this into the live wiki, confirm which RG set is current before publishing.

Alexis McKenna (Enterprise Architect, CUH) confirmed support for the approach and looped in Sean Donnelly to implement it: *"I'm happy to support the approach suggested. I've talked it through with Sean and we can set it up for you."*

The exact ABAC condition sent to Sean Donnelly:

```text
(
  !(ActionMatches{'Microsoft.Authorization/roleAssignments/write'})
  OR
  @Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] StringEqualsIgnoreCase 'ba92f5b4-2d11-453d-a403-e96b0029c'
)
AND
(
  !(ActionMatches{'Microsoft.Authorization/roleAssignments/delete'})
  OR
  @Resource[Microsoft.Authorization/roleAssignments:RoleDefinitionId] StringEqualsIgnoreCase 'ba92f5b4-2d11-453d-a403-e96b0029c'
)
```

**Note on the condition string itself:** the role-ID fragment in the ABAC condition as captured in LTM reads `'ba92f5b4-2d11-453d-a403-e96b0029c'` (missing the trailing `9fe`), while the full role ID stated in prose in the same email and in the earlier draft is `ba92f5b4-2d11-453d-a403-e96b0029c9fe`. This is very likely a capture/OCR truncation of the condition syntax rather than a real typo in the sent email, but I can't confirm which is correct from the tool output alone — verify against the actual sent email before relying on the condition string operationally.

Target SP identified in the final email: **FITFILE Terraform Cloud Provisioner**, App (Client) ID `c3791fe2-c768-49d0-8fa0-38ca6b42d4b5`. Note this differs from the AppId cited elsewhere in your notes for the same-named SP (`1a596ad4-d99d-468f-8703-820c09d0bb79`, from an internal security-review ticket) — another discrepancy I can't resolve from LTM alone; possibly two different subscriptions' instances of a similarly-named SP (test vs. CUH prod), but flagging rather than assuming.

#### Permissions audit reference

An internal permissions-audit ticket, `FTFL-605` (no browser history match found for a direct ticket URL — link not fabricated), identified three concrete gaps feeding into the above design:

- AKS cluster MSI needs **Contributor** on the snapshot RG.
- Backup Vault MSI needs **Reader/Contributor** on the snapshot RG.
- Extension MSI needs **Storage Blob Data Contributor** on the storage account.

#### ZRS conversion — a separate, currently manual, permission path

Distinct from the private-backup role-delegation work above: converting backup storage accounts to **Zone-Redundant Storage (Standard_ZRS)** is tracked under ticket [`FTFL-525` — "Ensure all backups are ZRS"](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2865528839/FITFILE+CI+CD+Pipeline+Design+Document+Improvement+Plan), confirmed via a direct Jira page visit in browser history. This ticket covers MKUH, NNUH, and CUH.

Per LTM, the ZRS migrations actually run (`aksffuksgp01backupsa`, `aksmkuhuksprd01bkp01`) were executed manually via `az storage account migration start` under a human operator's own Azure PIM-activated **Contributor** grant on the subscription — **not** by the Terraform SP, and the `terraform-azure-aks-backup` module does not currently automate this step. If Terraform is to own this in future, the SP would additionally need `Microsoft.Storage/storageAccounts/migration/start/action`, which sits in the built-in **Storage Account Contributor** role (confirmed via Azure documentation, not LTM — this specific action was not found anywhere in your captured memory, only the manual CLI usage was).

**Ticket cross-reference note:** the internal ticket referenced for the original SP UAA-removal recommendation (`EntraFF-03`, "Review and update FITFILE Terraform Cloud Provisioner Service Principal permissions") returned no matches in browser history at all — kept in backticks with no link, unconfirmed whether it's a real/live ticket ID or a session-local label.