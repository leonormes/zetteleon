---
title: pieces_copilot_message_export_july_31_2026_2_26pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-31-2026-2-26pm
created: 2026-07-31T13:26:55+00:00
modified: 2026-07-31T13:27:47+00:00
---
## Context: Azure Backup Tiering Failure — AKS Managed Disk Snapshots (MKUH/FitFile)

### Environment (verbatim from tool-grounded Azure CLI/Portal captures)

- **Subscription ID:** `454e1659-7f91-4963-b468-668ac7cef106`
- **Tenant ID:** `e96dd0a1-5d47-4a94-9e4a-5c1056daa82c`
- **AKS cluster:** `aks-mkuh-uks-prd-01` (resource group `rg-mkuh-uks-prd-net`)
- **AKS node resource group:** `rg-mkuh-uks-prd-aks`
- **VNet:** `vnet-mkuh-plat-uks-01` (in `rg-mkuh-uks-prd-net`)
- **Subnets confirmed in use by AKS node pools:** `snet-mkuh-uks-prd-system`, `snet-mkuh-uks-prd-workflows`
- **Backup snapshots resource group:** `aks-mkuh-uks-prd-01-backup-snapshots-rg`
- **Disk-access resource:** `aks-mkuh-uks-prd-01-backup-snapshots-rg-diskaccess`
  Full ID: `/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-snapshots-rg/providers/Microsoft.Compute/diskAccesses/aks-mkuh-uks-prd-01-backup-snapshots-rg-diskaccess`
- **Backup vault:** `aks-mkuh-uks-prd-01-backupvault` (resource group `aks-mkuh-uks-prd-01-backup-rg`)
  Vault identity: `principalId: 6cbab191-4cd3-4ee9-9aa9-acc5382b210f`, `tenantId: e96dd0a1-5d47-4a94-9e4a-5c1056daa82c`, type `SystemAssigned`
- **Backup instance (from real Teams chat with Oliver Rushton):** `aks-mkuh-uks-prd-01/aks-mkuh-uks-prd-01-backup`
- **Backup policy name:** `dailyaksbackups-v1`
- **Location:** `uksouth`
- **User:** `leon.ormes@fitfile.com` (org: Milton Keynes University Hospital / FitFile Group Limited)

### The problem

Azure Backup **Tiering** jobs for the AKS cluster's managed disk snapshots have been failing with:

```
Code: UserErrorNetworkAccessPolicyIsDenyAll
Message: Network access policy is set to deny all
RecommendedAction: Azure Backup is unable to perform the operation as network access
policy on the disk or snapshot is set to deny all. Please remove Deny All under network
access policy.
```

A real Teams chat with Oliver Rushton captured this exact failure detail:
- **Activity ID:** `71586b75-4629-43a0-beda-19cd322a2a56`
- **Operation:** Tiering
- **Status:** Failed
- **Source data store:** OperationalTierStore → **Destination:** Vault-standard
- Note: the captured start-time string read "27/07/2024, 06:19:01" — this may be a display/format artifact in the source capture (the surrounding session is dated 2026); flag but don't over-interpret.

### Remediation already attempted (grounded from real terminal/portal captures)

1. **Created the disk-access resource** — confirmed via `az disk-access show`, `provisioningState: Succeeded`.
2. **Updated snapshot network access policy to `AllowPrivate`** via a loop:
   ```bash
   for id in $(az resource list -g "$SNAP_RG" --resource-type Microsoft.Compute/snapshots --query "[].id" -o tsv); do
     az snapshot update --ids "$id" --network-access-policy AllowPrivate --disk-access "$DISK_ACCESS_ID"
   done
   ```
   Confirmed applied — sample snapshot `snapshot-49874259-b71a-4c11-8b5d-511f995c6139` shows `networkAccessPolicy: AllowPrivate`, `publicNetworkAccess: Disabled`, `diskAccessId` correctly set, `provisioningState: Succeeded`.
3. **Source disk referenced by that snapshot's tags:**
   `/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-aks/providers/Microsoft.Compute/disks/pvc-132d278d-6011-4f34-b981-9aa6b5e28864`
   — whether this disk itself has been updated to `AllowPrivate` is **not confirmed** in the retrieved captures; needs verification.
4. **Attempted to check for an existing private endpoint connection:**
   ```bash
   az network private-endpoint-connection list --id "<disk-access-resource-id>" -o table
   ```
   Result: **empty table** — no private endpoint connection exists yet against the disk-access resource. `AllowPrivate` alone is insufficient without an approved private link connection.

### Open/unresolved work

- **No private endpoint has been created yet** for the disk-access resource. This is the primary remaining blocker.
- **Group-id value for the private endpoint** is unresolved with full confidence. Two independent web searches in the prior work session both returned **`disks`** as the correct subresource/groupId for `Microsoft.Compute/diskAccesses` (not `diskAccess`), but neither search surfaced a clickable, citable Microsoft Learn URL — treat as provisional, verify against `az network private-endpoint create --help` or official docs before running.
- **Private DNS zone requirement is unresolved** — one search suggested `privatelink.blob.core.windows.net`, but this is the zone name normally associated with Blob Storage, not Managed Disks/diskAccesses specifically, and was flagged internally as an unconfirmed, possibly incorrect claim. Needs independent verification.
- **Source disk network access policy** (see point 3 above) not confirmed updated.
- **Whether the `az aks show` API-version error** (`InvalidApiVersionParameter` on `2026-03-01`, despite CLI's own supported-versions list including `2026-06-01`) was a transient CLI/extension bug or a persistent issue is unresolved — worth checking `az extension list` / `aks-preview` extension version if it recurs.
- **Tiering job re-test after private endpoint creation** has not yet been performed — this is the definitive test of whether the fix is complete:
  ```bash
  az dataprotection job list -g "$BACKUP_RG" --vault-name "$VAULT" \
    --query "[?properties.operationCategory=='Tiering'] | reverse(sort_by(@, &properties.startTime))[:3].{status:properties.status, start:properties.startTime, err:properties.errorDetails}" -o jsonc
  ```

### Task for you (the next LLM)

1. Confirm the correct `--group-id`/`--group-ids` value for a `Microsoft.Compute/diskAccesses` private endpoint against current Microsoft Learn documentation (do not trust the `disks` value above without independent verification).
2. Confirm whether a private DNS zone is required for this resource type, and if so, the correct zone name.
3. Produce the exact `az network private-endpoint create` command using: VNet `vnet-mkuh-plat-uks-01`, subnet `snet-mkuh-uks-prd-system` (or `snet-mkuh-uks-prd-workflows` — clarify which is appropriate), resource group `aks-mkuh-uks-prd-01-backup-snapshots-rg`, and the disk-access ID given above.
4. Provide verification commands to confirm the private endpoint connection reaches `Approved` state.
5. Provide the re-test command against the tiering job (given above) and specify what a successful vs. failed result looks like.

Do not invent additional resource names, subscription IDs, or error codes beyond what's listed above. If something is unconfirmed, say so explicitly rather than assuming.
