---
title: CUH-DP AKS Backup — Terraform
wiki_type: dossier
entity_kind: project
created: 2026-05-19T13:48:00+00:00
modified: 2026-05-19T13:48:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-19-pieces-cuh-dp-aks-backup-terraform
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

## Timeline

- **2026-05-19** — Module upgrade v1.0.5 → v1.2.6 performed; destructive plan issues identified and analysed; variable interface fixes drafted; storage account LRS fix applied; AKS cluster replacement risk assessed; FTFL-615 subnet error investigated.

## Connections

- [[Azure AKS Backup — FTFL]] (parent initiative, test cluster phase)
- [[Terraform-Backup]] (related Terraform backup workstream)
- [[Terraform IaC Modules]] (module management)

## Contradictions

_(none identified)_

## Open Questions

- Has the `snet-ff-uks-gp-pe` subnet been created in the CUH subscription, or does FTFL-615 still need to be completed?
- After the variable interface fix and LRS override, is the plan safe to apply to production?
- Does the `load_balancer_sku` drift need to be fixed in code or imported as-is to avoid AKS cluster replacement?
