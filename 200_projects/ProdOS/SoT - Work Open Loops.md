---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-27T10:15:00+01:00
modified: 2026-05-27T09:15:04+00:00
title: SoT - Work Open Loops
top3:
  - "FTFL-638: Grafana Monitoring in testing cluster — reactivated today, push forward"
  - "FTFL-476: OMOP Stress Testing infra — Blocked since 2026-05-18, escalate or deprioritise"
  - "FTFL-512: Nginx 302 info exposure — security issue, triage severity, batch with FTFL-511"
---

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-638 | Jira | Missing Grafana Monitoring in testing cluster | 🔴 critical | In Progress | 2026-05-27 08:41 | Push forward — branch `feature/FTFL-638-add-labels-for-logs` active |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Identify blocker, escalate or deprioritise (9 days blocked) |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-26 15:12 | Triage — assess exposure severity, schedule fix |
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🟡 medium | Selected for Development | 2026-05-26 15:12 | Triage — assess TLS version risk, batch with FTFL-511 |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 14:57 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Notes

- **FTFL-638 was reactivated** (updated 2026-05-27 08:41) — after being stale 5 days. No git activity detected on branch `feature/FTFL-638-add-labels-for-logs`. Issue remains the #1 execution risk.
- **FTFL-599** (Azure backup restore runbook) — **CONFIRMED CLOSED** 2026-05-26 15:36 after Confluence page delivery.
- **FTFL-144** — **CONFIRMED CLOSED** 2026-05-26 14:29 (newly discovered, was not in prior SoT).
- **FTFL-626** — **CONFIRMED CLOSED** 2026-05-26 09:11 (newly discovered, was not in prior SoT).
- **FTFL-511 & FTFL-512**: Nginx security issues, both Selected for Development. Likely quick wins — consider batching into current sprint.
- **Inbox** (`00_Inbox/Untitled.md`): 5 unattended action items — Hermes cron MCP fix, manual next-thing lookup, Todoist integration, routines, and one empty item. None are Jira-tracked.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Jira**: ~~Wrong 1Password item~~ — **FIXED 2026-05-27**: `jira-fetch.js` now uses item `ziqhlt2yuicadmmeio4odmimhi` ("JIRA_API_TOKEN") `credential` field. Script confirmed working with all 6 open issues returned.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist**: No Todoist CLI/tool available in cron context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD — not in prior SoT) | 2026-05-26 |
| FTFL-626 | (details TBD — not in prior SoT) | 2026-05-26 |
