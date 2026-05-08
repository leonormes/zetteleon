---
created: 2026-05-07T09:00:00+01:00
modified: 2026-05-07T09:28:28+00:00
tags: [ffnodes, ftfl, head, meeting, omop, stress-testing]
title: HEAD FFNode Stress Testing — Meeting 2026-05-07
---

## FFNode Stress Testing—Meeting 2026-05-07

### Meeting Purpose

Align the team on the FFNode / OMOP Stress Test execution plan. Output: a concrete test plan with phase assignments and a set of Jira tickets to drive the work.

---

### Context (from LTM + Vault)

#### Where We Are

- 5 Parquet datasets (one per node) are ready for stress testing.
- ~6 weeks of architectural planning captured since early April (see: [[wiki/projects/12 Million Patient Synthetic NHS-OMOP Pipeline]]).
- Key planning sessions: Thu Apr 16, 9:28 AM–12:08 PM (test dimensions) + 2:00–3:00 PM (team alignment on failure hypotheses).
- OMOP/The Hyve Design Document established ETL expectations: [Confluence](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1993637891/OMOP+The+Hyve+Design+Document?atl_f=PAGETREE)
- Miro board: [NHS Synthetic Data & OMOP Pipeline](https://miro.com/app/board/uXjVLe0zsY8=/?share_link_id=838293664518)

#### Existing Jira Tickets

| Ticket | Description |
|---|---|
| FTFL-475 | Script to generate OMOP synthetic data |
| FTFL-476 | OMOP Stress Testing—infra + monitoring |
| FTFL-479 | Database ingestion script |
| FTFL-480 | OMOP Stress Testing—script to create test userflows |
| FTFL-488 | Synthetic OMOP data storage |

#### Three Test Dimensions (established Apr 16)

1. Infrastructure Stress—System / DB / federation limits
2. Algorithmic / Workflow Stress—FTFL-480 userflow permutations
3. ETL / Hyve Pipeline Scalability—Throughput, governance, DQD

---

### Testing Plan

#### Permutation Grid (FTFL-480)

Variables and level sets—full grid = 216 test cases:

| Variable | Levels |
|---|---|
| Cohort size (C) | 1k, 10k, 100k, 1M, NodeFull, 5NodeFull |
| Scope (S) | S1 Minimal (PERSON + VISIT), S2 Core clinical (+CONDITIONS/DRUGS/MEASUREMENTS), S3 Full (+PROCEDURE/OBSERVATION/DEVICE) |
| Extract cap (E) | Uncapped, Capped |
| Privacy (P) | Off, On (k-anonymity + nullification) |
| Linkage scenario (L) | L1 Single node, L2 Two nodes (realistic overlap), L3 Five nodes (70–85% / 15–30% / 5–10%) |

Run in waves—not all 216 at once.

---

#### Phase 0—Register Assets (0.5 day)

- [ ] Produce a dataset manifest: version, vocab version, row counts, checksum, node ID mapping
- [ ] Confirm overlap engineering: are Person_IDs shared across nodes (linkage tests) or disjoint (volume tests)?

---

#### Phase 1—Pre-flight Quality Gates (1–2 days)

Do not start load testing until these pass.

- [ ] OMOP CDM v5.4 table presence + required columns per node
- [ ] PK uniqueness + FK consistency (PERSON ↔ clinical tables)
- [ ] Concept ID sanity: % standard concepts, % concept_id=0, deprecated concepts
- [ ] Run Achilles per node: row counts, top concepts per domain, visit distribution
- [ ] Run WhiteRabbit per node: field null rates, value frequency, "weirdness" detection
- [ ] Overlap validation: confirm 70–85% / 15–30% / 5–10% multi-trust distribution
- [ ] Stop condition: any node failing integrity gates blocks all load tests until fixed

---

#### Phase 2—Baseline Single-Node Performance (1–2 days)

Permutation subset: `C ∈ {1k, 10k, 100k, 1M, NodeFull}`, `S ∈ {S1, S2}`, `P=Off`, `L=L1`

Goal: establish "normal" latency/resource curves; calibrate monitoring dashboards.

- [ ] p50/p95/p99 query latency per cohort size
- [ ] DB CPU / memory / IO per run
- [ ] Confirm reindexer behaviour (OOM risk identified Apr 16)
- [ ] Verify run is restartable / idempotent (RAP/auditability requirement)

---

#### Phase 3—Full Permutation Waves (3–7 Days, parallelisable)

Run 216-case grid in three waves:

Wave A—Add privacy: `P=On` (keep C/S/E/L from Phase 2 baseline)

Wave B—Add scope: `S=S3`

Wave C—Add federation: `L=L2` then `L=L3`

- [ ] Record exact failure coordinates `(C, S, E, P, L)` for each breaking point
- [ ] Document first error per dimension: timeout / OOM / SQL error / referential integrity violation

---

#### Phase 4—Hyve/ETL Aligned Runs (2–5 Days, Tooling permitting)

Requires Parquet → Hyve pipeline (or Parquet → CSV → Hyve) to be ready.

- [ ] Run at `C = 100k, 1M, NodeFull`
- [ ] Capture: throughput (patients/hour, rows/hour), stage timings
- [ ] Run OHDSI DQD and capture pass/fail profile
- [ ] Verify opt-out removal + k-anonymity steps leave OMOP dataset internally consistent
- [ ] Confirm Hyve emits logs/metrics mappable to Grafana dashboards

---

#### Phase 5—Report Out (0.5–1 day)

Deliverables:

- [ ] "Where it breaks" table—first failure per dimension with exact reproduction coordinates
- [ ] Recommended infra spec per node: CPU / memory / disk / network
- [ ] Recommended DB/indexing changes vs architectural constraints
- [ ] Dashboard screenshots + run manifests (RAP auditability expectation)
- [ ] Updated Hyve SLA estimate extrapolated to 12M patients

---

### Monitoring Requirements (FTFL-476)

Three required dashboard panels:

| Panel | Key metrics |
|---|---|
| Run Overview | One row per test case—duration, peak CPU/mem, p95 latency, error flag |
| Bottleneck Board | Top offenders (queries / tables / stages) by time and IO |
| Federation Board | Cross-node network bytes + added latency per additional node |

Must-have metrics per node:

- System/container: CPU %, throttling, RSS, OOM kills, disk IOPS/throughput, network bytes + retransmits
- Database: active connections, query runtime (p50/p95/p99), lock waits, buffer cache hit ratio, temp spill, WAL growth
- Workflow: Run ID, scenario coordinates `(C,S,E,P,L)`, stage timings, rows scanned/returned, error taxonomy

---

### Known Failure Points (from Apr 16 analysis)

| # | Failure Mode | Risk |
|---|---|---|
| 1 | Multi-node federation cliffs—network bandwidth at 5 nodes | High |
| 2 | DB reindexer OOM—heavy maintenance jobs exceed memory | High |
| 3 | Privacy treatment destroying referential integrity—destructive masking breaks joins | High |
| 4 | Algorithmic tracing / linkage bottlenecks—MPS at scale with messy demographics | Medium |
| 5 | Vocabulary / concept mapping gaps—UK SNOMED/dm+d without OMOP equivalents | Medium |
| 6 | Run failure recovery—long jobs not resumable without manual DB surgery | Medium |

---

### Hyve Integration—Open Questions These Tests Must Answer

1. If Hyve runs weekly, what is the runtime for node-sized updates? What is the max feasible cadence?
2. What are the memory/disk/network requirements for ETL + DQD + governance stages?
3. Confirm practical output target (Postgres OMOP DB) and time to materialise from Parquet/CSV.
4. Does governance correctness (opt-out, k-anonymity) hold under load at 1M+ patients?
5. What logs/metrics does Hyve emit—are they mappable to the Grafana stack?

---

### Clarifiers Needed (Pre-Condition for L2/L3 Tests)

- [ ] Overlap engineered?—Are Person_IDs shared across the 5 Parquet node datasets, or are they currently disjoint? (Determines whether L2/L3 are true linkage tests or just federated-volume tests.)
- [ ] Query harness for FTFL-480—Is the test runner: FITFILE workflow runner / direct SQL scripts / Atlas or Achilles-driven queries?

---

### Jira Next Steps

#### New Tickets to Raise (or Sub-tasks under Existing epics)

| Ticket | Summary | Parent | Priority |
|---|---|---|---|
| NEW-1 | Register 5-node dataset manifest (versions, checksums, node IDs) | FTFL-488 | P1 |
| NEW-2 | Confirm / engineer Person_ID overlap across 5 Parquet nodes | FTFL-475 | P1 |
| NEW-3 | Run Achilles + WhiteRabbit pre-flight quality gates per node | FTFL-476 | P1 |
| NEW-4 | Define query harness for FTFL-480 userflow test runner | FTFL-480 | P1 |
| NEW-5 | Build Phase 2 baseline single-node test harness | FTFL-476 | P1 |
| NEW-6 | Implement Run Overview + Bottleneck + Federation Grafana dashboards | FTFL-476 | P1 |
| NEW-7 | Execute Wave A permutation runs (Privacy ON) | FTFL-480 | P2 |
| NEW-8 | Execute Wave B permutation runs (Full scope S3) | FTFL-480 | P2 |
| NEW-9 | Execute Wave C permutation runs (Federation L2 then L3) | FTFL-480 | P2 |
| NEW-10 | Confirm Hyve Parquet → OMOP pipeline readiness for Phase 4 | FTFL-479 | P2 |
| NEW-11 | Run Hyve ETL stress at 100k / 1M / NodeFull + DQD validation | FTFL-476 | P2 |
| NEW-12 | Produce final stress test report + infra spec recommendations | FTFL-476 | P2 |

#### Existing tickets—actions Needed

| Ticket | Action |
|---|---|
| FTFL-476 | Add monitoring dashboard spec (3 panels defined above) as acceptance criteria |
| FTFL-480 | Confirm permutation grid (216 cases, 5 variables) and wave execution order |
| FTFL-475 | Confirm data generation complete; close or move to done if Parquet files are final |
| FTFL-479 | Confirm DB ingestion script targets Postgres; align with Hyve output contract |

---

### Timeline (pragmatic estimate)

| Phase | Duration | Dependency |
|---|---|---|
| Phase 0 (manifest) | 0.5 day | None |
| Phase 1 (quality gates) | 1–2 days | Phase 0 |
| Phase 2 (baseline) | 1–2 days | Phase 1 |
| Phase 3 (full permutations) | 3–7 days | Phase 2 + monitoring ready |
| Phase 4 (Hyve ETL) | 2–5 days | Hyve pipeline readiness |
| Phase 5 (report) | 0.5–1 day | Phases 3 + 4 |
| Total | ~1–2 weeks | |

---

### Sources

- [[wiki/projects/12 Million Patient Synthetic NHS-OMOP Pipeline]]
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]]
- [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces LTM synthesis)
- Jira: [FTFL-476](https://fitfile.atlassian.net/browse/FTFL-476) · [FTFL-480](https://fitfile.atlassian.net/browse/FTFL-480)
