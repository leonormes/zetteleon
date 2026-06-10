---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-10T14:03:36+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-525: Diagnose why ZRS backup conversion is blocked — highest priority item stalled"
  - "FTFL-658: Complete MKUH Terraform spike investigation — re-opened as Blocked"
  - "FTFL-609: Continue EBS CSI Driver policy migration (actively In Progress)"
---

## Work Open Loops — Source of Truth

> ✅ **Fresh data** — Jira API queried directly with static PAT (JIRA_API_TOKEN via Python POST). All data current as of 2026-06-10T14:03.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | 🚫Blocked | 2026-06-10 | Diagnose why blocked — highest priority item stalled; unblock to resume |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | 🚫Blocked | 2026-06-10 | Complete spike investigation — re-opened as Blocked, determine scope |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | In Progress | 2026-06-10 | Continue policy migration work — actively being progressed |
| FTFL-686 | Jira | Optimise Loki log metadata: move high-cardinality labels to structured metadata and inject k8s annotations for richer log context | 🟡 medium | Backlog | 2026-06-09 | Scope the enrichment work — ready to pick up when bandwidth allows |
| FTFL-657 | Jira | Investigate possibility of using Bastion Direct to Private AKS cluster | 🟢 low | Selected for Development | 2026-06-10 | New spike (1 day timebox) — scope and schedule |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟢 low | Selected for Development | 2026-06-04 | Low-priority security item — pending review |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🟢 low | 🚫Blocked | 2026-06-10 | Deprioritised (was critical, now Low). Updated today 10:23 — likely comment/field edit |
| ude-cli MR !58 | GitLab | MinHash matching strategy in ude-cli (MR !58) | 🔵 watch | opened | 2026-01-05 | 5-month-old MR — decide: merge or close as stale |

### Status Changes (since last run 2026-06-10T12:01)

| ID | What Changed |
|----|-------------|
| — | **No changes detected.** All 7 Jira issues and 1 GitLab PR unchanged since the 12:01 run. |

### Top 3 Next Actions

1. **FTFL-525** — Diagnose the Blocked status. Highest priority In Progress item turned stale. Unblock to resume ZRS backup conversion.
2. **FTFL-658** — Complete MKUH Terraform spike investigation. Re-opened as Blocked after being previously Done.
3. **FTFL-609** — Continue EBS CSI Driver policy migration (actively In Progress, updated today).

### Notes

- **Data pipeline**: Jira API healthy. Static PAT from `JIRA_API_TOKEN` env var works directly with Python POST. No daemon dependency.
- **gk CLI status**: Jira ✓ connected. GitLab ✓ connected. Lacks status/priority/dates fields — direct API is preferred.
- **Pieces LTM**: MCP server running at localhost:39300 but CLI queries not returning usable data in cron context. Ambient context skipped.
- **ude-cli MR !58** — Open since January 2026 (5.2 months), no recent activity. Needs a decision (merge or close).

### Known Data Gaps

- **Pieces LTM** — CLI query timed out (30s) and `pieces search` returned no matches. MCP health endpoint unreachable. Ambient context skipped.
- **Microsoft Teams** — No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist** — No CLI or MCP tool available in cron context. Task sync skipped.

### Resolved (unchanged from previous runs)

| ID | Summary | Status Change |
|----|---------|---------------|
| FTFL-602 | The Hyve alerting | Selected for Development → **Closed** ✅ |
| FTFL-673 | Upgrade Grafana Alloy | Done (unchanged) |
| FTFL-478 | Grafana Workflows Monitoring Dashboard | Done (unchanged) |