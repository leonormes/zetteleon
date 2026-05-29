---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-29T17:00:00+00:00
modified: 2026-05-29T17:00:00+00:00
title: SoT - Work Open Loops
top3:
  - "FTFL-511 + FTFL-512: Both Nginx security bugs Ready for review — review and merge PRs"
  - "FTFL-476: Blocked 13+ days — escalate or deprioritise"
  - "FTFL-658: MKUH Terraform spike now In Progress — timebox and drive to completion"
---

## Work Open Loops — Source of Truth

> ✅ **Jira data fresh** as of 2026-05-29 17:00 UTC. Script returned 7 open issues. 0 stale.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🟡 medium | Ready for review | 2026-05-29 12:02 | Review and merge PR |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Ready for review | 2026-05-29 11:48 | Review and merge PR |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 13:41 | Identify blocker, escalate or deprioritise (13+ days blocked) |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | In Progress ⬆️ | 2026-05-27 10:26 | Timebox spike, drive to completion |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 09:52 | Review when higher-priority items cleared |

### Notes

- **Fresh data this run**: Jira fetch succeeded at 2026-05-29 17:00 UTC.
- **FTFL-658 status change**: Moved from "Selected for Development" → "In Progress" since last run (13:00 UTC). Good — spike is now active.
- **FTFL-511 + FTFL-512**: No status change since last run. Both remain Ready for review — PRs need review/merge.
- **FTFL-680 confirmed resolved**: [AZURE] Verify MANA Compatibility missing from open query for second consecutive run. Moved to Resolved table below.
- **FTFL-476** blocked since 2026-05-18 (13+ days). No movement. Needs escalation or explicit deprioritisation.
- **0 stale issues**: All In Progress/Ready issues updated within 3 days.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist MCP**: Read-only (no create-task tool available). Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-680 | [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs | 2026-05-29 (confirmed) |
| FTFL-638 | Add labels for logs | 2026-05-28 |
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |
