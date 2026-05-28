---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-28T16:34:22+00:00
modified: 2026-05-28T16:34:22+00:00
title: SoT - Work Open Loops
top3:
  - "FTFL-511: Nginx HTTPS hardening — actively In Progress, push to completion"
  - "FTFL-476: OMOP Stress Testing infra — Blocked 12+ days, escalate or deprioritise"
  - "FTFL-658: [SPIKE] Investigate MKUH Failing Terraform Runs — timebox and assess"
---

## Work Open Loops — Source of Truth

> ⚠️ **Jira data stale**: 1Password CLI timeout prevented Jira fetch this run. Data carried forward from 2026-05-28 23:00 UTC run. Verify fresh data on next successful run.

> **FTFL-638** missing from open query for second consecutive run — likely resolved/closed after active work on 2026-05-28. Move to Resolved table on next run if still absent.

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

- **Jira data stale**: 1Password CLI timeout at 2026-05-28 16:34 UTC. Last successful fetch was 2026-05-28 23:00 UTC (7 open issues). Data carried forward unchanged.
- **FTFL-638 disappeared**: Missing for second consecutive run. Was in the prior SoT with active branch `feature/FTFL-638-add-labels-for-logs`, last updated 2026-05-28 08:57. Likely resolved/closed — will move to Resolved table next run if still absent.
- **FTFL-511** status change noted in previous run: Moved from "Selected for Development" → "In Progress". Now the actively worked item.
- **FTFL-476** blocked since 2026-05-18 (12+ days). No movement. Needs escalation or explicit deprioritisation.
- **0 stale issues**: All In Progress issues updated within 3 days (at last successful fetch).
- **New issues this run**: 0 (no fresh data).

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Jira**: 1Password CLI timeout — `spawnSync /bin/sh ETIMEDOUT`. Token fetch failed, API query skipped. Data carried forward from last successful run.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist**: No Todoist CLI/tool available in cron context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |
