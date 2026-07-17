---
tags:
- fitfile
- grafana
- prometheus
- kube-state-metrics
- observability
- sandbox-testing
date: 2026-07-17
project: Sandbox Stress-Test Dashboards & Observability
todoist_task: https://app.todoist.com/app/task/6h6Ff2jhQX8vmW5F
permalink: llmeon/work/kube-pod-labels-metrics-plan-sandbox-stress-test-observability
---

# kube_pod_labels Metrics Plan

Full investigation and plan for getting `kube_pod_labels` (and `kube_namespace_labels`) flowing into Grafana Cloud Prometheus on `sandbox-testing-1`/`-2`. This is the metrics-side half of the join key needed for the [Argo Workflow instance drill-down dashboard](https://app.todoist.com/app/task/6h6FcvqcW7gGW6wm) — once workflows-api stamps `ffcloud.io/instance-id` on step pods, this metric is how it becomes queryable in Prometheus (as `label_ffcloud_io_instance_id`).

## Why this metric specifically

Source: [kube-state-metrics pod-metrics.md](https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md)

> `kube_pod_labels` — "Kubernetes labels converted to Prometheus labels"; labels: `pod`, `namespace`, `label_POD_LABEL`, `uid`

Any Kubernetes pod label automatically becomes a `label_<name>` dimension on this one metric. It's the only kube-state-metrics metric that exposes arbitrary pod labels as queryable Prometheus label values — which is exactly the mechanism needed to filter CPU/memory metrics down to one Argo Workflow instance once the instance-id label exists on step pods.

## Full audit: doc vs. live status

Checked every metric on the pod-metrics.md page against `sandbox-testing-1`/`-2` via `gcx metrics query -d grafanacloud-prom 'count({__name__=~"kube_pod_.*"}) by (__name__)' --since 168h`.

**59 metrics documented upstream. 27 currently flow. 32 are absent.**

Most of the 32 absent ones are *intentionally* excluded by the k8s-monitoring Helm chart's default 44-metric allow-list (things like `kube_pod_tolerations`, `kube_pod_resourceclaim_info`, per-init-container timestamp metrics) and don't matter for this project. The one that does matter — `kube_pod_labels` — is also absent, along with its namespace equivalent `kube_namespace_labels`.

### Currently flowing (27)
```
kube_pod_completion_time                          kube_pod_init_container_status_restarts_total
kube_pod_container_info                           kube_pod_init_container_status_running
kube_pod_container_resource_limits                kube_pod_init_container_status_terminated
kube_pod_container_resource_requests               kube_pod_init_container_status_terminated_reason
kube_pod_container_status_last_terminated_reason  kube_pod_init_container_status_waiting
kube_pod_container_status_last_terminated_timestamp kube_pod_init_container_status_waiting_reason
kube_pod_container_status_restarts_total          kube_pod_owner
kube_pod_container_status_running                 kube_pod_restart_policy
kube_pod_container_status_terminated_reason       kube_pod_spec_volumes_persistentvolumeclaims_info
kube_pod_container_status_waiting_reason          kube_pod_start_time
kube_pod_info                                     kube_pod_status_phase
kube_pod_init_container_info                      kube_pod_status_reason
kube_pod_init_container_resource_limits
kube_pod_init_container_resource_requests
kube_pod_init_container_status_ready
```

### Needed and absent
- `kube_pod_labels` — **the target metric**
- `kube_namespace_labels` — same mechanism, needed if namespace-level labeling is ever used as a join key too

## Root-cause investigation

### Ruled out: chart-version schema mismatch
Pulled the actual `grafana/k8s-monitoring-helm` source at the exact pinned tag (`k8s-monitoring-4.1.6`, per `charts/ffnode/values.yaml:515`) via `gh api`.

- `clusterMetrics` is a genuine Helm alias for the `feature-cluster-metrics` subchart (`Chart.yaml:37-41`), so `clusterMetrics.kube-state-metrics.metricsTuning.includeMetrics` set in `charts/ffnode/templates/_grafana.tpl:211-228` lands exactly where `charts/feature-cluster-metrics/templates/_kube_state_metrics.alloy.tpl` reads it (`index .Values "kube-state-metrics").metricsTuning.includeMetrics`).
- That template concatenates `includeMetrics` onto the chart's built-in 44-item `default-allow-lists/kube-state-metrics.yaml` and applies the merged list as a Prometheus `keep` relabel rule on `__name__`, before `forward_to = argument.metrics_destinations.value` (i.e. before remote-write to Grafana Cloud).
- `kube_pod_labels` and `kube_namespace_labels` are correctly present in `_grafana.tpl:225-226`'s `includeMetrics` list — the merged allow-list regex genuinely includes them.
- `kube-state-metrics.enabled` defaults to `true` in the subchart and isn't overridden to false anywhere.

**Conclusion: the cluster-side config is syntactically and semantically correct.** This retracts an earlier hypothesis (raised mid-investigation) that the config might be targeting a nonexistent schema path — it doesn't; it's wired correctly.

### Ruled out: ArgoCD sync drift
Queried `argocd_app_info{name="grafana-alloy-k8s-monitoring"}` live via `gcx metrics query`:

```
sync_status="Synced", health_status="Healthy"   (sandbox-testing-1, staging, testing)
```

The config is actually deployed, not sitting unsynced.

### REFUTED: Grafana Cloud Adaptive Metrics
Original hypothesis (below, struck through) has been checked directly and disproven.

~~With both the config and its deployment confirmed correct, the only remaining layer is server-side — Adaptive Metrics can aggregate away or fully drop a metric post-ingestion, independent of what Alloy sends to remote-write.~~

**2026-07-17 update**: got an org-level Grafana Cloud Access Policy token authenticated (`stacks:read`, `adaptive-metrics-config:read`, `adaptive-metrics-rules:read`, `adaptive-metrics-exemptions:write`, realm `fitfile (all stacks)`). Queried every active rule directly:

```
gcx metrics adaptive rules list --limit 0 -o json
→ 5,453 rule(s)
```

Filtered for `kube_pod_labels`, `kube_namespace_labels`, and (for the sibling investigation) `argo_workflows_*`: **zero matches for any of the three.** Rules are the actually-enforced mechanism — recommendations are unapplied suggestions and don't affect what's dropped — so this is conclusive: Adaptive Metrics is not touching either metric, and the sibling finding ("Raise with Grafana Cloud owner: adaptive metrics stripping labels off `argo_workflows_*`", Todoist `6h5ccJfq9wVQWG9F`) has been reopened as unconfirmed/likely wrong for the same reason.

For context, 9 other `kube_pod_*` metrics *do* have active rules (e.g. `kube_pod_restart_policy`, `kube_pod_init_container_status_running`), all dropping label sets like `k8s_cluster_name`/`container` via `sum`/`count` aggregations — confirming rules aggregate labels away rather than delete metrics outright, and that the rules endpoint is working correctly and would show a match if one existed.

### ROOT CAUSE CONFIRMED: kube-state-metrics' own `--metric-labels-allowlist` flag
Got direct cluster access via `bastion-tunnel.sh` (Azure Bastion tunnel → isolated kubeconfig → `aks-ff-uks-gp-1`, the `sandbox-testing-1` cluster) and went straight to the source, bypassing Alloy and Grafana Cloud entirely.

Port-forwarded to the `kube-state-metrics` pod itself and curled its own `/metrics`:
```
curl http://127.0.0.1:8081/metrics | grep -c '^kube_pod_labels'
→ 0
```
Zero series **at the source** — not an Alloy or Grafana Cloud problem at all. For comparison, `kube_pod_info` on the same endpoint has 84 series, so the scrape endpoint itself is healthy; this one metric specifically is never emitted.

Checked the pod's actual container args:
```
--metric-labels-allowlist=nodes=[agentpool,alpha.eksctl.io/cluster-name,...,topology.kubernetes.io/zone]
```
Only `nodes` is allow-listed. Per kube-state-metrics' own documented behavior (`prometheus-community/helm-charts` kube-state-metrics chart, `values.yaml`): a resource absent from `metricLabelsAllowlist` gets **zero series** for its `kube_<resource>_labels` metric — the whole family is suppressed at the source, not just missing `label_*` dimensions. `pods` and `namespaces` were never in this list.

Traced where the `nodes`-only default comes from: **not set anywhere in this deployment repo** (confirmed via repo-wide grep — zero matches for `metric-labels-allowlist`/`metricLabelsAllowlist`). It's a hardcoded default in the upstream chart itself: `grafana/k8s-monitoring-helm`, `charts/k8s-monitoring/charts/telemetry-services/values.yaml:82-83` (pinned version `k8s-monitoring-4.1.6`):
> `kube_<resource>_labels` metrics to generate. The default is to include a useful set for Node labels.

By design, upstream never allow-lists pod/namespace labels by default — this repo simply never overrode it.

**This supersedes every earlier theory**: not a chart schema mismatch, not ArgoCD sync drift, not Adaptive Metrics. All three were legitimately ruled out along the way, but none was *the* answer. The `clusterMetrics.kube-state-metrics.metricsTuning.includeMetrics` change from commit `46642843` was never going to work on its own — that only controls Alloy's post-scrape `keep` relabeling, which can't keep a metric kube-state-metrics never emitted. **Two separate mechanisms were needed, and only one was ever configured.**

## The fix

Add to `charts/ffnode/templates/_grafana.tpl` around line 162 (the `telemetryServices.kube-state-metrics` block):

```yaml
telemetryServices:
  kube-state-metrics:
    deploy: true
    metricLabelsAllowlist:
      - nodes=[agentpool,alpha.eksctl.io/cluster-name,alpha.eksctl.io/nodegroup-name,beta.kubernetes.io/instance-type,cloud.google.com/gke-nodepool,cluster-name,ec2.amazonaws.com/Name,ec2.amazonaws.com/aws-autoscaling-groupName,ec2.amazonaws.com/aws-autoscaling-group-name,ec2.amazonaws.com/name,eks.amazonaws.com/nodegroup,k8s.io/cloud-provider-aws,karpenter.sh/nodepool,kubernetes.azure.com/cluster,kubernetes.io/arch,kubernetes.io/hostname,kubernetes.io/os,node.kubernetes.io/instance-type,topology.kubernetes.io/region,topology.kubernetes.io/zone]
      - pods=[ffcloud.io/instance-id]
```

Important details:
- **Must re-list the full existing `nodes=[...]` entry too** — Helm replaces lists wholesale, it doesn't merge them. Setting `metricLabelsAllowlist` without the `nodes` entry would silently break OpenCost's existing node-label usage.
- **Use `pods=[ffcloud.io/instance-id]`, not `pods=[*]`** — the upstream chart's own comment warns `*` has "severe performance implications" since it allow-lists every label on every pod cluster-wide. Only the one instance-id label is needed, once it exists.
- This is still blocked on the [workflows-api instance-id label change](https://app.todoist.com/app/task/6h6Ff2fVr4pCP7fm) landing first — no point exposing `label_ffcloud_io_instance_id` if the label doesn't exist on any pod yet, though there's no harm in shipping this fix ahead of that.

## Plan

1. Add the `metricLabelsAllowlist` block above to `_grafana.tpl`, get it reviewed/merged.
2. Once deployed (ArgoCD sync), re-verify at the source the same way this was diagnosed: port-forward to `kube-state-metrics` and curl `/metrics` directly for `kube_pod_labels`.
3. Then verify it reaches Grafana Cloud:
   ```
   gcx metrics query -d grafanacloud-prom 'count({__name__=~"kube_pod_labels.*"})' --since 24h
   ```
   Should go from 0 to non-zero on `sandbox-testing-1`/`-2`.
4. Coordinate timing with the workflows-api `ffcloud.io/instance-id` label change — once both land, `kube_pod_labels{label_ffcloud_io_instance_id="..."}` becomes the working join key for the drill-down dashboard's metrics panel.
5. Separately, re-investigate the `argo_workflows_*` label-stripping finding with the same direct-cluster-access rigor — its Adaptive Metrics explanation was ruled out the same way this one's schema/sync/Adaptive-Metrics theories were, and the real answer is likely a similarly mundane KSM/Alloy config gap rather than anything server-side.

## Dependency chain back to the drill-down dashboard

```
workflows-api sets ffcloud.io/instance-id via spec.podMetadata.labels  [BLOCKING, external repo]
        │
        ▼
kube_pod_labels reaches Prometheus with label_ffcloud_io_instance_id   [this plan]
        │
        ▼
Per-container CPU/memory panel on the drill-down dashboard can filter
by $workflow_instance_id
```

Both branches (this one, and the Loki-side relabeling for step-pod logs) need to land before the drill-down dashboard's metrics panel can be built and tested against real data.

## References

- Todoist parent task: [Build Argo Workflow instance drill-down dashboard](https://app.todoist.com/app/task/6h6FcvqcW7gGW6wm)
- Todoist this investigation: [kube_pod_labels/kube_namespace_labels missing in Prometheus](https://app.todoist.com/app/task/6h6Ff2jhQX8vmW5F)
- Todoist related: [Raise with Grafana Cloud owner: adaptive metrics stripping labels off argo_workflows_*](https://app.todoist.com/app/task/6h5ccJfq9wVQWG9F)
- Chart config: `charts/ffnode/templates/_grafana.tpl:211-228` (this repo)
- Upstream chart source at pinned version: `github.com/grafana/k8s-monitoring-helm` @ `k8s-monitoring-4.1.6`
- Upstream metric docs: `github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md`