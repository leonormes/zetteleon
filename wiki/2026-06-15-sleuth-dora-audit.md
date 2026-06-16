---
tags: [sre, observability, dora, sleuth, audit, fitfile]
source: sleuth-graphql-api
created: 2026-06-15
---

# Sleuth DORA Audit — FITFILE

## Summary

GraphQL introspection and data extraction against `app.sleuth.io/graphql` using ALL-access API token. Full organisational structure, change sources, impact sources, and DORA metrics over the last 90 days.

**Organisation:** `fitfile` (leon.ormes@fitfile.com)

---

## Org Structure

### Project: Data Processing Service (`data-processing-service`)

| Field | Value |
|---|---|
| Environments | Production (HEALTHY), Test (HEALTHY) |
| Change Sources | 1 — `DPS` (CODE) |
| Repository | `gitlab.com/fitfile/data-and-analytics` |
| Deploy Tracking | **build** — but `buildProvider: NONE` |
| Impact Sources | **0** — no MTTR/CFR tracking |
| Issue Integration | Jira (jira-cloud-ffapp-board) |
| Rollback Detection | ✅ enabled |
| Has Impact History | ❌ no |

### Project: fitfile-app (`fitfile-app`)

| Field | Value |
|---|---|
| Environments | Production (**INCIDENT**), test (HEALTHY) |
| Change Sources | 4 — all **manual** tracking |
| Repositories | `data-and-analytics` (DPS dup), `InsightFILE` (FFCloud, FITConnect, frontend) |
| Impact Sources | 2 — Grafana AlertManager (test), Grafana Alerts Prod (Production) |
| Issue Integration | Jira (jira-cloud-ffapp-board) |
| Rollback Detection | ❌ disabled |
| Has Impact History | ✅ yes |

---

## DORA Metrics (Last 90 Days)

### Data Processing Service — Production

| Metric | Value | Status |
|---|---|---|
| Deployment Frequency | 0 deploys/day | ❌ No deploys tracked |
| Change Lead Time | 0s | ❌ No data |
| Change Failure Rate | 0% | ❌ No data |
| MTTR | 0s | ❌ No incident data |
| Deploy Volume | 0 | ❌ Dead project in Sleuth |

### fitfile-app — Production

| Metric | Value | Status |
|---|---|---|
| Deployment Frequency | 0 deploys/day | ❌ No deploys tracked |
| Change Lead Time | 0s | ❌ No data |
| Change Failure Rate | 0% | ❌ No data |
| MTTR | **55,573,212s (~643 days)** | ⚠️ Stale/ghost incident |
| Incidents Duration | 7,776,000s (90 days) | Spans full window |
| Deploy Volume | 0 | ❌ No deploys tracked |

---

## SRE Analysis

### 1. Duplicate / Ghost Config

- **DPS appears in both projects**: `dps` (fitfile-app) + `dps-2` (data-processing-service) — same repo, split tracking
- **DPS change source misconfigured**: `deployTrackingType: "build"` but `buildProvider: "NONE"` → receives no build events

### 2. Missing Integrations

| Gap | Impact |
|---|---|
| No CI/CD deploy tracking on any change source | All 5 sources use `manual` or broken `build` |
| No build provider connected (GitLab CI slug registered but not wired) | No deploy events reach Sleuth |
| No error-rate impact sources (Sentry, Rollbar, etc.) | No error-based CFR computation |
| No metric-based impact sources (Prometheus, Datadog, etc.) | No metric regression detection |
| Only Grafana AlertManager custom incidents | Weakest impact tracking tier |

### 3. Best Practice Gaps

- Deployment Frequency should come from GitLab CI pipeline data — blocked by no build provider
- Change Lead Time needs `cltStartDefinition` + Git commit data — both missing
- Change Failure Rate needs error-rate or deploy-health tracking — neither active on DPS
- MTTR has stale 643-day incident — needs clearing

---

## Recommended Actions

1. **Remove duplicate DPS** — delete `dps` change source from fitfile-app, keep `dps-2` on data-processing-service
2. **Connect GitLab CI** — wire up build provider integration so Sleuth receives deploy events
3. **Fix DPS tracking mode** — switch from broken `build` to `manual`, or connect GitLab properly
4. **Resolve Production INCIDENT** — clear the stale incident artifact on fitfile-app Production
5. **Enable rollback detection** on fitfile-app
6. **Add Sentry or similar** error-rate impact source
7. **Configure `cltStartDefinition`** per project for lead time computation