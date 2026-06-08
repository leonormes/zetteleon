---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-08T10:01:27+01:00
modified: 2026-06-08T10:01:27+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Escalate or deprioritise OMOP Stress Testing infra (blocked 21 days)"
  - "FTFL-673: Drive Upgrade Grafana Alloy to completion (In Progress)"
  - "FTFL-525: Start work on Ensure all backups are ZRS (High priority)"
type: project
project_category: prodos
project_status: archived
---

> ⚠️ Open-work data stale — GitKraken CLI (`gk`) not authenticated. Run `gk auth login` in a terminal to restore the pipeline. Data carried forward from 2026-06-05.

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|-----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Escalate or deprioritise (21 days blocked) |
| FTFL-673 | Jira | Upgrade Grafana Alloy | 🟠 high | In Progress | 2026-06-03 | Drive to completion |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🟠 high | Selected for Development | 2026-06-03 | Start work — high-priority issue |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-29 | Drive to review — security issue |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 | Review policies, plan rollout |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 | Timebox spike, drive to completion |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Pieces Ambient Signals (Mon 8 Jun)

Recent Pieces LTM conversations indicate active workstreams:

| Signal | Source | Notes |
|--------|--------|-------|
| Grafana Cloud Audit and Cost Optimization | Pieces LTM | Ongoing cost-optimisation evaluation |
| Securing Faro Collector Receiver Authentication | Pieces LTM | New security workstream |
| Helm Chart Templating Analysis and Review | Pieces LTM | Helm chart quality work |
| MKUH Terraform Failure Investigation (FTFL-658) | Pieces LTM | Recent spike activity (a minute ago) |
| Grafana Loki: Labels vs. Structured Metadata Filtering | Pieces LTM | Observability tuning |
| GitKraken CLI and Jira Workflow Guide | Pieces LTM | Exploring gk workflow (recent) |
| Follow-up: Bessie's School Provision Dispute | Pieces LTM | Personal — formal complaint follow-up |

### Known Data Gaps

- **Pieces LTM**: Lightweight `pieces --headless conversations` probe succeeded (10 conversations, 7 substantive signals captured). No deep asset detail retrieved.
- **GitKraken CLI (`gk`) not authenticated (2026-06-08 10:01:27 BST)**: `gk whoami` returns `not authenticated`. All providers (Jira, GitLab, GitHub) show disconnected. Run `gk auth login` in an interactive terminal to restore the open-work pipeline.
- **Microsoft Teams**: No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist MCP**: Read-only (no create-task tool available). Task sync skipped.
- **Issue metadata via `gk`**: Even when authenticated, `gk issue list --json` returns only `id`, `url`, `title`, `description`, `issueType`, `assignees` — no `status`, `priority`, or `updated` fields.

### Resolved

| ID | Summary | Resolved Date |
|-----|---------|---------------|
| FTFL-511 | [API-5] Nginx allows outdated HTTPS connection methods | ~2026-06-01 |
| FTFL-680 | [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs | 2026-05-29 |
| FTFL-638 | Add labels for logs | 2026-05-28 |
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-27 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |