---
created: 2026-07-02T08:18:56+00:00
modified: 2026-07-04T10:52:08+00:00
permalink: llmeon/00-inbox/spec-ftfl-525
title: SPEC-FTFL-525
type: note
---

## SPEC-FTFL-525—AKS Backup ZRS Compliance & Hardening

Version: 1.0 | Date: 2026-07-02 | Owner: Leon Ormes | Ticket: FTFL-525

### 1. Purpose

Repeatable specification for auditing and remediating Azure Backup for AKS across FITFILE customer sites (MKUH, NNUH, CUH, future). Designed for execution by any LLM given the output of `aks-backup-audit.sh`—the discovery script gathers all state deterministically so no LLM tokens are spent on interactive state-gathering.

Driver: FITFILE indemnity insurance requires customer backups stored in datacentres ≥10 km apart. ZRS is the most distributed within-region option (UK data residency). _The 10 km ↔ AZ-distance compliance question is owned by Leon/Robin and is out of scope here—do not re-raise it; execute the technical standard below._

### 2. Execution Protocol

```
Phase 0 (no LLM, ~0 tokens):  az login to site tenant → ./aks-backup-audit.sh [cluster] [rg]
Phase 1 (LLM):                Paste SPEC + report → LLM evaluates §4 decision table
Phase 2 (LLM):                LLM emits findings table + ordered remediation plan
                              using §5 templates with S13 variables substituted
Phase 3 (human):              Run commands; escalate any Owner/UAA-gated items
Phase 4 (no LLM or LLM):      Run §6 verification; re-run audit script → clean pass
```

Tenant note: each NHS trust is (assume until proven otherwise) a separate Azure tenant. `az account list` from one site's session will not show another's resources. Phase 0 starts with a fresh `az login` per site.

### 3. Domain model—read before Evaluating Anything

```
Backup Vault ──owns──> Backup Policy ──bound to──> Backup Instance ──protects──> AKS cluster
     │                                                                              │
     │ (Vault's OWN MSI: does Tiering                          (Backup Extension pod:
     │  copies to Vault Store)                                  writes Operational backups
     ▼                                                          via Extension Identity)
Vault Store (long retention,                                          │
lives in VAULT's own storage —                                        ▼
has its OWN redundancy setting)                    Storage account (blob container: manifests)
                                                   + Snapshot RG (disk snapshots of PVs)
```

Three distinct storage locations hold backup data—the ticket's "all backups are ZRS" plausibly touches all three:

| Location | Holds | Redundancy controlled by |
|---|---|---|
| L1. Storage account (blob) | Operational-store manifests/metadata | Storage account SKU (`Standard_LRS`/`Standard_ZRS`) |
| L2. Snapshot RG | PV disk snapshots (incremental) | Snapshot resource SKU |
| L3. Vault Store | Long-retention (tiered) copies | Vault `storageSettings.type` (set at vault creation) |

Two distinct identities—confusing them was the biggest diagnostic trap at MKUH:

| Identity | Does | Needs (on storage account) |
|---|---|---|
| Extension Identity (in-cluster) | 4-hourly Operational backups | `Storage Blob Data Contributor` |
| Vault's system MSI | Tiering (Operational → Vault Store) | `Storage Blob Data Reader` |

Operational backups succeeding proves nothing about Tiering, and vice versa.

### 4. Decision Table

Evaluate every check against the audit report. Severity: CRIT (data-protection outcome broken) / HIGH (security or ticket non-compliance) / REVIEW (needs human judgement) / INFO.

| ID | Report section | Condition for PASS | On FAIL | Sev |
|---|---|---|---|---|
| C1 | S1 | Tenant/subscription matches intended site | Wrong tenant—stop, re-login | INFO |
| C2 | S3 | Extension of type `microsoft.dataprotection.kubernetes` exists, `provisioningState: Succeeded` | Backup not deployed. Remediation = full provisioning (out of scope of this spec; separate work) | CRIT |
| C3 | S3 | `configurationSettings["…useAAD"] == "true"` | Gate: R4 must NOT run until key-based consumers are ruled out | INFO |
| C4 | S4 | A Trusted Access binding for `Microsoft.DataProtection/backupVaults` exists | Flag: vaulted operations may be blocked | HIGH |
| C5 | S5 | Instance exists, `currentProtectionState == "ProtectionConfigured"` | Cluster not protected → provisioning gap | CRIT |
| C6 | S8 | Most recent Backup job `Completed`, started within policy interval + 1 h | Investigate errorDetails before anything else | CRIT |
| C7 | S8 | Most recent Tiering job `Completed` | If error code `UserErrorMissingVaultMSIPermissionsOnBackupStorageLocation` → R1. Other code → investigate. No Tiering jobs at all → check S7 policy actually has a VaultStore rule | CRIT |
| C8 | S11 | Vault MSI (`VAULT_MSI`) holds `Storage Blob Data Reader` at SA scope | Corroborates C7 → R1 | CRIT |
| C9 | S10 | `sku == "Standard_ZRS"` | → R2 (after C10 clear). `migrationInProgress: true` = already converting, wait | HIGH |
| C10 | S10 | `nfsV3` and `hns` both null/false; `migrationInProgress` false | ZRS migration blocked/deferred—flag | REVIEW |
| C11 | S10 | `allowBlobPublicAccess == false` | → R3 immediately (anonymous data exposure) | HIGH |
| C12 | S10 | `allowSharedKeyAccess == false` explicitly | `null` means ENABLED (Azure default semantics—confirmed against MS docs). → R4, gated on C3 | HIGH |
| C13 | S10 | `resourceAccessRules` contains an entry with `resourceId == VAULT_ID` | → R5. Must PASS before R6 is ever attempted | HIGH |
| C14 | S10 | `publicNetworkAccess == "Disabled"` OR `defaultAction == "Deny"` | Network-exposed (the "Ollie finding"). → R6, gated: C13 PASS + C15 + human sign-off | HIGH |
| C15 | S10 | ≥1 private endpoint, status `Approved` | Info for R6 readiness; absence means lockdown needs PE work first | INFO |
| C16 | S6 | Vault `storageSettings[0].type == "ZoneRedundant"` | Flag `LocallyRedundant` for review—vault redundancy is set at creation; in-place change is constrained. Consult current MS docs / raise with team. Do not fabricate a conversion command | REVIEW |
| C17 | S12 | Snapshot SKUs are ZRS-class | Report distribution; LRS snapshots = REVIEW item vs ticket intent. Remediation path not yet established—flag, don't invent | REVIEW |
| C18 | S9 | `oldest` recovery point age ≈ vault-tier retention intent | Window ≈ operational-only retention (e.g. ~7 d against an 84 d policy) ⇒ Tiering has never worked—corroborates C7 | CRIT |
| C19 | S11 | Operator can self-serve `roleAssignments/write` | Escalate to a listed Owner/UAA using §7 template | INFO |

Ordering rule: R5 strictly before R6, always. R2 is long-running—start it early. R1 is independent and usually escalation-gated.

### 5. Remediation Templates

Substitute `{{VARS}}` from report section S13. All templates verified live at MKUH except R6 (marked).

#### R1—Grant Vault MSI Read on Backup Storage _(fixes C7/C8; Needs Owner/UAA)_

```bash
az role assignment create \
  --assignee-object-id {{VAULT_MSI}} \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Reader" \
  --scope {{SA_ID}}
```

#### R2—LRS → ZRS Conversion _(fixes C9)_

```bash
az extension add --name storage-preview --upgrade
az storage account migration start \
  --account-name {{SA_NAME}} --resource-group {{SA_RG}} \
  --sku Standard_ZRS --name default --no-wait
```

`--name default` is the literal required value, not a placeholder. Zero downtime; can take 72 h+ to even begin; 72 h cooldown after completion before redundancy can change again.

#### R3—Disable Anonymous Blob Access _(fixes C11)_

```bash
az storage account update --name {{SA_NAME}} --resource-group {{SA_RG}} \
  --allow-blob-public-access false
```

#### R4—Disable Shared-key Auth _(fixes C12; Gate on C3)_

```bash
az storage account update --name {{SA_NAME}} --resource-group {{SA_RG}} \
  --allow-shared-key-access false
```

Hard cutover—any residual key/SAS consumer gets an immediate 403. Extension uses AAD (`useAAD: true`), so expected impact is nil; if in doubt, check storage logs for shared-key auth traffic first.

#### R5—Vault Resource-instance Network exception _(fixes C13; Prerequisite for R6)_

```bash
az storage account network-rule add \
  --resource-id {{VAULT_ID}} --tenant-id {{TENANT_ID}} \
  --resource-group {{SA_RG}} --account-name {{SA_NAME}}
```

CLI prints `No subnet or ip address supplied`—harmless notice, not an error. Verify the rule appears in `resourceAccessRules` in the JSON echo.

#### R6—Close Public Network Access _(fixes C14 — not yet Executed at Any Site; gated)_

Preconditions: C13 PASS, C15 private endpoint Approved, team confirmation nothing else depends on the public path (portal blob browsing and Cloud Shell data-plane access are also affected).

```bash
az storage account update --name {{SA_NAME}} --resource-group {{SA_RG}} \
  --default-action Deny
# or the stricter:
az storage account update --name {{SA_NAME}} --resource-group {{SA_RG}} \
  --public-network-access Disabled
```

### 6. Verification Protocol

V1—Tiering fix (after R1, allow ~5 min RBAC propagation):

```bash
az dataprotection backup-instance adhoc-backup --rule-name "Daily" \
  --ids "/subscriptions/{{SUB_ID}}/resourceGroups/{{VAULT_RG}}/providers/Microsoft.DataProtection/backupVaults/{{VAULT_NAME}}/backupInstances/{{INSTANCE_NAME}}"

az dataprotection job list --resource-group {{VAULT_RG}} --vault-name {{VAULT_NAME}} \
  --query "[?properties.operation=='Tiering'] | [-1].{Status:properties.status, Start:properties.startTime, Error:properties.errorDetails}" -o json
```

Pass = `Completed`. The `Daily` rule name matters—only Daily-tagged backups trigger the Vault Store copy.

V2—Migration progress (after R2):

```bash
az storage account migration show --account-name {{SA_NAME}} \
  --resource-group {{SA_RG}} --migration-name default -o json
```

V3—Full re-audit: re-run `aks-backup-audit.sh`; every CRIT/HIGH check should PASS (or be a tracked, gated exception like C14 pending R6 sign-off).

### 7. Escalation Template (C19)

> Subject: Role assignment needed—fixes broken long-term retention on {{CLUSTER_NAME}} backups
>
> Every "Tiering" job fails with `UserErrorMissingVaultMSIPermissionsOnBackupStorageLocation`. Operational backups are fine—the failure is scoped to the copy into the long-retention Vault Store tier, so effective recoverability is currently ~{{OPERATIONAL_DAYS}} days, not {{VAULT_DAYS}} days. Root cause: the Backup vault's managed identity is missing `Storage Blob Data Reader` on the backup storage account. I hold Contributor only, so cannot assign roles. Could you run: _(paste R1 with values)_. I'll trigger an on-demand backup afterwards and confirm the tiering job completes.

Send to an Owner/UAA from report S11 (escalation contacts subsection).

### 8. Known Traps (All eNcountered live—do not rElearn tHese)

1. `allowSharedKeyAccess: null` means ENABLED. Azure treats unset as permit. Never read null as "off".
2. `-o table` silently drops all-null columns. Security posture checks must use `-o json`. (The audit script already does.)
3. Extension name is not reliably `azure-aks-backup`. Always discover via `k8s-extension list` filtered on `extensionType`.
4. Two identities (§3). "Backups are green" ≠ "long-term retention works". Check Tiering jobs and the recovery-point window (C18) explicitly.
5. `ProtectionConfigured` is config state, not outcome. MKUH sat "healthy" for weeks with 100 % Tiering failure.
6. Lockdown-before-exception regression: flipping `defaultAction` to `Deny` without R5 in place re-breaks Tiering silently. R5 is a free no-op while public access is open—do it pre-emptively.
7. Graph lookups can fail (`Cannot find user or service principal…`) in restricted tenants. Use object IDs, or list by `--scope` and filter—never depend on UPN resolution.
8. `--include-inherited` matters: role assignments usually live at subscription/management-group scope; a scope-only query returns misleadingly empty.
9. RBAC propagation lag: wait a few minutes after R1 before V1, or the retest fails spuriously.
10. A half-finished lockdown is a recognisable pattern (private endpoint approved + public access still open). Found at MKUH; suspected at NNUH. Check C14+C15 together.
11. ZRS migration blockers: NFSv3, HNS/archive-tier. Checked by C10 before R2.
12. Storage-account keys aren't the access path: extension uses AAD (`useAAD: true`); shared-key is pure unused attack surface unless proven otherwise.

### 9. LLM Execution Prompt (Paste vErbatim above the rEport)

> You are executing SPEC-FTFL-525 v1.0 (attached) against the attached audit report. Evaluate every check C1–C19 in order. Output exactly three sections: (1) Findings table—check ID, PASS/FAIL/REVIEW/UNKNOWN, one-line evidence quoting the report field; (2) Remediation plan—only templates triggered by FAILs, in dependency order, with all `{{VARS}}` substituted from report section S13, each with its verification step from §6; (3) Escalations—items the operator cannot self-serve, with the named contact from S11. Rules: do not invent resources, values, or commands not present in the spec or report; mark missing data UNKNOWN and state the exact command that would resolve it; do not re-raise the 10 km compliance question; British English.

### 10. Site Tracker

| Site | Tenant confirmed | Audit run | CRIT clear | R2 (ZRS) | R6 (lockdown) | Notes |
|---|---|---|---|---|---|---|
| MKUH | ✅ `subcr-sde-prd` | ✅ 2026-07-01/02 (interactive, pre-script) | R1 applied by Joao Andre 01/07—V1 verification still pending | In progress (started 02/07) | Gated—R5 done, awaiting sign-off | C16/C17 (vault redundancy, snapshot SKUs) never checked—first script run should backfill |
| NNUH | ☐ | ☐ | ☐ | ☐ | ☐ | Ollie suspects same public-exposure pattern |
| CUH | ☐ | ☐ | ☐ | ☐ | ☐ | Ollie's ticket comment suggests already OK—verify anyway |

---

_Spec changes require a version bump and a line here: v1.0—initial, distilled from the MKUH investigation of 2026-07-01/02._
