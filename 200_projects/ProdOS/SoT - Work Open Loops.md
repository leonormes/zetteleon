---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-01T08:15:00+01:00
modified: 2026-06-01T08:15:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Blocked 14+ days — escalate or deprioritise OMOP Stress Testing infra"
  - "FTFL-511 + FTFL-512: Both Nginx security bugs Ready for review — review and merge PRs"
  - "FTFL-658: MKUH Terraform spike In Progress — timebox and drive to completion"
---

## Work Open Loops — Source of Truth

> ⚠️ **1Password BLOCKED** — `op whoami` reports "account is not signed in". All `op` commands timeout in cron context (no GUI/Touch ID). Jira data is **stale since 2026-05-29 19:00 UTC**. User must run `op signin` in a terminal to restore Jira pipeline.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 13:41 | Identify blocker, escalate or deprioritise (14+ days blocked) |
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🟡 medium | Ready for review | 2026-05-29 12:02 | Review and merge PR |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Ready for review | 2026-05-29 11:48 | Review and merge PR |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | In Progress ⬆️ | 2026-05-27 10:26 | Timebox spike, drive to completion |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 09:52 | Review when higher-priority items cleared |

### Notes

- **Jira data stale**: Last successful fetch was 2026-05-29 19:00 UTC. 1Password session expired. Issues may have changed since.
- **No status changes confirmed** since last successful fetch.
- **FTFL-476** blocked since 2026-05-18 (14+ days). No movement. Needs escalation or explicit deprioritisation.
- **FTFL-511 + FTFL-512**: Both remain Ready for review. PRs need review/merge.
- **FTFL-658** spike is active (In Progress).
- **0 stale issues** at last check: All In Progress/Ready issues updated within 3 days.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **1Password / Jira**: `op whoami` reports "account is not signed in". All `op` CLI commands timeout in cron context (no Touch ID/GUI session). **Jira data is stale since 2026-05-29**. User must run `op signin` in an interactive terminal to restore the Jira fetch pipeline. The `op-session-wrapper.sh` also fails — it tries `op signin --raw` which requires interactive auth too.
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
