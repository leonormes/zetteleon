*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 13, 2026 - 9:36 AM*
---
I have a comprehensive picture from memory. Here is the complete teardown script, grounded in your actual resource names from the **Testing** subscription (`7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`) as recorded in your notes from 29 April 2026.

---

## Teardown script: Testing subscription backup resources

Your sandbox resources were split across two resource groups:
- **`pentest-1-backup-rg`** — vault, policy, instance, storage account, private endpoint
- **`pentest-1-backup-snapshots-rg`** — volume snapshots

And the **trusted access binding + AKS extension** live on the cluster (`aks-ff-uks-gp-1`) in `rg-ff-uks-gp-net`.

Run this in **order** — the dependencies mean you must remove the backup instance before the vault, and the extension before the storage account locks allow it to be deleted cleanly.

```bash
set -euo pipefail

export SUB_ID="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export BACKUP_RG="pentest-1-backup-rg"
export SNAPSHOT_RG="pentest-1-backup-snapshots-rg"
export VAULT_NAME="aksbackupvault"
export SA_NAME="stffuksgp1backup"
export AKS_NAME="aks-ff-uks-gp-1"
export AKS_RG="rg-ff-uks-gp-net"
export EXT_NAME="azure-aks-backup"
export BINDING_NAME="azbkup-trust"
export PE_NAME="pe-${SA_NAME}-blob"
export VNET_NAME="vnet-ff-uks-gp-1"

# ── Step 1: Delete the backup instance (must go first, before vault)
echo "==> Deleting backup instance..."
INSTANCE_NAME=$(az dataprotection backup-instance list \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[0].name" -o tsv)

az dataprotection backup-instance delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --backup-instance-name "$INSTANCE_NAME" \
  --yes

# ── Step 2: Delete the trusted access role binding from the AKS cluster
echo "==> Deleting trusted access role binding..."
az aks trustedaccess rolebinding delete \
  --subscription "$SUB_ID" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --yes

# ── Step 3: Remove the AKS backup extension from the cluster
echo "==> Removing AKS backup extension..."
az k8s-extension delete \
  --subscription "$SUB_ID" \
  --name "$EXT_NAME" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --cluster-type managedClusters \
  --yes

# ── Step 4: Delete the backup policy (inside the vault)
echo "==> Deleting backup policy..."
az dataprotection backup-policy delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --name "dailyaksbackups" \
  --yes

# ── Step 5: Delete the backup vault
echo "==> Deleting backup vault..."
az dataprotection backup-vault delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --yes

# ── Step 6: Delete the private endpoint
echo "==> Deleting private endpoint..."
az network private-endpoint delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "$PE_NAME" \
  --yes

# ── Step 7: Delete the Private DNS zone group + zone + VNet link
echo "==> Deleting Private DNS zone and VNet link..."
az network private-dns link vnet delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --zone-name "privatelink.blob.core.windows.net" \
  --name "${VNET_NAME}-blob-link" \
  --yes

az network private-dns zone delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "privatelink.blob.core.windows.net" \
  --yes

# ── Step 8: Delete the storage account
echo "==> Deleting storage account..."
az storage account delete \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "$SA_NAME" \
  --yes

# ── Step 9: Delete the PE subnet from the VNet
#    (only if you added snet-ff-uks-gp-pe specifically for this test)
echo "==> Deleting PE subnet..."
az network vnet subnet delete \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --vnet-name "$VNET_NAME" \
  --name "snet-ff-uks-gp-pe"

# ── Step 10: Nuke the resource groups entirely (catches any stragglers)
echo "==> Deleting backup resource group..."
az group delete \
  --subscription "$SUB_ID" \
  --name "$BACKUP_RG" \
  --yes --no-wait

echo "==> Deleting snapshot resource group..."
az group delete \
  --subscription "$SUB_ID" \
  --name "$SNAPSHOT_RG" \
  --yes --no-wait

echo "Done. Extension and trusted access binding removal on the cluster may take a few minutes to propagate."
```

---

### A few things to be aware of before running

- **Soft-delete is enabled** on `aksbackupvault` (your portal snapshot showed this). The vault itself may land in a soft-deleted state rather than immediately disappearing. If `az dataprotection backup-vault delete` completes but the vault shows as soft-deleted, you'll need to purge it: `az dataprotection backup-vault delete --yes` followed by checking "Manage Deleted Vaults" in the portal, or use `az dataprotection recovery-point delete` flows if it blocks.
- **Step 9 (PE subnet)** — only delete `snet-ff-uks-gp-pe` if you created it purely for the backup test. If it's shared with anything else in the VNet, skip this step and just leave the subnet empty.
- **Steps 10 nukes both RGs** with `--no-wait` for speed. Any snapshots in `pentest-1-backup-snapshots-rg` will be caught by the RG delete.
- **RBAC role assignments** on the storage account and snapshot RG are automatically removed when the resources/RGs are deleted — no need to clean them up manually.