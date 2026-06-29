---
created: 2026-06-09 09:14:56+00:00
last_updated: 2026-06-26 17:31:03+0100
title: SoT - Work Open Loops
top3:
- 'FTFL-694: Phase 0 asset registration still not kicked off — highest-priority epic, 9 days stale, needs activation'
- 'FTFL-692: CVE IDs in Trivy — at Ready for Release, quickest deployable win'
- 'FTFL-747: Grafana Alloy trivy-operator scraping — at Ready for Review, push _grafana.tpl change'
permalink: llmeon/200-projects/prod-os/so-t-work-open-loops
---

## Work Open Loops — Source of Truth

> Data current as of 2026-06-26T17:31. Carried forward from 16:01 run (Tier 2 quiet day — 4 consecutive stable runs).

| ID | Source | Summary | Priority | Status | Last Activity | Next Action |
|----|--------|---------|----------|--------|---------------|-------------|
| FTFL-694 | Jira | FFNode Stress Testing — full programme (Phase 0–4) | 🔴 critical | Selected for Development | 2026-06-17 | Kick off Phase 0: register assets, verify ≥500M-row dataset — 9 days stale, highest-priority epic still needs urgent activation |
| FTFL-525 | Jira | Ensure all backups are ZRS | 🔴 high | Selected for Development | 2026-06-24 | **Unblocked** — configure ZRS across MKUH/NNUH/CUH sites before it goes cold again |
| FTFL-692 | Jira | Add CVE ID's to Trivy helm operator | 🔴 high | Ready for Release | 2026-06-24 | Deploy `metricsVulnIdEnabled: "true"` in Trivy helm operator — quickest deployable win at Ready for Release |
| FTFL-747 | Jira | Configure Grafana Alloy to scrape trivy-operator metrics in staging | 🟡 medium | Ready for review | 2026-06-25 | Commit/push `_grafana.tpl` change to master, sync ff-test-a ArgoCD app, verify dashboard populates |
| FTFL-464 | Jira | Remove Calico Cloud Components from AKS/EKS Clusters | 🟡 medium | Ready for review | 2026-06-25 | Continue HIE SDE Calico Cloud cleanup. Was at Ready for Review as of last run — awaiting review. |
| FTFL-751 | Jira | Create DNS record for NCSC early warning service | 🟡 medium | Backlog | 2026-06-25 | Add DNS TXT record for domain verification — Backlog, no urgency yet |

### Priority Drift

| ID | Check |
|----|-------|
| All issues | No drift detected — Jira API values match SoT symbols. |

### Status Changes (since last run 2026-06-26T16:01)

| ID | What Changed |
|----|-------------|
| All items | No status changes. All 6 carry-over items remain at same status since 14:01 run. |

### Top 3 Next Actions

1. **FTFL-694** — Still the highest-priority epic. Phase 0 registration has not been kicked off. 9 days stale — needs immediate activation.
2. **FTFL-692** — CVE IDs in Trivy helm operator at Ready for Release. Deploy `metricsVulnIdEnabled: "true"` — quickest deployable win.
3. **FTFL-747** — Pending review approval for `_grafana.tpl` change. Commit and push to master once reviewed, sync ff-test-a ArgoCD app.

### Notes

- **Tier 2 quiet day**: SoT data carried forward from 16:01 run (4 consecutive stable journal entries). No full query executed.
- **No changes** since 16:01 run. All 6 items at same status, same priorities, same last activity dates.
- **Pieces LTM**: Skipped (Tier 2 shortcut). No new ambient activity expected.
- **GitLab MR**: !19 (FTFL-609 EBS CSI driver policy upgrade, hie-sde-v2) still open since 2026-06-16 — now 10 days stale, awaiting review/merge.
- **Staleness**: FTFL-694 last updated 2026-06-17 (9 days). FTFL-692 and FTFL-525 last updated 2026-06-24 (2 days). FTFL-464, FTFL-747, FTFL-751 fresh (yesterday).

### Known Data Gaps

- **Microsoft Teams**: No Teams MCP server configured. @mention action items not captured.

---

*Last updated: 2026-06-26 17:31 BST*