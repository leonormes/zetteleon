---
created: 2026-07-31T09:49:10+00:00
modified: 2026-08-29T09:36:45+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-31-2026-10-49am
title: Backup status check set
type: note
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Friday Jul 31, 2026 - 10:49 AM_
---

## Backup Status Check set—MKUH / CUH / NNUH

Grounded in your last ~4 weeks of work (`SPEC-FTFL-525`, ZRS checklist 13 Jul, MKUH remediation 15–20 Jul, CUH DNS/extension troubleshooting 9 Jul). Tooling is Azure Backup for AKS (`az dataprotection` + `azure-aks-backup` extension)—not standalone Velero/Kasten. Velero only shows up as the controller inside `dataprotection-microsoft`.

Activate PIM where needed (MKUH tenant `e96dd0a1-5d47-4a94-9e4a-5c1056daa82c`), then `az login` / set subscription before each site block.

---

### Shared Resource Map (From yOur nOtes)

| Site | Cluster | Cluster RG | Backup RG | Vault | Storage account | Sub (where known) |
|------|---------|------------|-----------|-------|-----------------|-------------------|
| MKUH | `aks-mkuh-uks-prd-01` | (cluster RG TBD via discovery) | `aks-mkuh-uks-prd-01-backup-rg` | `aks-mkuh-uks-prd-01-backupvault` | `aksmkuhuksprd01bkp01` | `454e1659-7f91-4963-b468-668ac7cef106` |
| CUH | `aks-ff-uks-gp-01` | `rg-ff-uks-gp-net` | `aks-ff-uks-gp-01-backup-rg` | `aksbackupvault` (confirm live) | `aksffuksgp01cuhbackup` | FitFile GP path; PE work used `709f3d57-b6d7-48c6-8252-6b1c1174a541` |
| NNUH | (name not stored) | | assumed `aks-ff-uks-gp-01-backup-rg` | (discover) | `aksffuksgp01backupsa` | RG thin—confirm first |

Snapshot RG (MKUH): `aks-mkuh-uks-prd-01-backup-snapshots-rg`
Vault MSI principal you checked: `6cbab191-4cd3-4ee9-9aa9-acc5382b210f`
Known MKUH instance: `aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09`

---

### 0. One-shot Discovery (All three—start hEre)

```bash
az account show -o table

az storage account list \
  --query "[?contains(name, 'backup') || contains(name, 'bkp')].{name:name, rg:resourceGroup, sku:sku.name, public:publicNetworkAccess}" \
  -o table

az dataprotection backup-instance list-from-resourcegraph \
  --datasource-type AzureKubernetesService \
  -o table

az k8s-extension list --cluster-type managedClusters \
  --query "[?name=='azure-aks-backup' || contains(extensionType, 'dataprotection')].{cluster:id, name:name, state:provisioningState}" \
  -o table
```

---

### 1. MKUH—full Posture (`454e1659-…`)

```bash
az account set --subscription 454e1659-7f91-4963-b468-668ac7cef106

# --- Identity / tenant ---
az account show --query "{sub:id, name:name, tenant:tenantId}" -o json

# --- Vault ---
az dataprotection backup-vault show \
  -g aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  -o jsonc

# Vault MSI principal (cross-check against 6cbab191-…)
az dataprotection backup-vault show \
  -g aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "identity" -o jsonc

# --- Backup instances + protection state ---
az dataprotection backup-instance list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "[].{Name:name, Cluster:properties.friendlyName, State:properties.currentProtectionState, Policy:properties.policyInfo.policyId}" \
  -o table

# Known instance detail
az dataprotection backup-instance show \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --backup-instance-name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  -o jsonc

# --- Jobs: Backups vs Tiering (your recurring failure mode) ---
az dataprotection job list \
  --subscription 454e1659-7f91-4963-b468-668ac7cef106 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "reverse(sort_by([].{JobId:name, Status:properties.status, Op:properties.operationCategory, Start:properties.startTime, End:properties.endTime}, &Start))[:20]" \
  -o table

# Latest Tiering only
az dataprotection job list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "[?properties.operation=='Tiering' || properties.operationCategory=='Tiering'] | reverse(sort_by(@, &properties.startTime))[:5].{Status:properties.status, Start:properties.startTime, Error:properties.errorDetails}" \
  -o jsonc

# Latest AKS-scoped job
az dataprotection job list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "sort_by([?properties.dataSourceType=='Microsoft.ContainerService/managedClusters'], &properties.startTime)[-1].{Status:properties.status, Start:properties.startTime, Error:properties.errorDetails}" \
  -o jsonc

# --- RBAC: vault MSI on snapshot RG (UserErrorMissingVaultMSIPermissionsOnSnapshotRG) ---
az role assignment list \
  --assignee 6cbab191-4cd3-4ee9-9aa9-acc5382b210f \
  --scope /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-snapshots-rg \
  -o table

# Expect Contributor (Joao confirmed 15 Jul textually; re-verify it still lands)
az role assignment list \
  --assignee 6cbab191-4cd3-4ee9-9aa9-acc5382b210f \
  --all \
  --query "[?contains(scope, 'mkuh')].{role:roleDefinitionName, scope:scope}" \
  -o table

# --- Storage: ZRS + public exposure (Ollie/FTFL-525) ---
az storage account show \
  --name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --query "{name:name, sku:sku.name, provisioningState:provisioningState, publicNetworkAccess:publicNetworkAccess, allowSharedKeyAccess:allowSharedKeyAccess}" \
  -o jsonc

az storage account migration show \
  --account-name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --name default \
  -o jsonc 2>/dev/null || echo "no migration record"

# --- Recovery points (are scheduled backups actually leaving snaps?) ---
az dataprotection recovery-point list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --backup-instance-name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  --query "reverse(sort_by([].{id:name, time:properties.recoveryPointTime, type:properties.recoveryPointType}, &time))[:10]" \
  -o table

# --- Policy: use real BACKUP rule name (BackupHourly), not retention "Daily" ---
POLICY_ID=$(az dataprotection backup-instance show \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --backup-instance-name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  --query "properties.policyInfo.policyId" -o tsv)
echo "POLICY_ID=$POLICY_ID"
az dataprotection backup-policy show --ids "$POLICY_ID" \
  --query "properties.policyRules[].{name:name, type:objectType}" -o table

# --- Cluster extension (fill cluster name/RG if needed via discovery) ---
# az k8s-extension show --name azure-aks-backup --cluster-type managedClusters \
#   --cluster-name aks-mkuh-uks-prd-01 -g <MKUH_CLUSTER_RG> \
#   --query "{state:provisioningState, statuses:statuses}" -o jsonc
```

How you read MKUH: Backups Completed + Tiering Failed (early–mid July pattern) → RSI snaps exist, vault-store tier poorly; almost always MSI/`Contributor` on snapshot RG or storage path. `sku!= Standard_ZRS` → FTFL-525 still open for this site.

---

### 2. CUH—`aks-ff-uks-gp-01`

```bash
# Switch to the FitFile GP subscription that owns rg-ff-uks-gp-net
# az account set --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541   # only if that is still the right sub

# --- Extension health (prior Helm timeout / ResourceNotFound) ---
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  -g rg-ff-uks-gp-net \
  --query "{state:provisioningState, statuses:statuses}" -o jsonc

# --- In-cluster: BSL + controller (DNS / proxy failures lived here) ---
az aks command invoke -g rg-ff-uks-gp-net -n aks-ff-uks-gp-01 --command \
  "kubectl get backupstoragelocation -n dataprotection-microsoft -o wide"

az aks command invoke -g rg-ff-uks-gp-net -n aks-ff-uks-gp-01 --command \
  "kubectl describe backupstoragelocation default -n dataprotection-microsoft"

az aks command invoke -g rg-ff-uks-gp-net -n aks-ff-uks-gp-01 --command \
  "helm list -n dataprotection-microsoft -a"

az aks command invoke -g rg-ff-uks-gp-net -n aks-ff-uks-gp-01 --command \
  "kubectl get pods -n dataprotection-microsoft -o wide"

az aks command invoke -g rg-ff-uks-gp-net -n aks-ff-uks-gp-01 --command \
  "kubectl logs -n dataprotection-microsoft -l app.kubernetes.io/name=dataprotection-microsoft-controller --tail=100"

# --- Storage ZRS + migration ---
az storage account show \
  --name aksffuksgp01cuhbackup \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --query "{name:name, sku:sku.name, provisioningState:provisioningState, publicNetworkAccess:publicNetworkAccess}" \
  -o jsonc

az storage account migration show \
  --account-name aksffuksgp01cuhbackup \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --name default -o jsonc 2>/dev/null || echo "no migration record"

# --- Private endpoint / DNS (prior PE name) ---
az network private-endpoint show \
  -g aks-ff-uks-gp-01-backup-rg \
  -n pe-aksffuksgp01cuhbackup-blob \
  --query "customDnsConfigs" -o jsonc

# --- Vault + instances (confirm vault name if aksbackupvault 404s) ---
az dataprotection backup-vault list -g aks-ff-uks-gp-01-backup-rg -o table

az dataprotection backup-policy list \
  --vault-name aksbackupvault \
  -g aks-ff-uks-gp-01-backup-rg -o table 2>/dev/null || true

az dataprotection backup-instance list \
  --resource-group aks-ff-uks-gp-01-backup-rg \
  --vault-name aksbackupvault \
  --query "[].{Name:name, Cluster:properties.friendlyName, State:properties.currentProtectionState}" \
  -o table 2>/dev/null || \
az dataprotection backup-instance list-from-resourcegraph \
  --datasource-type AzureKubernetesService \
  --datasource-id "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01" \
  -o table

# --- Jobs on CUH vault (after vault name confirmed) ---
# az dataprotection job list -g aks-ff-uks-gp-01-backup-rg --vault-name <CUH_VAULT> \
#   --query "reverse(sort_by([], &properties.startTime))[:15].{Status:properties.status, Op:properties.operationCategory, Start:properties.startTime}" -o table

# Storage Blob Data Contributor check for extension MSI (Alexis/Ryan work)
# After you have the extension principalId from az k8s-extension show:
# EXT_MSI=$(az k8s-extension show -n azure-aks-backup --cluster-type managedClusters \
#   -c aks-ff-uks-gp-01 -g rg-ff-uks-gp-net --query "identity.principalId" -o tsv)
# az role assignment list --assignee "$EXT_MSI" \
#   --scope $(az storage account show -n aksffuksgp01cuhbackup -g aks-ff-uks-gp-01-backup-rg --query id -o tsv) -o table
```

How you read CUH: `provisioningState!= Succeeded` or BSL `Available=False` → stop and fix DNS/proxy/PE before tiering. `sku=Standard_ZRS` + healthy BSL + recent Completed backups = good.

---

### 3. NNUH—confirm Names then Same Pattern

Evidence is thin: you have storage name `aksffuksgp01backupsa` and no solid vault/cluster pair in LTM. Discover first.

```bash
# Find NNUH storage + real RG
az storage account show --name aksffuksgp01backupsa \
  --query "{name:name, rg:resourceGroup, sku:sku.name, public:publicNetworkAccess}" -o jsonc \
  2>/dev/null || \
az storage account list --query "[?name=='aksffuksgp01backupsa'].{name:name, rg:resourceGroup, sku:sku.name}" -o table

NNUH_BACKUP_RG=$(az storage account list \
  --query "[?name=='aksffuksgp01backupsa'].resourceGroup | [0]" -o tsv)
echo "NNUH_BACKUP_RG=$NNUH_BACKUP_RG"

az storage account show -n aksffuksgp01backupsa -g "$NNUH_BACKUP_RG" \
  --query "{name:name, sku:sku.name, provisioningState:provisioningState, publicNetworkAccess:publicNetworkAccess}" -o jsonc

az storage account migration show \
  --account-name aksffuksgp01backupsa \
  --resource-group "$NNUH_BACKUP_RG" \
  --name default -o jsonc 2>/dev/null || echo "no migration"

# Vault + instances in that RG
az dataprotection backup-vault list -g "$NNUH_BACKUP_RG" -o table

for V in $(az dataprotection backup-vault list -g "$NNUH_BACKUP_RG" --query "[].name" -o tsv); do
  echo "=== vault $V ==="
  az dataprotection backup-instance list -g "$NNUH_BACKUP_RG" --vault-name "$V" \
    --query "[].{Name:name, Cluster:properties.friendlyName, State:properties.currentProtectionState}" -o table
  az dataprotection job list -g "$NNUH_BACKUP_RG" --vault-name "$V" \
    --query "reverse(sort_by([], &properties.startTime))[:10].{Status:properties.status, Op:properties.operationCategory, Start:properties.startTime}" -o table
done

# AKS clusters that look NNUH, then extension hygiene
az aks list --query "[?contains(name, 'nnuh') || contains(name, 'NNUH')].{name:name, rg:resourceGroup}" -o table
# Then for each: az k8s-extension show --name azure-aks-backup --cluster-type managedClusters -c <name> -g <rg> ...
```

---

### 4. Cross-site Scorecard (Fill after rUns)

| Check | MKUH | CUH | NNUH | Pass signal |
|-------|------|-----|------|-------------|
| Storage SKU ZRS | | | | `Standard_ZRS` (FTFL-525 gate) |
| `publicNetworkAccess` | | | | `Disabled` (or justified exception) |
| Extension `Succeeded` | | | | no Helm/proxy 407 |
| BSL Available | n/a ARM | | | `Phase=Available` |
| Instance `ProtectionConfigured` / similar | | | | not `SoftDeleted` / empty |
| Recent Backup job Completed | | | | last 24–48h |
| Recent Tiering Completed | | | | not serial Failed |
| Vault MSI Contributor on snapshot RG | | | | present (MKUH was the pain) |
| Extension/cluster MSI blob roles | | | | `Storage Blob Data *` on backup SA |
| Recovery points non-empty | | | | RPs within policy window |

---

### 5. Optional after Checks (Don't rUn until sCorecard is gReen)

```bash
# MKUH adhoc — ONLY with a real AzureBackupRule name from policy show
# (your earlier "Daily" failed: BMSUserErrorDPPAdhocBackupNotAllowedForBackupType;
#  real rule was BackupHourly)
az dataprotection backup-instance adhoc-backup \
  --rule-name "BackupHourly" \
  --retention-tag-override Daily \
  --ids "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-rg/providers/Microsoft.DataProtection/backupVaults/aks-mkuh-uks-prd-01-backupvault/backupInstances/aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09"
```

If you still have `./aks-backup-audit.sh` from SPEC-FTFL-525 Phase 0, prefer:

```bash
./aks-backup-audit.sh <cluster> <cluster-rg>
```

then re-run §6 of the SPEC against this scorecard.

---

### Context from the Last Few Weeks (So yOu kNow what yOu're vAlidating)

1. MKUH—Scheduled Backup jobs Completing; Tiering failing (`UserErrorMissingVaultMSIPermissionsOnSnapshotRG`). Joao Andre's "Done it now" (15 Jul) on `Contributor` for vault MSI `6cbab191-…` on snapshot RG—re-proof with `az role assignment list`, don't trust email alone. Adhoc with `--rule-name Daily` is wrong; policy rule is `BackupHourly`.
2. CUH—Extension install blocked by proxy/DNS; BSL/`dataprotection-microsoft` both matter; PE `pe-aksffuksgp01cuhbackup-blob`; Alexis applied Storage Blob Data Contributor—verify RBAC still present.
3. NNUH—Storage `aksffuksgp01backupsa` only; treat RG/vault/cluster as unknown until discovery.
4. FTFL-525 pass bar: all three backup SAs `Standard_ZRS` + vaults actually protecting clusters.

---

### Gaps / Don't Invent

- NNUH cluster name, vault name, and backup RG are not firmly in LTM—use §0 / §3 discovery.
- Exact MKUH AKS cluster resource-group string for `az k8s-extension show` was often placeholder; resolve via `az aks list` after `az account set`.
- CUH vault name `aksbackupvault` appeared in notes; if list is empty, take name from `backup-vault list` / resource graph, not assumptions.

Run MKUH §1 + CUH extension/BSL first (richest known failures); paste tables back and we can turn the scorecard into an ordered fix plan.
