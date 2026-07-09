---
created: 2026-07-09T11:36:32+00:00
modified: 2026-07-09T11:36:43+00:00
title: pieces_copilot_message_export_july_9_2026_12_36pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 9, 2026 - 12:36 PM_
---

## Checking the CUH Backup Role-assignment Change in Azure Cloud Shell

### What Was Requested & what Came back

On 6 Jul 12:47 (BST) you emailed Alexis McKenna (Cambridge University Hospitals NHS Foundation Trust) asking her to run an `az role assignment create` command granting Storage Blob Data Contributor to the `azure-aks-backup` extension's managed identity, scoped to the CUH backup storage account—you were blocked because you only hold `Contributor` on the subscription. The thread is titled "Role assignment needed - AKS backup extension on aks-ff-uks-gp-01".

Worth flagging precisely: the confirmation that the command had actually been run came from Ryan Quinn (Telefónica Tech), replying on that same Alexis thread on 8 Jul, 14:29: _"I ran the command just now and didn't get any errors. Could you please verify if the ID got added? I think this is it?"_—with the screenshot showing:

- `Storage Blob Data Contributor (2)` on `aksbackupvault`—assignment id `8801f415-8e3f-4e38-93a1-d88c74fc70f3`
- Managed identity `ext-21a39791cf3f1594075f3e9868e7b273-aks-ff-uks-gp-01`—object id `d5d329ef-8081-409e-a170-bb0710f50366`

So the "applied" report is on the record from Ryan (cc'ing/replying-to Alexis), not a direct confirmation message from Alexis herself—worth keeping that distinction in mind since he's explicitly asking you to double-check.

The relevant identifiers, all pulled verbatim from your emails:

| Item | Value |
|---|---|
| Subscription | `709f3d57-b6d7-48c6-8252-6b1c1174a541` |
| AKS cluster | `aks-ff-uks-gp-01` |
| AKS resource group | `rg-ff-uks-gp-net` |
| Backup storage account | `aksffuksgp01cuhbackup` |
| Backup resource group | `aks-ff-uks-gp-01-backup-rg` |
| Role | `Storage Blob Data Contributor` |
| Managed identity (assignee) | `d5d329ef-8081-409e-a170-bb0710f50366` |

### Cloud Shell (`az`) Commands to Verify it

```bash
# 1. Make sure you're pointed at the right subscription
az account set --subscription "709f3d57-b6d7-48c6-8252-6b1c1174a541"

# 2. Re-derive the extension's managed identity principal ID (confirms the ID Ryan quoted is correct)
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --query aksAssignedIdentity.principalId -o tsv

# 3. List role assignments on the exact storage account scope, filtered to that identity
az role assignment list \
  --assignee d5d329ef-8081-409e-a170-bb0710f50366 \
  --scope /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01cuhbackup \
  --output table

# 4. Alternative check: list ALL role assignments on that storage account and grep for the role name
az role assignment list \
  --scope /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01cuhbackup \
  --query "[?roleDefinitionName=='Storage Blob Data Contributor']" \
  --output table

# 5. Once the role assignment is confirmed present, re-check the extension's install/provisioning state
# (this was previously failing with "Helm installation failed: context deadline exceeded")
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --query "{name:name, provisioningState:provisioningState, installState:installState}" \
  --output table
```

Command 3 is the direct proof-of-change check—if it returns a row with `roleDefinitionName: Storage Blob Data Contributor` against that scope, the change Alexis's team applied is confirmed live. Command 5 tells you whether that role fix actually unblocked the Helm install, which was your real end goal.

### Adjacent Context Worth Knowing

This sits under Jira ticket FTFL-525 ("Ensure All Backups Are ZRS"), covering three NHS sites—MKUH, NNUH, and CUH—where CUH is the one that's been blocked on this exact role-assignment step since 6 Jul. Per your own notes:

- NNUH—ZRS migration was kicked off ~1 Jul; async, can take up to 72h; check with `az storage account migration show`.
- MKUH—the tiering failure (`UserErrorMissingVaultMSIPermissionsOnBackupStorageLocation`) was already diagnosed and fixed via RBAC; the actual LRS→ZRS storage-account conversion for `aksmkuhuksprd01bkp01` still needed confirmation as of your last note.

Once you've confirmed the CUH role assignment via command 3/5 above, the next step per your own runbook is to re-run `az k8s-extension create` for `azure-aks-backup` on `aks-ff-uks-gp-01` to verify the Helm install completes, then kick off the CUH storage account's LRS→ZRS conversion the same way you did for NNUH—happy to draft that command set too if you want it now.
