---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [backup]
title: backing_up_and_restoring_data_in_kubernetes_clusters_on_eks_and_aks
type: 
uid: 
updated: 
version: 
---

## Backing Up and Restoring Data in Kubernetes Clusters on EKS and AKS

This page provides an overview of strategies for backing up and restoring data in Kubernetes clusters on Amazon Elastic Kubernetes Service (EKS) and Azure Kubernetes Service (AKS). It highlights the differences between the platforms and offers best practices for each.

### EKS (AWS)

 Velero: Velero is a popular open-source tool for backing up and restoring Kubernetes cluster resources and persistent volumes. It supports scheduling backups to Amazon S3, providing a centralized backup mechanism for disaster recovery, data migration, and application protection.

 EKS Backup Strategy: EKS backup strategies can include cluster-level backups, node-level backups, data volume backups, control-plane backups, and application-level backups. The choice of strategy depends on specific goals such as disaster recovery or data protection.

 AWS Backup: AWS Backup can also be used to automate and centralize data protection across AWS services, including EKS. It allows for point-in-time recovery of applications.

### AKS (Azure)

 Azure Backup: Azure Backup provides a native solution for backing up AKS clusters. It requires the installation of a Backup extension in the cluster, which communicates with a Backup vault to perform operations. Backups can be stored in blob containers and include both cluster state and persistent volume snapshots.

 Backup Policy Configuration: You can configure backup policies to define retention rules and backup frequency. Azure supports both Operational Tier for frequent backups and Vault Tier for long-term retention with geo-redundancy options.

 Granular Control: AKS backup allows you to choose specific namespaces or entire clusters for backup, providing flexibility in managing your backup strategy.

### Key Differences

| Feature | EKS | AKS |
|---|---|---|
| Backup Tool | Velero, AWS Backup | Azure Backup |
| Storage Backend | Amazon S3 | Azure Blob Storage |
| Frequency | On-demand or scheduled | Scheduled (min 4-hour intervals) |
| Retention Options | Customizable via S3 lifecycle policies | Operational Tier and Vault Tier |

### Best Practices

 Regular Backups: Schedule regular backups to ensure data is consistently protected.

 Retention Policies: Define clear retention policies to manage storage costs and compliance requirements.

 Testing Restores: Regularly test your restore procedures to ensure data integrity and recovery capabilities.

 Security Considerations: Encrypt backup data at rest and in transit to protect against unauthorized access.

Links:

### Understanding Kubernetes Data Types

Before diving into backup solutions, it's important to understand the types of data we need to protect in a Kubernetes cluster:

{status:colour=blue}Kubernetes Objects{status}: These include ConfigMaps, Secrets, CustomResourceDefinitions (CRDs), and other cluster-level resources that define your application's configuration and state.

{status:colour=blue}Persistent Volumes{status}: While your question focuses on configuration and metadata, it's worth noting that any associated persistent volumes should be considered in a comprehensive backup strategy.

### Platform-Agnostic Backup Solutions

#### Velero - The Industry Standard

Velero (formerly Heptio Ark) serves as the primary tool for Kubernetes backup and restoration. It works seamlessly across both EKS and AKS, offering:

## Install Velero CLI

```sh
brew install velero # For macOS
```

## Or

```sh
wget https://github.com/vmware-tanzu/velero/releases/latest/download/velero-linux-amd64.tar.gz # For Linux
```

## Create a Backup of All Resources in the Cluster

`velero backup create my-backup --include-namespaces=`

## Restore to a New Cluster

`velero restore create --from-backup my-backup`

### EKS-Specific Implementation

For EKS clusters, we leverage AWS S3 for backup storage:

## Create an S3 Bucket for Backups

`aws s3 mb s3://my-cluster-backup-bucket`

## Install Velero with AWS Plugins

```sh
velero install
    --provider aws
    --plugins velero/velero-plugin-for-aws:v1.5.0
    --bucket my-cluster-backup-bucket
    --backup-location-config region=us-west-2
    --snapshot-location-config region=us-west-2
    --secret-file ./credentials-velero
```

### AKS-Specific Implementation

For AKS clusters, we utilize Azure Blob Storage:

## Create Azure Storage Account and Container

az storage account create

    --name mystorageaccount

    --resource-group myResourceGroup

    --sku Standard_GRS

## Install Velero with Azure Plugins

velero install

    --provider azure

    --plugins velero/velero-plugin-for-microsoft-azure:v1.5.0

    --bucket my-backup-container

    --secret-file ./credentials-velero

    --backup-location-config resourceGroup=myResourceGroup,storageAccount=mystorageaccount

### Backup Schedule and Retention Strategy

Implement automated backup schedules to ensure regular protection of your data:

## Create a Daily Backup Schedule

```sh
velero schedule create daily-backup
    --schedule="@daily"
    --include-namespaces=
    --ttl 720h # Retain backups for 30 days
```

### Platform Comparison Table

|Feature|EKS|AKS|
|---|---|---|
|Storage Backend|AWS S3|Azure Blob Storage|
|IAM Integration|AWS IAM Roles|Azure Managed Identity|
|Default Retention|No default limit|No default limit|
|Encryption Options|AWS KMS|Azure Storage Service Encryption|

### Best Practices and Recommendations

1. Regular Testing:

## Periodically Test Your Backups by Restoring to a Test Cluster

```sh
velero restore create test-restore
    --from-backup my-backup
    --namespace-mappings source-namespace:test-namespace
```

2. Documentation: Maintain detailed documentation of your backup configuration and restoration procedures:

> Backup Schedule: Daily at midnight
> Retention Period: 30 days
> Storage Location: <s3://my-cluster-backup-bucket>
> Required Permissions: List of IAM roles/permissions
> Restoration Procedure: Step-by-step guide

### Additional Considerations

For enhanced data protection, consider implementing:

1. Git-based configuration management for declarative resources
2. External secrets management (AWS Secrets Manager or Azure Key Vault)
3. Disaster recovery documentation and testing procedures

### Monitoring and Verification

Set up monitoring for your backup processes:

## Check Backup Status

velero backup get

## Verify Backup Contents

velero backup describe my-backup --details

### Useful Links and Documentation
