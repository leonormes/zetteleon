---
created: 2026-06-15T00:00:00+00:00
modified: 2026-07-08T08:12:07+00:00
permalink: llmeon/jira/ftfl-696-phase-0b-overlap-validation
source: FTFL-696
status: in-progress
tags: [federation-precondition, ftfl-696, jira, overlap, phase-0, stress-testing]
title: FTFL-696 Phase 0b Overlap Validation
---

## FTFL-696—Phase 0b: Confirm Person Overlap across 5 Parquet Nodes

Parent: [[FTFL-694 - FFNode Stress Testing Programme]] _The full stress testing programme this Phase 0b ticket belongs to._

| Field | Value |
|-------|-------|
| Priority | Highest |
| Sprint | FITFILE Sprint 25 |
| Effort | 0.5 d |
| Labels | `federation-precondition`, `overlap`, `phase-0` |
| Assignee | Leon Ormes |

---

### 1. Goal

Compute person overlap across the 5 OMOP Parquet node datasets—using `person_source_value` as the cross-node linking key—to validate the overlap distribution (Model C) used in linking stress test generation. This is the L2/L3 federation precondition: the overlap character determines the test strategy for L3 (5-dataset unified-output query).

> ⚠️ Why `person_source_value`, not `person_id`: In OMOP semantics, `person_id` is a dataset-local surrogate key. The same real-world patient will have different `person_id` values in different datasets. The cross-dataset identity is `person_source_value` (the NHS number). Within this generated test data, `person_id` ranges do overlap across linked nodes (each copy gets the same offset range), but the analysis must use `person_source_value` to be semantically correct and to also work for the non-linked dataset where `person_id` ranges are fully disjoint.

---

### 2. Data Sources

All under `services/omop_generator/` in the data-and-analytics repo:

| Path | Description |
|------|-------------|
| `synthea23m_parquet/` | Full single-source dataset: 2,709,803 persons (person_id 1..2,709,803) |
| `synthea23m_nodes/node_{0..4}/` | 5 linked nodes—each ~5.5M persons, overlapping `person_source_value` across nodes (~27.5M total rows, ~13.5M unique virtual persons) |
| `synthea23m_nodes_non_linked/node_{0..4}/` | 5 non-linked nodes—sequential disjoint person_id ranges (~2.7M each, total ~13.5M); `person_source_value` is the only linking key |

#### Generation Context

The linked nodes were produced by `scripts/azure_batch/generate_subsample_synthea.py` which:

- Replicates the 2.7M source patients 5 times (copies) with per-copy `person_id` offsets
- Routes each virtual patient to 1–5 nodes using a Model C probability distribution:

| Nodes per patient | Target % | Category |
|-------------------|----------|----------|
| 1 node | 40% | Single-trust patient |
| 2 nodes | 30% | Two-trust patient |
| 3 nodes | 20% | Three-trust patient |
| 4 nodes | 7% | Four-trust patient |
| 5 nodes | 3% | Complex multi-site patient |

- `person_source_value` is set to `<uuid>-c{copy_idx}`—identical across all nodes a virtual patient appears in, unique across all ~13.5M virtual patients.
- Clinical records are split across a patient's assigned nodes by deterministic hash routing: `hash(pk || '-copy') % n_nodes == node_rank`. No two nodes share the same clinical record for a patient—only the person row is duplicated across nodes.

#### Non-linked Control

The non-linked dataset gives 5 fully disjoint cohorts. Each node gets one copy's worth of patients with disjoint `person_id` ranges—every person appears in exactly 1 node. Cross-node identity resolution requires `person_source_value`.

---

### 3. ✅ Validation Results

#### 3.1 Method

Queried all 5 linked node Parquet files using duckdb with a bitmask signature approach:

```sql
SELECT person_source_value, BIT_OR(1 << node_id) AS mask
FROM (
    SELECT person_source_value, 0 AS node_id FROM 'node_0/person.parquet'
    UNION ALL ...
)
GROUP BY person_source_value
```

Each `person_source_value` gets a bitmask capturing exactly which nodes it appears in (e.g. mask `0b01011` = nodes 0, 1, 3). Grouping by mask gives exclusive counts for every combination in a single pass—no set operations or joins needed.

#### 3.2 Degree Distribution (k=1..5)

| k nodes | Count | % | Target |
|---------|-------|---|--------|
| 1 | 5,417,989 | 39.99% | 40% |
| 2 | 4,068,502 | 30.03% | 30% |
| 3 | 2,706,442 | 19.98% | 20% |
| 4 | 949,855 | 7.01% | 7% |
| 5 | 406,227 | 3.0% | 3% |
| Total | 13,549,015 | 100% | |

Model C is correctly implemented—all bands match target within 0.03 percentage points.

#### 3.3 Exclusive breakdown—all 26 Combinations

##### Pairs (10 combinations)—30.03% of Total

| Nodes | Exclusive Count | % |
|-------|---------------|---|
| 0,1 | 407,220 | 3.01% |
| 0,2 | 407,338 | 3.01% |
| 1,2 | 406,728 | 3.00% |
| 0,3 | 406,458 | 3.00% |
| 1,3 | 405,996 | 3.00% |
| 2,3 | 407,333 | 3.01% |
| 0,4 | 405,668 | 2.99% |
| 1,4 | 407,177 | 3.01% |
| 2,4 | 406,507 | 3.00% |
| 3,4 | 408,077 | 3.01% |

##### Triplets (10 combinations)—19.98% of Total

| Nodes | Exclusive Count | % |
|-------|---------------|---|
| 0,1,2 | 270,191 | 1.99% |
| 0,1,3 | 270,559 | 2.00% |
| 0,2,3 | 271,463 | 2.00% |
| 1,2,3 | 271,013 | 2.00% |
| 0,1,4 | 270,564 | 2.00% |
| 0,2,4 | 270,676 | 2.00% |
| 1,2,4 | 270,308 | 2.00% |
| 0,3,4 | 271,513 | 2.00% |
| 1,3,4 | 270,225 | 1.99% |
| 2,3,4 | 269,930 | 1.99% |

##### Quadruplets (5 combinations)—7.01% of Total

| Nodes | Exclusive Count | % |
|-------|---------------|---|
| 0,1,2,3 | 190,163 | 1.40% |
| 0,1,2,4 | 190,112 | 1.40% |
| 0,1,3,4 | 189,841 | 1.40% |
| 0,2,3,4 | 190,321 | 1.40% |
| 1,2,3,4 | 189,418 | 1.40% |

##### All 5 (1 combination)—3.00% of Total

| Nodes | Exclusive Count | % |
|-------|---------------|---|
| 0,1,2,3,4 | 406,227 | 3.00% |

---

### 4. Acceptance Criteria

- [x] AC1: Overlap stats computed across all 5 Parquet datasets—all 26 exclusive combinations computed by `person_source_value`. Distribution is uniform within each k-level (as expected for random assignment).
- [ ] AC2: Linkage distribution characterised against target—validated Model C perfectly. Target brackets from §4.3 (70–85% single-trust) are a _characterisation guide_, not a model target. Model C intentionally uses 40% single-trust to stress-test the federation.
- [x] AC3: L3 readiness noted—5-dataset unified-output query is feasible. Overlapping `person_source_value` values exist across all 5 nodes; duckdb reads and aggregates 13.5M rows across Parquet files without issue.

---

### 5. Query (For rEproducibility)

```sql
WITH node_sigs AS (
    SELECT person_source_value, BIT_OR(1 << node_id) AS mask
    FROM (
        SELECT person_source_value, 0 AS node_id FROM 'synthea23m_nodes/node_0/person.parquet'
        UNION ALL
        SELECT person_source_value, 1 FROM 'synthea23m_nodes/node_1/person.parquet'
        UNION ALL
        SELECT person_source_value, 2 FROM 'synthea23m_nodes/node_2/person.parquet'
        UNION ALL
        SELECT person_source_value, 3 FROM 'synthea23m_nodes/node_3/person.parquet'
        UNION ALL
        SELECT person_source_value, 4 FROM 'synthea23m_nodes/node_4/person.parquet'
    )
    GROUP BY person_source_value
),
mask_counts AS (
    SELECT mask, COUNT(*) AS cnt
    FROM node_sigs
    WHERE mask > 0
    GROUP BY mask
)
SELECT
    mask,
    bit_count(mask) AS k,
    CASE WHEN (mask & 1)  > 0 THEN '0,' ELSE '' END ||
    CASE WHEN (mask & 2)  > 0 THEN '1,' ELSE '' END ||
    CASE WHEN (mask & 4)  > 0 THEN '2,' ELSE '' END ||
    CASE WHEN (mask & 8)  > 0 THEN '3,' ELSE '' END ||
    CASE WHEN (mask & 16) > 0 THEN '4,' ELSE '' END AS nodes,
    cnt
FROM mask_counts
ORDER BY k, mask;
```

---

### 6. Remaining Items

- [ ] Formalise as reusable script: `scripts/overlap/analyse_person_overlap.py`
- [ ] Condition_occurrence overlap check (expected: 0%—clinical records are hash-routed to one node only)
- [ ] Non-linked node control run
- [ ] Characterise against §4.3 brackets and note in comment on FTFL-696

---

### References

- [FTFL-696 on Jira](https://fitfile.atlassian.net/browse/FTFL-696)
- [[FTFL-694 - FFNode Stress Testing Programme]] _The parent epic ticket._
- [[FTFL-475 Script to generate OMOP synthetic data]] _The original OMOP synthetic data generation ticket._
- [[FTFL-721 - Phase 0c Cohort Design]] _Sibling Phase 0c ticket—cohort design for permutation parameters._
- `Docs/OMOP_SYNTHETIC_DATA_PLAN.md` _Full implementation plan document._
- `scripts/azure_batch/generate_subsample_synthea.py` _The generation script that produced the 5-node datasets._
