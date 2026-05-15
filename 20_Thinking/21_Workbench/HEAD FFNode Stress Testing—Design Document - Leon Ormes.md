---
alias: []
aliases: []
captured: 2026-05-15T09:15:17+01:00 2026-05-15T09:15:17+01:00
created: 2026-05-07T09:00:00+01:00
journal: Daily
journal-date: 2026-05-13
modified: 2026-05-07T09:28:28+00:00
source: https://fitfile.atlassian.net/wiki/spaces/~633ae2b9fedc6169aed8f601/pages/2812477441/FFNode+Stress+Testing+Design+Document
status: processing
tags:
  - input
  - prodos/head
  - state/thinking
  - ffnodes
  - ftfl
  - head
  - meeting
  - omop
  - stress-testing
title: HEAD FFNode Stress Testing — Meeting 2026-05-07
type: daily
updated:
---

## Raw Output / Content

## FFNode Stress Testing—Design Document

Status: Draft | Author: Leon Ormes | Date: 14 May 2026 | Jira: [FTFL-476 — OMOP Stress Testing infra + monitoring](https://fitfile.atlassian.net/browse/FTFL-476) | [FTFL-480 — Stress Testing test userflows](https://fitfile.atlassian.net/browse/FTFL-480)

---

### Background and Motivation

The FITFILE platform federates OMOP CDM v5.4 data across multiple NHS provider nodes (ff-a, ff-b, ff-c, Barts, CUH, MKUH, NNUH, NWSDE, etc.). We have a live production signal that motivated this work: cohort-discovery queries against CUH are timing out against HDRUK's 5-minute SLA, with Jakub Jaworski (CUH) and Oliver Rushton actively remediating indexing strategy. The stress test must answer the same class of question systematically—before we reach production scale—across all node topologies we expect to operate by year-end (~5 nodes, 1M–3M patients each).

This document captures all open questions raised in the 14 May planning meeting and proposes a staged design to resolve them.

---

### Section 1—Hardware Heterogeneity

Problem statement. Production nodes are not homogeneous. Beyond CPU and memory, the following dimensions differ between nodes and are likely to dominate real-world query latency:

| Dimension | Why it matters |
| --- | --- |
| Disk type / IOPS | OMOP large-table scans (CONDITION\_OCCURRENCE, OBSERVATION, MEASUREMENT) are I/O-bound. NVMe vs HDD vs Azure Premium SSD produce order-of-magnitude latency differences. |
| Network bandwidth | Federated queries ship Parquet intermediates between nodes. A 100 Mbit/s link (NHS-internal) vs 10 Gbit/s intra-AZ link changes federation cost completely. |
| DB engine | MKUH runs PostgreSQL on the System Pool; other nodes may run MSSQL. Execution plan quality and index behaviour differ. |
| Kubernetes node pool sizing | mkuh-prd-4 today shows 23.25 GiB RAM across 3 nodes—much smaller than the EoE HIE nodes. |

Action items:

- Produce a hardware inventory table for all existing prod nodes before designing any synthetic node.
- Include disk\_type, iops\_limit, network\_egress\_mbps, db\_engine, and node\_pool\_spec columns.
- The stress test must record these specs alongside every test run so results are replayable against known hardware.

---

### Section 2—Network Topology and Cross-internet Vs Intra-cloud Testing

Problem statement. The fitConnectHosts topology ([network audit, March 2026](https://github.com/)) distinguishes two network classes: intra-cluster (.svc.cluster.local) and cross-internet public endpoints. All production SDE connections (EoE → NWSDE, CUH → HIE hub) traverse the public internet or Azure Private Link.

Questions to answer:

- Should the stress test environment reproduce intra-cloud latency only, or must it also test cross-internet federation performance?
- AWS and Azure are likely to be involved at different nodes. A federated query from an Azure-hosted node to an AWS-hosted node introduces asymmetric routing costs not present in synthetic tests.

Proposed approach:

- Phase 1: All synthetic nodes intra-AZ (Azure eu-west-2). This eliminates network as a variable and isolates query/join performance—answering the "workflow pool" feasibility question first (see Section 3).
- Phase 2: Two nodes placed in separate Azure regions (or Azure + AWS cross-cloud) to quantify network overhead as an independent variable.
- Decision gate: Document the expected p95 federation latency budget before Phase 2 begins, so pass/fail criteria are unambiguous.

---

### Section 3—Single-node Oversized Workflow Pool Vs Multi-node Topology

Core question from the meeting: _Is it feasible to use a single node with a massively oversized workflow pool to first isolate and resolve query/join problems, before introducing real multi-node complexity?_

Analysis:

| Approach | Pros | Cons |
| --- | --- | --- |
| 5 DBs on one node | Eliminates network variable; fast to spin up; easy to instrument; unblocks query optimisation work immediately | Does not expose federation routing overhead, cross-node privacy treatment, or per-node resource contention |
| 5 separate nodes | Matches prod topology; exposes real failure modes | More infra to manage; harder to isolate query bugs from network bugs |
| Single node, oversized pool | Cheapest/fastest; direct comparison against prod mkuh-prd-4 specs | All OMOP databases share one disk subsystem—IOPS contention will be artificial |

Recommendation: Start with Option C (single oversized node, multiple OMOP databases co-located) for the query/join problem isolation phase. This is consistent with [FTFL-480](https://fitfile.atlassian.net/browse/FTFL-480) which requires permutation-based test userflows before multi-node federation is relevant. Then escalate to 5 separate nodes to validate federation behaviour.

---

### Section 4—Mimicking Prod +2 Nodes

Requirement: Mimic the current prod setup, plus add 2 additional synthetic nodes to simulate the year-end state.

Current prod node inventory (to be confirmed):

| Node | DB engine | AKS cluster | Notes |
| --- | --- | --- | --- |
| ff-a | MSSQL | prod-1 | Coordinating hub |
| ff-b | MSSQL | prod-1 | Spoke |
| ff-c | MSSQL | prod-1 | Spoke |
| barts | MSSQL | prod-1 | Live NHS data |
| cuh-prod-1 | PostgreSQL | hie-prod-34 | ETL'd; currently slow for cohort discovery |
| mkuh-prd-4 | PostgreSQL | mkuh-prd-4 | ETL'd via The Hyve container |
| nwsde-prod-1 | (TBC) | nwsde-prod-1 | NWSDE |

Synthetic additions for stress test: Two nodes to be provisioned with identical Synthea-generated OMOP CDM v5.4 data (1M patients each), using the data pipeline from FTFL-475/FTFL-479. Node naming convention: ff-stress-a, ff-stress-b.

---

### Section 5—Federated SDE Queries

Question: Should the stress test cover federated SDE queries specifically, i.e. multi-node cohort discovery?

Context from the network topology audit: The fitConnectHosts config defines the entry-point hub. A federated query fans out from the hub to all coordinating spokes, aggregates results, and returns. Privacy treatment (DIRECT / QUASI / SAFE column classification, feasibility-phase aggregate-only return) adds latency at every node.

Proposed test dimensions for FTFL-480 script (from the existing Jira spec):

- cohort\_size ∈ {1k, 10k, 100k, 1M, NodeFull}
- num\_tables\_selected ∈ {Minimal (S1), Core clinical (S2), Full (S3)}
- extract\_size—controlled via LIMIT
- privacy\_treatment ∈ {true, false}
- num\_omop\_data\_sources ∈ {1, 2, 3, 5}

Total permutation space before filtering: 5 × 3 × 3 × 2 × 4 = 360 test cases. Run in waves—start with single-source, scale up.

---

### Section 6—Query Selection and Cohort Size Observability

Problem: We do not currently know what queries real HDRUK users run, or whether synthetic cohort sizes will match prod cohort sizes. This matters because a 100k synthetic cohort may produce a very different query plan than a 1k cohort.

Risks identified:

- Synthetic data may not produce realistic cardinality for joins (e.g. PERSON ⋈ CONDITION\_OCCURRENCE ⋈ CONCEPT). Oliver Rushton noted ([omock discussion, Apr 16](https://fitfile.atlassian.net/browse/FTFL-31)) that mock data may lack the table coverage of full Synthea-generated data, trading realism for speed.
- HDRUK's 5-minute timeout is enforced externally—we must track per-query wall time, not just DB-side execution time.

Observability requirements (cross-reference FTFL-476 Grafana dashboard):

- Grafana Workflows Monitoring Dashboard must capture:
	- p50 / p95 / p99 query latency per node, per query class
		- DB CPU, memory, and I/O during query execution
		- Cross-node bytes transferred during federation
		- Timeout events and error codes
- Slow query logging must be enabled at the DB level (PostgreSQL pg\_stat\_statements; MSSQL Query Store) with log\_min\_duration\_statement = 1000ms as a starting threshold.
- Database sizing must be logged per test run (total table row counts, index stats, storage consumed).

---

### Section 7—Staged / Progressive Enhancement Approach

Question from the meeting: _With so many variables, is there a better approach—staged or progressive enhancement?_

Proposed test phases:

| Phase | Scope | Goal | Success criterion |
| --- | --- | --- | --- |
| 0—Pre-flight | All nodes | Data quality gate (WhiteRabbit + Achilles + OMOP CDM v5.4 schema checks) | All nodes pass before any load test starts |
| 1—Single-node baseline | 1 node, 1 DB, oversized pool | Establish query latency baseline; validate slow query logging; identify query/join problems | No errors; p95 latency ≤ 5 min for S1 cohort |
| 2—Single-node multi-DB | 1 node, 5 DBs co-located | Test IOPS contention; validate parallelism assumptions | Latency degradation ≤ 2× vs Phase 1 under full concurrency |
| 3—Multi-node federation | 3 nodes (prod-mimic) | Test federation routing, privacy treatment overhead, cross-node bytes | Federation across 3 nodes completes without timeout for 75% of queries |
| 4—Full 5-node | 5 nodes (prod +2) | Confirm production readiness; document breakpoints | Federation across 5 nodes; p95 latency documented per cohort size |

---

### Section 8—Risk: ETL'd Nodes (MKUH with PostgreSQL on System Pool)

Risk identified in the meeting. mkuh-prd-4 runs PostgreSQL deployed on the System Pool of its AKS cluster (3 nodes, 23.25 GiB RAM total, 371.61 GiB disk). This node was ETL'd by The Hyve container. System Pool placement means the DB shares resources with core Kubernetes workloads (ArgoCD, Vault Secrets Operator, monitoring agents).

Failure modes:

- Memory pressure from co-located system workloads can cause query spill to disk or OOM kills during large cohort scans.
- I/O contention with Kubernetes logging and audit workloads.
- Resource limits not set on 41/127 containers on this cluster (per Grafana dashboard snapshot from Apr 13).

Mitigation: Before stress testing MKUH, set resource requests/limits on all containers in the mkuh-prd-4 cluster. Move PostgreSQL to a dedicated User Node Pool if possible. Document current baseline resource consumption from Grafana before any load is applied.

---

### Section 9—Graceful Vs Silent Failure under Resource Disparity

Question: _What happens if servers have very different amounts of resources—would a query fail gracefully or silently?_

This is a critical safety concern for federated queries. Evidence from the CUH incident (April 2026): queries were timing out at the HDRUK web layer while the DB-side bunny logs showed no active queries—the failure was silent at the DB level but visible at the upstream service layer.

Test requirements:

- Deliberately throttle one node (via Kubernetes resource limits) while running a federated 3-node query. Verify the error surfaces to the caller with a meaningful message, not a silent partial result.
- Test partial result vs full failure semantics: does the Patient Querier return aggregate counts from 2/3 nodes, or reject the entire query?
- Document whether fitConnect has a configurable timeout for per-node sub-queries, and what the fallback behaviour is.

---

### Section 10—Database Sizing and Monitoring / Slow Query Logging

Requirements summary:

- All stress test databases must be sized against the OMOP CDM v5.4 standard (DDL from OHDSI/CommonDataModel) before data is loaded.
- Pre-test sizing checklist:
	- Confirm sufficient disk allocation (target: 3× the Parquet data size to allow for indexes + temp space).
		- Apply the [canonical OHDSI index set](https://github.com/OHDSI/CommonDataModel) (Jakub Jaworski applied 3 "high-value missing indexes" to CUH on Apr 24 2026—incorporate this as baseline).
		- Run Achilles and WhiteRabbit on each synthetic DB before any load test.
- Slow query logging:
	- PostgreSQL: pg\_stat\_statements, auto\_explain, log\_min\_duration\_statement = 500ms
		- MSSQL: Query Store enabled, QUERY\_CAPTURE\_MODE = AUTO
- Grafana dashboard extension (FTFL-478):
	- Add per-DB IOPS panel
		- Add per-node query queue depth
		- Add cross-node federation bytes/sec

---

### Open Questions Requiring Decision

| # | Question | Owner | Target |
| --- | --- | --- | --- |
| 1 | Confirm hardware spec inventory for all prod nodes | Leon / Oliver | Sprint 16 |
| 2 | Confirm: single oversized node first, then multi-node? | Team | Planning meeting |
| 3 | Define which queries HDRUK users actually run (query log access?) | Oliver / Weronika | Sprint 16 |
| 4 | Partial result vs full-failure semantics for federated query node timeout | Enric / Pavlo | Design review |
| 5 | MKUH PostgreSQL: move to User Node Pool before stress test? | Leon | Sprint 16 |
| 6 | Cross-cloud (AWS + Azure)—Phase 2 or out of scope? | Team | Planning meeting |
| 7 | Set HDRUK 5-minute timeout as primary success criterion or use internal SLA? | Oliver | Sprint 16 |

---

### Related Jira Tickets

- [FTFL-476 — OMOP Stress Testing infra + monitoring](https://fitfile.atlassian.net/browse/FTFL-476)—infrastructure and Grafana dashboard
- [FTFL-477 — MS SQL Server deployment](https://fitfile.atlassian.net/browse/FTFL-477)—✅ Done
- [FTFL-478 — Grafana Workflows Monitoring Dashboard](https://fitfile.atlassian.net/browse/FTFL-476)—in progress
- [FTFL-479 — Script to install OMOP data into target DB](https://fitfile.atlassian.net/browse/FTFL-476)
- [FTFL-480 — Stress test userflow permutation script](https://fitfile.atlassian.net/browse/FTFL-480)—Leon Ormes
- [FTFL-488 — Synthetic OMOP data storage](https://fitfile.atlassian.net/browse/FTFL-476)—✅ Done

## Raw Output / Content

You

I'm struggling with the clarifying stage after capturing. For instance, I have a summer work to do with stress testing our distributed k8s clusters with large sets of omop data. I want to run a natural planning model for it but can't get started. Help me with a trigger list/checklist. Review the LLM response and over advise

---

## Clarifying a Fuzzy Project: Stress Testing Trigger List

### 1\. The Real Problem (Quick Reframe)

You're not actually stuck on _clarifying_—you're stuck because "stress test the clusters with OMOP data" is not yet a project, it's a _fuzzy aspiration_. Natural Planning Model assumes the input is a single, well-bounded outcome. If you feed it a vague commitment, every phase becomes equally vague (which is exactly what the LLM produced—see §3).

The missing step between Capture and Natural Planning is Scoping: turning the fuzzy aspiration into one or more well-defined projects. _That_ is what a trigger list is for.

---

### 2\. Scoping Trigger List (The Deliverable)

Work through this once. Answer in writing—even one-word answers count. The goal is to expose ambiguity, not produce a polished brief.

#### A. What Kind of Test, Actually?

These are _different projects_ with different tools, durations, and risk profiles. Pick one:

- Load—find max sustainable throughput
- Soak/Endurance—behaviour over hours/days (memory leaks, cert expiry, log rotation)
- Spike—sudden surge handling (HPA reaction time)
- Chaos—failure injection (node loss, network partition, Vault outage)
- Capacity planning—predictive model: "X patients/hour needs Y nodes"
- Scalability—does it scale linearly, or does coordination overhead dominate?
- Performance regression—detect degradations between releases

#### B. What is the System Under Test?

You have at least three candidates hiding inside "the clusters":

- B1. `omop-cli` itself—Spot VM orchestration + DuckDB merge pipeline
- B2. An AKS cluster _running_ an OMOP workload (ingestion/query path)
- B3. The cross-cluster data path (EOE → Azure FW DNAT → MKUH)

Plus the sidecars that always break first in your environment: Vault/VSO secret delivery, ArgoCD reconciliation, cert-manager DNS-01.

#### C. Workload Profile

- Read-heavy, write-heavy, or mixed?
- What is "OMOP data" doing here—ingest, transform, query, export?
- Synthetic (from `omop-cli`) or replayed real traffic?
- Steady arrival rate or bursty/diurnal?

#### D. Success Criteria—Discovery Vs Validation

Two opposite postures, can't do both at once:

- Discovery: "Find the unknown breaking point" → open-ended, you stop when something breaks
- Validation: "Prove it can handle 10× peak" → fixed target, you stop when SLO is met

#### E. Blast Radius & Safety

- Dedicated test cluster, or shared infra?
- Customer-facing impact possible? (MKUH is healthcare—this matters)
- Compute budget ceiling (£)?
- Real PHI risk, or synthetic-only?
- Kill criteria: what single observation aborts the test immediately?

#### F. Deliverable Shape

What artefact lets you tick this off and walk away?

- One-off report (markdown + Grafana screenshots)?
- Tuned config committed to GitOps repo (HPA/VPA/PDB/requests/limits)?
- SLO document?
- Runbook for capacity planning?
- Recurring CI job (kube-burner in a pipeline)?

#### G. Time, Budget, People

- "Summer"—calendar window vs. focus hours?
- Sole operator, or stakeholders to consult?
- Compute £ ceiling?

#### H. Definition of Done

> Complete this sentence: "I will know this project is finished when \_\_\_ exists / is committed / is signed off by \_\_\_."

If you can't complete it, you don't have a project yet—you have a theme.

---

### 3\. Critique of the LLM Response (stress\_tests.md)

It's a competent generic template, not a useful plan for _your_ environment. Specific gaps:

1. Generic, not contextualised. It never names `omop-cli`, `mkuh-prd-4`, ArgoCD, Vault/VSO, Azure Firewall, cert-manager—the systems where you've been bleeding for months. A genuine plan should leverage that pain.
2. Conflates 3+ projects into one. Stress-testing the _generation pipeline_ (`omop-cli`), an _AKS workload_ (ingestion under load), and a _cross-cluster network path_ are three distinct projects. The plan forces you to natural-plan all of them simultaneously, which is impossible.
3. No baseline phase. You cannot "stress" a system whose steady-state you haven't characterised. The first sub-project of any stress test is "establish baseline RED/USE metrics." The plan omits this.
4. No kill criteria. A stress test plan without explicit abort conditions is reckless—especially against a healthcare customer environment.
5. Risk section is bland. Missing your actual risks: ArgoCD auto-sync racing imperative test changes (a recurring pattern for you), Vault token TTL under sustained load, Let's Encrypt rate limits, cross-tenant blast radius, NHS regulatory exposure.
6. Brainstorming under-seeds. No concrete tools mentioned: `k6`, `kube-burner`, `Chaos Mesh` / `Litmus`, `Vegeta`, KEDA load tests, `clusterloader2`. No methodologies: USE (Brendan Gregg), RED (Tom Wilkie), SLO-driven testing.
7. "Next Action" is wrong for your role. It says _"Draft an email to the DevOps lead"_—you are the Principal Platform Engineer. You don't escalate to yourself.
8. No observability prerequisite check. You can't stress-test what you can't measure. Are SLIs defined? Are the right Prometheus series being scraped? Is there a dashboard ready _before_ load is applied?
9. No test-data lifecycle. Generation, loading, teardown, retention. You literally have a tool for this (`omop-cli`)—the plan should make it the first-class load generator.

---

### 4\. Over-Advice (Things You Didn't Ask About)

#### 4.1 The ADHD-specific Failure Mode here

Natural Planning can become procrastination by sophistication—you produce a beautiful plan and never run a test. Counter-measure: time-box planning to 90 minutes total. Output is a one-page brief, not a treatise. If you exceed 90 minutes, the project is still too fuzzy—go back to scoping.

#### 4.2 Use Omop-cli as the Load Generator

You don't need `k6` for the data plane. You're building a tool that produces 10M synthetic OMOP patients on Spot VMs. That tool IS the load generator. Frame the stress test as: "use `omop-cli` to drive `mkuh-prd-4` to breaking, observe what fails first." This collapses two projects into one and feeds dogfooding into both.

#### 4.3 USE and RED as Structuring Lenses

- USE (Utilisation, Saturation, Errors)—for every resource (CPU, memory, disk, network, IOPS)
- RED (Rate, Errors, Duration)—for every request-driven service

If your Grafana dashboards don't already give you USE+RED views per node and per service, build _those_ before applying load. That's a self-contained, completable sub-project.

#### 4.4 Search for prior Art before Planning

Before brainstorming, spend 30 minutes searching the Fitfile wiki / GitLab / Slack archives for:

- Previous load tests
- Post-incident reports (real-world stress tests already happened—read them)
- Capacity documents Cheap, high-yield, novelty-rewarding.

#### 4.5 Decompose Now, Sequence Later

I'd suggest the captured aspiration splits into three projects, run in this order:

1. P1: Observability readiness for OMOP workloads on AKS _(prerequisite, 1–2 weeks)_
2. P2: Capacity model for OMOP ingestion on a single AKS cluster _(main stress test, 3–4 weeks)_
3. P3: Resilience profile of the cross-cluster path under load _(follow-up, 2–3 weeks)_

Natural-plan only P1 first. The other two will sharpen once P1 is done.

#### 4.6 Write a Hypothesis, not just a Target

Every stress test scenario should be a falsifiable statement:

> _"We hypothesise that at 5,000 patients/sec ingestion sustained for 1 hour, the bottleneck will be DuckDB merge throughput rather than Vault token refresh or ArgoCD reconciliation latency."_

This forces precision and makes the test outcome interesting regardless of result.

#### 4.7 The "boring" Pre-flight Checklist

Before any actual load:

- ArgoCD auto-sync disabled on target apps (you've been bitten by this)
- Vault token TTLs documented for the test duration
- cert-manager `extraArgs` for DNS-01 persisted in GitOps (your outstanding item)
- Grafana dashboard URL pinned in the project brief
- Kill switch documented (one command to stop generation)
- Cost alert configured on the test subscription

---

### 5\. Your Next Physical Action

Open your notes app. Create one file: `stress-test/scoping-v0.md`.

In that file, answer only three questions—one or two sentences each, no more:

1. Which sub-project am I starting with—P1 (observability), P2 (single-cluster capacity), or P3 (cross-cluster resilience)?
2. What single breaking point would be most valuable to discover?
3. What one observation would make me abort the test immediately?

That's it. Don't write the trigger list answers yet. Don't natural-plan yet. Just those three questions. Target: 15 minutes.

Once `scoping-v0.md` exists with three answers, you have a project. Then—and only then—run the trigger list (§2) against the chosen sub-project, and _only then_ start Phase 1 of Natural Planning.

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

Based on the insights from your stress testing planning session (May 14, 2026) and related infrastructure discussions with Oliver and Robin, here is a draft for your Confluence design document.

I have integrated the specific hardware disparities, the vVPN vs. Leased Line networking trade-offs, and the specialized MKUH/Postgres risks identified in your recent communications.

## Stress Testing Strategy: FFNode & OMOP Federated SDE

### 1. Objectives & Proving Grounds

The primary goal is to align the team on the FFNode / OMOP Stress Test execution plan (Project ID: `FTFL-476`). We are validating whether the system can withstand realistic NHS-scale query loads while maintaining "Functional Persistence."

- Axis A: Infrastructure Scale—Proving single-node capacity vs. 5-node federated limits.
- Axis B: Observability Gap—Finalizing the Grafana monitoring dashboards (`FTFL-638`) to ensure visibility during peak loads.
- Axis C: Federated Query Integrity—Testing "Federated SDE" queries across internet boundaries (AWS/Azure).

### 2. Hardware & Environment Configuration

The test environment must account for significant technical variance that mirrors our current provider reality.

| Variable | Current Prod Setup (+2) | Stress Test Requirement |
|:--- |:--- |:--- |
| Node Count | 3 Mixed Nodes | 5 Nodes (Parquet datasets ready) |
| Disk/IOPS | Standard SSD | High-IOPS NVMe vs. Standard Disk Disk Mapping |
| Database | Postgres / MS SQL | Mixed pooling (Postgres on System Pool) |

Key Questions for Design:

- Massively Oversized Pool: We will first test query/join problems on a single Node with an oversized workflow pool to isolate logic errors from networking latency.
- Graceful vs. Silent Failure: We must document behavior when a query hits a resource-starved server. Does it return a partial result or time out?

### 3. Networking & Cross-Cloud Architecture

- Connectivity Strategy: We have decided on a vVPN / IPSC VPN connection rather than a physical Leased Line (which was deemed too expensive for current project scope).
- Latency Considerations: Testing must include "across internet" traffic simulations between AWS and Azure regions to baseline end-to-end latency.
- Grafana Sync Barrier: Note that the testing cluster currently has a sync issue due to Grafana Alloy monitoring changes—this must be resolved before Axis B testing begins.

### 4. Data Lineage & Query Design

- ETL Integrity: We are running on ETL'd Nodes (e.g., MKUH). A known risk exists with table name mismatches (e.g., `DEMOG` vs. `DEMOGS`) which was recently addressed in Generic ETL Container v1.2.0.
- Query Set: We will establish a "Smoke verification query set" including person counts and vocabulary consistency.
- Observability: Slow query logging must be enabled in both Postgres and MS SQL to identify "cliffs" in performance as cohort sizes scale.

### 5. Risk Assessment & Progressive Enhancement

- Risk Factor: High risk exists when running on shared system pools (MKUH/Postgres). This may lead to unpredictable resource contention during stress tests.
- Staged Rollout: We will adopt a progressive enhancement approach:
    1. Local Parquet performance.
    2. Single-node DB ingestion (`FTFL-479`).
    3. Multi-node federation (2 -> 3 -> 5 nodes).

Related Memory Context:

- Jira Tickets: `FTFL-475` (Synthetic OMOP), `FTFL-476` (Infra/Monitoring), `FTFL-652` (OMOP flows).
- Meeting ID: `pieces_copilot_message_export_may_13_2026_3_01pm`
- Infrastructure Lead: Oliver Rushton / Robin Mofakham (Networking)

All four search streams have now reached `recommendation: "sufficient"`. Here is the complete agenda and outcomes summary for your 4pm meeting.

---

## Stress Testing Goals—Meeting Brief (Today, 4:00 PM BST)

### Context Snapshot

Your memory holds an exceptionally detailed picture of this project. The FFNode Stress Testing Meeting note you wrote on 7 May captures the explicit meeting purpose verbatim:

> "Align the team on the FFNode / OMOP Stress Test execution plan. Output: a concrete test plan with phase assignments and a set of Jira tickets to drive the work."

Five Parquet datasets (one per node) are ready. Six weeks of architectural planning has been captured since early April. The core Jira tickets already exist: `FTFL-475`, `FTFL-476`, `FTFL-479`, `FTFL-480`, `FTFL-488`, and the newly spotted `FTFL-635` (Stress Testing in the Application). A new provisioning ticket `FTFL-652` (OMOP Database Provisioning for Stress Testing) appeared in the backlog on 8 May.

Previous meeting participants included Helena Ahlfors, Oliver Rushton, Robin Mofakham, Philip Russmeyer, Magali Ruffier, Jamie Reeve, Alexis McKenna (`alexis.mckenna1@nhs.net`), Sean Donnelly (`sean.donnelly@telefonicatech.uk`), Julia Kurps (`julia@thehyve.nl`), Weronika Jastrzebska, and Helen Duckworth (`helen.duckworth@nhs.net`).

---

### Proposed Agenda

1. Where we are—5 min

- 5 Parquet node datasets ready; synthetic data pipeline (`FTFL-475`, `FTFL-488`) complete.
- Infra provisioning (`FTFL-476`) current status: Grafana monitoring dashboard outstanding; MS SQL deployment done.
- `FTFL-480` (userflow permutation script) done per Sprint 13 board.

1. What we want to prove—the three test dimensions—15 min

Ground agreement on the three stress test axes from your execution plan:

| Axis                                                                                                 | What we're proving                                                                 | Success criteria                                                                                                |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| A. Single-node capacity                                                                              | p50/p95/p99 query latency; DB CPU/mem/IO; error rate                               | No errors; latency increases predictably (no "cliff") up to full node dataset                                   |
| B. Multi-node federation                                                                             | p95 end-to-end latency; cross-node bytes; timeouts (up to 5 nodes)                 | Federation across 2→3→5 nodes completes without timeout; identify max sustainable concurrency before SLA breach |
| C. Algorithmic / userflow permutations ([`FTFL-480`](https://fitfile.atlassian.net/browse/FTFL-480)) | Cohort size × table scope × extract size × privacy treatment × OMOP sources linked | No failures across permutation matrix; identify breaking thresholds                                             |

1. Userflow permutation variables—10 min

The script ([`FTFL-480`](https://fitfile.atlassian.net/browse/FTFL-480)) is built to vary:

- Cohort size
- Number of tables / fields selected
- Extract size (controlled via `LIMIT`)
- Privacy treatment (true / false)
- Number of OMOP data sources to link

Agree the recommended level sets: `{1k, 10k, 100k, 1M, NodeFull, 5NodeFull}`—estimated 216 total test cases across the matrix.

1. Infrastructure & monitoring requirements—10 min

- [`FTFL-476`](https://fitfile.atlassian.net/browse/FTFL-476): "Monitor resource consumption whilst running OMOP workflows" and "improve the generic workflows monitoring dashboard."
- [`FTFL-652`](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?selectedIssue=FTFL-652): New—OMOP database provisioning for stress testing; need to assign and sprint-slot.
- Grafana dashboard coverage: CPU, memory, IO, p95 latency per node, timeout rate.

1. Data quality pre-flight gates—5 min

From your Stress Test Execution Plan note (11 May), agree on the pre-flight checklist before any load runs:

- OMOP CDM v5.4 schema & integrity checks (PK/FK, Concept ID sanity).
- Achilles distribution sanity (row counts, top concepts, visit distribution).
- WhiteRabbit profiling.
- "Don't test garbage" gate—no load until each node's dataset passes.

1. ETL / Hyve pipeline scalability open questions—5 min

Captured from the Hyve design doc (Apr 16):

- What is the output format (ideally Postgres)?
- How long does OMOP ETL take—daily / weekly / hourly updates?

1. Jira ticket assignments and sprint slot—10 min

Walk the outstanding tickets and assign owners + target sprint.

---

### Desired Outcomes from the Meeting

By the end of the session you should have walked out with:

- A signed-off, phased test plan—Phase 1 (data quality gates), Phase 2 (single-node capacity), Phase 3 (multi-node federation), with measurable success criteria for each.
- Agreed permutation level sets for the userflow script (`FTFL-480`)—cohort sizes, scope tiers, privacy on/off.
- Monitoring confirmed—Grafana dashboard scope locked down (`FTFL-476` / `FTFL-478`); who owns it.
- `FTFL-652` (OMOP DB provisioning) assigned and sprint-slotted.
- Hyve pipeline questions answered (or escalated to Stefan / The Hyve)—output format and ETL cadence.
- A set of Jira tickets created or updated to drive the work, with owners.

---

### Key Open Questions to Bring in

From your Miro board (Mar 10) and your notes, the questions that have been live since the beginning:

- What is the maximum number of OMOP data sources the system works for without degradation?
- What is the maximum cohort size before the "cliff" (hard failure / timeout)?
- Is the warning mechanism for "too big" queries scoped into this test or a follow-on?
- Helena raised on 5 May: "Can we get the project plan details off of Wesam? We don't usually have clear use cases!"—is use-case clarity still needed before testing begins?

Based on the Miro board text provided in the CSV, here is a categorised breakdown of the statements, questions, and claims regarding the OMOP data generation project.

## Questions and Deliberations

- Do we need realistic data?
- Should realistic scenarios be required for stress testing?
- Should there also be separate databases for more realistic performance?
- Is creating one large dataset a good idea, or would multiple smaller sets be better and more agile?
- Will the synthetic data be separated by Nodes?
- Can we test the new Data Access Requests (DARs) from clients (cohort filtering, selection, and linkage) considering the expected data volume and sites by year-end?

## Claims and Strategic Rationale

- Synthetic data moves the project from theory to practicality and helps identify edge cases.
- Having synthetic data allows staff to understand the datasets more deeply.
- The base data enables the creation of and work with various other data formats.
- Infrastructure Scalability: Processing approximately 30 TiB of data identifies hardware bottlenecks before migrating real patient data.
- Linkage Validation: The project allows for measuring the accuracy and error rates of `Person_ID` and `Token_Person_ID` algorithms without privacy risks.
- Privacy-First Development: This serves as a "Gold Standard" testbed for developers to build and debug on realistic patterns without requiring high-level clearances.
- Methodological Transparency: Reproducible Analytical Pipeline (RAP) principles ensure explainable, auditable linkage and standardisation methods to maintain public trust.
- Clinical Mirroring: UK-adapted logic reflects the actual NHS primary care journey.

## Technical and Operational Statements

- Data Standards: The pipeline uses SNOMED CT for diagnoses, dm+d codes for prescriptions, and LOINC for lab results.
- Linkage Logic: `Person_ID` acts as the persistent master key across HES, Mental Health, and Maternity datasets.
- Identity Resolution: Identity is resolved through a three-stage process: Cross-check, Alphanumeric (Soundex), and Algorithmic (demographic scoring).
- Orchestration: The pipeline uses Kedro to create an automated, version-controlled Directed Acyclic Graph (DAG).
- Statistical Integrity: Every worker uses a cryptographically distinct seed offset by 1,000,003 to ensure statistical independence.
- US Logic Removal: US-specific insurance billing, payers, and cardiovascular calculators have been stripped from the engine.
- QA and Testing: * The `omock` R package is used for rapid unit testing before the 30 TiB production run.
    - Synthetic data acts as the QA layer for "High Volume" query warnings.
    - Siloed test nodes validate the UI's ability to select multiple data providers.
- Ownership: The Hyve should own the part related to Methodological Transparency.

Execute a scale test with synthetic data generating a project cohort from five or more data providers, where at least two have OMOP measurement tables with 500 million rows or more

Successfully deliver the synthetic dataset to an SDE project area.Document all blockers, bottlenecks, and cost inefficiencies impacting query execution and data delivery at this scale.Provide a clear report with quantified metrics (e.g., query execution time, resource utilisation, estimated cost per query).

31 July 2026

 AS05 Implement targeted improvements to the data provider network infrastructure to ensure large-scale, complex queries can be executed within acceptable timeframes and cost parameters. |

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
