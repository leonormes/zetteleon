---
permalink: llmeon/wiki/projects/azure-aks
---

---
|title: Azure AKS
wiki_type: dossier
entity_kind: project
created: 2026-05-12T22:07:56+0000
modified: 2026-06-24 15:30:00+00:00
tags:
- wiki
- dossier
- project
sources:
- raw/2026-05-12-pieces-azure-aks
- raw/2026-05-21-pieces-cuh-azure-aks
- raw/2026-05-21-pieces-cuh-azure-aks-1
- raw/2026-06-16-ftfl-657-bastion-direct-aks
- raw/2026-06-16-pieces-ftfl-657-ebs-csi
- raw/2026-06-24-pieces-ftfl-464-calico-cloud-cleanup
permalink: llmeon/wiki/projects/azure-aks
---

The **Azure AKS** workstream covers Kubernetes cluster management on Azure, with a focus on the CUH (Colchester University Hospital) Foundation Trust environment. This page tracks the project's scope, timeline, and key facts.

## Key Facts

- CUH AKS cluster: `aks-ff-uks-gp-01` in subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541`, resource group `rg-ff-uks-gp-net` / `rg-ff-uks-gp-aks`, location `uksouth`, SKU Free tier — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: e3a40c5d-1ff)
- The CUH jumpbox VM is named `FITFILEJumpbox` (not `vm-ff-uks-gp-jumpbox`) in resource group `rg-ff-uks-gp-net` — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: 9606afb5-85a)
- Bastion host `bas-ff-uks-gp` was investigated but found to NOT exist in `rg-ff-uks-gp-net` subscription (`709f3d57`); it exists in a different subscription (`7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` — FitFile subscription) — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: d9561ded-a35)
- `az network bastion list` returned EMPTY — no Bastion hosts exist anywhere in the CUH subscription — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: b2a21040-573)
- `AzureBastionSubnet` does NOT exist in `vnet-ff-uks-gp-01` — this is a prerequisite for Azure Bastion — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: b2a21040-573)
- **FTFL-657** (Spike, Low) — formal investigation ticket to assess using Bastion Direct to private AKS cluster, avoiding Jumpbox SSH/costs. Assigned to Leon. Timebox: 1 day. Test on Sandbox cluster (`aks-ff-uks-gp-1`). Sprint 22 (10–17 Jun 2026). — [[raw/2026-06-16-ftfl-657-bastion-direct-aks]]
- **FTFL-579** (High) — parent security ticket: FITFILEJumpbox allows password-based SSH (azadmin), scored CVSS 7.5, flagged by Prowler and Defender for Cloud. Pen test refinement meeting 14 May 2026 with Oliver Rushton, Robin Mofakham, Leon. — [[raw/2026-06-16-pieces-ftfl-657-ebs-csi]] (Pieces: c44adf14)
- **Bastion Direct approach** — use Azure Bastion native client tunneling (preview) to connect directly to AKS API server private endpoint on port 443, eliminating the jumpbox middleman. Preferred over jumpbox-based SOCKS5 proxy. — [[raw/2026-06-16-pieces-ftfl-657-ebs-csi]] (Pieces: c44adf14)
- There is a naming/resource confusion pattern: the agent repeatedly mixed up `NNUHFT-SDE-Networking` (wrong tenant) with `rg-ff-uks-gp-net` (correct CUH resource group) — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: c072bc97-9fc, 13de5368-25e, e6ba010c-413)
- The user's chezmoi repo is at `~/Documents/LeonLM/` with worktree on branch `master` — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: cd6387d0-d7c)

## Timeline

- **2026-05-12** — Project identified via Pieces LTM ingest; initial activity captured.
- **2026-05-21** — Active investigation of CUH AKS cluster access via Azure Bastion; discovered Bastion resource not found due to subscription mismatch.
- **2026-06-16** — Formal Spike ticket [[FTFL-657]] raised to investigate Bastion Direct to private AKS cluster (Sandbox cluster `aks-ff-uks-gp-1`, 1-day timebox). Agent LTM research completed: full summary delivered including test plan, Bastion Direct technical assessment, FTFL-579 parent context.
- **2026-06-24** — FTFL-464: Investigated Tigera Calico Cloud deployment state on CUH AKS cluster (`aks-ff-uks-gp-01`). Generated 8-phase kubectl investigation guide and Jira ticket comment for Calico Cloud cleanup status. Also executed cleanup on eoe-sde-codisc EKS cluster (related AWS workstream). — [[raw/2026-06-24-pieces-ftfl-464-calico-cloud-cleanup]]

## Connections

- [[Terraform IaC]]
- [[CUH-DP AKS Backup — Terraform]]
- [[Chezmoi]]

## Contradictions

*None identified.*

## Open Questions

- Does the Bastion host need to be created in the CUH subscription, or should the FitFile subscription's Bastion be used?
- Is `AzureBastionSubnet` planned for creation in `vnet-ff-uks-gp-01`?
- What is the exact tenant ID for CUH Foundation Trust?