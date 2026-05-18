*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 11:34 AM*
---
I now have a complete and thorough picture. Here's the full research and validation:

---

## CUH Private Endpoint Backup — Permission Request Research & Validation

### What the blocker actually is

Your Terraform Service Principal (SP) currently holds **Contributor** at the subscription level. When the private backup pipeline runs, Terraform attempts to assign the `Storage Blob Data Contributor` role to the AKS backup extension's Managed Service Identity (MSI) so it can write cluster data to the blob container. This hits a **403 Forbidden on `Microsoft.Authorization/roleAssignments/write`** — Contributor cannot delegate roles.

This was confirmed in investigation findings from **14 May 2026** (referenced in your Obsidian notes: `Terraform RBAC Updates for Private AKS Backups`). Additionally, ABAC conditions on existing role assignments are further gating the `roleAssignments/write` action (referenced error log: `run-qeQ41dgowhaGbMLn`).

---

### What permission was requested (the evolved ask)

The email went through several drafts this morning. The **final, most tightly scoped version** (captured at ~10:54 AM today, subject: *"Security Enhancement: Private Backup Implementation for CUH AKS Cluster — Permission Request"*) refined the ask beyond a simple RBAC Administrator elevation:

**Requested permission (final version):**

> Grant the Terraform SP the **`Role Based Access Control Administrator`** role with an **Azure ABAC condition** that constrains it to only ever assign one specific role:
> **`Storage Blob Data Contributor`** (Azure built-in role ID: `ba92f5b4-2d11-453d-a403-e96b0029c9fe`)

**Scoped strictly to these three Resource Groups only** (not the full subscription):

| Resource Group | Purpose |
|---|---|
| `rg-ff-uks-gp-net` | AKS cluster |
| `pentest-1-backup-rg` | Backup vault |
| `pentest-1-backup-snapshots-rg` | Snapshot store |

The ABAC condition approach means: the SP can only grant `Storage Blob Data Contributor` — it cannot assign any other role, and cannot act outside those three RGs. This is the documented Microsoft-supported pattern from the role assignment conditions documentation.

---

### Is this the **only** permission needed? Validation

Your memory also captured the FTFL-605 work (the permissions audit ticket, marked **Done** as of Sprint 16). The notes from the IaC audit (`aks_backup_iac_audit_plan_98daf4dd.plan.md`) explicitly documented the RBAC gaps as:

> - AKS cluster MSI → needs `Contributor` on snapshot RG
> - Vault MSI → needs `Reader`/`Contributor` on snapshot RG
> - Extension MSI → needs **`Storage Blob Data Contributor`** on storage account

The extension MSI role assignment is the **only one that requires the SP to perform a `roleAssignments/write`** action. The other two (cluster MSI and vault MSI contributions to the snapshot RG) are resource creation operations covered by the existing `Contributor` role — **they are not blocked**.

**Important caveat to check before you run Terraform:** Your notes flag that the `storage_use_azuread = true` flag is currently **omitted** from the stack's azurerm provider block. If that's still missing, you may get a secondary block on the storage account auth path even after the RBAC permission lands. Worth verifying before you trigger the apply.

---

### Summary verdict

✅ **The single granular permission is correct** — `Role Based Access Control Administrator` + ABAC condition restricting to `Storage Blob Data Contributor` only, scoped to the three named RGs.

⚠️ **One thing to double-check before running:**
- Confirm `storage_use_azuread = true` is in the azurerm provider block on the stack side (your audit plan flagged this as a known gap).
- There was also an internal question from **Susannah Thomas** (Project Director) asking whether EE SDE (Keiran) should be looped in before the request goes to CUH — worth confirming that routing is sorted before Alexis McKenna receives the email.