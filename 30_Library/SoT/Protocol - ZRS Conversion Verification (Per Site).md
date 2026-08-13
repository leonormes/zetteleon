---
created: 2026-07-13T21:26:14+00:00
modified: 2026-08-13T10:53:39+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-13-2026-4-11pm-1
tags: [1, 2]
title: Protocol - ZRS Conversion Verification (Per Site)
type: note
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Monday Jul 13, 2026 - 4:11 PM_
---

## ZRS Conversion Verification Checklist—per Site

Three commands cover everything: confirm the storage account's current SKU, check migration progress, and confirm the backup extension/vault are healthy. Run these from a machine with `az login`'d access to each site's tenant/subscription.

### CUH—`aks-ff-uks-gp-01` Cluster

Resource group: `aks-ff-uks-gp-01-backup-rg` (storage) / `rg-ff-uks-gp-net` (cluster)—confirmed from your Azure Resource Manager view ([Home - Microsoft Azure](https://portal.azure.com/#home)) and Terraform run output ([HCP Terraform run](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1/runs/run-XrLLk2g6pdUvx6Cd)). Storage account: `aksffuksgp01cuhbackup`.

```bash
# 1. Current SKU — is it still LRS or has it converted to ZRS?
az storage account show \
  --name aksffuksgp01cuhbackup \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --query "{name: name, sku:sku.name, provisioningState:provisioningState}" \
  -o json

# 2. Migration job status (if a migration was ever started)
az storage account migration show \
  --account-name aksffuksgp01cuhbackup \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --name default

# 3. Confirm the backup extension itself is healthy (separate blocker — Helm install)
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  -g rg-ff-uks-gp-net \
  --query "{state:provisioningState, statuses: statuses}" -o json
```

At the last check on `2026-07-13T08:43:44` your terminal output showed the account was still `"sku": "Standard_LRS"`, `"provisioningState": "Succeeded"`, and a migration had just been kicked off (`migrationStatus": "SubmittedForConversion"`)—so command 2 is the one to re-run to see if that's progressed to `Succeeded`.

### NNUH

Storage account referenced in your remediation runbook: `aksffuksgp01backupsa` (from the [Ensure All Backups Are ZRS — Current Status](obsidian://) note dated `2026-07-07`; exact resource group for this account wasn't captured in memory—check with `az storage account show` without `-g` first if unsure, or use the same `aks-ff-uks-gp-01-backup-rg` pattern as CUH).

```bash
# 1. Current SKU
az storage account show \
  --name aksffuksgp01backupsa \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --query "{name: name, sku:sku.name, provisioningState:provisioningState}" \
  -o json

# 2. Migration job status
az storage account migration show \
  --account-name aksffuksgp01backupsa \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --name default
```

Per your `2026-07-07` note: "NNUH ZRS migration was kicked off around Jul 1 … This is asynchronous and can take up to 72 hours—worth re-checking with `az storage account migration show` if you haven't confirmed completion yet." That window has long passed, so command 2 should now return a definitive `Succeeded` or `Failed`.

### MKUH

Storage account: `aksmkuhuksprd01bkp01`. Resource group / vault confirmed from an earlier backup-instance ID captured in memory: `aks-mkuh-uks-prd-01-backup-rg`, vault `aks-mkuh-uks-prd-01-backupvault`.

```bash
# 1. Current SKU
az storage account show \
  --name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --query "{name: name, sku:sku.name, provisioningState:provisioningState}" \
  -o json

# 2. Migration job status
az storage account migration show \
  --account-name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --name default

# 3. Check the public-network-access flag Ollie flagged as still exposed (26 Jun)
az storage account show \
  --name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --query "{publicNetworkAccess: publicNetworkAccess, allowSharedKeyAccess: allowSharedKeyAccess}" \
  -o json
```

As of `2026-07-07` your own note said: "The actual LRS→ZRS storage-account conversion command for MKUH's `aksmkuhuksprd01bkp01` account still needed to be run"—so if command 1 still shows `Standard_LRS` and 2 returns nothing (no migration in progress), you haven't actually kicked this one off yet. You'll need to run the conversion first:

```bash
az storage account migration start \
  --account-name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --sku Standard_ZRS \
  --name default \
  --no-wait
```

### Cross-cutting: Backup-instance / Vault Health (Any sIte)

If you want to confirm the Azure Backup vault itself is actually protecting the cluster (not just the storage tier), run this too—it's the read-only discovery pattern from your `aks-backup-audit.sh` script (`SPEC-FTFL-525`, purpose: "READ-ONLY discovery for AKS backup posture"):

```bash
az dataprotection backup-vault show \
  -g <resource-group> \
  --vault-name <vault-name>

az dataprotection backup-instance list \
  --resource-group <resource-group> \
  --vault-name <vault-name> \
  --query "[].{Name: name, Cluster: properties.friendlyName, State: properties.currentProtectionState}" \
  -o table
```

### One Caveat

I could not find NNUH's exact resource-group name explicitly stated anywhere in memory—only the storage account name (`aksffuksgp01backupsa`) from your own runbook notes. I've assumed the same `aks-ff-uks-gp-01-backup-rg` pattern CUH uses since the naming convention matches, but confirm this with `az storage account list --query "[].{name:name, resourceGroup:resourceGroup}" -o table` before running the NNUH commands if the resource-group flag fails.

Once you've run these, the definitive pass/fail signal for FTFL-525 is command 1 returning `"sku": "Standard_ZRS"` for all three storage accounts.
