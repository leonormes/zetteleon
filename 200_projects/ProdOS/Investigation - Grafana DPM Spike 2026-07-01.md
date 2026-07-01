---
created: 2026-07-01T10:30:00+00:00
modified: 2026-07-01T10:34:31+00:00
permalink: llmeon/200-projects/prod-os/investigation-grafana-dpm-spike-2026-07-01
source: hermes
tags: [1, alloy, cost, grafana, incident, observability]
title: Investigation - Grafana DPM Spike 2026-07-01
---

## Investigation—Grafana Cloud DPM Spike (2026-07-01)

### Alert Summary

Grafana Cloud emailed a billing alert: DPM jumped 63% from 111,815 → 181,870 in the last 2 days. Monthly projected run rate: $1,429.47.

This is active metric series being forwarded by Grafana Alloy agents (not API query usage).

---

### Root Cause

Commit [`450ad7fa4`](https://gitlab.fitfile.com/FITFILE/Deployment/deployment/-/commit/450ad7fa4)—"Extend Grafana Alloy metrics coverage to argocd, argo-workflows, minio, mongodb, postgresql, spicedb"—merged to master on June 25, 2026.

This change:

1. Extended `prometheusOperatorObjects.serviceMonitors.namespaces` from `["trivy-system"]` → `["argocd", "argo", "spicedb", "trivy-system", "<cluster_namespace>"]`
   - Activated previously-unscraped ServiceMonitors in argocd, argo, spicedb, trivy-system, and every cluster's default namespace
   - Spicedb's `grpc_server_handled_total` alone contributes ~1,913 series per cluster

2. Enabled `annotationAutodiscovery` for `spicedb` namespace
   - Scrapes services with `k8s.grafana.com/scrape: "true"` annotation
   - Spicedb service now has the annotation (via `charts/spicedb/templates/service.yaml`)

3. Added `bitnami.metrics` merge to PostgreSQL application
   - Activates postgresql's ServiceMonitor (was previously missing the template merge)

Applies to ALL clusters—the `_grafana.tpl` template is shared. Each cluster now scrapes ServiceMonitors in `[argocd, argo, spicedb, trivy-system, <cluster_namespace>]`.

---

### Cluster Breakdown

| Cluster | Active Series | Est. Share | Notes |
|---------|-------------|------------|-------|
| staging | ~245,000 (estimated) | >55% | 3.4× larger than testing. `kube_pod_status_reason` alone = 18,352 series. |
| testing | 72,009 | ~20% | Had FTFL-638 Alloy migration. `grpc_server_handled_total` = 1,913. |
| sandbox-testing-1 | 58,367 | ~16% | |
| dev | 25,825 | ~9% | |
| Total | ~401,000 | | DPM (at 95th %ile) = 181,870 (series > DPM because some series are scraped at 60s+ intervals) |

#### Staging Vs Testing (Same 20 mAjor mEtrics)

| Metric | Staging | Testing | Ratio |
|--------|---------|---------|-------|
| kube_pod_status_reason | 18,352 | 5,144 | 3.6× |
| kube_pod_status_phase | 11,470 | 3,215 | 3.6× |
| kube_pod_container_resource_requests | 6,533 | 1,915 | 3.4× |
| kube_pod_container_resource_limits | 5,510 | 923 | 6.0× |
| kube_pod_container_info | 4,322 | 1,263 | 3.4× |
| kube_pod_info | 2,651 | 685 | 3.9× |
| grpc_server_handled_total | 1,935 | 1,913 | 1.0× |
| Total (sampled) | 51,265 | 15,248 | 3.4× |

---

### High-Cardinality Offenders

#### 1. `kube_pod_status_reason`—THE 1 Offender

- Has a `uid` label—643 unique UIDs in testing alone
- Each pod generates 8+ entries (one per reason: Evicted, NodeAffinity, NodeLost, etc.)
- Staging: 18,352 series just from this metric → ~$50-100/month alone
- Fix: Drop the `uid` label in kube-state-metrics or via Alloy `discovery.relabel`

#### 2. `grpc_server_handled_total`

- 1,913 series per cluster with spicedb
- ggRPC cardinality: 17 codes × 85 methods × 19 services
- Aggregated recording rules help but don't eliminate the raw scrape cost

#### 3. `kube_pod_status_phase` / `kube_pod_info`

- Similar uid/pod-level cardinality patterns
- `kube_pod_info` = 685–2,651 series per cluster

#### 4. `annotationAutodiscovery` (New)

- Now scraping any service with `k8s.grafana.com/scrape: "true"` in the spicedb namespace
- Could discover additional metrics endpoints beyond what was intended

---

### Timeline

| Date | Event |
|------|-------|
| Apr 2026 | FTFL-638: Grafana Alloy migration (new k8s-monitoring chart) |
| Jun 22 | FTFL-747: Scrape trivy-operator metrics (single namespace) |
| Jun 25 | Commit 450ad7fa4: Extended coverage to 5 namespaces + annotation autodiscovery |
| Jun 29-30 | DPM jumps 63% as ArgoCD syncs the change to clusters |
| Jul 1 | Grafana Cloud billing alert triggered |

---

### Recommended Fixes

#### Immediate (Reduce DPM by ~40% qUickly)

1. Drop `uid` label from kube-state-metrics
   - In `_grafana.tpl`, add a `discovery.relabel` in the kube-state-metrics scrape job:

 ```alloy
 rule {
   action = "labeldrop"
   regex  = "uid"
 }
 ```

   - Removes the highest-cardinality label from `kube_pod_status_reason`, `kube_pod_info`, etc.
   - Estimated saving: 30-40% reduction in KSM-derived series

2. Increase scrape intervals for non-critical ServiceMonitors
   - Scrape interval from 30s → 60s halves DPM
   - Apply selectively to spicedb, argocd (can tolerate lower resolution)

#### Short-term (Review and tUne)

1. Audit which ServiceMonitors in each namespace are actually needed
   - argocd, argo: core metrics are useful but do we need every metric?
   - trivy-system: vulnerability metrics are non-critical for cost
   - Add `metricRelabelings` to keep only essential metrics

2. Restrict annotation autodiscovery scope
   - Replace blanket namespace scoping with label selectors
   - Or drop the `k8s.grafana.com/scrape` annotation from spicedb and build a targeted ServiceMonitor instead

#### Long-term

1. Per-cluster `extraDiscoveryRules`
   - Move cluster-specific tuning (only staging needs certain scrape jobs) into cluster values rather than the shared template

2. Implement adaptive metrics
   - Use Grafana Cloud's Adaptive Metrics to automatically reduce cardinality on expensive metric families

---

### How to Verify Fix

After applying config changes (via ArgoCD sync):

```bash
# 1. Run series count per cluster (compare to baseline above)
gcx metrics series '{k8s_cluster_name="staging",__name__=~".+"}' --since 1h -o json

# 2. Check specific offender
gcx metrics series '{k8s_cluster_name="staging",__name__="kube_pod_status_reason"}' --since 1h -o json

# 3. Grafana Cloud billing dashboard
# Dashboards → Grafana Cloud → Billing/Usage → live trend
```

---

### Related

- FTFL-638—Initial Grafana Alloy migration
- FTFL-747—Trivy-operator metrics scrape
- FTFL-686—Optimise Loki log metadata
- `charts/ffnode/templates/_grafana.tpl`—Source of the extended coverage config
- `ffnodes/fitfile/*/values.yaml`—Per-cluster overrides
