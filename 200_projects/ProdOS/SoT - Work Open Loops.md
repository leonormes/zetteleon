---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-28T16:00:00+01:00
modified: 2026-05-28T16:00:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-638: Grafana Monitoring in testing cluster — push forward, branch active"
  - "FTFL-476: OMOP Stress Testing infra — Blocked 10+ days, escalate or deprioritise"
  - "FTFL-658: [SPIKE] Investigate MKUH Failing Terraform Runs — timebox and assess"
---

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-638 | Jira | Missing Grafana Monitoring in testing cluster | 🔴 critical | In Progress | 2026-05-28 08:57 | Push forward — branch `feature/FTFL-638-add-labels-for-logs` active |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Identify blocker, escalate or deprioritise (10+ days blocked) |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Timebox spike, assess scope |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-26 15:12 | Triage — assess exposure severity, batch with FTFL-511 |
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🟡 medium | Selected for Development | 2026-05-26 15:12 | Triage — assess TLS version risk, batch with FTFL-512 |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Notes

- **Jira data fresh**: Successful fetch via `jira-fetch.js` at 2026-05-28 16:00 UTC. All 8 open issues confirmed.
- **FTFL-638** updated 2026-05-28 08:57. Active work in progress — branch `feature/FTFL-638-add-labels-for-logs` exists.
- **FTFL-476** blocked since 2026-05-18 (10+ days). No movement. Needs escalation or explicit deprioritisation.
- **FTFL-658 & FTFL-609** in Selected for Development since 2026-05-27.
- **FTFL-511 & FTFL-512**: Nginx security issues, both Selected for Development. Quick-win candidates.
- **FTFL-602**: The Hyve alerting, Selected for Development since 2026-05-26.
- **0 stale issues**: All issues updated within 3 days.
- No new issues since last run (2026-05-28 09:02).
- No disappeared issues — all prior SoT tickets still present in Jira open query.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist**: No Todoist CLI/tool available in cron context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |
