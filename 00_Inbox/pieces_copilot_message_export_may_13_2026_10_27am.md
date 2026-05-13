*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 13, 2026 - 10:27 AM*
---
Good — I have rich context from your memory on both the `sandbox-testing-1` subscription and the `terraform-azure-aks-backup` module. Here's the complete testing plan against the sandbox cluster, grounded in what your LTM actually records about that environment.

---

## Testing Plan: `terraform-azure-aks-backup` v2 Against `sandbox-testing-1`

### Environment facts (from your recorded context)

| Parameter | Value |
|---|---|
| Subscription | `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` (Testing subscription) |
| Location | `uksouth` |
| AKS Cluster | `aks-ff-uks-gp-1` |
| AKS Resource Group | `rg-ff-uks-gp-net` |
| VNet | `vnet-ff-uks-gp-1` (in `rg-ff-uks-gp-net`) |
| Existing Backup RG | `pentest-1-backup-rg` |
| Existing Snapshot RG | `pentest-1-backup-snapshots-rg` |
| Existing Vault | `aksbackupvault` |
| Existing Policy | `dailyaksbackups` |
| Existing Trusted Access Binding | `azbkup-trust` |
| Private endpoint subnet | `snet-ff-uks-gp-pe` (being added via `bastion.tf` / FTFL-615) |
| Included Namespaces (sandbox) | `["spicedb", "sandbox-test-1"]` |
| TF workspace path | `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/FITFILE/Non-Production/sandbox-testing-1` |
| Provider azurerm version in use | `v4.71.0` |

---

### Phase 0 — Pre-flight: Apply the module fixes

Before running any plan, the 10 corrections from the review must land on the `terraform-azure-aks-backup` module branch. Work through them in this order (dependency-ordered, not cosmetic):

1. **Create `versions.tf`** — pin `azurerm >= 3.85.0`, Terraform `>= 1.3.0`.
2. **`variables.tf`** — make the changes below, then move to `main.tf`:
   - Remove defaults from `storage_account_name`, `backup_vault_name`, `backup_policy_name`.
   - Change `backup_extension_name` default to `"azure-aks-backup"`.
   - Rename `private_dns_zone_vnet_id` → `vnet_id`.
   - Add `validation {}` to `trusted_access_binding_name` (≤ 24 chars).
   - Delete dead variable `kubernetes_cluster_name`.
3. **`main.tf`** — apply each HCL correction:
   - Add `default_to_oauth_authentication = true` to `azurerm_storage_account.backup_sa`.
   - Fix the `Reader` role scope: `join("/", slice(split("/", var.kubernetes_cluster_id), 0, 5))`.
   - Add missing `vault_msi_data_protection_reader_on_cluster` role assignment.
   - Add `skip_service_principal_aad_check = true` to **all** `azurerm_role_assignment` resources.
   - Add `azurerm_private_endpoint.backup_sa_blob` to `backup_extension` `depends_on`.
   - Add `azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access` to `backup_instance` `depends_on`.
   - Update `virtual_network_id` reference to `var.vnet_id`.

Once done, tag the module as `v1.2.0` (or whatever your next TFC registry version is — your prior sessions reference the plan to release `v1.2.0`).

---

### Phase 1 — Pre-existing resource discovery

Before running `terraform plan`, confirm the state of pre-existing resources against which imports are needed. Run from your jumpbox or Cloud Shell:

```bash
export SUB_ID="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export AKS_RG="rg-ff-uks-gp-net"
export AKS_NAME="aks-ff-uks-gp-1"
export BACKUP_RG="pentest-1-backup-rg"
export SNAPSHOT_RG="pentest-1-backup-snapshots-rg"

# 1. Confirm AKS cluster ARM ID (needed for kubernetes_cluster_id input)
az aks show --subscription "$SUB_ID" -g "$AKS_RG" -n "$AKS_NAME" --query id -o tsv

# 2. Confirm AKS UAI / kubelet object ID (needed for kubernetes_identity_principal_id)
az aks show --subscription "$SUB_ID" -g "$AKS_RG" -n "$AKS_NAME" \
  --query "identityProfile.kubeletidentity.objectId" -o tsv

# 3. Confirm trusted access binding still exists as 'azbkup-trust'
az aks trustedaccess rolebinding list \
  --subscription "$SUB_ID" --resource-group "$AKS_RG" --cluster-name "$AKS_NAME" -o table

# 4. Confirm existing backup extension name on cluster
az k8s-extension list \
  --subscription "$SUB_ID" --cluster-type managedClusters \
  --cluster-name "$AKS_NAME" --resource-group "$AKS_RG" -o table

# 5. Confirm existing private endpoint subnet is provisioned
az network vnet subnet list \
  --subscription "$SUB_ID" --resource-group "$AKS_RG" \
  --vnet-name "vnet-ff-uks-gp-1" \
  --query "[].{Name:name, Prefix:addressPrefix, PEPolicies:privateEndpointNetworkPolicies}" -o table
```

> **Namespace drift watch**: Your prior sessions flag that the live backup instance has `included_namespaces = ["barts","ff-a",...]` (production list), but your sandbox config targets `["spicedb","sandbox-test-1"]`. Changing `included_namespaces` on `azurerm_data_protection_backup_instance_kubernetes_cluster` **forces replacement** of the resource. Check the plan carefully before applying — forced replacement of the backup instance is expected and correct for the sandbox target.

---

### Phase 2 — `sandbox-testing-1/main.tf` module call

Update your `sandbox-testing-1` workspace's `main.tf` module block with these values (substituting ARM IDs from Phase 1 discovery):

```hcl
module "aks_backup" {
  source  = "app.terraform.io/FITFILE-Platforms/aks-backup/azure"
  version = "1.2.0"  # the corrected version

  # --- Required: cluster identity ---
  kubernetes_cluster_id             = "<FULL-AKS-ARM-ID>"         # from Phase 1, step 1
  kubernetes_identity_principal_id  = "<AKS-UAI-OBJECT-ID>"       # from Phase 1, step 2

  # --- Required: resource groups ---
  backup_resource_group_name        = "pentest-1-backup-rg"
  snapshot_resource_group_name      = "pentest-1-backup-snapshots-rg"

  # --- Required: naming (no defaults now) ---
  storage_account_name              = "sboxaksbackup<randomised>"  # globally unique, lowercase
  backup_vault_name                 = "aksbackupvault"             # existing — import needed
  backup_policy_name                = "dailyaksbackups"            # existing — import needed

  # --- Private endpoint (critical path) ---
  create_private_endpoint           = true
  private_endpoint_subnet_id        = "/subscriptions/7bbc8ae5-.../resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/virtualNetworks/vnet-ff-uks-gp-1/subnets/snet-ff-uks-gp-pe"
  vnet_id                           = "/subscriptions/7bbc8ae5-.../resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/virtualNetworks/vnet-ff-uks-gp-1"

  # --- Trusted access (uses corrected default) ---
  trusted_access_binding_name       = "azbkup-trust"              # existing — import needed

  # --- Extension name (corrected default will be "azure-aks-backup") ---
  # backup_extension_name = "azure-aks-backup"  # only needed if overriding

  # --- Backup scope for sandbox ---
  backup_instance_included_namespaces = ["spicedb", "sandbox-test-1"]

  # --- Storage replication ---
  storage_account_replication_type  = "ZRS"
  storage_public_network_access_enabled = false
}
```

---

### Phase 3 — Terraform import (pre-existing resources)

Your prior sessions established these exact import commands. Run them from the `sandbox-testing-1` workspace directory before the first `terraform plan`:

```bash
export SUB="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export AKS_RG="rg-ff-uks-gp-net"
export AKS_CLUSTER="aks-ff-uks-gp-1"
export BACKUP_RG="pentest-1-backup-rg"
export SNAPSHOT_RG="pentest-1-backup-snapshots-rg"

# Trusted access binding (pre-existing; must be imported before apply)
terraform import \
  'module.aks_backup.azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access' \
  "/subscriptions/$SUB/resourceGroups/$AKS_RG/providers/Microsoft.ContainerService/managedClusters/$AKS_CLUSTER/trustedAccessRoleBindings/azbkup-trust"

# Backup vault (pre-existing)
terraform import \
  'module.aks_backup.azurerm_data_protection_backup_vault.backup_vault' \
  "/subscriptions/$SUB/resourceGroups/$BACKUP_RG/providers/Microsoft.DataProtection/backupVaults/aksbackupvault"

# Backup policy (pre-existing)
terraform import \
  'module.aks_backup.azurerm_data_protection_backup_policy_kubernetes_cluster.backup_policy' \
  "/subscriptions/$SUB/resourceGroups/$BACKUP_RG/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupPolicies/dailyaksbackups"

# Backup extension (pre-existing — check name from Phase 1 step 4)
terraform import \
  'module.aks_backup.azurerm_kubernetes_cluster_extension.backup_extension' \
  "/subscriptions/$SUB/resourceGroups/$AKS_RG/providers/Microsoft.ContainerService/managedClusters/$AKS_CLUSTER/providers/Microsoft.KubernetesConfiguration/extensions/azure-aks-backup"
```

> ⚠️ **Extension name check**: Your existing extension in production was listed as `azbkuextension` in the prior PoC session notes — but the corrected module default is `"azure-aks-backup"`. Verify the actual name on the cluster from Phase 1 step 4 before importing. If it still exists under `azbkuextension`, the import path uses that name. The Terraform resource and Azure resource names must match at import time.

---

### Phase 4 — Plan review checklist

Run `terraform plan` (via HCP TFC or `terraform plan -out=plan.tfplan` locally). Review against this checklist before applying:

| Check | Expected |
|---|---|
| `azurerm_storage_account.backup_sa` — `default_to_oauth_authentication` | `= true` |
| `azurerm_role_assignment.vault_msi_read_on_cluster_rg` — `scope` | AKS **resource group** path (5 segments), not cluster ID |
| `azurerm_role_assignment.vault_msi_data_protection_reader_on_cluster` | Present and NEW |
| All `azurerm_role_assignment` blocks | `skip_service_principal_aad_check = true` present |
| `azurerm_kubernetes_cluster_extension.backup_extension` `depends_on` | Includes `azurerm_private_endpoint.backup_sa_blob` |
| `azurerm_data_protection_backup_instance_kubernetes_cluster` `depends_on` | Includes trusted access binding |
| `included_namespaces` change | Flagged as **forced replacement** — this is expected for sandbox |
| New resources (net new, not imported) | `azurerm_storage_account`, `azurerm_storage_container`, `azurerm_private_endpoint`, `azurerm_private_dns_zone` (if no existing), all new role assignments |
| Plan resource counts | Should be ~18 add, 0-2 change, 0-1 destroy (backup instance replacement only) |
| Cost estimate | Your prior sandbox plan showed ~$98.95/mo |

---

### Phase 5 — Post-apply validation

After `terraform apply`, validate the backup is functional:

```bash
# 1. Confirm backup instance is ProtectionConfigured
az dataprotection backup-instance list \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "aksbackupvault" \
  --query "[].{Name:name, State:protectionStatus.status}" -o table

# 2. Trigger an on-demand backup to verify end-to-end
az dataprotection backup-instance adhoc-backup \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "aksbackupvault" \
  --backup-instance-name "<INSTANCE-NAME-FROM-ABOVE>" \
  --rule-name "BackupHourly"

# 3. Poll job status
az dataprotection job list \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "aksbackupvault" \
  --query "[0].{Status:status, StartTime:startTime}" -o table

# 4. Confirm private endpoint resolves from within the cluster
# (exec into a pod and nslookup the storage account FQDN)
```

---

### Open loops before this plan is "ready to apply"

- **`snet-ff-uks-gp-pe` subnet**: confirm it was created by the FTFL-615 work — the `bastion.tf` edit adding this subnet was done in the prior Claude Code session, but check it is merged and applied in the sandbox workspace before referencing it as the `private_endpoint_subnet_id`.
- **Extension name drift**: the existing extension name (`azbkuextension` vs `azure-aks-backup`) must be reconciled before import — this may require destroying and recreating the extension resource.
- **`azurerm` provider block**: your `providers.tf` in `sandbox-testing-1` must include `storage_use_azuread = true` in the `azurerm` provider block (flagged in the README) now that `shared_access_key_enabled = false` and `default_to_oauth_authentication = true` are both active. Without it, Terraform's storage data-plane operations will fail.
- **Module release**: tag `v1.2.0` in GitLab (`gitlab.com/fitfile/terraform-infrastructure/tfc-modules/terraform-azure-aks-backup`) and publish to HCP TFC registry before pointing the sandbox workspace at the new version.