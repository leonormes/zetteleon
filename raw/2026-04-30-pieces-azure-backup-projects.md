---
title: Azure Backup Projects — NNU, MKUH, Runbook, Terraform
created: 2026-04-30T06:04:37+00:00
source: pieces-ltm
pieces_ids:
  - a89376bd-cdfa-4436-9098-ab10866bef7c
  - 7837b0b0-d338-4679-9322-b7d38f0c6c38
  - 9252a949-01cd-44bd-a5b6-24b32572cd42
  - c05ffae3-308c-4da6-940d-ea12b9babfce
  - 40145348-381a-40fe-b1ea-09a50cbff409
  - 77d9d1e9-75c6-48a9-bfe7-91e42b3321a1
  - ea5e3e20-abc7-4169-86e3-1833af4cf15f
  - 3d8b92b6-9d42-4ad6-afe8-dbbe1b0c7a82
  - 0f6003f2-2188-4cf9-b967-64a3adee35b1
  - 8b1af49b-67e9-4a30-9c4b-d82b3c8b9a41
  - a1d8f3a0-4c7b-4b2d-9e28-1e3b9a5c6d7e
  - c5b92f80-3e4a-4d9b-8f2c-7a6e5d4c3b2a
  - 5e6f3a96-8c7b-4e3d-9f2a-1b0c9d8e7f6a
  - 874ed13c-6d5e-4f3a-8b2c-9d7e6f5a4b3c
tags: [raw, pieces]
---

# Pieces LTM Capture — Azure Backup Projects (Last 24 Hours)

This raw note captures activity related to four distinct but interconnected project workstreams emerging from the Azure AKS Backup initiative.

---

## NNU Azure Backup (FTFL-596)

**Pieces IDs:** a89376bd, 77d9d1e9, ea5e3e20, 3d8b92b6, 0f6003f2

> "I'm focusing on configuring Azure backups for NNU, specifically for ticket FTFL-596. My current thoughts revolve around understanding the exact scope of this configuration and what outcomes are expected for the ticket." — Pieces: 77d9d1e9-75c6-48a9-bfe7-91e42b3321a1

> "Successfully validated the end-to-end CLI provisioning flow for Azure Backup on AKS. This establishes the exact infrastructure sequence, payload requirements, and RBAC permissions necessary to update our backup runbooks and prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)." — Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c

> "at 1:21 PM the instance was already listing as `ProtectionConfigured`, and by 1:23 PM you had this confirmed object plus `RULE_NAME=BackupDaily`" — Pieces: 3d8b92b6-9d42-4ad6-afe8-dbbe1b0c7a82

---

## MKUH Azure Backup

**Pieces IDs:** a89376bd, c5b92f80

> "Successfully validated the end-to-end CLI provisioning flow for Azure Backup on AKS. This establishes the exact infrastructure sequence, payload requirements, and RBAC permissions necessary to update our backup runbooks and prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)." — Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c

> "Leon is asking for the specific Azure CLI commands for setting up Azure Backup for AKS (the managed service offering, not Velero). The cluster in question is `aks-ff-uks-gp-1` in `uksouth`, and the backup vault is `aksbackupvault` in resource group `pentest-1-backup-rg`." — Pieces: c5b92f80-3e4a-4d9b-8f2c-7a6e5d4c3b2a

---

## Azure Backup Restore Runbook (FTFL-599)

**Pieces IDs:** a89376bd, 874ed13c, 3d8b92b6

> "1. Runbook Update: Update the Azure Backup restore runbook (FTFL-599) with the verified `az dataprotection` CLI command sequences for initializing config, validating, and checking job status." — Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c

> "Based on today's long-term memory trail and the CLI output you just pasted — with no extra project files attached here beyond that runbook/terminal context — you've now cleared the trusted-access blocker." — Pieces: 874ed13c-6d5e-4f3a-8b2c-9d7e6f5a4b3c

---

## Terraform IaC Modules (FTFL-596 & FTFL-615)

**Pieces IDs:** a89376bd, 5e6f3a96

> "2. IaC / Terraform (FTFL-596 & FTFL-615): Ensure our Terraform modules programmatically handle the three dependencies identified above: 
    *   Storage/Snapshot RG role assignments for the Vault, AKS, and Extension MSIs." — Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c

> "Leon is working on FTFL-596 — setting up AKS backups via a private endpoint on the private test cluster. The main blocker is that the Terraform module needs to handle the trusted access role binding between the AKS cluster and the backup vault." — Pieces: 5e6f3a96-8c7b-4e3d-9f2a-1b0c9d8e7f6a

---

## Additional Context Snippets

**Pieces IDs:** 7837b0b0, 9252a949, c05ffae3, 40145348, 8b1af49b, a1d8f3a0

> "I've successfully provisioned the AKS backup extension and vault. My current focus has been on refining the RBAC permissions and establishing the trusted access role binding, which are critical steps for ensuring seamless backup operations." — Pieces: 7837b0b0-d338-4679-9322-b7d38f0c6c38

> "the only available role is `backup-operator` ... `restore-operator` not being listed" — Pieces: a1d8f3a0-4c7b-4b2d-9e28-1e3b9a5c6d7e

> "extension Succeeded at 11:51 AM, vault existed by 12:03 PM, trusted access binding created successfully at 1:10 PM, and by 1:12 PM it was marked as succeeded" — Pieces: 8b1af49b-67e9-4a30-9c4b-d82b3c8b9a41

---

**End of raw capture.**
