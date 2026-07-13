---
chart: k8s-monitoring 4.1.3 (alloy 1.8.1, Alloy app v1.16.1)
cluster: testing
created: 2026-06-04T00:00:00+00:00
modified: 2026-07-13T08:44:41+00:00
permalink: llmeon/30-library/200-projects/grafana-k8s-monitoring-v2
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
source: owl-audit-agent — consolidated from 4 audit drafts + Loki labels reference
  + Prometheus/Alloy Reference
stack: fitfiletest (Grafana Cloud, prometheus-prod-05-gb-south-0)
tags: [adaptive-metrics, alloy, audit, cardinality, grafana, kubernetes, labels, loki, monitoring, seedling, structured-metadata, testing-cluster]
ticket: FTFL-638
title: Grafana k8s-monitoring v2
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

## Structured Metadata (Non-indexed)

Non-indexed key–value pairs attached to individual log lines, not streams. Introduced in Loki 3.0 with OTLP-native support; sometimes called "non-indexed labels".

```logql
{app="payments"} | traceID="abc123xyz"
```

 - Stored alongside the log entry, not in the index.
 - Not used for stream selection—only post-ingest filtering.
 - Safe to be high-cardinality—no cardinality penalty.
 - Maps natively from OpenTelemetry trace/span/resource attributes.

## The Practical Difference

| Dimension | Labels | Structured metadata |
|:--- |:--- |:--- |
| Indexed? | Yes | No |
| Query stage | Stream selection (fast) | Post-ingest filter (slower) |
| Cardinality risk | High—too many unique values = index explosion | Low—safe for high-cardinality |
| Scope | Entire stream | Individual log lines |
| Storage cost | Index overhead per unique combo | Inline with entry, no index overhead |
| Typical values | env, app, region, namespace | traceID, spanID, userID, requestID |
| OTel native? | Partial | Yes—OTLP resource/span attributes map here | <br> ### When to Use Each
| Use labels when… | Use structured metadata when… |
|:--- |:--- |
| Cardinality is low and stable (e.g. env ∈ {dev, staging, prod}) | Cardinality is high or unbounded (traceID, userID, requestID) |
| You need fast stream selection (always filtering app="payments") | Data originates from OpenTelemetry |
| You own the schema (deliberate architectural choice at ingest) | You want to correlate logs ↔ traces (carry trace_id/span_id) |
| Routing/retention depends on it (ruler, compactor, retention) | The field is useful for filtering but not routing |

## Common Pitfall

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

A well-designed Loki setup uses 3–6 low-cardinality labels (app, env, namespace, cluster) and pushes everything else—OTel attributes, request IDs, trace correlation—into structured metadata.

## In Prometheus / Mimir

Same principle, different mechanism: every unique label combination is a new time series. Prometheus has no native structured-metadata equivalent (3.x adds native histograms and OTLP resource attributes, but labels remain the cardinality driver). Rule is identical: keep label values low-cardinality; never label on requestID or userID.

For a monitoring system, every time series and sample has both a resource cost and a human cost. If you have more than one expanding label on a metric, the impact is compounded, resulting in a combinatorial explosion of time series. The strict rule of thumb is that the cardinality of an arbitrary metric on one application instance should be kept below 10.

## War story—FTFL-638 (The Lesson that Motivates the sTandard)

During debugging of fitfile-cloud-testing-aks-cluster under ticket FTFL-638, the pod field was being written into Loki's structured_metadata block by the default chart config—which strips it from the stream labels, rendering it unusable as an indexed selector ({pod="…"} stops working).

> [!warning] Collector self-collision
> A collector must not write the same field to both the indexed stream labels and structured metadata. If pod: pod is active in Loki's structured_metadata, it is removed from stream labels—breaking direct selector filters. Keep pod indexed only if you select streams by pod name, and in that case it must not also appear in structured metadata.

Fix validated on the testing cluster on 26 May: formatting job as namespace/container (e.g. testing/mongodb, testing/ffcloud-service) to prevent index collisions.

## Part 2—Recommended Label & Metadata Taxonomy

A unified, two-tier governance model applied across all namespaces (thehyve, argocd, monitoring, …).

### The Two Tiers

| Tier | Holds | Goes in | Constraint |
|:--- |:--- |:--- |:--- |
| Indexing layer | Low-cardinality, static identifiers | Kubernetes labels | Drives scheduling, ingress, replication, observability indices—must stay low-card |
| Metadata layer | High-cardinality, dynamic, or sensitive data | Annotations + Loki/OTel structured metadata | Prevents bloat in etcd, Prometheus TSDB, and Loki's stream index | <br> ### Standard Labels <br> Apply the Kubernetes recommended app.kubernetes.io/* set on every workload object (Deployment, Pod template, Service, ServiceMonitor, Ingress, ConfigMap), plus a small operational set.
| Label | Purpose | Example |
|:--- |:--- |:--- |
| app.kubernetes.io/name | Logical application identity | grafana-alloy, ffcloud-service, spicedb |
| app.kubernetes.io/instance | Unique deployed instance / Helm release | grafana-alloy-prod, fitconnect-dev-a |
| app.kubernetes.io/version | App / chart / image version | "v1.9.1" |
| app.kubernetes.io/component | Architectural tier | telemetry-agent, backend, frontend, database |
| app.kubernetes.io/part-of | Parent business platform | observability-platform, clinical-linkage |
| app.kubernetes.io/managed-by | Deployment driver | Helm, ArgoCD |
| environment | Logical environment zone | testing, staging, prod |
| team | Owning cohort for triage | platform-observability, clinical-sre |
| owner | Accountable owner | platform-observability |
| cost-center | Cost allocation | observability |
| criticality | Alert-routing tier | high / medium / low | <br> > To avoid collisions with third-party labels, optionally prefix the operational set DNS-style: yourcompany.com/environment, yourcompany.com/cost-center, etc. <br> > <br> Repeat the high-level ownership + cost + criticality labels on namespaces and use node-pool labels for scheduling only (nodepool-type, workload-type). <br> ### Selector Stability Rules <br> spec.selector.matchLabels is immutable once a workload exists—changing it requires recreation. <br> * DO use only stable logical identifiers in selectors: <br> app.kubernetes.io/name, app.kubernetes.io/instance, app.kubernetes.io/component. <br> * DO NOT put rolling variables in selectors or pod-template labels: <br> Git SHAs, release/container tags, build IDs, deployment timestamps. <br> ### Annotations (Kubernetes level) <br> Richer context for CI/CD, runbooks, and automation—never used as selectors.
| Annotation | Holds |
|:--- |:--- |
| yourcompany.com/repository | Git source URL |
| yourcompany.com/runbook-url | On-call triage page |
| yourcompany.com/slack-channel | On-call contact channel |
| yourcompany.com/git-sha / /build-id | Build provenance |
| yourcompany.com/last-deployed-at | ISO deploy timestamp |
| yourcompany.com/config-checksum | ConfigMap/Secret hash (triggers rolling restarts) | <br> ### Structured Metadata / OTel Resource Attributes (observability level) <br> Map Kubernetes metadata into stable resource attributes; do not promote all of them to metric/log labels.
| Index block (indexed stream labels) | Structured-metadata block (non-indexed) |
|:--- |:--- |
| cluster | pod _(indexed only if you select by it—then keep it out of structured metadata)_ |
| namespace | level (info/error) |
| container | caller, trace_id, span_id |
| job = namespace/container (e.g. testing/mongodb) | client_ip, user_id |
|  | build_id, version |

Recommended OTel resource attributes for indexing/grouping (the stable subset only): service.name, service.namespace, deployment.environment.name, k8s.cluster.name, k8s.namespace.name, team, cost_center, criticality.

### What NOT to Put in Labels

If Alloy forwards Kubernetes metadata into metrics/logs/traces, these become index dimensions and/or leak into dashboards, alerts, and billing exports:

```text
pod-name      pod-uid       container-id   image-digest
git-sha       build-id      request-id     session-id
user-id       email         customer-name  ticket-id
timestamp     full-url      ip-address     secret-name      token
```

Keep these as log fields / OTel attributes only. Using labeldrop is specifically recommended when you want to drop arbitrary metadata labels (such as container_label_.* from cAdvisor) without needing to know their exact names in advance.

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
    [yourcompany.com/repository](https://yourcompany.com/repository): "[https://gitlab.com/fitfile/deployment](https://gitlab.com/fitfile/deployment)"
    [yourcompany.com/runbook-url](https://yourcompany.com/runbook-url): "[https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1)"
    [yourcompany.com/slack-channel](https://yourcompany.com/slack-channel): "#clinical-alerts"
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
        [yourcompany.com/git-sha](https://yourcompany.com/git-sha): "cae7da9d8c0147ba82b775fc99b3df8d"
        [yourcompany.com/last-deployed-at](https://yourcompany.com/last-deployed-at): "2026-06-04T10:42:11+01:00"
        [yourcompany.com/config-checksum](https://yourcompany.com/config-checksum): "sha256:d8c4d39eada24257aff6e8403730"
    spec:
      containers:
        - name: fitconnect
          image: fitfile-registry.azurecr.io/fitconnect:v2.4.0
```

### Alloy Helm Values Pattern

Grafana Alloy is an open-source distribution of the OpenTelemetry Collector that is 100% OTLP compatible and offers native pipelines for OpenTelemetry and Prometheus telemetry formats. It natively uses a configuration language called River to define how telemetry data is collected and processed.

Use the chart's label-extension fields (keys vary by chart version—confirm with helm show values grafana/alloy).

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
  [yourcompany.com/repository](https://yourcompany.com/repository): "github-org/platform-observability"
  [yourcompany.com/runbook](https://yourcompany.com/runbook): "observability/grafana-alloy"
  [yourcompany.com/oncall](https://yourcompany.com/oncall): "platform-observability"
  [yourcompany.com/deployment-method](https://yourcompany.com/deployment-method): "helm"
```

## Part 3—testing Cluster Audit (2026-06-04)

> Scope: grafana/k8s-monitoring v4.1.3 on the testing AKS cluster (fitfile-cloud-testing-aks-cluster), shipping to Grafana Cloud stack fitfiletest. A small, already well-tuned estate (~9k active series). No runaway-cardinality emergency. Findings are efficiency/correctness wins—the largest is a config bug (node-exporter producing zero metrics).

### Executive Summary

| Field | Value |
|:--- |:--- |
| Chart version | 4.1.3 (k8s-monitoring) · alloy chart 1.8.1 · Alloy app v1.16.1 |
| Release | grafana-k8s-monitoring (umbrella, applied by ArgoCD, not helm install) |
| Sub-releases | …-alloy-metrics, …-alloy-logs, …-alloy-events |
| Namespace | monitoring |
| Cluster / Cloud | AKS UK South, K8s v1.34.7, 2× Standard_E4s_v5 (system pool) |
| Cluster label | cluster="testing" |
| Total active series | ~8,952 (consensus of 3 drafts; range 8,952–8,981) |
| Distinct label names | 313 · log labels: 15 |
| High-entropy labels | 4—id, name (cAdvisor) · uid, container_id (KSM) |
| Config bug | node-exporter runs on every node but 0 host metrics reach Cloud |
| Realistic active-series cut | ~6–9% immediate + large churn/index reduction from high-entropy drops | <br> ### Priority Action List (merged, deduped)
| # | Priority | Action | Effect | Data-loss risk |
|:--- |:--- |:--- |:--- |:--- |
| 1 | BUG / HIGH | node-exporter DaemonSet runs but host_metrics block renders empty → node_cpu__, node_filesystem__, node_network__, node_memory__ all = 0 series. Wire host metrics _or_ disable the DaemonSet to reclaim per-node CPU/mem | 0 series today (nothing collected); frees resources if disabled | None (you have nothing) |
| 2 | QUICK WIN | Drop kube_pod_status_reason via KSM allowlist exclusion | −470 series (~5.2%); 468/470 permanently 0 | Low (eviction _reason_ counts; phase still covered) |
| 3 | HIGH (entropy) | labeldrop id on cAdvisor (208-value cgroup path on ~2,206 series) | Negligible instantaneous; large churn/index cut | None (redundant w/ pod+container) |
| 4 | HIGH (entropy) | labeldrop name on cAdvisor (206-value container hash on ~2,206 series) | As above | None (redundant w/ container) |
| 5 | HIGH (entropy) | labeldrop container_id on KSM kube_pod_container_info/…_init_… (135 values) | Removes restart churn | Low (only breaks container_id joins—uncommon) |
| 6 | MEDIUM | Evaluate uid (pod UUID; 95 current / ~220 across 45 KSM metrics, ~2,875 series) for Adaptive Metrics aggregation or labeldrop | Removes churn on KSM pod metrics | Medium—some Grafana mixins join on uid. Validate before applying. |
| 7 | LOW | Remove duplicate k8s_cluster_name external label (identical to cluster, on ~8,675 series) | Label-bytes saving on nearly every series | None—confirm no dashboard/alert queries it first |
| 8 | LOW | labeldrop boot_id/system_uuid globally on cAdvisor (currently only set to NA on machine_memory_bytes) | Removes 6 stray distinct values | None (node-level dupes of node) |
| 9 | MEDIUM | Recording rules for container_* without image (74 distinct, grows over time) for dashboards that don't need image-level granularity | Reduces query-time cardinality | Low (raw data retained) |
| 10 | LOW (future) | Review open-ended OTel annotation labelmap __meta_kubernetes_pod_annotation_resource_opentelemetry_io_(.+)—future cardinality risk if devs inject dynamic annotations | Preventative | n/a |
| 11 | OPERATIONAL | Resolve alloy-logs-fsb5q Pending (one node not shipping logs) | Restores per-node log coverage | n/a | <br> ### Discovery
| Item | Value |
|:--- |:--- |
| RELEASE_NAME | grafana-k8s-monitoring |
| NAMESPACE | monitoring |
| CHART_VERSION | 4.1.3 (confirmed 4.x) |
| GitOps | ArgoCD app grafana-k8s-monitoring in ns argocd—no Flux HelmRelease CRD present |
| Sub-chart revs | alloy-events (rev 2), alloy-logs (rev 11), alloy-metrics (rev 4) | <br> Pod inventory (monitoring ns):
| Pod | Type | Status | Restarts | Age |
|:--- |:--- |:--- |:--- |:--- |
| …-alloy-events-6bc7658f54-rk9d6 | Deployment | Running | 1 | 14h |
| …-alloy-logs-w692p | DaemonSet | Running | 1 | 5h |
| …-alloy-logs-fsb5q | DaemonSet | Pending | 0 | 5h |
| …-alloy-metrics-0 | StatefulSet | Running | 1 | 14h |
| …-alloy-operator-df4fb5cff-rc49j | Deployment | Running | 0 | 14h |
| …-kube-state-metrics-76d5575c89-d78l5 | Deployment | Running | 0 | 14h |
| …-node-exporter-d25gv / -hqjhj | DaemonSet | Running | 0 | 5h |
| …-opencost-76475d9f45-zgpq5 | Deployment | Running | 0 | 14h | <br> > [!warning] Pending pod (Issue 11) <br> > alloy-logs-fsb5q is unschedulable: 0/2 nodes available: 1 Insufficient cpu, 1 didn't satisfy NodeAffinity. Capacity/scheduling, not config. One logs collector (w692p) is healthy. Add capacity or relax the DaemonSet's node constraints for full per-node coverage. <br> > ```bash <br> > kubectl describe pod grafana-k8s-monitoring-alloy-logs-fsb5q -n monitoring <br> > <br> > ``` <br> > <br> ### Current Config <br> Values pulled from the ArgoCD Application (.spec.source.helm.values); rendered Alloy (River
