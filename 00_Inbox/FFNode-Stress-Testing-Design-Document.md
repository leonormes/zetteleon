---
created: 2026-06-02T11:56:44+00:00
modified: 2026-06-02T12:02:32+00:00
tags: [1, 2, 7]
title: FFNode-Stress-Testing-Design-Document
---

## FFNode Stress Testing—Design Document

| Field | Value |
|---|---|
| Status | Draft—pending review |
| Author | Leon Ormes |
| Created | 7 May 2026 |
| Last updated | 2 June 2026 (v3—restructured + review comments addressed) |
| Primary epics | FTFL-476 (OMOP stress-testing infra + monitoring) · FTFL-480 (userflow permutation script) |
| Hard deadline | 31 July 2026—AS05 milestone: five-node cohort, ≥2 nodes with ≥500M-row `MEASUREMENT` tables, full report |
| Related | Confluence design doc · OMOP / The Hyve design doc · NHS Synthetic Data & OMOP Pipeline · Miro board |
| Reviewers | Oliver Rushton · Helena Ahlfors · Robin Mofakham · Philip Russmeyer · Weronika Jastrzębska · Julia Kurps (The Hyve) |

### Contents

1. [Executive Summary](#1-executive-summary)
- [⚡ Scope Decision — Option A vs Option B](#-scope-decision--option-a-full-vs-option-b-bare-bones)—_decision required before sprint planning_
1. [Programme Structure at a Glance](#2-programme-structure-at-a-glance)—_Option A; read this first_
2. [Background and Motivation](#3-background-and-motivation)
3. [Test Definition: System Under Test and Posture](#4-test-definition-system-under-test-and-posture)
4. [Objectives and Success Criteria](#5-objectives-and-success-criteria)
5. [Scope](#6-scope)
6. [Environment and Architecture](#7-environment-and-architecture)
7. [Test Design](#8-test-design)
8. [Data Quality Gates (Phase 1)](#9-data-quality-gates-pre-flight--phase-1)
9. [Monitoring and Observability](#10-monitoring-and-observability-ftfl-476--ftfl-478)
10. [Risks and Known Failure Points](#11-risks-and-known-failure-points)
11. [Execution Plan](#12-execution-plan-detail)
12. [Decision Log](#13-decision-log)
13. [Open Items Register](#14-open-items-register-unified-actions--decisions--questions)
14. [Jira Ticket Plan](#15-jira-ticket-plan)
15. [Stakeholders](#16-stakeholders)
16. [First Physical Actions](#17-first-physical-actions-this-week)
- [Appendix: Reviewer comment resolutions](#appendix--reviewer-comment-resolutions)

> How to read this document. Start with the ⚡ Scope Decision section (immediately above §2)—it presents Option A vs Option B and requires a team decision before sprint planning. If Option A is confirmed, the narrative runs: why we're doing this (§3) → what we're testing (§4–5) → scope (§6) → the kit (§7) → test matrix (§8) → gates, monitoring, risks (§9–11) → the plan, decisions, and tickets (§12–15). The two sections most worth reading in full are §2 (the map) and §4.4 (what we're trying to learn and the unresolved posture decision).

---

### 1. Executive Summary

FITFILE federates OMOP CDM v5.4 data across multiple NHS provider nodes. In April 2026, cohort-discovery queries against `cuh-prod-1` timed out against HDRUK's 5-minute SLA. The timeout itself was resolved by three indexes added on 24 April—but the incident exposed two problems that indexing does not fix:

1. We cannot predict where the federated system breaks under realistic clinical load.
2. We had no internal visibility into the failure—it was silent at the database tier and we only learned of it when the customer (via HDRUK) reported it.

This document defines a phased, evidence-driven testing programme to fix both: to measure how the system performs under normal load _and_ to find the limits where it breaks—before we reach year-end production scale (≈5 nodes, 1M–3M patients each).

The programme tests three axes:

- Single-node capacity (Axis A)
- Multi-node federation (Axis B)
- Algorithmic userflow permutations across a 432-case grid (Axis C)

It produces a phased execution plan, monitoring requirements, an explicit risk register, and a backlog of eleven new Jira tickets sequenced for delivery before the AS05 deadline of 31 July 2026.

---

### ⚡ Scope Decision—Option A (Full) Vs Option B (Bare-bones)

> Team decision required before sprint planning. The rest of this document describes Option A in full. Option B is presented here as an alternative.
>
> Context: the programme as designed (Option A) is a research-grade testing exercise. With 2 developers carrying other workstreams, the full plan is unlikely to complete before the AS05 deadline of 31 July 2026. Option B is a scoped-down alternative that meets all AS05 requirements with approximately one third of the effort.

#### Comparison

| Dimension | Option A (full plan) | Option B (bare-bones AS05) |
|---|---|---|
| Developer effort | ~20–30 dev-days | ~6–8 dev-days |
| Phases | 4 phases (0–4) | 3 phases |
| Pre-flight QA | WhiteRabbit + Achilles + schema integrity | Schema integrity only |
| Monitoring | 3 custom Grafana dashboards built from scratch | Existing K8s observability + DB query logs enabled |
| Test scenarios | 432-case permutation grid, 4 waves | ~10 fixed targeted scenarios |
| Cohort sizes | 1k · 10k · 100k · 1M · NodeFull · 5NodeFull | 100k · 1M · NodeFull · 5NodeFull |
| Privacy | Isolated wave (measure privacy overhead separately) | Always on (default template)—not isolated |
| S3 export | Isolated wave (measure export overhead separately) | Always on—not isolated |
| Linkage | L1 / L2 / L3 progressively | L3 only (5-node unified output—the AS05 requirement) |
| Cross-cloud | Conditional Phase 2 | Definitive follow-on |
| Root-cause precision | High—one variable changes per wave | Medium—scenarios chosen to cover the requirement |
| Report depth | Full infra spec + recommendations | AS05 deliverable: query time, resource use, cost, blockers |
| Meets AS05? | ✅ Yes | ✅ Yes |
| Survivable with 2 devs? | ⚠️ Unlikely alongside other work | ✅ Yes |

What Option B gives up: systematic root-cause isolation (you know _something_ struggled, but not always _which_ variable caused it) and the performance-overhead deltas for privacy and export individually.

What Option B does not give up: the AS05 deliverable, the five-node federation result, the MEASUREMENT table scale requirement, and a credible performance baseline.

---

#### Option B—Full Plan

##### Phases

```
Phase 0  Assets + schema check    0.5 day   ──►
Phase 1  Targeted scenario runs   3–4 days  ──►
Phase 2  Report                   1 day     ──►
Total:   ~5–6 days of focused work
```

Phase 0—Asset registration and schema check (0.5 day)

- Confirm all 5 Parquet datasets are loaded onto 5 new dedicated nodes.
- Run OMOP schema integrity check per node: table presence + FK consistency (`PERSON ↔ {VISIT_OCCURRENCE, CONDITION_OCCURRENCE, DRUG_EXPOSURE, MEASUREMENT}`).
- Record node spec (disk type, RAM, DB engine) in the run manifest for replayability.
- Stop condition: any node failing schema check → fix before proceeding. No load testing against bad data.

Phase 1—AS05 scenario runs (3–4 days)

Privacy on (default template), S3 export on, all default settings throughout. No combinatorial grid—10 fixed scenarios chosen to cover the AS05 requirement and produce a credible baseline.

| Scenario | Cohort | Scope | Nodes | Purpose |
|---|---|---|---|---|
| S1 | 100k | Core clinical (S2) | 1 | Single-node baseline—does it work? |
| S2 | 1M | Core clinical (S2) | 1 | Single-node at clinical scale |
| S3 | NodeFull | Core clinical (S2) | 1 | Single-node worst case |
| S4 | 1M | Core clinical (S2) | 1 | Repeat on one of the two 500M-row `MEASUREMENT` nodes—AS05 hard requirement |
| S5 | NodeFull | Core clinical (S2) | 1 | NodeFull on the 500M-row `MEASUREMENT` node—AS05 hard requirement |
| S6 | 100k | Core clinical (S2) | 5 | First federation test—does it return unified output? |
| S7 | 1M | Core clinical (S2) | 5 | Federation at clinical scale |
| S8 | NodeFull | Core clinical (S2) | 5 | Federation worst case—primary AS05 deliverable |
| S9 | NodeFull | Extended (S3) | 5 | Full-scope federation—what does max scale cost? |
| S10 | Whatever failed in S1–S9 | Same scope | Same nodes | Re-run with full logging to document the failure |

Capture per run: p50/p95/p99 latency · peak CPU/mem · error flag (yes/no + type) · export success (yes/no) · cost.

Phase 2—Report (1 day)

Write the AS05 deliverable directly from the run log. Required content:

- Query execution time per scenario (the table above, populated).
- Resource utilisation at peak.
- Estimated cost per query.
- Any blockers or degradation observed, with enough detail to act on.
- One-paragraph recommendation on what to test next (the full Option A waves, if the team has capacity post-AS05).

##### What Option B Defers (not loses)

Option A's full wave programme becomes the natural follow-on once AS05 is delivered. The scenarios above are a subset of the grid—all the wave infrastructure built for AS05 can run the full 432 cases in a subsequent sprint. Nothing is thrown away; it's sequenced.

---

#### Which Option?

> Decision required from: Leon Ormes · Oliver Rushton · Helena Ahlfors
>
> Please confirm which option to pursue before the next sprint planning session. The rest of this document is Option A in full detail—it remains valid if Option A is chosen, or serves as the follow-on plan if Option B is chosen now.

---

### 2. Programme Structure at a Glance

> _(This and all subsequent sections describe Option A in full. If Option B has been agreed, use the plan in the Scope Decision section above and treat this document as the follow-on reference.)_

The programme runs in five sequential phases (0–4). The heavy lifting is in Phase 3, which is itself broken into three waves (A → B → C). Phases and waves are _not_ the same axis of organisation:

```
Phase 0  Register assets        ──────────────────────────────►
Phase 1  Pre-flight QA gates    ──────────────────────────────►
Phase 2  Single-node baseline   ──────────────────────────────►
Phase 3  Full permutation grid  ── Wave A ─► Wave B ─► Wave C ─►
Phase 4  Report-out             ──────────────────────────────►
```

| Phase | Scope | Duration | Depends on |
|---|---|---|---|
| 0—Register assets | Dataset manifest | 0.5 day |—|
| 1—Pre-flight QA gates | WhiteRabbit + Achilles + schema integrity per node | 1–2 days | Phase 0 |
| 2—Single-node baseline | Permutation subset; calibrate monitoring | 1–2 days | Phase 1 · monitoring live |
| 3—Full permutation waves | 216-case grid, run as Waves A / B / C | 3–7 days | Phase 2 |
| 4—Report-out | Final report + infra spec | 0.5–1 day | Phase 3 |

The waves inside Phase 3 progressively add one variable at a time (see §8.2):

| Wave | Adds | Time-box |
|---|---|---|
| Wave A | Privacy `On` | 1–2 days |
| Wave B | Full scope `S3` | 1–2 days |
| Wave C | Linkage `L2`, then `L3` (federation) | 2–3 days |

_(Phase 2's baseline run—`P=Off`, `L=L1`—is the calibration step the waves build on. It is not a wave.)_

---

### 3. Background and Motivation

#### 3.1 The Production Incident (resolved—but Two Lessons remain)

In April 2026, cohort-discovery queries against `cuh-prod-1` timed out against HDRUK's external 5-minute SLA. Jakub Jaworski (CUH) and Oliver Rushton remediated it with three high-value indexes on 24 April 2026, and the timeout is now resolved.

We keep the incident in scope because indexing fixed the symptom, not the two underlying gaps:

- No predictability. We had no way of knowing that workload would breach the SLA until it did. We still cannot predict where the federated system breaks.
- No visibility. The DB-side logs showed no active queries while the upstream service reported timeouts—the failure was _silent_ at the database tier and only surfaced at the HDRUK web layer. We only learned of it when the customer told us. This failure-surface mismatch is itself a finding the programme must reproduce deliberately (see §8.3 and risk 7).

#### 3.2 Year-end Target

By year-end we expect five active provider nodes, each with 1M–3M patients. AS05 (31 July 2026) requires a scale test against a synthetic cohort spanning ≥5 data providers, with at least two providers exposing OMOP `MEASUREMENT` tables of ≥500M rows. The deliverable is a report quantifying query execution time, resource utilisation, and cost per query, with blockers and bottlenecks documented.

#### 3.3 What This Document Captures

Six weeks of architectural planning (since early April 2026), the 7 May team meeting outcomes, and the 14 May design review—consolidated into a single executable plan. Five Parquet datasets are ready; the stress harness, monitoring, and DB provisioning are the remaining work.

---

### 4. Test Definition: System Under Test and Posture

#### 4.1 What Kind of Test This Is—and What It Is Not

"Stress test" covers a family of distinct test types with different durations, tools, and deliverables. This programme is explicit about which it runs:

| Test type | In programme? | Notes |
|---|---|---|
| Capacity planning | ✅ Primary | "X patients per query needs Y node spec" / "five federated nodes break at Z concurrency" |
| Scalability | ✅ Primary | Does federation scale linearly, or does coordination overhead dominate? |
| Load testing | ✅ Supporting | Maximum sustainable throughput per node at a given hardware spec |
| Performance characterisation | ✅ Supporting | Baseline p50/p95/p99 latency curves per cohort size |
| Soak / endurance | ❌ Deferred | No multi-day sustained runs—candidate follow-on |
| Spike | ❌ Out of scope | No sudden-surge scenarios |
| Chaos engineering | ❌ Out of scope | No deliberate node loss, partition, or secret-store outage—explicit follow-on |
| Performance regression CI | ❌ Out of scope | Candidate follow-on once Phase 4 (report-out) lands |

In one sentence: this is a _capacity-and-scalability discovery exercise_ on the FFNode / OMOP federated query path, executed against synthetic NHS-scale data, with explicit exclusions for soak, chaos, and regression coverage.

#### 4.2 System Under Test—Foreground Vs Background

In plain terms: "the clusters" is too vague to test. We split the system into two groups. Foreground layers are the ones we're actually measuring—the stopwatch is on them. Background layers are everything that simply has to keep working for the result to count; we're not measuring them, but if one falls over it pollutes the result. Keeping them separate matters because, if you don't, a background hiccup looks like a real finding and a real finding gets written off as "infra being flaky."

##### Foreground—these Layers ARE the Test

| Layer | What we're measuring |
|---|---|
| F1. Federated query path (`fitConnect` hub + spokes) | End-to-end latency · routing overhead · cross-node bytes · partial-result vs full-failure semantics. _Tested last, not first—see baseline-first note below._ |
| F2. Per-node database tier (PostgreSQL / MSSQL per node) | Query latency · lock waits · temp spill · OOM behaviour · reindex viability · slow-query patterns. _We test this two ways: directly against the DB (raw capacity/limits, Axis A) and via the workflows (normal usage, Axis C)._ |
| F3. Userflow permutation engine (FTFL-480) | This is the load generator. It replays a real FITFILE cohort-discovery workflow many times over, varying five inputs (cohort size × scope × privacy × S3 export × extract cap × linkage). Privacy treatment is applied as part of this flow using the default privacy treatment template—it is not a separate benchmark layer. We measure workflow duration and classify any errors. |
| F4. Per-node database tier (PostgreSQL / MSSQL per node) | Query latency · lock waits · temp spill · OOM behaviour · slow-query patterns. _We test this two ways: directly against the DB (raw capacity, Axis A) and via the workflows (normal usage, Axis C)._ |

##### Background—these Layers MUST Work but Are NOT the Experiment

| Layer | Required state during a test window |
|---|---|
| AKS control plane | Stable; not under deliberate stress |
| ArgoCD reconciliation | Auto-sync disabled on target test apps (avoids imperative-patch races) |
| Vault / VSO secret delivery | Stable; token TTLs ≥ test-window duration |
| cert-manager / TLS | DNS-01 challenges working; certificates valid for the duration |
| Azure Firewall / vVPN | Phase 1: not in path (single region, Azure UK South). Phase 2: in path but pre-validated |
| Container registry (ACR) | Images pre-pulled on test nodes; no on-demand pulls during the window |
| Monitoring stack (Grafana / Prometheus / Alloy) | Live, scraping, with the three required dashboards (§10) populated before Phase 2 |

> Baseline-first (reviewer-requested, agreed). Federation (F1) is the _last_ thing we test, not the first. We characterise a single node on its own (Phase 2 / Axis A) before introducing any cross-node behaviour (Phase 3 Wave C / Axis B). This is Decision D1: the CUH problem was a single-node query/join issue, which is decoupled from federation—so we isolate and understand that before adding the federation variable.

> Operational rule: if a background layer fails during a test, that is a test invalidation, not a finding. The run is discarded, the fault is remediated, and the run is retried. Mis-classifying a background failure as a foreground finding is the single most common cause of bad stress-test reports.

##### Explicitly out of the SUT (this round)

- `omop-cli`—the internal tool used to provision synthetic OMOP data onto nodes. It is used during Phase 0 (data setup) but is not the load generator and is not being characterised in this programme. It has its own separate capacity programme targeting the 10M-patient scale.
- Cross-cluster private networking solutions (Azure ExpressRoute, site-to-site VPN)—out of scope for all phases. All test connectivity is via public endpoints (see §7.4).
- Customer-facing query UX—only the back-end federated query path is in scope.
- The pipeline that builds the test harness itself—assumed stable; if it fails, the test is _deferred, not failed_.

#### 4.3 Workload Profile

Having defined _what_ we measure (§4.2), this section pins down _the load we measure it under_—so every run is comparable and reproducible. The headline: realistic cohort _shapes_, synthetic clinical _content_, driven sequentially by one generator.

| Dimension | Specification |
|---|---|
| Direction | Read-only throughout all test phases. OMOP cohort discovery is overwhelmingly read-dominated; no writes occur during the permutation programme. |
| Source | Synthetic only. Synthea-generated OMOP CDM v5.4. No real PII. |
| Load generator | The FTFL-480 userflow permutation script. (`omop-cli` is the _data_ generator, not the load generator—important distinction.) |
| Arrival pattern | Discrete test cases run sequentially within a wave. No concurrent or bursty request modelling. |
| Realism trade-off | _"Realistic overlap in cohorts—not realistic clinical data"_ (Oliver Rushton, 16 Apr). Linkage distribution targets 70–85% single-trust / 15–30% 2+ trusts / 5–10% complex multi-site. |
| Query mix | Currently unknown—see OQ-8. The 216-case grid is a structured substitute for real query telemetry. _(Acknowledged limitation.)_ |

#### 4.4 Programme Posture—⚠️ Decision Required

> This section contains an unresolved team disagreement—see open item D-g in §14.2. Do not start Phase 3 until it is closed.

Two reviewers have given conflicting direction on the programme's stop condition:

| Position | From | Stance |
|---|---|---|
| A | Leon Ormes | "We need to know where the system fails—we have no idea right now." Run until something breaks to surface unknown limits. |
| B | Oliver Rushton | "Only move up to the defined customer requirement (AS05). We don't have time to keep going beyond it. If we get there, that defines the known working limit." |

Both positions agree on one thing: we currently have no performance baseline and no characterised failure modes. The disagreement is purely about how far beyond the AS05 requirement (if at all) we push.

What is agreed:

- Performance characterisation—p50/p95/p99 latency curves, resource utilisation, and cost-per-query at each cohort size and scope tier. This is the "how does it behave" picture and is in scope under either position.
- The AS05 milestone—at minimum, the system must be shown to work at the required scale (5 nodes, ≥500M-row `MEASUREMENT`, HDRUK 5-min SLA). This is a hard validation gate.
- Recording degradation—anything that struggles _on the way_ to the requirement is documented, regardless of which posture is adopted.

What differs:

- Under Position A, Phase 3 waves keep pushing beyond AS05 scale until something breaks.
- Under Position B, Phase 3 waves stop once the AS05 requirement is demonstrated; the requirement scale _is_ the known working limit.

Implications for the run plan (once decided):

- Breaking points and near-miss degradations are logged with reproduction coordinates `(C, S, E, X, P, L)`.
- Documenting a degradation or limit is a successful test outcome, not an indictment of the system—the whole point is to find it here, in synthetic testing, rather than via a customer.

#### 4.5 Hypothesis Framing—every Scenario is Falsifiable

Each Phase 3 test case is expressed as a falsifiable hypothesis _before_ it runs:

- H1. At cohort `1M`, scope `S2`, privacy `Off`, linkage `L1`: p95 latency on a synthetic test node will exceed 5 min due to a sequential scan on `CONDITION_OCCURRENCE` (no covering index).
- H2. At linkage `L3` (5 nodes): federation overhead adds ≥30% to p95 latency vs `L1`, dominated by `MEASUREMENT` transfers.
- H3. With privacy `On` (default template): privacy processing will not produce FK violations on `PERSON ↔ CONDITION_OCCURRENCE` joins.
- H4. With one node CPU-throttled to 50% baseline: a federated 3-node query returns a partial-results error surfaced to the caller—not a silent partial aggregate.
- H5. With S3 export `On`: export of a `NodeFull` cohort to S3 completes successfully and the output passes integrity checks.

This forces precision and makes outcomes informative either way—confirming advances the infra spec; refuting reveals an unknown.

---

### 5. Objectives and Success Criteria

The programme proves three axes. Each has explicit, measurable criteria.

#### Axis A—Single-node Capacity (infrastructure stress)

| What we're proving | Metrics | Success criterion |
|---|---|---|
| Single-node query capacity | p50/p95/p99 latency · DB CPU/mem/IO · error rate | No errors; latency rises predictably with cohort size (no "cliff") up to full node dataset |
| DB break points | Max connections, lock waits, temp spill, cancellations | First failure documented with exact error + resource snapshot; classify fixable (indexing/spec) vs architectural |
| Run-failure recovery | Restart time, idempotency | Not forced—observed if a run fails naturally during testing. If it occurs, verify the run can be retried without manual intervention (RAP auditability requirement). |

#### Axis B—Multi-node Federation

| What we're proving | Metrics | Success criterion |
|---|---|---|
| Federation up to 5 nodes | p95 end-to-end latency · cross-node bytes · timeout rate | Federation across 2 → 3 → 5 nodes completes without timeout; document max sustainable concurrency before SLA breach |
| Cross-cloud overhead (Phase 2 only) | Network RTT · federation latency delta | Cross-cloud (Azure UK South ↔ AWS eu-west-2) overhead quantified independently of query cost |
| Graceful failure under disparity | Error-propagation behaviour | A throttled node surfaces a meaningful error upstream; no silent partial result without an explicit "partial results" flag |

#### Axis C—Algorithmic / Userflow Permutations (FTFL-480)

| What we're proving | Metrics | Success criterion |
|---|---|---|
| Userflow scales with cohort size | Workflow duration per stage; error rate | Per cohort-size tier, completion within agreed budget; "cost per additional patient" curve is monotonic |
| Scope-of-extract impact | Rows exported, file sizes, stage timings | Export time correlates with selected scope; identify which tables dominate cost |
| Privacy-treatment overhead | Latency delta, CPU delta, suppression counts | Privacy `On` does not break referential integrity; overhead quantified |
| Multi-source linkage | Join counts, duplicate/missed links | Cross-node linkage preserves expected overlap (70–85% / 15–30% / 5–10%) |
| S3 export | Export duration · file integrity checks · error rate | Export to S3 completes at each cohort-size tier; output passes integrity check |

#### External Constraint—HDRUK Timeout

5 minutes wall-clock per query. Per-query _wall time_—not DB-side execution time—is the contractual measurement. This is the primary go/no-go criterion for federated cohort discovery. An internal SLA is a candidate alternative pending decision (see OQ-7 / §15).

---

### 6. Scope

#### 6.1 In Scope

- Synthetic OMOP CDM v5.4 data across 5 nodes (Parquet datasets already produced).
- Pre-flight data-quality gates per node.
- Single-node characterisation, multi-node federation (2/3/5 nodes), userflow permutations.
- Monitoring stack—three Grafana dashboards under FTFL-476 / FTFL-478 (detailed in §10).
- A documented "where it breaks" report with reproduction coordinates and infrastructure recommendations.

#### 6.2 Out of Scope (this round)

- Cross-cloud federation (Azure UK South ↔ AWS eu-west-2)—conditionally Phase 2; out of scope until the team confirms (OQ-6).
- Chaos engineering—node loss, partition, secret-store outage. Follow-up programme.
- Real-PII testing—synthetic only.
- Performance regression CI—candidate follow-on once Phase 4 (report-out) lands.
- Hyve ETL pipeline testing—out of scope. The Hyve pipeline is partner-owned; The Hyve will test it independently.

#### 6.3 Assumptions

- The 5 Parquet datasets are final and version-pinned (precondition for Phase 0).
- ArgoCD auto-sync on target test apps will be disabled during test windows—a recurring source of imperative-patch races.

---

### 7. Environment and Architecture

#### 7.1 Production Node Inventory (reference only—cannot Be Used for testing)

> Confirmed by Oliver Rushton: production nodes are off-limits for all stress-test activity. Using them would interrupt customer workloads and ongoing development. This table is provided for context only—to understand what the synthetic nodes need to mimic.

| Node | DB engine | AKS cluster | Notes |
|---|---|---|---|
| `ff-a` | MSSQL | prod-1 | Coordinating hub |
| `ff-b` | MSSQL | prod-1 | Spoke |
| `ff-c` | MSSQL | prod-1 | Spoke |
| `barts` | MSSQL | prod-1 | Live NHS data |
| `cuh-prod-1` | PostgreSQL | hie-prod-34 | ETL'd; source of the April 2026 incident (resolved 24 Apr) |
| `mkuh-prd-4` | PostgreSQL | mkuh-prd-4 | ETL'd via The Hyve container |
| `nwsde-prod-1` | TBC | nwsde-prod-1 | NWSDE—DB engine to confirm |

#### 7.2 Synthetic Test Nodes—5 Dedicated New Nodes Required

> Confirmed by Oliver Rushton: we need 5 brand new, dedicated nodes—none of the production estate can be used. The 5 Parquet datasets already generated are OMOP CDM v5.4 (no Hyve work required); the task is provisioning the infrastructure to host them.

The synthetic nodes are provisioned using the FTFL-475 / FTFL-479 data generation and ingestion pipelines.

> ⚠️ Open: see flagged inconsistency 1 at the top of this document. D1 specifies starting with 5 co-located DBs on _one_ oversized node; Ollie's comment implies 5 _separate_ nodes. Confirm which topology applies before provisioning work begins. (This affects cost, IOPS contention, and the network test path.)

#### 7.3 Hardware Heterogeneity—variance to Capture before Testing

Production nodes are not homogeneous. The harness must record these per run so results are replayable.

| Dimension | Why it matters | Required column |
|---|---|---|
| Disk type / IOPS | OMOP large-table scans (`CONDITION_OCCURRENCE`, `OBSERVATION`, `MEASUREMENT`) are I/O-bound; NVMe vs Premium SSD vs HDD = order-of-magnitude latency difference | `disk_type`, `iops_limit` |
| Network egress | Federated queries ship Parquet intermediates; 100 Mbit/s NHS-internal vs 10 Gbit/s intra-AZ entirely changes federation cost | `network_egress_mbps` |
| DB engine | MSSQL and PostgreSQL produce different execution plans and index behaviour | `db_engine`, `db_version` |
| K8s nodepool sizing | `mkuh-prd-4` has 23.25 GiB RAM across 3 nodes—much smaller than EoE HIE nodes | `node_pool_spec` |

> Action: produce a hardware-inventory table for all existing production nodes before designing the synthetic-node spec. Owner: Leon Ormes / Oliver Rushton. Target: Sprint 16. _(Tracked as PA-1 / OQ-1 → §15.)_

#### 7.4 Network Topology—phased

All test connectivity uses public endpoints (confirmed by Oliver Rushton). There is no intra-cluster networking in scope and no Azure Private Link in use. Private networking solutions (ExpressRoute, site-to-site VPN) are explicitly out of scope for all phases.

Cloud and region: the estate spans two clouds—Azure (region UK South) and AWS (region eu-west-2). The network testing is phased across this divide:

| Phase | Network class | Span | Goal |
|---|---|---|---|
| Phase 1 | Single cloud, public endpoints | Azure UK South only | Eliminate the network as a variable—isolate query/join behaviour |
| Phase 2 (conditional, OQ-6) | Cross-cloud, public endpoints | Azure UK South ↔ AWS eu-west-2 | Quantify cross-cloud network overhead as an independent variable |

- Decision gate before Phase 2: document the expected p95 federation latency budget so pass/fail is unambiguous (OQ-6). _Estimated effort: 1 day (per Oliver Rushton)._
- Pre-condition (Robin Mofakham): the testing cluster has a sync issue tied to recent Grafana Alloy monitoring changes (FTFL-638). This must be resolved before Axis B testing begins.

#### 7.5 Topology Approach—single Oversized First, Multi-node Second (Decision D1)

Four approaches were considered:

| Approach | Pros | Cons |
|---|---|---|
| 5 DBs on one oversized node (selected) | Eliminates network variable; fast to spin up; easy to instrument; direct comparison vs `mkuh-prd-4` specs | All DBs share one disk subsystem—IOPS contention is artificial |
| 5 separate nodes | Matches prod topology; exposes real failure modes | More infra to manage; harder to isolate query bugs from network bugs |
| Single node, single DB | Cheapest baseline | Does not probe co-located contention or federation routing |

Rationale: the original blocker was single-node query/join behaviour (the CUH incident), which is _decoupled_ from federation. We characterise that first, then introduce federation as an additional variable.

#### 7.6 MKUH-specific Risk—PostgreSQL on the System Pool

`mkuh-prd-4` runs PostgreSQL on the AKS cluster's System Pool (3 nodes, 23.25 GiB RAM total, 371.61 GiB disk), sharing resources with core Kubernetes workloads (ArgoCD, VSO, monitoring agents).

| Failure mode | Mechanism |
|---|---|
| Memory pressure | Co-located workloads cause query spill to disk or OOM kills during large cohort scans |
| I/O contention | Kubernetes logging/audit competes with DB I/O on shared disks |
| Unbounded containers | 41 / 127 containers on this cluster have no resource requests/limits (Grafana snapshot, 13 Apr) |

Mitigations before stress-testing MKUH:

1. Set resource requests/limits on all containers (priority on the 41 currently unbounded).
2. ~~Move PostgreSQL to a dedicated User Node Pool~~—closed: not required (confirmed by Oliver Rushton). Oliver has configured the MKUH OMOP PostgreSQL database settings based on estimated population size; those settings should be reviewed and confirmed before load is applied.
3. Capture current Grafana baseline resource consumption before any load is applied.

---

### 8. Test Design

#### 8.1 Permutation Grid (FTFL-480)

Six variables defined as discrete level-sets. The Cartesian product is the full grid; waves run subsets.

| Variable | Levels |
|---|---|
| C—Cohort size | 1k · 10k · 100k · 1M · NodeFull · 5NodeFull |
| S—Selection scope | S1 Minimal (`PERSON` + `VISIT_OCCURRENCE` + `DEATH`) · S2 Core clinical (S1 + `CONDITION_OCCURRENCE` + `DRUG_EXPOSURE` + `MEASUREMENT`) · S3 Extended (scope to be defined from actual SDE data access requests—see action below) |
| E—Extract cap | Uncapped · Capped (hard `LIMIT` / `TOP` on the extract SQL to isolate query planning from data volume—confirmed by Oliver Rushton) |
| P—Privacy treatment | Off · On (default privacy treatment template applied—_not_ k-anonymity; confirmed by Oliver Rushton) |
| X—S3 export | Off (query only) · On (export cohort extract to S3) |
| L—Linkage scenario | L1 Single node · L2 Two nodes · L3 Five nodes (primary goal: prove the system can query 5 OMOP datasets and produce a unified output—exact patient overlap distribution is secondary) |

> Action (Oliver Rushton): define the S3 table set for scope based on actual data access requests the SDE has processed to date. This replaces the previously assumed table list.

Full grid: |C| × |S| × |E| × |P| × |X| × |L| = 6 × 3 × 2 × 2 × 2 × 3 = 432 cases.

> ⚠️ The addition of X (S3 export) doubles the grid from 216 to 432 cases. The wave structure below should be reviewed to confirm whether X is tested in the baseline or added as a separate wave.

#### 8.2 Wave-based Execution (Phase 3)

In plain terms (Decision D4): running all 432 combinations in one go would mean that, when something breaks, we couldn't tell _which_ of the six variables caused it. So we don't. We start from the simplest baseline and add exactly one new variable at a time, in waves. Each wave changes one thing, so every degradation or failure has a single, obvious cause.

| Stage | What's switched on | The one thing it adds | Time-box |
|---|---|---|---|
| _Phase 2 baseline_ | `C ∈ {1k…NodeFull}`, `S ∈ {S1,S2}`, `E=Uncapped`, `P=Off`, `X=Off`, `L=L1` |—(the starting point) | 1–2 days |
| Wave A | Baseline + S3 export | Export to S3 (`X=On`) | 1–2 days |
| Wave B | Wave A + privacy on | Privacy treatment (`P=On`) | 1–2 days |
| Wave C | Wave B + extended scope | Extended extract scope (`S=S3`) | 1–2 days |
| Wave D | Wave C + multiple nodes | Federation (`L=L2`, then `L=L3`) | 2–3 days |

Each wave produces a ranked list of degradation/failure coordinates `(C, S, E, P, X, L)` with first-error classification: _timeout · OOM · SQL error · export failure_. Because only one variable changes per wave, the coordinate tells you the cause.

#### 8.3 Graceful Vs Silent Failure under Resource Disparity

A critical safety concern motivated by the CUH incident (April 2026), where queries timed out at the HDRUK web layer while the DB tier showed no active query.

- Deliberately throttle one node via Kubernetes resource limits while running a federated 3-node query. Confirm a meaningful error surfaces to the caller—not a silent partial result.
- Document partial-result behaviour: does the Patient Querier return aggregates from 2/3 nodes, or reject the whole query?
- Document whether `fitConnect` has a configurable per-node sub-query timeout, and what the fallback is (OQ-4—Enric / Pavlo).

#### 8.4 Database Sizing Requirements (before Any Data is loaded)

- Disk allocation ≥ 3× the Parquet data size, to allow for indexes plus temp space.
- Apply the canonical OHDSI index set plus the three high-value indexes added by Jakub Jaworski to CUH on 24 April 2026.
- Run Achilles and WhiteRabbit per node before the first load test (see §9).

#### 8.5 Slow-query Logging Configuration

| Engine | Configuration |
|---|---|
| PostgreSQL | `pg_stat_statements` enabled; `auto_explain` enabled; `log_min_duration_statement = 500ms` |
| MSSQL | Query Store enabled; `QUERY_CAPTURE_MODE = AUTO` |

---

### 9. Data Quality Gates (Pre-flight—Phase 1)

> Stop condition (Decision D5): any node failing a quality gate blocks all load tests until remediated. _"Don't test garbage."_

#### 9.1 Schema and Integrity

- OMOP CDM v5.4 table presence + required columns per node.
- PK uniqueness; FK consistency—minimally `PERSON ↔ {VISIT_OCCURRENCE, CONDITION_OCCURRENCE, DRUG_EXPOSURE, MEASUREMENT, OBSERVATION}`.
- Concept-ID sanity: % standard concepts, % `concept_id = 0`, % deprecated.
- Generic ETL Container version pinned to ≥ v1.2.0 (addresses the `DEMOG` vs `DEMOGS` table-name mismatch).

#### 9.2 Achilles—distribution Sanity (per node)

Row counts per table · top concepts per domain · person counts per clinical table · visit-distribution sanity.

#### 9.3 WhiteRabbit—profiling Sanity (per node)

Field null rates · value-frequency distributions · "weirdness" detection (e.g. all DOB on the same day, single-value columns).

#### 9.4 Overlap Validation (critical for L2/L3—hard pre-condition)

- Compute overlap stats across the 5 Parquet datasets: % persons in 1 node / 2 nodes / 3+ nodes.
- Confirm distribution matches target: 70–85% / 15–30% / 5–10%.
- If `Person_ID`s are disjoint across the 5 datasets, L2 and L3 degrade to federated-volume tests, not linkage tests. This is OQ-8 and a hard pre-condition for any test where `L > L1`.

#### 9.5 DQD (optional)

Run the OHDSI Data Quality Dashboard on a smaller cohort tier first (e.g. 100k / 1M) to validate the QA harness before scaling to NodeFull. Complements WhiteRabbit rather than replacing it.

---

### 10. Monitoring and Observability (FTFL-476 / FTFL-478)

#### 10.1 Required Metrics per Node

System / container—CPU (usage %, throttling, load avg) · Memory (RSS, working set, OOM kills, page faults) · Disk (read/write throughput, IOPS, latency, disk-full %, temp usage) · Network (bytes in/out, retransmits, cross-node bandwidth during federated runs).

Database—active connections, queue depth · query runtime (p50/p95/p99), timeouts, cancellations · lock waits, deadlocks · buffer-cache hit ratio, temp/sort spill · WAL/log growth and checkpoints (PostgreSQL; MSSQL equivalents) · index usage and top-N slow-query log.

Workflow / application—Run ID, scenario coordinates `(C, S, E, P, L)` · stage timings (query-build · execute · privacy · export-packaging) · rows scanned / returned / bytes returned · error taxonomy (timeout · OOM · SQL error · referential-integrity violation).

#### 10.2 Three Required Dashboard Panels

| Panel | Purpose | Key metrics |
|---|---|---|
| Run Overview | One row per test case for fast scanning | Duration · peak CPU/mem · p95 latency · error flag |
| Bottleneck Board | Identify dominant cost centres | Top offenders (queries, tables, stages) by time and IO |
| Federation Board | Quantify multi-node overhead | Cross-node network bytes · added latency per additional node |

#### 10.3 Dashboard Delivery

- Add the three panels as acceptance criteria on FTFL-476.
- Add per-DB IOPS, per-node query queue depth, and cross-node federation bytes/sec as panel extensions on FTFL-478.
- Dashboards must be live and verified before Phase 2 begins—you cannot stress-test what you cannot measure.

---

### 11. Risks and Known Failure Points

#### 11.1 Failure-point Register

| # | Failure mode | Risk | Detection | Mitigation |
|---|---|---|---|---|
| 1 | Multi-node federation cliffs—bandwidth saturates at 5 nodes | High | Federation Board cross-node bytes | Cap concurrency; route Phase 2 over higher-bandwidth links |
| 2 | DB reindexer OOM—maintenance jobs exceed memory | High | OOM kill counter; Grafana memory panel | Right-size DB; schedule reindex outside test window |
| 3 | Privacy treatment destroys referential integrity | High | Post-run FK consistency check | Validate every privacy-ON wave against the schema integrity gate |
| 4 | Algorithmic tracing / linkage bottlenecks—MPS struggles with messy demographics | Medium | Stage-timing breakdown | Capture linkage stage timings as a first-class metric |
| 5 | Vocabulary / concept-mapping gaps—UK SNOMED/dm+d lack OMOP equivalents | Medium | WhiteRabbit `concept_id = 0` rate | Document gaps; route to vocabulary backlog |
| 6 | Run-failure recovery—long jobs can't resume without manual DB surgery | Medium | Restart test in Phase 2 | Harness must be idempotent; RAP/auditability requires this |
| 7 | Silent failure at DB tier while upstream times out—and we only learn of it from the customer (the CUH incident class) | High | Throttle test in §8.3; plus the §10 dashboards must surface DB-tier silence in real time | Force surfacing of partial-result vs full-failure semantics; ensure our own monitoring catches it before a customer does |
| 8 | ArgoCD auto-sync racing imperative test changes | Medium | n/a—operational | Disable auto-sync on test apps before each window |

#### 11.2 Kill Criteria—abort the Test Immediately If

- Any production node (real, non-synthetic) shows error rate > baseline + 2σ for > 5 minutes.
- Any privacy-ON wave produces FK violations on `PERSON` joins.
- Cost burn on the test subscription exceeds the documented daily ceiling.
- Vault token or cert-manager error rate spikes (potential cascade into customer environments).

---

---

### 12. Execution Plan (detail)

_(Phase summary table is in §2. Per-phase detail follows.)_

- Phase 0—Register Assets (0.5 day): dataset manifest (version · vocabulary version · row counts · SHA-256 checksum · node-ID mapping) · confirm overlap engineering (OQ-8) · pin Generic ETL Container ≥ v1.2.0.
- Phase 1—Pre-flight Quality Gates (1–2 days): see §9. Stop-condition: any failing node blocks Phase 2.
- Phase 2—Baseline Single-node (1–2 days): subset `C ∈ {1k…NodeFull}`, `S ∈ {S1,S2}`, `E=Uncapped`, `P=Off`, `L=L1` · p50/p95/p99 latency per cohort size · DB CPU/mem/IO per run · confirm reindexer behaviour (risk 2) · verify run is restartable/idempotent (RAP).
- Phase 3—Full Permutation Waves (3–7 days, parallelisable): run the 216-case grid in Waves A → B → C (§8.2) · record exact failure coordinates · classify first error per dimension.
- Phase 4—Report-out (0.5–1 day): deliverables below.

Phase 4 deliverables:

- "Where it breaks" table—first failure per dimension with exact reproduction coordinates.
- Recommended infrastructure spec per node (CPU / memory / disk / network).
- Recommended DB/indexing changes vs architectural constraints—separating _"we can fix this"_ from _"this is a re-architect."_
- Dashboard screenshots + run manifests (RAP auditability).

> ⚠️ See flagged inconsistency 2: per-phase durations sum to ~7.5–12 working days; the "~1–2 weeks" figure in earlier drafts assumed parallelism. The per-phase figures above are the authoritative estimates.

---

### 13. Decision Log

| # | Decision | Source | Date |
|---|---|---|---|
| D1 | Start with a single oversized node hosting 5 co-located OMOP databases; escalate to 5 separate nodes only once query/join behaviour is understood | Planning meeting | 7 May 2026 |
| D2 | Connectivity for cross-cloud testing uses vVPN / IPsec—physical Leased Line ruled out on cost (Robin Mofakham) | Networking review | 13 May 2026 |
| D3 | Phase 1 of network testing is intra-region only (Azure UK South); cross-cloud (Azure UK South ↔ AWS eu-west-2) is Phase 2, conditional on Phase 1 outcomes | Planning meeting | 7 May 2026 |
| D4 | The full 216-case permutation grid runs in waves (A → B → C), never all at once | Planning meeting | 7 May 2026 |
| D5 | Pre-flight data-quality gates (WhiteRabbit + Achilles + schema/FK integrity) are an unconditional stop-condition—no load test runs against a node that has not passed | 16 Apr design session | 16 Apr 2026 |
| D6 | Hyve ETL pipeline testing is out of scope for this programme—The Hyve will test their own pipeline independently | This revision | 2 June 2026 |

---

### 14. Open Items Register (unified Actions + Decisions + questions)

> This single register replaces the old §13 (PA-_) and §14 (OQ-_), which tracked the same items twice. Original IDs are preserved in the Refs column.

#### 14.1 P0—Blockers (must Resolve This Sprint, before Execution starts)

| ID | Item | Owner | Target | Why it matters | Refs |
|---|---|---|---|---|---|
| B1 | Produce hardware-inventory table for all prod nodes (`disk_type`, `iops_limit`, `network_egress_mbps`, `db_engine`, `node_pool_spec`) | Leon Ormes / Oliver Rushton | Sprint 16 | Without it, results aren't replayable; synthetic spec is guessed | PA-1, OQ-1 |
| B2 | Confirm / engineer `Person_ID` overlap across the 5 Parquet datasets | Leon Ormes | Sprint 16 | If disjoint, L2/L3 become volume tests, not linkage tests | PA-2, OQ-2 |
| B3 | Define the query harness for FTFL-480 (workflow runner / direct SQL / Atlas-driven) | Oliver Rushton / Leon Ormes | Sprint 16 | Determines what "Selection scope" means concretely | PA-3, OQ-3 |
| B4 | Resolve the `mkuh-prd-4` Grafana Alloy sync issue (FTFL-638) blocking Axis B monitoring | Leon Ormes / Robin Mofakham | Sprint 16 | Monitoring must be live before Phase 2 | PA-4 |

#### 15.2 P1—Decisions For the next Planning Meeting

| ID | Decision required | Recommended | Owner | Refs |
|---|---|---|---|---|
| D-a | Confirm single-oversized-node-first approach (D1) vs 5 separate nodes—Ollie's comment implies 5 separate; D1 says co-located. Must resolve before provisioning. |—| Team | PA-5 |
| D-b | ~~Move `mkuh-prd-4` PostgreSQL to dedicated User Node Pool~~ | Closed: not needed (Oliver Rushton) |—| PA-6, OQ-5 |
| D-c | HDRUK 5-minute timeout—who owns the measurement? Ollie says it's the Hutch team's responsibility, not FITFILE's. Does it remain a success criterion for this programme, or do we define our own internal latency SLA? | Unresolved—see D-h | Oliver Rushton | PA-7, OQ-7 |
| D-d | Cross-cloud (Azure UK South ↔ AWS eu-west-2)—Phase 2 in this programme, or follow-on? | Recommend follow-on | Team | PA-8, OQ-6 |
| D-e | Partial-result vs full-failure semantics for federated node timeout—does `fitConnect` have a configurable per-node sub-query timeout? | Recommend explicit "partial results" flag, default fail-closed | Pavlo / Enric | PA-9, OQ-4 |
| D-f | Define which queries HDRUK users actually run (query-log access?) |—| Oliver Rushton / Weronika Jastrzębska | OQ-8 |
| D-g | Programme posture: open-ended limit-finding (Leon) vs stop at AS05 requirement (Ollie). Must be agreed before Phase 3. See §4.4. | Unresolved—team decision required | Leon Ormes / Oliver Rushton |—|
| D-h | HDRUK timeout ownership. Ollie: Hutch team should measure this, not FITFILE. Decision: does the 5-min timeout remain our external SLA gate, or do we define an internal query latency target for the path we own? | Unresolved | Oliver Rushton | OQ-7 |
| D-i | Monitoring sufficiency. Ollie: "Is the Kubernetes observability dashboards enough to monitor all the things we need?" Does the current K8s + Grafana/Alloy stack capture all §10.1 metrics (DB-tier query latency, lock waits, temp spill), or do we need DB-specific instrumentation? | Open | Leon Ormes / Robin Mofakham |—|
| D-j | S3 scope definition. Ollie: S3 table selection should be based on actual SDE data access requests, not an assumed table list. Oliver Rushton to provide the table list. | Open—action on Oliver Rushton | Oliver Rushton |—|

#### 14.3 P2—Deferred / Out-of-scope Candidates

| ID | Item | Disposition | Refs |
|---|---|---|---|
| F1 | Use-case clarity from Wesam (Helena's 5 May question) | Track as follow-on; do not block | OQ-9 |
| F2 | Warning mechanism for "too big" queries (upstream protection layer) | Follow-on programme, out of scope | OQ-10 |
| F3 | Chaos engineering—node loss, partition, Vault outage | Follow-on programme | OQ-11 |
| F4 | Performance-regression CI on the test harness | Follow-on once Phase 4 (report-out) lands | OQ-12 |

---

### 15. Jira Ticket Plan

#### 15.1 New Tickets to Raise

| Ticket | Summary | Parent | Priority | Owner |
|---|---|---|---|---|
| NEW1 | Register 5-node dataset manifest (versions, checksums, node IDs) | FTFL-488 | P1 | Leon Ormes |
| NEW2 | Confirm / engineer `Person_ID` overlap across 5 Parquet nodes | FTFL-475 | P1 | Leon Ormes |
| NEW3 | Run Achilles + WhiteRabbit pre-flight quality gates per node | FTFL-476 | P1 | TBC |
| NEW4 | Define query harness for FTFL-480 userflow test runner | FTFL-480 | P1 | Oliver Rushton |
| NEW5 | Build Phase 2 baseline single-node test harness | FTFL-476 | P1 | Leon Ormes |
| NEW6 | Implement Run Overview + Bottleneck + Federation Grafana dashboards | FTFL-476 | P1 | TBC |
| NEW7 | Execute Wave A permutation runs (S3 export) | FTFL-480 | P2 | TBC |
| NEW8 | Execute Wave B permutation runs (Privacy ON) | FTFL-480 | P2 | TBC |
| NEW9 | Execute Wave C permutation runs (Extended scope S3) | FTFL-480 | P2 | TBC |
| NEW10 | Execute Wave D permutation runs (Federation L2 then L3) | FTFL-480 | P2 | TBC |
| NEW11 | Produce final stress-test report + infra-spec recommendations | FTFL-476 | P2 | Leon Ormes |

#### 15.2 Existing Tickets Requiring Updates

| Ticket | Required action |
|---|---|
| FTFL-476 | Add the three dashboard panels (§10.2) as acceptance criteria |
| FTFL-480 | Confirm the 216-case permutation grid (5 variables) and wave execution order |
| FTFL-475 | Confirm data generation complete; close or move to Done if Parquet files are final |
| FTFL-479 | Confirm DB ingestion script targets Postgres for synthetic data loading |
| FTFL-638 | Resolve `mkuh-prd-4` Grafana Alloy sync issue (pre-condition for monitoring) |
| FTFL-652 | OMOP DB provisioning for stress testing—assign and sprint-slot |
| FTFL-635 | Stress Testing in the Application—clarify relationship to FTFL-476 / -480 |

---

### 16. Stakeholders

| Role | Name | Responsibility |
|---|---|---|
| Author / Platform lead | Leon Ormes | Document owner; Phase 0–3 execution; infrastructure |
| Query strategy | Oliver Rushton | Query design; CUH remediation context; HDRUK SLA owner |
| Indexing / DB tuning | Jakub Jaworski (CUH) | Index-strategy reference; CUH baseline data |
| Networking | Robin Mofakham | vVPN/IPsec design; cross-cloud feasibility |
| Programme / scoping | Helena Ahlfors | Use-case clarity; project-plan liaison |
| Federation semantics | Enric / Pavlo | `fitConnect` timeout & partial-result behaviour |
| Hyve liaison (observer) | Julia Kurps · Stefan (The Hyve) | Reviewers; Hyve will conduct their own pipeline testing independently |
| Query identification | Weronika Jastrzębska | HDRUK query-log access |
| NHS contacts | Alexis McKenna · Helen Duckworth | NHS-side validation |
| Other reviewers | Philip Russmeyer · Magali Ruffier · Jamie Reeve · Sean Donnelly (Telefónica Tech) | Design review |

---

### 17. First Physical Actions (this week)

1. Raise the eleven new Jira tickets listed in §15.1 (~30 minutes).
2. Add the three dashboard panels (§10.2) as acceptance criteria on FTFL-476.
3. Circulate this document to reviewers; book a 30-minute review session.
4. Confirm Phase 0 can start in Sprint 16 (5 Parquet datasets accessible to the test harness).

---

### Appendix—Reviewer Comment Resolutions

Tracking against Robin Mofakham's review comments. Delete this appendix before final publication (it exists to close the review loop).

| # | Comment (abridged) | Resolution in v3 |
|---|---|---|
| 1 | "Azure eu-west-2—do you mean UK South ↔ UK West?" | Fixed. `eu-west-2` is the _AWS_ region; "Azure" was the error. §7.4 now states the estate spans Azure (UK South) + AWS (eu-west-2); Phase 1 = intra-region Azure UK South; Phase 2 cross-cloud = Azure UK South ↔ AWS eu-west-2. D3 corrected. |
| 2 | "Translate the 216-grid-in-waves into something crystal clear." | Done. §8.2 opens with a plain-English explanation: we add one variable per wave so every failure has a single obvious cause. |
| 3 | "Three axes—just a formatting change to bullets." | Done. §1 lists the three axes as bullets. |
| 4 | "Three indexes added 24 April—didn't this resolve now?" | Confirmed resolved by Leon. §1 and §3.1 reframed: the timeout is fixed; the kept point is that we were blind to it until the customer reported it. |
| 5 | "§3 is noisy / high cognitive effort." | Addressed. Added a TOC + "how to read" guide; §4 reorganised with plain-language openers; abstract framing given concrete glosses. |
| 6 | "Foreground/background—what does this even mean?" | Done. §4.2 now opens with a plain definition (foreground = stopwatch is on it; background = just has to keep working). |
| 7 | "I'd like a single-node baseline first; federation is the final test." | Confirmed—this is already the design (D1). Made explicit with a "baseline-first" callout in §4.2 and in F1's row. |
| 8 | "Test the DB directly, or only via workflows?" | Answered: both. F2 now states we test the DB tier directly (Axis A, raw limits) _and_ via workflows (Axis C, normal usage). Harness _mechanism_ remains open item B3. |
| 9 | "Userflow permutation engine—don't understand the test." | Clarified. F3 row rewritten: it is the load generator that replays a real cohort-discovery workflow while varying six inputs. |
| 10 | "Phase 4—first mention of phases." | Fixed. §2 defines all phases (0–4) up front. |
| 11 | "Privacy-treatment (F5)—separate benchmark? relation to F3?" | Clarified, then confirmed by Ollie. F5 merged into F3: privacy is applied as part of F3 using the default template. No separate layer. |
| 12 | "§9—not familiar, is this a reference?" | Addressed. TOC added; cross-references spelled out on first use. |
| 13 | "No journey—add a table of contents." | Done. TOC + "How to read this document" narrative added. |
| 14 | "Stress-testing vs performance analysis?" | Reframed in §4.4—but now flagged as open decision D-g (Oliver Rushton adds a conflicting position; see §14.2). |
| 15 | "'…the deliverable, not an embarrassment'—what?" | Rephrased. §4.4 now: "Documenting a degradation or limit is a successful test outcome—better to find it here than via a customer." |

---

#### Oliver Rushton's Comment Resolutions (v4)

| # | Comment (abridged) | Resolution |
|---|---|---|
| 1 | "Phase 4—Hyve / ETL runs—out of scope" | ✅ Already removed in v3. Phase 4 (Hyve ETL) removed; Hyve will test independently. Captured as Decision D6. |
| 2 | "Extract cap—agreed, controlled via LIMIT / TOP" | ✅ Confirmed in grid. E variable description updated to name the `LIMIT` / `TOP` mechanism. |
| 3 | "Add export to S3 to the permutation list" | ✅ Done. New variable X (Export to S3: Off / On) added; grid now 432 cases; Wave A added; Axis C updated with export success criterion; H5 added to hypothesis set. |
| 4 | "F4. Hyve ETL pipeline—out of scope" | ✅ Already removed in v3. |
| 5 | "F5. Privacy—out of scope as a separate layer; included in F3 using default privacy treatment template" | ✅ Done. F4 (privacy layer) removed; F3 updated to note privacy is applied as part of the workflow using the default template. k-anonymity references removed. |
| 6 | "omop-cli—clarify or delete" | ✅ Clarified. Added a plain definition in the "out of SUT" list: it's the data-provisioning tool, not the load generator, and has its own separate capacity programme. |
| 7 | "Cross-cluster data path—note that ExpressRoute / site-to-site VPN are out of scope" | ✅ Done. Added explicitly to the out-of-SUT list and §7.4. |
| 8 | "PHI—do you mean PII?" | ✅ Done. Changed throughout to PII. |
| 9 | "diurnal—concurrent" | ✅ Done. Changed to "No concurrent or bursty request modelling." |
| 10 | "Capacity & limits—we don't have time to go beyond the requirement" | ⚠️ Flagged as open decision D-g. Conflicts with Leon's earlier position. §4.4 presents both stances; team must agree before Phase 3. |
| 11 | "Discovery (limit-finding)—out of scope; only up to the defined customer requirement" | ⚠️ Same as above—D-g. |
| 12 | "Reindex / maintenance jobs—out of scope" | ✅ Removed from Axis A success criteria. |
| 13 | "Run-failure recovery—can't force it; observe if it happens" | ✅ Done. Reframed as "observed if encountered during testing" rather than a deliberate test. |
| 14 | "packet loss—???" | ✅ Removed from Axis B cross-cloud metrics. |
| 15 | "Add export to Axis C" | ✅ Done. S3 export row added to Axis C success criteria table. |
| 16 | "Axis D—out of scope / pass to Hyve" | ✅ Already removed in v3. Confirmed as D6. |
| 17 | "HDRUK timeout—Hutch team owns this, not us" | ⚠️ Flagged as open decision D-h. Significant scope question; Leon and Oliver to align. |
| 18 | "data-quality—feels like Hyve's responsibility" | ✅ Clarified. The §9 quality gates are pre-flight checks on the synthetic OMOP datasets _we are generating for testing_—not Hyve pipeline QA. Hyve tests their own pipeline independently (D6). |
| 19 | "Monitoring—is K8s observability dashboards enough?" | ⚠️ Flagged as open decision D-i. Added to §14.2. |
| 20 | "datasets—OMOP, no Hyve work" | ✅ Already handled in v3. §7.2 confirms datasets are OMOP CDM v5.4 Parquet; no Hyve work involved. |
| 21 | "7.1—cannot use these" | ✅ Done. §7.1 reheaded as "reference only—cannot be used for testing"; rationale (interrupts customers and development) documented. |
| 22 | "7.2—need 5 brand new nodes, cannot use existing" | ✅ Done. §7.2 rewritten: 5 new dedicated nodes required. Topology open item (D-a) flagged. |
| 23 | "no intra-cluster—all via public endpoints" | ✅ Done. §7.4 corrected; intra-cluster and Azure Private Link references removed. |
| 24 | "None use Azure Private Link" | ✅ Done. Same as above. |
| 25 | "p95 federation latency budget—1 day" | ✅ Noted. §7.4 decision gate updated: "estimated effort 1 day (per Oliver Rushton)." |
| 26 | "3 nodes, 23.25 GiB RAM—see my configured settings" | ✅ Noted. §7.6 references Oliver's configured MKUH PostgreSQL settings. |
| 27 | "Move PostgreSQL to dedicated User Node Pool—no, we don't need this" | ✅ Closed. D-b marked as closed in §14.2; §7.6 mitigation updated. |
| 28 | "S3 scope—base off actual SDE data access requests" | ✅ Done. S variable description updated; action added to Oliver Rushton. |
| 29 | "k-anonymity + nullification—only default privacy treatment template" | ✅ Done. P variable and all references updated: "default privacy treatment template." k-anonymity removed. |
| 30 | "L3 linkage—just prove we can query 5 OMOP datasets and produce unified output" | ✅ Done. L3 description updated to focus on proving 5-node unified query output; exact overlap distribution removed as a requirement. |
