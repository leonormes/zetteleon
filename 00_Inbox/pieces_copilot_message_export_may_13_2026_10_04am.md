*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 13, 2026 - 10:04 AM*
---
Everything is clean except one thing: the private endpoint itself (`pe-stffuksgp1backup-blob`) survived because it was created in `rg-ff-uks-gp-net` (the VNet RG), not inside `pentest-1-backup-rg`. The backup RG delete didn't reach it. You need to delete the PE directly — Azure will then clean up the NIC automatically, unblocking the subnet.

```bash
# Step 1: Delete the private endpoint (it's in the VNet RG, not the backup RG)
az network private-endpoint delete \
  --subscription "$SUB_ID" \
  --resource-group "rg-ff-uks-gp-net" \
  --name "pe-stffuksgp1backup-blob" \
  --yes

# Step 2: Wait for Azure to clean up the NIC (it's tied to the PE lifecycle)
echo "Waiting 60s for PE and NIC cleanup to propagate..."
sleep 60

# Step 3: Delete the subnet
az network vnet subnet delete \
  --subscription "$SUB_ID" \
  --resource-group "rg-ff-uks-gp-net" \
  --vnet-name "vnet-ff-uks-gp-1" \
  --name "snet-ff-uks-gp-pe"

# Step 4: Confirm clean VNet state (snet-ff-uks-gp-pe should be absent)
az network vnet subnet list \
  --subscription "$SUB_ID" \
  --resource-group "rg-ff-uks-gp-net" \
  --vnet-name "vnet-ff-uks-gp-1" \
  --query "[].{name:name, prefix:addressPrefix}" \
  -o table
```

**Why this happened:** the original teardown script deleted the PE from `$BACKUP_RG`, but the PE was actually placed in `rg-ff-uks-gp-net` because that's where the VNet lives. The `az network private-endpoint delete` command in the script skipped it silently (no error, just no-op on a resource that didn't exist in that RG). The NIC cannot be deleted directly while the PE still exists — you have to delete the PE first and Azure tears down the NIC as part of that operation.

Once `snet-ff-uks-gp-pe` is absent from the subnet list output, you're fully clean and ready to run `terraform apply`.