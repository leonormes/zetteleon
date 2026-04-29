*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 11:36 AM*
---
# You're Blocked by Insufficient RBAC on the Testing Subscription

This is the same authorization wall you've been hitting all morning — since around 10:01 AM. Looking at the pattern across your session, your account (`leon.ormes@fitfile.com` / `053a0abe-0b3e-40a3-85c8-83f2af887382`) lacks write-level permissions on subscription `7bbc8ae5-...` (**Testing**) for essentially every action you've attempted:

| ~Time | Action Attempted | Permission Missing |
|---|---|---|
| 10:01 AM | `Microsoft.Storage/storageAccounts/write` | Storage Account create |
| 10:07 AM | `Microsoft.Network/virtualNetworks/subnets/write` | Subnet create |
| 10:08 AM | `az role assignment create` | Role assignment (also failed) |
| 11:33 AM | `Microsoft.KubernetesConfiguration/register/action` | Provider registration |
| 11:33 AM | `Microsoft.DataProtection/register/action` | Provider registration |

**Registering a resource provider requires at minimum `*/register/action`**, which is included in the **Contributor** role at subscription scope. You clearly don't have Contributor (or Owner) on this Testing subscription — and you can't self-elevate because `az role assignment create` also fails.

## What Needs to Happen

**This requires someone with Owner or User Access Administrator on the Testing subscription** to grant you permissions. You need to escalate to whoever controls IAM on that subscription — likely **Ollie Rushton** given your shared security/infra ownership, or whoever provisioned the Testing sub originally.

### What to ask them for (minimum viable set for this AKS Backup work):

```bash
# Option A: Contributor at subscription scope (broad, but lets you finish the whole runbook)
az role assignment create \
  --assignee "leon.ormes@fitfile.com" \
  --role "Contributor" \
  --scope "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"

# Option B: Scoped roles (least-privilege, but more assignments)
# 1. Provider registration (subscription-level)
az role assignment create \
  --assignee "leon.ormes@fitfile.com" \
  --role "Contributor" \
  --scope "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
  # Note: there's no narrower built-in role for just provider registration —
  # it requires subscription-scope Contributor or a custom role with */register/action
```

Realistically, given you need storage account creation, subnet creation, role assignments for MSIs, *and* provider registration, **Contributor at subscription scope** is the pragmatic ask for a Testing environment. If policy demands least-privilege, a custom role with the following actions would cover it:

```json
{
  "actions": [
    "*/register/action",
    "Microsoft.Storage/storageAccounts/*",
    "Microsoft.Network/virtualNetworks/subnets/*",
    "Microsoft.Authorization/roleAssignments/write",
    "Microsoft.KubernetesConfiguration/*",
    "Microsoft.DataProtection/*"
  ]
}
```

## In the Meantime

You can't proceed with the AKS Backup extension install until the providers are registered, and you can't register them yourself. **Nothing in the remaining runbook steps will work** until this IAM gap is closed — every subsequent step (extension create, MSI role grants, vault configuration) requires equal or higher privilege.

Send the ask now, and while you wait, you could document exactly which role assignments the backup extension's MSI will need (Storage Blob Data Contributor on `stffuksgp1backup`, Reader on the AKS cluster, Contributor on the snapshot RG) so you can chain them immediately once you're unblocked.