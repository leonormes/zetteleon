*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 13, 2026 - 9:59 AM*
---
Everything ran cleanly except one issue: the PE subnet deletion failed because the private endpoint NIC (`PE-STFFUKSGP1BACKUP-BLOB.NIC.366F02CA...`) is still registered in `RG-FF-UKS-GP-NET`. This is expected — Azure creates the PE NIC in the VNet's RG, not the backup RG, so it survives the backup RG group delete. You need to wait for the async RG delete to finish, then remove the NIC explicitly before retrying the subnet.

Here is the full validation + remediation script:

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
export VNET_NAME="vnet-ff-uks-gp-1"
export PE_NIC_NAME="PE-STFFUKSGP1BACKUP-BLOB.NIC.366F02CA-D6B5-42E4-BC2B-71AEE4103F97"

echo "============================================"
echo "1. Check RG deletion status (async — may still be in progress)"
echo "============================================"
az group show \
  --subscription "$SUB_ID" \
  --name "$BACKUP_RG" \
  --query "{name:name, state:properties.provisioningState}" \
  -o json 2>/dev/null || echo "  OK: $BACKUP_RG is gone"

az group show \
  --subscription "$SUB_ID" \
  --name "$SNAPSHOT_RG" \
  --query "{name:name, state:properties.provisioningState}" \
  -o json 2>/dev/null || echo "  OK: $SNAPSHOT_RG is gone"

echo ""
echo "============================================"
echo "2. Check backup vault (may be soft-deleted, not fully gone)"
echo "============================================"
az dataprotection backup-vault show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  -o json 2>/dev/null && echo "  WARN: vault still exists" || echo "  OK: vault is gone"

echo ""
echo "============================================"
echo "3. Check storage account is gone"
echo "============================================"
az storage account show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "$SA_NAME" \
  -o json 2>/dev/null && echo "  WARN: storage account still exists" || echo "  OK: storage account is gone"

echo ""
echo "============================================"
echo "4. Check AKS backup extension is gone"
echo "============================================"
az k8s-extension show \
  --subscription "$SUB_ID" \
  --name "$EXT_NAME" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --cluster-type managedClusters \
  --query "{name:name, state:provisioningState}" \
  -o json 2>/dev/null && echo "  WARN: extension still exists" || echo "  OK: extension is gone"

echo ""
echo "============================================"
echo "5. Check trusted access binding is gone"
echo "============================================"
az aks trustedaccess rolebinding list \
  --subscription "$SUB_ID" \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --query "[?name=='$BINDING_NAME'].name" -o tsv 2>/dev/null \
  | grep -q "$BINDING_NAME" && echo "  WARN: binding still exists" || echo "  OK: binding is gone"

echo ""
echo "============================================"
echo "6. Check DNS zone is gone"
echo "============================================"
az network private-dns zone show \
  --subscription "$SUB_ID" \
  --resource-group "$BACKUP_RG" \
  --name "privatelink.blob.core.windows.net" \
  -o json 2>/dev/null && echo "  WARN: DNS zone still exists" || echo "  OK: DNS zone is gone"

echo ""
echo "============================================"
echo "7. Fix: orphaned PE NIC blocking subnet delete"
echo "   Wait for RG delete to complete first, THEN run this block"
echo "============================================"

# Step 7a — wait for RG delete to finish
echo "  Waiting for $BACKUP_RG deletion to complete..."
az group wait \
  --subscription "$SUB_ID" \
  --name "$BACKUP_RG" \
  --deleted \
  --interval 15 \
  --timeout 600 && echo "  OK: $BACKUP_RG fully deleted" || echo "  WARN: timed out — check portal"

# Step 7b — delete the orphaned NIC now that the PE is gone
echo "  Deleting orphaned PE NIC from VNet RG..."
az network nic delete \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --name "$PE_NIC_NAME" \
  --no-wait
echo "  NIC delete triggered"

# Step 7c — wait a moment for NIC deletion to propagate, then retry subnet
sleep 30

echo "  Retrying PE subnet deletion..."
az network vnet subnet delete \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --vnet-name "$VNET_NAME" \
  --name "snet-ff-uks-gp-pe" \
  && echo "  OK: PE subnet deleted" \
  || echo "  WARN: subnet still blocked — NIC deletion may still be propagating, retry in 60s"

echo ""
echo "============================================"
echo "8. Final: confirm PE subnet is gone from VNet"
echo "============================================"
az network vnet subnet list \
  --subscription "$SUB_ID" \
  --resource-group "$AKS_RG" \
  --vnet-name "$VNET_NAME" \
  --query "[].{name:name, prefix:addressPrefix}" \
  -o table
```

---

### What to expect

| Step | Expected result |
|---|---|
| Backup RG | Either already gone or `Deleting` — `az group wait --deleted` will block until it's confirmed |
| Snapshot RG | Same pattern |
| Vault | Gone (or soft-deleted — harmless for a fresh Terraform apply since the name is recycled) |
| Storage account | Gone |
| Extension | Gone |
| Trusted access binding | Gone |
| PE NIC | Needs explicit delete (this is the one blocker) |
| Subnet | Deletable once the NIC is gone |

The SyntaxWarnings you saw (`invalid escape sequence '\W'`, `'\/'`) are harmless Python 3.13 compat warnings in the Azure CLI library itself — not errors, safe to ignore.