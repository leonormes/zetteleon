---
created: 2026-07-16T08:53:55+00:00
modified: 2026-07-20T16:34:46+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-16-2026-10-20am
title: "Current Terraform SP permissions vs what's needed for private ZRS backups"
type: note
---

## Current Terraform SP Permissions vs. What's Needed for Private ZRS Backups

Based on what's in your LTM, here's the grounded diff. I'm flagging explicitly where a fact is sourced from your memory vs. from external Azure documentation.

### What the Terraform SP Has Today (Grounded in LTM)

- Contributor at subscription/resource-group scope—this is the baseline the Terraform Cloud Provisioner service principal (AppId `1a596ad4-d99d-468f-8703-820c09d0bb79`) runs deployments under, confirmed in your `[EntraFF-03] Review and update FITFILE Terraform Cloud Provisioner Service Principal permissions` ticket note.
- That same note flags the SP _also_ historically held User Access Administrator (UAA) on the subscription—which a Prowler check (`iam_role_user_access_admin_restricted`) failed, because UAA is effectively Owner-equivalent (it can assign _any_ role to _any_ identity).
- A separate security remediation doc from your Backlog Refinement session (Jul 6) explicitly recommends: _"Remove User Access Administrator role from the Terraform SP immediately… create a scoped custom role with only `Microsoft.Authorization/roleAssignments/write` on specific resource groups."_ So the direction of travel your team already committed to is narrow-scoped role-assignment delegation, not blanket UAA.
- Contributor alone is confirmed insufficient for the backup pipeline: your `terraform-azure-aks-backup` module needs to create several `azurerm_role_assignment` resources itself (`vault_msi_snapshot_contributor_on_snap_rg`, `vault_msi_read_on_snap_rg`, `vault_msi_read_on_cluster`, `vault_data_operator_on_snap_rg`, `vault_data_contributor_on_storage`, `extension_storage_account_permission` → Storage Blob Data Contributor), and Contributor "can create resources but cannot delegate rights to them."

### The Specific Permission Gap Already Identified and Requested (Grounded)

Your `2026-05-18` email thread to Alexis McKenna (Cambridge University Hospitals NHS FT), cc Susannah Thomas / Robin Mofakham / Helena Ahlfors, documents the exact blocker and the exact ask:

- Blocker: `403 Forbidden` on `Microsoft.Authorization/roleAssignments/write`—Contributor "cannot do this."
- Requested fix: grant the Terraform SP Role Based Access Control Administrator, constrained by an Azure ABAC condition so it can _only_ ever assign one role—Storage Blob Data Contributor (built-in role ID `ba92f5b4-2d11-453d-a403-e96b0029c9fe`)—and _only_ within three named resource groups: `rg-ff-uks-gp-net`, `pentest-1-backup-rg`, `pentest-1-backup-snapshots-rg`.

This request covers the private backup / private-endpoint half of the work but does not mention ZRS anywhere in that thread—it predates the ZRS conversion work by about two months.

### What ZRS Conversion Additionally Needs (Mixed: LTM + web_search)

From your LTM: the ZRS conversions you've actually run (`aksffuksgp01backupsa`, `aksmkuhuksprd01bkp01` → `Standard_ZRS`) were done manually via `az storage account migration start`/`show`, executed under your own Azure PIM-activated Contributor role at the `suber-sde-prd` subscription scope (per the Jul 13 "ZRS Conversion Verification Checklist" and Cloud Shell session)—not by the Terraform SP, and not via the `terraform-azure-aks-backup` module. Terraform never touches storage replication type migration today.

External confirmation (Microsoft Azure docs, via web_search—this specific fact is not in your LTM): the action that gates `az storage account migration start` is `Microsoft.Storage/storageAccounts/migration/start/action`, which is included in the built-in Storage Account Contributor role but _not_ in the plain Storage Contributor role. Storage Blob Data Contributor (the data-plane role your team already grants) does not cover this—it's a separate management-plane action.

### The Diff

| Permission | Currently on TF SP? | Needed for private backup | Needed for ZRS | Source |
|---|---|---|---|---|
| Contributor (sub/RG scope) | ✅ Yes | Baseline (insufficient alone) | Baseline (insufficient alone) | LTM |
| User Access Administrator | ⚠️ Yes (flagged for removal) | Not recommended—over-broad | Not recommended—over-broad | LTM |
| RBAC Administrator + ABAC condition limited to `Storage Blob Data Contributor`, scoped to `rg-ff-uks-gp-net` / `pentest-1-backup-rg` / `pentest-1-backup-snapshots-rg` | ❌ Requested, not yet confirmed granted | ✅ Required (unblocks `roleAssignments/write` for vault MSI + extension identity) | Not directly relevant | LTM (email to Alexis McKenna, 2026-05-18) |
| Storage Account Contributor (or custom role carrying `Microsoft.Storage/storageAccounts/migration/start/action`), scoped to the backup storage account(s) | ❌ Not present—ZRS migrations run manually under your personal PIM Contributor grant | Not required | ✅ Required if you want Terraform (not a human with PIM) to trigger ZRS conversion | web_search (Azure docs)—no LTM equivalent found |

### Bottom line—what to Add to the SP

1. Confirm/chase the already-requested RBAC Administrator + ABAC-constrained delegation (Storage Blob Data Contributor only, 3 RGs) from Alexis McKenna at CUH—this is what unblocks the existing backup-vault role assignments Terraform needs to create. I don't have a tool result confirming this was ever granted; worth checking directly with CUH.
2. Net-new for ZRS automation: add `Storage Account Contributor` (or a narrower custom role exposing just `Microsoft.Storage/storageAccounts/migration/start/action`) scoped to each customer's backup storage account, since today that step happens manually under your own elevated access rather than through the SP at all.

Caveat on scope: this diff is built from the CUH thread and the shared `terraform-azure-aks-backup` module—I did not find LTM evidence of per-customer variance (e.g. whether NNUH/MKUH SPs already have the RBAC-Admin grant that CUH is still pending). If you want, I can check NNUH/MKUH-specific threads next to see if that grant landed there first.

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 16, 2026 - 10:20 AM_
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

- Compute-Related Permissions: essential for managing virtual machines (VMs), disks, and related components that make up the AKS nodes:
  - `Microsoft.Compute/diskEncryptionSets/read`: to read disk encryption set IDs.
  - `Microsoft.Compute/proximityPlacementGroups/write`: for updating proximity placement groups.
  - `Microsoft.Compute/disks/`: for configuring Azure Disks.
  - `Microsoft.Compute/virtualMachines/`: for managing virtual machines. This likely includes `Microsoft.Compute/virtualMachines/extensions/` and `Microsoft.Compute/virtualMachines/powerOff/action`.
  - `Microsoft.Compute/locations/vmSizes/read`: to find information about virtual machine sizes for volume limits.
  - `Microsoft.Compute/locations/operations/read`: to find information about virtual machine operations.
- Network-Related Permissions: necessary for configuring virtual networks, load balancers, and network interfaces:
  - `Microsoft.Network/virtualNetworks/joinLoadBalancer/action`: required to configure IP-based Load Balancer Backend Pools.
  - `Microsoft.Network/networkInterfaces/`: for managing network interfaces.
  - `Microsoft.Network/virtualNetworks/` and `Microsoft.Network/virtualNetworks/subnets/`: for managing virtual networks and subnets. More specifically, if using a custom VNet, you'd need `Microsoft.Network/virtualNetworks/subnets/read` and `Microsoft.Network/virtualNetworks/subnets/join/action`.
- Managed Identity Permissions: crucial for enabling the AKS cluster to use its own managed identity for Azure resource access (recommended over Service Principals for AKS cluster identity):
  - `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action`: needed by the identity creating the cluster to assign user-assigned managed identities to resources (like the AKS nodes).
- AKS Cluster Management Permissions:
  - `Microsoft.ContainerService/managedClusters/`: a broad permission for creating and operating the AKS cluster itself. While still broad, it's specific to the AKS resource type.
- Resource Management Permissions: for managing resource groups and subscriptions:
  - `Microsoft.Resources/subscriptions/providers/read`: to read providers.
  - `Microsoft.Resources/subscriptions/resourcegroups/`: for managing resource groups.
- Monitoring-Related Permissions: for configuring Log Analytics workspaces and Container Insights:
  - `Microsoft.OperationalInsights/workspaces/sharedkeys/read`.
  - `Microsoft.OperationalInsights/workspaces/read`.
  - `Microsoft.OperationsManagement/solutions/write`.
  - `Microsoft.OperationsManagement/solutions/read`: required to create and update Log Analytics workspaces and Azure monitoring for containers.
- Role Assignment Permissions (for assigning roles to the AKS Cluster Identity):
  - `User Access Administrator` role with a specific condition: the "FITFILE Azure Deployment - Customer Checklist" explicitly states that "another role assignment needs to be added to allow the service principal to assign a specific role for the AKS cluster identity." This role is `User Access Administrator` on the subscription, with a condition to constrain it to the `Network Contributor` role. This is critical because the AKS cluster's managed identity requires `Network Contributor` access on the virtual network and API server subnet for its operations, especially in AKS Automatic with custom VNets. The Service Principal needs permission to _assign_ this role.

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

### Permissions for Private Backups (ZRS)—new Section, Added 2026-07-16

Deploying fully private, zone-redundant (ZRS) backups on top of an already-running cluster surfaces a gap the base Contributor role does not cover: role delegation. This section documents the specific request that was made for CUH and the actual, evidenced pattern behind it.

#### The Core Blocker

The `azure-aks-backup` Kubernetes extension installs its own Managed Service Identity (MSI) into the cluster. To let that MSI write backup data to the private blob container, Terraform must assign it Storage Blob Data Contributor on the backup storage account—an action gated by `Microsoft.Authorization/roleAssignments/write`. Contributor "can create resources but cannot delegate rights to them," so every apply hits:

> `403 Forbidden` on `Microsoft.Authorization/roleAssignments/write`

This is confirmed independently in two places in the CUH thread: the 2026-05-18 email to Alexis McKenna ("Technical Update: Required Terraform Permissions for CUH Private AKS Backups") and a later reply to Sean Donnelly on the same thread—both describe the identical mechanism.

#### The requested/granted Permission

Two versions of the ask appear in the record, and the record shows the final, narrower version is what was actually sent and actioned:

- Early draft (2026-05-18, to Alexis McKenna directly): a straight upgrade to RBAC Administrator scoped to three resource groups—`rg-ff-uks-gp-net`, `pentest-1-backup-rg`, `pentest-1-backup-snapshots-rg`.
- Final version sent to Sean Donnelly (same thread, after Alexis looped Sean in on 2026-05-18/19): RBAC Administrator + an Azure ABAC condition restricting the SP to delegate _only_ one role—Storage Blob Data Contributor, built-in role ID `ba92f5b4-2d11-453d-a403-e96b0029c9fe`—scoped to a _different_ three-RG set: `rg-ff-uks-gp-net`, `rg-ff-uks-gp-backup`, `rg-ff-uks-gp-snapshot`.

Unresolved discrepancy—flagging rather than guessing: the RG names differ between the two emails in the same thread (`pentest-1-backup-rg`/`pentest-1-backup-snapshots-rg` vs. `rg-ff-uks-gp-backup`/`rg-ff-uks-gp-snapshot`). Both are verbatim from LTM tool output, so this isn't a transcription error on my part—it looks like the RG naming itself shifted between the sandbox/pentest environment and the production CUH environment as the request was finalized. If you're pasting this into the live wiki, confirm which RG set is current before publishing.

Alexis McKenna (Enterprise Architect, CUH) confirmed support for the approach and looped in Sean Donnelly to implement it: _"I'm happy to support the approach suggested. I've talked it through with Sean and we can set it up for you."_

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

Note on the condition string itself: the role-ID fragment in the ABAC condition as captured in LTM reads `'ba92f5b4-2d11-453d-a403-e96b0029c'` (missing the trailing `9fe`), while the full role ID stated in prose in the same email and in the earlier draft is `ba92f5b4-2d11-453d-a403-e96b0029c9fe`. This is very likely a capture/OCR truncation of the condition syntax rather than a real typo in the sent email, but I can't confirm which is correct from the tool output alone—verify against the actual sent email before relying on the condition string operationally.

Target SP identified in the final email: FITFILE Terraform Cloud Provisioner, App (Client) ID `c3791fe2-c768-49d0-8fa0-38ca6b42d4b5`. Note this differs from the AppId cited elsewhere in your notes for the same-named SP (`1a596ad4-d99d-468f-8703-820c09d0bb79`, from an internal security-review ticket)—another discrepancy I can't resolve from LTM alone; possibly two different subscriptions' instances of a similarly-named SP (test vs. CUH prod), but flagging rather than assuming.

#### Permissions Audit Reference

An internal permissions-audit ticket, `FTFL-605` (no browser history match found for a direct ticket URL—link not fabricated), identified three concrete gaps feeding into the above design:

- AKS cluster MSI needs Contributor on the snapshot RG.
- Backup Vault MSI needs Reader/Contributor on the snapshot RG.
- Extension MSI needs Storage Blob Data Contributor on the storage account.

#### ZRS conversion—a Separate, Currently Manual, Permission Path

Distinct from the private-backup role-delegation work above: converting backup storage accounts to Zone-Redundant Storage (Standard_ZRS) is tracked under ticket [`FTFL-525` — "Ensure all backups are ZRS"](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2865528839/FITFILE+CI+CD+Pipeline+Design+Document+Improvement+Plan), confirmed via a direct Jira page visit in browser history. This ticket covers MKUH, NNUH, and CUH.

Per LTM, the ZRS migrations actually run (`aksffuksgp01backupsa`, `aksmkuhuksprd01bkp01`) were executed manually via `az storage account migration start` under a human operator's own Azure PIM-activated Contributor grant on the subscription—not by the Terraform SP, and the `terraform-azure-aks-backup` module does not currently automate this step. If Terraform is to own this in future, the SP would additionally need `Microsoft.Storage/storageAccounts/migration/start/action`, which sits in the built-in Storage Account Contributor role (confirmed via Azure documentation, not LTM—this specific action was not found anywhere in your captured memory, only the manual CLI usage was).

Ticket cross-reference note: the internal ticket referenced for the original SP UAA-removal recommendation (`EntraFF-03`, "Review and update FITFILE Terraform Cloud Provisioner Service Principal permissions") returned no matches in browser history at all—kept in backticks with no link, unconfirmed whether it's a real/live ticket ID or a session-local label.
