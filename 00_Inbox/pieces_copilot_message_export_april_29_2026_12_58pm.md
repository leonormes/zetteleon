---
created: 2026-04-29T11:58:51+00:00
modified: 2026-04-29T11:59:53+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 12:58 PM*
---
Based on your long-term memory trail from this morning: the AKS backup extension was **Succeeded at 11:51 AM**, and the backup vault existed by **12:03 PM**. There aren’t any additional project files attached here beyond that runbook/CLI context, so this now looks like a **cluster-side trusted access issue**, not JSON shape or snapshot-RG RBAC.

## What this means

You’ve moved past the earlier blockers:

- bad backup-instance JSON → fixed
- snapshot RG permissions → progressed far enough to hit the next gate

The current blocker is now:

- **the AKS Trusted Access role binding between the cluster and the backup vault is missing or stale**

That’s what this error means:

```text
UserErrorTrustedAccessGatewayReturnedForbidden
The Trusted Access role binding is missing/has gotten removed from the cluster.
```

This often happens if:

- the cluster was stopped/started
- the binding was never created correctly
- the binding exists but is stale/broken

---

## Fastest next step

### 1) Inspect the trusted access bindings

Run this first:

```bash

SUB_ID="${SUB_ID:-7bbc8ae5-1710-48ab-ab83-59b52bd0de1a}"
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_RG="rg-ff-uks-gp-net"
VAULT_NAME="aksbackupvault"
VAULT_RG="pentest-1-backup-rg"
LOCATION="uksouth"

az account set --subscription "$SUB_ID"

VAULT_ID="$(az dataprotection backup-vault show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query id -o tsv)"

echo "VAULT_ID=$VAULT_ID"
echo
echo "Trusted access role bindings on cluster:"
az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "[].{Name:name,Source:sourceResourceId,Roles:roles,ProvisioningState:provisioningState}" \
  -o table

echo
echo "Available trusted access roles in $LOCATION:"
az aks trustedaccess role list \
  --location "$LOCATION" \
  -o table
```

## What you want to see

A binding where:

- `Source` = your vault ID
- roles include Azure Backup/Data Protection roles, typically backup/restore operator roles

---

## 2) If the vault binding is missing, create it

Use this:

```bash
BINDING_NAME="azurebackup-trustedaccess"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator Microsoft.DataProtection/backupVaults/restore-operator
```

Then verify:

```bash
az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "[].{Name:name,Source:sourceResourceId,Roles:roles,ProvisioningState:provisioningState}" \
  -o table
```

Then wait a minute or two:

```bash
sleep 120
```

And retry validation:

```bash
nocorrect az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

---

## 3) If a binding already exists but validate still fails

That usually means the binding is **stale or wrong**.

### Option A — delete and recreate that binding

First list names:

```bash
az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  -o table
```

Then delete the existing vault-related one and recreate it:

```bash
az aks trustedaccess rolebinding delete \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "<existing-binding-name>"
```

Then recreate:

```bash
az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "azurebackup-trustedaccess" \
  --source-resource-id "$VAULT_ID" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator Microsoft.DataProtection/backupVaults/restore-operator
```

---

## 4) If `trustedaccess` commands fail or roles differ on your CLI

Check local help:

```bash
az aks trustedaccess -h
az aks trustedaccess rolebinding create -h
az aks trustedaccess role list --location "$LOCATION" -o table
```

I’d trust the role names returned by your local `role list` over memory.

---

## Important: don’t rerun `create` yet

Only rerun:

```bash
az dataprotection backup-instance create ...
```

**after** `validate-for-backup` succeeds.

---

## Likely status summary

Your sequence now looks like this:

| Stage | Status |
|---|---|
| Extension install | Passed |
| Vault creation | Passed |
| Backup-instance JSON generation | Passed |
| Snapshot RG RBAC | At least partially addressed |
| Trusted access binding | **Current blocker** |

---

## If you want the shortest likely fix

This is the one-liner most likely to unblock you, assuming the binding is missing:

```bash
az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "azurebackup-trustedaccess" \
  --source-resource-id "$(az dataprotection backup-vault show --vault-name "$VAULT_NAME" --resource-group "$VAULT_RG" --subscription "$SUB_ID" --query id -o tsv)" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator Microsoft.DataProtection/backupVaults/restore-operator
```

Then:

```bash
sleep 120
nocorrect az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

If you want, I can turn this into a **single pasteable recovery block** that checks binding existence, recreates it if needed, then retries validate/create.