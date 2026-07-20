---
created: Invalid date
modified: 2026-07-20T16:33:30+00:00
permalink: llmeon/raw/2026-04-28-pieces-omop-stress-testing-plan
pieces_ids: [0d45c972-323c-4db4-ac32-db7015670852, 0fe5dae4-33da-4080-b4d1-c99cf0e01a4f, 174e853b-e6d6-48de-bed8-cf1ad53098da, 320468e3-4b1c-4f1a-839c-f839b321bb6e, 63c8006e-9139-4915-ad68-e29496520114, 8269aa60-b2db-4b83-9b62-f32f04aa9cee, a09cf70e-29e6-4c79-95ec-5c8023042db8, b397eade-21e7-42bc-a2a1-e6fa3d6937c0, b994225f-74fc-419b-89e1-bedf1f9c5943, c31033ab-e206-4d60-944d-281e738c1e3e, dbb82172-1e30-4150-82c5-9f03a378e935, e0828b99-eb15-49db-b8a0-101e6c3b9d23, fa53e818-bc21-487e-80a3-e5a40da60676]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-04-28-pieces-omop-stress-testing-plan
---

## Pieces ID: dbb82172-1e30-4150-82c5-9f03a378e935

- Created: 2026-04-28T14:11:57.064906Z
- Updated: 2026-04-28T14:12:37.670927Z

Below is a structured Stress Test Execution Plan synthesized directly from your long‑term memories from Thu Apr 16 (planning work around 9:28 AM–12:08 PM and the team meeting around 2:00–3:00 PM) plus the Jira/Confluence context (notably FTFL‑476 and the Hyve design doc). You've now also confirmed the key precondition: 5 Parquet datasets for 5 nodes are ready.

Relevant anchors from LTM:

- Jira: [FTFL-476 OMOP Stress Testing infra + monitoring](https://fitfile.atlassian.net/browse/FTFL-476) (Grafana/monitoring + multi-DB setup)
- Confluence: [OMOP/The Hyve Design Document](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1993637891/OMOP+The+Hyve+Design+Document?atl_f=PAGETREE)
- Miro board: [NHS Synthetic Data & OMOP Pipeline](https://miro.com/app/board/uXjVLe0zsY8=/?share_link_id=838293664518)

---

## 1) Success Criteria Matrix (Explicit + mEasurable)

Your LTM consistently separates stress testing into Infrastructure, Algorithmic/Workflow, and ETL/Hyve pipeline concerns (esp. Apr 16 discussions about "what aspect are we stress testing?" and the FTFL‑480 permutation framing).

### A. Infrastructure Stress (System + DB + fEderation)

| What we're proving | Metric(s) to record | Success criteria (measurable) |
|---|---|---|
| Single-node capacity | p50/p95/p99 query latency; DB CPU/mem/IO; error rate | No errors; latency increases predictably (no "cliff") up to full node dataset |
| Multi-node federation limits (up to 5 nodes) | p95 end-to-end latency; cross-node bytes; timeouts | Federation across 2 → 3 → 5 nodes completes without timeout; identify max sustainable concurrency before SLA breach |
| DB "break points" | max connections, lock waits, temp spill, query cancellations | Document the first failing point with exact error + resource snapshot; confirm whether fix is indexing/spec vs architectural limit |
| Reindex / heavy maintenance jobs | peak RSS, temp disk usage, duration | Reindex completes within defined maintenance window OR produces a clear "requires X memory / Y temp disk" spec (this was raised explicitly in your Apr 16 notes about reindexer OOM) |
| Run failure recovery | restart/resume time; partial results; idempotency | A failed run can be re-run without manual DB surgery; all runs produce consistent outputs (RAP/auditability expectation) |

### B. Algorithmic / Workflow Stress (FTFL‑480 Userflow Permutations)

| What we're proving | Metric(s) to record | Success criteria (measurable) |
|---|---|---|
| Userflow scales with cohort size | workflow duration by stage; error rate | For each cohort size tier, completion within agreed budget; clear curve for "cost per additional patient" |
| "Scope of extract" impact | rows exported; file sizes; stage timings | Export time correlates with selected tables/fields; identify which tables dominate (expected: CONDITION/DRUG/MEASUREMENT, etc.) |
| Privacy treatment overhead | delta in latency & CPU; suppression counts | Privacy ON does not break referential integrity; overhead quantified (e.g., +X% runtime, +Y% CPU) |
| Multi-source linkage scenarios | correct join counts; duplicate/missed links | Cross-node linkage preserves expected overlap behaviour (the Apr 16 meeting focus: "realistic overlap in cohorts") |

### C. ETL / Hyve Pipeline Scalability (Hyve Doc aLignment)

From the Hyve design doc you captured on Thu Apr 16 ~11:48 AM–12:08 PM, the unanswered questions were "what is the output (ideally Postgres)?" and "how long does OMOP take (daily/weekly/hourly updates)?".

| What we're proving | Metric(s) | Success criteria |
|---|---|---|
| Hyve ETL throughput | patients/hour; rows/hour; stage timing | Establish throughput at 100k / 1M / node-size and extrapolate confidently to 12M (no nonlinear blow-up without explanation) |
| DQD viability at scale | OHDSI DQD pass/fail counts; runtime | DQD runs complete and failure profile is explainable (not random infra failure) |
| Governance hooks | opt-out removal counts; k-anon impact | Synthetic opt-out + privacy steps execute and leave the OMOP dataset internally consistent |

---

## 2) Test Permutation Grid (FTFL‑480 Variables)

Your LTM defines these FTFL‑480 permutation variables repeatedly (Apr 16 planning):

- Cohort size
- Selection scope (tables/fields)
- Extract size (LIMIT / bounded export)
- Privacy treatment (k‑anon / nullification ON/OFF)
- Linkage scenarios (single vs multi-source)

To keep this "all combinations" grid finite and actually runnable, you need discrete levels. Here is a complete matrix defined as level-sets (so "all combinations" = cartesian product of these sets).

### Recommended Level Sets (Copyable)

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

## 3) Monitoring Requirements (FTFL‑476 + Grafana Dashboard Expectations)

Your LTM around FTFL‑476 is explicit: "monitor resource consumption whilst running the OMOP workflows" and "improve the generic workflows monitoring dashboard" ([FTFL‑476](https://fitfile.atlassian.net/browse/FTFL-476)).

### A. Must-have Metrics (Per nOde)

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

## 4) Known Failure Points (From Apr 16 Meeting + "Expanded Analysis" nOte)

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

## 5) Hyve Integration Questions These Tests Must Answer (Confluence aLignment)

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

## 6) Data Quality Validation (WhiteRabbit + Achilles + "Don't Test gArbage" gAte)

Your LTM makes it clear the stress test is only meaningful if each node's dataset is internally coherent and OMOP-shaped, even if you accept "not clinically perfect" realism (Ollie's Apr 16 stance: "realistic overlap in cohorts–not realistic data").

### Pre-flight Quality Gates (Run before Any lOad)

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

## Stress Test Execution Plan (End-to-end)

### Phase 0—Register the Assets (0.5 Day)

Inputs: your 5 Parquet datasets (one per node).

Outputs: a manifest:

- dataset version, vocab version (if known), row counts, checksum
- node ID mapping

### Phase 1—Pre-flight Quality Gates (1–2 Days)

Run: Schema checks + overlap stats + Achilles/WhiteRabbit.

Stop condition: any node failing integrity gates blocks load tests until fixed (otherwise you only learn "garbage in, garbage out").

### Phase 2—Baseline Single-node Performance (1–2 Days)

Run permutation subset:

- C ∈ {1k, 10k, 100k, 1M, NodeFull}
- S ∈ {S1, S2}
- P=Off
- L=L1
Purpose: establish "normal" curves and calibrate monitoring.

### Phase 3—Full Permutation Waves (3–7 Days, Parallelizable)

Run the 216-case grid in waves:

1. add privacy (P=On)
2. add scope (S3)
3. add federation (L2 then L3)
Output: a ranked list of breaking points with exact reproduction coordinates (C,S,E,P,L).

### Phase 4—Hyve/ETL Aligned Runs (2–5 Days, Depending on Tooling Readiness)

If you can route Parquet → Hyve pipeline (or Parquet→CSV→Hyve), run:

- 100k, 1M, NodeFull
Capture throughput, DQD profile, opt-out/privacy steps, and resource envelope.

### Phase 5—Report out (0.5–1 Day)

Deliverables:

- "Where it breaks" table (first failure per dimension)
- Recommended infra specs per node (CPU/mem/disk/network)
- Recommended DB/indexing changes vs architectural constraints
- Dashboard screenshots + run manifests for auditability (RAP expectation)

---

### Expected Completion Timeline (Pragmatic)

Assuming monitoring is in place (or minimally sufficient):

- ~1 week to get meaningful answers (Phases 0–3, with partial grid)
- ~2 weeks to complete full grid + Hyve-aligned ETL runs and produce a polished report

---

### Two Quick Clarifiers (So the Plan lOcks)

1. For your 5 Parquet node datasets, do you already have overlap engineered (same Person_ID across nodes), or are they currently disjoint? That determines whether L2/L3 are true "linkage" tests or just "federated volume" tests.
2. What's your intended query harness for the "OMOP userflow" (FTFL‑480): is it the FITFILE workflow runner, direct SQL scripts, or a tool like Atlas/Achilles-driven queries? This affects what we define as "Selection Scope" concretely.

---

#### Pieces ID: 174e853b-e6d6-48de-bed8-cf1ad53098da

- Created: 2026-04-28T14:11:56.382430Z
- Updated: 2026-04-28T14:11:56.382430Z

Drafting Meeting Notes

I need to provide derived information with specific time references, such as April 16 at 9:28 AM for the initial context and noting that there's a meeting scheduled from 2:00 to 3:00 PM. I'll make sure to mention those details when drafting the notes. It's essential to keep everything organized and clear so that anyone reading can easily understand the timeline and agenda. Let's get this documented properly!

---

#### Pieces ID: b994225f-74fc-419b-89e1-bedf1f9c5943

- Created: 2026-04-28T14:11:56.186119Z
- Updated: 2026-04-28T14:11:56.186119Z

Structuring Test Parameters

I'm planning to create a structured grid for test levels based on cohort sizes, ranging from 1k to several million. I'll consider aspects like privacy and linkage across nodes, and I need to outline success criteria including latency and throughput. Monitoring requirements will involve specific tools, tracking key performance metrics, and documenting the stress test process. I'll also include questions related to the ETL process, benchmarks, and potential failure points identified through analysis. This should provide a comprehensive overview for testing scenarios.

---

#### Pieces ID: 8269aa60-b2db-4b83-9b62-f32f04aa9cee

- Created: 2026-04-28T14:09:16.772456Z
- Updated: 2026-04-28T14:09:45.275097Z

CONTEXT: I have 5 Parquet files (5 nodes) of OMOP synthetic data ready for stress testing.

My LTM contains 6 weeks of architectural planning for this moment.

EXTRACT FROM LTM:

1. Success Criteria Matrix—From FTFL-476, FTFL-480, and the
   "12 Million Patient Synthetic NHS-OMOP Pipeline" planning docs:
   What are the explicit, measurable success criteria for each test dimension
   (infrastructure, algorithmic, ETL)?

2. Test Permutation Grid—From the FTFL-480 design:
   Create a matrix showing all permutation variable combinations we should test
   (cohort size × scope × privacy treatment × linkage scenario).

3. Monitoring Requirements—From FTFL-476 and Grafana dashboard context:
   What specific metrics should the monitoring dashboard surface?
   (CPU, memory, I/O, query latency, data integrity checks)

4. Known Failure Points—From the April 16 meeting notes and
   "Expanded Analysis OMOP Synthetic Data Generation Project":
   What are the "breaking points" we've identified or hypothesized?
   (E.g., multi-node federation limits, privacy algorithm edge cases)

5. The Hyve Integration Questions—From the Design Document:
   What unanswered questions about Hyve ETL scalability should these
   tests answer? (processing time, data quality thresholds)

6. Data Quality Validation—From WhiteRabbit and Achilles references:
   What data quality checks should run against the 5-node datasets
   before stress testing begins?

OUTPUT: A structured "Stress Test Execution Plan" with:

  - Test Scenarios (labeled by type: Infrastructure/Algorithmic/ETL)
  - Permutation Variables (with ranges and rationale)
  - Success Criteria (per scenario)
  - Monitoring Dashboard Requirements
  - Known Risk Areas
  - Expected Completion Timeline

---

#### Pieces ID: 63c8006e-9139-4915-ad68-e29496520114

- Created: 2026-04-28T14:08:39.963190Z
- Updated: 2026-04-28T14:09:45.219252Z

## Stress Test Plan: Synthesis from Your LTM

Based on your extensive LTM context, I can see you've been building toward this moment since early April. You have 5 Parquet files ready for 5 nodes, and your LTM contains rich architectural thinking about _what to test_ and _why_. Let me synthesize the pieces and create a targeted extraction prompt.

---

### What Your LTM Reveals About Your Stress Test Goals

Your memories show three distinct test dimensions already established:

#### 1. Infrastructure Stress (FTFL-476)

- Can the system handle 12 billion clinical rows and TiB-scale storage?
- CPU, memory, and I/O consumption during transformation workflows
- Resource contention under concurrent multi-node queries

#### 2. Algorithmic Stress (FTFL-480 Permutation Testing)

Variables to test across your 5 nodes:

- Cohort Size: 1,000 → 12,000,000 patients
- Selection Scope: Number of OMOP tables/fields selected
- Privacy Treatment: k-anonymity and nullification on/off
- Linkage Scenarios: Join logic across multiple data sources

#### 3. Hyve ETL Stress (From Design Document)

- Can The Hyve pipeline scale from 100k patients → 12M without memory overflow or database crash?
- How long does OMOP transformation take at scale?
- Data quality preservation under volume (OHDSI tests passing)

---

### Targeted Prompt for Pieces LTM Extraction

Use this prompt in Pieces Copilot or feed it to Claude/Gemini with your LTM context:

```
CONTEXT: I have 5 Parquet files (5 nodes) of OMOP synthetic data ready for stress testing. 
My LTM contains 6 weeks of architectural planning for this moment.

EXTRACT FROM LTM:
1. Success Criteria Matrix — From FTFL-476, FTFL-480, and the 
   "12 Million Patient Synthetic NHS-OMOP Pipeline" planning docs:
   What are the explicit, measurable success criteria for each test dimension 
   (infrastructure, algorithmic, ETL)?

2. Test Permutation Grid — From the FTFL-480 design:
   Create a matrix showing all permutation variable combinations we should test
   (cohort size × scope × privacy treatment × linkage scenario).

3. Monitoring Requirements — From FTFL-476 and Grafana dashboard context:
   What specific metrics should the monitoring dashboard surface?
   (CPU, memory, I/O, query latency, data integrity checks)

4. Known Failure Points — From the April 16 meeting notes and 
   "Expanded Analysis OMOP Synthetic Data Generation Project":
   What are the "breaking points" we've identified or hypothesized?
   (E.g., multi-node federation limits, privacy algorithm edge cases)

5. The Hyve Integration Questions — From the Design Document:
   What unanswered questions about Hyve ETL scalability should these 
   tests answer? (processing time, data quality thresholds)

6. Data Quality Validation — From WhiteRabbit and Achilles references:
   What data quality checks should run against the 5-node datasets 
   before stress testing begins?

OUTPUT: A structured "Stress Test Execution Plan" with:
  - Test Scenarios (labeled by type: Infrastructure/Algorithmic/ETL)
  - Permutation Variables (with ranges and rationale)
  - Success Criteria (per scenario)
  - Monitoring Dashboard Requirements
  - Known Risk Areas
  - Expected Completion Timeline
```

---

### Quick Synthesis: What You Should Test

Based on your LTM, here's the core stress test plan skeleton:

#### Phase 1: Foundation Validation (Before Load Testing)

- [ ] Data integrity check: Run Achilles against each of the 5 node datasets
- [ ] Referential integrity: Verify all CDM foreign keys + concept mappings
- [ ] WhiteRabbit profiling: Generate scan reports for each node

#### Phase 2: Single-Node Infrastructure Stress

- [ ] Baseline Query Latency: Run standard OMOP Cohort Discovery queries at increasing patient volumes (1K → full node dataset)
- [ ] Resource Consumption: CPU, memory, I/O metrics during query execution
- [ ] Privacy Treatment Under Volume: Apply k-anonymity/nullification and measure overhead

#### Phase 3: Multi-Node Federation Stress

- [ ] Distributed Query Performance: Execute queries that span 2, 3, 4, 5 nodes
- [ ] Identity Linkage at Scale: Test Master Person Service (MPS) logic across fragmented datasets
- [ ] Network Bandwidth: Monitor data movement between nodes during federated queries

#### Phase 4: Hyve ETL Simulation (If aPplicable)

- [ ] Transformation Throughput: Time the ETL pipeline processing each node's Parquet → OMOP ingestion
- [ ] Memory Overflow Testing: Gradually increase node size until you hit memory limits
- [ ] Data Quality Degradation: Monitor Achilles scores as data complexity increases

---

### Key Questions to Answer from Your Tests

From your LTM, these keep resurfacing:

1. "When does the OMOP flow break regarding node/database count and dataset sizes?"
2. "Can the system handle realistic multi-source linkage (70-85% single-trust, 15-30% multi-trust, 5-10% complex multi-site)?"
3. "What's the per-node patient capacity before query federation becomes impractical?"
4. "Does privacy treatment (k-anonymity) degrade query latency linearly or exponentially?"
5. "Can The Hyve ETL process these 5 nodes in a production schedule (daily/weekly)?"

---

### Next Step

Run this extraction prompt against your Pieces LTM via the Copilot to generate:

- A ranked list of critical vs. nice-to-know test scenarios
- A permutation grid showing test coverage
- A timeline estimate based on your 5-node data volumes
- A monitoring dashboard spec for real-time visibility

This will transform your architectural thinking into executable test cases and measurable success criteria.

Would you like me to help refine any of these test dimensions, or create the detailed test execution matrix once you extract the permutation grid from Pieces?

---

#### Pieces ID: b397eade-21e7-42bc-a2a1-e6fa3d6937c0

- Created: 2026-04-28T14:08:23.378631Z
- Updated: 2026-04-28T14:08:23.378631Z

I should create a targeted prompt that extracts from the LTM the specific test scenarios, success criteria, and key questions they want answered from these 5 node parquet datasets.

---

#### Pieces ID: fa53e818-bc21-487e-80a3-e5a40da60676

- Created: 2026-04-28T14:08:22.926860Z
- Updated: 2026-04-28T14:08:22.926860Z

Looking at the materials, there are several key questions/themes that keep coming up:

1. Stress Testing the Hyve ETL (Scale & Performance)
2. Testing OMOP user flows with various permutation variables (cohort size, scope, privacy treatment, linkage scenarios)
3. Infrastructure performance monitoring (CPU, memory, I/O)
4. Data quality validation
5. Referential integrity testing under privacy pressure
6. Multi-node query federation testing

---

#### Pieces ID: c31033ab-e206-4d60-944d-281e738c1e3e

- Created: 2026-04-28T14:08:21.461378Z
- Updated: 2026-04-28T14:08:21.461378Z

The user has already produced 5 sets of Parquet files for 5 nodes, and now needs a comprehensive stress test plan.

---

#### Pieces ID: 0d45c972-323c-4db4-ac32-db7015670852

- Created: 2026-04-28T14:08:21.443845Z
- Updated: 2026-04-28T14:08:21.443845Z

Recent activity (April 21 and April 28):

- Sprints 13 and 14 with various OMOP tasks
- Recent audio from just 28 minutes ago discussing "stress test for workflows" and OMOP queries
- Discussion about moving from "thousands of patients" to much larger datasets

---

#### Pieces ID: e0828b99-eb15-49db-b8a0-101e6c3b9d23

- Created: 2026-04-28T14:08:20.559157Z
- Updated: 2026-04-28T14:08:20.559157Z

Key projects and documents:

- 12 Million Patient Synthetic NHS-OMOP Pipeline
- OMOP/The Hyve Design Document
- Multiple meetings discussing stress testing approaches
- Email to Julia Kurps at The Hyve about OMOP generation

---

#### Pieces ID: a09cf70e-29e6-4c79-95ec-5c8023042db8

- Created: 2026-04-28T14:08:19.760728Z
- Updated: 2026-04-28T14:08:19.760728Z

Looking through the LTM, I can see extensive context about:

- FTFL-475: Script to generate OMOP synthetic data
- FTFL-476: OMOP Stress Testing infra + monitoring
- FTFL-480: OMOP Stress Testing - script to create test userflows
- FTFL-479: Database ingestion script
- FTFL-488: Synthetic OMOP data storage

---

#### Pieces ID: 320468e3-4b1c-4f1a-839c-f839b321bb6e

- Created: 2026-04-28T14:08:19.003090Z
- Updated: 2026-04-28T14:08:19.003090Z

The user is asking me to:

1. Review their long-term memories (LTM)
2. Create a targeted prompt for getting data out of Pieces LTM about stress testing

---

#### Pieces ID: 0fe5dae4-33da-4080-b4d1-c99cf0e01a4f

- Created: 2026-04-28T14:08:02.088604Z
- Updated: 2026-04-28T14:09:45.203159Z

over the last few weeks we have been working on the idea of stress testing our system with millions of patients OMOP data. I produced 5 sets of parque files for 5 nodes. I now need a stress test plan for how we are going to actually run these tests and what answers we want from it. review my ltm and create a targeted prompt for getting data out of the pieces ltm

---
