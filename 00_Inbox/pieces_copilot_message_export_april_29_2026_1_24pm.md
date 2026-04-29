*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:24 PM*
---
From your long-term memory trail today, this is the successful end-state of the AKS backup setup: at **1:21 PM** the instance was already listing as `ProtectionConfigured`, and by **1:23 PM** you had this confirmed object plus `RULE_NAME=BackupDaily`. There isn’t additional relevant project-file context attached here beyond that runbook/CLI trail, so the interpretation is straightforward:

## Status

Your AKS backup instance is now **fully configured and healthy**.

### What each field means

| Field | Value | Meaning |
|---|---|---|
| `FriendlyName` | `aks-ff-uks-gp-1/aks-ff-uks-gp-1-backup` | Human-readable label for the protected datasource |
| `Name` | `aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5` | Actual Azure backup instance resource name |
| `ProtectionState` | `ProtectionConfigured` | Protection is active |
| `ProtectionStatus` | `ProtectionConfigured` | No longer configuring; now in steady protected state |
| `Provisioning` | `Succeeded` | Resource creation completed successfully |
| `RULE_NAME` | `BackupDaily` | Policy rule name to use for an ad-hoc backup |

## Practical conclusion

You are past all the earlier blockers:

- backup payload shape
- snapshot RG permissions
- trusted access role binding
- async protection configuration

This is now a **good final state**.

## What you can do next

### 1. Verify recent jobs

```bash
az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query "reverse(sort_by([].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}, &Start))" \
  -o table
```

### 2. Trigger an ad-hoc backup using the discovered rule name

```bash
INSTANCE_NAME="aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5"
RULE_NAME="BackupDaily"

az dataprotection backup-instance adhoc-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$INSTANCE_NAME" \
  --rule-name "$RULE_NAME"
```

### 3. Re-check instance state if you want a final confirmation

```bash
az dataprotection backup-instance show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$INSTANCE_NAME" \
  --query '{FriendlyName:properties.friendlyName,Name:name,ProtectionState:properties.currentProtectionState,ProtectionStatus:properties.protectionStatus.status,Provisioning:properties.provisioningState}' \
  -o json
```

## Bottom line

Yes — this is **success**.