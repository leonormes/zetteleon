---
title: NNU Azure Backup
wiki_type: dossier
entity_kind: project
created: 2026-04-30 06:04:37+00:00
modified: 2026-05-23 00:23:00+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-04-30-pieces-azure-backup-projects
- raw/2026-05-22-pieces-nnuh-mkuh-storage-public-access.md
permalink: llmeon/wiki/projects/nnu-azure-backup
---

## Summary

Azure Backup configuration project for Norfolk and Norwich University Hospital (NNUH) NHS trust. Tracked under Jira ticket FTFL-596, this initiative involves setting up Azure Backup for AKS clusters via private endpoint on a private test cluster, establishing the infrastructure patterns and Terraform modules that will be reused for MKUH and other EoE Data Providers.

## Key Facts

- The project is tracked under Jira ticket FTFL-596, focusing on Azure Backup configuration for NNUH.
  > "I'm focusing on configuring Azure backups for NNU, specifically for ticket FTFL-596." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: 77d9d1e9-75c6-48a9-bfe7-91e42b3321a1)

- The work involves setting up AKS backups via a private endpoint on a private test cluster.
  > "Leon is working on FTFL-596 — setting up AKS backups via a private endpoint on the private test cluster." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: 5e6f3a96-8c7b-4e3d-9f2a-1b0c9d8e7f6a)

- The Terraform module for this project needs to handle the trusted access role binding between the AKS cluster and the backup vault.
  > "The main blocker is that the Terraform module needs to handle the trusted access role binding between the AKS cluster and the backup vault." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: 5e6f3a96-8c7b-4e3d-9f2a-1b0c9d8e7f6a)

- This project is part of a broader initiative to prepare Terraform modules for EoE Data Providers including NNUH and MKUH.
  > "prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)" — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- The validation of end-to-end CLI provisioning flow on the `aks-ff-uks-gp-1` cluster establishes the infrastructure sequence and RBAC permissions needed for NNU deployment.
  > "Successfully validated the end-to-end CLI provisioning flow for Azure Backup on AKS." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- NNUH storage accounts may have `publicNetworkAccess` enabled despite private endpoint configuration — flagged for verification 2026-05-22.
  > "[NNUH and MKUH] storage accounts, although using private endpoint, are available to public network" — [[raw/2026-05-22-pieces-nnuh-mkuh-storage-public-access]] (Pieces: 5e900cc2-d3af-43d1-ab6b-4a0fd9cdd305)

## Timeline

- **2026-04-29**: Initial configuration work on FTFL-596, focusing on understanding scope and expected outcomes.
- **2026-04-29**: End-to-end CLI provisioning validated on `aks-ff-uks-gp-1` pentest cluster.
- **2026-04-30**: Terraform module requirements identified — trusted access role binding is the main blocker.

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (parent initiative covering all FTFL backup tickets)
- [[wiki/projects/MKUH Azure Backup]] (sister project for Milton Keynes University Hospital)
- [[wiki/projects/Terraform IaC Modules]] (infrastructure-as-code workstream)
- [[raw/2026-04-30-pieces-azure-backup-projects]]

## Contradictions

_(none identified)_

## Open Questions

- What is the target deployment timeline for NNUH production environment?
- Are there specific compliance or data residency requirements for NNUH backup data?
- Will NNUH use the same backup policy (daily at 9 PM UTC, 14-day retention) as the pentest cluster?
- **2026-05-22**: NNUH storage accounts flagged as potentially having `publicNetworkAccess` enabled at the Azure portal level despite using private endpoints — needs verification and remediation.