---
aliases: []
created: 2025-12-21T00:00:00+00:00
modified: 2026-07-13T08:45:09+00:00
permalink: llmeon/30-library/so-t/so-t-azure-backup-and-restore
tags: []
tier: 3-Tactic
title: SoT - Azure Backup and Restore
---

## 2. Core Concepts

### Main Components

| Component | Role/Function |
|:-- |:-- |
| Recovery Services Vault | Stores backup data for most classic workloads (VMs, SQL, SAP, etc.). Central management hub. |
| Backup Vault | Stores backup data for newer workloads (Azure Database for PostgreSQL, Blob Storage, disks). |
| Backup Items | The specific resources being protected (VMs, file shares, databases, etc.). |
| Backup Agents | Tools for on-premises backup or enhanced backup (like MARS Agent, DPM, Azure VM Extension). |
| Backup Policies | Define backup schedule and retention (how often and how long to keep backups). |
| Jobs/Alerts/Reports | Provide status, auditing, and monitoring for backup activities. |

### How it All Fits Together

1. Configure:
    - Choose the resources (VMs, DBs, files, etc.) to back up.
    - Assign them to a vault (Recovery Services or Backup Vault).
    - Set backup policies (schedule and retention).
2. Backup Operation:
    - Azure Backup triggers jobs as per policy (automated or on-demand).
    - Data is deduplicated, compressed, encrypted, and transferred to the vault.
    - Uses incremental backups to save bandwidth/storage after initial backup.
3. Monitoring & Security:
    - Centralized monitoring via Azure Portal, alerts, and audit logs.
    - Data is protected with encryption and Azure RBAC.
    - Geo-redundant or zone-redundant storage for resiliency.
4. Restore:
    - Data can be restored to original or alternate locations.
    - Point-in-time recovery is available for supported workloads.

### Quick Glossary

- MARS Agent: For on-premises or individual file/folder backup.
- DPM/MABS: For advanced, on-premises workloads.
- Azure VM Extension: For agentless VM-level backups in Azure.
- Incremental Backups: Only changed data is backed up after the first full backup.
- GRS/ZRS/LRS: Redundancy options for storing backup copies.

---

## 3. AKS Cluster Backup

Azure Backup provides a native solution for backing up AKS clusters. It requires the installation of a Backup extension in the cluster, which communicates with a Backup vault to perform operations. Backups can be stored in blob containers and include both cluster state and persistent volume snapshots.

### OOP Model for AKS Backup

From an object-oriented programming (OOP) perspective, the architecture for backing up AKS clusters can be modeled as follows:

- BackupVault
    - _Attributes_: storage location, policies, redundancy type, supported clusters
    - _Methods_: addBackup(), restoreBackup(), setPolicy(), getStatus()
    - _Relationships_: Owns and stores BackupInstance objects
- AKSCluster
    - _Attributes_: resourceGroup, subscription, clusterState, persistentVolumes[]
    - _Methods_: registerForBackup(), snapshotVolume(), restoreFromBackup()
    - _Relationships_: Registers with BackupVault for protection
- BackupPolicy
    - _Attributes_: schedule, retentionPeriod, type (Operational/Vault tier), targetResources
    - _Methods_: createPolicy(), updatePolicy(), applyPolicy()
    - _Relationships_: Linked to BackupVault; applied to AKSCluster and volumes
- BackupExtension (Agent/CSI Driver)
    - _Attributes_: version, installedOn
    - _Methods_: initBackup(), captureSnapshot(), pushToVault(), restoreJob()
    - _Relationships_: Installed on AKSCluster; communicates with BackupVault
- BackupInstance
    - _Attributes_: AKSCluster reference, timestamp, recoveryPoint, location (Operational/Vault)
    - _Methods_: startBackup(), viewRecoveryPoint(), deleteBackup(), restore()
    - _Relationships_: Contained _inside_ BackupVault; references AKSCluster
- PersistentVolume
    - _Attributes_: diskType, volumeSize, backupStatus, snapshotId
    - _Methods_: snapshot(), restore(), registerForBackup()
    - _Relationships_: Belongs to AKSCluster; snapshots managed by BackupInstance
- StorageAccount/BlobContainer
    - _Attributes_: redundancy, region, blobs[]
    - _Methods_: storeBackup(), retrieveBackup()
    - _Relationships_: Linked to BackupVault and AKSCluster, holds backup blobs/snapshots

### Typical Flow

1. AKSCluster registers with BackupVault via extension/CSI agent.
2. BackupVault associates a BackupPolicy with the cluster (daily snapshot, retention X days, etc).
3. When backup is triggered (scheduled/on-demand), BackupExtension creates a BackupInstance:
    - Calls AKSCluster methods to snapshot PersistentVolumes.
    - Persists those snapshots in StorageAccount/BlobContainer per policy/tier.
4. Metadata/state/config backups are stored as blobs in the container; disk snapshots as cloud snapshots.
5. Restore: BackupVault directs AKSCluster to recover state/volumes from relevant BackupInstance.

---

## 4. Comparison with Velero

While Azure Backup provides a native, managed solution, Velero is a popular open-source alternative with its own set of trade-offs.

| Feature | Velero (Optimal Usage) | Azure Backup |
|:--- |:--- |:--- |
| Flexibility | Highly flexible, cloud-agnostic, multi-cloud support | Azure-centric, tied to Azure ecosystem |
| Cost | Mainly cloud storage cost; open-source, no license fees | Additional service fees and licensing |
| Kubernetes Native | Yes, designed specifically for Kubernetes backups | Not Kubernetes-native; general VM and disk backup |
| Persistence Layer Support | Supports PVC snapshots & Restic file backups | VM disk backup; limited Kubernetes PVC support |
| Application-Aware Backup | Supports pre/post hooks and application consistency | Generally limited for Kubernetes apps |
| Restore Granularity | Granular resource and namespace-level restores | VM/disk level restore, less granular |
| Multi-Cloud Suitability | Yes, can be used across AWS, Azure, GCP, on-prem | No, Azure-only |

Recommendation: If your primary concern is Kubernetes workload backup flexibility, multi-cloud compatibility, and cost efficiency, Velero used optimally is typically sufficient and more cost-effective than Azure Backup for Kubernetes workloads. However, if you want a fully managed, SLA-backed service tightly integrated with Azure, with less operational overhead but more cost, Azure Backup can complement workloads outside Kubernetes or other Azure resources.

---

## 6. Troubleshooting & Common Issues

### UserErrorMissingVaultMSIReaderPermissionsOnCluster

- Error Message: `UserErrorMissingVaultMSIReaderPermissionsOnCluster: Backup Vault managed identity requires Reader role on the Kubernetes cluster`
- Root Cause: The Backup Vault's Managed Service Identity (MSI) does not have the "Reader" role on the target AKS cluster. This can happen if the cluster has been deleted and recreated, or if the permissions were never granted in the first place.
- Solution: Grant the Backup Vault's MSI the "Reader" role on the AKS cluster.

### Backups Failing for Non-Existent Resources

- Problem: Backups are failing for resources that no longer exist (e.g., a deleted AKS cluster).
- Symptom: Backup jobs fail consistently, and the error messages may indicate that the target resource cannot be found.
- Solution:
    1. Identify and delete the backup instances for the non-existent resources.
    2. Clean up any orphaned resources, such as snapshots, that are associated with the deleted resources. This will also save costs.
    3. Update the backup configuration to target the correct, existing resources.

### Cost Optimization

- Problem: Paying for backups that are not providing value (e.g., failing backups, backups of non-existent resources).
- Recommendations:
    - Regularly review your backup infrastructure to identify and clean up orphaned resources.
    - For non-production environments, consider using Locally-Redundant Storage (LRS) instead of Zone-Redundant Storage (ZRS) for snapshots to save costs.
    - Review retention policies. 7-14 days may be excessive for test environments.

### Security Improvements

- Problem: Poor BCDR (Business Continuity and Disaster Recovery) security score.
- Recommendations:
    - Enable immutability for ransomware protection.
    - Enable Resource Guard protection.
