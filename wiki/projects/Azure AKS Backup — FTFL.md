---
title: Azure AKS Backup — FTFL
created: 2026-04-29T12:46:00+00:00
modified: 2026-05-01T22:04:48+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-04-29-pieces-azure-aks-backup-ftfl
  - raw/2026-04-30-pieces-aks-backup-iac
  - raw/2026-05-01-pieces-terraform-backup-module-review
  - raw/2026-05-01-pieces-terraform-backup-review
---

## Summary

An infrastructure project to enable and validate Azure Backup for AKS (Azure Kubernetes Service) in the `aks-ff-uks-gp-1` cluster. The work spans three Jira tickets — FTFL-596 (backup configuration), FTFL-599 (restore runbook), and FTFL-615 (Terraform / IaC modules) — and covers end-to-end CLI provisioning, RBAC alignment, trusted access role binding, and Jira documentation. A subsequent production phase on the CUH-DP cluster is tracked separately.

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

- Nine core components created in the validated end-state: (1) hardened storage account `stffuksgp1backup` with container `aks-backups`, (2) private endpoint subnet `snet-ff-uks-gp-pe` (10.0.0.96/27), (3) private endpoint `pe-stffuksgp1backup-blob`, (4) private DNS zone `privatelink.blob.core.windows.net` with VNet link, (5) backup vault `aksbackupvault` in `pentest-1-backup-rg`, (6) snapshot RG `pentest-1-backup-snapshots-rg`, (7) AKS extension `azure-aks-backup`, (8) policy `dailyaksbackups` (daily at 2:00 AM UTC, 14-day retention), (9) trusted access binding `azbkup-trust` with `backup-operator` role.
  > "Hardened backup storage target... Storage account: stffuksgp1backup... Private endpoint subnet: snet-ff-uks-gp-pe (10.0.0.96/27)... Private DNS zone: privatelink.blob.core.windows.net... Azure Backup vault: aksbackupvault in pentest-1-backup-rg" — [[raw/2026-04-30-pieces-aks-backup-iac]] (Pieces: 34008ead-155e-472e-b577-24d57d65eb10)

- Protected namespaces in backup instance scope: `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`, `thehyve`, `thehyve-cuh`, `thehyve-mkuh`. Snapshot volumes enabled. Final state: `ProtectionConfigured`.
  > "Backup instance for aks-ff-uks-gp-1 with included namespaces: barts, ff-a, ff-b, ff-c, spicedb, thehyve, thehyve-cuh, thehyve-mkuh. Snapshot volumes enabled. Final state: ProtectionConfigured" — [[raw/2026-04-30-pieces-aks-backup-iac]] (Pieces: 34008ead-155e-472e-b577-24d57d65eb10)

- IaC action plan defined: Phase 1 (storage + private endpoint + DNS), Phase 2 (vault + extension), Phase 3 (RBAC + trusted access + policy + instance). Terraform modules to reproduce all 9 components for FTFL-596/FTFL-599/FTFL-615.
  > "IaC coverage for Phase 1–3 resources... Implement Terraform modules to reproduce... Hardened storage account... Private endpoint subnet... Private DNS zone... Backup vault... AKS backup extension... Shadow RBAC... Trusted Access binding... Backup policy" — [[raw/2026-04-30-pieces-aks-backup-iac]] (Pieces: 34008ead-155e-472e-b577-24d57d65eb10)

- Validation plan established: DNS resolution to private IP, extension provisioning status, policy association, backup instance `ProtectionConfigured` state, restore point existence, and smoke-test restore in sandbox namespace.
  > "Validate that DNS resolves to private IP from within the VNet... Validate that the AKS extension shows provisioning Succeeded... Validate policy association and that backup instance reaches ProtectionConfigured... Validate that a restore point exists" — [[raw/2026-04-30-pieces-aks-backup-iac]] (Pieces: 34008ead-155e-472e-b577-24d57d65eb10)

- User requested an LLM prompt to review the Terraform backup module and identify gaps between the CLI implementation and what needs to be automated in IaC. The prompt should cover: current state inventory, gaps, proposed changes with HCL snippets, migration plan, and mapping to FTFL-596/FTFL-615.
  > "give me a llm prompt for my ide to review the terraform backup module and work out what needs to change. What do we already have, what needs updating and what needs adding in order to automate the backup we implemented via az cli" — [[raw/2026-05-01-pieces-terraform-backup-module-review]] (Pieces: 464355f2-7b36-4546-889d-0d111422acdf)

- The Terraform review prompt should include: (1) goal section, (2) input files list, (3) expected output format (structured plan + checklist), (4) constraints (Azure provider versions, idempotency), and (5) references to FTFL-596/FTFL-615. Output format should include current state inventory, gaps, proposed changes with pseudo-HCL blocks, migration plan with implementation steps, acceptance criteria, and tests.
  > "The prompt will include sections for the goal, input files, and expected output, such as a structured plan and a checklist of changes... mention constraints like Azure provider versions and idempotency... sections like the current state inventory, gaps, proposed changes including new resources, and a migration plan with implementation steps" — [[raw/2026-05-01-pieces-terraform-backup-module-review]] (Pieces: 4fbea6fd-4068-4046-8517-40bfd58d993f)

- The prompt should reference the 9 core components already implemented via CLI (storage account, private endpoint subnet, private endpoint, private DNS zone, backup vault, snapshot RG, AKS extension, policy, trusted access binding) and ask for a "Patch diff" in "git apply friendly patch" style for each component, showing: naming, type, current Terraform state, proposed state, delta, and HCL snippet.
  > "I'll reference the memory, including details like 1.26 TB unprotected storage and 9 components such as DNS, vaults, and RBAC. Each item will require naming, type, current state in Terraform, proposed state, delta, and an HCL snippet. I'll instruct generating a 'Patch diff' in a 'git apply friendly patch' style" — [[raw/2026-05-01-pieces-terraform-backup-module-review]] (Pieces: 044c1ba4-b38b-4716-955c-bb6e86767c66)

- The Terraform backup module plan was validated against the proven manual CLI end-state (not HCL source) and found to have good coverage of major AKS backup components but requires refinement for safe 1:1 reproduction.
  > "Using the long-term memories from your Azure/Obsidian work on Wednesday Apr 29 — and the plan output you pasted here — this is **mostly aligned with the manual Azure CLI backup implementation**, but it is **not yet a clean/safe 1:1 reproduction**" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 8c980488-a9e5-471d-b2fb-81dfdb85df77)

- Task status review: snapshot resource group is pre-existing; extension installation has partial visibility; policy creation passed; RBAC and trusted access are partial but passed with reduced privileges pending review.
  > "Creating the snapshot resource group isn't something planned; it's pre-existing. The extension installation has partial visibility since config settings aren't visible. The policy creation passed, while the RBAC and trusted access are partial but passed with extra RBAC and fewer privileges to review" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 8ad1dfac-05e1-42f8-941a-f7a099d72d17)

- The backup instance plan does not explicitly show secrets enabled; the Azure portal configuration blade states 'Include Secrets' and should be referenced for clarity on secret backup scope.
  > "The plan doesn't show explicit secrets enabled, which could be important... the configuration blade would be even better since it clearly states 'Include Secrets'" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 67aa67a1-387e-4a04-a48b-b70a09617ead)

- Critical distinction: if targeting the same Testing subscription/resources as April 29, the plan is an IMPORT case not a creation case. The backup instance name matches the manually created instance GUID, confirming import scenario.
  > "If this workspace targets the same Testing subscription and resources as on April 29, the plan isn't safe to apply as-is since it's trying to create resources that already existed... the backup instance name matches the manually created instance GUID, indicating this is likely an import case" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: f7d2c2ce-771c-4547-9d3a-53b1f5605eab)

- Security considerations identified: managed user accounts (MUA) relevance, explicit dependency relationships in resource configurations (especially role assignments and managed identity), and drift/warnings should be documented separately.
  > "I'm considering a few potential issues regarding security levels and whether the managed user accounts (MUA) are relevant. It may be important to explicitly mention the dependency relationships in resource configurations, especially with role assignments and the managed identity" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: bec2f628-5f32-44f9-af7f-4af41adf3660)

- The Terraform backup module plan was validated against the proven manual CLI end-state (not HCL source) and found to have good coverage of major AKS backup components but requires refinement for safe 1:1 reproduction.
  > "Using the long-term memories from your Azure/Obsidian work on Wednesday Apr 29 — and the plan output you pasted here — this is **mostly aligned with the manual Azure CLI backup implementation**, but it is **not yet a clean/safe 1:1 reproduction**" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 8c980488-a9e5-471d-b2fb-81dfdb85df77)

- Task status review: snapshot resource group is pre-existing; extension installation has partial visibility; policy creation passed; RBAC and trusted access are partial but passed with reduced privileges pending review.
  > "Creating the snapshot resource group isn't something planned; it's pre-existing. The extension installation has partial visibility since config settings aren't visible. The policy creation passed, while the RBAC and trusted access are partial but passed with extra RBAC and fewer privileges to review" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 8ad1dfac-05e1-42f8-941a-f7a099d72d17)

- The backup instance plan does not explicitly show secrets enabled; the Azure portal configuration blade states 'Include Secrets' and should be referenced for clarity on secret backup scope.
  > "The plan doesn't show explicit secrets enabled, which could be important... the configuration blade would be even better since it clearly states 'Include Secrets'" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 67aa67a1-387e-4a04-a48b-b70a09617ead)

- Critical distinction: if targeting the same Testing subscription/resources as April 29, the plan is an IMPORT case not a creation case. The backup instance name matches the manually created instance GUID, confirming import scenario.
  > "If this workspace targets the same Testing subscription and resources as on April 29, the plan isn't safe to apply as-is since it's trying to create resources that already existed... the backup instance name matches the manually created instance GUID, indicating this is likely an import case" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: f7d2c2ce-771c-4547-9d3a-53b1f5605eab)

- Security considerations identified: managed user accounts (MUA) relevance, explicit dependency relationships in resource configurations (especially role assignments and managed identity), and drift/warnings should be documented separately.
  > "I'm considering a few potential issues regarding security levels and whether the managed user accounts (MUA) are relevant. It may be important to explicitly mention the dependency relationships in resource configurations, especially with role assignments and the managed identity" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: bec2f628-5f32-44f9-af7f-4af41adf3660)

- The plan shows resource naming duplication issue: "aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5" matches the existing manual backup instance, confirming this is an import scenario not a fresh creation.
  > "the plan is using the name 'aks-ff-uks-gp-1-aks-ff-uks-gp-1-950fac30-43c0-11f1-867c-d20551df63e5,' which matches the existing manual backup instance" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 15f3ce2a-15af-4cf8-9bb4-c1320938bbe0)

- Validation table approach proposed: categorize components by match status (100% = subnet/policy/trusted access; partial = extension/role set; mismatch = storage/vault names needing alignment).
  > "I'm considering how to categorize statuses: a 100% match may include subnet, policy, and trusted access; a partial match could cover extension and role set; while mismatch could cover storage and vault names" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 5afa0154-74ba-4f97-b012-d1502a48628e)

- Immutability configuration discrepancy noted: Terraform plan shows "immutability = Disabled" but portal memory indicates "Immutable vault: Enabled" at two different times during the CLI session.
  > "I'm noticing a potential issue with the configuration of the backup vault. It shows 'immutability = Disabled,' which contradicts the portal memory indicating 'Immutable vault: Enabled' at two different times" — [[raw/2026-05-01-pieces-terraform-backup-review]] (Pieces: 9b567817-4ec6-4296-8543-92133cbe61e0)


## Connections

- [[raw/2026-04-29-pieces-azure-aks-backup-ftfl]]
- [[wiki/projects/Security and Maintenance Roadmap]] (backup/restore is one of the four standing epics)
- [[wiki/projects/CUH-DP AKS Backup — Terraform]] (production continuation: module upgrade & plan remediation)

## Contradictions

_(none identified)_

## Open Questions

- How will the Terraform modules handle the three RBAC/binding dependencies in a declarative way?
- What is the recovery time objective (RTO) / recovery point objective (RPO) target for this backup policy?
