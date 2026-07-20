---
created: 2026-04-28T10:30:02+00:00
modified: 2026-07-20T16:33:33+00:00
permalink: llmeon/work/jira/jira-ftfl-596
title: Jira-FTFL-596
---

## FTFL-596: Configure the Azure Backups Module for NNUH & MKUH

Status: In Progress

Assignee: Leon Ormes

Priority: Medium

### Description

We need to configure the backups module for the EoE Data Providers which don't currently have it enabled.

We should have answers to the following before we start this ticket:

1. What is the backup frequency (must be outside of operational hours)
2. What is the backup retention period
3. What is the minimum number of backups to retain?
4. Has cost of backups been factored in to Node costs (including the OMOP data)?
5. Do different PVCs have different backup requirements?
    - If yes, then we need a ticket to modify the azure backups module
6. Will the Terraform service account have access to create/update/delete these resources?
    - If no, need to create a ticket to request each data provider to update the SP's roles.

Backup requirements we already know:

- Any application PVC should be backed up - I.e. our MongoDB, SpiceDB (postgresql), PostgreSQL
- The Hyve OMOP database should be backed up

### Infrastructure Dependencies

- [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615): Azure Backups private endpoint subnet
    - Requirement: Deploy a private endpoints subnet in the `azure-private-infra` terraform module.
    - Reasoning: Necessary for the private endpoint of the storage container used by backups. This is the recommended approach for the Azure backup extension for Kubernetes to write cluster data to the blob container.

### Subtasks

- [ ] FTFL-605: Access the permissions and roles needed by backups and make relevant change requests to customers (Backlog)
- [ ] FTFL-615: Deploy private endpoint subnet for backups (Backlog)
- [ ] FTFL-597: Deploy Azure Backups Module to NNUH (Backlog)
- [ ] FTFL-598: Deploy Azure Backups Module to MKUH (Backlog)

---

### Current State—2026-04-28

#### Verified Facts (Prod Audit Session, 10:56 AM–~12:00 PM)

| Area | Finding |
|:---|:---|
| Policy cadence | Daily at 21:00 UTC; ISO 8601 interval `R/…/PT24H` |
| Retention | P14D (14 days) |
| Instance: includedNamespaces | `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb` |
| Instance: excludedResourceTypes | `volumesnapshotcontent.snapshot.storage.k8s.io`, `secrets` |
| Instance: labelSelectors | `[]` (empty—not used) |
| Instance: snapshotVolumes | `true` |
| Instance: includeClusterScopeResources | `true` |
| Operational store RG | `prod-1-snapshot-v2-rg` |
| Backup jobs | Completed nightly 21:00–21:10 UTC, 2026-04-21 → 2026-04-27 |
| AKS Backup Extension | `microsoft.dataprotection.kubernetes`—ProvisioningState: Succeeded |
| Storage: prod1backupv2sa | PublicNetworkAccess = Enabled; defaultAction = Allow |
| Storage: Private Endpoints | None |
| Blob privatelink DNS zone | Not found in subscription |
| AKS VNet | Managed VNet `aks-vnet-25797305` in node RG `MC_fitfile-cloud-prod-1-rg_…_uksouth`; address space `10.224.0.0/12` |
| AKS Subnets | Single subnet: `aks-subnet` (10.224.0.0/16, PE policies Disabled) |
| Dedicated PE subnet | Does not exist |
| OMOP namespaces in backup? | NO—`thehyve`, `thehyve-cuh`, `thehyve-mkuh` have bound PVCs but are absent from `includedNamespaces` |

#### NNUH-specific Facts

| Area | Finding |
|:---|:---|
| Microsoft.DataProtection provider | Registered ✓ |
| Storage aksffuksgp01backupsa | PublicNetworkAccess = Enabled; no PEs |
| Entra SP role checks | 401 Insufficient Privileges—customer must confirm Terraform SP role assignment |

---

### Delta Plan

#### 1. OMOP Scope Remediation (FTFL-596 / iMmediate)

Recommendation: Option B—append namespaces to `includedNamespaces`.

| | Option A: labelSelectors | Option B: Append namespaces (recommended) |
|:---|:---|:---|
| Mechanism | Add `backup: "enabled"` label to thehyve* namespaces; set `labelSelectors` on instance | Add `thehyve`, `thehyve-cuh`, `thehyve-mkuh` to `includedNamespaces` |
| Pro | Scalable—label new namespaces without touching backup config | Simple Terraform diff; explicit allowlist matches existing pattern |
| Con | `labelSelectors` in AKS Backup filters _resources within_ included namespaces, not namespace selection—misuse risks silent exclusion; requires kubectl label applied before backup runs | Config must be updated for each new namespace |
| Risk | Medium (Azure docs ambiguous on namespace-level label selection) | Low |

With Option B, the corrected `includedNamespaces` list for prod becomes:

```
barts, ff-a, ff-b, ff-c, spicedb, thehyve, thehyve-cuh, thehyve-mkuh
```

#### 2. Cadence / Retention

Keep as-is: Daily 21:00 UTC + P14D. Extending to 30 days or adding weekly backups requires cost approval (Q4 question in FTFL-596).

#### 3. Private Networking (FTFL-615—prerequisite for 597/598)

Required changes, in order:

1. Create `private-endpoints` subnet in the AKS VNet (or a shared hub VNet). Needs a CIDR carved out of available space—`10.224.1.0/24` is a candidate if `aks-subnet` only uses `10.224.0.0/16`—but confirm with network design.
2. Create `azurerm_private_endpoint` for `prod1backupv2sa` (group: `blob`) in that subnet.
3. Create `privatelink.blob.core.windows.net` DNS zone + VNet link to AKS VNet.
4. Set storage network rules: `defaultAction = Deny`, `publicNetworkAccess = Disabled`, `bypass = []`.
5. Optional: PE to Backup Vault only if policy mandates (not currently required by Microsoft for AKS Backup extension, which uses MSI).

#### Checklist Mapped to Tickets

- [ ] FTFL-596—Update `includedNamespaces` to add thehyve, thehyve-cuh, thehyve-mkuh in prod
- [ ] FTFL-605—Confirm Terraform SP roles with NNUH/MKUH (Entra 401 blocks automated check); draft email already sent
- [ ] FTFL-615—Deploy private-endpoints subnet + PE + DNS zone (see Terraform below)
- [ ] FTFL-597—Deploy AKS Backup module to NNUH (after FTFL-615)
- [ ] FTFL-598—Deploy AKS Backup module to MKUH (after FTFL-615)

---

### Terraform Changes

#### Module: aks_backup—scope + Schedule Variables

```hcl
# variables.tf
variable "backup_repeating_time_intervals" {
  description = "ISO 8601 repeating interval for backup schedule (e.g. daily at 21:00 UTC)"
  type        = list(string)
  default     = ["R/2024-04-14T21:00:00+00:00/PT24H"]
}

variable "backup_retention_duration" {
  description = "ISO 8601 duration for backup retention"
  type        = string
  default     = "P14D"
}

variable "backup_included_namespaces" {
  description = "Kubernetes namespaces included in the AKS backup scope"
  type        = list(string)
  default     = []
}

variable "backup_excluded_resource_types" {
  description = "Kubernetes resource types excluded from backup"
  type        = list(string)
  default     = [
    "volumesnapshotcontent.snapshot.storage.k8s.io",
    "secrets",
  ]
}

variable "backup_snapshot_volumes" {
  type    = bool
  default = true
}

variable "backup_include_cluster_scope" {
  type    = bool
  default = true
}
```

```hcl
# prod.tfvars — add thehyve namespaces
backup_included_namespaces = [
  "barts",
  "ff-a",
  "ff-b",
  "ff-c",
  "spicedb",
  "thehyve",
  "thehyve-cuh",
  "thehyve-mkuh",
]
```

```hcl
# nnuh.tfvars — parameterised for NNUH (adjust namespace names as confirmed)
backup_repeating_time_intervals = ["R/2024-04-14T21:00:00+00:00/PT24H"]
backup_retention_duration       = "P14D"
backup_snapshot_volumes         = true
backup_include_cluster_scope    = true
backup_included_namespaces = [
  # TODO: confirm NNUH namespace names matching barts/ff-*/spicedb equivalents
  "spicedb",
  "thehyve",
  "thehyve-nnuh",  # placeholder — confirm with The Hyve
]
```

```hcl
# mkuh.tfvars — parameterised for MKUH
backup_repeating_time_intervals = ["R/2024-04-14T21:00:00+00:00/PT24H"]
backup_retention_duration       = "P14D"
backup_snapshot_volumes         = true
backup_include_cluster_scope    = true
backup_included_namespaces = [
  # TODO: confirm MKUH namespace names
  "spicedb",
  "thehyve",
  "thehyve-mkuh",  # placeholder — confirm with The Hyve
]
```

#### Module: azure-private-infra—PE Subnet + Storage PE + DNS (FTFL-615)

```hcl
# subnet — add to existing VNet module or create standalone
resource "azurerm_subnet" "private_endpoints" {
  name                 = "private-endpoints"
  resource_group_name  = var.vnet_resource_group_name
  virtual_network_name = var.vnet_name
  address_prefixes     = [var.private_endpoints_subnet_cidr]

  # Required for private endpoints
  private_endpoint_network_policies = "Disabled"
}

# Blob private endpoint for backup storage
resource "azurerm_private_endpoint" "backup_storage_blob" {
  name                = "${var.prefix}-backup-storage-blob-pe"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "${var.prefix}-backup-storage-blob-psc"
    private_connection_resource_id = var.backup_storage_account_id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "blob-dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.blob_privatelink.id]
  }
}

# Private DNS zone
resource "azurerm_private_dns_zone" "blob_privatelink" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = var.resource_group_name

  tags = var.tags
}

# Link DNS zone to AKS VNet
resource "azurerm_private_dns_zone_virtual_network_link" "blob_aks_vnet" {
  name                  = "${var.prefix}-blob-aks-vnet-link"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.blob_privatelink.name
  virtual_network_id    = var.aks_vnet_id
  registration_enabled  = false

  tags = var.tags
}

# Lock down storage network access AFTER PE is in place
resource "azurerm_storage_account_network_rules" "backup_storage" {
  storage_account_id = var.backup_storage_account_id

  default_action             = "Deny"
  bypass                     = []
  ip_rules                   = []
  virtual_network_subnet_ids = []

  depends_on = [azurerm_private_endpoint.backup_storage_blob]
}

# Update storage account to disable public access
resource "azurerm_storage_account" "backup" {
  # ... existing config ...
  public_network_access_enabled = false

  network_rules {
    default_action = "Deny"
    bypass         = []
  }
}
```

```hcl
# Variables needed for private-infra module
variable "private_endpoints_subnet_cidr" {
  description = "CIDR for the dedicated private-endpoints subnet"
  type        = string
  # Prod candidate: carve from 10.224.0.0/12 space; confirm with network team
  # e.g. "10.224.1.0/24"
}

variable "backup_storage_account_id" {
  description = "Resource ID of the backup storage account"
  type        = string
}

variable "aks_vnet_id" {
  description = "Resource ID of the AKS VNet to link to the DNS zone"
  type        = string
}
```

---

### Blocked / Needs Customer Action

| Item | Blocker | Action Required |
|:---|:---|:---|
| NNUH Terraform SP roles | Entra 401 on role checks | NNUH to confirm SP has Contributor + required dataprotection roles |
| NNUH/MKUH namespace names | Not yet confirmed | Confirm exact namespace names with The Hyve for OMOP namespaces |
| PE subnet CIDR | Network design not confirmed | Agree CIDR with network team before FTFL-615 apply |

---

### Non-Production Current State—2026-04-28

Subscription: FITCloud Non-Production (`249df46b-f75d-4492-8e78-b33a00473548`)

#### Clusters

| Cluster | RG | PowerState | Backup Extension |
|:---|:---|:---|:---|
| `fitfile-cloud-staging-aks-cluster` | `fitfile-cloud-staging-rg` | Running | `azbkuextension`—Succeeded ✓ |
| `fitfile-cloud-testing-aks-cluster` | `fitfile-cloud-testing-rg` | Running | None |

#### Backup Infrastructure

| Resource | Name | RG |
|:---|:---|:---|
| Backup Vault | `aksbackupvault` | `staging-backup-rg` |
| Backup Policy | `dailyaksbackups` | staging-backup-rg |
| Backup Instance | `stagingaksdaily` | staging-backup-rg |
| Operational Store RG | `staging-snapshot-rg` |—|
| Storage Account | `stagingbackupsa` | `staging-backup-rg` |

Testing cluster has no backup vault, instance, or extension—backups not configured.

#### Policy (Staging)

| Setting | Value |
|:---|:---|
| Cadence | Daily at 21:00 UTC (`R/2024-09-02T21:00:00+00:00/P1D`) |
| Retention | P14D (14 days)—matches prod |

#### Backup Instance Scope (Staging)

| Setting | Value |
|:---|:---|
| `includedNamespaces` | `ff-test-a`, `ff-test-b`, `ff-test-c`, `spicedb` |
| `excludedResourceTypes` | `volumesnapshotcontent.snapshot.storage.k8s.io`, `secrets` |
| `labelSelectors` | `[]` (empty) |
| `snapshotVolumes` | `true` |
| `includeClusterScopeResources` | `true` |

#### OMOP/The Hyve Scope Gap (staging)—CRITICAL

Namespaces with bound PVCs that are NOT in `includedNamespaces`:

| Namespace | PVC | Size | Storage Class | Age |
|:---|:---|:---|:---|:---|
| `omopdb` | `data-omopdb-postgresql-0` | 1000 Gi | default-retain | 140d |
| `omopdb` | `omop-staging-pvc` | 200 Gi | default-retain | 140d |
| `thehyve` | `data-thehyve-postgresql-0` | 20 Gi | default | 362d |
| `thehyve` | `thehyve-reports` | 1 Gi | default | 362d |
| `thehyve-test` | `data-thehyve-postgresql-0` | 32 Gi | default-retain | 36d |
| `thehyve-test` | `thehyve-reports` | 1 Gi | default-retain | 36d |
| `ohdsi` | `data-ohdsi-postgresql-0` | 8 Gi | default-retain |—|

Total unprotected data: ~1.26 TB—predominantly OMOP database content.

#### Backup Job failures—CRITICAL

Every nightly backup has Failed for 10 consecutive days (2026-04-18 → 2026-04-27):

```
Error code:    UserErrorKubernetesBackupClusterIsStopped
Error message: Kubernetes cluster is in stopped state.
Inner detail:  PowerState is set to false.
```

The staging cluster is now `Running` (confirmed 2026-04-28). The cluster was stopped for a period—likely a cost-saving measure—but the backup schedule kept firing and failing against a deallocated control plane. Next backup run tonight (21:00 UTC) should succeed if the cluster remains running.

Action required: Confirm whether staging is routinely stopped/started on a schedule. If so, either:

- Align the backup window to run only when the cluster is guaranteed to be up, or
- Treat staging backup failures as expected during stop windows and update alerting accordingly.

#### Storage Network Posture (Staging)

| Setting | Value |
|:---|:---|
| `PublicNetworkAccess` | Enabled |
| `networkAcls` | null (no rules configured at all) |
| Private Endpoints | None |
| Blob privatelink DNS zone | Not found in subscription |

#### VNet / Subnet Inventory

| Cluster VNet | Address Space | Subnets |
|:---|:---|:---|
| `aks-vnet-32767343` (staging, MC RG) | 10.224.0.0/12 | `aks-appgateway` (10.238.0.0/24), `aks-virtualkubelet` (10.239.0.0/16), `aks-subnet` (10.224.0.0/16) |
| `aks-vnet-65505898` (testing, MC RG) | 10.224.0.0/12 | `aks-appgateway` (10.238.0.0/24), `aks-virtualkubelet` (10.239.0.0/16), `aks-subnet` (10.224.0.0/16) |

No dedicated `private-endpoints` subnet exists on either cluster. `aks-appgateway` and `aks-virtualkubelet` subnets are delegated; `aks-subnet` (PE policies Disabled) is the only candidate.

#### Provider Registration

`Microsoft.DataProtection`—Registered ✓ in non-prod subscription.

---

### Non-Production Delta Plan

#### Priority 0—Stop the Bleeding (Staging Job fAilures)

Confirm the cluster-stopped scenario and decide on backup window alignment or alerting adjustment. No Terraform change needed—cluster is already Running.

#### Priority 1—OMOP Scope Remediation (Staging)

Add to `includedNamespaces` for the staging backup instance:

```hcl
# staging.tfvars
backup_included_namespaces = [
  "ff-test-a",
  "ff-test-b",
  "ff-test-c",
  "spicedb",
  "omopdb",      # 1.2 TB of OMOP data — highest priority
  "thehyve",
  "thehyve-test",
  "ohdsi",       # OHDSI stack, part of OMOP ecosystem
]
```

> Cost note: Adding `omopdb` (1.2 TB PVCs) to snapshotted backup scope will significantly increase storage costs. Flag for cost-approval before apply.

#### Priority 2—Testing Cluster (No bAckup)

Testing does not have a vault or extension. Decide whether testing needs backup at all—likely not for ephemeral test data, but `thehyve-test` has 36d-old PVCs which may have value. Document the explicit decision.

#### Priority 3—Private Networking (Non-prod, Mirrors Prod FTFL-615)

Same pattern as prod required:

1. Carve `private-endpoints` subnet from available address space in the staging VNet (10.224.0.0/12—specific CIDR TBD)
2. Create blob PE to `stagingbackupsa`
3. Create `privatelink.blob.core.windows.net` DNS zone + link to staging VNet
4. Flip `stagingbackupsa` to `defaultAction = Deny`, `publicNetworkAccess = Disabled`

Use the same Terraform module templates as prod (parameterised; see Terraform Changes section above).

#### Non-prod Checklist

- [ ] Immediate—Investigate/confirm staging cluster stop schedule; assess backup window alignment
- [ ] FTFL-596—Add `omopdb`, `thehyve`, `thehyve-test`, `ohdsi` to staging `includedNamespaces` (cost sign-off required for 1.2 TB snapshot delta)
- [ ] Decision—Document whether testing cluster requires backup (thehyve-test PVCs are 36 days old)
- [ ] FTFL-615 (non-prod)—Deploy private-endpoints subnet + PE + DNS for `stagingbackupsa`
- [ ] FTFL-605 (non-prod)—Verify Terraform SP has dataprotection roles in non-prod subscription
