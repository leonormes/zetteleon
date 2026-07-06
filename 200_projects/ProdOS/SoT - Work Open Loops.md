---
created: 2026-06-09T09:14:56+00:00
last_updated: 2026-07-02 08:21:14+0100
modified: 2026-07-04T10:52:08+00:00
permalink: llmeon/200-projects/prod-os/so-t-work-open-loops
title: SoT - Work Open Loops
top3: ["FTFL-694: FFNode Stress Testing — In Progress. Phase 0 registration needs activation", "FTFL-752: ACR 401 Unauthorised bug, Highest priority. VaultDynamicSecret overwrite=false causing stale creds. Ready for review — needs immediate attention", "FTFL-757: Grafana Cloud metrics spike +63% (181,870 DPM). Ready for review — investigate source exporters"]
---

## Work Open Loops—Source of Truth

> Data current as of 2026-07-02T08:21. 0 new | 0 resolved. Jira open: 6. GitLab MRs: 2.—No changes since last run.

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-752 | Jira | ACR 401 Unauthorised: ArgoCD cannot sync Helm charts from fitfileregistry.azurecr.io | 🔴 critical | Ready for review | 2026-07-01 | VaultDynamicSecret `overwrite: false` causing stale ACR creds; fix `overwrite: true`, clean up 30+ dangling credentials |
| FTFL-694 | Jira | FFNode Stress Testing—full programme (Phase 0–4) | 🔴 critical | In Progress | 2026-07-01 | Kick off Phase 0: register assets, verify ≥500M-row dataset—epic needs activation |
| FTFL-757 | Jira | Investigate unexpected 63% increase in Grafana Cloud metrics usage (181,870 DPM) | 🔴 high | Ready for review | 2026-07-01 | Review Grafana Cloud billing/usage dashboard; identify which services or exporters caused the spike |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | In Progress | 2026-07-01 | Configure ZRS across MKUH/NNUH/CUH sites; push while momentum holds |
| FTFL-464 | Jira | Remove Calico Cloud Components from AKS/EKS Clusters | 🟡 medium | Ready for review | 2026-07-01 | Continue HIE SDE Calico Cloud cleanup. Awaiting review. |
| FTFL-751 | Jira | Create DNS record for NCSC early warning service | 🟡 medium | Ready for test | 2026-07-01 | Test DNS TXT record for domain verification |

### Resolved

| ID | Summary | Previous Status | Resolution |
|----|---------|----------------|------------|
| FTFL-692 | Add CVE ID's to Trivy helm operator | Ready for Release | Deleted from Jira—likely completed and closed out |
| FTFL-747 | Configure Grafana Alloy to scrape trivy-operator metrics in staging | Ready for review | Deleted from Jira—likely completed and closed out |

### Priority Drift

| ID | Check |
|----|-------|
| All issues | No drift detected—Jira API values match SoT symbols. |

### Status Changes (Since lAst rUn 2026-07-01T16:01)

No changes since last run.

### Top 3 Next Actions

1. FTFL-752—Highest-priority bug. ACR 401 Unauthorised in ArgoCD. Root cause: `VaultDynamicSecret` with `overwrite: false` freezes ACR credentials on first write while Vault rotates them underneath. Fix `overwrite: true` and clean up 30+ dangling Azure AD app password credentials. Actively blocking Helm chart syncs from `fitfileregistry.azurecr.io`.
2. FTFL-694—In Progress. FFNode Stress Testing epic. Phase 0 registration (register assets, verify ≥500M-row dataset) needs activation. Core capacity programme for NHS-scale query path.
3. FTFL-757—Grafana Cloud metrics spike: 181,870 DPM (+63% from 111,815 DPM), projected $1,429.47 monthly billing run rate. Investigate which exporters/services caused the increase. Review billing/usage dashboard.

### Notes

- Pieces LTM: N/A—Pieces OS unresponsive (dual-failure: CLI time out + REST API empty response). No ambient signals captured for this window.
- GitLab MRs: 2 open—!2 (FTFL-525 ZRS, mkuh-prd-4) and!19 (FTFL-609 EBS CSI driver, hie-sde-v2, awaiting review). ⚠️ MR!19 (FTFL-609) is still open but FTFL-609 is no longer in the open loops—pre-existing drift, likely stale MR.
- Staleness: No items currently stale (>7d without status change). All items last updated 2026-07-01 (1 day ago—first run of the day).

### Known Data Gaps

- Microsoft Teams: No Teams MCP server configured. @mention action items not captured.
- Pieces LTM: Ambient context unavailable this run due to Pieces OS unresponsiveness.

---

_Last updated: 2026-07-02 08:21 BST_
