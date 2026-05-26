---
created: Invalid date
modified: 2026-05-26T11:43:36+00:00
pieces_ids: ["2cf9d16d-4b94-41ab-ba2c-6016852742b2", "9021743f-dd37-4f74-bd57-a205dabcc2c1", "9957a1d5-1092-4b6a-bfc7-8804badb5d44", "9c097ed5-8991-49e7-8a79-5569010904fb"]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-19-pieces-azure-backup
---

## Asset 1 (Pieces: 9021743f-dd37-4f74-bd57-a205dabcc2c1)

These commands are going in circles. Look up across my memoryes and offer a solution to deploy the extension. az k8s-extension create \
  --resource-group rg-ff-uks-gp-net \
  --cluster-name aks-ff-uks-gp-01 \
  --cluster-type managedClusters \
  --name azbkuextension \
  --extension-type microsoft.dataprotection.kubernetes \
  --configuration-settings blobContainer=aksbackups \
  --config-protected-settings storageAccount=aksffuksgp01cuhbackup,storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg

## Asset 2 (Pieces: 2cf9d16d-4b94-41ab-ba2c-6016852742b2)

The user is having trouble deploying a Kubernetes extension for Azure Backup. They're running in circles with the `az k8s-extension create` command. Let me search their memory for context about this deployment issue, previous attempts, and any solutions they may have encountered.

Let me search memory for relevant context about this Azure Kubernetes extension deployment issue.

## Asset 3 (Pieces: 9957a1d5-1092-4b6a-bfc7-8804badb5d44)

The review feedback says I need to:

1. Paginate both search_memory calls using their nextCursor values
2. Run 2-3 additional search_memory queries with variants

Let me do all of these in parallel where possible. I'll paginate both cursors and run the additional searches simultaneously.

Cursor 1 (azbkuextension): `eyJxIjoiaDphemJrdWV4dGVuc2lvbiIsIm8iOjUwfQ==`

Cursor 2 (az k8s-extension create): `eyJxIjoiaDpheiBrOHMtZXh0ZW5zaW9uIGNyZWF0ZSIsIm8iOjUwfQ==`

I'll also run a few more targeted searches in parallel—looking for results around Kubernetes backup functionality, AKS backup extensions with storage accounts, and the Microsoft data protection Kubernetes provider specifically.

## Asset 4 (Pieces: 9c097ed5-8991-49e7-8a79-5569010904fb)

The circuit breaker has fired on two of the remaining chains (`azbkuextension` and `az k8s-extension create`), and both `AKS backup extension storageAccount` and `microsoft.dataprotection.kubernetes` have returned `sufficient`. The corpus is exhausted. I have more than enough evidence to synthesize a precise solution. Here it is:

---

## Why the `az k8s-extension create` Command is Going in circles—and how to Fix it

### Root Cause Diagnosis

Your command has three compounding problems that your memory shows have tripped you up before (Apr 29 → May 5 → May 7 → today):

#### Problem 1: Missing `--scope cluster` and `--release-train stable`

Your current command:

```bash
az k8s-extension create \
  --resource-group rg-ff-uks-gp-net \
  --cluster-name aks-ff-uks-gp-01 \
  --cluster-type managedClusters \
  --name azbkuextension \
  --extension-type microsoft.dataprotection.kubernetes \
  --configuration-settings blobContainer=aksbackups \
  --config-protected-settings storageAccount=aksffuksgp01cuhbackup,...
```

The canonical working form from your memory (May 5, successfully deployed on `aks-ff-uks-gp-01`) is:

```bash
az k8s-extension create \
  --name "$EXT_NAME" \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --release-train stable \
  --configuration-settings \
    blobContainer="$CONTAINER_NAME" \
    storageAccount="$SA_NAME" \
    storageAccountResourceGroup="$BACKUP_RG" \
    storageAccountSubscriptionId="$SUB_ID"
```

You are missing `--scope cluster`, `--release-train stable`, and critically `storageAccountSubscriptionId`.

#### Problem 2: Wrong Storage account name

Your command passes `storageAccount=aksffuksgp01cuhbackup`—but your memory records show the actual storage account for `aks-ff-uks-gp-01` is `aksffuksgp01backupsa` (confirmed from portal screenshots on May 5 at [aksffuksgp01backupsa overview](https://portal.azure.com/#@nnuhnorwich.onmicrosoft.com/resource/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01backupsa/overview)).

- `aksffuksgp01cuhbackup`—wrong (this looks like a CUH-specific naming variant, not the GP-net cluster's SA)
- `aksffuksgp01backupsa`—correct (what's deployed in `aks-ff-uks-gp-01-backup-rg`)

#### Problem 3: Wrong Backup RG in `--config-protected-settings`

Your command uses `storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg`. But `--config-protected-settings` is the wrong parameter for these values—storage account settings go in `--configuration-settings` as flat key=value pairs, not as protected settings. `--config-protected-settings` is for secrets that need to be encrypted (like keys), and the CLI syntax for it is also different.

Also: your memory shows a previous run that got the warning `useAAD flag is not specified. Setting it to 'true'. Please provide extension MSI Storage Blob Data Contributor role on the storage account.`—this is expected and fine, but it confirms the storage account name must resolve correctly.

---

### The Corrected Command for `aks-ff-uks-gp-01`

```bash
# Set variables first
export SUB_ID="4ae8fd93-d084-481f-ba6e-370b7d4d8d0d"
export AKS_NAME="aks-ff-uks-gp-01"
export AKS_RG="rg-ff-uks-gp-net"
export BACKUP_RG="aks-ff-uks-gp-01-backup-rg"
export SA_NAME="aksffuksgp01backupsa"
export CONTAINER_NAME="aksbackups"
export EXT_NAME="azbkuextension"

az k8s-extension create \
  --subscription "$SUB_ID" \
  --name "$EXT_NAME" \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --release-train stable \
  --configuration-settings \
    blobContainer="$CONTAINER_NAME" \
    storageAccount="$SA_NAME" \
    storageAccountResourceGroup="$BACKUP_RG" \
    storageAccountSubscriptionId="$SUB_ID"
```

---

### After the Extension deploys—capture the EXT_MSI Immediately

Your memory shows you need to grab the extension's MSI principal ID before the next RBAC step:

```bash
export EXT_MSI="$(az k8s-extension show \
  --subscription "$SUB_ID" \
  --name "$EXT_NAME" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --cluster-type managedClusters \
  --query "aksAssignedIdentity.principalId" -o tsv)"

echo "EXT_MSI=$EXT_MSI"
```

Then grant `EXT_MSI` the Storage Blob Data Contributor role on the storage account (this is what the `useAAD` warning is telling you to do):

```bash
export SA_ID="$(az storage account show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "$SA_NAME" \
  --query id -o tsv)"

az role assignment create \
  --subscription "$SUB_ID" \
  --assignee-object-id "$EXT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$SA_ID"
```

---

### If the Extension Already Exists (idempotent re-run)

If `azbkuextension` already partially exists and the create errors with a conflict, use `update` instead:

```bash
az k8s-extension update \
  --name "$EXT_NAME" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --cluster-type managedClusters \
  --configuration-settings \
    blobContainer="$CONTAINER_NAME" \
    storageAccount="$SA_NAME" \
    storageAccountResourceGroup="$BACKUP_RG" \
    storageAccountSubscriptionId="$SUB_ID"
```

Your memory shows you hit exactly this pattern on May 5 (`az k8s-extension update` on `aks-ff-uks-gp-01`) when the prior create had partially completed.

---

### Summary of Fixes

| Issue | Your command | Fix |
|---|---|---|
| Missing flags | No `--scope cluster`, no `--release-train stable` | Add both |
| Wrong storage account | `aksffuksgp01cuhbackup` | Use `aksffuksgp01backupsa` |
| Wrong param for SA config | `--config-protected-settings` | Move all SA settings to `--configuration-settings` |
| Missing `storageAccountSubscriptionId` | Not present | Add `storageAccountSubscriptionId="$SUB_ID"` |
