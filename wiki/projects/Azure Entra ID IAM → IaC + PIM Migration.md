---
created: 2026-05-23T12:52:00+00:00
entity_kind: project
modified: 2026-07-23T21:05:42+00:00
permalink: llmeon/wiki/projects/azure-entra-id-iam-ia-c-pim-migration
sources: [raw/2026-05-23-pieces-natural-planning-model.md]
tags: [dossier, wiki]
title: Azure Entra ID IAM → IaC + PIM Migration
wiki_type: dossier
---

## Summary

High-stakes project to restructure Azure Entra ID Identity and Access Management by migrating all configuration to Infrastructure as Code (Terraform or Bicep), implementing Privileged Identity Management (PIM) for all elevated access, and tidying stale policies. A break-glass account blueprint has been defined as a prerequisite before any changes are made.

## Key Facts

- Goal: Move Entra ID configuration to IaC, implement PIM for privileged access, tidy stale policies—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Drivers: Post-audit requirements, stopping portal config drift, achieving Zero Trust architecture—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Non-negotiables: All IAM changes via pull request; no standing privileges for any human user; cloud-only break-glass account excluded from all Conditional Access policies—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Success vision: All Conditional Access, App Registrations, Enterprise Apps in Terraform/Bicep; PIM gates all elevation; standing Global Admin eradicated—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Phasing: Phase A: Audit & tidy (export assignments, delete dead weight manually) → Phase B: Break-glass + baseline alerting → Phase C: PIM rollout (eligible roles, approval workflows) → Phase D: Codification (write IaC, import existing state)—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Current state concerns: Stale guest accounts, undocumented security groups, conflicting Conditional Access policies—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Next action identified: Run PowerShell script to export CSV of all Global Admin + Privileged Role Admin assignments, OR create empty git repo for Entra IaC project—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Tooling decision pending: Terraform (AzureAD provider) vs Bicep—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- Risk: Malformed IaC deployment could delete a core Conditional Access policy; strict PIM could block automated overnight deployments—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 201d6e29-282f-4295-8bf1-44282a6752d3)

### Break-Glass Account Blueprint (Prerequisite)

Before any Entra/Conditional Access changes, two emergency access accounts must be created:

- Cloud-only on `*.onmicrosoft.com` domain (never federated, never on-prem synced)
- Standing Global Administrator (NOT behind PIM)
- Excluded from ALL Conditional Access policies
- Credentials: 30+ char random password + FIDO2 hardware key (YubiKey), stored in physical safe with split-knowledge protocol
- Monitoring: Azure Monitor alert on Entra ID Sign-in logs filtered by break-glass Object IDs, routed to PagerDuty/Opsgenie + dedicated Slack/Teams channel, firing within seconds
- 90-day drill: test sign-in, verify tripwire fires, immediately rotate credentials after each drill—[[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)

## Timeline

- 2026-05-23: Project scoped using Natural Planning Model; break-glass blueprint prerequisite defined

## Connections

- [[wiki/projects/K8s Cluster Stress Testing with OMOP Data]]—sister project from same planning session
- [[SOT - CI-CD Pipelines|CI/CD Pipelines]]—sister project from same planning session

## Contradictions

None identified.

## Open Questions

- Terraform vs Bicep for Entra IaC—which tool to use?
- Who owns current policies and must approve deletion/refactoring?
- How will CI/CD pipeline authenticate to Entra without creating a security risk?
- What is the communication plan for engineering/IT teams about login workflow changes?
- How many stale guest accounts and undocumented groups currently exist?
