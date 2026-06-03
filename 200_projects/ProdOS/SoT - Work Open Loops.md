---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-03T10:29:00+01:00
modified: 2026-06-03T10:29:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Blocked 22+ days — escalate or deprioritise OMOP Stress Testing infra"
  - "FTFL-525: New — ensure all backups are ZRS (High priority)"
  - "FTFL-673: Upgrade Grafana Alloy now In Progress — drive to completion"
---

## Work Open Loops — Source of Truth

> ⚠️ **Jira data stale** — 1Password CLI session locked at 10:29 BST. Open/stale issue state carried forward from 08:54 run. Run `op signin` in a terminal to restore Jira data pipeline.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 13:41 | Identify blocker, escalate or deprioritise (22+ days blocked) |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🟠 high | Selected for Development | 2026-06-03 | Start work — new high-priority issue |
| FTFL-673 | Jira | Upgrade Grafana Alloy | 🟠 high | In Progress | 2026-06-03 | Drive to completion — just moved to In Progress |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-29 11:48 | Drive to review — security issue (was In Progress, now Selected) |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Timebox spike, drive to completion |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 09:52 | Review when higher-priority items cleared |

### Notes

- **Stale data**: 1Password CLI session expired — Jira data not refreshed this run. State carried forward from 2026-06-03T08:54.
- **FTFL-476** blocked since 2026-05-18 (22+ days). No movement. Needs escalation or explicit deprioritisation.
- **0 stale issues**: No In Progress issues untouched for >3 days (as of last fresh data).

### Known Data Gaps

- **Jira pipeline**: 1Password CLI session locked (`op` promptError). Run `op signin` in terminal to restore.
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
