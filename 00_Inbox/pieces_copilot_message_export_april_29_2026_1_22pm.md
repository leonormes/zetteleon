*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:22 PM*
---
Based on your long-term memory trail today — **11:51 AM** extension healthy, **12:03 PM** vault in place, **1:10 PM** trusted access binding created, and **1:16 PM** validation accepted — plus the CLI output you just pasted, this has now moved into the **successful create / async settle** phase. There’s no extra attached project file context beyond that runbook trail, so I’m reading this directly from the Azure response.

## Status: this is a success

The important bits in your output are:

| Field | Meaning |
|---|---|
| `properties.provisioningState = "Succeeded"` | The **backup instance resource was created successfully** |
| `currentProtectionState = "ConfiguringProtection"` | Azure is still **finishing protection setup asynchronously** |
| `protectionStatus.status = "ConfiguringProtection"` | Same story: not failed, just still converging |

So: **create succeeded**.  
You are no longer blocked on:

- payload shape
- snapshot RG RBAC
- trusted access binding

## What this means practically

You’ve crossed the key line:

- the backup instance exists
- it is wired to the AKS cluster
- policy + namespace scope + snapshot RG are attached
- Azure is still finalizing protection

That means the next step is **not** to recreate anything.  
The next step is to **poll until protection finishes**.

---

## Do this next

### 1) Save the instance name

```bash
INSTANCE_NAME="aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5"
```

### 2) Poll the backup instance state

```bash
watch -n 15 "az dataprotection backup-instance show \
  --vault-name \"$VAULT_NAME\" \
  --resource-group \"$VAULT_RG\" \
  --subscription \"$SUB_ID\" \
  --name \"$INSTANCE_NAME\" \
  --query '{Name:name,Provisioning:properties.provisioningState,ProtectionState:properties.currentProtectionState,ProtectionStatus:properties.protectionStatus.status,FriendlyName:properties.friendlyName}' \
  -o json"
```

If you don’t want `watch`, use:

```bash
az dataprotection backup-instance show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$INSTANCE_NAME" \
  --query '{Name:name,Provisioning:properties.provisioningState,ProtectionState:properties.currentProtectionState,ProtectionStatus:properties.protectionStatus.status,FriendlyName:properties.friendlyName}' \
  -o json
```

## What you want to see

Ideally it should move away from:

```text
ConfiguringProtection
```

to something like:

```text
ProtectionConfigured
```

or another clearly steady/healthy protected state.

---

## 3) Check jobs as protection settles

```bash
az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query "[].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}" \
  -o table
```

If you want the most recent first:

```bash
az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query "reverse(sort_by([].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}, &Start))" \
  -o table
```

---

## 4) Once protection is configured, trigger or verify a backup

Before running an ad-hoc backup, get the policy rule name:

```bash
az dataprotection backup-policy show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$POLICY_NAME" \
  --query "properties.policyRules[?objectType=='AzureBackupRule'].name" \
  -o tsv
```

That will likely return something like `BackupIntervals`.

Then trigger the ad-hoc backup:

```bash
RULE_NAME="$(az dataprotection backup-policy show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$POLICY_NAME" \
  --query "properties.policyRules[?objectType=='AzureBackupRule'].name | [0]" \
  -o tsv)"

az dataprotection backup-instance adhoc-backup \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$INSTANCE_NAME" \
  --rule-name "$RULE_NAME"
```

Then watch jobs again:

```bash
az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query "reverse(sort_by([].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}, &Start))" \
  -o table
```

---

## Interpretation of your returned object

A few specific observations from the payload:

### Good signs
- `dataSourceSetInfo` is present — this confirms you fixed the earlier `Null DatasourceSet object` problem.
- `policyParameters.backupDatasourceParametersList` includes your namespace scope:
  - `barts`
  - `ff-a`
  - `ff-b`
  - `ff-c`
  - `spicedb`
  - `thehyve`
  - `thehyve-cuh`
  - `thehyve-mkuh`
- `snapshotVolumes: true` is set
- snapshot RG is correctly attached:
  - `pentest-1-backup-snapshots-rg`

### Also good
- `properties.provisioningState` is already `Succeeded`
- the resource is in the expected vault/resource group:
  - vault RG: `pentest-1-backup-rg`

So structurally, this is exactly what you were trying to achieve.

---

## Short version

You’re through the hard part.

**This create worked.**  
The only remaining task is to let Azure finish moving from:

```text
ConfiguringProtection
```

to a steady protected state, then verify with:

1. `backup-instance show`
2. `job list`
3. optional `adhoc-backup`

---

## Pasteable next-step block

```bash
INSTANCE_NAME="aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5"

az dataprotection backup-instance show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$INSTANCE_NAME" \
  --query '{Name:name,Provisioning:properties.provisioningState,ProtectionState:properties.currentProtectionState,ProtectionStatus:properties.protectionStatus.status,FriendlyName:properties.friendlyName}' \
  -o json

az dataprotection job list \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --query "reverse(sort_by([].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}, &Start))" \
  -o table

RULE_NAME="$(az dataprotection backup-policy show \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --name "$POLICY_NAME" \
  --query "properties.policyRules[?objectType=='AzureBackupRule'].name | [0]" \
  -o tsv)"

echo "RULE_NAME=$RULE_NAME"
```

If you want, paste the output of:

```bash
az dataprotection backup-instance show ...
```

and I’ll tell you whether it has fully transitioned to protected state yet.