# Manage Azure Kubernetes Service (AKS) backups using Azure Backup - Azure Backup

[Skip to main content](#main)

This browser is no longer supported.

Upgrade to Microsoft Edge to take advantage of the latest features, security updates, and technical support.

[Learn](https://learn.microsoft.com/en-us/)

- [Documentation](https://learn.microsoft.com/en-us/docs/)

   In-depth articles on Microsoft developer tools and technologies

   - [Training](https://learn.microsoft.com/en-us/training/)

      Personalized learning paths and courses

   - [Credentials](https://learn.microsoft.com/en-us/credentials/)

      Globally recognized, industry-endorsed credentials

   - [Q&A](https://learn.microsoft.com/en-us/answers/)

      Technical questions and answers moderated by Microsoft

   - [Code Samples](https://learn.microsoft.com/en-us/samples/)

      Code sample library for Microsoft developer tools and technologies

   - [Assessments](https://learn.microsoft.com/en-us/assessments/)

      Interactive, curated guidance and recommendations

   - [Shows](https://learn.microsoft.com/en-us/shows/)

      Thousands of hours of original programming from Microsoft experts

   Microsoft Learn for Organizations

   [ Boost your team's technical skills](https://learn.microsoft.com/en-us/training/organizations/)

   Access curated resources to upskill your team and close skills gaps.

- 

- 

- 

[ Sign in](#)

## Manage Azure Kubernetes Service backups using Azure Backup

- Article

- 02/28/2024

- 

## In this article

1. [Resource provider registrations](#resource-provider-registrations)

2. [Enable the feature flag](#enable-the-feature-flag)

3. [Backup Extension related operations](#backup-extension-related-operations)

4. [Trusted Access related operations](#trusted-access-related-operations)

5. [Monitor AKS backup jobs completed with warnings](#monitor-aks-backup-jobs-completed-with-warnings)

6. [Next steps](#next-steps)

This article describes how to register resource providers on your subscriptions for using Backup Extension and Trusted Access. Also, it provides you with the Azure CLI commands to manage them.

Azure Backup now allows you to back up AKS clusters (cluster resources and persistent volumes attached to the cluster) using a backup extension, which must be installed in the cluster. AKS cluster requires Trusted Access enabled with Backup vault, so that the vault can communicate with the Backup Extension to perform backup and restore operations.

## Resource provider registrations

- You must register these resource providers on the subscription before initiating any backup and restore operation.

- Once the registration is complete, you can perform backup and restore operations on all the cluster under the subscription.

### Register the Backup Extension

To install Backup Extension, you need to register `Microsoft.KubernetesConfiguration` resource provider on the subscription. To perform the registration, run the following command:

```
az provider register --namespace Microsoft.KubernetesConfiguration

```

The registration may take up to *10 minutes*. To monitor the registration process, run the following command:

```
az provider show --name Microsoft.KubernetesConfiguration --output table

```

### Register the Trusted Access

To enable Trusted Access between the Backup vault and AKS cluster, you must register *TrustedAccessPreview* feature flag on *Microsoft.ContainerService* over the subscription. To perform the registration, run the following commands:

## Enable the feature flag

To enable the feature flag follow these steps:

1. Install the *aks-preview* extension:

   ```
   az extension add --name aks-preview
   
   ```

2. Update to the latest version of the extension released:

   ```
   az extension update --name aks-preview
   
   ```

3. Register the *TrustedAccessPreview* feature flag:

   ```
   az feature register --namespace "Microsoft.ContainerService" --name "TrustedAccessPreview"
   
   ```

   It takes a few minutes for the status to show *Registered*.

4. Verify the registration status:

   ```
   az feature show --namespace "Microsoft.ContainerService" --name "TrustedAccessPreview"
   
   ```

5. When the status shows *Registered*, refresh the `Microsoft.ContainerService` resource provider registration:

   ```
   az provider register --namespace Microsoft.ContainerService
   
   ```

This section provides the set of Azure CLI commands to perform create, update, or delete operations on the Backup Extension. You can use the update command to change compute limits for the underlying Backup Extension Pods.

### Install Backup Extension

To install the Backup Extension, run the following command:

```
az k8s-extension create --name azure-aks-backup --extension-type microsoft.dataprotection.kubernetes --scope cluster --cluster-type managedClusters --cluster-name <aksclustername> --resource-group <aksclusterrg> --release-train stable --configuration-settings blobContainer=<containername> storageAccount=<storageaccountname> storageAccountResourceGroup=<storageaccountrg> storageAccountSubscriptionId=<subscriptionid>

```

### View Backup Extension installation status

To view the progress of Backup Extension installation, use the following command:

```
az k8s-extension show --name azure-aks-backup --cluster-type managedClusters --cluster-name <aksclustername> --resource-group <aksclusterrg>

```

### Update resources in Backup Extension

To update blob container, CPU, and memory in the Backup Extension, use the following command:

```
az k8s-extension update --name azure-aks-backup --cluster-type managedClusters --cluster-name <aksclustername> --resource-group <aksclusterrg> --release-train stable --configuration-settings [blobContainer=<containername> storageAccount=<storageaccountname> storageAccountResourceGroup=<storageaccountrg> storageAccountSubscriptionId=<subscriptionid>] [cpuLimit=1] [memoryLimit=1Gi]

[]: denotes the 3 different sub-groups of updates possible (discard the brackets while using the command)


```

### Delete Backup Extension installation operation

To stop the Backup Extension install operation, use the following command:

```
az k8s-extension delete --name azure-aks-backup --cluster-type managedClusters --cluster-name <aksclustername> --resource-group <aksclusterrg>

```

### Grant permission on storage account

To provide *Storage Account Contributor Permission* to the Extension Identity on storage account, run the following command:

```
az role assignment create --assignee-object-id $(az k8s-extension show --name azure-aks-backup --cluster-name <aksclustername> --resource-group <aksclusterrg> --cluster-type managedClusters --query aksAssignedIdentity.principalId --output tsv) --role 'Storage Blob Data Contributor' --scope /subscriptions/<subscriptionid>/resourceGroups/<storageaccountrg>/providers/Microsoft.Storage/storageAccounts/<storageaccountname> 

```

To enable Trusted Access between Backup vault and AKS cluster, use the following Azure CLI command:

```
az aks trustedaccess rolebinding create \
--resource-group <aksclusterrg> \
--cluster-name <aksclustername> \
--name <randomRoleBindingName> \
--source-resource-id $(az dataprotection backup-vault show --resource-group <vaultrg> --vault <VaultName> --query id -o tsv) \
--roles Microsoft.DataProtection/backupVaults/backup-operator   

```

Learn more about [other commands related to Trusted Access](https://learn.microsoft.com/en-us/azure/aks/trusted-access-feature#trusted-access-feature-overview).

## Monitor AKS backup jobs completed with warnings

When a scheduled or an on-demand backup or restore operation is performed, a job is created corresponding to the operation to track its progress. In case of a failure, these jobs allow you to identify error codes and fix issues to run a successful job later.

For AKS backup, backup and restore jobs can show the status **Completed with Warnings**. This status appears when the backup and restore operation isn't fully successful due to issues in user-defined configurations or internal state of the workload.



For example, if a backup job for an AKS cluster completes with the status **Completed with Warnings**, a restore point will be created, but it might not have been able to back up all the resources in the cluster as per the backup configuration. The job will show warning details, providing the *issues* and *resources* that were impacted during the operation.

To view these warnings, select **View Details** next to **Warning Details**.



Learn [how to identify and resolve the error](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-troubleshoot#aks-backup-extension-installation-error-resolutions).

## Next steps

- [Back up Azure Kubernetes Service cluster](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-backup)

- [Restore Azure Kubernetes Service cluster](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-restore)

- [Supported scenarios for backing up Azure Kubernetes Service cluster](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-backup-support-matrix)

---

## Feedback

## Additional resources

---

Training

---

Documentation

- [Restore Azure Kubernetes Service (AKS) using Azure Backup - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-restore?source=recommendations)

   This article explains how to restore backed-up Azure Kubernetes Service (AKS) using Azure Backup.

- [Azure Kubernetes Service (AKS) backup support matrix - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-backup-support-matrix?source=recommendations)

   This article provides a summary of support settings and limitations of Azure Kubernetes Service (AKS) backup.

- [Quickstart - Configure backup for an Azure Kubernetes Service (AKS) cluster using Azure Backup via Terraform - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/quick-kubernetes-backup-terraform?source=recommendations)

   Learn how to quickly configure backup for a Kubernetes cluster using Terraform.

- [Quickstart - Install Azure Backup extension in an AKS cluster - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/quick-install-backup-extension?source=recommendations)

   In this quickstart, learn how to install the Azure Backup extension in an AKS cluster and get it ready to configure backup.

- [Back up Azure Kubernetes Service (AKS) using Azure CLI - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-backup-using-cli?source=recommendations)

   This article explains how to back up Azure Kubernetes Service (AKS) using Azure CLI.

- [AKS Backup and Recovery - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/operator-guides/aks/aks-backup-and-recovery?source=recommendations)

   Learn how to back up and recover your AKS clusters and their workloads.

- [Tutorial - Enable Vault Tier protection for Azure Kubernetes Cluster (AKS) clusters and restore backups in secondary region using Azure Backup - Azure Backup](https://learn.microsoft.com/en-us/azure/backup/tutorial-restore-aks-backups-across-regions?source=recommendations)

   Learn how to enable Vault Tier protection for AKS clusters and restore backups in secondary region using Azure Backup.

### In this article



Source: <https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-manage-backups>