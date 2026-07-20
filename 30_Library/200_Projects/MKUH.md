---
created: 2026-03-30T08:34:07+00:00
modified: 2026-07-20T07:36:19+00:00
permalink: llmeon/30-library/200-projects/mkuh
project_category: deployments
project_name: Deployments
project_status: active
title: MKUH
type: null
---

## Access

Tenant ID: `e96dd0a1-5d47-4a94-9e4a-5c1056daa82c`

Activate PIM: <https://portal.azure.com/#view/Microsoft_Azure_PIMCommon/ActivationMenuBlade/~/azurerbac>

Contact: Joao.Andre@mkuh.nhs.uk

## Key Identifiers (verified 17 Jul 2026)

| Item | Value |
|---|---|
| Subscription (`subcr-sde-prd`) | `454e1659-7f91-4963-b468-668ac7cef106` |
| Backup RG | `aks-mkuh-uks-prd-01-backup-rg` |
| Snapshot RG | `aks-mkuh-uks-prd-01-backup-snapshots-rg` |
| Backup vault | `aks-mkuh-uks-prd-01-backupvault` |
| Storage account | `aksmkuhuksprd01bkp01` (confirmed `Standard_ZRS`) |
| Backup instance name | `aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09` |
| Backup policy | `dailyaksbackups-v1` |
| Vault MSI (role assignee) | `6cbab191-4cd3-4ee9-9aa9-acc5382b210f` |

Full backup-instance resource ID:

```
/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-rg/providers/Microsoft.DataProtection/backupVaults/aks-mkuh-uks-prd-01-backupvault/backupInstances/aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09
```

## Gotchas (learned the hard way)

- **`--rule-name "Daily"` fails** with `BMSUserErrorDPPAdhocBackupNotAllowedForBackupType`. `Daily` and `Default` are `AzureRetentionRule` entries (retention tags), not backup rules. The only triggerable backup rule in `dailyaksbackups-v1` is `BackupHourly`. Working pattern: `--rule-name BackupHourly --retention-tag-override Daily` (routes the recovery point into the Daily/vault tier). Same pattern as NNUH.
- **`backup-policy show --name` takes the bare policy name** (`dailyaksbackups-v1`), not the full ARM resource ID — full ID gives `BMSUserErrorInvalidInput`.
- First `az dataprotection` command prompts to install the extension. To skip prompts: `az config set extension.use_dynamic_install=yes_without_prompt`
- Backup schedule: every 4 hours (01:00, 05:00, 09:00, 13:00, 17:00, 21:00 UTC), ~7–10 min each.

## RBAC — Check Role Assignment on Snapshot RG

Confirm the vault MSI has Contributor on the snapshot RG (needed for Tiering; was the blocker under `SPEC-FTFL-525`, fixed by Joao 17 Jul):

```bash
az role assignment list \
  --assignee 6cbab191-4cd3-4ee9-9aa9-acc5382b210f \
  --scope /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-snapshots-rg \
  -o table
```

## Backup Instances

List instances (Name column = instance name for other commands):

```bash
az dataprotection backup-instance list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "[].{Name:name, Cluster:properties.friendlyName, State:properties.currentProtectionState}" \
  -o table
```

Show instance state:

```bash
az dataprotection backup-instance show \
  --subscription 454e1659-7f91-4963-b468-668ac7cef106 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  --query "{Name:name, FriendlyName:properties.friendlyName, ProtectionState:properties.currentProtectionState, ProvisioningState:properties.provisioningState, LastBackup:properties.lastBackupStatus}" \
  -o json
```

## Backup Policy

Get the policy ID attached to the instance:

```bash
az dataprotection backup-instance show \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --backup-instance-name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  --query "properties.policyInfo.policyId" -o tsv
```

List the policy's rules (bare name, not full ID):

```bash
az dataprotection backup-policy show \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --name dailyaksbackups-v1 \
  --query "properties.policyRules[].{Name:name, ObjectType:objectType, TriggerType:trigger.objectType}" -o table
```

Result (17 Jul 2026): `BackupHourly` = AzureBackupRule (schedule-triggered); `Default`, `Daily` = AzureRetentionRule.

## Trigger On-Demand (Adhoc) Backup — WORKING COMMAND

Verified working 17 Jul 2026 (returned job `68f71d0d-96c5-44ac-9c11-190ca891f7d1`):

```bash
az dataprotection backup-instance adhoc-backup \
  --rule-name BackupHourly \
  --retention-tag-override Daily \
  --ids "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/aks-mkuh-uks-prd-01-backup-rg/providers/Microsoft.DataProtection/backupVaults/aks-mkuh-uks-prd-01-backupvault/backupInstances/aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09"
```

Split-argument alternative if `--ids` + `--retention-tag-override` errors:

```bash
az dataprotection backup-instance adhoc-backup \
  --name aks-mkuh-uks-prd-01-aks-mkuh-uks-prd-01-c39aa3ec-4a0b-11f1-a04a-00155d666a09 \
  --rule-name BackupHourly \
  --retention-tag-override Daily \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault
```

## Job Monitoring

Latest Tiering job status (the `SPEC-FTFL-525` verification check):

```bash
az dataprotection job list \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "[?properties.operation=='Tiering'] | [-1].{Status:properties.status, Start:properties.startTime}" \
  -o table
```

Show a specific job (swap in the job ID from the adhoc-backup output):

```bash
az dataprotection job show \
  --subscription 454e1659-7f91-4963-b468-668ac7cef106 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --job-id <JOB_ID> \
  --query "{JobId:id, Status:properties.status, Operation:properties.operationCategory, StartTime:properties.startTime, EndTime:properties.endTime, ProgressPercent:properties.progressPercent, ErrorDetails:properties.errorDetails}" \
  -o json
```

List all recent jobs, newest first:

```bash
az dataprotection job list \
  --subscription 454e1659-7f91-4963-b468-668ac7cef106 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --vault-name aks-mkuh-uks-prd-01-backupvault \
  --query "reverse(sort_by([].{JobId:id, Status:properties.status, Operation:properties.operationCategory, StartTime:properties.startTime, EndTime:properties.endTime}, &StartTime))" \
  -o table
```

Poll a job until it finishes:

```bash
while true; do
  STATUS=$(az dataprotection job show \
    --subscription 454e1659-7f91-4963-b468-668ac7cef106 \
    --resource-group aks-mkuh-uks-prd-01-backup-rg \
    --vault-name aks-mkuh-uks-prd-01-backupvault \
    --job-id <JOB_ID> \
    --query "properties.status" -o tsv)
  echo "$(date): Job status = $STATUS"
  if [[ "$STATUS" == "Completed" ]] || [[ "$STATUS" == "Failed" ]] || [[ "$STATUS" == "CompletedWithWarnings" ]]; then
    echo "Job finished with status: $STATUS"
    break
  fi
  sleep 10
done
```

Status values: `InProgress` → `Completed` / `Failed` / `CompletedWithWarnings`. Backups typically take 5–15 min.

## Storage Account Replication (ZRS conversion, FTFL-525)

```bash
az storage account show \
  --name aksmkuhuksprd01bkp01 \
  --resource-group aks-mkuh-uks-prd-01-backup-rg \
  --query "sku.name" -o tsv
```

Confirmed `Standard_ZRS` on 17 Jul 2026 — ZRS conversion done. (If ever needed again: `az storage account migration start --sku Standard_ZRS`, per NNUH pattern.)

## Status Log

- **17 Jul 2026**: Contributor role confirmed on snapshot RG for vault MSI (Joao). Adhoc backup triggered successfully with `BackupHourly` + `Daily` override. Storage already `Standard_ZRS`. Scheduled backups completing every 4 h; **Tiering jobs still failing repeatedly** (~13:16 UTC daily among others) — check whether they succeed now RBAC has propagated.
