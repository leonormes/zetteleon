---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-02T09:30:00+01:00
modified: 2026-06-02T09:30:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Blocked 20+ days — escalate or deprioritise OMOP Stress Testing infra"
  - "FTFL-512: Nginx 302 security bug In Progress — drive to review"
  - "FTFL-658: MKUH Terraform spike — timebox and drive to completion"
---

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 13:41 | Identify blocker, escalate or deprioritise (20+ days blocked) |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟠 high | In Progress | 2026-05-29 11:48 | Drive to review — security issue, needs PR follow-up |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Timebox spike, drive to completion |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-673 | Jira | Upgrade Grafana Alloy | 🟢 low | Backlog | 2026-06-01 | Assess effort, schedule or deprioritise |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 09:52 | Review when higher-priority items cleared |

### Notes

- **Jira data fresh**: Successful fetch at 2026-06-02 09:30 BST via `jira-fetch.js`. 1Password CLI session active.
- No status changes since 2026-06-02 09:00 BST run. Same 7 open issues.
- **FTFL-476** blocked since 2026-05-18 (20+ days). No movement. Needs escalation or explicit deprioritisation.
- **FTFL-512** remains In Progress — no status change. Security-related, should be prioritised.
- **FTFL-658** spike still "Selected for Development" — not yet started. Consider starting or confirming backlog placement.
- **FTFL-673** remains in Backlog — no assessment yet.
- **0 stale issues**: No In Progress issues untouched for >3 days.
- **No new issues**: Set unchanged since prior run.

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
