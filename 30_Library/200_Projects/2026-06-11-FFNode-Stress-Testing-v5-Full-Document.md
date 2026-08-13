---
author: Leon Ormes
created: 2026-06-11T00:00:00+00:00
modified: 2026-08-13T10:53:17+00:00
permalink: llmeon/30-library/200-projects/2026-06-11-ffnode-stress-testing-v5-full-document
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
source: confluence/doc/v3=2839871490, v4=2841247752
status: draft
tags: [confluence, design-document, ffnode, ollie-rushton, stress-testing, v5, weronika-jastrzebska]
title: 2026-06-11-FFNode-Stress-Testing-v5-Full-Document
type: null
version: 5
---

## Option A: FFNode Stress Testing—Design Document V5

> Status: Draft—pending review (reviewed by Ollie Rushton)
> Author: Leon Ormes
> Created: 7 May 2026
> Last updated: 11 June 2026 (v5—remaining Ollie comments + Weronika SDE requirements addressed)
> Primary epics: FTFL-476 (OMOP stress-testing infra + monitoring) · FTFL-480 (userflow permutation script)
> Hard deadline: 31 July 2026—AS05 milestone: five-node cohort, ≥2 nodes with ≥500M-row MEASUREMENT tables, full report
> Reviewers: Oliver Rushton · Helena Ahlfors · Robin Mofakham · Philip Russmeyer · Weronika Jastrzębska · Julia Kurps (The Hyve)

---

### How to Read This Document

The narrative runs: why we're doing this (§3, a real incident we couldn't see) → what we're testing and how we're framing it (§4–5) → what's in and out of scope (§6) → the kit (§7) → the test design (§8) → gates and monitoring (§9–10) → risks (§11) → the plan, decisions, and tickets (§12–16).

---

### Table of Contents

[[#1 Executive Summary]]

[[#2 Programme Structure at a Glance]]

[[#3 Background and Motivation]]

[[#4 Test Definition System Under Test and Posture]]

[[#5 Objectives and Success Criteria]]

[[#6 Scope]]

[[#7 Environment and Architecture]]

[[#8 Test Design]]

[[#9 Data Quality Gates Pre-flight]]

[[#10 Monitoring and Observability]]

[[#11 Risks and Known Failure Points]]

[[#12 Execution Plan]]

[[#13 Decision Log]]

[[#14 Open Items Register]]

[[#15 Jira Ticket Plan]]

[[#16 Stakeholders]]

[[#17 First Physical Actions]]

[[Appendix A — Reviewer Comment Resolutions v3 to v5]]

---

### 1. Executive Summary

FITFILE federates OMOP CDM v5.4 data across multiple NHS provider nodes. In April 2026, cohort-discovery queries against `cuh-prod-1` timed out against HDRUK's 5-minute SLA. The timeout itself was resolved by three indexes added on 24 April—but the incident exposed two problems that indexing does not fix:

1. We cannot predict where the federated system breaks under realistic clinical load.
2. We had no internal visibility into the failure—it was silent at the database tier and we only learned of it when the customer (via HDRUK) reported it.

This document defines a phased, evidence-driven testing programme to fix both: to measure how the system performs under normal load and to establish the known working limit up to the AS05 contractual requirement (by consensus: Position B from §4.4). This covers ≈5 synthetic nodes, 1M–3M patients each.

The programme tests three axes:

- Single-node capacity (Axis A)
- Multi-node federation (Axis B)
- Algorithmic userflow permutations across a structured subset of the 432-case grid, sequenced one variable at a time (Axis C)

It produces a phased execution plan, monitoring requirements (using existing dashboards where possible), an explicit risk register, and a backlog of eleven Jira tickets sequenced for delivery before the AS05 deadline of 31 July 2026.

---

### 2. Programme Structure at a Glance

Read this section first—everything else references it.

The programme runs in five sequential phases (0–4). The heavy lifting is in Phase 3, which is itself broken into four structured waves (A → B → C → D).

```
Phase 0  Register assets        ──────────────────────────────►
Phase 1  Pre-flight QA gates    ──────────────────────────────►
Phase 2  Single-node baseline   ──────────────────────────────►
Phase 3  Structured permutation waves  ── Wave A ─► Wave B ─► Wave C ─► Wave D ─►
Phase 4  Report-out             ──────────────────────────────►
```

| Phase | Scope | Duration | Depends on |
|---|---|---|---|
| 0—Register assets | Dataset manifest + 500M-row gate | 0.5 day |—|
| 1—Pre-flight QA gates | Achilles + schema integrity per node | 1–2 days | Phase 0 |
| 2—Single-node baseline | Permutation subset; calibrate monitoring | 1–2 days | Phase 1 · monitoring live |
| 3—Structured permutation waves | Structured subset of the 432-case grid, sequenced one variable at a time (Waves A/B/C/D) | 5–9 days | Phase 2 |
| 4—Report-out | Final report + infra spec | 0.5–1 day | Phase 3 |

The waves inside Phase 3 progressively add one variable at a time (see §8.2):

| Wave | Adds | Time-box |
|---|---|---|
| Wave A | S3 export (X=On) | 1–2 days |
| Wave B | Privacy on (P=On) | 1–2 days |
| Wave C | Extended scope (S=S3) | 1–2 days |
| Wave D | Federation (L=L2, then L=L3) | 2–3 days |

Phase 2's baseline run (P=Off, X=Off, L=L1) is the calibration step the waves build on. It is not a wave.

---

### 3. Background and Motivation

#### 3.1 The Production Incident (Resolved—but Two Lessons Remain)

In April 2026, cohort-discovery queries against `cuh-prod-1` timed out against HDRUK's external 5-minute SLA. Jakub Jaworski (CUH) and Oliver Rushton remediated it with three high-value indexes on 24 April 2026, and the timeout is now resolved.

We keep the incident in scope because indexing fixed the symptom, not the two underlying gaps:

- No predictability. We had no way of knowing that workload would breach the SLA until it did.
- No visibility. The DB-side logs showed no active queries while the upstream service reported timeouts—the failure was silent at the database tier.

#### 3.2 Year-End Target / AS05–AS06 Milestone Context

By year-end we expect five active provider nodes, each with 1M–3M patients. AS05 (31 July 2026) requires:

- A scale test against a synthetic cohort spanning ≥5 data providers
- At least two providers exposing OMOP MEASUREMENT tables of ≥500M rows (verified in Phase 0—see §12)
- SDE project area delivery confirmation with evidence
- Cost-per-query metric as a documented output

AS06 (follow-on) requires acting on the three highest-priority findings in collaboration with the EoE SDE team, demonstrating measurable improvement against the AS05 baseline.

#### 3.3 What This Document Captures

Six weeks of architectural planning (since early April 2026), the 7 May team meeting outcomes, and the 14 May design review—consolidated into a single executable plan.

---

### 4. Test Definition: System Under Test and Posture

#### 4.1 What Kind of Test This Is—and What It Is Not

"Stress test" covers a family of distinct test types. This programme is explicit about which it runs:

| Test type | In programme? | Notes |
|---|---|---|
| Capacity planning | ✅ Primary | "X patients per query needs Y node spec" / federation latency overhead per additional node |
| Scalability | ✅ Primary | Does federation scale linearly, or does coordination overhead dominate? |
| Load testing | ✅ Supporting | Maximum sustainable throughput per node at a given hardware spec |
| Performance characterisation | ✅ Supporting | Baseline p50/p95/p99 latency curves per cohort size |
| Soak / endurance | ❌ Deferred | No multi-day sustained runs—candidate follow-on |
| Spike | ❌ Out of scope | No sudden-surge scenarios |
| Chaos engineering | ❌ Out of scope | No deliberate node loss, partition, or secret-store outage |
| Performance regression CI | ❌ Out of scope | Candidate follow-on once Phase 4 (report-out) lands |
| Concurrency / throughput | ❌ Not testable | Sequential load generator—no concurrent request modelling (see §4.2) |

In one sentence: this is a capacity-and-scalability characterisation exercise on the FFNode / OMOP federated query path, executed against synthetic NHS-scale data at sequential load, with explicit exclusions for soak, chaos, concurrency, and regression.

#### 4.2 System Under Test—Foreground Vs Background

In plain terms: "the clusters" is too vague to test. We split the system into two groups. Foreground layers are the ones we're actually measuring—the stopwatch is on them. Background layers are everything that simply has to keep working for the result to count.

Foreground—these layers ARE the Test

| Layer | What we're measuring |
|---|---|
| F1. Federated query path (fitConnect hub + spokes) | End-to-end latency · routing overhead · cross-node bytes · partial-result vs full-failure semantics. Tested last. |
| F2. Per-node database tier (PostgreSQL / MSSQL per node) | Query latency · lock waits · temp spill · OOM behaviour · slow-query patterns. Tested directly (Axis A) and via workflows (Axis C). |
| F3. Userflow permutation engine (FTFL-480) | The load generator. Replays a real FITFILE cohort-discovery workflow varying six inputs (C×S×E×P×X×L). Privacy applied via default template. |

Background—these layers MUST Work but Are NOT the Experiment

| Layer | Required state during a test window |
|---|---|
| AKS control plane | Stable; not under deliberate stress |
| ArgoCD reconciliation | Auto-sync disabled on target test apps |
| Vault / VSO secret delivery | Stable; token TTLs ≥ test-window duration |
| cert-manager / TLS | DNS-01 challenges working; certificates valid |
| Container registry (ACR) | Images pre-pulled on test nodes |
| Monitoring stack (Grafana / Prometheus / Alloy) | Live, scraping, with standard k8s dashboards live before Phase 2 |

Load generator constraint: The FTFL-480 script runs discrete test cases sequentially within each wave. There is no concurrent or bursty request modelling. This means the programme cannot measure concurrency limits or throughput ceilings—it measures per-query latency at sequential load. Axes B and C criteria are written to match this constraint (see §5). NEW4's acceptance criteria must reflect this.

Explicitly out of the SUT (this round):

- omop-cli—the data-provisioning tool, not the load generator. Has its own separate capacity programme.
- Cross-cluster private networking (Azure ExpressRoute, site-to-site VPN)—out of scope. All connectivity via public endpoints.
- Customer-facing query UX—only the back-end federated query path is in scope.
- The harness build pipeline itself—assumed stable.
- Hyve ETL pipeline—partner-owned; The Hyve tests independently.

#### 4.3 Workload Profile

| Dimension | Specification |
|---|---|
| Direction | Read-only throughout all test phases. OMOP cohort discovery is overwhelmingly read-dominated. |
| Source | Synthetic only. Synthea-generated OMOP CDM v5.4. No real PII. |
| Load generator | The FTFL-480 userflow permutation script, running sequentially (no concurrency). |
| Arrival pattern | Discrete test cases run sequentially within a wave. No concurrent or bursty request modelling. |
| Realism trade-off | "Realistic overlap in cohorts—not realistic clinical data" (Ollie). Linkage distribution targets 70–85% single-trust / 15–30% 2+ trusts / 5–10% complex multi-site. |
| Query mix | Currently unknown. The structured permutation grid is a substitute for real query telemetry (OQ-8). |

#### 4.4 Programme Posture—Position B (Confirmed)

After review, the team has agreed on Position B (Oliver Rushton):

> "Only move up to the defined customer requirement (AS05). We don't have time to keep going beyond it. If we get there, that defines the known working limit."

- Phase 3 waves stop once AS05 is demonstrated—the requirement scale IS the known working limit.
- Performance characterisation (p50/p95/p99 latency, resource utilisation, cost-per-query) collected at each tier.
- Degradations observed on the way to AS05 are documented with reproduction coordinates.
- Documenting a degradation is a successful outcome—better to find it here than via a customer.

#### 4.5 Hypothesis Framing—Every Scenario is Falsifiable

Each Phase 3 wave tests one or more falsifiable hypotheses:

- H1. At cohort 1M, scope S2, privacy Off, linkage L1: p95 latency on a synthetic test node will remain within the internal FITFILE SLA (to be set—see P0 blocker B5). _Note: §8.4 mandates the OHDSI index set + Jakub's three indexes before loading. If these indexes are applied, CONDITION_OCCURRENCE sequential scans should be mitigated. H1 tests the _un-optimised_ path—it assumes indexes are NOT yet applied. If indexes are applied before H1 runs, the hypothesis is null; a replacement H1b (with indexes) should be written._
- H2. At linkage L3 (5 nodes): federation overhead adds ≥30% to p95 latency vs L1, dominated by `MEASUREMENT` transfers.
- H3. With privacy On (default template): no FK violations on `PERSON` ↔ `CONDITION_OCCURRENCE` joins.
- H4. Observation protocol (not a deliberate test): if a node becomes unresponsive during a federated run, record whether fitConnect returns a partial-results error, a timeout, or a silent partial aggregate.
- H5. With S3 export On: export of a NodeFull cohort to S3 completes and passes integrity checks.

---

### 5. Objectives and Success Criteria

Each axis has explicit, measurable criteria mapped to AS05/AS06 milestones. Cost-per-query methodology: subscription-level Azure/AWS cost burn divided by number of query runs executed in the test window, broken out per cohort-size tier. Accurate to ±10% at NodeFull scale; smaller cohorts may use pro-rata estimates.

#### Axis A—Single-node Capacity

| What we're proving | Metrics | Success criterion | Milestone |
|---|---|---|---|
| Single-node query capacity | p50/p95/p99 latency · DB CPU/mem/IO · error rate · cost-per-query | No errors; latency rises predictably with cohort size (no "cliff") up to NodeFull. Cost-per-query documented per cohort tier. | AS05 |
| DB break points | Max connections, lock waits, temp spill, cancellations | First failure documented with resource snapshot; classify fixable vs architectural. | AS05 |
| Run-failure recovery | Restart time, idempotency | Observed if encountered naturally. If it occurs, verify retry without manual DB surgery. | AS05 |

#### Axis B—Multi-node Federation

| What we're proving | Metrics | Success criterion | Milestone |
|---|---|---|---|
| Federation up to 5 nodes (sequential load) | p95 end-to-end latency · cross-node bytes · timeout rate · cost-per-query | Federation across 2→3→5 nodes completes without timeout. Document latency overhead per additional node at sequential load. Cost-per-query per node count. | AS05 |
| Cross-cloud overhead (follow-on cross-cloud stage only) | Network RTT · federation latency delta | Cross-cloud (Azure UK South ↔ AWS eu-west-2) overhead quantified independently of query cost. | AS06 follow-on |
| Graceful failure under disparity | Error-propagation behaviour | Observed if encountered (no deliberate throttle). If a node fails, document the error surface. | AS05 |

#### Axis C—Algorithmic / Userflow Permutations (FTFL-480)

| What we're proving | Metrics | Success criterion | Milestone |
|---|---|---|---|
| Userflow scales with cohort size | Workflow duration per stage; error rate; cost-per-query | Per cohort-size tier, completion within agreed budget; "cost per additional patient" curve is monotonic. | AS05 |
| Scope-of-extract impact | Rows exported, file sizes, stage timings | Export time correlates with selected scope; identify which tables dominate cost. | AS05 |
| Privacy-treatment overhead | Latency delta, CPU delta, suppression counts | Privacy On does not break referential integrity; overhead quantified. | AS05 |
| Multi-source linkage | Join counts, duplicate/missed links | Cross-node linkage preserves expected overlap (70–85% / 15–30% / 5–10%). | AS05 |
| S3 export | Export duration · file integrity checks · error rate | Export completes at each cohort-size tier; output passes integrity check. | AS05 |

#### External Constraint—HDRUK Timeout

5 minutes wall-clock per query. The contractual measurement is FITFILE application query latency (SDE primarily uses the FITFILE application, not HDRUK). The HDRUK 5-minute timeout is retained as an external reference. The primary SLA gate is the FITFILE application internal latency target—this must be defined before Phase 2 begins (P0 blocker B5).

#### AS05 Delivery Confirmation

The Phase 4 report must include explicit evidence of SDE project area delivery—confirmed that the correct SDE area received the stress-test outputs.

---

### 6. Scope

#### 6.1 In Scope

- Synthetic OMOP CDM v5.4 data across 5 nodes.
- Pre-flight quality gates (Achilles + schema/FK integrity only).
- Single-node characterisation, structured multi-node federation, structured userflow permutations.
- Monitoring via standard k8s observability dashboards; bespoke panels only if gaps are found.
- Dual-audience report (internal FITFILE + external SDE).

#### 6.2 Out of Scope

- Cross-cloud federation (Azure UK South ↔ AWS eu-west-2)—conditional follow-on cross-cloud stage; out of scope until confirmed.
- Chaos engineering—follow-up programme.
- Real-PII testing—synthetic only.
- Performance regression CI—follow-on once Phase 4 lands.
- Hyve ETL pipeline testing—partner-owned.
- Soak / endurance testing—deferred.
- Private networking (ExpressRoute, site-to-site VPN).
- WhiteRabbit profiling.
- OHDSI DQD.
- Concurrency / throughput limits—sequential load generator constraint.

#### 6.3 Assumptions

- The 5 Parquet datasets are final and version-pinned (precondition for Phase 0).
- ArgoCD auto-sync on target test apps disabled during test windows.
- 5 new dedicated synthetic nodes will be provisioned—production nodes are off-limits.

---

### 7. Environment and Architecture

#### 7.1 Production Node Inventory (Reference Only)

Production nodes are off-limits for all stress-test activity. Table provided for context only.

| Node | DB engine | AKS cluster | Notes |
|---|---|---|---|
| ff-a | MSSQL | prod-1 | Coordinating hub |
| ff-b | MSSQL | prod-1 | Spoke |
| ff-c | MSSQL | prod-1 | Spoke |
| barts | MSSQL | prod-1 | Live NHS data |
| cuh-prod-1 | PostgreSQL | hie-prod-34 | ETL'd; source of April 2026 incident |
| mkuh-prd-4 | PostgreSQL | mkuh-prd-4 | ETL'd; DB settings per Ollie |
| nwsde-prod-1 | TBC | nwsde-prod-1 | NWSDE—DB engine to confirm |

#### 7.2 Synthetic Test Node Additions

Five dedicated synthetic nodes must be provisioned. No existing production infrastructure is reused. Topology decision (co-located on one oversized node vs 5 separate) is open item D-a.

#### 7.3 Connectivity

All inter-node traffic via public endpoints. Cross-cloud (Azure UK South ↔ AWS eu-west-2) connectivity is a separate follow-on stage, not part of the main execution phases (renamed to avoid confusion with Phase 0–4).

#### 7.4 Synthetic Node Sizing

Ollie's MKUH PostgreSQL settings should be reviewed and applied as baseline. Capture current Grafana resource consumption before any load is applied.

---

### 8. Test Design

#### 8.1 Permutation Grid (FTFL-480)

Six variables defined as discrete level-sets. The Cartesian product is the full grid (432 cases). However, the wave execution in §8.2 covers a structured subset sequenced one variable at a time—this is the deliberate design under Position B time pressure, not the full product. The framing "structured subset of the 432-case grid" is used throughout this document.

Variable E (Extract cap—Capped) is not independently exercised by any wave. Rationale: under Position B (stop at AS05) the primary concern is uncapped query performance. Capped extraction produces a smaller data subset and is implicitly tested when smaller cohort sizes (1k, 10k, 100k) hit naturally during runs. If headroom is found, E=Capped can be added as a follow-on wave. _This gap should be acknowledged if Ollie or Weronika quotes "432" in the report._

Grid overstates valid combinations. For example, `C=5NodeFull` at `L=L1` (single node) is nonsensical. The usable subset is smaller than 432.

| Variable | Levels |
|---|---|
| C—Cohort size | 1k · 10k · 100k · 1M · NodeFull · 5NodeFull |
| S—Selection scope | S1 Minimal · S2 Core clinical · S3 Extended (from SDE data access requests—Ollie action) |
| E—Extract cap | Uncapped · Capped (LIMIT/TOP per Ollie) |
| P—Privacy treatment | Off · On (default template; no k-anonymity per Ollie) |
| X—S3 export | Off (query only) · On (export to S3) |
| L—Linkage scenario | L1 Single node · L2 Two nodes · L3 Five nodes (unified output is primary; overlap distribution secondary) |

#### 8.2 Wave-Based Execution (Phase 3)

Running all 432 combinations in one pass would make failures untraceable. The structured subset adds one variable at a time, so each degradation has a single, obvious cause.

| Stage | What's switched on | The one thing it adds | Time-box |
|---|---|---|---|
| Phase 2 baseline | C ∈ {1k…NodeFull}, S ∈ {S1,S2}, E=Uncapped, P=Off, X=Off, L=L1 |—(the starting point) | 1–2 days |
| Wave A | Baseline + S3 export | Export to S3 (X=On) | 1–2 days |
| Wave B | Wave A + privacy on | Privacy treatment (P=On) | 1–2 days |
| Wave C | Wave B + extended scope | Extended extract scope (S=S3) | 1–2 days |
| Wave D | Wave C + multiple nodes | Federation (L=L2, then L=L3) | 2–3 days |

Each wave produces a ranked list of degradation/failure coordinates (C, S, E, P, X, L) with classification: timeout · OOM · SQL error · export failure.

#### 8.3 Graceful Vs Silent Failure

Observation protocol (not a deliberate throttle test): if a node becomes unresponsive during a federated run, document whether fitConnect returns a partial result, a timeout, or a meaningful error, and whether the Patient Querier returns aggregates from available nodes or rejects the whole query.

#### 8.4 Database Sizing Requirements

- Disk ≥ 3× Parquet data size, for indexes + temp space.
- Apply the canonical OHDSI index set + Jakub's three CUH indexes.
- Run Achilles per node before the first load test.

#### 8.5 Slow-Query Logging

| Engine | Configuration |
|---|---|
| PostgreSQL | `pg_stat_statements` + `auto_explain` + `log_min_duration_statement` = 500ms |
| MSSQL | Query Store enabled; `QUERY_CAPTURE_MODE` = AUTO |

---

### 9. Data Quality Gates (Pre-flight—Phase 1)

Stop condition (D5): any node failing a quality gate blocks all load tests.

#### 9.1 Schema and Integrity

- OMOP CDM v5.4 table presence + required columns per node.
- PK uniqueness; FK consistency—`PERSON` ↔ {`VISIT_OCCURRENCE`, `CONDITION_OCCURRENCE`, `DRUG_EXPOSURE`, `MEASUREMENT`, `OBSERVATION`}.
- Concept-ID sanity: % standard concepts, % concept_id = 0, % deprecated.
- Generic ETL Container pinned to ≥ v1.2.0.

#### 9.2 Achilles—Distribution Sanity (Per Node)

Row counts · top concepts · person counts per clinical table · visit-distribution sanity.

#### 9.3 Overlap Validation (L2/L3 Pre-condition)

- Compute overlap stats across the 5 Parquet datasets.
- Primary goal for L3: prove the system can query 5 OMOP datasets and produce unified output. Overlap distribution is secondary.

_WhiteRabbit and OHDSI DQD are not required. Achilles + schema/FK integrity suffice for Phase 1._

---

### 10. Monitoring and Observability

#### 10.1 Approach

Use existing Kubernetes observability dashboards as the primary tool. Bespoke panels only if gaps are identified after Phase 2.

#### 10.2 Required Metrics

| Category | Metrics |
|---|---|
| System / container | CPU (usage %, throttling), Memory (RSS, OOM kills), Disk (IOPS, latency), Network (bytes, cross-node bandwidth) |
| Database | Active connections, query runtime (p50/p95/p99), timeouts, lock waits, buffer-cache hit ratio, slow-query log |
| Workflow / application | Run ID, scenario coordinates (C,S,E,P,X,L), stage timings, rows scanned/returned, error taxonomy |

#### 10.3 Dashboard Panels (Nice-to-have)

If existing dashboards fall short:

1. Run Overview—One row per test case: duration · peak CPU/mem · p95 latency · error flag
2. Bottleneck Board—Top offenders by time and IO
3. Federation Board—Cross-node bytes · latency per additional node

---

### 11. Risks and Known Failure Points

#### 11.1 Failure-Point Register

| # | Failure mode | Risk | Detection | Mitigation |
|---|---|---|---|---|
| 1 | Multi-node federation bandwidth saturates at 5 nodes | High | Cross-node network bytes | Cap concurrency |
| 2 | DB reindexer OOM | High | OOM kill counter | Right-size DB; schedule outside test window |
| 3 | Privacy treatment breaks referential integrity | High | Post-run FK consistency check | Validate every privacy-ON wave |
| 4 | Linkage bottlenecks—MPS struggles with messy demographics | Medium | Stage-timing breakdown | Capture linkage stage timings |
| 5 | Vocabulary / concept-mapping gaps | Medium | Achilles concept_id = 0 rate | Document gaps; route to vocabulary backlog |
| 6 | Run-failure recovery—long jobs can't resume | Medium | Observed if encountered | Harness must be idempotent |
| 7 | Silent failure at DB tier (CUH incident class) | High | Observed during testing | Ensure monitoring surfaces DB-tier silence |
| 8 | ArgoCD auto-sync racing imperative test changes | Medium | n/a—operational | Disable auto-sync before each window |

#### 11.2 Kill Criteria—Abort Immediately If

- Any production node shows error rate > baseline + 2σ for > 5 minutes.
- Any privacy-ON wave produces FK violations on `PERSON` joins.
- Cost burn exceeds documented daily ceiling.
- Vault token or cert-manager error rate spikes.

---

### 12. Execution Plan

#### Phase 0—Register Assets (0.5 Day)

Dataset manifest (version · vocabulary version · row counts · SHA-256 checksums · node-ID mapping) · confirm overlap engineering (OQ-8).

500M-row gate: Verify that ≥2 datasets contain ≥500M rows in their `MEASUREMENT` tables. If this threshold is not met, the AS05 condition cannot be satisfied. Discovering a shortfall at Phase 4 would be unrecoverable before 31 July. If unmet, either (a) regenerate the Parquet datasets with higher Synthea patient counts, or (b) escalate to the programme team for scope adjustment.

#### Phase 1—Pre-flight Quality Gates (1–2 Days)

Achilles + schema/FK integrity (§9). Stop-condition: any failing node blocks Phase 2.

#### Phase 2—Baseline Single-Node (1–2 Days)

C ∈ {1k…NodeFull}, S ∈ {S1,S2}, E=Uncapped, P=Off, X=Off, L=L1 · p50/p95/p99 latency · DB CPU/mem/IO · verify idempotency · baseline cost-per-query.

#### Phase 3—Structured Permutation Waves (5–9 Days)

Run the structured subset as Waves A → B → C → D (§8.2). Record degradation coordinates. Classify per dimension. Collect cost-per-query at each tier.

#### Phase 4—Report-Out (0.5–1 Day)

Internal (FITFILE team):

- Degradation table with reproduction coordinates
- Recommended infrastructure spec per node
- DB/indexing change recommendations
- Dashboard screenshots + run manifests

External (SDE stakeholders):

- AS05 milestone evidence: scale test results, SDE delivery confirmation, cost-per-query metric with documented methodology
- Top-three issues nominated for AS06/EoE SDE collaboration, with reproduction coordinates and observed SLA/cost impact
- Baseline metrics with full query configs preserved for AS06 comparative re-testing

---

### 13. Decision Log

| # | Decision | Source | Date |
|---|---|---|---|
| D1 | Start with single oversized node hosting 5 co-located OMOP databases; escalate to 5 separate later. _⚠ Superseded / under review pending D-a._ | Planning meeting | 7 May 2026 |
| D2 | Connectivity: public endpoints only. No vVPN/IPsec, no Azure Private Link. | Ollie's review | June 2026 |
| D3 | Cross-cloud connectivity is a separate follow-on stage, not part of main phases. | Planning meeting | 7 May 2026 |
| D4 | Waves sequenced one variable at a time (A→B→C→D), never all 432 at once. | Planning meeting | 7 May 2026 |
| D5 | Quality gates (Achilles + schema/FK integrity) are unconditional stop-condition. | 16 Apr session | 16 Apr 2026 |
| D6 | Hyve ETL pipeline out of scope—The Hyve tests independently. | v4 revision | 2 June 2026 |
| D7 | Programme posture: Position B—stop at AS05 requirement. | v5 revision | 11 June 2026 |
| D8 | Monitoring: use existing k8s dashboards; bespoke only if gaps found. | v5 revision | 11 June 2026 |
| D9 | WhiteRabbit and DQD not required—Achilles + schema/FK suffice. | v5 revision | 11 June 2026 |

---

### 14. Open Items Register

#### 14.1 P0—Blockers (Must Resolve Before Execution Starts)

| ID | Item | Owner | Target | Why it matters |
|---|---|---|---|---|
| B1 | Produce hardware-inventory table for all prod nodes | Leon / Ollie | Sprint 16 | Without it, synthetic spec is guessed |
| B2 | Confirm Person_ID overlap across the 5 Parquet datasets | Leon | Sprint 16 | Determines L2/L3 test character |
| B3 | Define the query harness for FTFL-480 | Ollie / Leon | Sprint 16 | Determines what "Selection scope" means |
| B4 | Provision 5 new synthetic nodes | Leon | Sprint 16 | Production nodes are off-limits |
| B5 | Define FITFILE internal latency SLA (replaces HDRUK 5-min as primary gate) | Ollie / Leon | Sprint 16 | H1, Axis B criteria, and the external constraint all reference a threshold that doesn't exist yet. Phase 2 cannot gate against an undefined target. Promote from D-c/D-h. |

#### 14.2 P1—Decisions For Next Planning Meeting

| ID | Decision required | Status |
|---|---|---|
| D-a | Single oversized node vs 5 separate nodes? (D1 superseded) | Open |
| D-e/OQ-4 | Partial-result vs full-failure semantics—does fitConnect have configurable per-node sub-query timeout? | Open—Pavlo / Enric |
| D-f/OQ-8 | Which queries do HDRUK users actually run? Query-log access? | Open—Ollie / Weronika |

#### 14.3 P2—Deferred / Out-of-Scope Candidates

| ID | Item | Disposition |
|---|---|---|
| F1 | Use-case clarity from Wesam | Track as follow-on |
| F2 | Warning mechanism for "too big" queries | Follow-on programme |
| F3 | Chaos engineering | Follow-on programme |
| F4 | Performance-regression CI | Follow-on once Phase 4 lands |

---

### 15. Jira Ticket Plan

#### 15.1 New Tickets to Raise

| Ticket | Summary | Parent | Priority | Owner |
|---|---|---|---|---|
| NEW1 | Register 5-node dataset manifest + verify ≥2 datasets meet 500M-row MEASUREMENT threshold | FTFL-488 | P1 | Leon Ormes |
| NEW2 | Confirm Person_ID overlap across 5 Parquet nodes | FTFL-475 | P1 | Leon Ormes |
| NEW3 | Run Achilles pre-flight quality gates per node | FTFL-476 | P1 | TBC |
| NEW4 | Define query harness for FTFL-480 userflow test runner (sequential, no concurrency—acceptance criteria must reflect this) | FTFL-480 | P1 | Oliver Rushton |
| NEW5 | Build Phase 2 single-node baseline test harness | FTFL-476 | P1 | Leon Ormes |
| NEW6 | Verify existing k8s dashboards capture required metrics; build only if gaps found | FTFL-476 | P2 | TBC |
| NEW7 | Execute Wave A permutation runs (S3 export) | FTFL-480 | P2 | TBC |
| NEW8 | Execute Wave B permutation runs (Privacy ON) | FTFL-480 | P2 | TBC |
| NEW9 | Execute Wave C permutation runs (Extended scope S3) | FTFL-480 | P2 | TBC |
| NEW10 | Execute Wave D permutation runs (Federation L2 then L3) | FTFL-480 | P2 | TBC |
| NEW11 | Produce final stress-test report + infra-spec recommendations (dual-audience) | FTFL-476 | P2 | Leon Ormes |

NEW11 acceptance criteria:

- AS05 milestone evidence: scale test results, SDE delivery confirmation, cost-per-query with documented methodology
- Top-three issues nominated for AS06/EoE SDE collaboration
- Baseline metric exports preserved for AS06 comparative re-testing
- Internal FITFILE infrastructure recommendations + run manifests

#### 15.2 Existing Tickets Requiring Updates

| Ticket | Required action |
|---|---|
| FTFL-476 | Update AC: monitoring uses existing k8s dashboards; add cost-per-query metric |
| FTFL-480 | Confirm structured 6-variable grid and A→B→C→D wave order |
| FTFL-475 | Confirm data generation complete; close if Parquet files are final |
| FTFL-479 | Close or re-scope—Hyve pipeline out of scope (D6) |
| FTFL-638 | Close—no production nodes; monitoring uses existing stack |
| FTFL-652 | OMOP DB provisioning for new synthetic nodes |
| FTFL-635 | Stress Testing in the Application—clarify relationship to FTFL-476/480 |

---

### 16. Stakeholders

| Role | Name | Responsibility |
|---|---|---|
| Author / Platform lead | Leon Ormes | Document owner; Phase 0–3 execution; infrastructure |
| Query strategy | Oliver Rushton | Query design; CUH remediation context |
| Indexing / DB tuning | Jakub Jaworski (CUH) | Index-strategy reference |
| Networking | Robin Mofakham | Cross-cloud feasibility |
| Programme / scoping | Helena Ahlfors | Use-case clarity; project-plan liaison |
| Federation semantics | Enric / Pavlo | fitConnect timeout behaviour |
| Hyve liaison (observer) | Julia Kurps / Stefan (The Hyve) | Independent pipeline testing |
| SDE liaison | Weronika Jastrzębska | AS05/AS06 milestone alignment; SDE report audience |
| NHS contacts | Alexis McKenna / Helen Duckworth | NHS-side validation |
| Other reviewers | Philip Russmeyer / Magali Ruffier / Jamie Reeve / Sean Donnelly | Design review |

---

### 17. First Physical Actions (This Week)

- Raise the eleven new Jira tickets listed in §15.1 (~30 minutes).
- Update FTFL-476 acceptance criteria per §15.2.
- Circulate this v5 document to reviewers; book a 30-minute review session.
- Confirm Phase 0 can start in Sprint 16 (5 Parquet datasets + 5 synthetic nodes).
- Resolve P0 blocker B5 (internal SLA definition) before Phase 2 begins.
- Resolve D-a (single vs separate nodes) before provisioning starts.

---

### Appendix A—Reviewer Comment Resolutions (V3 → v5)

_Delete this appendix before final publication._

#### Ollie Rushton—Resolved in V4

| # | Comment | Resolution |
|---|---|---|
| 1 | "Phase 4—Hyve / ETL runs—out of scope" | ✅ D6 formalises. |
| 2 | "Extract cap—agreed, controlled via LIMIT / TOP" | ✅ Confirmed in grid. |
| 3 | "Add S3 export to permutation list" | ✅ X variable added; Wave A added. |
| 4 | "F4 Hyve—out of scope" | ✅ Removed. |
| 5 | "F5 Privacy—included in F3 using default template" | ✅ k-anonymity removed. |
| 6 | "omop-cli—clarify or delete" | ✅ Clarified. |
| 7 | "ExpressRoute / site-to-site VPN out of scope" | ✅ Added. |
| 8 | "PII vs PHI" | ✅ Changed to PII. |
| 9 | "diurnal → concurrent" | ✅ Changed. |
| 10 | "Reindex OOS" | ✅ Removed from Axis A. |
| 11 | "Run-failure recovery—observe if it happens" | ✅ Reframed. |
| 12 | "Packet loss—???" | ✅ Removed. |
| 13 | "Add export to Axis C" | ✅ Done. |
| 14 | "Axis D—OOS / pass to Hyve" | ✅ D6 confirmed. |
| 15 | "Data quality—Hyve's responsibility?" | ✅ Clarified. |
| 16 | "Datasets—OMOP, no Hyve work" | ✅ Done. |
| 17 | "7.1—cannot use these" | ✅ Reheaded reference-only. |
| 18 | "7.2—5 brand new nodes" | ✅ Done. |
| 19 | "No intra-cluster—public endpoints" | ✅ Done. |
| 20 | "None use Azure Private Link" | ✅ Removed. |
| 21 | "3 nodes, 23 GiB RAM—see my settings" | ✅ Referenced in §7.4. |
| 22 | "Move PostgreSQL to dedicated pool—no" | ✅ Closed (D-b resolved). |
| 23 | "S3 scope from actual SDE requests" | ✅ Action on Ollie. |
| 24 | "Default template only, no k-anonymity" | ✅ Done. |
| 25 | "L3—prove 5-node unified query" | ✅ Overlap distribution secondary. |

#### Ollie Rushton—Resolved in V5

| # | Comment | Resolution |
|---|---|---|
| 26 | "Not WhiteRabbit, just Achilles" | ✅ WhiteRabbit removed. |
| 27 | "DQD—Remove this" | ✅ DQD removed. |
| 28 | "Deliberately throttle—observe if it happens" | ✅ §8.3 observation protocol. |
| 29 | "We don't have time to go beyond requirement" | ✅ Position B adopted. |
| 30 | "HDRUK timeout—Hutch team owns this" | ✅ B5 promoted; internal SLA recommended. |
| 31 | "Monitoring—K8s dashboards enough?" | ✅ D8 adopted (existing dashboards). |
| 32 | "Remove" (multiple tickets) | ✅ Ticket plan simplified. |
| 33 | "5 brand new nodes—prov prod first" | ✅ B4 added. |
| 34 | "E=Capped never exercised by any wave" | ✅ Acknowledged in §8.1 with rationale. |
| 35 | "Can't measure concurrency with sequential generator" | ✅ §4.2 constraint documented; Axis B criteria rewritten. |
| 36 | "Phase collision—connectivity named same as execution" | ✅ Renamed to "follow-on cross-cloud stage". |
| 37 | "D1 vs D-a topo conflict" | ✅ D1 marked superseded / pending D-a. |

#### Weronika Jastrzębska—Resolved in V5

| # | Comment | Resolution |
|---|---|---|
| W1 | "HDRUK low importance—SDE uses FITFILE app" | ✅ §5: FITFILE app SLA is primary; HDRUK external reference. |
| W2 | "SDE not using HDRUK currently" | ✅ Noted. |
| W3 | "No query-log access from SDE" | ✅ Acknowledged in §4.3. |
| W4 | "Create benchmarking for wider audience" | ✅ §5 success criteria + Phase 4 dual report. |
| W5 | "AS06 requires acting on findings" | ✅ NEW11 AC + §3.2 reference. |
| W6 | "Link axes to AS05/AS06 milestones" | ✅ Milestone column in §5. |
| W7 | "Cost-per-query is required AS05 metric" | ✅ Added to all axes + methodology defined in §5. |
| W8 | "SDE delivery confirmation as explicit AC" | ✅ Added to §5 and NEW11 AC. |
| W9 | "Phase 4 report needs dual audience" | ✅ Phase 4 deliverables restructured. |
| W10 | "Timeline needs review based on blockers" | ✅ P0 blockers B1–B5 + timeline included in §17. |
| W11 | "NEW11 AC must include AS05 evidence, top-3, baselines" | ✅ NEW11 AC expanded per spec. |
