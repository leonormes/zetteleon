*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday May 5, 2026 - 2:03 PM*
---
Yes — use the **same validated path**, just with a new variable set.

From your memories, you were in the **NNUHFT-SDE** subscription in [Azure Resource Manager](https://portal.azure.com/#servicemenu/Microsoft_Azure_Resources/ResourceManager/subscriptions) at **11:56 AM** today, and you had the target AKS open in [aks-ff-uks-gp-01 overview](https://portal.azure.com/#@nnuhnorwich.onmicrosoft.com/resource/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01/overview) at **12:00 PM**. In our thread, that cluster ended up with `ProtectionConfigured` and a completed test backup, so I’d treat that as the **golden path**.

I don’t see extra project files attached right now, so below is the reusable version.

## What I need from you
Send me these values and I can pre-fill it exactly:

| Variable | Example |
|---|---|
| `SUB_ID` | subscription GUID |
| `LOCATION` | `uksouth` |
| `AKS_RG` | AKS resource group |
| `AKS_NAME` | AKS cluster name |
| `BACKUP_RG` | backup resource group |
| `VAULT_NAME` | backup vault name |
| `SA_NAME` | storage account name |
| `CONTAINER_NAME` | blob container for backups |
| `SNAPSHOT_RG` | snapshot resource group |

If you already know them, you can use the template below directly.

---

## Reusable AKS backup onboarding template

### 1) Set variables
```bash
export SUB_ID=""
export LOCATION="uksouth"

export AKS_RG=""
export AKS_NAME=""

export BACKUP_RG=""
export VAULT_NAME=""
export SA_NAME=""
export CONTAINER_NAME=""

export SNAPSHOT_RG=""
export POLICY_NAME="dailyaksbackups-$(date +%Y%m%d-%H%M)"
export EXT_NAME="azure-aks-backup"
export TRUSTED_ACCESS_NAME="azbkup-trust"
```

---

### 2) Set subscription and register providers
This avoids the provider-registration problem you hit on **April 29 at 11:34 AM**.

```bash
az account set --subscription "$SUB_ID"

for NS in Microsoft.DataProtection Microsoft.KubernetesConfiguration Microsoft.ContainerService; do
  az provider register --namespace "$NS" --subscription "$SUB_ID" --wait
done
```

---

### 3) Resolve core resource IDs
```bash
AKS_ID="$(az aks show \
  --subscription "$SUB_ID" \
  --name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --query id -o tsv)"

SA_ID="$(az storage account show \
  --subscription "$SUB_ID" \
  --name "$SA_NAME" \
  --resource-group "$BACKUP_RG" \
  --query id -o tsv)"

SNAPSHOT_RG_ID="$(az group show \
  --subscription "$SUB_ID" \
  --name "$SNAPSHOT_RG" \
  --query id -o tsv)"

VAULT_ID="$(az dataprotection backup-vault show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --query id -o tsv)"

VAULT_MSI="$(az dataprotection backup-vault show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --query identity.principalId -o tsv)"
```

---

### 4) Ensure the AKS backup extension exists
This avoids the “multiple extensions of same type is not allowed” issue you hit earlier today.

```bash
if ! az k8s-extension show \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --cluster-name "$AKS_NAME" \
  --cluster-type managedClusters \
  --name "$EXT_NAME" >/dev/null 2>&1; then

  az k8s-extension create \
    --subscription "$SUB_ID" \
    --resource-group "$AKS_RG" \
    --cluster-name "$AKS_NAME" \
    --cluster-type managedClusters \
    --name "$EXT_NAME" \
    --extension-type Microsoft.DataProtection.Kubernetes \
    --scope cluster \
    --release-train stable \
    --configuration-settings \
      blobContainer="$CONTAINER_NAME" \
      storageAccount="$SA_NAME" \
      storageAccountResourceGroup="$BACKUP_RG" \
      storageAccountSubscriptionId="$SUB_ID"
fi

EXT_MSI="$(az k8s-extension show \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --cluster-name "$AKS_NAME" \
  --cluster-type managedClusters \
  --name "$EXT_NAME" \
  --query aksAssignedIdentity.principalId -o tsv)"

echo "EXT_MSI=$EXT_MSI"
```

---

### 5) Resolve AKS identities
This is the important bit for **UserAssigned** clusters: `identity.principalId` may be null by design.

```bash
AKS_UAI_PRINCIPAL_ID="$(az aks show \
  --subscription "$SUB_ID" \
  --name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --query "identity.userAssignedIdentities.*.principalId | [0]" -o tsv)"

AKS_KUBELET_OBJECT_ID="$(az aks show \
  --subscription "$SUB_ID" \
  --name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --query "identityProfile.kubeletidentity.objectId" -o tsv)"

echo "AKS_UAI_PRINCIPAL_ID=$AKS_UAI_PRINCIPAL_ID"
echo "AKS_KUBELET_OBJECT_ID=$AKS_KUBELET_OBJECT_ID"
echo "VAULT_MSI=$VAULT_MSI"
```

---

### 6) Assign RBAC
This is the same role shape that got your earlier cluster working.

```bash
# Extension MSI -> backup storage
az role assignment create \
  --assignee-object-id "$EXT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$SA_ID"

# AKS kubelet -> snapshot RG
az role assignment create \
  --assignee-object-id "$AKS_KUBELET_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"

# AKS UAI -> snapshot RG
az role assignment create \
  --assignee-object-id "$AKS_UAI_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"

# Vault MSI -> AKS
az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "$AKS_ID"

# Vault MSI -> snapshot RG
az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "$SNAPSHOT_RG_ID"
```

If any of those say the role assignment already exists, that’s fine.

---

### 7) Create trusted access binding
```bash
if ! az aks trustedaccess rolebinding show \
  --subscription "$SUB_ID" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --name "$TRUSTED_ACCESS_NAME" >/dev/null 2>&1; then

  az aks trustedaccess rolebinding create \
    --subscription "$SUB_ID" \
    --cluster-name "$AKS_NAME" \
    --resource-group "$AKS_RG" \
    --name "$TRUSTED_ACCESS_NAME" \
    --source-resource-id "$VAULT_ID" \
    --roles "Microsoft.DataProtection/backupVaults/backup-operator"
fi
```

---

### 8) Create the policy
Use a fresh policy name to avoid the “update of existing policy is not supported” error.

```bash
az dataprotection backup-policy get-default-policy-template \
  --datasource-type "AzureKubernetesService" \
  -o json > policy.json

az dataprotection backup-policy create \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --name "$POLICY_NAME" \
  --policy "@policy.json"

POLICY_ID="$(az dataprotection backup-policy show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --name "$POLICY_NAME" \
  --query id -o tsv)"

echo "POLICY_ID=$POLICY_ID"
```

---

### 9) Initialize and create the backup instance
```bash
az dataprotection backup-instance initialize-backupconfig \
  --datasource-type "AzureKubernetesService" \
  -o json > backupconfig.json

az dataprotection backup-instance initialize \
  --subscription "$SUB_ID" \
  --datasource-id "$AKS_ID" \
  --datasource-location "$LOCATION" \
  --datasource-type "AzureKubernetesService" \
  --policy-id "$POLICY_ID" \
  --backup-configuration @backupconfig.json \
  --friendly-name "${AKS_NAME}-backup" \
  --snapshot-resource-group-name "$SNAPSHOT_RG" \
  -o json > backupinstance.json

az dataprotection backup-instance validate-for-backup \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --backup-instance @backupinstance.json \
  -o jsonc

BI_NAME="$(az dataprotection backup-instance create \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --backup-instance @backupinstance.json \
  --query name -o tsv)"

echo "BI_NAME=$BI_NAME"
```

---

### 10) Wait for `ProtectionConfigured`
```bash
az dataprotection backup-instance list \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,FriendlyName:properties.friendlyName,State:properties.currentProtectionState}" \
  -o table
```

You want the new instance to move to:

```text
ProtectionConfigured
```

---

### 11) Trigger a test backup
```bash
RULE_NAME="$(az dataprotection backup-policy show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --name "$POLICY_NAME" \
  --query "properties.policyRules[?objectType=='AzureBackupRule'].name | [0]" -o tsv)"

echo "RULE_NAME=$RULE_NAME"

az dataprotection backup-instance adhoc-backup \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --name "$BI_NAME" \
  --rule-name "$RULE_NAME" \
  -o jsonc
```

---

### 12) Verify the job completed
```bash
az dataprotection job list \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}" \
  -o table
```

You want:

```text
Status = Completed
```

---

## The 4 gotchas to remember
1. **UserAssigned AKS**: `identity.principalId` may be empty. Use:
   - `identity.userAssignedIdentities.*.principalId`
   - `identityProfile.kubeletidentity.objectId`

2. **Extension already exists**: don’t try to create a second one.

3. **Policy names are immutable** for practical purposes:
   - if `dailyaksbackups` already exists, create `dailyaksbackups-v2` or timestamp it.

4. **Old failed backup instances**:
   - if the cluster already has a stale `ProtectionError` instance, leave it alone until the new one is healthy,
   - then delete the stale one.

---

## Fastest way to proceed
If you send me just this filled block:

```bash
export SUB_ID=""
export LOCATION="uksouth"
export AKS_RG=""
export AKS_NAME=""
export BACKUP_RG=""
export VAULT_NAME=""
export SA_NAME=""
export CONTAINER_NAME=""
export SNAPSHOT_RG=""
```

I’ll turn it into the **exact ready-to-run command sequence** for that cluster.