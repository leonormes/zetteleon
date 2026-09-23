---
created: 2026-09-23T14:51:06+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-23T14:56:28+00:00
permalink: llmeon/00-inbox/link-report-cue-assessment
source_atoms: '[[tmp_atoms_cue-assessment]]'
status: tmp
title: _link_report_cue-assessment
type: link_report
---

## Link Report: Multi-customer Deployment Review, and an Assessment of CUE

### Summary

- Atoms processed: 24
- Notes created: 24
- Total links made: 46
- Personal library citations added: 0 (lens skipped—this is an internal platform-engineering assessment; the ARCHILLES corpus is general/personal-development leaning and unlikely to independently corroborate CUE/Helm/Terraform-specific claims, so the queries were not run rather than run-and-report-zero)
- Unlinked atoms (no connections found): 0

### Link Map

| Atom | Links | Strongest Connection |
|------|-------|---------------------|
| [[Four-Layer Customer Deployment Pipeline]] | 2 | [[SoT - CUE Configuration]]—extends |
| [[Two Parallel Customer-Onboarding Paths Coexist]] | 2 | [[SoT - Strategy - Helm to CUE Migration]]—extends |
| [[Unvalidated Helm Values Accept Arbitrary Keys Silently]] | 2 | [[SoT - CUE Configuration]]—shared mechanism |
| [[CI Pipeline Validates Nothing About Customer Configuration Changes]] | 2 | [[SoT - Strategy - Helm to CUE Migration]]—extends |
| [[Triple-Escaped Vault Secret Templates Are Hand-Written Per Customer]] | 2 | [[SoT - Pattern - CUE Data Architecture]]—shared mechanism |
| [[Over Half of Customer Configuration Lines Are Exact Duplicates]] | 1 | [[SoT - Generative Infrastructure Configuration Framework]]—contradicts |
| [[Production-Shaped Defaults Mean Omission Silently Selects Production]] | 2 | [[SoT - Pattern - CUE Data Architecture]]—shared mechanism |
| [[A Tenth of Customer-Config Commits Are Repairs to Earlier Commits]] | 1 | [[SoT - Infrastructure Complexity]]—shared mechanism |
| [[CUE Unification Is a Commutative Deep Merge]] | 2 | [[Configuration Unification]]—shared mechanism (near-duplicate) |
| [[CUE Closed Structs Reject Unknown Fields at Build Time]] | 2 | [[Unvalidated Helm Values Accept Arbitrary Keys Silently]]—contradicts |
| [[CUE Is a Second Language With Unusual Semantics]] | 2 | [[SoT - Strategy - Helm to CUE Migration]]—extends |
| [[POC A Is an Unfinished Abandoned Output-Side Schema]] | 1 | [[SoT - CUE Configuration]]—extends |
| [[POC B Generates ~1,150 Lines From 64 Hand-Written Lines]] | 2 | [[SoT - Generative Infrastructure Configuration Framework]]—extends |
| [[POC B Does Not Validate Its Own Generated Output]] | 2 | [[SoT - Generative Infrastructure Configuration Framework]]—contradicts |
| [[Moving Deep-Merge Logic Into Terraform HCL Relocates Complexity to a Worse Place]] | 2 | [[SoT - Generative Infrastructure Configuration Framework]]—contradicts |
| [[A JSON Round-Trip Forces a Hand-Rolled String-Dispatch Interpreter Inside CUE]] | 1 | [[SoT - Generative Infrastructure Configuration Framework]]—extends |
| [[Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies]] | 2 | [[Two Parallel Customer-Onboarding Paths Coexist]]—shared mechanism |
| [[An OCI Push Pattern for CUE Modules Is Already Proven on This Platform]] | 2 | [[Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies]]—extends |
| [[CUE Only Makes Helms Input Trustworthy Not the Template Engine Itself]] | 3 | [[SoT - Strategy - Helm to CUE Migration]]—extends |
| [[Committing Generated Configuration Files Creates a Reviewability Trade-off]] | 1 | [[SoT - Generative Infrastructure Configuration Framework]]—extends |
| [[Three Architectural Options Exist for Where the CUE Boundary Sits]] | 3 | [[Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies]]—extends |
| [[Recommended CUE Adoption Sequence Is Validate Publish Merge Then Generate]] | 3 | [[SoT - Strategy - Helm to CUE Migration]]—extends |
| [[A Hand-Written Helm Schema Is a Cheaper Partial Alternative to CUE]] | 2 | [[Unvalidated Helm Values Accept Arbitrary Keys Silently]]—extends |
| [[Skipping CUE Adoption Beyond Validation Risks a Single-Maintainer System]] | 2 | [[CUE Is a Second Language With Unusual Semantics]]—extends |

### Orphan Atoms (No Links Found)

None.

### Notes for Triage

- Two near-duplicate pairs were flagged rather than silently merged (linking, not authoring, is this pass's mandate): [[CUE Unification Is a Commutative Deep Merge]] vs. the existing [[Configuration Unification]] note, and this whole batch vs. the existing [[SoT - CUE Configuration]] cluster generally—the new notes are the _specific, evidenced_ (this assessment, this platform) layer; the existing SoTs are the _general theory_ layer. Consider whether any of the 24 should be folded into `SoT - CUE Configuration`'s body via [[Knowledge Harvesting & Normalization Agent]] rather than staying standalone.
- [[Moving Deep-Merge Logic Into Terraform HCL Relocates Complexity to a Worse Place]] is flagged by the source document itself as "the single most important finding"—it also carries the strongest `contradicts` edge in this batch (against [[SoT - Generative Infrastructure Configuration Framework]]'s Layer Ownership Rule) and is the one atom most worth a deeper read before triage.
- All 24 notes currently sit in `00_Inbox/` per the pipeline's design, awaiting your triage into `30_Library/`.
