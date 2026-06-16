---
created: 2026-06-09T09:14:56+00:00
last_updated: 2026-06-16T10:05:29+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-694: Kick off Phase 0 asset registration — still highest-priority epic, unaudited"
  - "FTFL-525: Diagnose why ZRS backup conversion is blocked — stalled since 11 Jun"
  - "FTFL-609: Continue EBS CSI Driver policy migration to V2 — actively In Progress"
---

## Work Open Loops — Source of Truth

> ✅ **Fresh data** — Jira API queried via `cos-jira-fetch.py` (static PAT). All data current as of 2026-06-16T10:05.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-694 | Jira | FFNode Stress Testing — full programme (Phase 0–4) | 🔴 critical | Backlog | 2026-06-15 | Kick off Phase 0: register assets, verify ≥500M-row dataset — highest-priority epic |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | 🚫Blocked | 2026-06-11 | Diagnose why blocked — still stalled since 11 Jun |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | In Progress | 2026-06-11 | Continue policy migration to V2 — actively being progressed |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | 🚫Blocked | 2026-06-11 | Determine path forward — still blocked, needs unblocking or re-scoping |
| FTFL-686 | Jira | Optimise Loki log metadata: move high-cardinality labels to structured metadata and inject k8s annotations for richer log context | 🟡 medium | Backlog | 2026-06-09 | Scope the enrichment work — ready to pick up when bandwidth allows |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟢 low | Selected for Development | 2026-06-11 | Scope the fix — low-priority security bug |
| FTFL-657 | Jira | Investigate possibility of using Bastion Direct to Private AKS cluster | 🟢 low | Selected for Development | 2026-06-10 | New spike (1 day timebox) — scope and schedule |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🟢 low | 🚫Blocked | 2026-06-15 | Touched — priority remains Low, blocked |

### Priority Drift

| ID | Check |
|----|-------|
| All 8 issues | No drift detected — Jira API values match existing SoT symbols. |

### Status Changes (since last run 2026-06-16T08:16)

| ID | What Changed |
|----|-------------|
| All 8 issues | No changes detected — all statuses, priorities, and last-activity dates unchanged since previous run. 1h48m gap (08:16→10:05). |

### Top 3 Next Actions

1. **FTFL-694** — Kick off Phase 0: register assets, verify ≥500M-row MEASUREMENT dataset. Highest-priority epic (FFNode Stress Testing) still unaudited since creation.
2. **FTFL-525** — Diagnose why ZRS backup conversion is blocked. Still the highest active-blocker item; unblock to resume progress.
3. **FTFL-609** — Continue EBS CSI Driver policy migration to V2. Actively In Progress — maintain momentum.

### Notes

- **Data pipeline**: Healthy — `cos-jira-fetch.py` via static PAT. No daemon dependency.
- **gk CLI cross-reference**: `gk issue list --all --json` confirmed all 8 IDs match — pipeline consistent.
- **gk pr list --all --json**: Empty — no open GitLab MRs.
- **Pieces LTM**: Unavailable — Pieces OS not running on port 39300 (connection refused). No ambient signals captured.
- **Morning quiet period**: 1h48m gap yielded zero Jira activity. Expected for post-run quiet (08:16→10:05).
- **Staleness**: FTFL-686 (Loki) last updated 2026-06-09 (7 days). FTFL-657 last updated 2026-06-10 (6 days). FTFL-525/609/658/512 last updated 2026-06-11 (5 days). FTFL-694 and FTFL-476 fresh at 2026-06-15.

### Known Data Gaps

- **Pieces LTM**: REST API at `http://localhost:39300/messages` returned connection refused. Pieces OS was not running during this cron window. No ambient signals captured.