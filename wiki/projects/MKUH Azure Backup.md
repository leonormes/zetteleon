---
title: MKUH Azure Backup
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
permalink: llmeon/wiki/projects/mkuh-azure-backup
---

## Summary

Azure Backup configuration project for Milton Keynes University Hospital (MKUH) NHS trust. This initiative is part of the EoE (East of England) Data Providers program, leveraging the infrastructure patterns and Terraform modules developed under FTFL-596 (NNUH) and the broader Azure AKS Backup initiative.

## Key Facts

- MKUH is one of two EoE Data Providers (alongside NNUH) that will receive Azure Backup for AKS infrastructure.
  > "prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)" — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- The Azure CLI commands and provisioning flow validated on `aks-ff-uks-gp-1` cluster will be reused for MKUH deployment.
  > "Leon is asking for the specific Azure CLI commands for setting up Azure Backup for AKS (the managed service offering, not Velero). The cluster in question is `aks-ff-uks-gp-1` in `uksouth`, and the backup vault is `aksbackupvault` in resource group `pentest-1-backup-rg`." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: c5b92f80-3e4a-4d9b-8f2c-7a6e5d4c3b2a)

- The infrastructure sequence, payload requirements, and RBAC permissions established in the pentest environment will inform the MKUH deployment.
  > "Successfully validated the end-to-end CLI provisioning flow for Azure Backup on AKS. This establishes the exact infrastructure sequence, payload requirements, and RBAC permissions necessary to update our backup runbooks and prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- MKUH storage accounts may have `publicNetworkAccess` enabled despite private endpoint configuration — flagged for verification 2026-05-22.
  > "[NNUH and MKUH] storage accounts, although using private endpoint, are available to public network" — [[raw/2026-05-22-pieces-nnuh-mkuh-storage-public-access]] (Pieces: 5e900cc2-d3af-43d1-ab6b-4a0fd9cdd305)

## Timeline

- **2026-04-29**: Infrastructure patterns validated on pentest cluster; MKUH identified as target deployment site.
- **2026-04-30**: Terraform module development underway to support MKUH deployment.
- **2026-05-22**: MKUH storage accounts flagged for public network access verification — `publicNetworkAccess` may be enabled despite private endpoint.

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (parent initiative)
- [[wiki/projects/NNU Azure Backup]] (sister project for Norfolk and Norwich University Hospital)
- [[wiki/projects/Terraform IaC Modules]] (infrastructure-as-code workstream)
- [[raw/2026-04-30-pieces-azure-backup-projects]]

## Contradictions

_(none identified)_

## Open Questions

- What is the target AKS cluster name and resource group for MKUH?
- Will MKUH require a dedicated backup vault or share infrastructure with other trusts?
- Are there MKUH-specific compliance requirements that differ from NNUH?