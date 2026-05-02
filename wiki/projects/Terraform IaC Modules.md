---
title: Terraform IaC Modules
wiki_type: dossier
entity_kind: project
created: 2026-04-30T06:04:37+00:00
modified: 2026-04-30T13:14:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-04-30-pieces-azure-backup-projects
---

## Summary

Infrastructure-as-Code (IaC) project to develop Terraform modules for Azure Backup for AKS deployments. This workstream spans Jira tickets FTFL-596 and FTFL-615, focusing on programmatically handling the three critical dependencies identified during CLI validation: Vault MSI role assignments, AKS cluster MSI role assignments, and trusted access role bindings.

## Key Facts

- The project is tracked under two Jira tickets: FTFL-596 (Backup Config) and FTFL-615 (IaC / Terraform modules).
  > "2. IaC / Terraform (FTFL-596 & FTFL-615): Ensure our Terraform modules programmatically handle the three dependencies identified above" — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- Three Terraform dependencies were identified from the CLI validation work:
  1. Vault MSI → snapshot resource group Contributor role
  2. AKS cluster MSI → snapshot resource group Contributor role
  3. Trusted access role binding with `backup-operator` role
  > "Ensure our Terraform modules programmatically handle the three dependencies identified above: 
    *   Storage/Snapshot RG role assignments for the Vault, AKS, and Extension MSIs." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- The trusted access role binding is the main blocker for the Terraform module development.
  > "The main blocker is that the Terraform module needs to handle the trusted access role binding between the AKS cluster and the backup vault." — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: 5e6f3a96-8c7b-4e3d-9f2a-1b0c9d8e7f6a)

- The trusted access role binding must use the fully qualified source resource type: `Microsoft.DataProtection/backupVaults/backup-operator`.
  > "the only available role is `backup-operator` ... `restore-operator` not being listed" — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a1d8f3a0-4c7b-4b2d-9e28-1e3b9a5c6d7e)

- The modules will be reused for EoE Data Providers including NNUH and MKUH.
  > "prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH)" — [[raw/2026-04-30-pieces-azure-backup-projects]] (Pieces: a89376bd-cdfa-4436-9098-ab10866bef7c)

- A structured LLM prompt was created to audit the Terraform backup module and produce an implementable plan for automating Azure AKS backup via `az dataprotection` CLI.
  > "You are an infrastructure-as-code (IaC) and Azure backup expert. Your mission is to audit an existing Terraform backup module and produce a precise, implementable plan to automate the Azure AKS bac" — [[raw/2026-04-30-pieces-terraform-backup-review]] (Pieces: 1293bd24-54eb-4d21-9746-ef947bce9ca6)

- The prompt includes sections for current state inventory, gaps, proposed changes with new resources, migration plan, and Terraform code snippets in pseudo-HCL blocks.
  > "I want to include sections like the current state inventory, gaps, proposed changes including new resources, and a migration plan with implementation steps. I'll add Terraform code snippets in pseudo-HCL blocks" — [[raw/2026-04-30-pieces-terraform-backup-review]] (Pieces: 588b1723-a6f7-45d7-a381-e7730999559c)

- The prompt maps components to Jira tickets FTFL-596 and FTFL-615, includes acceptance criteria and tests, and references 9 core components (DNS, vaults, RBAC) with 1.26 TB unprotected storage context.
  > "I'll reference the memory, including details like 1.26 TB unprotected storage and 9 components such as DNS, vaults, and RBAC. Each item will require naming, type, current state in Terraform, proposed state, delta, and an HCL snippet" — [[raw/2026-04-30-pieces-terraform-backup-review]] (Pieces: 044c1ba4-b38b-4716-955c-bb6e86767c66)

- Output format specified as "git apply friendly patch" style diffs, with reminders not to create unknown resources.
  > "I'll instruct generating a \"Patch diff\" in a \"git apply friendly patch\" style and remind them not to create unknown resources" — [[raw/2026-04-30-pieces-terraform-backup-review]] (Pieces: 044c1ba4-b38b-4716-955c-bb6e86767c66)

## Timeline

- **2026-04-29**: CLI validation completed; three RBAC/binding dependencies identified for Terraform implementation.
- **2026-04-30**: Terraform module development initiated; trusted access role binding identified as main blocker.

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (parent initiative)
- [[wiki/projects/NNU Azure Backup]] (deployment target)
- [[wiki/projects/MKUH Azure Backup]] (deployment target)
- [[wiki/projects/Azure Backup Restore Runbook]] (operational documentation)
- [[raw/2026-04-30-pieces-azure-backup-projects]]
- [[raw/2026-04-30-pieces-terraform-backup-review]]

## Contradictions

_(none identified)_

## Open Questions

- Should the Terraform module support multiple backup policies or hardcode the `dailyaksbackups` policy?
- Will the module need to support both private endpoint and public endpoint configurations?
- How should the module handle snapshot resource group creation — as part of the module or as an external dependency?
