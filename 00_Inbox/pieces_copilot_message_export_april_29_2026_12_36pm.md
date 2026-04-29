*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 12:36 PM*
---
Based on your **11:51 AM** extension success, **12:03 PM** vault creation, and **12:26 PM** policy creation, this is the single pasteable sequence to avoid the **12:31 PM** `NO_PARAM / Null DatasourceSet object` error:

```bash
set -euo pipefail

SUB_ID="${SUB_ID:-7bbc8ae5-1710-48ab-ab83-59b52bd0de1a}"
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_RG="rg-ff-uks-gp-net"
VAULT_NAME="aksbackupvault"
VAULT_RG="pentest-1-backup-rg"
POLICY_NAME="dailyaksbackups"
SNAPSHOT_RG="pentest-1-backup-snapshots-rg"
LOCATION="uksouth"

az account set --subscription "$SUB_ID"

az group create \
  --name "$SNAPSHOT_RG" \
  --location "$LOCATION" \
  --subscription "$SUB_ID" \
  >/dev/null

AKS_CLUSTER_ID="$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --subscription "$SUB_ID" \
  --query id -o tsv)"

POLICY_ID="$(az dataprotection backup-policy show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$POLICY_NAME" \
  --query id -o tsv)"

az dataprotection backup-instance initialize-backupconfig \
  --datasource-type AzureKubernetesService \
  --include-namespaces barts ff-a ff-b ff-c spicedb thehyve thehyve-cuh thehyve-mkuh \
  --snapshot-volumes true \
  -o json > backup-config.json

az dataprotection backup-instance initialize \
  --datasource-id "$AKS_CLUSTER_ID" \
  --datasource-location "$LOCATION" \
  --datasource-type AzureKubernetesService \
  --policy-id "$POLICY_ID" \
  --backup-configuration @backup-config.json \
  --friendly-name "${AKS_CLUSTER_NAME}-backup" \
  --snapshot-resource-group-name "$SNAPSHOT_RG" \
  -o json > backup-instance.json

az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json

az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```