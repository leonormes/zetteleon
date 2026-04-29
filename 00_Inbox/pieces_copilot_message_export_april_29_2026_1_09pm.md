*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:09 PM*
---
From your long-term memory trail in Ghostty/Obsidian today between **1:00 PM** and **1:08 PM**, plus the runbook note you had open earlier at **11:48 AM**, and with no extra project files attached here, the pattern is now clear:

## Diagnosis

You’ve actually hit the **third and final syntax correction** for this trusted access binding:

1. **Wrong extra role** → `restore-operator` was invalid for your environment
2. **Binding name too long** → `azurebackup-trustedaccess` exceeded 24 chars
3. **Role format too short** → `backup-operator` alone is also wrong for `create`

Your latest error proves #3:

```text
role must begin with source resource type
```

So the role value must start with:

```text
Microsoft.DataProtection/backupVaults/
```

## Correct command

Use the **short binding name** you already fixed, but the **fully-qualified single role**:

```bash
BINDING_NAME="azbkup-trust"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator
```

## Why this is the right combination

Your earlier attempts established two separate facts:

- At **1:00 PM**, `az aks trustedaccess role list --location "$LOCATION"` showed:
  - `Name = backup-operator`
  - `SourceResourceType = Microsoft.DataProtection/backupVaults`
- At **1:04 PM**, adding `restore-operator` caused CLI parsing failure
- At **1:08 PM**, using only `backup-operator` caused service validation failure because it **must begin with source resource type**

So the valid value is the combination of those two columns:

```text
Microsoft.DataProtection/backupVaults/backup-operator
```

Not:

```text
backup-operator
```

and not:

```text
Microsoft.DataProtection/backupVaults/backup-operator Microsoft.DataProtection/backupVaults/restore-operator
```

## Run this exact recovery block

```bash
set -euo pipefail

BINDING_NAME="azbkup-trust"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles Microsoft.DataProtection/backupVaults/backup-operator

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

## What you want to see

After the `list` command, you want:

| Field | Expected |
|---|---|
| Name | `azbkup-trust` |
| Source | your vault ID |
| Roles | `Microsoft.DataProtection/backupVaults/backup-operator` |
| ProvisioningState | `Succeeded` |

## If create still fails

Run local help to confirm exact argument expectations:

```bash
az aks trustedaccess rolebinding create -h
```

and:

```bash
az aks trustedaccess role list --location "$LOCATION" -o table
```

But based on the sequence in memory up to **1:08 PM**, the most likely correct fix is exactly this:

```bash
--name azbkup-trust
--roles Microsoft.DataProtection/backupVaults/backup-operator
```

## Bottom line

You were between two half-correct versions:

- **short role name** was too short
- **two fully-qualified roles** included an invalid extra one

The correct form is:

```bash
Microsoft.DataProtection/backupVaults/backup-operator
```

with the shorter binding name:

```bash
azbkup-trust
```

Paste the output of that `rolebinding create` if you want, and I’ll tell you immediately whether you’re clear to rerun `backup-instance create`.