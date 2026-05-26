---
created: 2026-04-16T14:41:12+00:00
modified: 2026-05-26T11:44:31+00:00
title: NHS Synthetic Data & OMOP Pipeline Meeting
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Apr 16, 2026 - 3:41 PM_
---

## Summary: NHS Synthetic Data & OMOP Pipeline Meeting (2:00-3:00 PM)

### Meeting Context

Your afternoon meeting with Helena Ahlfors, Oliver Rushton, Robin Mofakham, Pavlo Kotov, Yasir Mansoor, and Weronika Jastrzebska centered on a critical strategic question: how to generate realistic, high-quality OMOP data at scale for the 12-million patient target.

---

### Key Discussions & Decisions

#### 1. The Two-Path Problem

The team grappled with a fundamental architectural choice:

- Synthea Tool: Generates realistic patient data but requires conversion to OMOP format
- Native OMOP Generators: Produce OMOP-formatted data but lack clinical realism

Your Position (strongly stated around 2:42-2:52 PM): You advocated for quality over convenience—realistic OMOP data where a person has comprehensive clinical details properly linked to their Person ID. You expressed concern that generating "crappy data" would undermine credibility with customers who expect authentic OMOP data handling.

#### 2. Use Case Differentiation

The discussion clarified two distinct scenarios:

- Stress Testing: Requires massive volume (billion+ records) for performance benchmarking—doesn't need sophisticated clinical realism
- HIE (Health Information Exchange) Scenarios: Requires authentic OMOP data that mirrors real-world patient complexity—this is what customers will evaluate you against

#### 3. Infrastructure & Scale Planning (Miro Board, 3:25 PM)

Technical specifications crystallized:

- Target: 12 million unique patient identities
- Storage: ~60 TiB total footprint
- Engine: swpc_synthea (UK fork) with NICE guidelines, dm+d codes, SNOMED CT
- Efficiency Gain: Moving from FHIR (~26.4 TiB) to Parquet (~2 TiB) = 13x storage reduction

Open Technical Questions:

- When does the OMOP flow break? (node limits, database numbers, dataset sizes)
- DB spec/indexing ownership (your team vs DBA team?)
- Network bandwidth sufficiency across 5 nodes
- Memory constraints for OMOP reindexer with accurate multi-provider cohorts

#### 4. Patient Distribution Realism

Discussed realistic healthcare utilization patterns:

- 70-85% use one main hospital trust
- 15-30% interact with 2+ trusts
- 5-10% have complex care across multiple hospitals

---

### How This Connects to Today's Earlier Work

Your morning research and documentation sprint (8:33 AM - 12:18 PM) directly fed into this meeting:

#### Morning Foundation (8:33-11:48 AM)

- Deep-dive into [OMOP CDM structure and OHDSI standards](https://www.ohdsi.org/data-standardization/)
- Review of [FITFILE design documents](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2305032194/) by Helena Ahlfors
- Consolidated [requirements documentation](file:///Users/username/path/to/requirements.md) from Jira tickets:
  - [FTFL-475](https://fitfile.atlassian.net/browse/FTFL-475): Synthetic data generation script (12M patients, variable cohort sizes, CSV output)
  - [FTFL-476](https://fitfile.atlassian.net/browse/FTFL-476): Multi-tech DB setup & monitoring
  - [FTFL-479](https://fitfile.atlassian.net/browse/FTFL-479): Database ingestion for PostgreSQL/MSSQL
  - [FTFL-488](https://fitfile.atlassian.net/browse/FTFL-488): Centralized blob storage for vocabularies and CDM data

#### Pre-Meeting Prep (12:18 PM - 2:09 PM)

- Created [Miro diagram prompts](https://miro.com/app/board/uXjVGh4h0_g=/) for visualizing the OMOP pipeline (shared in meeting at 2:06 PM)
- Sent outreach email to Julia Kurps at The Hyve (2:09 PM) seeking expert guidance on large-scale OMOP generation—she confirmed forwarding to their team

---

### Outstanding Actions

1. Immediate: The Hyve response pending—their expertise may resolve the Synthea→OMOP conversion complexity
2. Architecture Decision: Formalize the "two-tier" approach (basic OMOP for stress tests, realistic OMOP for HIE scenarios)
3. Technical Specs: Get answers to the infrastructure questions raised (DB ownership, network bandwidth, reindexer memory)
4. Storage Strategy: Finalize FTFL-488 blob storage design to support both internal testing and customer SDE/Atlas instances

---

### Bottom Line

Today's trajectory moved from theoretical research (morning) → requirements consolidation (midday) → strategic alignment (afternoon meeting). The meeting surfaced a critical tension between pragmatic volume generation and clinical authenticity—your strong stance on quality suggests the team needs a hybrid solution that serves both stress-testing and customer-facing realism requirements.
