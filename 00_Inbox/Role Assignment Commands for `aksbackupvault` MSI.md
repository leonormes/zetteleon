---
created: 2026-04-29T11:22:52+00:00
modified: 2026-04-29T11:31:01+00:00
title: Role Assignment Commands for `aksbackupvault` MSI
---

Here are the `az` CLI commands using the MSI principal ID and resource IDs from your session. Adjust the AKS cluster resource group if it differs in the pentest environment.

## 1. Variables (set These first)

```bash
# MSI from the vault creation output
VAULT_MSI="18bd104a-e5fb-4c8c-8abc-55e739ce600f"

# Subscription
SUB_ID="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"

# AKS cluster details (adjust RG if pentest AKS is in a different RG)
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_CLUSTER_RG="rg-ff-uks-gp-net"   # <-- confirm this for pentest

# Storage account for backups
STORAGE_ACCOUNT_ID="/subscriptions/${SUB_ID}/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Storage/storageAccounts/stffuksgp1backup"

# Snapshot resource group (AKS backup needs a dedicated RG for snapshots)
SNAPSHOT_RG="pentest-1-backup-snapshots-rg"
```

## 2. Create the Snapshot Resource Group (if it Doesn't exist)

```bash
az group create \
  --name "$SNAPSHOT_RG" \
  --location uksouth \
  --subscription "$SUB_ID" \
  --tags Environment=pentest Department=SDE ManagedBy=FITFILE
```

## 3. Grant Reader on AKS Cluster

```bash
AKS_CLUSTER_ID=$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_CLUSTER_RG" \
  --subscription "$SUB_ID" \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "$AKS_CLUSTER_ID"
```

## 4. Grant Contributor on the Snapshot Resource Group

```bash
SNAPSHOT_RG_ID="/subscriptions/${SUB_ID}/resourceGroups/${SNAPSHOT_RG}"

az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"
```

## 5. Grant Storage Blob Data Contributor on the Backup Storage account

```bash
az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ACCOUNT_ID"
```

## 6. Create the Backup Policy (daily, 14-day Retention, Mirroring prod)

```bash
az dataprotection backup-policy create \
  --vault-name "aksbackupvault" \
  --resource-group "pentest-1-backup-rg" \
  --subscription "$SUB_ID" \
  --name "dailyaksbackups" \
  --policy '{
    "datasourceTypes": ["Microsoft.ContainerService/managedClusters"],
    "objectType": "BackupPolicy",
    "policyRules": [
      {
        "name": "BackupDaily",
        "objectType": "AzureBackupRule",
        "backupParameters": {
          "objectType": "AzureBackupParams",
          "backupType": "Incremental"
        },
        "trigger": {
          "objectType": "ScheduleBasedTriggerContext",
          "schedule": {
            "repeatingTimeIntervals": ["R/2026-04-29T02:00:00+00:00/P1D"]
          },
          "taggingCriteria": [
            {
              "isDefault": true,
              "tagInfo": { "tagName": "Default" },
              "taggingPriority": 99
            }
          ]
        },
        "dataStore": {
          "objectType": "DataStoreInfoBase",
          "dataStoreType": "OperationalStore"
        }
      },
      {
        "name": "Default",
        "objectType": "AzureRetentionRule",
        "isDefault": true,
        "lifecycles": [
          {
            "deleteAfter": {
              "objectType": "AbsoluteDeleteOption",
              "duration": "P14D"
            },
            "sourceDataStore": {
              "objectType": "DataStoreInfoBase",
              "dataStoreType": "OperationalStore"
            }
          }
        ]
      }
    ]
  }'
```

> Note: The policy uses `OperationalStore` (snapshot-based) to match your prod pattern, not the `VaultStore` that the vault itself advertises.

## 7. Create the Backup Instance (after Policy is created)

```bash
# First, install the AKS backup extension if not already present
az aks update \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_CLUSTER_RG" \
  --subscription "$SUB_ID" \
  --enable-disk-driver

# Then configure protection — adjust namespace list to match your pentest namespaces
az dataprotection backup-instance create \
  --vault-name "aksbackupvault" \
  --resource-group "pentest-1-backup-rg" \
  --subscription "$SUB_ID" \
  --backup-instance '{
    "objectType": "BackupInstanceResource",
    "properties": {
      "dataSourceInfo": {
        "resourceID": "'"$AKS_CLUSTER_ID"'",
        "resourceType": "Microsoft.ContainerService/managedClusters",
        "resourceName": "'"$AKS_CLUSTER_NAME"'",
        "resourceLocation": "uksouth",
        "objectType": "Datasource",
        "datasourceType": "Microsoft.ContainerService/managedClusters"
      },
      "policyInfo": {
        "policyId": "/subscriptions/'"$SUB_ID"'/resourceGroups/pentest-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupPolicies/dailyaksbackups"
      },
      "objectType": "BackupInstance",
      "friendlyName": "aks-ff-uks-gp-1-backup"
    }
  }'
```

## Things to Confirm before Running

| Item                | Action                                                                                                                                                                                                                |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AKS cluster RG      | Verify `AKS_CLUSTER_RG`—I used `rg-ff-uks-gp-aks` as a placeholder                                                                                                                                                    |
| AKS cluster name    | Confirm `aks-ff-uks-gp-1` is the correct pentest cluster (not the prod one)                                                                                                                                           |
| Namespace selection | Prod backs up `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`—the backup instance JSON above doesn't filter namespaces (backs up everything). If you need namespace filtering, you'll add it to the backup instance config |
| Snapshot RG name    | `pentest-1-backup-snapshots-rg` is my suggestion—adjust to match your naming convention                                                                                                                               |
| Backup extension    | The AKS backup extension (`microsoft.dataprotection`) should already be installed on the cluster from the `~11:51 AM` step—verify with `az k8s-extension list`                                                        |

Want me to also draft the validation commands to confirm each role assignment took effect?
