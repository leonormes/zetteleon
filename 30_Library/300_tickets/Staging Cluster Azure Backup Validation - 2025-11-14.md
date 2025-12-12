---
aliases: []
cluster: staging-cluster-2
confidence: 
created: 2025-11-14T12:11:50Z
date: 2025-11-14
epistemic: 
last_reviewed: 
modified: 2025-12-04T13:27:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: validated
tags: [azure, backup, infrastructure, staging, validation]
title: Staging Cluster Azure Backup Validation - 2025-11-14
type: 
uid: 
updated: 
---

## Azure Backup Validation Summary - Staging Cluster

**Date**: 2025-11-14  
**Cluster**: staging-cluster-2  
**Subscription**: FITCloud Non-Production (249df46b-f75d-4492-8e78-b33a00473548)  
**Status**: ✓ ALL CHECKS PASSED

### Terraform Configuration

**Module**: `app.terraform.io/FITFILE-Platforms/aks-backup/azure` v1.0.5  
**Location**: `main.tf` lines 73-91

```hcl
module "backups" {
  source     = "app.terraform.io/FITFILE-Platforms/aks-backup/azure"
  version    = "1.0.5"

  backup_resource_group_name   = "staging-backup-rg"
  snapshot_resource_group_name = "staging-snapshot-rg"
  storage_account_name         = "stagingbackupsa"
  backup_instance_name         = "stagingaksdaily"
  
  backup_included_namespaces       = ["ff-test-a", "ff-test-b", "ff-test-c", "spicedb"]
  backup_excluded_resource_types   = ["volumesnapshotcontent.snapshot.storage.k8s.io", "secrets"]
  
  kubernetes_cluster_id            = module.azure_public_infrastructure.aks_id
  kubernetes_cluster_name          = module.azure_public_infrastructure.aks_name
  kubernetes_identity_principal_id = module.azure_public_infrastructure.cluster_identity.principal_id
}
```

### 1. Resource Groups

| Resource Group | Status | Location | Provisioning State |
|----------------|--------|----------|-------------------|
| `staging-backup-rg` | ✓ | uksouth | Succeeded |
| `staging-snapshot-rg` | ✓ | uksouth | Succeeded |

### 2. Storage Account

| Property | Value | Status |
|----------|-------|--------|
| Name | `stagingbackupsa` | ✓ |
| Location | `uksouth` | ✓ |
| SKU | `Standard_LRS` | ✓ |
| Kind | `StorageV2` | ✓ |
| Provisioning State | `Succeeded` | ✓ |

### 3. Backup Vault

| Property | Value | Status |
|----------|-------|--------|
| Name | `aksbackupvault` | ✓ |
| Location | `uksouth` | ✓ |
| Identity Type | `SystemAssigned` | ✓ |
| Identity Principal ID | `7fb2a7a0-ec39-4232-b0ab-edc8d6133559` | ✓ |
| Storage Type | `LocallyRedundant (VaultStore)` | ✓ |
| Soft Delete | `On` | ✓ |

### 4. Backup Policy

| Property | Value | Status |
|----------|-------|--------|
| Name | `dailyaksbackups` | ✓ |
| Datasource Type | `Microsoft.ContainerService/managedClusters` | ✓ |
| Backup Type | `Incremental` | ✓ |
| Schedule | Daily at 21:00 UTC (9 PM) | ✓ |
| Retention | 14 days (P14D) | ✓ |
| Datastore | `OperationalStore` | ✓ |

**Schedule Details:**

- Repeating time interval: `R/2024-09-02T21:00:00+00:00/P1D`
- Time zone: UTC
- Backup type: Incremental

### 5. Backup Instance

| Property | Value | Status |
|----------|-------|--------|
| Name | `stagingaksdaily` | ✓ |
| Protection State | `ProtectionConfigured` | ✓ |
| Provisioning State | `Succeeded` | ✓ |
| AKS Cluster | `fitfile-cloud-staging-aks-cluster` | ✓ |
| AKS Resource Group | `fitfile-cloud-staging-rg` | ✓ |
| Policy | `dailyaksbackups` | ✓ |
| Snapshot RG | `staging-snapshot-rg` | ✓ |

#### Namespace Configuration

**Included Namespaces:** ✓ MATCHES TERRAFORM

- `ff-test-a`
- `ff-test-b`
- `ff-test-c`
- `spicedb`

#### Resource Type Filtering

**Excluded Resource Types:** ✓ MATCHES TERRAFORM

- `volumesnapshotcontent.snapshot.storage.k8s.io`
- `secrets`

#### Additional Settings

| Setting | Value |
|---------|-------|
| Include Cluster Scope Resources | `true` |
| Snapshot Volumes | `true` |
| Label Selectors | `[]` (none) |

### 6. IAM Permissions

#### AKS Cluster Identity

**Principal ID**: `6f4cb9a4-cdd5-42af-9d0a-5b8817446af1`

| Role | Scope | Status |
|------|-------|--------|
| Backup Contributor | `aksbackupvault` | ✓ |

#### Backup Vault Identity

**Principal ID**: `7fb2a7a0-ec39-4232-b0ab-edc8d6133559`

| Role | Scope | Status |
|------|-------|--------|
| Reader | `staging-snapshot-rg` | ✓ |
| Disk Snapshot Contributor | `staging-snapshot-rg` | ✓ |
| Data Operator for Managed Disks | `staging-snapshot-rg` | ✓ |

### Validation Results

#### ✓ ALL CHECKS PASSED

The Azure backup configuration for the staging cluster is correctly set up and matches the Terraform `module.backups` configuration in `main.tf`.

#### Key Points

- ✓ All resource groups and storage accounts exist in the correct location (UK South)
- ✓ Backup vault is properly configured with system-assigned identity
- ✓ Backup policy schedules daily incremental backups at 21:00 UTC with 14-day retention
- ✓ Backup instance correctly targets the staging AKS cluster
- ✓ Namespace selection matches Terraform: `ff-test-a`, `ff-test-b`, `ff-test-c`, `spicedb`
- ✓ Resource exclusions match Terraform: `volumesnapshotcontent` and `secrets`
- ✓ All required IAM permissions are properly assigned

### Validation Commands Used

#### Switch to Correct Subscription

```bash
az account set -s "249df46b-f75d-4492-8e78-b33a00473548"
```

#### Verify Resource Groups

```bash
az group show -n "staging-backup-rg" --query "{name:name, location:location, provisioningState:properties.provisioningState}" -o json
az group show -n "staging-snapshot-rg" --query "{name:name, location:location, provisioningState:properties.provisioningState}" -o json
```

#### Verify Storage account

```bash
az storage account show -n "stagingbackupsa" -g "staging-backup-rg" --query "{name:name, location:location, sku:sku.name, kind:kind, provisioningState:provisioningState}" -o json
```

#### Verify Backup Vault

```bash
az dataprotection backup-vault show --resource-group "staging-backup-rg" --vault-name "aksbackupvault" -o json
```

#### Verify Backup Policy

```bash
az dataprotection backup-policy show --resource-group "staging-backup-rg" --vault-name "aksbackupvault" --name "dailyaksbackups" -o json
```

#### Verify Backup Instance

```bash
az dataprotection backup-instance show --resource-group "staging-backup-rg" --vault-name "aksbackupvault" --backup-instance-name "stagingaksdaily" -o json
```

#### Verify IAM Permissions

```bash
# AKS cluster identity on backup vault
az role assignment list --assignee "6f4cb9a4-cdd5-42af-9d0a-5b8817446af1" --scope "/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/staging-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault" -o table

# Backup vault identity on snapshot RG
az role assignment list --assignee "7fb2a7a0-ec39-4232-b0ab-edc8d6133559" --scope "/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/staging-snapshot-rg" -o table
```

### Related Resources

- **AKS Cluster ID**: `/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/fitfile-cloud-staging-rg/providers/Microsoft.ContainerService/managedClusters/fitfile-cloud-staging-aks-cluster`
- **Backup Vault ID**: `/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/staging-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault`
- **Backup Policy ID**: `/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/staging-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupPolicies/dailyaksbackups`
- **Backup Instance ID**: `/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/staging-backup-rg/providers/Microsoft.DataProtection/backupVaults/aksbackupvault/backupInstances/stagingaksdaily`

### Next Steps

- Monitor backup job execution (scheduled for 21:00 UTC daily)
- Verify first successful backup completion
- Test restore procedures periodically
- Review retention policy as cluster usage evolves

---

**Validated by**: Azure CLI  
**Tools used**: `az dataprotection`, `az storage`, `az group`, `az role assignment`  
**Date validated**: 2025-11-14T12:09:38Z
