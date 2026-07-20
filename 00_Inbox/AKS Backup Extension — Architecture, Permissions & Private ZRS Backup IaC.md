---
created: 2026-07-16 09:49:11+00:00
modified: 2026-07-20 09:24:50+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-16-2026-10-49am
title: AKS Backup Extension — Architecture, Permissions & Private ZRS Backup IaC
type: note
---

## AKS Backup Extension—Architecture, Permissions & Private ZRS Backup IaC

### Overview

The AKS backup extension is Microsoft's Azure Backup for AKS integration—a Kubernetes-side extension (`azure-aks-backup`, extension type `Microsoft.DataProtection.Kubernetes`) that connects an AKS cluster to an Azure Data Protection Backup Vault, snapshotting cluster-scope resources and PVC volumes on a schedule and writing the vault-store copy to a hardened, privately-networked, ZRS-replicated blob storage account. FITFILE's implementation was first proven manually via Azure CLI on the sandbox cluster `aks-ff-uks-gp-1`, then productionized into the shared Terraform registry module `FITFILE-Platforms/aks-backup/azure` (from `[Editor Content]` capture, "Azure Backup and Restore Runbook"—no URL captured, Obsidian local note).

### Components

| Component | What it is | Evidence |
|---|---|---|
| Backup extension | Kubernetes extension `azure-aks-backup` (`Microsoft.DataProtection.Kubernetes`), installed via `az k8s-extension create --extension-type microsoft.dataprotection.kubernetes` | `pieces_copilot_message_export_may_19_2026_4_50pm` (Obsidian, no URL captured) |
| Backup vault | `Microsoft.DataProtection/backupVaults` resource (e.g. `aksbackupvault`), holds policy + backup-instance metadata, has a system-assigned managed identity | "Azure Backup Vault: sbox-aks-backup-vault"—[portal.azure.com backup vault dashboard](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/GenericPolicyDashboardBlade/PolicyId/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Fsbox-aks-backup-vault%2FbackupPolicies%2Fsbox-aks-backup-policy/dataSourceType/AzureKubernetesServices) |
| Backup storage account (ZRS) | Hardened target storage account (e.g. `aksffuksgp01cuhbackup`, `aksffuksgp01backupsa`), `public_network_access_enabled = false`, TLS 1.2, `shared_access_key_enabled = false`, replication type Standard_ZRS | confirmed live via `az storage account show`: `{"name":"aksffuksgp01backupsa","provisioningState":"Succeeded","sku":"Standard_ZRS"}`—[Azure Cloud Shell session](https://portal.azure.com/auth/login/) |
| Blob container | `aks-backups` (or `aksbackups`), the container the extension writes snapshot metadata/vault-store data into | `az k8s-extension update --configuration-settings blobContainer=…`—[aks-ff-uks-gp-01 Azure Portal](https://portal.azure.com/#@nnuhnorwich.onmicrosoft.com/resource/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01/helm) |
| Private endpoint + subnet | Dedicated PE subnet (e.g. `snet-ff-uks-gp-pe`, `10.0.0.96/27`), private endpoint (e.g. `pe-stffuksgp1backup-blob`) attaching the storage account's blob service to the VNet | "Azure AKS Private Endpoint Backup" (Obsidian, no URL captured) |
| Private DNS zone | `privatelink.blob.core.windows.net`, VNet-linked, with an A record resolving the storage account's public-suffix FQDN to its private IP | "Azure AKS Private Endpoint Backup" (Obsidian, no URL captured) |
| Snapshot resource group | Dedicated RG (e.g. `pentest-1-backup-snapshots-rg`, `aks-ff-uks-gp-01-backup-snapshots-rg`) holding the Azure Disk snapshots that back up PVs | "Azure AKS Private Endpoint Backup Implementation Plan" (Obsidian, no URL captured) |
| Trusted access role binding | `azurerm_kubernetes_cluster_trusted_access_role_binding` (e.g. name `azbkup-trust`, max 24 chars), links the vault to the cluster with role `Microsoft.DataProtection/backupVaults/backup-operator`—note: `restore-operator` is not a valid role in this location | "AKS Trusted Access and Backup Vault CLI Commands" (Obsidian, no URL captured) |
| Backup policy | `azurerm_data_protection_backup_policy_kubernetes_cluster`—defines snapshot cadence (e.g. every 4h, 7-day retention) and vault-store copy cadence (e.g. daily, ~84-day retention) | "AKS Backup Tiering Fix Verification" narrative (Obsidian)—see ZRS section below |
| Backup instance | `azurerm_data_protection_backup_instance_kubernetes_cluster`—the actual protected-resource binding: cluster + included namespaces + backup policy | run [`run-6fpUcdgbAZoMSwB8`](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1/runs/run-6fpUcdgbAZoMSwB8) |

### The private-DNS Routing Dependency (Why tHis is a private-ZRS-specific fOotgun)

Because the storage account has public network access disabled, the AKS nodes must resolve the storage account's public-suffix FQDN (e.g. `aksffuksgp01cuhbackup.blob.core.windows.net`) to the private IP registered in the `privatelink.blob.core.windows.net` zone—not the public Azure IP. FITFILE hit this exact failure on CUH (`aks-ff-uks-gp-01`) on 2026-07-13: DNS queries for the storage account "never reach" the correct zone, confirmed by directly querying the DNS resolver's inbound IP (`10.252.154.40`) and finding the correct private IP (`10.250.16.84`) was registered but never consulted (`AKS Backup DNS Resolution Issue and Fix`, Obsidian note, no URL captured). This was tracked as `FTFL-762` ("Helm Timeout on azure-aks-backup Extension: Proxy & DNS Resolution Failure")—visible on the [FITFILE Sprint 26 Scrum board](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281) (board URL confirmed via browser history; direct issue-level link not separately captured). The fix required a cluster-level `httpProxyConfig.noProxy` entry for the blob domain, applied via the deployment repo (commit tracked at [`a8b068d1`](https://gitlab.com/fitfile/deployment/-/tags)).

### Permissions Model (Three dIstinct iDentities)

1. Terraform Service Principal—needs delegated role-assignment rights (`Microsoft.Authorization/roleAssignments/write`) scoped to `Storage Blob Data Contributor` only, via RBAC Administrator + ABAC condition. Documented in the prior wiki turn (email to Alexis McKenna, CUH, 2026-05-18/19—not re-quoted here per instructions).
2. Backup vault's managed identity (system-assigned)—needs, per the CUH-DP Terraform remediation notes ("CUH-DP AKS Backup—Terraform", Obsidian, no URL captured):
   - `vault_msi_snapshot_contributor_on_snap_rg`—Snapshot Contributor on the snapshot RG
   - `vault_msi_read_on_snap_rg`—Reader on the snapshot RG
   - `vault_msi_read_on_cluster`—Reader on the AKS cluster
   - `vault_data_operator_on_snap_rg`—Data Operator for Managed Disks on the snapshot RG
   - `vault_data_contributor_on_storage`—Storage Blob Data Contributor on the backup storage account
3. Backup extension's own managed identity (distinct from the vault's identity)—needs `extension_storage_account_permission`: Storage Blob Data Contributor, scoped to the backup storage account, so the extension pod can write blob data directly. This is the specific role assignment that appears as its own Terraform resource, `module.aks_backup.azurerm_role_assignment.extension_storage_account_permission`, in every HCP Terraform plan—e.g. run [`run-ZHneBExMGdRmuEWU`](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1/runs/run-ZHneBExMGdRmuEWU) and run [`run-XrLLk2g6pdUvx6Cd`](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1/runs/run-XrLLk2g6pdUvx6Cd).

### The Terraform IaC—module Structure and Versions

FITFILE's backup automation lives in the shared private registry module `FITFILE-Platforms/aks-backup/azure` (`terraform-azure-aks-backup` source repo). Confirmed versions in the registry: v1.0.5 → v1.2.6 → v2.0.0—see [module v2.0.0 registry page](https://app.terraform.io/app/FITFILE-Platforms/registry/modules/private/FITFILE-Platforms/aks-backup/azure/2.0.0), captured earlier this session.

Example module invocation (from Cursor, `main.tf — CUH-DP`, vision capture, no URL—local editor content):

```hcl
module "aks_backup" {
  source                        = "app.terraform.io/FITFILE-Platforms/aks-backup/azure"
  version                        = "1.2.6"
  create_backup_resource_group   = false
  backup_resource_group_name     = data.azurerm_resource_group.backup.name
  snapshot_resource_group_name   = "${local.aks_cluster_name}-snapshot-rg"
  storage_account_name           = data.azurerm_storage_account.backup.name
  backup_vault_name              = data.azurerm_data_protection_backup_vault.backup.name
  create_private_endpoint        = true
  private_endpoint_subnet_id     = azurerm_subnet.private_endpoint.id
  vnet_id                        = data.azurerm_virtual_network.aks.id
  kubernetes_cluster_id          = local.aks_cluster_id
  backup_included_namespaces     = ["cuh-prod-1", "spicedb"]
  backup_policy_name             = "dailyaksbackups"
  retention_days                 = 14
}
```

Resources the module actually creates, confirmed directly from live HCP Terraform plan output:

- `module.aks_backup.azurerm_data_protection_backup_vault.backup_vault`
- `module.aks_backup.azurerm_data_protection_backup_policy_kubernetes_cluster.backup_policy`
- `module.aks_backup.azurerm_data_protection_backup_instance_kubernetes_cluster.backup_instance`
- `module.aks_backup.azurerm_kubernetes_cluster_extension.backup_extension`
- `module.aks_backup.azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access`
- `module.aks_backup.azurerm_role_assignment.extension_storage_account_permission`
- `module.aks_backup.azurerm_storage_account.backup_sa`
- `azurerm_subnet.private_endpoint`
- `module.aks_backup.azurerm_private_endpoint.backup_sa_blob[0]`
- `module.aks_backup.azurerm_private_dns_zone.blob[0]`
- `module.aks_backup.azurerm_private_dns_zone_virtual_network_link.blob[0]`

Source: run [`run-VsHz6gWZmEyW3MzJ`](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1/runs/run-VsHz6gWZmEyW3MzJ), which shows all of these transitioning `Created`/`Creating` in a single apply.

Breaking variable renames between module versions (v1.0.5 → v1.2.6), from `CUH-DP AKS Backup — Terraform` (Obsidian, no URL captured):

- `vault_name` → `backup_vault_name`
- `kubernetes_cluster_name`—removed
- `backup_policy_type`, `backup_policy_time`, `backup_policy_retention_days`—removed

Provider-level requirement: `storage_use_azuread = true` must be set on the `azurerm` provider block itself, not just inside the module—the storage account disables shared-key auth (`shared_access_key_enabled = false`), so Terraform must authenticate to the storage data plane via Azure AD. Source: "Azure Backup and Restore Runbook" (Obsidian, no URL captured).

### The ZRS-specific Destructive-replace Trap

The single most important IaC gotcha for the private ZRS variant: bumping the module version (or otherwise touching `storage_account_replication_type`) can cause Terraform to plan a destructive replacement of the backup storage account—deleting all existing backup data—if the module's default replication type doesn't match what's live in Azure. This happened on CUH-DP:

> "Storage account `aksffuksgp01cuhbackup` was flagged for replacement (LRS to ZRS) which would destroy all existing backup data. Fix: explicitly set `storage_account_replication_type = "LRS"` in the module block."
> —"CUH-DP AKS Backup—Terraform" (Obsidian, no URL captured)

The safe migration path used elsewhere in the estate is: (1) leave `storage_account_replication_type` matching the live SKU in Terraform to avoid a plan-time replacement, (2) run the actual LRS→ZRS conversion out-of-band via `az storage account migration start --sku Standard_ZRS` (an async, up-to-72-hour operation under a human's PIM-elevated `Storage Account Contributor`/`Contributor` grant—not currently modeled in the Terraform module at all), (3) once `az storage account migration show` confirms `Succeeded`, optionally reconcile the Terraform variable to `ZRS` afterward so a future `terraform plan` doesn't drift. This sequencing is confirmed by the tracked ticket `FTFL-525` ("Ensure all backups are ZRS")—[Jira ticket](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2865528839/FITFILE+CI+CD+Pipeline+Design+Document+Improvement+Plan)—which as of 2026-07-07 showed NNUH's migration kicked off and MKUH's RBAC blocker fixed, with CUH still blocked on the DNS issue described above (source: "FTFL-525: Ensure All Backups Are ZRS—Current Status" 2026-07-07 daily note, Obsidian, no URL captured).

### Open Loops Worth Flagging

- `FTFL-615`—private endpoint subnet work for the backup storage container—[Jira ticket](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2865528839/FITFILE+CI+CD+Pipeline+Design+Document+Improvement+Plan).
- `FTFL-605`—the permissions-audit ticket that originally identified the three-MSI gap (vault, extension, cluster) documented above—no URL captured in memory for this specific ticket.
- `FTFL-762`—DNS/proxy fix for the backup extension's Helm install—tracked on the [Sprint 26 board](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281), no issue-level URL captured separately.
- CUH's private ZRS backup was still blocked on DNS as of the most recent evidence (2026-07-14 email to Alexis McKenna re: DNS resolution)—I found no later tool result confirming resolution; worth verifying live before treating this wiki's "working" architecture description as CUH's current production state.