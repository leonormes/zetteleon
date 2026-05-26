---
created: Invalid date
modified: 2026-05-26T11:43:42+00:00
pieces_ids: ["9a3343df-e428-4381-9a3e-587c7129d980"]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-14-pieces-grafana
---

## Grafana Session—2026-05-14

### Asset 1 (Pieces: 9a3343df-e428-4381-9a3e-587c7129d980)

Captured: 2026-05-13T14:01:07.417202Z

```
All four search streams have now reached `recommendation: "sufficient"`. Here is the complete agenda and outcomes summary for your 4pm meeting.

---

## Stress Testing Goals — Meeting Brief (Today, 4:00 PM BST)

### Context snapshot

Your memory holds an exceptionally detailed picture of this project. The FFNode Stress Testing Meeting note you wrote on 7 May captures the explicit meeting purpose verbatim:

> "Align the team on the FFNode / OMOP Stress Test execution plan. Output: a concrete test plan with phase assignments and a set of Jira tickets to drive the work."

Five Parquet datasets (one per node) are ready. Six weeks of architectural planning has been captured since early April. The core Jira tickets already exist: `FTFL-475`, `FTFL-476`, `FTFL-479`, `FTFL-480`, `FTFL-488`, and the newly spotted `FTFL-635` (Stress Testing in the Application). A new provisioning ticket `FTFL-652` (OMOP Database Provisioning for Stress Testing) appeared in the backlog on 8 May.

Previous meeting participants included Helena Ahlfors, Oliver Rushton, Robin Mofakham, Philip Russmeyer, Magali Ruffier, Jamie Reeve, Alexis McKenna (`alexis.mckenna1@nhs.net`), Sean Donnelly (`sean.donnelly@telefonicatech.uk`), Julia Kurps (`julia@thehyve.nl`), Weronika Jastrzebska, and Helen Duckworth (`helen.duckworth@nhs.net`).

---

### Proposed agenda

1. Where we are — 5 min
- 5 Parquet node datasets ready; synthetic data pipeline (`FTFL-475`, `FTFL-488`) complete.
- Infra provisioning (`FTFL-476`) current status: Grafana monitoring dashboard outstanding; MS SQL deployment done.
- `FTFL-480` (userflow permutation script) done per Sprint 13 board.

2. What we want to prove — the three test dimensions — 15 min

Ground agreement on the three stress test axes from your execution plan:

| Axis | What we're proving | Success criteria |
|---|---|---|
| A. Single-node capacity | p50/p95/p99 query latency; DB CPU/mem/IO; error rate | No errors;  # Truncate for safety
```

---
