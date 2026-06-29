---
title: FITFILE Testing Infrastructure
wiki_type: dossier
entity_kind: project
created: 2026-05-27 12:13:00+00:00
modified: 2026-05-27 21:30:00+00:00
tags:
- wiki
- dossier
- project
sources:
- raw/2026-05-27-pieces-terraform-aks-upgrade-override
- raw/2026-05-27-pieces-terraform-iac
- raw/2026-05-27-pieces-k8s-deployment
permalink: llmeon/wiki/projects/fitfile-testing-infrastructure
---

## Summary

Operational infrastructure work on the FITFILE Azure testing environment, covering AKS cluster management, Terraform state conflicts, and Kubernetes secrets propagation. The testing cluster (`fitfile-cloud-testing-aks-cluster`) serves as the primary development and integration environment for FITFILE cloud services.

## Key Facts

- **2026-05-27**: Terraform apply against the FITFILE testing AKS cluster failed with `upgrade_override cannot be unset` error on resource `module.azure_public_infrastructure.azurerm_kubernetes_cluster.main` — [[raw/2026-05-27-pieces-terraform-aks-upgrade-override]] (Pieces: 4f80d935-1bc0-44ea-b0e0-3e1c24a07f8d)

- **Root cause**: Provider-state conflict. The AKS cluster has `upgrade_override` set in Azure state, but the Terraform config does not declare it. The Azure provider refuses to "unset" a value present in the real resource.

- **Fix Option 1**: Add explicit `upgrade_settings` block to the `azurerm_kubernetes_cluster` resource to match what Azure state already has — [[raw/2026-05-27-pieces-terraform-aks-upgrade-override]] (Pieces: 8aedc7fd-869c-49d7-8513-a8fffe34bf09)

- **Testing cluster details**: `fitfile-cloud-testing-aks-cluster` in resource group `fitfile-cloud-testing-rg`, subscription `249df46b-f75d-4492-8e78-b33a00473548`, location `uksouth`, SKU Free tier — [[raw/2026-05-27-pieces-terraform-aks-upgrade-override]] (Pieces: 804011cd-efc2-4983-afaf-c59320dcff4b)

- **2026-05-27**: The Hermes LTM confirmed no prior `upgrade_override` fix exists in memory — this is a new problem for the user — [[raw/2026-05-27-pieces-terraform-aks-upgrade-override]] (Pieces: 2786291a-0ade-44d1-9531-2807a745b29b)

- **2026-05-27**: User requested a Hermes-style handoff/transfer prompt for the `upgrade_override` fix (Option 1: adding `upgrade_settings` block explicitly) for use in Cursor, Claude, ChatGPT contexts — [[raw/2026-05-27-pieces-terraform-iac]] (Pieces: 34866d84-dd4d-400b-88a7-bc5012d6b34f)

- **2026-05-27**: User requested a Hermes `/goal` prompt to analyse `https://gitlab.com/fitfile/deployment` using MCP code analysis tools and generate a structured k8s deployment report — [[raw/2026-05-27-pieces-k8s-deployment]] (Pieces: 525cd726-dd4d-400b-88a7-bc5012d6b34f)

## Timeline

- **2026-05-27** — Terraform `upgrade_override` debugging; AKS cluster state investigation; memory search for prior fix attempts.

## Connections

- [[Grafana Alloy Monitoring — FTFL-638]] (same testing cluster; FTFL program)
- [[Azure-AKS]] (parent Azure AKS workstream; CUH cluster vs FITFILE testing cluster)
- [[FITFILE Frontend — Cohort Discovery]] (frontend cohort discovery workstream)
- [[Terraform IaC Modules]] (Terraform module development for AKS)

## Contradictions

_None identified._

## Open Questions

- Has the explicit `upgrade_settings` block been added to the Terraform config for `azure_public_infrastructure`?
- Is the `upgrade_override` fix for the testing cluster also needed for production clusters?
- Are there other provider-state mismatches lurking in the FITFILE testing infrastructure?