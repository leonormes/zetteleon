*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:07 PM*
---
Based on your long-term memory from **1:04 PM–1:06 PM today** in Ghostty, plus the earlier AKS backup runbook notes around **12:58 PM**, the diagnosis is now very clean: there’s no new project file context attached here, so this is purely the next CLI fix.

## What changed

You already fixed the **role value** issue.

- Earlier, `restore-operator` was wrong for your CLI/location.
- Your own role listing at **1:00 PM** showed the correct role is just:
  - `backup-operator`

Now the **only blocker** is the **binding name**.

## Root cause

This name is too long:

```bash
azurebackup-trustedaccess
```

AKS says the trusted access role binding name:

- must be **24 chars or fewer**
- can contain only **letters, numbers, or dashes**

`azurebackup-trustedaccess` is **25 characters**, so it fails.

## Use a shorter name

For example:

```bash
BINDING_NAME="azbkup-trust"
```

That is safely under the limit.

## Run this

```bash
BINDING_NAME="azbkup-trust"

az aks trustedaccess rolebinding create \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --name "$BINDING_NAME" \
  --source-resource-id "$VAULT_ID" \
  --roles backup-operator
```

## Then verify it landed

```bash
az aks trustedaccess rolebinding list \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query "[].{Name:name,Source:sourceResourceId,Roles:roles,ProvisioningState:provisioningState}" \
  -o table
```

You want to see:

- `Name` = `azbkup-trust` (or whatever short name you use)
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

## Quick proof

If you want to confirm the original problem numerically:

```bash
echo -n "azurebackup-trustedaccess" | wc -c
```

That should return `25`.

## Smallest possible recovery block

```bash
set -euo pipefail

BINDING_NAME="azbkup-trust"

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

## Bottom line

You’re no longer fighting:

- JSON shape
- snapshot RG RBAC
- wrong trusted access role string

You’re just hitting an AKS naming rule.

Use a shorter binding name like:

```bash
azbkup-trust
```

If you paste the output of the successful `rolebinding create` or the post-create `list`, I can tell you immediately whether you’re clear to run `backup-instance create`.