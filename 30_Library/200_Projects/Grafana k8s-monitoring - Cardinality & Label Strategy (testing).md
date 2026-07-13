---
chart: k8s-monitoring 4.1.3 (alloy 1.8.1, Alloy app v1.16.1)
cluster: testing
created: 2026-06-04T00:00:00+00:00
modified: 2026-07-13T08:44:39+00:00
permalink: llmeon/30-library/200-projects/grafana-k8s-monitoring-cardinality-label-strategy-testing
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
source: owl-audit-agent — consolidated from 4 audit drafts + Loki labels reference
stack: fitfiletest (Grafana Cloud, prometheus-prod-05-gb-south-0)
tags: [adaptive-metrics, alloy, audit, cardinality, grafana, kubernetes, labels, loki, monitoring, seedling, structured-metadata, testing-cluster]
ticket: FTFL-638
title: Grafana k8s-monitoring - Cardinality & Label Strategy (testing)
type: infra-audit
---

## Grafana k8s-monitoring—Cardinality & Label Strategy (Testing cLuster)

> [!note] Consolidation provenance
> Merged from four overlapping audit drafts of the `testing` cluster (all 2026-06-04) plus the Loki _Labels vs Structured Metadata_ reference. Canonical figures are taken from the three consistent drafts; one outlier draft is set aside—see [[#Data reconciliation note]]. All actions are robust to that discrepancy: only the _size_ of the saving is uncertain, not the fixes themselves.

This doc has three parts:

1. [[#Part 1 — Principles Labels vs Structured Metadata|Principles]]—the indexing model that everything else follows from.
2. [[#Part 2 — Recommended Label & Metadata Taxonomy|Taxonomy]]—the cluster-wide label/metadata governance standard.
3. [[#Part 3 — testing Cluster Audit 2026-06-04|Audit]]—the concrete findings + fixes for `testing`.

---

## Part 1—Principles: Labels Vs Structured Metadata

The single rule everything below depends on:

> Labels answer _"which stream?"_—Structured metadata answers _"which line within the stream?"_

### Labels (Indexed)

Indexed key–value pairs that define and identify a stream (Loki) or series (Prometheus/Mimir).

```logql
{app="payments", env="production", region="eu-west-1"}
```

- Evaluated at ingest time.
- Stored as stream identifiers in the index.
- Used for stream selection—the first stage of any query.
- Directly drive cardinality and storage structure.

### Structured Metadata (Non-indexed)

Non-indexed key–value pairs attached to individual log lines, not streams. Introduced in Loki 3.0 with OTLP-native support; sometimes called "non-indexed labels".

```logql
{app="payments"} | traceID="abc123xyz"
```

- Stored alongside the log entry, not in the index.
- Not used for stream selection—only post-ingest filtering.
- Safe to be high-cardinality—no cardinality penalty.
- Maps natively from OpenTelemetry trace/span/resource attributes.

### The Practical Difference

| Dimension | Labels | Structured metadata |
|---|---|---|
| Indexed? | Yes | No |
| Query stage | Stream selection (fast) | Post-ingest filter (slower) |
| Cardinality risk | High—too many unique values = index explosion | Low—safe for high-cardinality |
| Scope | Entire stream | Individual log lines |
| Storage cost | Index overhead per unique combo | Inline with entry, no index overhead |
| Typical values | `env`, `app`, `region`, `namespace` | `traceID`, `spanID`, `userID`, `requestID` |
| OTel native? | Partial | Yes—OTLP resource/span attributes map here |

### When to Use Each

| Use labels when… | Use structured metadata when… |
|---|---|
| Cardinality is low and stable (e.g. `env` ∈ {dev, staging, prod}) | Cardinality is high or unbounded (`traceID`, `userID`, `requestID`) |
| You need fast stream selection (always filtering `app="payments"`) | Data originates from OpenTelemetry |
| You own the schema (deliberate architectural choice at ingest) | You want to correlate logs ↔ traces (carry `trace_id`/`span_id`) |
| Routing/retention depends on it (ruler, compactor, retention) | The field is useful for filtering but not routing |

### Common Pitfall

Using a high-cardinality value as a label is the number-one Loki performance mistake.

```yaml
# ❌ BAD — millions of unique streams, index explosion
labels:
  userID: "user-38291"
  requestID: "req-abc-xyz-123"

# ✅ GOOD — low-cardinality label + high-cardinality metadata
labels:
  app: "api-gateway"
structured_metadata:
  userID: "user-38291"
  requestID: "req-abc-xyz-123"
```

The bad pattern grows the index unboundedly, degrades query performance, and spikes ingester memory pressure.

A well-designed Loki setup uses 3–6 low-cardinality labels (`app`, `env`, `namespace`, `cluster`) and pushes everything else—OTel attributes, request IDs, trace correlation—into structured metadata.

### In Prometheus / Mimir

Same principle, different mechanism: every unique label combination is a new time series. Prometheus has no native structured-metadata equivalent (3.x adds native histograms and OTLP resource attributes, but labels remain the cardinality driver). Rule is identical: keep label values low-cardinality; never label on `requestID` or `userID`.

### War story—FTFL-638 (The Lesson that Motivates the sTandard)

During debugging of `fitfile-cloud-testing-aks-cluster` under ticket FTFL-638, the `pod` field was being written into Loki's `structured_metadata` block by the default chart config—which strips it from the stream labels, rendering it unusable as an indexed selector (`{pod="…"}` stops working).

> [!warning] Collector self-collision
> A collector must not write the same field to both the indexed stream labels and structured metadata. If `pod: pod` is active in Loki's `structured_metadata`, it is removed from stream labels—breaking direct selector filters. Keep `pod` indexed only if you select streams by pod name, and in that case it must not also appear in structured metadata.

Fix validated on the testing cluster on 26 May: formatting `job` as `namespace/container` (e.g. `testing/mongodb`, `testing/ffcloud-service`) to prevent index collisions.

---

## Part 2—Recommended Label & Metadata Taxonomy

A unified, two-tier governance model applied across all namespaces (`thehyve`, `argocd`, `monitoring`, …).

### The Two Tiers

| Tier | Holds | Goes in | Constraint |
|---|---|---|---|
| Indexing layer | Low-cardinality, static identifiers | Kubernetes labels | Drives scheduling, ingress, replication, observability indices—must stay low-card |
| Metadata layer | High-cardinality, dynamic, or sensitive data | Annotations + Loki/OTel structured metadata | Prevents bloat in etcd, Prometheus TSDB, and Loki's stream index |

### Standard Labels

Apply the Kubernetes recommended `app.kubernetes.io/*` set on every workload object (Deployment, Pod template, Service, ServiceMonitor, Ingress, ConfigMap), plus a small operational set.

| Label | Purpose | Example |
|---|---|---|
| `app.kubernetes.io/name` | Logical application identity | `grafana-alloy`, `ffcloud-service`, `spicedb` |
| `app.kubernetes.io/instance` | Unique deployed instance / Helm release | `grafana-alloy-prod`, `fitconnect-dev-a` |
| `app.kubernetes.io/version` | App / chart / image version | `"v1.9.1"` |
| `app.kubernetes.io/component` | Architectural tier | `telemetry-agent`, `backend`, `frontend`, `database` |
| `app.kubernetes.io/part-of` | Parent business platform | `observability-platform`, `clinical-linkage` |
| `app.kubernetes.io/managed-by` | Deployment driver | `Helm`, `ArgoCD` |
| `environment` | Logical environment zone | `testing`, `staging`, `prod` |
| `team` | Owning cohort for triage | `platform-observability`, `clinical-sre` |
| `owner` | Accountable owner | `platform-observability` |
| `cost-center` | Cost allocation | `observability` |
| `criticality` | Alert-routing tier | `high` / `medium` / `low` |

> To avoid collisions with third-party labels, optionally prefix the operational set DNS-style: `yourcompany.com/environment`, `yourcompany.com/cost-center`, etc.

Repeat the high-level ownership + cost + criticality labels on namespaces and use node-pool labels for scheduling only (`nodepool-type`, `workload-type`).

### Selector Stability Rules

`spec.selector.matchLabels` is immutable once a workload exists—changing it requires recreation.

- DO use only stable logical identifiers in selectors:
  `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/component`.
- DO NOT put rolling variables in selectors or pod-template labels:
  Git SHAs, release/container tags, build IDs, deployment timestamps.

### Annotations (Kubernetes lEvel)

Richer context for CI/CD, runbooks, and automation—never used as selectors.

| Annotation | Holds |
|---|---|
| `yourcompany.com/repository` | Git source URL |
| `yourcompany.com/runbook-url` | On-call triage page |
| `yourcompany.com/slack-channel` | On-call contact channel |
| `yourcompany.com/git-sha` / `/build-id` | Build provenance |
| `yourcompany.com/last-deployed-at` | ISO deploy timestamp |
| `yourcompany.com/config-checksum` | ConfigMap/Secret hash (triggers rolling restarts) |

### Structured Metadata / OTel Resource Attributes (Observability lEvel)

Map Kubernetes metadata into stable resource attributes; do not promote all of them to metric/log labels.

| Index block (indexed stream labels) | Structured-metadata block (non-indexed) |
|---|---|
| `cluster` | `pod` _(indexed only if you select by it—then keep it out of structured metadata)_ |
| `namespace` | `level` (`info`/`error`) |
| `container` | `caller`, `trace_id`, `span_id` |
| `job` = `namespace/container` (e.g. `testing/mongodb`) | `client_ip`, `user_id` |
| | `build_id`, `version` |

Recommended OTel resource attributes for indexing/grouping (the stable subset only): `service.name`, `service.namespace`, `deployment.environment.name`, `k8s.cluster.name`, `k8s.namespace.name`, `team`, `cost_center`, `criticality`.

### What NOT to Put in Labels

If Alloy forwards Kubernetes metadata into metrics/logs/traces, these become index dimensions and/or leak into dashboards, alerts, and billing exports:

```text
pod-name      pod-uid       container-id   image-digest
git-sha       build-id      request-id     session-id
user-id       email         customer-name  ticket-id
timestamp     full-url      ip-address     secret-name      token
```

Keep these as log fields / OTel attributes only.

### Canonical Deployment Template

One template for a general backend service—shows exactly where labels vs annotations belong.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fitconnect-service
  namespace: clinical-linkage
  labels:
    app.kubernetes.io/name: fitconnect-service
    app.kubernetes.io/instance: fitconnect-prod-1
    app.kubernetes.io/version: "v2.4.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: fitconnect-platform
    app.kubernetes.io/managed-by: ArgoCD
    environment: prod
    team: clinical-sre
    criticality: high
  annotations:
    yourcompany.com/repository: "https://gitlab.com/fitfile/deployment"
    yourcompany.com/runbook-url: "https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1"
    yourcompany.com/slack-channel: "#clinical-alerts"
spec:
  replicas: 3
  selector:
    matchLabels:                       # static, low-cardinality, immutable
      app.kubernetes.io/name: fitconnect-service
      app.kubernetes.io/instance: fitconnect-prod-1
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:                          # must match selector exactly
        app.kubernetes.io/name: fitconnect-service
        app.kubernetes.io/instance: fitconnect-prod-1
        app.kubernetes.io/component: backend
        environment: prod              # sibling context for metrics grouping
        team: clinical-sre
      annotations:                     # mutable provenance lives here, not in labels
        yourcompany.com/git-sha: "cae7da9d8c0147ba82b775fc99b3df8d"
        yourcompany.com/last-deployed-at: "2026-06-04T10:42:11+01:00"
        yourcompany.com/config-checksum: "sha256:d8c4d39eada24257aff6e8403730"
    spec:
      containers:
        - name: fitconnect
          image: fitfile-registry.azurecr.io/fitconnect:v2.4.0
```

### Alloy Helm Values Pattern

Use the chart's label-extension fields (keys vary by chart version—confirm with `helm show values grafana/alloy`).

```yaml
fullnameOverride: grafana-alloy
controller:
  type: daemonset
  extraLabels:
    app.kubernetes.io/name: grafana-alloy
    app.kubernetes.io/instance: grafana-alloy-prod
    app.kubernetes.io/component: telemetry-agent
    app.kubernetes.io/part-of: observability-platform
    app.kubernetes.io/managed-by: Helm
    environment: prod
    team: platform-observability
    owner: platform-observability
    cost-center: observability
    criticality: high
serviceAccount:
  additionalLabels: { app.kubernetes.io/name: grafana-alloy, app.kubernetes.io/instance: grafana-alloy-prod, app.kubernetes.io/component: telemetry-agent }
serviceMonitor:
  enabled: true
  additionalLabels: { app.kubernetes.io/name: grafana-alloy, app.kubernetes.io/instance: grafana-alloy-prod, release: kube-prometheus-stack }
podAnnotations:
  yourcompany.com/repository: "github-org/platform-observability"
  yourcompany.com/runbook: "observability/grafana-alloy"
  yourcompany.com/oncall: "platform-observability"
  yourcompany.com/deployment-method: "helm"
```

### Optimisation Checklist

- [x] Label/selector separation—no dynamic tags (image tags, build sigs) inside `spec.selector.matchLabels`. [completion:: 2026-06-11]
- [x] Standardise `job` pattern—`job = namespace/container` in the collector config (prevents index collisions). [completion:: 2026-06-11]
- [x] No duplicate metadata stages—a field is written to stream labels or structured metadata, never both (see FTFL-638). [completion:: 2026-06-11]
- [ ] Audit & drop high-cardinality indices—periodically confirm request IDs, user codes, and row hashes are never promoted to labels.

---

## Part 3—testing Cluster Audit (2026-06-04)

> Scope: `grafana/k8s-monitoring` v4.1.3 on the `testing` AKS cluster (`fitfile-cloud-testing-aks-cluster`), shipping to Grafana Cloud stack `fitfiletest`. A small, already well-tuned estate (~9k active series). No runaway-cardinality emergency. Findings are efficiency/correctness wins—the largest is a config bug (node-exporter producing zero metrics).

### Executive Summary

| Field | Value |
|---|---|
| Chart version | 4.1.3 (k8s-monitoring) · alloy chart 1.8.1 · Alloy app v1.16.1 |
| Release | `grafana-k8s-monitoring` (umbrella, applied by ArgoCD, not `helm install`) |
| Sub-releases | `…-alloy-metrics`, `…-alloy-logs`, `…-alloy-events` |
| Namespace | `monitoring` |
| Cluster / Cloud | AKS UK South, K8s v1.34.7, 2× `Standard_E4s_v5` (system pool) |
| Cluster label | `cluster="testing"` |
| Total active series | ~8,952 (consensus of 3 drafts; range 8,952–8,981) |
| Distinct label names | 313 · log labels: 15 |
| High-entropy labels | 4—`id`, `name` (cAdvisor) · `uid`, `container_id` (KSM) |
| Config bug | node-exporter runs on every node but 0 host metrics reach Cloud |
| Realistic active-series cut | ~6–9% immediate + large churn/index reduction from high-entropy drops |

### Priority Action List (Merged, dEduped)

| # | Priority | Action | Effect | Data-loss risk |
|---|---|---|---|---|
| 1 | BUG / HIGH | node-exporter DaemonSet runs but `host_metrics` block renders empty → `node_cpu_*`, `node_filesystem_*`, `node_network_*`, `node_memory_*` all = 0 series. Wire host metrics _or_ disable the DaemonSet to reclaim per-node CPU/mem | 0 series today (nothing collected); frees resources if disabled | None (you have nothing) |
| 2 | QUICK WIN | Drop `kube_pod_status_reason` via KSM allowlist exclusion | −470 series (~5.2%); 468/470 permanently `0` | Low (eviction _reason_ counts; phase still covered) |
| 3 | HIGH (entropy) | `labeldrop` `id` on cAdvisor (208-value cgroup path on ~2,206 series) | Negligible instantaneous; large churn/index cut | None (redundant w/ `pod`+`container`) |
| 4 | HIGH (entropy) | `labeldrop` `name` on cAdvisor (206-value container hash on ~2,206 series) | As above | None (redundant w/ `container`) |
| 5 | HIGH (entropy) | `labeldrop` `container_id` on KSM `kube_pod_container_info`/`…_init_…` (135 values) | Removes restart churn | Low (only breaks `container_id` joins—uncommon) |
| 6 | MEDIUM | Evaluate `uid` (pod UUID; 95 current / ~220 across 45 KSM metrics, ~2,875 series) for Adaptive Metrics aggregation or `labeldrop` | Removes churn on KSM pod metrics | Medium—some Grafana mixins join on `uid`. Validate before applying. |
| 7 | LOW | Remove duplicate `k8s_cluster_name` external label (identical to `cluster`, on ~8,675 series) | Label-bytes saving on nearly every series | None—confirm no dashboard/alert queries it first |
| 8 | LOW | `labeldrop` `boot_id`/`system_uuid` globally on cAdvisor (currently only set to `NA` on `machine_memory_bytes`) | Removes 6 stray distinct values | None (node-level dupes of `node`) |
| 9 | MEDIUM | Recording rules for `container_*` without `image` (74 distinct, grows over time) for dashboards that don't need image-level granularity | Reduces query-time cardinality | Low (raw data retained) |
| 10 | LOW (future) | Review open-ended OTel annotation labelmap `__meta_kubernetes_pod_annotation_resource_opentelemetry_io_(.+)`—future cardinality risk if devs inject dynamic annotations | Preventative | n/a |
| 11 | OPERATIONAL | Resolve `alloy-logs-fsb5q` Pending (one node not shipping logs) | Restores per-node log coverage | n/a |

### Discovery

| Item | Value |
|---|---|
| RELEASE_NAME | `grafana-k8s-monitoring` |
| NAMESPACE | `monitoring` |
| CHART_VERSION | `4.1.3` (confirmed 4.x) |
| GitOps | ArgoCD app `grafana-k8s-monitoring` in ns `argocd`—no Flux `HelmRelease` CRD present |
| Sub-chart revs | alloy-events (rev 2), alloy-logs (rev 11), alloy-metrics (rev 4) |

Pod inventory (monitoring ns):

| Pod | Type | Status | Restarts | Age |
|---|---|---|---|---|
| `…-alloy-events-6bc7658f54-rk9d6` | Deployment | Running | 1 | 14h |
| `…-alloy-logs-w692p` | DaemonSet | Running | 1 | 5h |
| `…-alloy-logs-fsb5q` | DaemonSet | Pending | 0 | 5h |
| `…-alloy-metrics-0` | StatefulSet | Running | 1 | 14h |
| `…-alloy-operator-df4fb5cff-rc49j` | Deployment | Running | 0 | 14h |
| `…-kube-state-metrics-76d5575c89-d78l5` | Deployment | Running | 0 | 14h |
| `…-node-exporter-d25gv` / `-hqjhj` | DaemonSet | Running | 0 | 5h |
| `…-opencost-76475d9f45-zgpq5` | Deployment | Running | 0 | 14h |

> [!warning] Pending pod (Issue 11)
> `alloy-logs-fsb5q` is unschedulable: `0/2 nodes available: 1 Insufficient cpu, 1 didn't satisfy NodeAffinity`. Capacity/scheduling, not config. One logs collector (`w692p`) is healthy. Add capacity or relax the DaemonSet's node constraints for full per-node coverage.
> ```bash
> kubectl describe pod grafana-k8s-monitoring-alloy-logs-fsb5q -n monitoring
> ```

### Current Config

Values pulled from the ArgoCD Application (`.spec.source.helm.values`); rendered Alloy (River) configs from the three `…-alloy-*` ConfigMaps. Chart repo `fitfileregistry.azurecr.io`, path `helm/k8s-monitoring`, `targetRevision: 4.1.3`.

Destinations (Grafana Cloud—mutual-TLS + Basic Auth; creds from Vault → `monitoring` secret):

| Destination | Type | URL | Auth |
|---|---|---|---|
| prometheus | remote_write | `https://prometheus-prod-05-gb-south-0.grafana.net/api/prom/push` | basicauth + `X-Scope-OrgID={tenantId}` + mTLS |
| loki | loki push | `{loki-host}/loki/api/v1/push` | basicauth + `tenant_id` + mTLS |
| tempo | otlp http | `{tempo-host}` | basicauth + mTLS |

external_labels (identical on metrics + logs writers):

```hcl
external_labels = {
  "cluster"          = "testing",
  "k8s_cluster_name" = "testing",   // ← redundant duplicate of cluster (Issue 7)
}
```

WAL + queue (`prometheus.remote_write`):

```yaml
wal:   { truncate_frequency: 2h, min_keepalive_time: 5m, max_keepalive_time: 8h }
queue_config:
  capacity: 10000
  min_shards: 1
  max_shards: 50
  max_samples_per_send: 2000
  batch_send_deadline: 5s
  min_backoff: 30ms
  max_backoff: 5s
  retry_on_http_429: true
  sample_age_limit: 0s
```

Collector resources:

| Collector | Controller | CPU req/lim | Mem req/lim |
|---|---|---|---|
| alloy-events | deployment | 50m / 200m | 128Mi / 256Mi |
| alloy-logs | daemonset | 5m / 200m | 64Mi / 256Mi |
| alloy-metrics | statefulset | 50m / 200m | 256Mi / 512Mi |

Scrape jobs (alloy-metrics)—all gated by `__name__` keep-lists, 60s interval:

| Job                                                       | Source                      | Keep-list (abbrev.)                                                                                                                                          |
| --------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `integrations/kubernetes/kubelet`                         | node role, https kubelet    | `up`, `kubelet_*`, `kubernetes_build_info`, `namespace_workload_pod`, `process_*`, `rest_client_requests_total`, `storage_*`, `volume_manager_total_volumes` |
| `integrations/kubernetes/resources`                       | kubelet `/metrics/resource` | `node_cpu_usage_seconds_total`, `node_memory_working_set_bytes`                                                                                              |
| `integrations/kubernetes/cadvisor`                        | kubelet `/metrics/cadvisor` | `container_cpu_*`, `container_fs_*`, `container_memory_*`, `container_network_*`, `machine_memory_bytes`                                                     |
| `integrations/kubernetes/kube-state-metrics`              | KSM service                 | large `kube_*` allowlist                                                                                                                                     |
| `integrations/opencost`                                   | opencost pod (honor_labels) | `kubecost_*`, `container_*_allocation`, `node_*`, `pv_hourly_cost`, …                                                                                        |
| `integrations/kubernetes/kubernetes_monitoring_telemetry` | self-report                 | `grafana_kubernetes_monitoring_.*`                                                                                                                           |
| `host_metrics` (node-exporter)                            | declare block is EMPTY  |—see Issue 1                                                                                                                                                |

Pod logs (alloy-logs): discovers pods on local node (`spec.nodeName=$HOSTNAME`); relabels `namespace`/`pod`/`container`; extra rule `namespace/container → job`; drops pods annotated `logs.grafana.com/pods.enabled = false|no|skip`; CRI/docker runtime detection; structured metadata = `service_instance_id` only; drops `filename`, `tmp_container_runtime`.

Existing hygiene (good—already in place):

- cAdvisor: drops empty `container`/`image`; normalises `boot_id`/`system_uuid` → `NA` on `machine_memory_bytes`; filters non-physical fs devices & network interfaces.
- No cluster-wide `metric_relabel_configs` beyond job-level keep/drop. `honor_labels: true` on opencost (its labels pass through unfiltered).

### Label Audit

Buckets: A external · B static · C relabel-generated · D k8s-meta auto · E dropped.

| Label | Bucket | Source | Example | Notes |
|---|---|---|---|---|
| `cluster` | A | `external_labels` | `testing` | canonical ✓ |
| `k8s_cluster_name` | A | `external_labels` | `testing` | REDUNDANT—duplicates `cluster` |
| `source` | B/C | discovery.relabel replacement | `kubernetes` | constant |
| `job` | B/C | `integrations/kubernetes/<x>` | `…/cadvisor` | canonical ✓ |
| `node` | C/D | `__meta_kubernetes_node_name` | `aks-…` | canonical ✓ |
| `instance` | C/D | `__address__` / pod node | `10.0.x.x:10250` | ok (≤6) |
| `namespace` | D | `__meta_kubernetes_namespace` | `monitoring` | canonical ✓ (~15–39) |
| `pod` | D | `__meta_kubernetes_pod_name` / KSM | `…-d78l5` | canonical ✓ (~95–470) |
| `container` | D | `__meta_kubernetes_pod_container_name` / KSM | `alloy` | canonical ✓ (~12–87) |
| `image` | D | KSM / cAdvisor | `…@sha256:…` | MEDIUM (74) |
| `service_name` / `service_namespace` / `service_instance_id` | C | annotation→label→fallback | `alloy` | logs; OTel-compatible |
| `reason` | D | KSM | `Evicted` | low value (mostly 0) |
| `phase` | D | KSM | `Running` | low (≤11) |
| `replicaset` | D | KSM | `…-76d5575c89` | meaningful name (~182) |
| `created_by_name` | D | KSM |—| medium (~72) |
| `uid` | D | KSM pod UID | `be91cc17-…` | HIGH-entropy (UUID) |
| `id` | D | cAdvisor cgroup path | `/kubepods.slice/…/cri-containerd-…scope` | HIGH-entropy (path+hash) |
| `name` | D | cAdvisor container hash | `<64-hex>` | HIGH-entropy (hash)—dup of `container` |
| `container_id` | D | KSM containerd id | `containerd://282b…` | HIGH-entropy (hash) |
| `boot_id` / `system_uuid` | E* | normalised → `NA` on `machine_memory_bytes` only | `NA` | still on other cAdvisor metrics |
| `filename` / `tmp_container_runtime` / `kind` | E | `stage.label_drop` |—| already dropped ✓ |

Flags:

- 🔴 High-entropy: `id`, `name` (cAdvisor); `uid`, `container_id` (KSM). Each rotates on every pod/container restart → series churn (Grafana Cloud bills active + churned).
- 🟠 Duplicate info: `k8s_cluster_name == cluster`; `id`/`name`/`container_id` all duplicate `pod`+`container`.
- 🟢 Taxonomy: core labels (`job, instance, cluster, namespace, pod, container, node`) all present and canonically named.

### Cardinality Report

Via `gcx metrics query` (PromQL) against stack `fitfiletest`.

> Cluster enumeration `count by (cluster)({__name__!=""})`: dev 2,715 · ollie 2,913 · sandbox-testing-1 9,766 · testing 8,981 · staging 21,803 · `<aggregated>` 5,136. The `<aggregated>` bucket confirms Adaptive Metrics aggregation is already active on this stack.

Top metrics by series count (`cluster="testing"`):

| Rank | Metric | Series | Notes |
|---:|---|---:|---|
| 1–2 | `kube_pod_status_phase` / `kube_pod_status_reason` | 470 ea | 94 pods × 5; 468 of `reason` are `0` |
| 3 | `kube_deployment_status_condition` | 288 | |
| 4 | `kube_secret_metadata_resource_version` | 237 | |
| 5 | `kube_replicaset_*` (7–8 metrics) | 182 ea | |
| 6 | `kube_pod_container_resource_requests` | 179 | |
| 7 | `kube_pod_container_resource_limits` | 142 | |
| 8 | `kube_pod_container_info` | 122 | carries `container_id` |
| 9 | `container_cpu_usage_seconds_total` | 117 | carries `id`,`name`,`image` |
| 10 | `container_memory_*` (6 metrics) | 117 ea | carries `id`,`name`,`image` |
| 11 | `container_fs_*` (4 metrics) | 99 ea | + `device` |
| 12 | `container_network_*` (6 metrics) | 88 ea | + `interface` |

Top labels by distinct value count:

| Rank | Label | Distinct | In N metrics | Series | Risk |
|---:|---|---:|---:|---:|---|
| 1 | `id` (cAdvisor) | 206–208 | 23 | ~2,206 | HIGH (entropy) |
| 2 | `name` (cAdvisor) | 206 | many | ~2,206 | HIGH (entropy) |
| 3 | `uid` (KSM) | 95 _(–220 across 45 metrics)_ | 45 | ~2,875 | HIGH (entropy) |
| 4 | `container_id` (KSM) | 135 | 2 | 135 | HIGH (entropy) |
| 5 | `pod` | ~95–470 | many |—| LOW (canonical) |
| 6 | `replicaset` | 182 | 8 | ~1,456 | MEDIUM (meaningful) |
| 7 | `container` | ~12–87 | many |—| LOW |
| 8 | `image` | 74 | several |—| MEDIUM |
| 9 | `created_by_name` | 72 | KSM |—| MEDIUM |
| 10 | `namespace` | ~15–39 | all |—| LOW |
|—| `reason` / `phase` | 17 / 11 | 1 ea | 470 ea | LOW (mostly 0) |
|—| `job` / `instance` / `node` | 6 / 6 / 2 |—|—| LOW |

> [!info] Risk thresholds (per brief)
> CRITICAL > 500 distinct or high-entropy · HIGH 100–500 · MEDIUM 20–100 · LOW < 20.
> No label exceeds 500 distinct (small cluster), so none is CRITICAL by count—but `id`, `name`, `uid`, `container_id` are CRITICAL by entropy: they rotate on restart and drive churn-based billing. On a CI/test cluster with frequent restarts this is the biggest real cost lever, which is why these drops matter far more than their instantaneous counts suggest.

Series breakdown by job (sums to ~8,952 ✓):

| Job | Series | % |
|---|---:|---:|
| kube-state-metrics | 5,578 | 62.3% |
| cadvisor | 2,206 | 24.6% |
| opencost | 503 | 5.6% |
| kubelet | 387 | 4.3% |
| telemetry | 9 | 0.1% |
| resources | 6 | 0.1% |
| _(unlabelled)_ | 263 | 2.9% |

### Issues & Fixes

> [!note] Delivery model
> This is Alloy (River), not classic Prometheus—there is no `metric_relabel_configs` YAML. The equivalents are `rule { action = "labeldrop" }` blocks surfaced through the chart's `metricsTuning` / `extraMetricProcessingRules` values. Because the release is GitOps via ArgoCD, the correct delivery is a Helm-values patch to `.spec.source.helm.values` (FIX TYPE D). River snippets below are for reference.

#### Issue 1—node-exporter Collects Nothing (CONFIG BUG · HIGH)

DaemonSet deployed (`telemetryServices.node-exporter.deploy: true`, `hostMetrics.enabled: true`) but the rendered `declare "host_metrics"` block is empty; `node_filesystem_avail_bytes`, `node_network_receive_bytes_total`, `node_memory_MemAvailable_bytes`, `node_cpu_seconds_total` all return 0 series. Root cause = known 4.1.3 wiring gap when node-exporter is declared under `telemetryServices` but the feature source isn't linked.

- Fix A (keep): bind a scrape source to the node-exporter service / upgrade chart.
- Fix B (reclaim, recommended on test): disable the DaemonSet. Series impact 0; frees per-node CPU/mem. Data-loss risk none (already nothing).

#### Issue 2—`kube_pod_status_reason` is 99.6% Dead Weight (QUICK WIN · FIX TYPE A)

470 series, 468 permanently `0`, only 2 ever `=1`. Drop via KSM allowlist exclusion. −470 series (~5.2%). Data-loss risk Low (lose eviction _reason_ counts; `kube_pod_status_phase` still covers status).

#### Issue 3 + 4—high-entropy cAdvisor Labels `id` + `name` (CHURN · FIX TYPE A)

`id` = 208-value cgroup path; `name` = 206-value container hash; both on ~2,206 cAdvisor series, fully redundant with `pod`+`container`. Instantaneous reduction negligible, but large churn/index reduction (each rotates on container restart, minting fresh series). Data-loss risk none.

#### Issue 5—high-entropy KSM `container_id` (CHURN · FIX TYPE A)

135-value containerd hash on `kube_pod_container_info` / `kube_pod_init_container_info`. Removes restart churn. Data-loss risk Low (only `container_id` joins).

#### Issue 6—KSM `uid` across 45 Metrics (EVALUATE · FIX TYPE C pReferred)

95 current / ~220-value pod UUID on ~2,875 series; churns on every pod recreation. Preferred = Adaptive Metrics (already active): aggregate dropping `uid` where unused, keeping `pod`. Or a recording-rule rollup.

```yaml
# via Adaptive Metrics aggregation (gcx metrics adaptive rules) — needs cloud-admin token
# drop dimension "uid" from kube_pod_* where unused → (cluster, namespace, pod, container)
```

> [!warning] Validate first
> Medium data-loss risk—some Grafana mixins join on `uid`. Keep it if in doubt. This is the one fix to verify before applying.

#### Issue 7—duplicate `k8s_cluster_name` External Label (STORAGE · FIX TYPE D)

Identical to `cluster`, on ~8,675 series. No series-count change; removes a redundant indexed label from nearly every series. Data-loss risk none—confirm no dashboards/alerts query it first.

#### Issue 8—`boot_id` / `system_uuid` not Fully Dropped (LOW · FIX TYPE A)

Currently only set to `NA` on `machine_memory_bytes`; still present (2 / 4 distinct) on other cAdvisor metrics. Drop globally.

#### Issue 9—`image` Cardinality on cAdvisor (MEDIUM · FIX TYPE C)

74 distinct, grows over time. For dashboards that don't need image-level granularity, add recording rules that strip `image`:

```yaml
groups:
  - name: testing_cluster_agg
    interval: 60s
    rules:
      - record: job:container_cpu_usage_seconds_total:rate5m
        expr: sum by (job, namespace, pod, container, node, cluster)
                (rate(container_cpu_usage_seconds_total{cluster="testing"}[5m]))
      - record: job:container_memory_working_set_bytes:sum
        expr: sum by (job, namespace, pod, container, node, cluster)
                (container_memory_working_set_bytes{cluster="testing"})
```

Risk Low—raw data retained.

### Consolidated Helm Values Patch (FIX TYPE D)

Apply to ArgoCD app `grafana-k8s-monitoring` → `.spec.source.helm.values` (k8s-monitoring 4.1.3 schema). Validate with `--dry-run` / Argo diff before sync.

```yaml
clusterMetrics:
  collector: alloy-metrics
  destinations: [prometheus]
  enabled: true

  kube-state-metrics:
    discoveryType: service
    metricsTuning:
      excludeMetrics:
        - kube_pod_status_reason          # Issue 2: ~470 series, 468 always 0
    extraMetricProcessingRules: |
      rule { action = "labeldrop", regex = "container_id" }   # Issue 5: containerd hash (churn)
      # rule { action = "labeldrop", regex = "uid" }          # Issue 6: VALIDATE mixin joins first

  cadvisor:
    extraMetricProcessingRules: |
      rule { action = "labeldrop", regex = "id" }                    # Issue 3: cgroup path (churn)
      rule { action = "labeldrop", regex = "name" }                  # Issue 4: container hash (churn)
      rule { action = "labeldrop", regex = "boot_id|system_uuid" }   # Issue 8: node ids (dup of node)

# Issue 7: remove the redundant external label from BOTH writers
# loki.write "loki" / prometheus.remote_write "prometheus":
#   external_labels = { "cluster" = "testing" }   # drop "k8s_cluster_name"

# Issue 1: node-exporter currently produces 0 series (empty host_metrics block).
# Option B — reclaim per-node resources on test:
telemetryServices:
  node-exporter:
    deploy: false
```

> [!note] Why a values patch (not a ConfigMap edit)
> FIX TYPE A changes can't be applied via Helm values alone in older flows—they need the ConfigMap or `extraObjects`/`alloy.metrics.extraConfig`. With ArgoCD `selfHeal: true`, a direct ConfigMap patch will be reverted. Either route the rules through chart values (above) or temporarily pause auto-sync / use `ignoreDifferences`.

### Verification Commands

```bash
# Series count drops
gcx metrics query 'count({cluster="testing"})'

# Confirm high-entropy labels gone
gcx metrics query 'count by (name) ({cluster="testing"})'
gcx metrics query 'count by (id) ({cluster="testing"})'
gcx metrics query 'count by (uid) ({cluster="testing"})'

# Quick-win check (expect the always-zero count to vanish with the metric)
gcx metrics query 'count(kube_pod_status_reason{cluster="testing"} == 0)'

# Bug check — expect 0 series TODAY (node-exporter collecting nothing)
gcx metrics query 'count(node_filesystem_avail_bytes{cluster="testing"})'
```

### Data Reconciliation Note

> [!important] One outlier draft was set aside
> Of the four audit drafts merged here, three agree (~8,950–8,980 active series; the per-job breakdown above sums to ~8,952; `id`/`name` ≈ 206; `uid` ≈ 95). One draft is a ~6× outlier, claiming 51,557 total series, label `name` = 914 / `id` = 839 / `container_id` = 523 / `uid` = 512, and ~15,000 series / 30–40% savings (it also referenced `image_id` and `trivy_*` metrics absent from the others).
>
> Decision: the outlier's figures are not used. Most likely it was an early draft using a different query scope (possibly a multi-cluster `count` mistaken for single-cluster) or a directional estimate.
>
> Confidence in ~8,952 series: HIGH—three independent drafts agree and the per-job sum reconciles.
> Robustness: the _actions_ are unaffected—the fixes (`labeldrop` on `id`/`name`/`uid`/`container_id`, dropping `kube_pod_status_reason`, removing `k8s_cluster_name`) are identical regardless of exact counts. Only the magnitude of saving is uncertain, hence the honest ~6–9% immediate + churn reduction rather than the outlier's 30–40%.

### Caveats / Limitations

- Adaptive-Metrics admin API returned 401 (`gcx metrics adaptive rules/recommendations`)—the configured context holds a datasource query token, not a cloud-admin token. FIX TYPE C savings are directional, not pulled from Grafana's recommender. Re-run after `gcx login` with an admin token.
- Series counts are instantaneous (`count(…)` at query time); billing reflects active + churned over the window—which is precisely why the high-entropy drops matter more than their snapshot counts.
- No `kubectl` RBAC failures encountered; all data available.

### Open Threads

- [ ] Re-run adaptive-metrics recommendations with a cloud-admin token for exact savings figures.
- [ ] Decide node-exporter: wire `host_metrics` source vs disable DaemonSet (Issue 1).
- [ ] Validate `uid` joins in Grafana mixins before dropping (Issue 6).
- [ ] Confirm nothing queries `k8s_cluster_name` before removing it (Issue 7).
- [ ] Resolve `alloy-logs-fsb5q` Pending—add capacity or relax DaemonSet tolerations (Issue 11).
- [ ] Discard or re-derive the outlier draft's 51,557-series figure (reconciliation closed pending source check).

---

### Related Notes / Typed Links

> Plain wikilinks below are candidates—wire them to existing vault notes or create stubs.

- `instance_of` → [[Cardinality]], [[Series Churn]]
- `prerequisite_of` → [[Adaptive Metrics]] (this audit assumes it's active)
- `related_to` → [[Grafana Alloy]], [[Loki Structured Metadata]], [[ArgoCD GitOps]], [[FTFL-638]]
- `contrasts_with` → classic Prometheus `metric_relabel_configs` (no River equivalent)
