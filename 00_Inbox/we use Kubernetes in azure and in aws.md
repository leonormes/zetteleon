---
created: 2026-05-02T19:38:13+00:00
modified: 2026-05-02T20:40:35+00:00
title: we use Kubernetes in azure and in aws
---

Okay, let's explore some Kubernetes-native options for backing up Persistent Volumes (PVs) in your Azure and AWS environments, steering clear of cloud-provider-specific products.

The most prominent open-source, Kubernetes-native tool for this purpose is Velero.

## ---

Velero

Velero (formerly Heptio Ark) is an open-source tool designed to safely back up and restore, perform disaster recovery, and migrate Kubernetes cluster resources and persistent1 volumes.2 It's a Cloud Native Computing Foundation (CNCF) project and is widely adopted in the community.3

How it Works for PVs:

- Snapshots (Default and Preferred for many cases): Velero can integrate with your underlying storage provider (via CSI \- Container Storage Interface \- drivers) to take snapshots of your PVs.4
  - For Azure Disk, this would typically involve the Azure Disk CSI driver.
  - For AWS EBS, this would involve the AWS EBS CSI driver.5
  - Velero itself orchestrates the snapshotting process, but the actual snapshot is created by the storage system. The snapshot data usually remains in the same storage system initially.
- Filesystem Backup (Restic or Kopia Integration): If your storage provider doesn't have a native snapshot capability, or you want to back up data at the file level (which can be useful for moving data between different storage types or for more granular control), Velero integrates with tools like Restic and Kopia.6
  - These tools work by deploying a pod that mounts the PV and then copies the data, file by file, to a backup storage location (like an S3 bucket on AWS, Azure Blob Storage, or any S3-compatible object store).
  - This method is generally more storage-agnostic but can be slower and more resource-intensive than native snapshots.
- CSI Snapshot Data Movement: This is a newer Velero feature that combines the efficiency of CSI snapshots with the flexibility of filesystem backups. It first takes a CSI snapshot and then uses Restic/Kopia to move the data from that snapshot to an offsite backup storage location.7 This can be a good compromise for performance and data portability.

Key Features Relevant to Your Needs:

- Kubernetes-Native: Operates using Custom Resource Definitions (CRDs) and integrates deeply with the Kubernetes API.8
- Cloud Agnostic (for backup storage): While it uses cloud provider CSI drivers for snapshots, the backup _target_ (where the backup metadata and filesystem backups are stored) can be an object store on any cloud (e.g., AWS S3, Azure Blob Storage, MinIO on-premises).9 This gives you flexibility in where you store your backups.
- Resource Filtering: You can back up entire clusters, specific namespaces, or resources selected by labels.10 This allows you to target specific applications and their PVs.
- Scheduled Backups: You can define schedules for regular backups.11
- Hooks: Pre and post-backup hooks allow you to run custom commands or scripts (e.g., to quiesce a database before backup).12
- Migration Capabilities: Velero is also excellent for migrating resources and PVs between clusters, which can be useful in multi-cloud scenarios.13

Considerations for Azure and AWS:

- CSI Drivers: Ensure you have the appropriate CSI drivers installed and configured in your AKS (Azure Kubernetes Service) and EKS (Amazon Elastic Kubernetes Service) clusters. These drivers allow Kubernetes to interact with the underlying storage (Azure Disk, AWS EBS).14
- Backup Storage Location: You'll need to set up an object storage location (e.g., an S3 bucket in AWS or an Azure Blob Storage container) for Velero to store its backup metadata and, if using Restic/Kopia, the actual PV data.15 You can choose to store backups in the same cloud as the cluster or a different one for disaster recovery purposes.
- Permissions: Velero will need appropriate permissions to interact with your Kubernetes clusters and the chosen backup storage location.16

## ---

Other Open Source Considerations

While Velero is the most common Kubernetes-native, cloud-agnostic tool, some storage solutions themselves offer backup capabilities:

- OpenEBS: If you are using OpenEBS as your storage solution within Kubernetes, it has its own mechanisms for backup and restore, often integrating with Velero as well for a comprehensive solution.17 OpenEBS can create backups of entire deployments, pods, and PVs. It aims to provide a storage layer that is independent of the underlying cloud provider.
- Longhorn: Another CNCF project, Longhorn is a distributed block storage system for Kubernetes.18 It provides built-in backup to an external backup target (like NFS or S3-compatible storage) and can create recurring snapshots and backups.19 It supports cross-cluster recovery.

## ---

General Strategy for Cross-Cloud PV Backup

1. Choose your Tool: Velero is a strong candidate given your requirements.
2. Standardise on CSI: Utilise CSI drivers in both your Azure and AWS clusters. This provides a standard interface for storage operations.
3. Select a Backup Storage Target: Decide where your backups will reside. This could be:
   - An S3 bucket in AWS.
   - Azure Blob Storage.
   - A third-party S3-compatible object store.
   - For cross-cloud DR, you might back up an Azure cluster's PVs to AWS S3, and an AWS cluster's PVs to Azure Blob, or both to a third location.
4. Configure Velero:
   - Install Velero in each cluster.
   - Configure it with the appropriate plugins for your cloud providers (e.g., velero-plugin-for-aws, velero-plugin-for-microsoft-azure).20 These plugins enable Velero to interact with the native snapshot capabilities of EBS and Azure Disk.
   - Point Velero to your chosen backup storage location.
   - If you need filesystem-level backups for certain PVs or for portability between fundamentally different storage types, enable and configure the Restic or Kopia integration.
5. Define Backup Schedules and Policies: Determine what to back up (specific namespaces, applications via labels), how often, and your retention policies.
6. Test Regularly: Crucially, regularly test your restore procedures to ensure your backups are viable and you can meet your Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO). Test restores within the same cluster, to a different cluster in the same cloud, and, if part of your strategy, to a cluster in the other cloud.

By focusing on tools like Velero and leveraging the CSI standard, you can achieve a more cloud-agnostic approach to backing up your PV data across Azure and AWS Kubernetes environments.
