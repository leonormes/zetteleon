---
title: CUH-DP AKS Backup — Terraform
wiki_type: dossier
entity_kind: project
created: 2026-05-19 13:48:00+00:00
modified: 2026-05-22 07:29:00+00:00
tags:
- wiki
- dossier
- project
sources:
- raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform
- raw/2026-05-19-pieces-cuh-dp-aks
- raw/2026-05-19-pieces-terraform-iac
- raw/2026-05-19-pieces-azure-backup
- raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions
- raw/2026-05-21-pieces-cuh-aks-backup-session-compaction
permalink: llmeon/wiki/projects/cuh-dp-aks-backup-terraform
---

## Summary

Production Terraform remediation for Azure AKS Backup on the CUH-DP cluster (`aks-ff-uks-gp-01`). This phase covers the `aks_backup` Terraform module upgrade from v1.0.5 to v1.2.6, fixing destructive plan issues (backup resource group deletion, storage account replacement, AKS cluster replacement), resolving variable interface changes between module versions, and addressing subnet/private endpoint errors blocking FTFL-615. Working directory: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/CUH-DP`.

## Key Facts

- The `aks_backup` module was upgraded from v1.0.5 to v1.2.6, which introduced breaking variable interface changes.
  > "Hermes used variable names from v1.0.5/v1.1.0. The v1.2.x module interface changed." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: 6e187ea0-ea19-4c1a-b738-68c4d21324d1)

- Module v1.2.6 renamed variables: `vault_name` → `backup_vault_name`; `kubernetes_cluster_name` removed; `backup_policy_type`, `backup_policy_time`, `backup_policy_retention_days` removed.
  > "| `vault_name` | `backup_vault_name` |\n  > | `kubernetes_cluster_name` | *(removed — module uses `cluster_id` or reads from data)* |\n  > | `backup_policy_type` | *(removed in v1.2.x)* |" — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: 6e187ea0-ea19-4c1a-b738-68c4d21324d1)

- The module upgrade set `create_backup_resource_group = false` but left `module.aks_backup.azurerm_resource_group.backup_rg` in state, causing a `delete_because_count_index` destroy in the plan.
  > "When Hermes updated the CUH-DP `main.tf` from v1.0.5 to v1.2.6, it added `create_backup_resource_group = false` and switched to referencing the backup RG via a data source. However, `module.aks_backup.azurerm_resource_group.backup_rg` is still in Terraform state from when the module was v1.0.5." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: e0f1c5c0-e3f1-4373-88f3-4183bab8075b)

- Storage account `aksffuksgp01cuhbackup` was flagged for replacement (LRS→ZRS) which would destroy all existing backup data. Fix: explicitly set `storage_account_replication_type = "LRS"` in the module block.
  > "The storage account already has backup data in it. ZRS is better than LRS for resilience, but migrating to it should be a planned, separate piece of work — not a side-effect of a module upgrade." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: 6feaa166-4da9-42aa-82f7-3aa3402866f8)

- AKS cluster `aks-ff-uks-gp-01` was at risk of replacement due to `load_balancer_sku null→standard` drift. The cluster serves live NHS data and must not be destroyed.
  > "The plan shows `module.private-infrastructure.module.aks_cluster.aks_cluster (old)` as a destroy, reason: `load_balancer_sku null→standard`. If this is a full replacement of the AKS cluster, applying will destroy your production cluster and everything running in it." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: d2d30907-fd2d-488c-bfa7-61668f364950)

- FTFL-615 relates to the private endpoint subnet `snet-ff-uks-gp-pe` which doesn't exist yet in `vnet-ff-uks-gp-01` in `rg-ff-uks-gp-net`, causing plan errors.
  > "**Subnet not found**: `snet-ff-uks-gp-pe` doesn't exist in `vnet-ff-uks-gp-01` in `rg-ff-uks-gp-net`. This subnet needs to be created first (it's what FTFL-615 was about - the private endpoint subnet in azure-private-infra)." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: 3be5a210-b419-4345-9460-0193603e1dec)

- A Hermes prompt was crafted to fix three plan errors: (1) subnet not found, (2) storage container 403, (3) module variable mismatches. The prompt instructs reading the actual module interface from `.terraform/modules/` before making changes.
  > "You are an infrastructure-as-code expert fixing three specific plan errors in:\n  /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/CUH-DP" — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: 0793d60b-28cc-4c8f-a1bc-9dbc8c4e3f0e)

- Terraform Cloud plan assessment confirmed the AKS cluster is NOT being deleted (in-place update only), but the backup vault replacement was flagged as CRITICAL.
  > "1. AKS cluster is NOT being deleted - it's an in-place update (good news)\n  > 2. The backup vault is being replaced (CRITICAL - this would lose all backups)" — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: ff9be86d-46ce-4850-8fd7-67f602bb156e)

- Final plan state after fixes: 17 to add, 3 to change, 12 to destroy. Storage account changed from replacement to in-place update (no data loss).
  > "Clean plan. 0 errors.\n  > Plan: 17 to add, 3 to change, 12 to destroy.\n  > • Storage account aksffuksgp01cuhbackup is now an in-place update (not a replacement) — no data loss." — [[raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform]] (Pieces: e561bde9-9ba1-4d64-92c7-8df17177cd3d)

- The existing AKS backup extension on `aks-ff-uks-gp-01` in the CUH/FitFile subscription is named `azure-aks-backup` (not `azbkuextension`), installed in `Failed` state from a prior Terraform timeout. The v1.0.x module used `azure-aks-backup`; the upgraded v1.2.x module uses `azbkuextension`. The type conflict between these two names was resolved by deleting `azure-aks-backup` first.
  > "Extension name on this cluster: `azure-aks-backup` (not `azbkuextension`) — installed in `Failed` state, likely from the Terraform timeout you described in the sprint planning meeting. Terraform v1.0.x used `azure-aks-backup` as the extension name; the upgraded v1.2.x module uses `azbkuextension`." — [[raw/2026-05-19-pieces-terraform-iac]] (Pieces: a55085fd-ea64-43cb-b750-4a1b62880c95)

- After deleting `azure-aks-backup`, the `azbkuextension` must be created fresh. The correct create command uses `--scope cluster`, `--release-train stable`, and passes storage account settings via `--configuration-settings` (not `--config-protected-settings`).
  > "Run the create now:\n  > az k8s-extension create \\\n  >   --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \\\n  >   --name azbkuextension \\\n  >   --extension-type Microsoft.DataProtection.Kubernetes \\\n  >   --scope cluster \\\n  >   --cluster-type managedClusters \\\n  >   --cluster-name aks-ff-uks-gp-01 \\\n  >   --resource-group rg-ff-uks-gp-net" — [[raw/2026-05-19-pieces-terraform-iac]] (Pieces: a4e75b56-6094-48ef-b660-5a548874f4f2)

- The `az k8s-extension create` command was failing with "Multiple extensions of same type is not allowed at this scope" because the existing `azure-aks-backup` extension (type `Microsoft.DataProtection.Kubernetes`) was still present. The JMESPath filter `[?extensionType=='microsoft.dataprotection.kubernetes']` returned empty because the extension was in Failed state and the query was case-sensitive.
  > "az k8s-extension list with a JMESPath query - returned nothing (empty table, because the query used extensionType=='microsoft.dataprotection.kubernetes' but the actual extensionType might be different case or the name is different)" — [[raw/2026-05-19-pieces-terraform-iac]] (Pieces: 9dd3aefc-8d02-4607-963d-ca1158552d87)

### RBAC & Permissions (Sean Donnelly thread)

- Sean Donnelly (CUH) replied confirming the three in-scope resource groups: `aks-ff-uks-gp-01-backup-rg`, `aks-ff-uks-gp-01-snapshot-rg`, and `rg-ff-uks-gp-net`. He noted there appear to be 2 backup groups and asked which snapshot group is correct.
  > "Morning Leon, Thank you for the detailed instructions. Can I confirm the 3 resource groups in-scope? The list below are all the resource groups in the FitFile subscription. We appear to have 2x backup groups and I assume this is the correct snapshot group below? aks-ff-uks-gp-01-backup-rg, aks-ff-uks-gp-01-snapshot-rg" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: 494b0b46-a4e5-4e4a-83c3-9ef0ea139709)

- The correct three resource groups were confirmed as: `rg-ff-uks-gp-net` (AKS cluster RG), `aks-ff-uks-gp-01-backup-rg` (backup vault + storage account), and `aks-ff-uks-gp-01-snapshot-rg` (snapshot RG).
  > "The correct three Resource Groups are: rg-ff-uks-gp-net ✅, aks-ff-uks-gp-01-backup-rg — this is the one containing the backup vault (aksbackupvault) and the storage account (aksffuksgp01backupsa), aks-ff-uks-gp-01-snapshot-rg — this is the correct snapshot group" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: e8302685-7bd8-4b72-bc76-07e7bea2dd06)

- Analysis of `Azureresources.csv` revealed that `aks-ff-uks-gp-01-snapshot-rg` has **zero presence** in the CUH subscription — no matching RG, no resources with "snapshot" anywhere. This means Terraform hasn't created it yet.
  > "Critical finding 1: Snapshot RG doesn't exist yet — aks-ff-uks-gp-01-snapshot-rg has zero presence in the CUH subscription — no matching RG, no resources with 'snapshot' anywhere. This means either: Terraform hasn't created it yet (which is fine — Contributor handles RG creation), OR it will be created during the backup deployment with a different name" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: d0002e72-4ef5-45ed-b426-305b461ec1f8)

- The storage account name was corrected: it is `aksffuksgp01cuhbackup` (not `aksffuksgp01backupsa` which is the NNUH storage account).
  > "The storage account is named aksffuksgp01cuhbackup, not aksffuksgp01backupsa (which is the NNUH storage account)" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: 24c41e73-8c65-4a1a-8dca-dfcddf2812fe)

- The service principal for the Terraform deployment has `ARM_CLIENT_ID: c3791fe2-c768-49d0-8fa0-38ca6b42d4b5`. This was confirmed as the correct SP via HCP Terraform workspace `cuh-poc-1`.
  > "ARM_CLIENT_ID: c3791fe2-c768-49d0-8fa0-38ca6b42d4b5 — confirmed. That's the right SP. Your memory captured two pieces of evidence that together lock this in: 1. HCP Terraform workspace cuh-poc-1 shows this SP" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: 64b8bcbe-8776-470e-a9f5-18878d1a531e)

- Sean needs to apply the `Role Based Access Control Administrator` role at the subscription scope for the Terraform SP. Alexis McKenna (CUH) confirmed she's happy to support the permission request and has looped in Sean.
  > "here is alexis reply to my email. Hi Leon, Thanks for the note. I'm happy to support the approach suggested. I've talked it through with Sean and we can set it up for you. @Sean Donnelly – thank you for picking this up" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: 9a716e2f-9df5-436a-9cb2-bec5ab873663)

- The CUH `cuh-prod-1` cluster is the production blocker — it is in a different subscription and tenant, requiring cross-tenant RBAC which adds complexity and delay to sprint timelines.
  > "The CUH cuh-prod-1 cluster is the production blocker — it is in a different subscription and tenant, requiring cross-tenant RBAC which adds complexity and delay to sprint timelines" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: b6108825-a48d-4afc-84bf-609304ddc985)

- A corrected email reply was drafted to Sean with the right RG names, noting that `pentest-1*` names were from another cluster and the correct names follow the `aks-ff-uks-gp-01-*` pattern.
  > "the rg are called pentest-1* this is not correct! That is from another cluster. it should be rg-ff-uks-gp-backup and rg-ff-uks-gp-snapshot to match the naming of the other rg. update the email reply" — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: 417ee93a-5444-4c4b-8dd5-5e7bf00b8015)

- A Hermes prompt was prepared for updating the CUH-DP Terraform to use the new private endpoint backup module, taking into account existing resources and the FitFile subscription context.
  > "Here's a Hermes prompt ready to paste: You are an infrastructure-as-code expert working on a production Azure AKS Terraform deployment. Mission: Update the Terraform configuration at: /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/CUH-DP to use the updated terraform-azure-aks-backup module configured for fully private endpoint backups." — [[raw/2026-05-19-pieces-cuh-aks-backup-rbac-permissions]] (Pieces: f28df051-70a5-4513-a58f-38fef2818705)

## Timeline

- **2026-05-19** — Module upgrade v1.0.5 → v1.2.6 performed; destructive plan issues identified and analysed; variable interface fixes drafted; storage account LRS fix applied; AKS cluster replacement risk assessed; FTFL-615 subnet error investigated.
- **2026-05-19 (afternoon)** — Extension name conflict discovered: existing `azure-aks-backup` (Failed) vs new `azbkuextension`; delete-and-recreate workflow executed; correct `az k8s-extension create` command identified with proper `--scope cluster` and `--configuration-settings` flags.
- **2026-05-19 (morning)** — Azure resources CSV analysis performed to identify correct resource group names; Sean Donnelly email thread initiated for RBAC permissions; Alexis McKenna confirmed support and looped in Sean; SP details confirmed (`c3791fe2-c768-49d0-8fa0-38ca6b42d4b5`); corrected email drafted with right RG names; Hermes prompt prepared for private endpoint backup module update.

## Connections

- [[Azure AKS Backup — FTFL]] (parent initiative, test cluster phase)
- [[Terraform-Backup]] (related Terraform backup workstream)
- [[Terraform IaC Modules]] (module management)

## Contradictions

- **Storage account name**: Earlier references used `aksffuksgp01backupsa` (NNUH naming convention). Correct name for CUH/FitFile is `aksffuksgp01cuhbackup`. The `aksffuksgp01backupsa` belongs to a different cluster/subscription.
- **Resource group naming**: Earlier references used `pentest-1-backup-rg` and `pentest-1-backup-snapshots-rg`. Correct names follow the `aks-ff-uks-gp-01-*` pattern: `aks-ff-uks-gp-01-backup-rg` and `aks-ff-uks-gp-01-snapshot-rg`.

## Open Questions

- Has the `snet-ff-uks-gp-pe` subnet been created in the CUH subscription, or does FTFL-615 still need to be completed?
- After the variable interface fix and LRS override, is the plan safe to apply to production?
- Does the `load_balancer_sku` drift need to be fixed in code or imported as-is to avoid AKS cluster replacement?
- Has the `azbkuextension` been successfully created and reached `Succeeded` state after the delete-and-recreate workflow?
- After extension creation, have the RBAC role assignments (vault MSI → snapshot RG Contributor, AKS MSI → snapshot RG Contributor) and trusted access binding (`backup-operator`) been re-established for the new extension's MSI?
- Has Sean Donnelly applied the `Role Based Access Control Administrator` role for the Terraform SP at the subscription scope?
- What is the expected timeline for the cross-tenant RBAC setup for the `cuh-prod-1` cluster?