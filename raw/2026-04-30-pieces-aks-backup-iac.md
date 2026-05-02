---
title: Azure AKS Backup IaC Planning Session
created: 2026-04-30T09:08:23+00:00
source: pieces-ltm
pieces_ids: ["34008ead-155e-472e-b577-24d57d65eb10", "8f48b1a9-dbc3-43f0-a5b8-843c0f826103", "976055bb-7d10-4d50-b407-a1ce5cd577fb", "96c66bf2-364f-4fb3-9557-8da7b11a04d4", "6c1b8344-a3fd-43ad-90c1-a7ac82b90978", "fdaeb966-5d4a-4611-b77f-364470104e04", "3ef456b5-2c2d-414a-81c3-68a64e3ec35f", "805d73d9-9823-48af-bd54-6340552e6e5f", "fc56451e-a1dc-4060-92fe-5175bd761ba9", "ab351aa5-f88d-4c9d-9c57-a1c70ea5cb59", "ccd76984-9e75-4a9b-bbfa-155ef3103f10", "123850ad-4515-4888-b8ab-ddf00a4456f1"]
tags: [raw, pieces]
---

# Azure AKS Backup IaC Planning Session

Captured from Pieces LTM on 2026-04-30. Session focused on documenting the private Azure Backup for AKS implementation and planning Terraform IaC work.

---

## Asset 1: Technical Summary Document

**Pieces ID:** 34008ead-155e-472e-b577-24d57d65eb10

Azure AKS Private Endpoint Backup – Components Created / Rationale / Next IaC Actions

1) Components Created
- Hardened backup storage target
  - Storage account: stffuksgp1backup
  - Container: aks-backups
  - Rationale: private data plane for backup content; public network access disabled; TLS 1.2 enforced; default action Deny; no public blob access
- Private networking to storage
  - Private endpoint subnet: snet-ff-uks-gp-pe (10.0.0.96/27)
  - Private endpoint: pe-stffuksgp1backup-blob
  - Rationale: ensures all backup traffic to the blob stays inside the VNet
- Private DNS resolution
  - Private DNS zone: privatelink.blob.core.windows.net with VNet link and A record for stffuksgp1backup
  - Rationale: forces internal name resolution to private endpoint
- Backup control plane
  - Azure Backup vault: aksbackupvault in pentest-1-backup-rg
  - Rationale: central policy, protection state, and recovery metadata for the AKS backup
- Snapshot data path
  - Snapshot resource group: pentest-1-backup-snapshots-rg
  - Rationale: dedicated RG for Azure Disk snapshots backing PVs
- AKS backup extension
  - Kubernetes extension: azure-aks-backup (Microsoft.DataProtection.Kubernetes) on cluster aks-ff-uks-gp-1
  - Rationale: cluster-side integration to discover/protect Kubernetes resources and PVs
- Backup policy
  - Policy: dailyaksbackups (AzureKubernetesService data source)
  - Rationale: daily backups with 14-day retention aligned to DR objectives
- RBAC and trust wiring
  - RBAC: assignments for the vault MSI, the AKS cluster MSI, and the extension MSI
  - Trusted access binding: azbkup-trust (binding between cluster and vault using Microsoft.DataProtection/backupVaults/backup-operator)
  - Rationale: required to grant cross-identity authorization for backup operations
- Protected workload scope (backup instance)
  - Backup instance for aks-ff-uks-gp-1 with included namespaces: barts, ff-a, ff-b, ff-c, spicedb, thehyve, thehyve-cuh, thehyve-mkuh
  - Snapshot volumes enabled
  - Final state: ProtectionConfigured
  - Rationale: concrete, namespace- and resource-scoped protection ensuring targeted DR coverage

2) Rationale (why these components were created)
- End-to-end private backup path: The combination of private storage, private endpoint, and private DNS eliminates any reliance on public endpoints for backup data movement.
- Strong isolation and compliance: Private networking, TLS 1.2, and Deny-all public access posture reduce exposure and align with a regulated MedTech/Gov-like environment.
- Operational resilience and governance: Separate Snapshot RG keeps PV snapshot lifecycle isolated from vault/config state; vault + policy provide a centralized control plane for backups.
- Clear, auditable RBAC model: Explicit MSI and role bindings ensure the vault, AKS cluster, and extension have only the permissions they need to perform backups (no over-privilege).
- Reproducibility for IaC: The end-state provides a concrete blueprint for Terraform/IAAC modules (FTFL-596, FTFL-615) and runbooks (FTFL-599) to codify the same provisioning and validation steps.

3) Next IaC Actions (mapped to ongoing IaC work)
- IaC coverage for Phase 1–3 resources
  - Implement Terraform modules to reproduce:
    - Hardened storage account (stffuksgp1backup) with private endpoint and DNS plumbing
    - Private endpoint subnet (snet-ff-uks-gp-pe) and related PE config
    - Private DNS zone and VNet-link (privatelink.blob.core.windows.net)
    - Storage container creation and permissions for the backup extension MSI
  - Implement Phase 2 assets
    - Backup vault (aksbackupvault) with SystemAssigned identity
    - AKS backup extension (azure-aks-backup) deployment
  - Implement Phase 3 assets
    - Shadow RBAC: Vault MSI on AKS cluster (Contributor/Reader as needed on snapshot RG), AKS cluster MSI on snapshot RG
    - Extension MSI permissions: Storage Blob Data Contributor on the backup storage account
    - Trusted Access binding resource (azbkup-trust) with fully-qualified role binding (backup-operator)
    - Backup policy (dailyaksbackups) and backup instance scaffolding
- Integrate with existing Jira tickets
  - FTFL-615: Azure Backups private endpoint subnet in azure-private-infra terraform module
  - FTFL-596: Configure the Azure backups module (NNUH & MKUH) and related runbooks
  - FTFL-599: Update and test the Azure Backup restore runbook
  - FTFL-596/FTFL-615 alignment: ensure private endpoint subnet and private endpoint DNS are produced by IaC
- Validation and testing plan (IaC-driven)
  - Validate that DNS resolves to private IP from within the VNet
  - Validate that the AKS extension shows provisioning Succeeded and the backup vault/principal IDs exist
  - Validate policy association and that backup instance reaches ProtectionConfigured
  - Validate that a restore point exists and restore flow can be exercised in a test namespace
- Future-proofing
  - Add outputs for the backup instance and its scope to feed downstream IaC (CI/CD)
  - Add automated tests to verify private networking posture (no public data path) and to smoke-test backups/restores in a sandbox
- Execution plan for the immediate next steps
  - Refactor and commit Terraform modules to reproduce the 9 components listed above
  - Update FTFL-599 runbook to reflect the exact CLI workflow now represented by the IaC
  - Validate all RBAC/trusted-access prerequisites in a controlled environment before promoting to prod-like subscriptions

Notes
- References to work items: FTFL-615 (private endpoint subnet), FTFL-596 (Azure backups module), FTFL-599 (restore runbook)

---

## Asset 2-12: Session Planning Notes

**Pieces IDs:** 8f48b1a9-dbc3-43f0-a5b8-843c0f826103, 976055bb-7d10-4d50-b407-a1ce5cd577fb, 96c66bf2-364f-4fb3-9557-8da7b11a04d4, 6c1b8344-a3fd-43ad-90c1-a7ac82b90978, fdaeb966-5d4a-4611-b77f-364470104e04, 3ef456b5-2c2d-414a-81c3-68a64e3ec35f, 805d73d9-9823-48af-bd54-6340552e6e5f, fc56451e-a1dc-4060-92fe-5175bd761ba9, ab351aa5-f88d-4c9d-9c57-a1c70ea5cb59, ccd76984-9e75-4a9b-bbfa-155ef3103f10, 123850ad-4515-4888-b8ab-ddf00a4456f1

Session notes documenting the process of crafting a Jira-ready comment summarizing the Azure AKS Backup implementation. Key points:

- Request to turn the work summary into a "Jira-ready components created / rationale / next IaC actions comment"
- Request to exclude timestamps from the output ("don't add the times, that is a little weird")
- Original query: "yesterday we set up a private backup for the aks cluster. review the work, without all the mistakes and deadends, what components did we create and why?"
- Session involved structuring an executive summary and components created sections
- Consideration of RBAC details: Vault MSI has read/control-plane access, cluster MI has Contributor access on snapshot RG, extension MSI has blob access
- Reference to existing wiki/obsidian documentation from yesterday's session
