---
created: 2026-04-28T14:12:37+00:00
modified: 2026-04-28T14:14:54+00:00
title: Stress Test Execution Plan
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 3:12 PM_
---

Below is a structured Stress Test Execution Plan synthesized directly from your long‑term memories from Thu Apr 16 (planning work around 9:28 AM–12:08 PM and the team meeting around 2:00–3:00 PM) plus the Jira/Confluence context (notably FTFL‑476 and the Hyve design doc). You've now also confirmed the key precondition: 5 Parquet datasets for 5 nodes are ready.

Relevant anchors from LTM:

- Jira: [FTFL-476 OMOP Stress Testing infra + monitoring](https://fitfile.atlassian.net/browse/FTFL-476) (Grafana/monitoring + multi-DB setup)
- Confluence: [OMOP/The Hyve Design Document](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1993637891/OMOP+The+Hyve+Design+Document?atl_f=PAGETREE)
- Miro board: [NHS Synthetic Data & OMOP Pipeline](https://miro.com/app/board/uXjVLe0zsY8=/?share_link_id=838293664518)

---

## 1) Success Criteria Matrix (explicit + measurable)

Your LTM consistently separates stress testing into Infrastructure, Algorithmic/Workflow, and ETL/Hyve pipeline concerns (esp. Apr 16 discussions about "what aspect are we stress testing?" and the FTFL‑480 permutation framing).

### A. Infrastructure Stress (system + DB + federation)

| What we're proving | Metric(s) to record | Success criteria (measurable) |
|---|---|---|
| Single-node capacity | p50/p95/p99 query latency; DB CPU/mem/IO; error rate | No errors; latency increases predictably (no "cliff") up to full node dataset |
| Multi-node federation limits (up to 5 nodes) | p95 end-to-end latency; cross-node bytes; timeouts | Federation across 2 → 3 → 5 nodes completes without timeout; identify max sustainable concurrency before SLA breach |
| DB "break points" | max connections, lock waits, temp spill, query cancellations | Document the first failing point with exact error + resource snapshot; confirm whether fix is indexing/spec vs architectural limit |
| Reindex / heavy maintenance jobs | peak RSS, temp disk usage, duration | Reindex completes within defined maintenance window OR produces a clear "requires X memory / Y temp disk" spec (this was raised explicitly in your Apr 16 notes about reindexer OOM) |
| Run failure recovery | restart/resume time; partial results; idempotency | A failed run can be re-run without manual DB surgery; all runs produce consistent outputs (RAP/auditability expectation) |

### B. Algorithmic / Workflow Stress (FTFL‑480 Userflow permutations)

| What we're proving | Metric(s) to record | Success criteria (measurable) |
|---|---|---|
| Userflow scales with cohort size | workflow duration by stage; error rate | For each cohort size tier, completion within agreed budget; clear curve for "cost per additional patient" |
| "Scope of extract" impact | rows exported; file sizes; stage timings | Export time correlates with selected tables/fields; identify which tables dominate (expected: CONDITION/DRUG/MEASUREMENT, etc.) |
| Privacy treatment overhead | delta in latency & CPU; suppression counts | Privacy ON does not break referential integrity; overhead quantified (e.g., +X% runtime, +Y% CPU) |
| Multi-source linkage scenarios | correct join counts; duplicate/missed links | Cross-node linkage preserves expected overlap behaviour (the Apr 16 meeting focus: "realistic overlap in cohorts") |

### C. ETL / Hyve Pipeline Scalability (Hyve Doc alignment)

From the Hyve design doc you captured on Thu Apr 16 ~11:48 AM–12:08 PM, the unanswered questions were "what is the output (ideally Postgres)?" and "how long does OMOP take (daily/weekly/hourly updates)?".

| What we're proving     | Metric(s)                              | Success criteria                                                                                                            |
| ---------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Hyve ETL throughput    | patients/hour; rows/hour; stage timing | Establish throughput at 100k / 1M / node-size and extrapolate confidently to 12M (no nonlinear blow-up without explanation) |
| DQD viability at scale | OHDSI DQD pass/fail counts; runtime    | DQD runs complete and failure profile is explainable (not random infra failure)                                             |
| Governance hooks       | opt-out removal counts; k-anon impact  | Synthetic opt-out + privacy steps execute and leave the OMOP dataset internally consistent                                  |

---

## 2) Test Permutation Grid (FTFL‑480 variables)

Your LTM defines these FTFL‑480 permutation variables repeatedly (Apr 16 planning):

- Cohort size
- Selection scope (tables/fields)
- Extract size (LIMIT / bounded export)
- Privacy treatment (k‑anon / nullification ON/OFF)
- Linkage scenarios (single vs multi-source)

To keep this "all combinations" grid finite and actually runnable, you need discrete levels. Here is a complete matrix defined as level-sets (so "all combinations" = cartesian product of these sets).

### Recommended Level Sets (copyable)

- Cohort size (C): `{1k, 10k, 100k, 1M, NodeFull, 5NodeFull}`
- Scope (S):
  - `S1 Minimal`: PERSON + VISIT_OCCURRENCE (+ DEATH if present)
  - `S2 Core clinical`: S1 + CONDITION_OCCURRENCE + DRUG_EXPOSURE + MEASUREMENT
  - `S3 Full-ish`: S2 + PROCEDURE_OCCURRENCE + OBSERVATION + DEVICE_EXPOSURE (whatever your pipeline exports)
- Extract cap (E): `{Uncapped, Capped}` where `Capped` = a hard LIMIT (or row budget) to isolate "query planning" from "data volume transfer"
- Privacy (P): `{Off, On}`
- Linkage scenario (L):
  - `L1 Single node`
  - `L2 Two nodes (with realistic overlap)`
  - `L3 Five nodes (70–85% single trust, 15–30% 2+ trusts, 5–10% complex multi-site)` (this overlap distribution was explicitly discussed in your Apr 16 meeting notes)

### Total Test Count

If you run _every_ combination:
`|C| * |S| * |E| * |P| * |L| = 6 * 3 * 2 * 2 * 3 = 216 test cases`

That's your full permutation grid. In practice, you'll run it in waves (below) to avoid spending a week finding out your dashboard is missing one metric.

---

## 3) Monitoring Requirements (FTFL‑476 + Grafana Dashboard expectations)

Your LTM around FTFL‑476 is explicit: "monitor resource consumption whilst running the OMOP workflows" and "improve the generic workflows monitoring dashboard" ([FTFL‑476](https://fitfile.atlassian.net/browse/FTFL-476)).

### A. Must-have Metrics (per node)

System / container

- CPU: usage %, throttling, load average
- Memory: RSS, working set, OOM kills, page faults
- Disk: read/write throughput, iops, latency, disk full %, temp usage
- Network: bytes in/out, retransmits, cross-node bandwidth during federated runs

Database

- Active connections, queue depth
- Query runtime (p50/p95/p99), timeouts, cancellations
- Lock waits, deadlocks
- Buffer cache hit ratio, temp spill / sort spill
- WAL / log growth and checkpoints (for Postgres), or equivalent in MSSQL
- Index usage and slow query log sampling (top N)

Workflow / application-level

- Run ID, scenario ID (the permutation coordinates C,S,E,P,L)
- Stage timings (e.g., "query build", "execute", "privacy", "export packaging")
- Rows scanned / rows returned / bytes returned
- Error taxonomy: timeout vs OOM vs SQL error vs referential integrity violation

### B. Dashboard Outputs

- A "Run Overview" board: one row per test case with duration, peak CPU/mem, p95 latency, error flag
- A "Bottleneck board": top offenders (queries/tables/stages) by time and IO
- A "Federation board": cross-node network + added latency per additional node

---

## 4) Known Failure Points (from Apr 16 Meeting + "Expanded Analysis" note)

From your Apr 16 ~2:00–3:00 PM meeting synthesis and the "Expanded Analysis…" capture (Apr 17 9:54 AM in your notes), the repeatedly stated/implicit breaking points were:

1. Multi-node federation cliffs
   - "When does the OMOP flow break regarding node/database count and dataset sizes?"
   - Network bandwidth sufficiency across 5 nodes
2. DB reindexer / heavy maintenance OOM
   - "Will the OMOP reindexer task run out of memory…?"
3. Privacy treatment destroying referential integrity
   - Your Hyve overlap notes: destructive masking/nullification must preserve joins
4. Algorithmic tracing / linkage bottlenecks
   - Especially if you force "messy" demographics to exercise the expensive stages (your earlier MPS planning made this a central risk)
5. Vocabulary / concept mapping gaps
   - UK-specific coding (SNOMED/dm+d) lacking standard OMOP equivalents → downstream query weirdness or DQD failures
6. Run failure recovery for long jobs
   - LTM flags "strategy for resuming" long runs; even if your current Parquet is done, the stress harness must still be restartable and auditable

---

## 5) Hyve Integration Questions These Tests Must Answer (Confluence alignment)

Directly aligned to [OMOP/The Hyve Design Document](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1993637891/OMOP+The+Hyve+Design+Document?atl_f=PAGETREE) (captured in your LTM on Thu Apr 16 ~11:48 AM–12:08 PM):

1. Throughput & schedule feasibility
   - If Hyve runs weekly (per doc), what's the runtime for node-sized updates? What's the max feasible cadence?
2. Operational resource envelope
   - Memory/disk/network requirements for the ETL + DQD + governance stages
3. Output contract
   - Confirm the practical output target (Postgres OMOP DB) and the time/effort to materialize it from Parquet/CSV
4. Governance correctness under load
   - Opt-out scanning + k-anonymity/small-number suppression behaviour at scale (and its impact on joins + counts)
5. Observability requirements
   - What logs/metrics Hyve emits and how they map into your Grafana dashboards (the doc explicitly calls for a dedicated logging workshop)

---

## 6) Data Quality Validation (WhiteRabbit + Achilles + "don't Test garbage" gate)

Your LTM makes it clear the stress test is only meaningful if each node's dataset is internally coherent and OMOP-shaped, even if you accept "not clinically perfect" realism (Ollie's Apr 16 stance: "realistic overlap in cohorts–not realistic data").

### Pre-flight Quality Gates (run before Any load)

Schema & integrity

- OMOP CDM v5.4 table presence + required columns
- PK uniqueness + FK consistency checks (at least for PERSON ↔ clinical tables)
- Concept ID sanity: % standard concepts, % concept_id=0, deprecated concepts

Achilles (distribution sanity)

- Run Achilles (or equivalent concept distribution stats, which you referenced as a desired artefact in your planning) per node:
  - row counts per table
  - top concepts per domain
  - person counts per clinical table
  - visit distribution sanity checks

WhiteRabbit (profiling sanity)

- Generate scan reports per node:
  - field null rates
  - value frequency distributions
  - "weirdness" detection (e.g., all DOB same day)

DQD (optional but ideal if you're matching Hyve expectations)

- Run OHDSI Data Quality Dashboard on a smaller tier first (e.g., 100k / 1M) to validate the harness, then scale.

Overlap validation (critical for your 5-node design)

- Compute overlap stats:
  - % persons appearing in 1 node vs 2 nodes vs 3+ nodes
  - confirm it matches the target distribution you discussed (70–85% / 15–30% / 5–10%)

---

## Stress Test Execution Plan (end-to-end)

### Phase 0—Register the Assets (0.5 day)

Inputs: your 5 Parquet datasets (one per node).
Outputs: a manifest:

- dataset version, vocab version (if known), row counts, checksum
- node ID mapping

### Phase 1—Pre-flight Quality Gates (1–2 days)

Run: Schema checks + overlap stats + Achilles/WhiteRabbit.
Stop condition: any node failing integrity gates blocks load tests until fixed (otherwise you only learn "garbage in, garbage out").

### Phase 2—Baseline Single-node Performance (1–2 days)

Run permutation subset:

- C ∈ {1k, 10k, 100k, 1M, NodeFull}
- S ∈ {S1, S2}
- P=Off
- L=L1
Purpose: establish "normal" curves and calibrate monitoring.

### Phase 3—Full Permutation Waves (3–7 Days, parallelizable)

Run the 216-case grid in waves:

1. add privacy (P=On)
2. add scope (S3)
3. add federation (L2 then L3)
Output: a ranked list of breaking points with exact reproduction coordinates (C,S,E,P,L).

### Phase 4—Hyve/ETL Aligned Runs (2–5 Days, Depending on Tooling readiness)

If you can route Parquet → Hyve pipeline (or Parquet→CSV→Hyve), run:

- 100k, 1M, NodeFull
Capture throughput, DQD profile, opt-out/privacy steps, and resource envelope.

### Phase 5—Report out (0.5–1 day)

Deliverables:

- "Where it breaks" table (first failure per dimension)
- Recommended infra specs per node (CPU/mem/disk/network)
- Recommended DB/indexing changes vs architectural constraints
- Dashboard screenshots + run manifests for auditability (RAP expectation)

---

### Expected Completion Timeline (pragmatic)

Assuming monitoring is in place (or minimally sufficient):

- ~1 week to get meaningful answers (Phases 0–3, with partial grid)
- ~2 weeks to complete full grid + Hyve-aligned ETL runs and produce a polished report

---

### Two Quick Clarifiers (so the Plan locks)

1. For your 5 Parquet node datasets, do you already have overlap engineered (same Person_ID across nodes), or are they currently disjoint? That determines whether L2/L3 are true "linkage" tests or just "federated volume" tests.
2. What's your intended query harness for the "OMOP userflow" (FTFL‑480): is it the FITFILE workflow runner, direct SQL scripts, or a tool like Atlas/Achilles-driven queries? This affects what we define as "Selection Scope" concretely.
