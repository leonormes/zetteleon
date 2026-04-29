*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:17 PM*
---
Based on today’s long-term memory trail and the CLI output you just pasted — with no extra project files attached here beyond that runbook/terminal context — you’ve now cleared the trusted-access blocker.

## Current state

Timeline from your session:

- **11:51 AM**: AKS backup extension was healthy
- **12:03 PM**: backup vault existed
- **1:10 PM**: trusted access role binding was created successfully
- **1:12 PM**: binding listed as `Succeeded`
- **1:16 PM**: `validate-for-backup` returned:

```json
{
  "objectType": "OperationJobExtendedInfo"
}
```

## What that means

That is a good sign.

The important difference is: you are **no longer getting**:

- `UserErrorTrustedAccessGatewayReturnedForbidden`
- snapshot RG permission errors
- JSON shape / `DatasourceSet` errors

So the chain has moved from **blocked during validation** to **validation request accepted**.

In practice, that means you’re now clear to move to **create**.

## The exact fix that worked

For the record, the winning combination was:

- short binding name: `azbkup-trust`
- fully-qualified single role:
  `Microsoft.DataProtection/backupVaults/backup-operator`

Not:

- `restore-operator`
- `backup-operator` by itself
- overly long binding name

## Next step

Run this now:

```bash
nocorrect az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json
```

## Then verify protection is configured

```bash
az dataprotection backup-instance list \
  --resource-group "$VAULT_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Cluster:properties.friendlyName,State:properties.currentProtectionState}" \
  -o table
```

What you want:

- your backup instance present
- state like `ProtectionConfigured`

## Then inspect jobs

```bash
az dataprotection job list \
  --resource-group "$VAULT_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}" \
  -o table
```

## Practical read of where you are

| Stage | Status |
|---|---|
| Extension install | Passed |
| Vault creation | Passed |
| Backup instance JSON generation | Passed |
| Snapshot RG RBAC | Passed far enough to continue |
| Trusted access binding | Passed |
| Validate-for-backup | Accepted |
| Create | **Next** |

## Recommended copy/paste block

```bash
nocorrect az dataprotection backup-instance create \
  --vault-name "$VAULT_NAME" \
  --resource-group "$VAULT_RG" \
  --subscription "$SUB_ID" \
  --backup-instance @backup-instance.json

az dataprotection backup-instance list \
  --resource-group "$VAULT_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Cluster:properties.friendlyName,State:properties.currentProtectionState}" \
  -o table

az dataprotection job list \
  --resource-group "$VAULT_RG" \
  --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}" \
  -o table
```

## Bottom line

Yes — this looks like you’ve **successfully fixed the trusted access issue** and are ready for `backup-instance create`.

If you paste the output of the `create` command, I can tell you immediately whether the instance is fully configured or whether there’s one final post-create check to do.