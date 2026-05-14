*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday May 14, 2026 - 9:10 AM*
---
Your LTM has solid evidence on this exact pattern — you've hit this `Microsoft.Authorization/roleAssignments/write` block multiple times across different customer deployments. Here's the definitive answer across all three issues.

---

## Minimum roles needed to fix each error

### Issue 1 — 403 on `Microsoft.Authorization/roleAssignments/write`

**Do NOT grant `User Access Administrator`** — that's the "Contributor-plus" suggestion that your own research notes flag as **overpowered**. Your Feb 2026 notes from researching the exact same error state:

> "For a private AKS deployment, the step that trips up a 'Contributor-only' SP is the role assignment creation. The minimal permission is `Microsoft.Authorization/roleAssignments/write`."

The smallest role that grants **only** `Microsoft.Authorization/roleAssignments/write` is:

**`Role Based Access Control Administrator`** (built-in, GUID `f58310d9-a9f6-439a-9e8d-f62e7b41a168`)

This is what you used on the LCA-DP deployment in Feb 2026 — your Teams message to "Davitt" requesting it verbatim asked for **"Role Based Access Control Administrator (or equivalent)"**, not full `User Access Administrator`.

**Scope it to the specific resource groups only**, not the subscription:
- `rg-ff-uks-gp-net` (AKS cluster RG)
- `pentest-1-backup-rg` (backup vault RG)
- `pentest-1-backup-snapshots-rg` (snapshot RG)

```bash
# Grant on each RG — not subscription-wide
az role assignment create \
  --assignee "48d9047f-3ac6-4d1a-9c6f-b43e9352c01f" \
  --role "Role Based Access Control Administrator" \
  --scope "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net"

az role assignment create \
  --assignee "48d9047f-3ac6-4d1a-9c6f-b43e9352c01f" \
  --role "Role Based Access Control Administrator" \
  --scope "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/pentest-1-backup-rg"

az role assignment create \
  --assignee "48d9047f-3ac6-4d1a-9c6f-b43e9352c01f" \
  --role "Role Based Access Control Administrator" \
  --scope "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/pentest-1-backup-snapshots-rg"
```

> ⚠️ **ABAC condition flag**: Your error specifically mentions an **ABAC condition** on the existing role assignment for this SP (`authorization with ABAC condition that is not fulfilled`). This means the SP already has some form of RBAC write permission but it's gated by an ABAC condition (likely restricting which principal types it can assign roles to). When requesting the grant, flag this — the ABAC condition needs to be removed or broadened to allow assignments to **Service Principals** and **Managed Identities**, not just users.

---

### Issue 2 — Private DNS zone conflict

This is an architectural fix, not a role fix. The module needs a `private_dns_zone_id` variable to accept an existing zone ID. No new role needed — `Contributor` on the resource group already covers DNS zone linking. The TFC SP just needs to **use** the existing zone rather than try to create a duplicate.

---

### Issue 3 — `Data Protection Reader` role not found

This is a **module code fix**, not a permissions issue. The role does exist in Azure but the azurerm provider is failing to resolve the name. Use the GUID directly in the module to bypass the name resolution issue:

```hcl
resource "azurerm_role_assignment" "vault_msi_data_protection_reader_on_cluster" {
  scope                            = var.kubernetes_cluster_id
  role_definition_id               = "/subscriptions/${var.subscription_id}/providers/Microsoft.Authorization/roleDefinitions/094c5728-821c-4802-bd55-40405834743f"
  principal_id                     = azurerm_data_protection_backup_vault.backup_vault.identity[0].principal_id
  skip_service_principal_aad_check = true
}
```

Use `role_definition_id` (full ARM path with GUID `094c5728-821c-4802-bd55-40405834743f`) instead of `role_definition_name`. No additional permissions required for this fix.

---

## Summary table

| Issue | Fix type | Role/action needed |
|---|---|---|
| 403 on `roleAssignments/write` | IAM grant | `Role Based Access Control Administrator` on the 3 backup RGs — **not** subscription-wide `User Access Administrator` |
| ABAC condition block | IAM change | Remove/broaden the ABAC condition on the existing assignment to allow SP/MI principal types |
| DNS zone conflict | Module code | No role needed — add `private_dns_zone_id` variable and reference existing zone |
| `Data Protection Reader` not found | Module code | No role needed — switch to `role_definition_id` with GUID `094c5728-821c-4802-bd55-40405834743f` |