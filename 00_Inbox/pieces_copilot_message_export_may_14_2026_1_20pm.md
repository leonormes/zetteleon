*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday May 14, 2026 - 1:20 PM*
---
The key evidence is in your LTM — your memory from today at 12:27 PM shows this session was already deep in debugging this exact backup instance error sequence. Here's the full diagnosis.

---

## `406 Not Acceptable` on `BackupInstancesCreateOrUpdate` — Root Cause & Fix

### What the 406 actually means

A `406 Not Acceptable` with **no body** from the Azure Data Protection API is the service's way of saying the **prerequisite validation failed before the request was even processed**. It is NOT a permissions error or a conflict error — it means the API's pre-flight check of your request payload found something it couldn't accept. The most common causes after a clean-delete + re-create cycle are:

---

### The three likely culprits (in order of probability)

**1. The trusted access binding doesn't exist yet (most common)**

The backup instance API validates the trusted access binding is present on the cluster **before** accepting the create request. You deleted it as part of the cleanup. Even though your `depends_on` includes it, **AAD replication lag** means the binding may be registered in Terraform state but not yet visible to the Data Protection API.

Run this immediately to confirm it exists from Azure's perspective:

```bash
export SUB="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export AKS_RG="rg-ff-uks-gp-net"
export AKS_NAME="aks-ff-uks-gp-1"

az aks trustedaccess rolebinding list \
  --subscription "$SUB" \
  --resource-group "$AKS_RG" \
  --cluster-name "$AKS_NAME" \
  -o table
```

If it's missing or shows `Updating` provisioning state — that's your problem. Wait for `Succeeded` before re-applying.

---

**2. The backup extension is not yet fully provisioned**

The extension (`azure-aks-backup`) has its own provisioning state, and the Data Protection API also validates the extension's identity is resolvable before accepting a backup instance. Check:

```bash
az k8s-extension show \
  --subscription "$SUB" \
  --cluster-type managedClusters \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --name "azure-aks-backup" \
  --query "{State:provisioningState, MSI:aksAssignedIdentity.principalId}" \
  -o table
```

Must show `Succeeded` and a non-null `principalId`. If `provisioningState` is still `Creating` or `Updating`, the 406 will keep happening until it settles.

---

**3. Role assignments not yet propagated in AAD (the `skip_service_principal_aad_check` race)**

Even with `skip_service_principal_aad_check = true`, the Data Protection control plane does its **own** MSI resolution check server-side before accepting the backup instance create. Role assignments on dynamically-created MSIs (extension MSI, vault MSI) can take 3–10 minutes to propagate.

Verify the critical ones are in place:

```bash
export BACKUP_RG="pentest-1-backup-rg"
export VAULT_NAME="sbox-aks-backup-vault"

# Get vault MSI principal ID
VAULT_MSI=$(az dataprotection backup-vault show \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "$VAULT_NAME" \
  --query "identity.principalId" -o tsv)

# Get extension MSI principal ID
EXT_MSI=$(az k8s-extension show \
  --subscription "$SUB" \
  --cluster-type managedClusters \
  --cluster-name "$AKS_NAME" \
  --resource-group "$AKS_RG" \
  --name "azure-aks-backup" \
  --query "aksAssignedIdentity.principalId" -o tsv)

echo "Vault MSI: $VAULT_MSI"
echo "Extension MSI: $EXT_MSI"

# Check vault MSI has Data Protection Reader on the cluster
az role assignment list \
  --subscription "$SUB" \
  --assignee "$VAULT_MSI" \
  --query "[].{Role:roleDefinitionName, Scope:scope}" -o table

# Check extension MSI has Storage Blob Data Contributor on the SA
az role assignment list \
  --subscription "$SUB" \
  --assignee "$EXT_MSI" \
  --query "[].{Role:roleDefinitionName, Scope:scope}" -o table
```

---

### The fix

**Wait, then re-apply.** The 406 is a transient timing error, not a permanent configuration failure. The sequence:

1. Confirm the trusted access binding is `Succeeded` (step 1 above).
2. Confirm the extension is `Succeeded` with a valid MSI (step 2 above).
3. Confirm all role assignments are visible (step 3 above).
4. Wait **5 minutes** after everything shows green.
5. Run `terraform apply` again — Terraform will retry the backup instance create and it will succeed.

If you want to accelerate without waiting on Terraform, you can also **validate** via the CLI first to get a clearer error message:

```bash
# This gives a much more descriptive error than the 406
az dataprotection backup-instance validate-for-backup \
  --subscription "$SUB" \
  --resource-group "$BACKUP_RG" \
  --vault-name "$VAULT_NAME" \
  --backup-instance @<your-backup-instance-json>
```

Your LTM from your prior PoC sessions (Apr 29) shows you hit `UserErrorTrustedAccessGatewayReturnedForbidden` using this validate command before — that diagnostic path gives you the exact error code rather than a naked 406.

---

### If the 406 persists after everything is green

Add an explicit `time_sleep` resource in the module between the trusted access binding + role assignments and the backup instance:

```hcl
resource "time_sleep" "wait_for_rbac_propagation" {
  depends_on = [
    azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access,
    azurerm_role_assignment.vault_msi_data_protection_reader_on_cluster,
    azurerm_role_assignment.extension_storage_account_permission,
  ]
  create_duration = "300s"  # 5 minutes
}

resource "azurerm_data_protection_backup_instance_kubernetes_cluster" "backup_instance" {
  depends_on = [
    time_sleep.wait_for_rbac_propagation,
    # ... rest of depends_on
  ]
}
```

This is the standard pattern for AKS backup — the Azure provider has no native retry on this 406 and the API genuinely needs the propagation time.