---
tags:
- jira
- ftfl-696
- phase-0
- overlap
- federation-precondition
- stress-testing
source: FTFL-696
status: in-progress
created: 2026-07-07T00:00:00+00:00
permalink: llmeon/jira/ftfl-696-phase-0b-overlap-validation
modified: 2026-07-07T09:45:40+00:00
---
# FTFL-696 — Phase 0b: Confirm Person Overlap across 5 Parquet Nodes

**Parent:** [[FFNode Stress Testing — FTFL-500]] *The full stress testing programme this Phase 0b ticket belongs to.*

| Field | Value |
|-------|-------|
| Priority | Highest |
| Sprint | FITFILE Sprint 25 |
| Effort | 0.5 d |
| Labels | `federation-precondition`, `overlap`, `phase-0` |
| Assignee | Leon Ormes |

---

## 1. Goal

Compute **person overlap** across the 5 OMOP Parquet node datasets — using `person_source_value` as the cross-node linking key — to validate the overlap distribution (Model C) used in linking stress test generation. This is the L2/L3 federation precondition: the overlap character determines the test strategy for L3 (5-dataset unified-output query).

> **⚠️ Why `person_source_value`, not `person_id`:** In OMOP semantics, `person_id` is a dataset-local surrogate key. The same real-world patient will have different `person_id` values in different datasets. The cross-dataset identity is `person_source_value` (the NHS number). Within this generated test data, `person_id` ranges do overlap across linked nodes (each copy gets the same offset range), but the analysis must use `person_source_value` to be semantically correct and to work for the non-linked dataset where `person_id` ranges are fully disjoint.

---

## 2. Data Sources

All under `services/omop_generator/` in the data-and-analytics repo:

| Path | Description |
|------|-------------|
| `synthea23m_parquet/` | Full single-source dataset: **2,709,803** persons (person_id 1..2,709,803) |
| `synthea23m_nodes/node_{0..4}/` | **5 linked nodes** — each ~5.5M persons, overlapping `person_source_value` across nodes (~27.5M total rows, ~13.5M unique virtual persons) |
| `synthea23m_nodes_non_linked/node_{0..4}/` | **5 non-linked nodes** — sequential disjoint person_id ranges (~2.7M each, total ~13.5M); `person_source_value` is the **only** linking key |

### Generation context

The linked nodes were produced by `scripts/azure_batch/generate_subsample_synthea.py` which:
- Replicates the 2.7M source patients 5 times (copies) with per-copy `person_id` offsets
- Routes each virtual patient to 1–5 nodes using a **Model C** probability distribution:

| Nodes per patient | Target % | Category |
|-------------------|----------|----------|
| 1 node | 40% | Single-trust patient |
| 2 nodes | 30% | Two-trust patient |
| 3 nodes | 20% | Three-trust patient |
| 4 nodes | 7% | Four-trust patient |
| 5 nodes | 3% | Complex multi-site patient |

- `person_source_value` is set to `<uuid>-c{copy_idx}` — **identical across all nodes** a virtual patient appears in, unique across all ~13.5M virtual patients.
- Clinical records are split across a patient's assigned nodes by deterministic hash routing: `hash(pk || '-copy') % n_nodes == node_rank`. No two nodes share the same clinical record for a patient — only the person row is duplicated across nodes.

### ✅ Spot-check confirmed

A duckdb query grouping by `person_source_value` across all 5 linked nodes returned:

| k nodes | Count | % | Target |
|---------|-------|---|--------|
| 1 | 5,417,989 | 39.99% | 40% |
| 2 | 4,068,502 | 30.03% | 30% |
| 3 | 2,706,442 | 19.98% | 20% |
| 4 | 949,855 | 7.01% | 7% |
| 5 | 406,227 | 3.0% | 3% |

**Model C is correctly implemented** — the distribution is spot-on.

### Non-linked control

The non-linked dataset gives 5 fully disjoint cohorts. Each node gets one copy's worth of patients with disjoint `person_id` ranges — every person appears in exactly 1 node. Cross-node identity resolution requires `person_source_value`.

---

## 3. Acceptance Criteria

- [ ] **AC1: Overlap stats computed across all 5 Parquet datasets** — % of `person_source_value` values appearing in exactly k nodes (PERSON table), and % shared CONDITION records.
- [ ] **AC2: Linkage distribution characterised against target** — validate against Model C: 70–85% single-trust / 15–30% 2+ trusts / 5–10% complex multi-site (§4.3).
- [ ] **AC3: L3 readiness noted** — confirm 5-dataset unified-output query is feasible from the Parquet data using `person_source_value` as join key (§9.3).

---

## 4. Implementation Plan

### 4.1 Build overlap analysis script

Create `scripts/overlap/analyse_person_overlap.py` that:

1. **Reads `person.parquet` from all 5 linked nodes** — collects `person_source_value` per node
2. **Computes per-person node membership** — for each unique `person_source_value`, count how many of the 5 nodes it appears in
3. **Produces overlap distribution** — histogram k=1..5 → count and % of persons
4. **Repeats for `condition_occurrence`** — count unique `person_source_value` distribution in condition records (note: clinical records are hash-routed to exactly one node, so CONDITION overlap should show 0% — only PERSON records are duplicated)
5. **Compares against Model C target** — table of actual vs expected distribution
6. **Repeats analysis on non-linked nodes** as control baseline

**Tech stack:** Use duckdb (already in the venv) — it handles 13.5M rows comfortably with `SET memory_limit`.

### 4.2 Verification

Run the script and verify:
- Linked nodes match Model C: ~40/30/20/7/3%
- Non-linked control: 100% in exactly 1 node (sanity check)
- `§4.3` characterisation: single-trust (k=1) 70–85% — *this is a **test characterisation bracket**, not a target for Model C. Model C has 40% single-trust. The computed distribution should be noted relative to both numbers.*

### 4.3 Document L3 readiness

The existence of overlapping `person_source_value` values across all 5 nodes, and duckdb's ability to read + aggregate 13.5M Parquet rows across nodes, confirms 5-dataset unified-output query is technically feasible. The overlap distribution determines the *character* of the test, not its feasibility.

---

## 5. Deliverables

| Artifact | Description |
|----------|-------------|
| `scripts/overlap/analyse_person_overlap.py` | Reusable analysis script, grouping by `person_source_value` |
| Terminal output | Actual overlap distribution data |
| This note — AC checkboxes updated | Results and confidence assessment |
| L3 readiness statement | One-paragraph summary of 5-dataset query feasibility |

---

## 6. Open Questions / Risks

- **Memory budget:** ~27.5M person rows, 13.5M unique `person_source_value` values — duckdb handles this with 4GB limit.
- **Condition overlap is expected to be 0%** — clinical records are hash-routed to exactly one node. Only PERSON rows overlap by design.
- **Non-linked generation:** Need to confirm how `person_source_value` is set in the non-linked set (likely the same UUID scheme without overlap).

---

## References

- [FTFL-696 on Jira](https://fitfile.atlassian.net/browse/FTFL-696)
- [[FTFL-694 - FFNode Stress Testing Programme]] *The parent epic ticket.*
- [[FTFL-475 Script to generate OMOP synthetic data]] *The original OMOP synthetic data generation ticket.*
- [[FTFL-721 - Phase 0c Cohort Design]] *Sibling Phase 0c ticket — cohort design for permutation parameters.*
- `Docs/OMOP_SYNTHETIC_DATA_PLAN.md` *Full implementation plan document.*
- `scripts/azure_batch/generate_subsample_synthea.py` *The generation script that produced the 5-node datasets.*