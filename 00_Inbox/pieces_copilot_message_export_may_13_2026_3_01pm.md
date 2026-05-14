---
created: 2026-05-13T14:01:14+00:00
modified: 2026-05-13T15:35:28+00:00
title: pieces_copilot_message_export_may_13_2026_3_01pm
---

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

2. What we want to prove—the three test dimensions—15 min

Ground agreement on the three stress test axes from your execution plan:

| Axis                                                                                                 | What we're proving                                                                 | Success criteria                                                                                                |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| A. Single-node capacity                                                                              | p50/p95/p99 query latency; DB CPU/mem/IO; error rate                               | No errors; latency increases predictably (no "cliff") up to full node dataset                                   |
| B. Multi-node federation                                                                             | p95 end-to-end latency; cross-node bytes; timeouts (up to 5 nodes)                 | Federation across 2→3→5 nodes completes without timeout; identify max sustainable concurrency before SLA breach |
| C. Algorithmic / userflow permutations ([`FTFL-480`](https://fitfile.atlassian.net/browse/FTFL-480)) | Cohort size × table scope × extract size × privacy treatment × OMOP sources linked | No failures across permutation matrix; identify breaking thresholds                                             |

3. Userflow permutation variables—10 min

The script ([`FTFL-480`](https://fitfile.atlassian.net/browse/FTFL-480)) is built to vary:

- Cohort size
- Number of tables / fields selected
- Extract size (controlled via `LIMIT`)
- Privacy treatment (true / false)
- Number of OMOP data sources to link

Agree the recommended level sets: `{1k, 10k, 100k, 1M, NodeFull, 5NodeFull}`—estimated 216 total test cases across the matrix.

4. Infrastructure & monitoring requirements—10 min

- [`FTFL-476`](https://fitfile.atlassian.net/browse/FTFL-476): "Monitor resource consumption whilst running OMOP workflows" and "improve the generic workflows monitoring dashboard."
- [`FTFL-652`](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?selectedIssue=FTFL-652): New—OMOP database provisioning for stress testing; need to assign and sprint-slot.
- Grafana dashboard coverage: CPU, memory, IO, p95 latency per node, timeout rate.

5. Data quality pre-flight gates—5 min

From your Stress Test Execution Plan note (11 May), agree on the pre-flight checklist before any load runs:

- OMOP CDM v5.4 schema & integrity checks (PK/FK, Concept ID sanity).
- Achilles distribution sanity (row counts, top concepts, visit distribution).
- WhiteRabbit profiling.
- "Don't test garbage" gate—no load until each node's dataset passes.

6. ETL / Hyve pipeline scalability open questions—5 min

Captured from the Hyve design doc (Apr 16):

- What is the output format (ideally Postgres)?
- How long does OMOP ETL take—daily / weekly / hourly updates?

7. Jira ticket assignments and sprint slot—10 min

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
