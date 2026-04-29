---
created: 2026-04-29T10:20:51+00:00
modified: 2026-04-29T10:23:09+00:00
title: Azure Backup for AKS — Full CLI Command Sequence
---

Based on your current work on [FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596) and the container you just confirmed at `stffuksgp1backup/aks-backups`, here's the full command sequence end-to-end.

---

## 0. Set Variables

```bash
# Cluster
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_RG="<your-aks-resource-group>"
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Backup infra
VAULT_NAME="aksbackupvault"
VAULT_RG="<your-backup-rg>"
STORAGE_ACCOUNT="stffuksgp1backup"
STORAGE_RG="<your-storage-rg>"
BLOB_CONTAINER="aks-backups"
LOCATION="uksouth"

# Policy
POLICY_NAME="dailyaksbackups"
```

---

## 1. Register the Resource Provider (if not already)

```bash
az provider register --namespace Microsoft.DataProtection
az provider show --namespace Microsoft.DataProtection --query "registrationState" -o tsv
```

You confirmed this is already `Registered` on prod yesterday (~10:16 AM). Check the target subscription too.

---

## 2. Install the AKS Backup Extension

```bash
az k8s-extension create \
  --name azure-aks-backup \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --release-train stable \
  --configuration-settings \
    blobContainer="$BLOB_CONTAINER" \
    storageAccount="$STORAGE_ACCOUNT" \
    storageAccountResourceGroup="$STORAGE_RG" \
    storageAccountSubscriptionId="$SUBSCRIPTION_ID"
```

Verify it's healthy:

```bash
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "{name:name, provisioningState:provisioningState, isSystemExtension:isSystemExtension}" \
  -o table
```

---

## 3. Create a Backup Vault (if it Doesn't Already exist)

```bash
az dataprotection backup-vault create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --location "$LOCATION" \
  --type SystemAssigned \
  --storage-setting "[{type:LocallyRedundant,datastore-type:VaultStore}]"
```

Get the Vault's Managed Identity principal ID (you'll need this for role assignments):

```bash
VAULT_PRINCIPAL_ID=$(az dataprotection backup-vault show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --query "identity.principalId" -o tsv)
echo "Vault MSI: $VAULT_PRINCIPAL_ID"
```

---

## 4. Assign Required RBAC Roles

The vault's managed identity needs three roles:

### a) Reader on the AKS Cluster

```bash
AKS_ID=$(az aks show --name "$AKS_CLUSTER_NAME" --resource-group "$AKS_RG" --query id -o tsv)

az role assignment create \
  --assignee-object-id "$VAULT_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "$AKS_ID"
```

### b) Reader on the Snapshot Resource Group (if Using Disk snapshots)

```bash
# If you have a dedicated snapshot RG:
SNAPSHOT_RG="<your-snapshot-rg>"
SNAPSHOT_RG_ID=$(az group show --name "$SNAPSHOT_RG" --query id -o tsv)

az role assignment create \
  --assignee-object-id "$VAULT_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"
```

### c) Storage Blob Data Contributor on the Storage account

```bash
STORAGE_ID=$(az storage account show --name "$STORAGE_ACCOUNT" --resource-group "$STORAGE_RG" --query id -o tsv)

az role assignment create \
  --assignee-object-id "$VAULT_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ID"
```

### d) The AKS Cluster's Extension Identity also Needs Roles

```bash
# Get the extension's identity
EXTENSION_PRINCIPAL_ID=$(az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "aksAssignedIdentity.principalId" -o tsv)

# Storage Blob Data Contributor on the storage account
az role assignment create \
  --assignee-object-id "$EXTENSION_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ID"
```

---

## 5. Create a Backup Policy

```bash
# First, get the default policy template
az dataprotection backup-policy get-default-policy-template \
  --datasource-type AzureKubernetesService \
  -o json > backup-policy.json
```

Edit `backup-policy.json` to set your desired schedule and retention (e.g., daily at 21:00 UTC, 30-day retention), then:

```bash
az dataprotection backup-policy create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --name "$POLICY_NAME" \
  --policy backup-policy.json
```

Or list existing policies (as you did yesterday on prod):

```bash
az dataprotection backup-policy list \
  --resource-group "$VAULT_RG" \
  --vault-name "$VAULT_NAME" \
  -o table
```

---

## 6. Configure the Backup Instance (Enable Protection)

```bash
# Initialize the backup config body
az dataprotection backup-instance initialize-backupconfig \
  --datasource-type AzureKubernetesService \
  --include-namespaces "barts" "ff-a" "ff-b" "ff-c" "spicedb" "thehyve" \
  --snapshot-volumes true \
  -o json > backup-config.json

# Initialize the backup instance request
az dataprotection backup-instance initialize \
  --datasource-id "$AKS_ID" \
  --datasource-location "$LOCATION" \
  --datasource-type AzureKubernetesService \
  --policy-id $(az dataprotection backup-policy show \
      --vault-name "$VAULT_NAME" \
      --resource-group "$VAULT_RG" \
      --name "$POLICY_NAME" \
      --query id -o tsv) \
  --backup-configuration backup-config.json \
  --friendly-name "${AKS_CLUSTER_NAME}-daily" \
  --snapshot-resource-group-name "$SNAPSHOT_RG" \
  -o json > backup-instance.json

# Create the backup instance (enable protection)
az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --backup-instance backup-instance.json
```

---

## 7. Trigger an On-Demand Backup (Optional—for testing)

```bash
BACKUP_INSTANCE_NAME=$(az dataprotection backup-instance list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --query "[0].name" -o tsv)

az dataprotection backup-instance adhoc-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --name "$BACKUP_INSTANCE_NAME" \
  --rule-name "BackupDaily"
```

---

## 8. Verify—Status & Jobs

```bash
# List backup instances
az dataprotection backup-instance list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  -o table

# Check recent backup jobs
az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --query "[].{name:properties.backupInstanceFriendlyName, status:properties.status, startTime:properties.startTime}" \
  -o table

# Verify the extension health
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "provisioningState" -o tsv
```

---

## Quick Reference—Command Flow

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `az provider register` | Enable `Microsoft.DataProtection` |
| 2 | `az k8s-extension create` | Install backup extension on AKS |
| 3 | `az dataprotection backup-vault create` | Create the vault |
| 4 | `az role assignment create` (×4) | RBAC for vault MSI + extension MSI |
| 5 | `az dataprotection backup-policy create` | Define schedule + retention |
| 6 | `az dataprotection backup-instance create` | Wire cluster → vault → storage |
| 7 | `az dataprotection backup-instance adhoc-backup` | Test it |
| 8 | `az dataprotection job list` | Confirm it ran |

Since you've already confirmed the `Microsoft.DataProtection` provider is registered and the `aks-backups` container exists on `stffuksgp1backup`, you can likely jump straight to Step 2 (install the extension) and then work through the role assignments. The existing prod infrastructure you audited yesterday (`aksbackupvault` / `prod-1-backup-v2-rg`) can serve as a reference for the policy JSON structure—pull it with `az dataprotection backup-policy show` and adapt.

The open questions from FTFL-596 (frequency, retention, namespace scope) will determine what goes into `backup-policy.json` and `backup-config.json`.
