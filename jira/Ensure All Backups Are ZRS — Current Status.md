---
created: 2026-07-07T08:31:57+00:00
modified: 2026-07-07T10:03:43+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-7-2026-9-31am
title: Ensure All Backups Are ZRS — Current Status
type: note
---

## FTFL-525: Ensure All Backups Are ZRS—Current Status

The ticket ([FTFL-525](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281)) is In Progress in FITFILE Sprint 25, assigned to you, reported by Robin Mofakham, covering three NHS sites: MKUH, NNUH, and CUH.

### What's Completed so far

- NNUH—ZRS migration was kicked off around Jul 1 (`az storage account migration start --account-name aksffuksgp0lbackupsa … --sku Standard_ZRS`). A Gemini session noted that once the migration returns `Succeeded`, "the storage requirement for FTFL-525 is formally met for NNUH." This is asynchronous and can take up to 72 hours—worth re-checking with `az storage account migration show` if you haven't confirmed completion yet.
- MKUH—The blocking Tiering failure (`UserErrorMissingVaultMSIPermissionsOnBackupStorageLocation`) was diagnosed and the fix applied: RBAC assignment (`Storage Blob Data Reader`) granted to the Vault MSI and shared-key access disabled (`AllowSharedKeyAccess: false`), per the [AKS Backup Tiering Fix Verification](https://gemini.google.com/app/6e06764146e07ad6) writeup from Jul 3. The actual LRS→ZRS storage-account conversion command for MKUH's `aksmkuhuksprd01bkp01` account still needed to be run as of that session—worth confirming whether that migration has actually been kicked off.

### CUH—where You're Currently Blocked (The Alexis tHread)

- On Jul 6 at 12:47 (BST) you emailed Alexis McKenna (Cambridge University Hospitals NHS Foundation Trust) with subject _"Role assignment needed - AKS backup extension on aks-ff-uks-gp-01"_—the `azure-aks-backup` extension's managed identity needs `Storage Blob Data Contributor` on the backup storage account `aksffuksgp01cuhbackup` (resource group `aks-ff-uks-gp-01-backup-rg`), and you only hold `Contributor` on that subscription so you can't grant it yourself. You gave her the exact `az role assignment create` command to run.
- Root cause behind this ask: the `azure-aks-backup` extension install on `aks-ff-uks-gp-01` had been failing with `Helm installation failed: context deadline exceeded` (seen Jul 2, 14:27)—the extension can't validate its connection to storage without that role.
- Your Jul 6 09:09 standup audio also references creating "another ticket for CUH" and moving it in from the backlog, and your Jul 7 09:04 journal entry notes _"The backups are still not done! This takes ages."_—consistent with CUH still being unresolved as of this morning.
- I found no reply from Alexis in your memory yet—the email at Jul 6 12:47 is the last touch on this thread, roughly 21 hours ago as of now (Jul 7, 09:30 BST).

### What You Should Do

1. Give it a bit more runway before chasing—21 hours isn't unusually long for a role-assignment request, and per her persona profile Alexis is generally proactive/responsive, so she may just not have gotten to it yet.
2. While waiting, make progress elsewhere on the ticket rather than blocking entirely:
   - Confirm the NNUH migration actually hit `Succeeded` status.
   - Kick off (or confirm) the MKUH LRS→ZRS storage conversion now that the RBAC blocker is fixed.
   - Pick up the linked subtask FTFL-749 ("Retrospectively add the evidence of restoration"), which is still sitting untouched in the backlog and doesn't depend on Alexis.
3. If no reply by end of day or tomorrow morning, send a short, polite follow-up nudge referencing the original email and the exact command again—Alexis's pattern (per her persona notes) is to be responsive to direct, low-friction asks, so a brief "just checking if you've had a chance to run this" should be enough rather than escalating.
4. Once she confirms the role assignment, re-run the `az k8s-extension create` for `azure-aks-backup` on `aks-ff-uks-gp-01` to verify the Helm install now completes, then proceed with the ZRS conversion for CUH's storage account the same way you did for NNUH.
