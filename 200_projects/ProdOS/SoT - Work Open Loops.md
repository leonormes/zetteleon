---
created: 2026-06-09 09:14:56+00:00
last_updated: 2026-06-29 16:02:30+0100
title: SoT - Work Open Loops
top3:
- 'FTFL-752: NEW — ACR 401 Unauthorised bug, Highest priority. VaultDynamicSecret overwrite=false causing stale creds. Ready for review — needs immediate attention'
- 'FTFL-694: Phase 0 asset registration still not kicked off — highest-priority epic, 12 days stale, needs urgent activation'
- 'FTFL-525: ZRS backups In Progress — configure ZRS across MKUH/NNUH/CUH today'
permalink: llmeon/200-projects/prod-os/so-t-work-open-loops
---

## Work Open Loops — Source of Truth

> Data current as of 2026-06-29T16:02. No changes since last run. 0 resolved. GitLab MRs: 2.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-752 | Jira | ACR 401 Unauthorised: ArgoCD cannot sync Helm charts from fitfileregistry.azurecr.io | 🔴 critical | Ready for review | 2026-06-29 | **NEW** — VaultDynamicSecret `overwrite: false` causing stale ACR creds; fix `overwrite: true`, clean up 30+ dangling credentials |
| FTFL-694 | Jira | FFNode Stress Testing — full programme (Phase 0–4) | 🔴 critical | Selected for Development | 2026-06-17 | Kick off Phase 0: register assets, verify ≥500M-row dataset — 12 days stale, highest-priority epic still needs urgent activation |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | In Progress | 2026-06-29 | Configure ZRS across MKUH/NNUH/CUH sites; push while momentum holds |
| FTFL-464 | Jira | Remove Calico Cloud Components from AKS/EKS Clusters | 🟡 medium | Ready for review | 2026-06-29 | Continue HIE SDE Calico Cloud cleanup. Awaiting review. |
| FTFL-751 | Jira | Create DNS record for NCSC early warning service | 🟡 medium | Ready for test | 2026-06-29 | Test DNS TXT record for domain verification |

### Resolved

| ID | Summary | Previous Status | Resolution |
|----|---------|----------------|------------|
| FTFL-692 | Add CVE ID's to Trivy helm operator | Ready for Release | Deleted from Jira — likely completed and closed out |
| FTFL-747 | Configure Grafana Alloy to scrape trivy-operator metrics in staging | Ready for review | Deleted from Jira — likely completed and closed out |

### Priority Drift

| ID | Check |
|----|-------|
| All issues | No drift detected — Jira API values match SoT symbols. |

### Status Changes (since last run 2026-06-29T14:01)

No status changes detected. All 5 open items unchanged.

### Top 3 Next Actions

1. **FTFL-752** — NEW Highest-priority bug. ACR 401 Unauthorised in ArgoCD. Root cause: `VaultDynamicSecret` with `overwrite: false` freezes ACR credentials on first write while Vault rotates them underneath. Fix `overwrite: true` and clean up 30+ dangling Azure AD app password credentials. This is actively blocking Helm chart syncs from `fitfileregistry.azurecr.io`.
2. **FTFL-694** — Still the highest-priority epic. Phase 0 registration has not been kicked off. 12 days stale — needs immediate activation.
3. **FTFL-525** — In Progress. Configure ZRS across MKUH/NNUH/CUH sites while momentum is fresh.

### Notes

- **Pieces LTM**: 106 signals in 8h window — all [6h ago] (stale). Internal agent self-reflection activity around ACR credential investigation. No new ambient signals since last update.
- **No Jira changes** since last run at 14:01. All 5 IDs stable for 3 consecutive runs (12:06→14:01→16:02).
- **GitLab MRs**: 2 open — !2 (FTFL-525 ZRS, mkuh-prd-4) and !19 (FTFL-609 EBS CSI driver, hie-sde-v2, 13 days stale, awaiting review).
- **Staleness**: FTFL-694 last updated 2026-06-17 (12 days — most stale). All others refreshed today (2026-06-29).

### Known Data Gaps

- **Microsoft Teams**: No Teams MCP server configured. @mention action items not captured.

---

*Last updated: 2026-06-29 16:02 BST*