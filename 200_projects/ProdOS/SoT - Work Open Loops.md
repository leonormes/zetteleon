---
last_updated: 2026-05-26T10:28:01+01:00
top3:
  - "FTFL-638: Unblock Grafana Monitoring in testing cluster (stale 4d, going cold)"
  - "FTFL-599: Update and test Azure backup restore runbook"
  - "FTFL-602: The Hyve alerting implementation"
---

# Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | — | Identify blocker, escalate or deprioritise |
| FTFL-638 | Jira | Missing Grafana Monitoring in testing cluster | 🟠 high | In Progress | 2026-05-22 | Resume work — stale 4 days, going cold |
| FTFL-599 | Jira | Update and test the runbook for Azure backup restore | 🟡 medium | Selected for Development | — | Schedule into current sprint |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | — | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | — | Review when higher-priority items cleared |

## Known Data Gaps

- **Microsoft Teams**: No Teams MCP server configured. @mention action items from Teams chat must be captured manually into Todoist until a Teams MCP is added.
- **Jira MCP server** (`@aashari/mcp-server-atlassian-jira`): Not used — Node `fetch()` does not honour macOS system proxies. Using `jira-fetch.js` with `https.request()` instead.

## Resolved

*(No resolved issues since last run — this is the initial run.)*
