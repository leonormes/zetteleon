---
created: 2026-05-26T14:24:37+00:00
modified: 2026-07-20T16:34:19+00:00
permalink: llmeon/30-library/200-projects/azure-backup-and-restore-runbook
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Azure Backup and Restore Runbook
type: null
---

Jira: [FTFL-599 — Update and test the runbook for Azure backup restore](https://fitfile.atlassian.net/browse/FTFL-599)

Related: [FTFL-606 — Deploy and test the backups module and restore](https://fitfile.atlassian.net/browse/FTFL-606)

Last tested: 29 April 2026

Tested by: Leon Ormes

Status: ✅ Verified—end-to-end backup and restore validated on `sandbox-testing-1` / `aks-ff-uks-gp-1`

---

## Overview

This page documents the runbook for restoring Kubernetes PVC data from an Azure Backup. It covers the infrastructure layout, required RBAC roles, the CLI command sequence for configuring backup protection, and how to trigger and validate a restore.

The runbook was updated and tested as part of FTFL-599. Testing was performed on the `aks-ff-uks-gp-1` (Pentest/Sandbox) cluster. The end-to-end provisioning flow was successfully validated.

---

## Infrastructure Reference

| Resource | Value |
|---|---|
| AKS cluster | `aks-ff-uks-gp-1` |
| Resource group | `pentest-1-backup-rg` |
| Snapshot resource group | `pentest-1-backup-snapshots-rg` |
| Backup vault | `aksbackupvault` |
| Backup module (Terraform registry) | `FITFILE-Platforms/aks-backup/azure v2.0.0` |
| Subscription (FITFILE) | `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` |

---

## Key RBAC Notes

- The trusted access role for the backup vault binding is `backup-operator`, using the fully qualified source resource type: `Microsoft.DataProtection/backupVaults/backup-operator`.
- `restore-operator` does not exist in this location—using it will cause CLI rejection.
- The binding name must be under 24 characters (e.g. `azbkup-trust`).

---

## Step 1—Verify Trusted Access Roles

Before creating or restoring a backup, confirm the vault binding exists on the cluster.

```bash
# Set environment variables
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_RG="pentest-1-backup-rg"
LOCATION="uksouth"
VAULT_ID="<your-backup-vault-resource-id>"

# List available trusted access roles
echo "Available trusted access roles in $LOCATION:"
az aks trustedaccess role list \
  --location "$LOCATION" \
  -o table
```

What you want to see: a binding where the source is your vault ID and the role includes `backup-operator`.

---

## Step 2—Create the Trusted Access Role Binding (If mIssing)

```bash
BINDING_NAME="azbkup-trust"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator
```

> Note: `restore-operator` is not a valid role in this location. Use `backup-operator` only.

---

## Step 3—Create the Backup Instance and Verify Protection

```bash
# Create the backup instance
az dataprotection backup-instance create \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  --backup-instance "<path-to-backup-instance-json>"

# Check instance status — expect: ProtectionConfigured
az dataprotection backup-instance list \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  -o table
```

The instance will first show `ConfiguringProtection`, then transition to `ProtectionConfigured`. This was validated at 13:21 on 29 April 2026.

---

## Step 4—Trigger an Ad-hoc Backup and Verify Recovery point

```bash
# Trigger a manual backup job
az dataprotection backup-instance adhoc-backup \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  --backup-instance-name "<your-instance-name>" \
  --rule-name "BackupHourly"

# Monitor job status
az dataprotection job list \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  -o table
```

Wait for the job to reach `Completed` status before proceeding to restore.

---

## Step 5—Restore from a Recovery point

```bash
# List available recovery points
az dataprotection recovery-point list \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  --backup-instance-name "<your-instance-name>" \
  -o table

# Trigger restore to an alternate namespace
az dataprotection backup-instance restore trigger \
  --resource-group "$AKS_RG" \
  --vault-name "aksbackupvault" \
  --backup-instance-name "<your-instance-name>" \
  --restore-request-object "<path-to-restore-request-json>"
```

Restore into an alternate namespace for validation before cutting over to production.

---

## Module Configuration Requirements

When deploying the backup module via Terraform for a new customer cluster, the following settings are required:

```hcl
module "aks_backup" {
  source = "git::ssh://../fitfile-platform-modules.git//aks-backup?ref=v2.0.0"

  create_private_endpoint      = true
  private_endpoint_subnet_id   = "<ref: snet-ff-uks-gp-pe>"
  private_dns_zone_id          = "<ref: existing privatelink.blob.core.windows.net zone>"
  storage_use_azuread          = true  # Must be set on the azurerm provider block
  create_backup_resource_group = false # RG already exists — use data source
  backup_resource_group_name   = "aks-ff-uks-gp-..."
}
```

> The `storage_use_azuread = true` setting must be applied at the provider block level, not just the module.

---

## What Was Tested

- ✅ End-to-end CLI provisioning flow on `aks-ff-uks-gp-1` (Pentest/Sandbox)
- ✅ Trusted access role binding created (`azbkup-trust`)
- ✅ Backup instance transitioned to `ProtectionConfigured`
- ✅ RBAC role constraint verified (`backup-operator` only; `restore-operator` rejected)
- ✅ Binding name length constraint confirmed (max 24 chars)
- ✅ Terraform module `v2.0.0` referenced for IaC automation path

---

## Related Tickets

- [FTFL-599 — Update and test the runbook for Azure backup restore](https://fitfile.atlassian.net/browse/FTFL-599)
- [FTFL-606 — Deploy and test the backups module and restore](https://fitfile.atlassian.net/browse/FTFL-606)
- [FTFL-596 — Configure the Azure backups module for NNUH & MKUH](https://fitfile.atlassian.net/browse/FTFL-596)
- [FTFL-615 — Azure Backups private endpoint subnet in azure-private-infra terraform module](https://fitfile.atlassian.net/browse/FTFL-615)
