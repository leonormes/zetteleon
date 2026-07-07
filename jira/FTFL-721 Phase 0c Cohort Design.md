---
created: 2026-06-15T00:00:00+00:00
modified: 2026-07-07T09:50:15+00:00
permalink: llmeon/jira/ftfl-721-phase-0c-cohort-design
source: FTFL-721
status: selected-for-development
tags: [cohort, ftfl-721, jira, permutation, phase-0c, stress-testing]
title: FTFL-721 Phase 0c Cohort Design
---

## FTFL-721—Phase 0c: Cohort Design + Creation for Permutation Parameters

Parent: [[FTFL-694 - FFNode Stress Testing Programme]] _The full stress testing programme this Phase 0c ticket belongs to._

| Field | Value |
|-------|-------|
| Priority | High |
| Sprint | FITFILE Sprint 25 |
| Labels | `cohort`, `permutation`, `phase-0c`, `stress-testing` |
| Assignee | Unassigned |
| Status | Selected for Development |

---

### 1. Goal

Design and create the OMOP cohorts that map to the C (Cohort size) dimension of the six-variable permutation grid from the FFNode Stress Testing Design Document (FTFL-480, §8.1).

#### The Permutation Grid

| Variable | Dimension | Levels |
|----------|-----------|--------|
| C | Cohort size | 1k, 10k, 100k, 1M, NodeFull |
| S | Selection scope | S1, S2, S3 |
| E | Extract cap | Uncapped (Phase 2 baseline) |
| P | Privacy treatment | On / Off |
| X | S3 export | On / Off |
| L | Linkage scenario | L1, L2, L3 |

This ticket covers the C dimension only: designing the cohort SQL/specification for each C tier against the ingested synthetic data, and creating + validating the cohorts inside the node's OMOP database so that Phase 1 QA gates and the Phase 2 harness can reference them directly.

---

### 2. Context

Raised at Backlog Refinement 15 June 2026 by Oliver Rushton:

> _"Extra ticket to design the cohorts to match the permutation parameters—dependency on the data being available."_

Hard dependency: Phase 00 (node + database + data ingestion) must be complete before this ticket is started. Do not begin cohort creation on an empty or partially loaded database.

---

### 3. Acceptance Criteria

- [ ] AC1: Cohort specification document (or inline ticket comment) maps each C tier (1k / 10k / 100k / 1M / NodeFull) to the OMOP `PERSON` and `MEASUREMENT` tables in the ingested data
- [ ] AC2: Cohorts for at least `C = 1k` and `C = 10k` created and validated in the OMOP database and confirmed queryable via FFNode
- [ ] AC3: Cohort SQL / generation scripts committed to version control and the script location referenced in a comment on this ticket
- [ ] AC4: NodeFull cohort size documented (row count of the full `MEASUREMENT` table after ingestion)
- [ ] AC5: Hard dependency confirmed: Phase 00 (node + database + data ingestion) is Done before this ticket is started

---

### 4. Implementation Notes (From rElated Phase 0b wOrk)

- The 5-node Parquet datasets sit under `services/omop_generator/synthea23m_nodes/node_{0..4}/` in the data-and-analytics repo
- Each node has ~5.5M persons, ~10 OMOP tables in Parquet format
- Linking key across nodes is `person_source_value`
- The `measurement` table is the largest (~6.2 GB Parquet, ~200M+ rows in full dataset)—relevant for NodeFull sizing
- Cohort design should consider using duckdb for Parquet-native queries, or via PostgreSQL/MSSQL if ingested into a database

---

### References

- [FTFL-721 on Jira](https://fitfile.atlassian.net/browse/FTFL-721)
- [[FTFL-694 - FFNode Stress Testing Programme]] _The parent epic._
- [[FTFL-696 - Phase 0b Overlap Validation]] _Sibling Phase 0b ticket—overlap distribution across 5 nodes._
- `Docs/FTFL-696-PHASE-0B-OVERLAP-VALIDATION.md` _Phase 0b work doc._
- `scripts/azure_batch/generate_subsample_synthea.py` _The generation script producing the 5-node datasets._
