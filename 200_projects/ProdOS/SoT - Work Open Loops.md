---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-09T10:02:00+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-476: Escalate or deprioritise OMOP Stress Testing infra (blocked 22 days)"
  - "FTFL-673: Drive Upgrade Grafana Alloy to completion — structured metadata pilot validated, ready for MR"
  - "FTFL-525: Start work on Ensure all backups are ZRS (High priority)"
---

> ⚠️ **Jira data stale (7th consecutive stale run)** — All data pipelines remain blocked:
> - `gk whoami` → `not authenticated` — session-level expiry (worse than per-provider token expiry)
> - `gk issue list --all --json` — returns empty (session authentication required)
> - `gk pr list --all --json` — returns empty (same auth failure)
> - Pieces LTM — MCP server running but no query tools registered
>
> Data below is **carried forward** from the last confirmed fresh fetch (2026-06-04 16:01 BST).
> To restore pipeline: run `gk auth login` interactively — this failure has persisted through 7 cron runs across 2 days.

## Work Open Loops — Source of Truth

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🔴 critical | 🚫Blocked | 2026-05-18 | Escalate or deprioritise (blocked 22 days) |
| FTFL-673 | Jira | Upgrade Grafana Alloy | 🟠 high | In Progress | 2026-06-08 | Structured metadata pilot validated — ready to MR |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🟠 high | Selected for Development | 2026-06-03 | Start work — high-priority issue |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | Selected for Development | 2026-05-27 | Timebox spike, drive to completion |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟡 medium | Selected for Development | 2026-05-29 | Drive to review — security issue |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | Selected for Development | 2026-05-27 | Review policies, plan rollout |
| FTFL-602 | Jira | The Hyve alerting | 🟡 medium | Selected for Development | 2026-05-26 | Schedule into current sprint |
| FTFL-478 | Jira | Grafana Workflows Monitoring Dashboard | 🟢 low | Backlog | 2026-04-29 | Review when higher-priority items cleared |

### Ambient Signals (08:17 scan)

| Signal | Source | Notes |
|--------|--------|-------|
| Grafana Cloud Logs Enrichment Pilot | Session (2026-06-08 12:48 TUI) | FTFL-673 follow-on: structured metadata pilot implemented and Helm-validated for ff-test-a. 3 files modified, all validation gates pass. Ready for MR. |
| CoS runs (6 stale yesterday, 1 today) | Cron sessions (09 Jun) | 08:17, 10:02 — both stale data, all pipelines blocked. Today is the 7th stale run in a row. |

### Notes

- ⚠️ All Jira data **carried forward** from 2026-06-04 (last fresh fetch). No pipelines operational in current cron context.
- FTFL-476 blocked since 2026-05-18 — now **22 days** blocked. Critical escalation trigger.
- FTFL-673 progress confirmed: structured metadata enrichment pilot implemented, code-written, Helm-validated, ready for MR. This reduces pressure on this item.
- **7th consecutive cron run with stale data** (5 yesterday + 2 today). The `gk whoami` session-level failure is persistent and will not self-recover.
- No stale issue check possible — no fresh Jira data this run.
- No new or resolved issues detected — data frozen from prior fetch. No changes since yesterday's 17:30 CoS.
- Current time: 2026-06-09 10:02 BST

### Known Data Gaps

- **GitKraken gk CLI** — `gk whoami` returns `not authenticated` (exit 1). Session-level expiry — all commands fail silently. Needs interactive `gk auth login` to restore. This has been broken since ~2026-06-04.
- **Pieces LTM** — MCP server initialises successfully but exposes zero query tools (`capabilities.tools: {}`). Server running at port 39300 but non-functional for context retrieval.
- **Microsoft Teams** — No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist** — MCP unavailable/read-only in current container context. Task sync skipped.

### Resolved

| ID | Summary | Resolved Date |
|----|---------|---------------|
| FTFL-511 | [API-5] Nginx allows outdated HTTPS connection methods | ~2026-06-01 |
| FTFL-680 | [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs | 2026-05-29 |
| FTFL-638 | Add labels for logs | 2026-05-28 |
| FTFL-599 | Update and test the runbook for Azure backup restore | 2026-05-26 |
| FTFL-144 | (details TBD) | 2026-05-26 |
| FTFL-626 | (details TBD) | 2026-05-26 |