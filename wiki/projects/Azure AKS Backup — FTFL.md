---
title: Azure AKS Backup — FTFL
created: 2026-04-29T12:46:00+00:00
modified: 2026-04-29T12:46:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-04-29-pieces-azure-aks-backup-ftfl
---

## Summary

An infrastructure project to enable and validate Azure Backup for AKS (Azure Kubernetes Service) in the `aks-ff-uks-gp-1` cluster. The work spans three Jira tickets — FTFL-596 (backup configuration), FTFL-599 (restore runbook), and FTFL-615 (Terraform / IaC modules) — and covers end-to-end CLI provisioning, RBAC alignment, trusted access role binding, and Jira documentation.

## Key Facts

- Three Jira tickets track this initiative: FTFL-596 (Backup Config), FTFL-599 (Restore Runbook), and FTFL-615 (IaC / Terraform).
  > "1. Runbook Update: Update the Azure Backup restore runbook (FTFL-599)... 2. IaC / Terraform (FTFL-596 & FTFL-615): Ensure our Terraform modules..." — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- The target cluster is `aks-ff-uks-gp-1` in `uksouth`.
  > "at 1:21 PM the instance was already listing as `ProtectionConfigured`, and by 1:23 PM you had this confirmed object plus `RULE_NAME=BackupDaily`" — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: 3d8b92b6-9d42-4ad6-afe8-dbbe1b0c7a82)

- Backup vault name: `aks-ff-uks-gp-1-backup`; snapshot storage account: `stffuksgp1backup`.
  > `{"FriendlyName": "aks-ff-uks-gp-1/aks-ff-uks-gp-1-backup", "Name": "aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5"}` — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: 0f6003f2-2188-4cf9-b967-64a3adee35b1)

- Correct trusted access role is `backup-operator`; `restore-operator` does not exist in this location and causes CLI rejection.
  > "the only available role is `backup-operator` ... `restore-operator` not being listed" — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: a1d8f3a0-4c7b-4b2d-9e28-1e3b9a5c6d7e)

- Three Terraform / IaC dependencies identified:
  1. Vault MSI → snapshot resource group Contributor role
  2. AKS cluster MSI → snapshot resource group Contributor role
  3. `trustedaccess rolebinding` with `backup-operator` role
  > "Ensure our Terraform modules programmatically handle the three dependencies identified above" — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- End-state achieved: backup extension healthy, vault in place, trusted access binding created, validation accepted, instance `ProtectionConfigured`, rule `BackupDaily`.
  > "extension Succeeded at 11:51 AM, vault existed by 12:03 PM, trusted access binding created successfully at 1:10 PM, and by 1:12 PM it was marked as succeeded" — [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]] (Pieces: 8b1af49b-67e9-4a30-9c4b-d82b3c8b9a41)

## Connections

- [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]]
- [[wiki/projects/Security and Maintenance Roadmap]] (backup/restore is one of the four standing epics)

## Contradictions

_(none identified)_

## Open Questions

- How will the Terraform modules handle the three RBAC/binding dependencies in a declarative way?
- What is the recovery time objective (RTO) / recovery point objective (RPO) target for this backup policy?
