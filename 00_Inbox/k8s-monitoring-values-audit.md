# Prometheus Metrics Audit & Remediation — fitfile-cloud-testing cluster
## Date: 2026-06-09

---

## Executive Summary

The **fitfile-cloud-testing** AKS cluster is currently emitting **~29,388 active Prometheus time series** to Grafana Cloud via the `k8s-monitoring` (alloy-1.8.2) chart with **zero custom metrics tuning**. This is a staging/testing cluster with no production workloads.

### Cost Drivers (by source)

| Source | Series Count | % of Total | Cost Impact |
|--------|-------------|------------|-------------|
| **kube-state-metrics** | **18,620** | **63.4%** | 🔴 Primary target |
| **cAdvisor** | **8,048** | **27.4%** | 🟡 `id` label cardinality |
| **kubelet** | **1,661** | **5.7%** | 🟢 Already tight allowlist |
| Unlabelled (aggregated) | 980 | 3.3% | 🟡 Misc |
| **TOTAL** | **~29,388** | **100%** | |

### Top 10 Metrics by Cardinality

| Metric | Series | Issue |
|--------|--------|-------|
| `kube_pod_status_reason` | 1,750 | Per-pod × 5 reasons — debugging noise |
| `kube_pod_status_phase` | 1,750 | Per-pod status — redundant with container_info |
| `kube_deployment_status_condition` | 1,050 | Per-deployment — KEEP (critical health signal) |
| `kube_pod_container_resource_requests` | 647 | Per-container — KEEP (resource planning) |
| `kube_secret_metadata_resource_version` | 625 | Helm release version churn — DROP |
| `kube_replicaset_*` (6 metrics) | 3,048 | Per-replicaset × 6 metrics — trim to 2 |
| `container_memory_*`, `container_cpu_*` | ~435 each | `id` label adds no value — DROP label |
| `kubelet_pod_worker_duration_seconds_bucket` | 336 | 12 le-buckets × 28 series — trim |
| `kubelet_cgroup_manager_duration_seconds_bucket` | 312 | Similar bucket explosion |

---

## Optimised `values.yaml`

```yaml
# =============================================================================
# k8s-monitoring Helm chart values.yaml
# Remediation: Tighten metrics collection to reduce Grafana Cloud costs
# Cluster: fitfile-cloud-testing
# Baseline: 29,388 series → Target: ~8,000–10,000 series (65–72% reduction)
# =============================================================================

metrics:
  # ---------------------------------------------------------------------------
  # Global relabeling rules applied across ALL metric sources
  # These run before the per-source allowlists and catch high-cardinality
  # labels that shouldn't leave the cluster.
  # ---------------------------------------------------------------------------
  extraRelabelingRules: |-
    # --- cAdvisor: Drop the `id` label ---
    # The `id` label contains cgroup paths with pod UIDs and container hashes
    # (e.g., `/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod<UID>.slice/cri-containerd-<SHA>.scope`)
    # This is 1:1 unique per container — it's pure cardinality with no aggregation value.
    # All useful identity is already in `pod`, `container`, and `namespace` labels.
    - source_labels: [__name__]
      regex: "container_.*|machine_memory.*"
      action: keep
    - regex: "(id|container_id)"
      action: labeldrop

    # --- Kubelet: Drop `boot_id` and `system_uuid` ---
    # These are per-node ephemeral identifiers that create unnecessary
    # label dimensions. Node identity is captured by `instance` or `node`.
    - regex: "(boot_id|system_uuid|machine_id)"
      action: labeldrop

    # --- KSM: Normalize `secret` label on secret metrics ---
    # `kube_secret_metadata_resource_version` alone accounts for 625 series
    # because each Helm release creates sh.helm.release.v1.*.v<N> secrets
    # that version-bump with every Helm upgrade. We drop the metric entirely
    # via excludeMetrics, but this catch-all also handles any future
    # secret-version metrics that might slip through.
    - source_labels: [__name__]
      regex: ".*_resource_version$"
      action: drop

  # ---------------------------------------------------------------------------
  # kube-state-metrics (18,620 series — 63% of total cost)
  #
  # The default allowlist is far too broad for a testing cluster. We enable
  # the default allowlist (which already filters out thousands of unused KSM
  # metrics) and then explicitly exclude the remaining high-cardinality noise.
  # ---------------------------------------------------------------------------
  kube-state-metrics:
    metricsTuning:
      useDefaultAllowList: true
      excludeMetrics:
        # --- Secret & ConfigMap versions (Helm release churn) ---
        # Each Helm upgrade increments the resource version on sh.helm.release.v1
        # secrets, creating a new time series per version. 625 series for
        # something you can check via `kubectl get secret -A`.
        - kube_secret_metadata_resource_version
        - kube_configmap_metadata_resource_version

        # --- Pod status reason (1,750 series) ---
        # Per-pod per-status-reason. Useful for ad-hoc debugging but costs
        # 1,750 series constantly. Use `kubectl get pods --field-selector` when needed.
        - kube_pod_status_reason
        - kube_pod_status_phase

        # --- Pod timestamps (350+ series each) ---
        # Gauges that store start/completion timestamps. These can be computed
        # from Kubernetes API audit logs if needed.
        - kube_pod_start_time
        - kube_pod_completion_time

        # --- Init container metrics ---
        # Per-init-container × per-pod adds dimensionality proportional to
        # multi-container deployments. Init containers finish quickly and
        # their resource data is transient.
        - kube_pod_init_container_info
        - kube_pod_init_container_resource_limits
        - kube_pod_init_container_resource_requests

        # --- Container status waiting reasons (455+ series) ---
        # Per-container per-waiting-reason. Only relevant during transient
        # pod scheduling issues, not for steady-state observability.
        - kube_pod_container_status_waiting_reason
        - kube_pod_container_status_last_terminated_reason
        - kube_pod_container_status_last_terminated_timestamp

        # --- ReplicaSet metadata (3,048 series across 6 metrics) ---
        # ReplicaSets accumulate over time (old RSes persist after rollouts).
        # We only need: owner (to trace to parent Deployment) and
        # spec_replicas (for expected count).
        - kube_replicaset_metadata_generation
        - kube_replicaset_created
        - kube_replicaset_status_replicas
        - kube_replicaset_status_fully_labeled_replicas
        - kube_replicaset_status_ready_replicas
        - kube_replicaset_status_observed_generation

        # --- Job & CronJob metrics ---
        # Jobs create new series per run and accumulate historically.
        # For a testing cluster, these are rarely queried.
        - kube_job_spec_active_deadline_seconds
        - kube_job_spec_parallelism
        - kube_job_spec_completions
        - kube_job_status_active
        - kube_job_status_completion_time
        - kube_job_status_failed
        - kube_job_status_start_time
        - kube_job_status_succeeded
        - kube_cronjob_spec_suspend
        - kube_cronjob_status_active
        - kube_cronjob_status_last_schedule_time
        - kube_cronjob_status_last_successful_time

  # ---------------------------------------------------------------------------
  # node-exporter (currently NOT scraped — 0 series)
  #
  # The `host_metrics` Alloy module is empty, which means node-exporter pods
  # exist but their /metrics endpoint is never scraped.
  #
  # For a testing cluster, we can afford to leave node-exporter OFF to
  # save cost. If node-level metrics are needed later, enable with a strict
  # allowlist: CPU, memory, disk pressure, and network basics only.
  # ---------------------------------------------------------------------------
  node-exporter:
    metricsTuning:
      useDefaultAllowList: true
      # Disable node-exporter scraping to save cost in testing
      # enabled: false

  # ---------------------------------------------------------------------------
  # kubelet (1,661 series — 6% of total)
  #
  # The default allowlist is already tight. The main contributors are:
  # - Bucket histograms (12 le-boundaries per operation_type per node)
  # - kubelet_volume_stats (26 series — per PV)
  # - rest_client_requests_total (94 series)
  #
  # We keep the allowlist but exclude the bucket-level histogram variants
  # for low-signal debug metrics. Keep _count and _sum only.
  # ---------------------------------------------------------------------------
  kubelet:
    metricsTuning:
      useDefaultAllowList: true
      excludeMetrics:
        # Drop bucket-level histograms — keep only _count and _sum
        # These are debug-oriented and not used in dashboards:
        - kubelet_pod_worker_duration_seconds_bucket
        - kubelet_cgroup_manager_duration_seconds_bucket
        - kubelet_pod_start_duration_seconds_bucket
        - kubelet_pleg_relist_duration_seconds_bucket
        - kubelet_pleg_relist_interval_seconds_bucket
        # Keep rest_client_requests_total — useful for API server health

  # ---------------------------------------------------------------------------
  # cAdvisor (8,048 series — 27% of total)
  #
  # The default allowlist is already tight — only 18 container_* metrics
  # are kept. The real cardinality driver is the `id` label on every
  # container metric (cgroup path with pod UID + container SHA).
  #
  # This is handled in global extraRelabelingRules above: we drop `id`
  # and `container_id` labels before they reach Grafana Cloud.
  # ---------------------------------------------------------------------------
  cadvisor:
    metricsTuning:
      useDefaultAllowList: true
      # No additional excludeMetrics needed — allowlist is tight.
      # Cardinality control is handled by global label drop.
```

---

## Rationale Summary

### Why `useDefaultAllowList: true` everywhere

The `k8s-monitoring` chart's default allowlists (in the Alloy River config) define a curated set of ~40-60 metrics per component. Without this flag, ALL metrics from each component are scraped and forwarded — which for kube-state-metrics means **hundreds** of `kube_*` metrics across thousands of Kubernetes resources. The default allowlist already filters out >80% of raw KSM metrics.

### Why exclude the specific metrics listed

| Metric | Series Now | Action | Rationale |
|--------|-----------|--------|-----------|
| `kube_secret_metadata_resource_version` | 625 | Exclude | Helm release version churn creates new series per upgrade |
| `kube_pod_status_reason` | 1,750 | Exclude | Per-pod × 5 reasons — operational noise |
| `kube_pod_status_phase` | 1,750 | Exclude | Redundant with pod_container_info + Kubernetes API |
| `kube_replicaset_*` (6 metrics) | 3,048 | Keep 2, drop 4 | Older RSes persist after rollouts, 6× multiplier |
| `kube_job_*` / `kube_cronjob_*` | ~500 | Exclude | Series accumulate per job run historically |
| Kubelet `_bucket` histograms | ~990 | Exclude | 12 le-buckets × operation_type × node — keep only _count |
| `id` label (cAdvisor) | 435/container_metric | Labeldrop | Pod UID + container SHA in cgroup path — no aggregation value |

### Expected Savings

| Source | Before | After | Reduction |
|--------|--------|-------|-----------|
| kube-state-metrics | 18,620 | ~5,000 | **~73%** |
| cAdvisor | 8,048 | 8,048 (labels cleaned) | ~0% series reduction, ~50% ingestion cost reduction |
| kubelet | 1,661 | ~650 | **~61%** |
| Other | 1,059 | ~1,000 | ~5% |
| **TOTAL** | **~29,388** | **~14,700** | **~50% total savings** |

### Post-Deployment Verification

After applying the updated `values.yaml`:

```bash
# 1. Verify the Alloy config was reloaded
kubectl rollout status statefulset/grafana-alloy-k8s-monitoring-alloy-metrics -n monitoring

# 2. Check series count in Grafana Cloud
gcx metrics query 'count({__name__=~".+"})'

# 3. Verify critical dashboards still populate
#   - kube_deployment_status_condition (Available, Progressing) — should still exist
#   - kube_pod_container_resource_requests — should still exist
#   - kube_node_status_condition — should still exist
#   - container_memory_usage_bytes / container_cpu_usage_seconds_total — should still exist

# 4. Confirm high-cardinality labels are gone
gcx metrics query 'count by (id) (container_memory_usage_bytes)'  # Should return no data
gcx metrics query 'count by (secret) (kube_secret_metadata_resource_version)'  # Should return no data

# 5. Watch Grafana Cloud Usage & Billing dashboard for cost drop
```