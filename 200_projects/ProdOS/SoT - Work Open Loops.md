---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-28T23:00:00+01:00
modified: 2026-05-28T23:00:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-511: Nginx HTTPS hardening — actively In Progress, push to completion"
  - "FTFL-476: OMOP Stress Testing infra — Blocked 12+ days, escalate or deprioritise"
  - "FTFL-658: [SPIKE] Investigate MKUH Failing Terraform Runs — timebox and assess"
---

## Work Open Loops — Source of Truth

> **FTFL-638** missing from open query — likely resolved/closed after active work today (branch `feature/FTFL-638-add-labels-for-logs` was active, last updated 2026-05-28 08:57). Verify and move to Resolved table next run.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🔴 critical | In Progress | 2026-05-28 | Push to completion — was Selected for Development, now actively In Progress |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Identify blocker, escalate or deprioritise (12+ days blocked) |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Timebox spike, assess scope |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-26 15:12 | Triage — assess exposure severity, batch with FTFL-511 |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Notes

- **Jira data fresh**: Successful fetch via `jira-fetch.js` at 2026-05-28 23:00 UTC. 7 open issues returned (down from 8).
- **FTFL-638 disappeared**: Was in the prior SoT with active branch and updated 2026-05-28 08:57, now absent from open query. Likely resolved/closed — verify next run before moving to Resolved table.
- **FTFL-511 status change**: Moved from "Selected for Development" → "In Progress" since last run. Now the actively worked item.
- **FTFL-476** blocked since 2026-05-18 (12+ days). No movement. Needs escalation or explicit deprioritisation.
- **0 stale issues**: All In Progress issues updated within 3 days.
- **New issues this run**: 0.
- **Disappeared issues**: FTFL-638 (see note above — not yet confirmed resolved).

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
