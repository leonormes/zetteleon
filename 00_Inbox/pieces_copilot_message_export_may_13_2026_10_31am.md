*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 13, 2026 - 10:31 AM*
---
Clean slate changes everything — no imports, no drift, no forced replacements to manage. Here's the revised plan.

---

## Updated Testing Plan: Clean-Slate Apply Against `sandbox-testing-1`

### What changed from the previous plan

| Area | Before | Now |
|---|---|---|
| Terraform imports | Required for 4 resources | **None — skip entirely** |
| Namespace drift | Forced replacement risk | **No risk — new resource** |
| PE subnet | Assumed pre-existing | **Must be created fresh** |
| Backup RGs | Pre-existing, import-or-skip | **Created fresh by Terraform** |
| Extension name conflict | `azbkuextension` vs `azure-aks-backup` | **No conflict — net new** |

---

### Phase 0 — Module fixes (unchanged — must land first)

Ensure the corrected `terraform-azure-aks-backup` branch is tagged and published to the TFC registry as `v1.2.0` with all 10 fixes applied. No changes to this phase.

---

### Phase 1 — Pre-flight: resolve the two required ARM IDs

You need exactly two values before writing the module call. Run from Cloud Shell or your jumpbox:

```bash
export SUB_ID="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export AKS_RG="rg-ff-uks-gp-net"
export AKS_NAME="aks-ff-uks-gp-1"

# 1. Full AKS ARM ID → kubernetes_cluster_id
az aks show --subscription "$SUB_ID" -g "$AKS_RG" -n "$AKS_NAME" \
  --query id -o tsv

# 2. Kubelet UAI object ID → kubernetes_identity_principal_id
az aks show --subscription "$SUB_ID" -g "$AKS_RG" -n "$AKS_NAME" \
  --query "identityProfile.kubeletidentity.objectId" -o tsv

# 3. Confirm VNet ID (needed for vnet_id input)
az network vnet show --subscription "$SUB_ID" -g "$AKS_RG" \
  -n "vnet-ff-uks-gp-1" --query id -o tsv
```

---

### Phase 2 — Add/confirm the PE subnet in `sandbox-testing-1/bastion.tf`

The PE subnet is provisioned at the **workspace** level (not inside the backup module). It was previously at `10.0.0.96/27`. Add this block back to `bastion.tf`:

```hcl
resource "azurerm_subnet" "backup_pe" {
  name                 = "snet-ff-uks-gp-pe"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
  address_prefixes     = ["10.0.0.96/27"]
  depends_on           = [module.private-infrastructure]
}
```

This subnet's full ARM ID flows into the module call as `private_endpoint_subnet_id`. The module call should reference it as:

```hcl
private_endpoint_subnet_id = azurerm_subnet.backup_pe.id
```

---

### Phase 3 — `sandbox-testing-1/main.tf` module call (clean-slate version)

```hcl
module "aks_backup" {
  source  = "app.terraform.io/FITFILE-Platforms/aks-backup/azure"
  version = "1.2.0"

  # Cluster identity (from Phase 1)
  kubernetes_cluster_id            = "<FULL-AKS-ARM-ID>"
  kubernetes_identity_principal_id = "<AKS-UAI-OBJECT-ID>"

  # Resource groups — both created fresh
  backup_resource_group_name   = "pentest-1-backup-rg"
  snapshot_resource_group_name = "pentest-1-backup-snapshots-rg"

  # Storage — globally unique name required
  storage_account_name            = "sboxaksbackup<randomised>"
  storage_account_replication_type = "ZRS"
  storage_public_network_access_enabled = false

  # Vault and policy — all new
  backup_vault_name  = "sbox-aks-backup-vault"
  backup_policy_name = "sbox-aks-backup-policy"

  # Private endpoint — subnet created in Phase 2
  create_private_endpoint    = true
  private_endpoint_subnet_id = azurerm_subnet.backup_pe.id
  vnet_id                    = "<VNET-ARM-ID>"  # from Phase 1, step 3

  # Extension — uses corrected default "azure-aks-backup"
  # backup_extension_name = "azure-aks-backup"  # only needed if overriding

  # Trusted access binding — corrected default "azbkup-trust"
  trusted_access_binding_name = "azbkup-trust"

  # Backup scope — sandbox namespaces only
  backup_instance_included_namespaces = ["spicedb", "sandbox-test-1"]
}
```

---

### Phase 4 — Provider block check (`sandbox-testing-1/providers.tf`)

With `shared_access_key_enabled = false` and `default_to_oauth_authentication = true` both active on the storage account, the `azurerm` provider **must** have this set or Terraform's storage data-plane operations will fail at plan time:

```hcl
provider "azurerm" {
  features {}
  storage_use_azuread = true
}
```

Confirm this is present before running `terraform plan`.

---

### Phase 5 — Plan review checklist

Run `terraform plan`. Expected outcome on a clean slate:

| Check | Expected |
|---|---|
| Total `add` | ~20 resources |
| `change` | 0 |
| `destroy` | 0 |
| `azurerm_storage_account` — `default_to_oauth_authentication` | `= true` |
| `azurerm_role_assignment.vault_msi_read_on_cluster_rg` — `scope` | Resource group path (5 ARM segments), not cluster ID |
| `azurerm_role_assignment.vault_msi_data_protection_reader_on_cluster` | Present |
| All role assignments | `skip_service_principal_aad_check = true` |
| `azurerm_kubernetes_cluster_extension.backup_extension` `depends_on` | Includes `azurerm_private_endpoint.backup_sa_blob` |
| `azurerm_data_protection_backup_instance_kubernetes_cluster` `depends_on` | Includes trusted access binding |
| `included_namespaces` | `["spicedb", "sandbox-test-1"]` |
| Cost estimate | ~$99/mo (consistent with your prior sandbox plan runs) |

---

### Phase 6 — Apply and validate

```bash
terraform apply plan.tfplan
```

Once complete, validate end-to-end:

```bash
export SUB="7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"
export BACKUP_RG="pentest-1-backup-rg"

# 1. Confirm backup instance is ProtectionConfigured
az dataprotection backup-instance list \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "sbox-aks-backup-vault" \
  --query "[].{Name:name, State:protectionStatus.status}" -o table

# 2. Trigger an on-demand backup
az dataprotection backup-instance adhoc-backup \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "sbox-aks-backup-vault" \
  --backup-instance-name "<INSTANCE-NAME>" \
  --rule-name "BackupHourly"

# 3. Poll job to completion
az dataprotection job list \
  --subscription "$SUB" -g "$BACKUP_RG" --vault-name "sbox-aks-backup-vault" \
  --query "[0].{Status:status, StartTime:startTime, EndTime:endTime}" -o table
```

---

### Remaining open loop

The only open item before hitting apply is the **storage account name** — it must be globally unique across all of Azure. Pick something like `sboxaksbackup<5-char-random>` (all lowercase, no hyphens, ≤ 24 chars) and verify availability:

```bash
az storage account check-name --name "sboxaksbackup<random>" --query nameAvailable -o tsv
```

Everything else is fully defined. Once you have the two ARM IDs from Phase 1 and a confirmed storage account name, you're good to run `terraform plan`.