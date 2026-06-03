---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-03T13:00:00+01:00
modified: 2026-06-03T13:00:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Blocked 22+ days — escalate or deprioritise OMOP Stress Testing infra"
  - "FTFL-673: Upgrade Grafana Alloy In Progress — drive to completion"
  - "FTFL-525: Ensure all backups are ZRS (High priority) — start work"
---

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Identify blocker, escalate or deprioritise (22+ days blocked) |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🟠 high | Selected for Development | 2026-06-03 | Start work — high-priority issue |
| FTFL-673 | Jira | Upgrade Grafana Alloy | 🟠 high | In Progress | 2026-06-03 | Drive to completion |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-29 | Drive to review — security issue |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 | Timebox spike, drive to completion |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Notes

- **0 stale issues**: No In Progress issues untouched for >3 days. 1Password pipeline active — fresh data confirmed this run.
- **FTFL-476** blocked since 2026-05-18 (22+ days). No movement. Needs escalation or explicit deprioritisation.
- **FTFL-512** priority downgraded Low (was Medium) — still a security issue, plan into sprint.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist MCP**: Read-only (no create-task tool available). Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-511 | [API-5] Nginx allows outdated HTTPS connection methods | ~2026-06-01 |
| FTFL-680 | [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs | 2026-05-29 |
| FTFL-638 | Add labels for logs | 2026-05-28 |
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |
