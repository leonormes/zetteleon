---
aliases: []
confidence: 
created: 2025-11-07T16:40:50Z
epistemic: 
last_reviewed: 
modified: 2025-11-07T17:01:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [action-required, azure, backup, cost-optimization, infrastructure, investigation]
title: Azure Backup Investigation - 2025-11-07
type: 
uid: 
updated: 
---

## Azure Backup Investigation Report

**Date**: 2025-11-07
**Subscription**: 249df46b-f75d-4492-8e78-b33a00473548 (FITCloud Non-Production)
**Resource Group**: AzureBackupRG_uksouth_1

---

### Executive Summary

Backup infrastructure is **failing consistently** and **costing money** while protecting resources that **no longer exist**. Main issue: **permissions problem** failing for 2+ weeks.

---

### Critical Issues

#### 1. Failing AKS Backup - PRIMARY ISSUE

- **Backup Instance**: `Fitfile-cloud-test-aks-cluster\staging-aks-daily-everything`
- **Status**: ❌ Failing since **October 24, 2025**
- **Failure Rate**: 12 consecutive failures (100%)
- **Last Successful Backup**: **August 27, 2024** (2+ months ago)

**Root Cause**:

```sh
Error: UserErrorMissingVaultMSIReaderPermissionsOnCluster
Message: Backup Vault managed identity requires Reader role on the Kubernetes cluster
```

**The Problem**:
- Backup vault MSI (ID: `21ddeb8d-d52d-415e-83d1-8545d54638ee`) lacks Reader permissions on target AKS cluster
- **Resource group `Fitfile-cloud-test-rg` DOES NOT EXIST** - cluster has been deleted!

---

### Infrastructure Status

#### Backup Vault: `akstesttemp`
- Location: UK South
- Storage: Locally Redundant
- Security Score: **None** (Poor BCDR security)
- Soft Delete: Enabled (14 days)

#### Backup Instances (3 total)

1. **fitfile-cloud-test-aks-cluster** (test)
- Status: ❌ BackupsSuspended
- Policy: `akktestbackup` (every 4h, 7d retention)

2. **Fitfile-cloud-test-aks-cluster** (staging)
- Status: ❌ ProtectionConfigured but **FAILING**
- Policy: `nonproddailyeverything` (daily, 7d retention)
- **⚠️ THIS IS THE FAILING ONE**

3. **Fitfile-cloud-development-aks-cluster**
- Status: ❌ BackupsSuspended
- Policy: `aksdevelopmentpolicy` (daily, 14d retention)

#### VM Restore Point Collections (2)
- `sonarqube-ubuntu` - ✅ VM exists
- `sonarqube` (old VM) - May not exist

---

### Storage Costs

#### Snapshots: 93 Total
- All using **Standard ZRS** (Zone-Redundant Storage)
- Created: August 22-27, 2024
- **Last snapshot**: August 27, 2024
- Sizes: Mix of 8GB and 64GB disks
- ⚠️ **Snapshots are from defunct AKS cluster that no longer exists**

#### Current AKS Clusters (NOT Being Backed up)
- `fitfile-cloud-testing-aks-cluster` in `fitfile-cloud-testing-rg`
- `fitfile-cloud-staging-aks-cluster` in `fitfile-cloud-staging-rg`

---

### Permissions Analysis

Backup vault managed identity has:

- ✅ Data Operator for Managed Disks (on AzureBackupRG_uksouth_1)
- ✅ Disk Backup Reader (on AzureBackupRG_uksouth_1)
- ✅ Disk Snapshot Contributor (on AzureBackupRG_uksouth_1)
- ✅ Storage Blob Data Reader/Contributor (on tempakstest)
- ❌ **MISSING: Reader role on AKS cluster** - Causing all failures

---

### Cost Implications

**Paying for**:
1. Backup Vault - ongoing storage costs
2. 93 Snapshots using Zone-Redundant Storage
3. Storage Account (`tempakstest` - RAGRS)
4. Failed backup job attempts

**Getting**:
- ❌ No current backups (last success: Aug 27, 2024)
- ❌ Outdated recovery points
- ❌ No protection for current production AKS clusters

---

### Recommendations

#### Immediate Actions (High Priority)

1. **Decide backup strategy**:
- **Option A**: Delete all backup infrastructure if not needed
- **Option B**: Fix permissions and update to backup current clusters

2. **If keeping backups (Option B)**:
- Delete backup instance for non-existent cluster
- Update backup to target actual AKS clusters:
 - `fitfile-cloud-staging-aks-cluster`
 - `fitfile-cloud-testing-aks-cluster`
- Grant Reader role to backup vault MSI on new clusters

3. **Clean up orphaned resources**:
- Delete 93 snapshots from deleted cluster (💰 save significant )
- Remove restore point collections for non-existent VMs
- Review need for `tempakstest` storage account

#### Cost Optimization
- Switch from Zone-Redundant to Locally Redundant snapshots
- Review retention policies (7-14 days may be excessive for test environments)
- Downgrade storage account from RA-GRS if geo-redundancy not needed

#### Security Improvements
- Improve BCDR security score (currently "Poor")
- Consider enabling immutability for ransomware protection
- Enable Resource Guard protection

---

### Summary

Backup infrastructure that:

- ✅ Has correct permissions on backup resource group
- ❌ **Cannot access** the cluster it's trying to backup
- ❌ Is targeting a **deleted** AKS cluster
- ❌ Has been **failing for 2+ weeks**
- ❌ Is **NOT** backing up current production clusters

**Recommendation**: Clean up this infrastructure and start fresh with proper backups for current clusters, or remove entirely if backups aren't needed for test environments.
SUCCESS! All 93 Snapshots Deleted

Summary

Final snapshot count in AzureBackupRG_uksouth_1: 0

All 93 orphaned snapshots from the deleted fitfile-cloud-test-aks-cluster have been successfully removed!

What Was Done

1. ✅ Verified correct Azure subscription (FITCloud Non-Production)
2. ✅ Created deletion manifest: snapshot-ids-2025-11-07.txt (93 IDs)
3. ✅ Created audit trail: snapshot-audit-2025-11-07.tsv (full metadata)
4. ✅ Confirmed no resource locks blocking deletion
5. ✅ Deleted all 93 snapshots in parallel (8 concurrent operations)
6. ✅ Waited for all deletions to complete
7. ✅ Verified zero snapshots remaining

Cost Savings

-  Eliminated: Zone-Redundant Storage (ZRS) costs for 93 snapshots
-  Stopped: Ongoing storage charges for orphaned backup data from August 2024
-  Billing: Cost savings will reflect in next billing cycle

Audit Files Preserved

Both files saved to your home directory for compliance:

-  snapshot-ids-2025-11-07.txt (16K) - Resource IDs
-  snapshot-audit-2025-11-07.tsv (25K) - Complete metadata

Next Steps Recommended

Based on your investigation report, you should consider:

1. Delete backup vault akstesttemp if no longer needed
2. Remove backup instances for the deleted clusters (3 instances)
3. Set up proper backups for current production clusters:
◦ fitfile-cloud-testing-aks-cluster
◦ fitfile-cloud-staging-aks-cluster
4. Review storage account tempakstest (RAGRS) - may no longer be needed

The memory has been saved to Pieces for future reference!
