---
title: Azure AKS
wiki_type: dossier
entity_kind: project
created: 2026-05-12T22:07:56+0000
modified: 2026-05-21T13:30:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-12-pieces-azure-aks
  - raw/2026-05-21-pieces-cuh-azure-aks
  - raw/2026-05-21-pieces-cuh-azure-aks-1
---

The **Azure AKS** workstream covers Kubernetes cluster management on Azure, with a focus on the CUH (Colchester University Hospital) Foundation Trust environment. This page tracks the project's scope, timeline, and key facts.

## Key Facts

- CUH AKS cluster: `aks-ff-uks-gp-01` in subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541`, resource group `rg-ff-uks-gp-net` / `rg-ff-uks-gp-aks`, location `uksouth`, SKU Free tier — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: e3a40c5d-1ff)
- The CUH jumpbox VM is named `FITFILEJumpbox` (not `vm-ff-uks-gp-jumpbox`) in resource group `rg-ff-uks-gp-net` — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: 9606afb5-85a)
- Bastion host `bas-ff-uks-gp` was investigated but found to NOT exist in `rg-ff-uks-gp-net` subscription (`709f3d57`); it exists in a different subscription (`7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` — FitFile subscription) — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: d9561ded-a35)
- `az network bastion list` returned EMPTY — no Bastion hosts exist anywhere in the CUH subscription — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: b2a21040-573)
- `AzureBastionSubnet` does NOT exist in `vnet-ff-uks-gp-01` — this is a prerequisite for Azure Bastion — [[raw/2026-05-21-pieces-cuh-azure-aks]] (Pieces: b2a21040-573)
- There is a naming/resource confusion pattern: the agent repeatedly mixed up `NNUHFT-SDE-Networking` (wrong tenant) with `rg-ff-uks-gp-net` (correct CUH resource group) — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: c072bc97-9fc, 13de5368-25e, e6ba010c-413)
- The user's chezmoi repo is at `~/Documents/LeonLM/` with worktree on branch `master` — [[raw/2026-05-21-pieces-cuh-azure-aks-1]] (Pieces: cd6387d0-d7c)

## Timeline

- **2026-05-12** — Project identified via Pieces LTM ingest; initial activity captured.
- **2026-05-21** — Active investigation of CUH AKS cluster access via Azure Bastion; discovered Bastion resource not found due to subscription mismatch.

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
