---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-05-26T11:00:00+01:00
modified: 2026-05-26T11:43:27+00:00
title: SoT - Work Open Loops
top3: ["FTFL-476: Identify and escalate blocker on OMOP Stress Testing infra", "FTFL-599: Schedule Azure backup restore runbook update into current sprint", "FTFL-638: Resume Grafana Monitoring in testing cluster — stale 4d, going cold"]
---

## Work Open Loops—Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked |—| Identify blocker, escalate or deprioritise |
| FTFL-638 | Jira | Missing Grafana Monitoring in testing cluster | 🔴 critical | In Progress | 2026-05-22 | Resume work—stale 4 days, going cold |
| FTFL-599 | Jira | Update and test the runbook for Azure backup restore | 🟡 medium | Selected for Development |—| Schedule into current sprint |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development |—| Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog |—| Review when higher-priority items cleared |

### Known Data Gaps

- Microsoft Teams: No Teams MCP server configured. @mention action items from Teams chat must be captured manually into Todoist until a Teams MCP is added.
- Jira MCP server (`@aashari/mcp-server-atlassian-jira`): Not used—Node `fetch()` does not honour macOS system proxies. Using `jira-fetch.js` with `https.request()` instead.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
|—| No issues resolved since last run (2026-05-26 10:28) |—|
