---
created: 2026-04-30T07:33:45+00:00
modified: 2026-07-20T16:34:19+00:00
permalink: llmeon/30-library/200-projects/azure-backup-for-aks
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Azure Backup for AKS
type: null
---

From yesterday's memory trail in Obsidian/Azure/Jira—and with no extra workspace files attached in project context—the clean end-state was:

you built a private Azure Backup for AKS path for `aks-ff-uks-gp-1`, proved it worked end-to-end in the Testing subscription, and identified the exact components Terraform/runbooks now need to reproduce.

## What We Created, and why

| Component                                        | What we created                                                                                          | Why it exists                                                                                                                                                             |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Private backup storage                       | Storage account `stffuksgp1backup` + blob container `aks-backups`                                        | This is where AKS backup data lands. It was hardened so backup data does not rely on public internet access.                                                          |
| Private network path to storage              | Dedicated PE subnet `snet-ff-uks-gp-pe` (`10.0.0.96/27`) + private endpoint `pe-stffuksgp1backup-blob`   | This gives the storage account a private blob endpoint inside the VNet, which is the core of the "private backup" design.                                             |
| Private name resolution                      | Private DNS zone for `privatelink.blob.core.windows.net`, VNet link, and A record for `stffuksgp1backup` | Without this, clients in the VNet would still resolve the storage account to its public address. This makes the blob FQDN resolve to the private IP instead.              |
| Backup control plane                         | Backup vault `aksbackupvault` in `pentest-1-backup-rg`                                                   | Azure Backup needs a vault to own policy, protection state, jobs, and recovery metadata.                                                                                  |
| Snapshot landing zone                        | Snapshot resource group `pentest-1-backup-snapshots-rg`                                                  | AKS PV backup uses snapshots for Azure Disks, so Azure needed a place to store those snapshot resources.                                                                  |
| AKS-side backup agent                        | AKS extension `azure-aks-backup` (`Microsoft.DataProtection.Kubernetes`)                                 | This is the cluster-side integration that lets Azure Backup actually discover and protect Kubernetes resources/PVs.                                                       |
| Backup policy                                | Policy `dailyaksbackups`                                                                                 | This defines the schedule/retention used by the vault for the cluster backup. Final portal state showed daily at 2:00 AM UTC with 14-day retention.               |
| Trust relationship between vault and cluster | Trusted access role binding `azbkup-trust` using `Microsoft.DataProtection/backupVaults/backup-operator` | This is what allows the backup vault to act against the AKS cluster. It turned out to be a required explicit dependency, not just "nice to have."                         |
| RBAC wiring                                  | Role assignments for the vault MSI, AKS cluster MSI, and extension MSI                                   | These permissions were required so the vault/cluster/extension could write to storage, create snapshots, and validate protection.                                         |
| Protected workload definition                | Backup instance for `aks-ff-uks-gp-1`                                                                    | This is the actual object that says "protect this cluster with this policy and this scope." It bound the cluster to the vault/policy and moved to `ProtectionConfigured`. |

---

## The Final Architecture, in Plain English

### 1. A Hardened Storage Target

By around 10:08 AM, you had created the backup storage account `stffuksgp1backup` with the important security posture:

- public network access disabled
- default network action deny
- TLS 1.2
- no public blob access

Why: backup data should sit behind private networking, not be reachable over the public storage endpoint.

---

### 2. A Private Endpoint Path to that Storage

By 10:28 AM you had the dedicated private-endpoint subnet in place, and by 10:48 AM you had created the private endpoint for blob plus the DNS plumbing.

That consisted of:

- `snet-ff-uks-gp-pe`
- blob private endpoint for `stffuksgp1backup`
- private DNS zone for `privatelink.blob.core.windows.net`
- VNet link
- A record resolving the storage account to `10.0.0.100`

Then by 11:03 AM you verified DNS from inside the VNet/cluster path and confirmed the storage account resolved privately.

Why: this is the actual "private backup" part. The extension can talk to blob storage over the VNet instead of traversing a public endpoint.

---

### 3. The Azure Backup Vault

By 12:03 PM, the backup vault `aksbackupvault` existed in `pentest-1-backup-rg`.

Why: the vault is Azure Backup's control plane object. It owns:

- backup policies
- backup instances
- jobs
- protection state
- recovery points

You can see that final vault state in [aksbackupvault overview](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/BackupVaults/aksbackupvault/overview) and later in the more detailed [vault/backup instance portal view](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/GenericBackupInstanceDashboardBlade/id/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Faksbackupvault%2FbackupInstances%2Faks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5/dataSourceType/AzureKubernetesServices/friendlyname/aks-ff-uks-gp-1%2Faks-ff-uks-gp-1-backup/isInCRRContext~/false).

---

### 4. The AKS Backup Extension

By 11:51 AM, the `azure-aks-backup` extension was healthy on `aks-ff-uks-gp-1`.

Why: Azure Backup for AKS is not just a vault-side config. The cluster needs the Microsoft Data Protection extension installed so Azure can interact with Kubernetes resources and persistent volumes.

This is the cluster integration point.

---

### 5. The Snapshot Resource Group

You also created `pentest-1-backup-snapshots-rg`.

Why: because persistent volume protection for Azure Disk-backed PVs needs a resource group where snapshots can be created and managed. This is separate from the vault itself.

So conceptually there were two storage layers:

1. Blob container for backup metadata/cluster backup content
2. Snapshot RG for Azure Disk snapshot operations

---

### 6. The Policy

You created the `dailyaksbackups` policy.

The final portal state later in the day showed:

- frequency: every day at 2:00 AM UTC
- retention: 14 days

That's visible in [dailyaksbackups policy](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/GenericPolicyDashboardBlade/PolicyId/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Faksbackupvault%2FbackupPolicies%2Fdailyaksbackups/dataSourceType/AzureKubernetesServices).

Why: the vault needs a reusable schedule + retention definition before you can configure protection on the cluster.

---

### 7. The Trust + Permission Model

This was a real part of the final solution, not incidental setup.

You ended up with these required permission components:

- AKS cluster managed identity → `Contributor` on the snapshot RG
- Backup vault managed identity → access on the cluster/snapshot scope as required for validation/protection
- Extension MSI → `Storage Blob Data Contributor` on `stffuksgp1backup`
- Trusted access role binding `azbkup-trust` between cluster and vault using
  `Microsoft.DataProtection/backupVaults/backup-operator`

The trusted access binding was successfully in place by 1:12 PM.

Why: Azure Backup for AKS is a multi-identity workflow:

- the extension needs to write to blob
- the cluster identity needs to create/manage snapshots
- the vault needs authority to coordinate backup operations against the cluster

This permission model is one of the main outputs you now need to encode into Terraform.

---

### 8. The Backup Instance

By 1:21 PM, you created the backup instance and it reached `ProtectionConfigured`.

That backup instance bound together:

- cluster: `aks-ff-uks-gp-1`
- vault: `aksbackupvault`
- policy: `dailyaksbackups`
- snapshot RG: `pentest-1-backup-snapshots-rg`
- storage account/container: `stffuksgp1backup` / `aks-backups`

Scope included:

- namespaces: `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`, `thehyve`, `thehyve-cuh`, `thehyve-mkuh`
- cluster-scoped resources
- secrets
- persistent volumes
- Azure Disks / snapshot volumes

That final configuration is visible in [backup instance configuration](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/AzureKubernetesBackupInstanceConfigurationBlade/clusterName/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Faksbackupvault%2FbackupInstances%2Faks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5/excludedNamespaces~/null/includedNamespaces~/%5B%22barts%22%2C%22ff-a%22%2C%22ff-b%22%2C%22ff-c%22%2C%22spicedb%22%2C%22thehyve%22%2C%22thehyve-cuh%22%2C%22thehyve-mkuh%22%5D/includedResourceTypes~/null/excludedResourceTypes~/null/labelSelectors~/null/includeClusterScopeResources~/true/snapshotVolumes~/true/includedVolumeTypes~/null/backupHookReferences~/null).

Why: this is the actual "turn protection on" resource. Everything else was scaffolding for this.

---

## What the Work Achieved

By the end of the day, you had proved three things:

1. The storage path is private
   - DNS resolved the blob endpoint to the private IP, not public internet.

2. The cluster is actually under protection
   - the backup instance reached `ProtectionConfigured` by 1:21 PM.

3. A real recovery point exists
   - later portal state showed a restore point for the cluster, expiring May 13, which proves it wasn't just configured—it actually backed up.

You can see that operational end-state in:

- [backup jobs](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/JobDetailsBlade/jobId/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Faksbackupvault%2FbackupJobs%2Faf9a0d80-1fc0-41fa-b626-74dbc72368a4/subtitle/aks-ff-uks-gp-1%2Faks-ff-uks-gp-1-backup/isCrrContext~/false)
- [backup instance JSON view](https://portal.azure.com/#view/Microsoft_Azure_DataProtection/GenericBackupInstanceDashboardBlade/id/%2Fsubscriptions%2F7bbc8ae5-1710-48ab-ab83-59b52bd0de1a%2FresourceGroups%2Fpentest-1-backup-rg%2Fproviders%2FMicrosoft.DataProtection%2FbackupVaults%2Faksbackupvault%2FbackupInstances%2Faks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5/dataSourceType/AzureKubernetesServices/friendlyname/aks-ff-uks-gp-1%2Faks-ff-uks-gp-1-backup/isInCRRContext~/false)

---

## The short Version

If you want the cleanest possible summary:

We created:

1. a hardened backup storage account and container
2. a private endpoint subnet + blob private endpoint
3. private DNS so the storage account resolves privately inside the VNet
4. an Azure Backup vault
5. a snapshot resource group for PV snapshots
6. the AKS backup extension on the cluster
7. the policy `dailyaksbackups`
8. the required RBAC assignments and trusted access binding
9. the AKS backup instance itself

Why:

To make AKS backups work privately, with no public storage path, while protecting the selected namespaces, secrets, cluster-scoped resources, and Azure Disk-backed persistent volumes—and to turn that validated manual sequence into the basis for FTFL-596 / FTFL-599 / FTFL-615 Terraform and runbook updates.

If you want, I can turn this into a Jira-ready "components created / rationale / next IaC actions" comment next.
