---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-29T09:01:00+00:00
modified: 2026-05-29T09:01:00+00:00
title: SoT - Work Open Loops
top3:
  - "FTFL-511 + FTFL-512: Both Nginx security bugs now In Progress — batch and push to completion"
  - "FTFL-476: Blocked 13+ days — escalate or deprioritise"
  - "FTFL-680: New Azure VM兼容性 task (High priority) — triage into current sprint"
---

## Work Open Loops — Source of Truth

> ✅ **Jira data fresh** as of 2026-05-29 09:01 UTC. Script returned 8 open issues. `op whoami` still reports "not signed in" but token fetch succeeded.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🔴 critical | In Progress | 2026-05-28 14:50 | Push to completion — batch with FTFL-512 |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🔴 critical | In Progress ⬆️ | 2026-05-28 19:14 | Push to completion — batch with FTFL-511 |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 13:41 | Identify blocker, escalate or deprioritise (13+ days blocked) |
| FTFL-680 | Jira | [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs | 🟡 medium | Backlog 🆕 | 2026-05-28 19:25 | Triage into current sprint — High priority, new issue |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Timebox spike, assess scope |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 10:26 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 09:52 | Review when higher-priority items cleared |

### Notes

- **Fresh data this run**: Jira fetch succeeded at 2026-05-29 09:01 UTC despite `op whoami` reporting "not signed in". Token was still accessible from 1Password.
- **FTFL-680 is new**: [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs — High priority, created 2026-05-28. Needs sprint triage.
- **FTFL-512 status change**: Moved from "Selected for Development" → "In Progress" since last run. Both Nginx security bugs (FTFL-511, FTFL-512) now actively In Progress.
- **FTFL-638 resolved**: Missing for fourth consecutive run (since 2026-05-28 13:00 UTC). Moved to Resolved table below.
- **FTFL-476** blocked since 2026-05-18 (13+ days). No movement. Needs escalation or explicit deprioritisation.
- **0 stale issues**: All In Progress issues updated within 3 days.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist**: No Todoist tool available in cron context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-638 | Add labels for logs | 2026-05-28 |
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |
