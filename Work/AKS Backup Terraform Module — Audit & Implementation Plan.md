---
created: 2026-04-30T00:00:00+00:00
jira: ["[FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596)", "[FTFL-599](https://fitfile.atlassian.net/browse/FTFL-599)", "[FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615)"]
modified: 2026-07-20T16:33:33+00:00
module: terraform-azure-aks-backup
permalink: llmeon/work/aks-backup-terraform-module-audit-implementation-plan
tags: [aks, azure, backup, ftfl-596, ftfl-599, ftfl-615, infrastructure, terraform]
title: AKS Backup Terraform Module — Audit & Implementation Plan
---

Module: `terraform-azure-aks-backup` (master, tag v1.1.2)

Jira: [FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596) · [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615) · [FTFL-599](https://fitfile.atlassian.net/browse/FTFL-599)

---

## 1. Current State Inventory

### Files Present

| File | Purpose |
|------|---------|
| `main.tf` | All resources (218 lines) |
| `variables.tf` | All inputs (197 lines) |
| `moved_2026-04-21.tf` | State migration blocks from rename refactor |
| `README.md` | Sparse; contains one inaccurate note |

No `outputs.tf`. No `versions.tf`.

### Resources in `main.tf`

| Resource | Logical name | Status |
|---|---|---|
| `azurerm_resource_group` | backup RG + snap RG | ✅ Create-or-data pattern |
| `azurerm_storage_account` | `backup_sa` | ✅ Hardened; PE-ready (`public_network_access_enabled` variable) |
| `azurerm_storage_container` | `backup_container` | ✅ |
| `azurerm_data_protection_backup_vault` | `backup_vault` | ✅ SystemAssigned identity |
| `azurerm_kubernetes_cluster_trusted_access_role_binding` | `aks_cluster_trusted_access` | ✅ Correct role; name mismatch (see §2) |
| `azurerm_kubernetes_cluster_extension` | `backup_extension` | ✅ `Microsoft.DataProtection.Kubernetes` |
| `azurerm_role_assignment` × 6 | RBAC suite | ⚠️ One role wrong (see §2) |
| `azurerm_data_protection_backup_policy_kubernetes_cluster` | `backup_policy` | ✅ Default retention rule wired |
| `azurerm_data_protection_backup_instance_kubernetes_cluster` | `backup_instance` | ✅ Namespace filter wired; all RBAC in `depends_on` |

### Data Sources & Provider

- `azurerm_client_config.current`—used for subscription/tenant ID in extension config settings.
- No `terraform {}` block, no `required_providers`, no `required_version`. Provider constraints are entirely caller-side.

---

## 2. Gaps (What Is Missing to Replicate the End-to-End CLI Path)

### Gap 1—Private Endpoint (Most Critical, [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615))

The module has `backup_storage_account_allowed_subnet_ids` wired into `network_rules.virtual_network_subnet_ids`—that is a service endpoint mechanism, not a private endpoint. There is no `azurerm_private_endpoint`, no `azurerm_private_dns_zone`, and no VNet link. With `public_network_access_enabled = false` and no private endpoint, the backup instance cannot reach the storage account.

### Gap 2—Private DNS Zone + VNet Link

`privatelink.blob.core.windows.net` is not created or linked. In a Hub-Spoke topology (which Fitfile uses) this zone lives centrally; the module needs either a data-source lookup or optional creation, plus an optional VNet link.

### Gap 3—Extension MSI RBAC Role is Wrong

`azurerm_role_assignment.extension_storage_account_permission` assigns "Storage Account Contributor" (management-plane only). The RBAC playbook from [FTFL-599](https://fitfile.atlassian.net/browse/FTFL-599) identifies the gap as: _Extension MSI requires Storage Blob Data Contributor on the storage account_ (data-plane write access for backup objects). The extension needs to write blobs, not manage the account.

### Gap 4—Trusted Access Binding Name Drift

Code hardcodes `name = "aksbackuprb"`. The manually created binding in `pentest-1-backup-rg` is named `azbkup-trust`. If the module is applied against an environment where the manual binding already exists, there will be two bindings or a state import is required. The name should be a variable.

### Gap 5—No `outputs.tf`

No outputs exported. Downstream stacks (CI/CD, restore runbooks per [FTFL-599](https://fitfile.atlassian.net/browse/FTFL-599)) cannot reference vault ID, policy ID, instance ID, or principal IDs without them.

### Gap 6—No `versions.tf`

Provider constraints are not pinned. The `azurerm_kubernetes_cluster_trusted_access_role_binding` and `azurerm_data_protection_backup_instance_kubernetes_cluster` resources have had breaking argument changes across azurerm `3.x` vs `4.x`. A minimum version floor must be explicit.

### Gap 7—README Accuracy

README states `shared_access_key_enabled = false`, but `main.tf:40` sets it to `true` with a comment explaining this is required for the backup instance. The README is the reverse of the truth and will mislead operators.

### Gap 8—Backup time Default is a 2024 past Date, Wrong Hour

`backup_repeating_time_intervals` default is `"R/2024-09-02T21:00:00+00:00/P1D"` (21:00 UTC). The intended schedule is 02:00 daily per context. Azure accepts past ISO 8601 start dates, but the default should reflect intent and be documented.

---

## 3. Proposed Changes

### 3a. Private Endpoint + DNS (New rEsources)

Add four new variables and three conditional resources:

```hcl
# variables.tf additions

variable "create_private_endpoint" {
  description = "Create a private endpoint for the backup storage account."
  type        = bool
  default     = false
}

variable "private_endpoint_subnet_id" {
  description = "Subnet ID for the private endpoint (from azure-private-infra per FTFL-615). Required when create_private_endpoint = true."
  type        = string
  default     = null
}

variable "private_dns_zone_id" {
  description = "Resource ID of an existing privatelink.blob.core.windows.net private DNS zone. When provided, no new zone is created. When null and create_private_endpoint = true, a new zone is created in the backup RG."
  type        = string
  default     = null
}

variable "private_dns_zone_vnet_id" {
  description = "VNet resource ID to link to a newly created private DNS zone. Required when create_private_endpoint = true and private_dns_zone_id is null."
  type        = string
  default     = null
}
```

```hcl
# main.tf additions — private networking

locals {
  create_private_dns_zone = var.create_private_endpoint && var.private_dns_zone_id == null

  effective_private_dns_zone_id = local.create_private_dns_zone ? (
    azurerm_private_dns_zone.blob[0].id
  ) : var.private_dns_zone_id
}

resource "azurerm_private_dns_zone" "blob" {
  count               = local.create_private_dns_zone ? 1 : 0
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = local.backup_rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "blob" {
  count                 = local.create_private_dns_zone ? 1 : 0
  name                  = "${var.storage_account_name}-dns-link"
  resource_group_name   = local.backup_rg.name
  private_dns_zone_name = azurerm_private_dns_zone.blob[0].name
  virtual_network_id    = var.private_dns_zone_vnet_id
  registration_enabled  = false
}

resource "azurerm_private_endpoint" "backup_sa" {
  count               = var.create_private_endpoint ? 1 : 0
  name                = "${var.storage_account_name}-pe"
  resource_group_name = local.backup_rg.name
  location            = local.backup_rg.location
  subnet_id           = var.private_endpoint_subnet_id

  private_service_connection {
    name                           = "${var.storage_account_name}-psc"
    private_connection_resource_id = azurerm_storage_account.backup_sa.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [local.effective_private_dns_zone_id]
  }
}
```

> Note on `network_rules`: When using a private endpoint with `public_network_access_enabled = false`, the `virtual_network_subnet_ids` list (service endpoints) is not needed for the PE subnet—traffic routes via the PE automatically. `bypass = ["AzureServices"]` must stay so the Azure Backup service plane can reach the account.

### 3b. Fix Extension MSI RBAC Role

```hcl
resource "azurerm_role_assignment" "extension_storage_account_permission" {
  scope                = azurerm_storage_account.backup_sa.id
  role_definition_name = "Storage Blob Data Contributor"   # was: "Storage Account Contributor"
  principal_id         = azurerm_kubernetes_cluster_extension.backup_extension.aks_assigned_identity[0].principal_id
}
```

> The extension MSI writes backup objects to the blob container—it needs data-plane access (`Storage Blob Data Contributor`), not management-plane control (`Storage Account Contributor`). The vault MSI already holds `Storage Blob Data Contributor` separately.

> Drift risk: Terraform will destroy the old assignment and create the new one. The brief gap is safe but plan the apply outside the 02:00 backup window.

### 3c. Parameterise Trusted Access Binding Name

```hcl
# variables.tf
variable "trusted_access_binding_name" {
  description = "Name of the AKS trusted access role binding."
  type        = string
  default     = "aksbackuprb"
}

# main.tf
resource "azurerm_kubernetes_cluster_trusted_access_role_binding" "aks_cluster_trusted_access" {
  kubernetes_cluster_id = var.kubernetes_cluster_id
  name                  = var.trusted_access_binding_name
  roles                 = ["Microsoft.DataProtection/backupVaults/backup-operator"]
  source_resource_id    = azurerm_data_protection_backup_vault.backup_vault.id
}
```

> Import note for pentest-1: Set `trusted_access_binding_name = "azbkup-trust"` and run `terraform import` before applying. Never destroy-and-recreate a live trusted access binding.

### 3d. Add `outputs.tf`

```hcl
output "backup_vault_id" {
  description = "Resource ID of the backup vault."
  value       = azurerm_data_protection_backup_vault.backup_vault.id
}

output "backup_vault_name" {
  description = "Name of the backup vault."
  value       = azurerm_data_protection_backup_vault.backup_vault.name
}

output "backup_vault_principal_id" {
  description = "Principal ID of the backup vault's system-assigned managed identity."
  value       = azurerm_data_protection_backup_vault.backup_vault.identity[0].principal_id
}

output "backup_policy_id" {
  description = "Resource ID of the backup policy."
  value       = azurerm_data_protection_backup_policy_kubernetes_cluster.backup_policy.id
}

output "backup_instance_id" {
  description = "Resource ID of the backup instance."
  value       = azurerm_data_protection_backup_instance_kubernetes_cluster.backup_instance.id
}

output "storage_account_id" {
  description = "Resource ID of the backup storage account."
  value       = azurerm_storage_account.backup_sa.id
}

output "storage_account_name" {
  description = "Name of the backup storage account."
  value       = azurerm_storage_account.backup_sa.name
}

output "extension_principal_id" {
  description = "Principal ID of the backup extension's system-assigned managed identity."
  value       = azurerm_kubernetes_cluster_extension.backup_extension.aks_assigned_identity[0].principal_id
}

output "private_endpoint_ip" {
  description = "Private IP address of the storage account private endpoint, if created."
  value = (
    var.create_private_endpoint
    ? azurerm_private_endpoint.backup_sa[0].private_service_connection[0].private_ip_address
    : null
  )
}
```

### 3e. Add `versions.tf`

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.116.0, < 5.0.0"
    }
  }
}
```

> `3.116` is the last patch before `4.x` known stable with these resources. If workspace runs azurerm `4.x`, bump floor to `>= 4.0.0` and verify argument compatibility (`storage_account_id` vs `storage_account_name` on the container resource changed in 4.x).

---

## 4. Implementation Plan

### Phase 1—Private Networking & Storage ([FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615))

Prerequisite: `snet-ff-uks-gp-pe` subnet must already exist in the VNet (provisioned by `azure-private-infra`). Confirm subnet ID before proceeding.

1. Add `versions.tf` (no resource changes, safe to apply immediately).
2. Add the four PE-related variables.
3. Add the three PE resources to `main.tf` (behind `count` gates).
4. Add `outputs.tf`.
5. Tag: `v1.2.0`.
6. In the calling stack (pentest-1):
   - Set `create_private_endpoint = true`
   - Set `private_endpoint_subnet_id` to the `snet-ff-uks-gp-pe` subnet ID
   - Set `private_dns_zone_id` to existing hub zone ID (or omit to create standalone zone)
   - Set `storage_public_network_access_enabled = false`
7. Run `terraform plan`—confirm PE, DNS group, and (if applicable) new zone are created. No existing resources destroyed.
8. Apply.

### Phase 2—Vault, Policy, Extension (Confirm State / iMport)

The module already provisions vault, policy, and extension. For environments created via CLI:

```bash
terraform import 'azurerm_data_protection_backup_vault.backup_vault' \
  /subscriptions/<sub>/resourceGroups/pentest-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault

terraform import 'azurerm_kubernetes_cluster_extension.backup_extension' \
  /subscriptions/<sub>/resourceGroups/<aks-rg>/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-1/providers/Microsoft.KubernetesConfiguration/extensions/azure-aks-backup

terraform import 'azurerm_data_protection_backup_policy_kubernetes_cluster.backup_policy' \
  /subscriptions/<sub>/resourceGroups/pentest-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupPolicies/dailyaksbackups
```

> Set `backup_extension_name = "azure-aks-backup"` in the calling stack to match the manually created extension name.

### Phase 3—RBAC & Trusted Access Binding

1. Apply the RBAC role fix (`Storage Account Contributor` → `Storage Blob Data Contributor`). Plan will show one destroy + one create on `extension_storage_account_permission`. Apply during maintenance window.
2. For the trusted access binding—if environment has manual binding `azbkup-trust`:

   ```bash
   terraform import 'azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access' \
     /subscriptions/<sub>/resourceGroups/<aks-rg>/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-1/trustedAccessRoleBindings/azbkup-trust
   ```

3. Import or create backup instance:

   ```bash
   terraform import 'azurerm_data_protection_backup_instance_kubernetes_cluster.backup_instance' \
     /subscriptions/<sub>/resourceGroups/pentest-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupInstances/dailyaksbackup
   ```

4. Verify caller sets:

   ```hcl
   backup_included_namespaces = ["barts", "ff-a", "ff-b", "ff-c", "spicedb", "thehyve", "thehyve-cuh", "thehyve-mkuh"]
   backup_repeating_time_intervals = ["R/2026-01-01T02:00:00+00:00/P1D"]
   ```

### Phase 4—Validation & CI/CD Integration

See §6 below.

### Phase 5—Rollout & Rollback

- Rollout order: Infra (PE + DNS) → RBAC fix → instance import/create. Never destroy a running backup instance.
- Rollback: All PE resources are additive. RBAC role swap is the only potentially disruptive step; schedule outside backup windows.
- Drift guard: Run `terraform plan` in CI on every merge to master. Any out-of-band CLI change surfaces as a diff. See [FTFL-599](https://fitfile.atlassian.net/browse/FTFL-599) runbook to ensure restore steps don't mutate Terraform-managed resources.

---

## 5. Sample HCL—Calling Stack (Pentest-1)

```hcl
module "aks_backup" {
  source = "git::https://gitlab.com/fitfile/terraform-azure-aks-backup.git?ref=v1.2.0"

  location = "uksouth"

  # Resource groups (pre-existing)
  create_backup_resource_group   = false
  backup_resource_group_name     = "pentest-1-backup-rg"
  create_snapshot_resource_group = false
  snapshot_resource_group_name   = "pentest-1-backup-snapshots-rg"

  # Storage
  storage_account_name                  = "stffuksgp1backup"
  container_name                        = "aks-backups"
  storage_account_replication_type      = "ZRS"
  storage_public_network_access_enabled = false

  # Private endpoint (FTFL-615 subnet)
  create_private_endpoint    = true
  private_endpoint_subnet_id = data.azurerm_subnet.backup_pe.id
  private_dns_zone_id        = data.azurerm_private_dns_zone.blob.id  # existing hub zone

  # Vault
  backup_vault_name       = "aksbackupvault"
  backup_vault_redundancy = "LocallyRedundant"

  # Extension (matches the manually created extension name)
  backup_extension_name = "azure-aks-backup"

  # Trusted access binding (matches the manually created binding)
  trusted_access_binding_name = "azbkup-trust"

  # AKS cluster
  kubernetes_cluster_id            = data.azurerm_kubernetes_cluster.aks.id
  kubernetes_cluster_name          = "aks-ff-uks-gp-1"
  kubernetes_identity_principal_id = data.azurerm_kubernetes_cluster.aks.identity[0].principal_id

  # Policy & instance
  backup_policy_name              = "dailyaksbackups"
  backup_instance_name            = "dailyaksbackup"
  retention_days                  = 14
  backup_repeating_time_intervals = ["R/2026-01-01T02:00:00+00:00/P1D"]

  # Included namespaces per FTFL-599 runbook
  backup_included_namespaces = [
    "barts", "ff-a", "ff-b", "ff-c",
    "spicedb", "thehyve", "thehyve-cuh", "thehyve-mkuh"
  ]
  backup_volume_snapshot_enabled          = true
  backup_cluster_scoped_resources_enabled = true
  backup_excluded_resource_types          = ["volumesnapshotcontent.snapshot.storage.k8s.io"]
}
```

---

## 6. Validation & Testing Plan

### DNS Resolution (Private eNdpoint)

```bash
# From a pod inside the AKS cluster
kubectl run dns-test --image=busybox --rm -it --restart=Never -- \
  nslookup stffuksgp1backup.blob.core.windows.net
# Expected: resolves to a 10.x.x.x private IP, NOT a public Azure range.

# Confirm PE IP matches DNS
az network private-endpoint show \
  --name stffuksgp1backup-pe \
  --resource-group pentest-1-backup-rg \
  --query "customDnsConfigs[].ipAddresses" -o tsv
```

### Backup Vault & Extension State

```bash
az dataprotection backup-vault show \
  --resource-group pentest-1-backup-rg \
  --vault-name aksbackupvault \
  --query "properties.provisioningState"
# Expected: "Succeeded"

az k8s-extension show \
  --cluster-name aks-ff-uks-gp-1 \
  --resource-group <aks-rg> \
  --cluster-type managedClusters \
  --name azure-aks-backup \
  --query "{state: installState, health: statuses[0].message}"
# Expected installState: "Installed"
```

### Backup Instance Protection State

```bash
az dataprotection backup-instance list \
  --resource-group pentest-1-backup-rg \
  --vault-name aksbackupvault \
  --query "[].{name:name, state:properties.currentProtectionState}"
# Expected: "ProtectionConfigured"
```

### Ad-hoc Backup Trigger

```bash
az dataprotection backup-instance adhoc-backup \
  --name dailyaksbackup \
  --resource-group pentest-1-backup-rg \
  --vault-name aksbackupvault \
  --rule-name BackupHourly

az dataprotection job list \
  --resource-group pentest-1-backup-rg \
  --vault-name aksbackupvault \
  --query "[0].{status:properties.status, dataSource:properties.dataSourceInfo.datasourceType}"
# Expected status: "Completed"
```

### Terraform Drift Check

```bash
terraform plan -detailed-exitcode
# Exit code 0 = no drift. Exit code 2 = diff exists (investigate before applying).
```

---

## 7. Jira / PR Deliverables

### PR Title

```
feat(backup): add private endpoint, fix extension RBAC, add outputs and version constraints
```

### PR Description

```
## Summary

- Adds private endpoint support for the backup storage account (`create_private_endpoint`
  variable gate). Wires private DNS zone group with optional create-or-reference pattern to
  support both hub-zone and standalone deployments. Closes FTFL-615.

- Fixes `azurerm_role_assignment.extension_storage_account_permission` from
  `Storage Account Contributor` to `Storage Blob Data Contributor` — the extension MSI
  needs data-plane blob write access, not management-plane control. Identified in FTFL-599
  RBAC gap analysis.

- Parameterises trusted access binding name (`trusted_access_binding_name` variable, default
  `aksbackuprb`) to allow import of manually created binding `azbkup-trust`. See FTFL-596.

- Adds `outputs.tf` with vault ID, policy ID, instance ID, storage account name/ID, and
  principal IDs — required for restore runbook automation (FTFL-599).

- Adds `versions.tf` with `azurerm >= 3.116.0, < 5.0.0` floor.

- Fixes misleading README (shared_access_key_enabled description was inverted).

## Jira cross-references
- FTFL-615 — Azure Backups private endpoint subnet
- FTFL-596 — Configure Azure Backups module (NNUH & MKUH)
- FTFL-599 — Restore Runbook Update

## Test plan
- [ ] terraform plan shows no unexpected destroys (imports required for CLI-created resources)
- [ ] DNS resolves to private IP from within AKS cluster after PE apply
- [ ] az dataprotection backup-instance show reports ProtectionConfigured
- [ ] Ad-hoc backup job completes with status Completed
- [ ] terraform plan -detailed-exitcode exits 0 after full apply (no drift)

## Gating criteria before merge
- [ ] FTFL-615 subnet ID confirmed from azure-private-infra outputs
- [ ] Hub private DNS zone ID confirmed (or decision made to create standalone zone)
- [ ] Import commands run and verified for pentest-1 manually-created resources
```

---

## 8. Assumptions & Risks

### Assumptions (Verify before aPplying)

| # | Assumption | How to confirm |
|---|---|---|
| A1 | `snet-ff-uks-gp-pe` subnet exists and has `privateEndpointNetworkPolicies = Disabled` | `az network vnet subnet show --query privateEndpointNetworkPolicies` |
| A2 | Hub `privatelink.blob.core.windows.net` DNS zone exists (or decision to create standalone) | `az network private-dns zone list --query "[?name=='privatelink.blob.core.windows.net']"` |
| A3 | The manually created backup instance is named `dailyaksbackup` | `az dataprotection backup-instance list --vault-name aksbackupvault` |
| A4 | azurerm provider in calling workspace is `>= 3.116.0` | TFC workspace provider version or `terraform version` |
| A5 | AKS cluster identity is `kubelet` MSI (system-assigned), not OIDC workload identity | `az aks show --query "identityProfile.kubeletidentity.objectId"` |

### Risks

Drift between CLI and IaC: The pentest-1 environment has resources created out-of-band by `az dataprotection` CLI. Until imports are run, Terraform has no knowledge of them and will attempt to create duplicates or fail on name conflicts (especially the trusted access binding and backup instance). Import commands in Phase 2/3 are mandatory before first apply in any environment with prior CLI work.

RBAC role swap window: Changing the extension MSI role means ~1–2 seconds where no assignment exists. The extension may log transient 403s during this window. Plan the apply outside active backup windows (not around 02:00).

Provider version `4.x` compatibility: In azurerm `4.x`, `azurerm_storage_container` changed from `storage_account_name` to `storage_account_id`. The current code uses `storage_account_id` (line 67) which is the 4.x form—confirm provider version consistency across all stacks consuming this module before setting the floor.

Private endpoint + `network_rules.bypass = AzureServices`: Even with `public_network_access_enabled = false`, the `bypass = ["AzureServices"]` entry is required so that Azure Backup's internal service plane can reach the storage account for health checks. Do not remove it.

Snapshot RG location: Disk snapshots must be in the same region as the disks. `backup_rg_snap.location` must match the AKS node pool region (`uksouth`). If the snap RG is imported (`create_snapshot_resource_group = false`), verify the region before applying.

---

## 9. Diff-Ready Change Summary

```
+ versions.tf                              NEW — provider constraints
+ outputs.tf                              NEW — 9 outputs for downstream stacks

~ variables.tf
  + var.create_private_endpoint            NEW (default false)
  + var.private_endpoint_subnet_id         NEW
  + var.private_dns_zone_id                NEW
  + var.private_dns_zone_vnet_id           NEW
  + var.trusted_access_binding_name        NEW (default "aksbackuprb")

~ main.tf
  + locals.create_private_dns_zone         NEW local
  + locals.effective_private_dns_zone_id   NEW local
  + azurerm_private_dns_zone.blob          NEW (conditional)
  + azurerm_private_dns_zone_virtual_network_link.blob   NEW (conditional)
  + azurerm_private_endpoint.backup_sa     NEW (conditional)
  ~ azurerm_role_assignment.extension_storage_account_permission
      role_definition_name: "Storage Account Contributor"
                          → "Storage Blob Data Contributor"
  ~ azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access
      name: "aksbackuprb" → var.trusted_access_binding_name

~ README.md
  ~ shared_access_key_enabled description corrected (inverted in current text)
```

---

## 10. Pre-Apply Checklist

- [ ] Confirm `snet-ff-uks-gp-pe` subnet ID from azure-private-infra outputs ([FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615))
- [ ] Confirm hub DNS zone resource ID (or decide to create standalone zone in backup RG)
- [ ] Run `terraform import` for vault, extension, trusted access binding, policy, instance in any environment with prior CLI-created resources
- [ ] Verify azurerm provider version `>= 3.116.0` in all consuming workspaces
- [ ] Set `backup_extension_name = "azure-aks-backup"` in pentest-1 calling stack
- [ ] Set `trusted_access_binding_name = "azbkup-trust"` in pentest-1 calling stack
- [ ] Set `backup_included_namespaces` to the 8-namespace list
- [ ] Set `backup_repeating_time_intervals` to a current-year ISO 8601 start date at 02:00 UTC
- [ ] Run `terraform plan`—confirm no unexpected destroys
- [ ] Schedule RBAC role swap apply outside 02:00 backup window
- [ ] After apply: DNS test, extension health check, backup instance state = `ProtectionConfigured`
- [ ] After apply: `terraform plan -detailed-exitcode` exits 0

---

## Related Notes

- [[Azure AKS Private Endpoint Backup]]
- [[Azure Backup for AKS — Full CLI Command Sequence]]
- [[Azure Backup for AKS]]
- [[End-to-End Manual Proof AKS Backup via Private Endpoint]]
- [[Role Assignment Commands for `aksbackupvault` MSI]]
