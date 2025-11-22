---
aliases: []
cluster: prod-1
confidence: 
created: 2025-11-14T12:21:06Z
date: 2025-11-14
epistemic: 
last_reviewed: 
modified: 2025-11-20T10:43:00Z
priority: high
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: investigation-complete
tags: [azure, backup, comparison, infrastructure, investigation, production]
title: Production Backup Investigation - prod1aksdaily - 2025-11-14
type: 
uid: 
updated: 
---

## Production Backup Investigation - prod1aksdaily

**Date**: 2025-11-14  
**Cluster**: prod-1 (fitfile-cloud-prod-1-aks-cluster)  
**Subscription**: FITCloud Production (a448d869-4ec5-4c81-82c5-d6e8fa0ec0df)  
**Investigation Type**: Pre-Terraform Configuration Review

> [!important] Critical Finding
> Production is backing up **ALL namespaces** (entire cluster), while Staging only backs up specific namespaces. This is a significant configuration difference that must be addressed before updating Terraform.

### Investigation Summary

This investigation was conducted to understand the current production backup configuration **before** updating the Terraform code. The goal was to document the existing state to ensure Terraform changes match production requirements.

### 1. Resource Groups

| Resource Group | Status | Location | Notes |
|----------------|--------|----------|-------|
| `prod-1-backup-rg` | ✓ Exists | uksouth | Primary backup resources |
| `prod-1-snapshot-rg` | ✓ Exists | uksouth | Snapshot storage |
| `Fitfile-cloud-production-cluster-snapshots` | ✓ Exists | uksouth | Legacy/alternative snapshot RG? |

> [!note] Additional Snapshot Resource Group
> Found an additional snapshot resource group: `Fitfile-cloud-production-cluster-snapshots`. This may be a legacy resource or used for a different purpose. Needs investigation.

### 2. Storage Account

| Property | Value |
|----------|-------|
| Name | `prod1backupsa` |
| Location | `uksouth` |
| SKU | `Standard_LRS` |
| Kind | `StorageV2` |
| Status | ✓ Provisioned |

**Naming Pattern**: `<cluster-name-no-hyphens>backupsa`

### 3. Backup Vault

| Property | Value |
|----------|-------|
| Name | `aksbackupvault` |
| Location | `uksouth` |
| Identity Type | `SystemAssigned` |
| Identity Principal ID | `ed69f0a8-1346-4a7e-94d1-6af7b6075367` |
| Storage Type | `LocallyRedundant (VaultStore)` |
| Soft Delete | `On` |

**Vault ID**: `/subscriptions/a448d869-4ec5-4c81-82c5-d6e8fa0ec0df/resourceGroups/prod-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault`

### 4. Backup Policy: Dailyaksbackups

| Property | Value |
|----------|-------|
| Name | `dailyaksbackups` |
| Datasource Type | `Microsoft.ContainerService/managedClusters` |
| Backup Type | `Incremental` |
| Schedule | Daily at 21:00 UTC (9 PM) |
| Retention Period | 14 days (P14D) |
| Datastore | `OperationalStore` |
| Time Zone | UTC |

**Schedule Details**:

- Repeating time interval: `R/2024-09-02T21:00:00+00:00/P1D`
- Backup jobs run every day at 21:00 UTC

### 5. Backup Instance: prod1aksdaily

#### Basic Configuration

| Property | Value |
|----------|-------|
| Name | `prod1aksdaily` |
| Protection State | `ProtectionConfigured` |
| Provisioning State | `Succeeded` |
| AKS Cluster | `fitfile-cloud-prod-1-aks-cluster` |
| AKS Resource Group | `fitfile-cloud-prod-1-rg` |
| Backup Policy | `dailyaksbackups` |
| Snapshot Resource Group | `prod-1-snapshot-rg` |

#### Namespace Configuration

> [!warning] All Namespaces Backed Up
> Production is configured to back up **ALL namespaces** in the cluster. This is different from the staging configuration.

| Setting | Value | Impact |
|---------|-------|--------|
| **Included Namespaces** | `[]` (EMPTY) | ⚠️ Backs up **entire cluster** |
| **Excluded Namespaces** | `[]` (EMPTY) | No namespaces excluded |

**What this means**:

- ✓ All application namespaces are backed up
- ✓ All system namespaces (kube-system, kube-public, etc.) are backed up
- ⚠️ Larger backup size compared to selective backup
- ⚠️ Potentially backing up unnecessary system resources
- ⚠️ Higher storage costs
- ✓ More comprehensive disaster recovery capability

#### Resource Type Filtering

**Excluded Resource Types**:

- `volumesnapshotcontent.snapshot.storage.k8s.io`
- `secrets`

**Why these are excluded**:

- VolumeSnapshotContent is handled separately by the snapshot mechanism
- Secrets are sensitive and should be managed through other means (e.g., Key Vault)

#### Additional Settings

| Setting | Value |
|---------|-------|
| Include Cluster Scope Resources | `true` |
| Snapshot Volumes | `true` |
| Label Selectors | `[]` (none) |

### 6. IAM Permissions

#### AKS Cluster Identity

**Principal ID**: `e80e29ae-dced-4ed8-89c8-58fef036254f`

> [!warning] Unusual IAM Configuration
> The AKS cluster identity has **NO explicit role assignments** on the backup vault, yet backups are succeeding consistently. This suggests an alternative permission model or legacy configuration.

**Role Assignments on Backup Vault**: ⚠️ **NONE FOUND**

#### Backup Vault Identity

**Principal ID**: `ed69f0a8-1346-4a7e-94d1-6af7b6075367`

**Role Assignments on Snapshot Resource Group** (`prod-1-snapshot-rg`):

| Role | Purpose |
|------|----------|
| `Reader` | Read access to snapshot RG |
| `Disk Snapshot Contributor` | Create and manage disk snapshots |
| `Data Operator for Managed Disks` | Perform operations on managed disks |

### 7. Backup Job History

#### Recent Performance (Last 14 Days)

**Status**: ✅ **100% Success Rate**

| Date | Start Time (UTC) | Duration | Status |
|------|------------------|----------|--------|
| 2025-11-13 | 21:00:27 | 00:11:18 | Completed |
| 2025-11-12 | 21:00:14 | 00:10:44 | Completed |
| 2025-11-11 | 21:00:08 | 00:10:24 | Completed |
| 2025-11-10 | 21:00:23 | 00:10:26 | Completed |
| 2025-11-09 | 21:00:17 | 00:10:15 | Completed |
| 2025-11-08 | 21:00:24 | 00:10:34 | Completed |
| 2025-11-07 | 21:00:21 | 00:10:16 | Completed |
| 2025-11-06 | 21:00:40 | 00:10:35 | Completed |
| 2025-11-05 | 21:00:24 | 00:10:19 | Completed |
| 2025-11-04 | 21:00:31 | 00:10:25 | Completed |
| 2025-11-03 | 21:00:38 | 00:10:23 | Completed |
| 2025-11-02 | 21:00:32 | 00:12:14 | Completed |
| 2025-11-01 | 21:00:21 | 00:12:26 | Completed |
| 2025-10-31 | 21:00:19 | 00:12:24 | Completed |

#### Performance Metrics

- **Success Rate**: 100% (14/14 jobs)
- **Average Duration**: ~10-12 minutes
- **Most Recent Backup**: 2025-11-13 at 21:00 UTC
- **Backup Window**: Consistent timing around 21:00 UTC
- **Duration Trend**: Stable, no performance degradation

### 8. Comparison: Production Vs Staging

#### Critical Differences

| Aspect | Production | Staging | Impact |
|--------|------------|---------|--------|
| **Namespace Scope** | ⚠️ ALL (empty list) | Specific: `ff-test-a`, `ff-test-b`, `ff-test-c`, `spicedb` | **CRITICAL** - Different backup scope |
| **AKS Identity IAM** | ⚠️ No explicit role on vault | `Backup Contributor` on vault | Unusual but functional |
| **Backup Duration** | ~10-12 minutes | ~10-12 minutes | Similar despite scope difference |

#### Similarities

| Aspect | Configuration |
|--------|---------------|
| **Schedule** | Daily at 21:00 UTC |
| **Retention** | 14 days |
| **Excluded Resource Types** | `volumesnapshotcontent.snapshot.storage.k8s.io`, `secrets` |
| **Backup Type** | Incremental |
| **Storage Redundancy** | Standard_LRS |
| **Soft Delete** | Enabled |
| **Snapshot Volumes** | Enabled |
| **Include Cluster Scope** | Enabled |

### 9. Key Findings

#### ⚠️ Critical Finding: Namespace Scope

**Production backs up the ENTIRE cluster** (all namespaces), while **Staging backs up only specific application namespaces**.

**Production Backup Includes**:

- All application namespaces
- System namespaces (kube-system, kube-public, etc.)
- Infrastructure components
- Platform services
- Everything in the cluster

**Implications**:

- ✓ **Pros**: Complete disaster recovery capability, no missed workloads
- ⚠️ **Cons**: Larger backup size, higher storage costs, potentially unnecessary system data

#### ⚠️ IAM Anomaly

**The AKS cluster identity has no explicit role on the backup vault**, yet backups are succeeding consistently at 100% success rate.

**Possible Explanations**:

1. Using a different permission model (subscription-level roles?)
2. Legacy configuration that still works
3. Permissions inherited from another source
4. Azure Backup service uses alternative authentication

**Risk**: When recreating via Terraform, may need to explicitly add this role assignment.

#### ✅ Operational Health

- Backups are running successfully on schedule
- 100% success rate over the last 14 days
- Consistent ~10 minute backup windows
- No failed or stuck jobs
- System is production-ready and stable

### 10. Recommendations for Terraform Configuration

#### Decision Required: Namespace Strategy

Before updating Terraform, you must decide on the namespace backup strategy:

##### Option A: Keep Backing Up ALL Namespaces (Current Behavior)

```hcl
backup_included_namespaces = []
```

**Pros**:

- ✓ Complete cluster backup
- ✓ No risk of missing workloads
- ✓ Comprehensive disaster recovery
- ✓ No manual updates needed for new namespaces

**Cons**:

- ⚠️ Larger backup size
- ⚠️ Higher storage costs
- ⚠️ Backs up system namespaces (may be unnecessary)
- ⚠️ Longer restore times if only specific namespaces needed

##### Option B: Switch to Selective Namespaces (Like Staging)

```hcl
backup_included_namespaces = [
  "namespace1",
  "namespace2",
  "namespace3",
  # etc.
]
```

**Pros**:

- ✓ Targeted backups (only what you need)
- ✓ Lower storage costs
- ✓ Faster, more focused restores
- ✓ Explicit control over backup scope

**Cons**:

- ⚠️ Must manually add new production namespaces to Terraform
- ⚠️ Risk of forgetting to add critical namespaces
- ⚠️ Doesn't backup system/infrastructure namespaces
- ⚠️ Less comprehensive disaster recovery

#### IAM Configuration

**Action Required**: Investigate the IAM configuration before Terraform changes

1. ✓ Determine why AKS identity doesn't need explicit vault role
2. ✓ Document the actual permission model in use
3. ⚠️ Likely need to add `Backup Contributor` role in Terraform (like staging)
4. ✓ Test IAM changes in staging first
5. ⚠️ Ensure Terraform recreate doesn't break existing backups

#### Storage Account Naming

**Pattern Identified**:

- Production: `prod1backupsa`
- Staging: `stagingbackupsa`
- Format: `<cluster-name-with-no-hyphens>backupsa`

This pattern should be maintained in Terraform configuration.

### 11. Next Steps

#### Before Updating Terraform

- [ ] **Decide on namespace backup strategy** (all vs selective)
- [ ] **Investigate IAM permission model** (why no explicit AKS role needed?)
- [ ] **Determine purpose of legacy snapshot RG** (`Fitfile-cloud-production-cluster-snapshots`)
- [ ] **Review backup costs** (understand impact of all-namespace backup)
- [ ] **Document production namespace list** (if switching to selective)

#### When Updating Terraform

- [ ] Match namespace configuration to business requirements
- [ ] Add explicit IAM role assignments (test in staging first)
- [ ] Maintain storage account naming pattern
- [ ] Preserve retention policy (14 days)
- [ ] Keep backup schedule (21:00 UTC)
- [ ] Maintain exclusions (volumesnapshotcontent, secrets)

#### After Terraform Apply

- [ ] Verify backup instance configuration matches expectations
- [ ] Confirm next scheduled backup runs successfully
- [ ] Validate IAM permissions are correct
- [ ] Check namespace scope is as intended
- [ ] Monitor backup job history for any failures

### 12. Investigation Commands Used

#### Switch Subscription

```bash
az account set -s "a448d869-4ec5-4c81-82c5-d6e8fa0ec0df"
az account show --query "{subscription_id: id, subscription_name: name}" -o table
```

#### Resource Groups

```bash
az group show -n "prod-1-backup-rg" --query "{name:name, location:location, provisioningState:properties.provisioningState}" -o json
az group list --query "[?contains(name, 'prod') && contains(name, 'snapshot')].{name:name, location:location}" -o table
```

#### Storage Account

```bash
az storage account list -g "prod-1-backup-rg" --query "[].{name:name, location:location, sku:sku.name, kind:kind}" -o table
```

#### Backup Vault

```bash
az dataprotection backup-vault show --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" -o json
```

#### Backup Policy

```bash
az dataprotection backup-policy list --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" -o table
az dataprotection backup-policy show --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" --name "dailyaksbackups" -o json
```

#### Backup Instance

```bash
az dataprotection backup-instance list --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" -o table
az dataprotection backup-instance show --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" --backup-instance-name "prod1aksdaily" -o json
```

#### IAM Permissions

```bash
# AKS cluster identity
AKS_ID="/subscriptions/a448d869-4ec5-4c81-82c5-d6e8fa0ec0df/resourceGroups/fitfile-cloud-prod-1-rg/providers/Microsoft.ContainerService/managedClusters/fitfile-cloud-prod-1-aks-cluster"
AKS_PRINCIPAL_ID=$(az resource show --ids "$AKS_ID" --query "identity.principalId" -o tsv)

VAULT_ID="/subscriptions/a448d869-4ec5-4c81-82c5-d6e8fa0ec0df/resourceGroups/prod-1-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault"
az role assignment list --assignee "$AKS_PRINCIPAL_ID" --scope "$VAULT_ID" -o table

# Backup vault identity
VAULT_PRINCIPAL_ID="ed69f0a8-1346-4a7e-94d1-6af7b6075367"
SNAPSHOT_RG_ID="/subscriptions/a448d869-4ec5-4c81-82c5-d6e8fa0ec0df/resourceGroups/prod-1-snapshot-rg"
az role assignment list --assignee "$VAULT_PRINCIPAL_ID" --scope "$SNAPSHOT_RG_ID" -o table
```

#### Backup Jobs

```bash
az dataprotection job list --resource-group "prod-1-backup-rg" --vault-name "aksbackupvault" --query "[].{operation:properties.operation, status:properties.status, startTime:properties.startTime, duration:properties.duration, backupInstanceName:properties.backupInstanceFriendlyName}" -o table
```

### Related Documentation

- [[Staging Cluster Azure Backup Validation - 2025-11-14]] - Comparison baseline
- Azure Resource IDs documented above for quick reference
- Screenshot from Azure Portal included in investigation request

---

**Investigation completed**: 2025-11-14T12:19:42Z  
**Tools used**: Azure CLI (`az dataprotection`, `az storage`, `az group`, `az role assignment`)  
**Status**: ✅ Complete - Ready for Terraform configuration decisions
