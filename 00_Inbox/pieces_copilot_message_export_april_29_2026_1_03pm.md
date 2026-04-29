*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:03 PM*
---
Based on your long-term memory from **1:00 PM today**, the cluster had **no trusted access role bindings**, and `az aks trustedaccess role list --location "$LOCATION"` showed **`backup-operator`** as the only backup-vault role available there. The relevant project context/runbook trail also shows the extension was healthy by **11:51 AM** and the vault existed by **12:03 PM**, so this error is just the role name being wrong.

## What went wrong

This part is the problem:

```bash
--roles Microsoft.DataProtection/backupVaults/backup-operator Microsoft.DataProtection/backupVaults/restore-operator
```

Your CLI/location does **not** accept that second value, and from your own role listing at **1:00 PM**, it looks like the correct role to use is simply:

```bash
backup-operator
```

Not the fully-qualified provider string, and not `restore-operator`.

## Use this instead

```bash
BINDING_NAME="azurebackup-trustedaccess"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles backup-operator
```

## Then verify it

```bash
az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "[].{Name:name,Source:sourceResourceId,Roles:roles,ProvisioningState:provisioningState}" \
  -o table
```

You want to see:

- `Source` = your vault ID
- `Roles` = `backup-operator`
- `ProvisioningState` = `Succeeded`

## Then retry validation

```bash
sleep 120

nocorrect az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

If that passes:

```bash
nocorrect az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

## Why this is the right fix

Your own output at **1:00 PM** showed:

- trusted access bindings: **empty**
- available trusted access backup role in `uksouth`: **`backup-operator`**

So the correction is:

| Wrong | Right |
|---|---|
| `Microsoft.DataProtection/backupVaults/restore-operator` | omit it |
| `Microsoft.DataProtection/backupVaults/backup-operator` | `backup-operator` |

## Pasteable block

```bash
set -euo pipefail

BINDING_NAME="azurebackup-trustedaccess"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles backup-operator

az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "[].{Name:name,Source:sourceResourceId,Roles:roles,ProvisioningState:provisioningState}" \
  -o table

sleep 120

nocorrect az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

If you paste the output of the `rolebinding create` or the post-create `list`, I can tell you immediately whether you're clear to run `backup-instance create`.