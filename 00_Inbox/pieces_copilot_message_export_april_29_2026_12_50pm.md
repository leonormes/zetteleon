---
created: 2026-04-29T11:50:59+00:00
modified: 2026-04-29T11:51:47+00:00
title: pieces_copilot_message_export_april_29_2026_12_50pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 12:50 PM_
---

From your long-term memory today, you're past the JSON-shape problem we fixed earlier: by 11:51 AM the AKS backup extension was Succeeded, by 11:59 AM the vault MSI was available, and your working note is [Jira-FTFL-596.md](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-596.md). Relevant project context in this prompt is otherwise sparse, so I'm basing this on the CLI/runbook trail plus the error you just pasted.

## What This Error means

This is now a permissions issue on the snapshot resource group:

- AKS cluster managed identity needs Contributor on the snapshot RG
- Backup vault managed identity needs Reader on the snapshot RG

So the payload is now good enough to validate, but Azure is refusing to proceed because the snapshot target RG permissions are incomplete.

## Important Nuance

Your later terminal activity around 12:26 PM shows you already assigned the vault MSI a Contributor role on the snapshot RG. If that happened after this validation failure, then that part may already be fixed.

That means the most likely remaining gap is:

- AKS cluster identity still missing Contributor on the snapshot RG
- or RBAC propagation delay if you assigned both very recently

Also, separately, your extension install at 11:51 AM explicitly warned that the extension MSI needs Storage Blob Data Contributor on the storage account. That is a different permission plane, and it may be your next blocker after snapshot RG RBAC.

---

## Do This now

### 1) Identify the Principals

```bash
SUB_ID="${SUB_ID:-7bbc8ae5-1710-48ab-ab83-59b52bd0de1a}"
AKS_CLUSTER_NAME="aks-ff-uks-gp-1"
AKS_RG="rg-ff-uks-gp-net"
VAULT_NAME="aksbackupvault"
VAULT_RG="pentest-1-backup-rg"
SNAPSHOT_RG="pentest-1-backup-snapshots-rg"

SNAPSHOT_RG_ID="$(az group show \
  --name "$SNAPSHOT_RG" \
  --subscription "$SUB_ID" \
  --query id -o tsv)"

VAULT_MSI="$(az dataprotection backup-vault show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query identity.principalId -o tsv)"

AKS_IDENTITY_TYPE="$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --subscription "$SUB_ID" \
  --query identity.type -o tsv)"

AKS_PRINCIPAL_ID="$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --subscription "$SUB_ID" \
  --query identity.principalId -o tsv)"

if [[ -z "${AKS_PRINCIPAL_ID:-}" || "${AKS_PRINCIPAL_ID:-null}" == "null" ]]; then
  AKS_UAMI_ID="$(az aks show \
    --name "$AKS_CLUSTER_NAME" \
    --resource-group "$AKS_RG" \
    --subscription "$SUB_ID" \
    --query "keys(identity.userAssignedIdentities)[0]" -o tsv)"
  AKS_PRINCIPAL_ID="$(az identity show \
    --ids "$AKS_UAMI_ID" \
    --query principalId -o tsv)"
fi

echo "SNAPSHOT_RG_ID=$SNAPSHOT_RG_ID"
echo "VAULT_MSI=$VAULT_MSI"
echo "AKS_IDENTITY_TYPE=$AKS_IDENTITY_TYPE"
echo "AKS_PRINCIPAL_ID=$AKS_PRINCIPAL_ID"
```

---

### 2) Grant the Exact Missing Roles on the Snapshot RG

```bash
az role assignment create \
  --assignee-object-id "$AKS_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"

az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "$SNAPSHOT_RG_ID"
```

### If You Already Gave the Vault MSI `Contributor`

If you already ran this around 12:26 PM:

```bash
az role assignment create \
  --assignee-object-id "$VAULT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Contributor" \
  --scope "$SNAPSHOT_RG_ID"
```

then you can skip the Reader assignment, because Contributor includes Reader.

---

### 3) Verify the Assignments Landed

```bash
az role assignment list \
  --scope "$SNAPSHOT_RG_ID" \
  --query "[?principalId=='$AKS_PRINCIPAL_ID' || principalId=='$VAULT_MSI'].{PrincipalId:principalId, Role:roleDefinitionName, Scope:scope}" \
  -o table
```

You want to see:

- AKS principal → `Contributor`
- Vault MSI → `Reader` or `Contributor`

---

### 4) Wait a Few Minutes for RBAC Propagation, then Retry Validation

```bash
sleep 120

nocorrect az dataprotection backup-instance validate-for-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

If that passes, then run:

```bash
nocorrect az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

---

## Likely next Thing to Check after This

Your extension creation output at 11:51 AM said:

> "Please provide extension MSI Storage Blob Data Contributor role on the storage account."

So before/after `create`, verify that too:

```bash
STORAGE_ACCOUNT="stffuksgp1backup"
STORAGE_RG="rg-ff-uks-gp-net"

EXTENSION_MSI="$(az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query aksAssignedIdentity.principalId -o tsv)"

STORAGE_ACCOUNT_ID="$(az storage account show \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$STORAGE_RG" \
  --subscription "$SUB_ID" \
  --query id -o tsv)"

az role assignment list \
  --assignee-object-id "$EXTENSION_MSI" \
  --scope "$STORAGE_ACCOUNT_ID" \
  -o table
```

If missing, grant it:

```bash
az role assignment create \
  --assignee-object-id "$EXTENSION_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ACCOUNT_ID"
```

---

## Short Version

You've cleared the bad JSON stage.
This failure means:

- AKS cluster MSI → needs Contributor on `pentest-1-backup-snapshots-rg`
- Vault MSI → needs Reader on `pentest-1-backup-snapshots-rg`

If you already granted the vault MSI broader access at 12:26 PM, then the missing piece is probably just the AKS cluster identity role assignment plus a short RBAC propagation wait.

If you want, I can turn this into one single pasteable recovery block that includes:

1. identity discovery
2. snapshot RG role assignments
3. extension MSI storage role check
4. validate + create retry
