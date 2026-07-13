---
created: 2026-06-12T08:01:45+00:00
modified: 2026-07-13T08:44:36+00:00
permalink: llmeon/30-library/200-projects/complete-jira-work-item-text-structure
project_name: Refined Deployment
title: Complete Jira Work Item Text Structure
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Friday Jun 12, 2026 - 9:01 AM_
---

## Complete Jira Work Item Text Structure (Phase 0–2)

Ready to copy into Jira. Don't forget to replace placeholders with actual assignees/sprint dates.

---

## EPIC: FTFL-500—FFNode Stress Testing Programme (Phase 0–2: Asset Registration, Pre-flight QA, Single-Node Baseline)

Type: Epic

Project: FTFL

Summary: FFNode Stress Testing—Phase 0–2 Foundation, QA Gates, and Single-Node Baseline Execution

Description:

Comprehensive stress testing programme to measure system performance and establish known working limits up to the AS05 contractual requirement (31 July 2026). This epic covers three sequential phases:

- Phase 0 (0.5d): Asset registration and dataset manifest validation
- Phase 1 (1–2d): Pre-flight quality gates (Achilles + schema/FK integrity)
- Phase 2 (1–2d): Single-node baseline capacity characterization

Acceptance Criteria (Epic):

- All Phase 0 assets registered and validated
- All Phase 1 pre-flight gates passed (no schema/FK blockers)
- Phase 2 baseline executed on at least one node with p50/p95/p99 latency and resource metrics captured
- Monitoring stack (Grafana/Prometheus/Alloy) live throughout all phases
- Kill criteria evaluated; Phase 3 readiness decision logged

Parent Epic: FTFL-476 (OMOP stress-testing infra + monitoring)

Linked Epics: FTFL-480 (userflow permutation script)

Hard Deadline: 31 July 2026 (AS05 milestone)

Priority: High

Effort Estimate (Epic): 4–6 days total

---

## STORY: FTFL-501—Register and Manifest Stress Test Assets (Phase 0)

Type: Story

Parent Epic: FTFL-500

Summary: Phase 0—Register Assets and Confirm Dataset Manifest

Description:

Assemble dataset inventory, confirm dataset quality, and validate overlap engineering prerequisites before pre-flight QA gates. Produce the authoritative dataset manifest that all subsequent phases reference.

Acceptance Criteria:

- [ ] Dataset manifest created and documented (version, vocabulary version, row counts per node, SHA-256 checksums, node-ID mapping)
- [ ] Overlap engineering analysis (OQ-8) completed and sign-off documented
- [ ] 500M-row MEASUREMENT table gate verified on at least 2 nodes
- [ ] No missing datasets; all 5 nodes confirmed present in test environment
- [ ] Manifest reviewed and approved by SDE lead (Weronika)

Subtasks:

1. FTFL-501.1—Gather and Validate Dataset Metadata
   Generate row counts, version identifiers, and vocabulary version for all 5 nodes. Verify no dataset corruption (row counts vs. expected range).

2. FTFL-501.2—Compute SHA-256 Checksums and Cross-Validate Node Overlap
   Calculate checksums for each Parquet file per node; document overlap (% shared PERSON/CONDITION records across nodes).

3. FTFL-501.3—Verify 500M-Row MEASUREMENT Gate
   Confirm at least 2 nodes have MEASUREMENT tables with ≥500M rows (AS05 requirement). Document row count summary per node.

Effort: 0.5 days

Story Points: 3

Assignee: [DevOps/Infra Lead]

Sprint: [Next Sprint]

Labels: phase-0, stress-testing, asset-registration

Depends on: Dataset pipeline (FTFL-485, if exists)

Blocks: FTFL-502 (Pre-flight QA)

---

## STORY: FTFL-502—Pre-flight Quality Gates and Schema Validation (Phase 1)

Type: Story

Parent Epic: FTFL-500

Summary: Phase 1—Pre-flight QA Gates (Achilles + Schema/FK Integrity)

Description:

Execute data quality profiling and schema validation on all nodes before baseline testing. Any failing node blocks Phase 2 progression and triggers root-cause investigation.

Acceptance Criteria:

- [ ] Achilles summary checks executed on all 5 nodes; results documented (no critical data quality issues)
- [ ] Schema integrity validated per node (all expected OMOP v5.4 tables present, correct column types)
- [ ] Foreign key integrity verified (PERSON → DEATH, VISIT_OCCURRENCE → PERSON, CONDITION_OCCURRENCE → PERSON, DRUG_EXPOSURE → PERSON, MEASUREMENT → PERSON)
- [ ] No blocking FK violations; any deviations documented and triaged
- [ ] Kill criteria evaluated (no production node errors, cost burn within budget ceiling, vault/cert-manager healthy)
- [ ] Go/no-go decision logged; if fail, Phase 2 blocked and escalation triggered

Subtasks:

1. FTFL-502.1—Deploy and Execute Achilles on All Nodes
   Install Achilles on each of the 5 nodes sequentially. Capture full characterization reports (data density, completeness, uniqueness checks).

2. FTFL-502.2—Validate Schema Integrity and PK/FK Constraints
   Confirm all OMOP CDM v5.4 required tables exist per node. Verify primary key uniqueness and foreign key referential integrity.

3. FTFL-502.3—Triage and Document Schema Deviations
   Log any schema mismatches (missing columns, type mismatches, FK violations). Assign severity and owner for remediation.

4. FTFL-502.4—Verify Monitoring Stack Readiness
   Confirm Grafana dashboards active, Prometheus scrape targets healthy, Alloy pipeline end-to-end operational before Phase 2 baseline.

5. FTFL-502.5—Evaluate Kill Criteria
   Check production node error rates at baseline, cost burn within documented ceiling, vault/cert-manager health. Document blockers; escalate if any critical.

Effort: 1–2 days

Story Points: 5

Assignee: [QA/Data Lead]

Sprint: [Next Sprint]

Labels: phase-1, stress-testing, pre-flight-qa, data-quality

Depends on: FTFL-501 (Asset Registration)

Blocks: FTFL-503 (Single-Node Baseline)

---

## STORY: FTFL-503—Single-Node Baseline Capacity Characterization (Phase 2)

Type: Story

Parent Epic: FTFL-500

Summary: Phase 2—Single-Node Baseline (Latency and Resource Metrics)

Description:

Execute a constrained permutation wave on a single node to establish baseline latency (p50/p95/p99) and resource utilization (CPU, memory, disk I/O) under normal federation load. Calibrate monitoring and validate harness restartability.

Acceptance Criteria:

- [ ] Baseline test executed on Node 1 (or designated single-node) with parameters: Cohort size C = {1k, 10k, 100k, Full}, Scope S ∈ {S1, S2}, Export X=Off, Privacy P=Off, Federation L=L1
- [ ] Latency metrics captured (p50, p95, p99 query response times in seconds)
- [ ] Resource metrics captured (DB CPU %, memory %, disk I/O operations/sec, network throughput)
- [ ] Test harness suspend/resume validated (confirm restartability across wave boundaries)
- [ ] Monitoring dashboard snapshot captured and baseline comparison documented
- [ ] Any resource bottlenecks identified (CPU saturation, memory pressure, disk I/O ceiling)
- [ ] Phase 3 readiness decision logged

Subtasks:

1. FTFL-503.1—Provision and Configure Single-Node Test Environment
   Deploy test harness, load FTFL-480 permutation script, configure test database on Node 1. Validate network connectivity and baseline latency with synthetic query.

2. FTFL-503.2—Execute Baseline Permutation Subset (C, S Variables)
   Run structured permutation: cohort sizes {1k, 10k, 100k, NodeFull} × scopes {S1, S2}. Each combination executed sequentially; pause between waves to capture metrics.

3. FTFL-503.3—Capture and Plot Latency and Resource Metrics
   Record p50/p95/p99 latency per query type. Plot CPU, memory, disk I/O, network utilization during each wave. Identify inflection points and resource saturation thresholds.

4. FTFL-503.4—Validate Test Harness Restartability
   Suspend test harness mid-wave; resume after 5 minutes. Confirm no data corruption, query results consistent, metrics pipeline uninterrupted.

5. FTFL-503.5—Document Baseline Results and Assess Phase 3 Readiness
   Compile baseline report: latency profiles, resource headroom, identified bottlenecks, recommendations for Phase 3 (waves A–D). Decision gate: proceed to multi-node federation or remediate first?

Effort: 1–2 days

Story Points: 8

Assignee: [Performance/Test Lead]

Sprint: [Sprint +1]

Labels: phase-2, stress-testing, baseline, single-node

Depends on: FTFL-502 (Pre-flight QA)

Blocks: FTFL-504 (Phase 3 Permutation Waves—not included in this ticket set, for future sprint)

---

## Summary Table for Copy-Paste

| Level | ID | Title | Effort | Parent | Blocks |
|-------|-----|-------|--------|--------|--------|
| Epic | FTFL-500 | FFNode Stress Testing—Phase 0–2 | 4–6d | FTFL-476 | FTFL-504 |
| Story | FTFL-501 | Phase 0: Register Assets | 0.5d | FTFL-500 | FTFL-502 |
| ├─ Subtask | FTFL-501.1 | Gather Dataset Metadata |—| FTFL-501 |—|
| ├─ Subtask | FTFL-501.2 | Compute Checksums & Overlap |—| FTFL-501 |—|
| └─ Subtask | FTFL-501.3 | Verify 500M-Row Gate |—| FTFL-501 |—|
| Story | FTFL-502 | Phase 1: Pre-flight QA Gates | 1–2d | FTFL-500 | FTFL-503 |
| ├─ Subtask | FTFL-502.1 | Deploy Achilles |—| FTFL-502 |—|
| ├─ Subtask | FTFL-502.2 | Schema/FK Validation |—| FTFL-502 |—|
| ├─ Subtask | FTFL-502.3 | Triage Deviations |—| FTFL-502 |—|
| ├─ Subtask | FTFL-502.4 | Monitoring Stack Readiness |—| FTFL-502 |—|
| └─ Subtask | FTFL-502.5 | Kill Criteria Evaluation |—| FTFL-502 |—|
| Story | FTFL-503 | Phase 2: Single-Node Baseline | 1–2d | FTFL-500 | FTFL-504 |
| ├─ Subtask | FTFL-503.1 | Provision Test Environment |—| FTFL-503 |—|
| ├─ Subtask | FTFL-503.2 | Execute Baseline Permutation |—| FTFL-503 |—|
| ├─ Subtask | FTFL-503.3 | Capture Metrics & Plot |—| FTFL-503 |—|
| ├─ Subtask | FTFL-503.4 | Validate Restartability |—| FTFL-503 |—|
| └─ Subtask | FTFL-503.5 | Phase 3 Readiness Assessment |—| FTFL-503 |—|

---

## Notes for Manual Entry

- Project: FTFL
- Epic Link: All stories link to FTFL-500
- Dependencies: Phase progression: FTFL-501 → FTFL-502 → FTFL-503 (sequential blocks)
- Assignees: Suggest splitting: Infra/DevOps (FTFL-501), QA/Data (FTFL-502), Performance/Test (FTFL-503)
- Sprint: Phase 0–1 (FTFL-501 + FTFL-502) fit in next sprint; Phase 2 (FTFL-503) in sprint +1
- Labels: phase-0, phase-1, phase-2, stress-testing, ffnode, omop
- Hard Deadline: 31 July 2026 (log in Epic due date)

Copy the above text into Jira. You have all hierarchy levels (Epic → Stories → Subtasks) with acceptance criteria and effort estimates.
