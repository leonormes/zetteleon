---
created: 2026-07-16T08:53:55+00:00
modified: 2026-07-16T09:02:27+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-16-2026-9-53am
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
