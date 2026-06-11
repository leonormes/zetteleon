---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-11T14:01:32+01:00
title: SoT - Work Open Loops
top3:
  - "FTFL-525: Diagnose why ZRS backup conversion is blocked — highest priority item stalled"
  - "FTFL-609: Continue EBS CSI Driver policy migration to V2 (actively In Progress)"
  - "FTFL-658: Complete MKUH Terraform spike investigation — still Blocked"
---

## Work Open Loops — Source of Truth

> ✅ **Fresh data** — Jira API queried directly with static PAT (JIRA_API_TOKEN via Python POST). All data current as of 2026-06-11T14:01.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | 🚫Blocked | 2026-06-11 | Diagnose why blocked — highest priority item stalled; unblock to resume |
| FTFL-609 | Jira | [EE] New Managed Policies Available for the EBS CSI Driver | 🟡 medium | In Progress | 2026-06-11 | Continue policy migration work to V2 — actively being progressed |
| FTFL-658 | Jira | [SPIKE] Investigate MKUH Failing Terraform Runs | 🟡 medium | 🚫Blocked | 2026-06-11 | Complete spike investigation — still Blocked, determine path forward |
| FTFL-686 | Jira | Optimise Loki log metadata: move high-cardinality labels to structured metadata and inject k8s annotations for richer log context | 🟡 medium | Backlog | 2026-06-09 | Scope the enrichment work — ready to pick up when bandwidth allows |
| FTFL-512 | Jira | [API-6] Nginx 302 exposes information | 🟢 low | Selected for Development | 2026-06-11 | Low-priority security bug — scope the fix |
| FTFL-657 | Jira | Investigate possibility of using Bastion Direct to Private AKS cluster | 🟢 low | Selected for Development | 2026-06-10 | New spike (1 day timebox) — scope and schedule |
| FTFL-476 | Jira | OMOP Stress Testing infra + monitoring | 🟢 low | 🚫Blocked | 2026-06-10 | Deprioritised (was critical, now Low). Blocked — unblock if priority rises |

### Status Changes (since last run 2026-06-11T12:00)

| ID | What Changed |
|----|-------------|
| — | **No status changes detected.** All 7 Jira issues still open with same statuses. No new issues created. |

### Top 3 Next Actions

1. **FTFL-525** — Diagnose the Blocked status. Highest priority item still stalled. Updated today — check what was done and continue unblocking.
2. **FTFL-609** — Continue EBS CSI Driver policy migration to V2. Actively In Progress with update today.
3. **FTFL-658** — Complete MKUH Terraform spike investigation. Still Blocked — determine path forward.

### Notes

- **Data pipeline**: Jira API healthy. Static PAT from `JIRA_API_TOKEN` env var works directly with Python POST. No daemon dependency.
- **gk CLI status**: `gk pr list --all --json` returned empty — no open GitLab MRs.
- **Pieces LTM**: REST API available. Recent activity shows CI/CD pipeline report generation (completed ~10:07) and an AKS upgrade action item (cluster `aks-ff-uks-gp-01`, Kubernetes v1.33.x upgrade due 31 July 2026) — not yet tracked in Jira.
- **FTFL-681** (CUH: Upgrade Grafana K8s Monitoring Helm chart to v4.1.3) exists in Jira Backlog but is unassigned — not in current open loop set.
- **No new issues** created since last run. Data stable.

### Known Data Gaps

- **Pieces LTM** — REST API available but no server-side time filter; all 11k assets scanned. Potential for noise from compaction/reflection artifacts.
- **Microsoft Teams** — No Teams MCP server configured. @mention action items must be captured manually.
- **Todoist** — No CLI or MCP tool available in cron context. Task sync skipped.
- **AKS cluster upgrade** — Email notification about `aks-ff-uks-gp-01` upgrade (deadline 31 July 2026) surfaced in Pieces context but no corresponding Jira issue created yet. Not tracked in this SoT.

### Resolved

| ID | Summary | Status Change |
|----|---------|---------------|
| ude-cli MR !58 | MinHash matching strategy in ude-cli | Removed — no longer open in GitLab (merged or closed) |
| FTFL-602 | The Hyve alerting | Selected for Development → **Closed** ✅ |
| FTFL-673 | Upgrade Grafana Alloy | Done (unchanged) |
| FTFL-478 | Grafana Workflows Monitoring Dashboard | Done (unchanged) |