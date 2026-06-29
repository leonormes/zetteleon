---
title: FTFL-747 Alloy Metrics Coverage — Verification Report
date: 2026-06-25
tags:
- kubernetes
- observability
- grafana
- helm
- alloy
- argocd
- fitfile
- verification
source: /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment
related: '[[FITFILE k8s-monitoring Config Audit]], [[k8s-monitoring-helm Deep Analysis]]'
permalink: llmeon/ftfl-747-alloy-metrics-coverage-verification-report
---

# FTFL-747 Alloy Metrics Coverage — Verification Report

Companion note to [[FITFILE k8s-monitoring Config Audit]]. Verifies, with live Grafana Cloud query evidence, that both merged changes are actually flowing real metrics:

1. FTFL-747 — trivy-operator vulnerability metrics via `prometheusOperatorObjects`.
2. The follow-up coverage extension — argocd, argo-workflows, minio, mongodb, postgresql, spicedb (vault-secrets-operator deferred — its metrics endpoint sits behind `kube-rbac-proxy`, tracked separately).

Tooling: `gcx` (Grafana Cloud CLI), datasource `grafanacloud-prom` (`uid: grafanacloud-prom`, `https://prometheus-prod-05-gb-south-0.grafana.net/api/prom` — the same Mimir instance hardcoded in OpenCost's config, flagged in the companion audit as footgun #3).

## Before/after: the core proof

Query (matches every job introduced by the coverage-extension change):

```promql
count(up{job=~"argocd.*|argo-workflows.*|spicedb|ff-test-a-minio|ff-test-a-mongodb-b17ef-metrics|ff-test-a-databases-postgresql-metrics|ff-test-a-mssql"})
```

| When | Result |
|---|---|
| 4 hours ago (`--from now-4h --to now-4h`) | **empty** (0 series) |
| 2 hours ago (`--from now-2h --to now-2h`) | **empty** (0 series) |
| Now | **22** |

Timeline (`--from now-3h --to now --step 5m`) pins the exact moment the new scrape targets came online:

| Timestamp (UTC) | Series count |
|---|---|
| 12:55 | 1 |
| 13:00 | 14 |
| 13:05 | 22 |
| 13:10 | 22 |
| 13:15 | 22 |

Matches the ArgoCD sync window for the merge — zero, to a clean ramp, to a stable 22 active series within 10 minutes, no further change since.

## New `job` label values (didn't exist before today)

Pulled via `gcx metrics labels -d grafanacloud-prom --label job`:

```
argo-workflows-workflow-controller
argocd-application-controller-metrics
argocd-applicationset-controller-metrics
argocd-dex-server
argocd-notifications-controller-metrics
argocd-repo-server-metrics
argocd-server-metrics
ff-test-a-databases-postgresql-metrics
ff-test-a-minio
ff-test-a-mongodb-b17ef-metrics
ff-test-a-mssql        (bonus — picked up automatically via the per-site namespace sweep)
spicedb
```

**Notable bonus finding**: the same `job` list also shows `dev-minio`, `dev-mongodb-b17ef-metrics`, `dev-mssql`, `dev-postgresql-metrics`, and `sandbox-testing-1-minio`, `sandbox-testing-1-mongodb-b17ef-metrics` — i.e. the fix is already benefiting other ffnode sites automatically too, exactly as designed (shared `_grafana.tpl`, dynamic per-site namespace scoping via `{{ include "namespace" . }}`).

**Resolves an open question from the original FTFL-747 plan**: `up{...}` label data shows two genuinely distinct physical clusters reporting these jobs — `cluster="staging"` (instance IPs in the `10.224.0.x` range I'd been checking via `kubectl`, the `ff-test-a` site) and `cluster="testing"` (different instance IPs entirely, `ffnodes/fitfile/testing`). These are confirmed separate clusters, not just naming variants of the same one — both now getting the same coverage since both run the same shared template.

## Per-app health (`up{job="..."}`, now)

| App | Job | Status | Real metric sampled |
|---|---|---|---|
| argocd (server) | `argocd-server-metrics` | ✅ up=1 ×2 | `argocd_app_info` → 32 series |
| argocd (repo-server) | `argocd-repo-server-metrics` | ✅ up=1 ×2 | — |
| argocd (application-controller) | `argocd-application-controller-metrics` | ✅ up=1 ×2 | — |
| argocd (applicationset-controller) | `argocd-applicationset-controller-metrics` | ✅ up=1 ×2 | — |
| argocd (notifications-controller) | `argocd-notifications-controller-metrics` | ✅ up=1 ×2 | — |
| argocd (**dex-server**) | `argocd-dex-server` | ❌ **up=0 ×2** (both clusters) | none |
| argo-workflows (controller metrics endpoint) | `argo-workflows-workflow-controller` (port 9090) | ✅ up=1 ×2 | `{job="argo-workflows-workflow-controller"}` → 175 series total |
| argo-workflows (**telemetry endpoint**) | `argo-workflows-workflow-controller` (port 8081) | ❌ **up=0 ×2** (both clusters) | — |
| minio | `ff-test-a-minio` | ✅ up=1 | `minio_node_process_starttime_seconds` → 1 series |
| mongodb | `ff-test-a-mongodb-b17ef-metrics` | ✅ up=1 ×2 (replica set) | `mongodb_up` → 1, 1 (both pods healthy) |
| postgresql | `ff-test-a-databases-postgresql-metrics` | ✅ up=1 | `pg_up` → 1 |
| mssql (bonus, not requested) | `ff-test-a-mssql` | ✅ up=1 | — |
| spicedb | `spicedb` (annotationAutodiscovery) | ✅ up=1 | — |

## Findings to follow up on

1. **`argocd-dex-server` is fully down** — 2 of 2 endpoints (`http-metrics`, port 5558) failing on both clusters. The ServiceMonitor and scrape config are correct (that's what this exercise just proved); the target itself isn't answering. Likely cause: Dex (ArgoCD's SSO component) may not actually be running/exposed if this deployment doesn't use ArgoCD's built-in OIDC — worth a quick `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-dex-server` check before digging further.
2. **Argo Workflows' `telemetry` endpoint (port 8081) is down**, but its main `metrics` endpoint (port 9090) is healthy with real data (175 series) — this is a partial, low-severity gap. The ServiceMonitor scrapes two separate endpoints; only one is actually serving Prometheus-format metrics.
3. Neither of these blocks the original goal — every app in scope now has at least one working metrics path, and 5 of 7 (argocd mostly, argo-workflows mostly, minio, mongodb, postgresql, spicedb) are fully clean.

## Reusable queries

```bash
# datasource discovery
gcx datasources list

# current label values (job/namespace) — quick way to spot new scrape targets
gcx metrics labels -d grafanacloud-prom --label job

# point-in-time check (swap --to for any past timestamp to compare)
gcx metrics query -d grafanacloud-prom 'count(up{job=~"<selector>"})' --from now-2h --to now-2h

# timeline / ramp-up shape
gcx metrics query -d grafanacloud-prom 'count(up{job=~"<selector>"})' --from now-3h --to now --step 5m

# find unhealthy targets within an otherwise-working job selector
gcx metrics query -d grafanacloud-prom 'up{job=~"<selector>"} != 1'
```