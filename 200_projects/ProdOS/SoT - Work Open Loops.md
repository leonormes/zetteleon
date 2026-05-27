---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-27T08:17:00+00:00
modified: 2026-05-27T08:17:00+00:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Identify and escalate blocker on OMOP Stress Testing infra"
  - "FTFL-638: Resume Grafana Monitoring in testing cluster — stale 5d, going cold"
  - "FTFL-512: Triage Nginx 302 information exposure — new, Selected for Development"
---

## Work Open Loops—Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked |—| Identify blocker, escalate or deprioritise |
| FTFL-638 | Jira | Missing Grafana Monitoring in testing cluster | 🔴 critical | In Progress | 2026-05-22 | Resume work—stale 5 days, going cold |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development |—| Triage — assess exposure severity, schedule fix |
| FTFL-511 | Jira | [API-5] Nginx allows outdated HTTPS connection methods | 🟡 medium | Selected for Development |—| Triage — assess TLS version risk, schedule fix |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development |—| Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog |—| Review when higher-priority items cleared |

### Notes

- **FTFL-599** (Azure backup restore runbook) no longer appears in open Jira query. Confluence page was delivered 2026-05-26. Verify if ticket was closed/moved to Done — if so, move to Resolved table.
- **FTFL-638**: Extensive analysis done 2026-05-26 (Cursor + Antigravity prompts for Grafana Helm values fix). Branch `feature/FTFL-638-add-labels-for-logs` active. No git activity detected since. Issue remains the #1 execution risk — 5 days stale.
- **FTFL-511 & FTFL-512**: New Nginx security issues, both Selected for Development. Likely quick wins — consider batching into current sprint.
- **Inbox** (`00_Inbox/Untitled.md`): 5 unattended action items — Hermes cron MCP fix, manual next-thing lookup, Todoist integration, routines, and one empty item. None are Jira-tracked.

### Known Data Gaps

- **Pieces LTM**: Memory tool unavailable in cron context. No ambient context retrieved this run.
- **Jira**: 1Password field mismatch — the "Fitfile Atlassian" item has no "API Token" field (it has `password` instead). Script `jira-fetch.js` line 30 hardcodes `OP_FIELD = 'API Token'`. Jira data not refreshed since 12:00; table reflects last successful query. **Fix needed**: update `OP_FIELD` in jira-fetch.js to use the correct field name or switch to `op item get ... --fields password`.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items from Teams chat must be captured manually into Todoist until a Teams MCP is added.
- **Jira MCP server** (`@aashari/mcp-server-atlassian-jira`): Not used—Node `fetch()` does not honour macOS system proxies. Using `jira-fetch.js` with `https.request()` instead.
- **Todoist**: No Todoist CLI/tool available in cron context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
|—| No issues resolved since last run (2026-05-26 17:30) |—|
