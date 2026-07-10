---
title: FFNode Stress Testing — FTFL-500
description: Stress testing programme for FFNode infrastructure across asset registration,
  pre-flight QA, and single-node baseline testing. Defined in FTFL-500 Epic.
wiki_type: dossier
entity_kind: project
created: 2026-06-12 08:50:00+00:00
modified: 2026-06-15 14:08:00+00:00
tags:
- wiki
- project
- ffnode
- stress-testing
- ftfl
- jira
sources:
- raw/2026-06-12-pieces-ffnode-mcp-proxy
- raw/2026-06-15-pieces-ffnode-refinement-pre-tickets
- 30_Library/200_Projects/2026-06-11-FFNode-Stress-Testing-v5-Full-Document
- 00_Inbox/FFNode-Stress-Testing-Jira-Backlog-REVISED-2026-06-12
- 30_Library/200_Projects/Complete Jira Work Item Text Structure
permalink: llmeon/wiki/projects/ffnode-stress-testing-ftfl-500
---

## Summary

Stress testing programme for the FFNode Kubernetes platform, spawned from the "Stress Testing - next steps" meeting and the **FFNode Stress Testing Design Document v5** (author: Leon Ormes, reviewed by Ollie Rushton). The programme is tracked under FTFL-500 (Epic) in Jira and spans five phases (0–4), with Phase 0–2 planned for the immediate sprint. Hard deadline: 31 July 2026 (AS05 milestone).

## Key Facts

- **Design document:** "FFNode Stress Testing Design Document v5" — authored 7 May 2026, last updated 11 June 2026 — covers objectives, scope, execution plan, and acceptance criteria — [[raw/2026-06-12-pieces-ffnode-mcp-proxy]] (Pieces: 6ed5444d) via [[30_Library/200_Projects/2026-06-11-FFNode-Stress-Testing-v5-Full-Document]]
- **Epic:** FTFL-500 — umbrella epic for the programme; stories link to FTFL-500 rather than existing epics (Option A) OR link directly to existing FTFL-476/480/488/475 (Option B) — per user's validated Jira backlog
- **Phases defined in design doc:** Phase 0 (Asset Registration), Phase 1 (Pre-flight QA Gates), Phase 2 (Single-Node Baseline), Phase 3 (Waves A–D), Phase 4 (Report & AS05 deliverable)
- **Jira backlog (validated):** 12 June 2026 — user produced a corrected and validated backlog identifying: Pieces export omitted Phase 3–4; FTFL-500 epic invention was debatable; FK-integrity table and cohort tier errors corrected — [[00_Inbox/FFNode-Stress-Testing-Jira-Backlog-REVISED-2026-06-12]] (Pieces: 8950f0db)
- **Hard deadline:** 31 July 2026 — AS05 milestone: five-node cohort, ≥2 nodes with ≥500M-row MEASUREMENT tables, full report
- **Primary existing epics:** FTFL-476 (OMOP stress-testing infra + monitoring), FTFL-480 (userflow permutation script)
- **Collaborators:** Ollie Rushton (reviewer), Helena Ahlfors, Robin Mofakham, Philip Russmeyer, Weronika Jastrzębska, Julia Kurps (The Hyve)
- **User-validated structure:** FTFL-501 (Phase 0: Register Assets), FTFL-502 (Phase 1: Pre-flight QA Gates), FTFL-503 (Phase 2: Single-Node Baseline), FTFL-504 (Phase 3 onwards) — [[30_Library/200_Projects/Complete Jira Work Item Text Structure]] (Pieces: 53233e6d)
- **Inbox artifact:** `00_Inbox/FFNode-Stress-Testing-Jira-Backlog-REVISED-2026-06-12.md` — 334-line corrected backlog with Option A (umbrella epic) vs Option B (epicless) decision tree — (Pieces: f967bfdd)
- **Refinement meeting (15 June 2026):** Oliver Rushton proposed two new pre-tickets: (1) Phase00 — Node + Database Setup (dependency for Phase 0 asset registration), (2) Cohort design ticket to design test cohorts matching permutation parameters (depends on data availability) — [[raw/2026-06-15-pieces-ffnode-refinement-pre-tickets]] (Pieces: 1c6b6bf3)
- **Backlog expansion:** The original 5-phase structure (Phases 0–4) is expanding to include Phase00 and a cohort design workstream. The agent generated a full Hermes prompt for Jira ticket creation on 15 June 2026 — [[raw/2026-06-15-pieces-ffnode-refinement-pre-tickets]]

## Timeline

| Date | Event | Source |
|------|-------|--------|
| 2026-05-07 | Design document v1 drafted | [[30_Library/200_Projects/2026-06-11-FFNode-Stress-Testing-v5-Full-Document]] |
| 2026-06-11 | Design document v5 published (reviewed by Ollie) | [[30_Library/200_Projects/2026-06-11-FFNode-Stress-Testing-v5-Full-Document]] |
| 2026-06-12 07:47 | "Stress Testing - next steps" meeting → Jira ticket creation prompted | [[raw/2026-06-12-pieces-ffnode-mcp-proxy]] |
| 2026-06-12 08:34 | Revised/corrected Jira backlog written (Inbox) | [[00_Inbox/FFNode-Stress-Testing-Jira-Backlog-REVISED-2026-06-12]] |
| 2026-06-12 08:34 | Complete Jira Work Item Structure produced (200_Projects) | [[30_Library/200_Projects/Complete Jira Work Item Text Structure]] |
| 2026-06-15 14:03 | Refinement meeting — Oliver Rushton proposes Phase00 + cohort design pre-tickets | [[raw/2026-06-15-pieces-ffnode-refinement-pre-tickets]] |
| 2026-06-15 14:08 | Agent generates Hermes prompt for Jira ticket creation | [[raw/2026-06-15-pieces-ffnode-refinement-pre-tickets]] |
| 2026-07-31 | AS05 milestone deadline | [[00_Inbox/FFNode-Stress-Testing-Jira-Backlog-REVISED-2026-06-12]] |

## Connections

- [[wiki/projects/K8s Cluster Stress Testing with OMOP Data]] — *Related stress testing initiative specifically for OMOP clinical data pipeline workloads under existing epics FTFL-476/480.*
- [[wiki/projects/ffnode Helm Chart Review]] — *Related FFNode infrastructure workstream assessing umbrella chart complexity and library chart migration.*
- [[SOT - CI-CD Pipelines|CI/CD Pipelines]] — *Umbrella project covering FITFILE software delivery practices; stress testing is a sub-workstream.*

## Open Questions

1. Will the FTFL-500 umbrella epic (Option A) be adopted, or will stories link directly to existing epics (Option B)?
2. When will Phase 3 (Waves A–D) and Phase 4 (Report) be scoped into Jira?
3. What is the plan for creating the Confluence-backed Epic descriptions vs the agent-generated text?