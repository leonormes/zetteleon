*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 12:00 PM*
---
## All Three Steps Succeeded ✅

Everything landed cleanly:

| Resource | Name | Status |
|---|---|---|
| Resource Group | `pentest-1-backup-rg` | `Succeeded` |
| Backup Vault | `aksbackupvault` | `Succeeded` |
| Vault MSI | `18bd104a-e5fb-4c8c-8abc-55e739ce600f` | Captured |

One housekeeping note: the deprecation warning about `--type` → `--mi-system-assigned` is non-blocking but worth updating in your runbook for future runs.

---

## Next: Role Assignments (Step 4)

You have **two MSIs** that need roles now:

### A) Extension MSI → Storage Blob Data Contributor on the storage account
This was flagged when you installed the extension at ~11:51 AM — the CLI told you to grant it.

```bash
EXTENSION_MSI="67825eb3-72bf-44d0-89ae-ef85726fb25f"
STORAGE_ACCOUNT_ID=$(az storage account show \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$STORAGE_RG" \
  --query id -o tsv)

az role assignment create \
  --assignee "$EXTENSION_MSI" \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ACCOUNT_ID"
```

### B) Vault MSI → Roles on the AKS cluster

```bash
AKS_ID=$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query id -o tsv)

# Reader on the AKS cluster
az role assignment create \
  --assignee "$VAULT_PRINCIPAL_ID" \
  --role "Reader" \
  --scope "$AKS_ID"

# Contributor on the AKS node resource group (for snapshot access)
AKS_NODE_RG=$(az aks show \
  --name "$AKS_CLUSTER_NAME" \
  --resource-group "$AKS_RG" \
  --query nodeResourceGroup -o tsv)
AKS_NODE_RG_ID=$(az group show --name "$AKS_NODE_RG" --query id -o tsv)

az role assignment create \
  --assignee "$VAULT_PRINCIPAL_ID" \
  --role "Contributor" \
  --scope "$AKS_NODE_RG_ID"
```

---

### After role assignments, you're onto Step 5 (Backup Policy) and Step 6 (Backup Instance)

From your [runbook](file:///), those are:
1. `az dataprotection backup-policy get-default-policy-template` → save → create
2. `az dataprotection backup-instance initialize-backupconfig` with your namespaces (`barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`, `thehyve`)
3. Trigger the test backup

Tackle the two role assignments first — the extension one is the one most likely to bite you if skipped, since without it Velero can't write blobs to `aks-backups`.