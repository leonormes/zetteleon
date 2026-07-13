---
created: 2026-06-05T00:00:00+00:00
modified: 2026-07-13T08:51:58+00:00
permalink: llmeon/30-library/200-projects/2026-06-05-fitfile-loki-prometheus-cardinality-audit
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
source: gcx CLI audit (fitfiletest context)
tags: [audit, cardinality, cost-optimisation, fitfile, grafana-cloud, loki, prometheus]
title: 2026-06-05-fitfile-loki-prometheus-cardinality-audit
type: null
---

## FITFILE—Loki & Prometheus Cardinality Audit

Scope: fitfiletest Grafana Cloud stack (`https://fitfiletest.grafana.net`)

Date: 2026-06-05

Note: fitfileprod context was not configured in `gcx config`—only fitfiletest was available. Prod analysis deferred.

---

### 1. Labels That Can Be DROPPED Immediately

#### Loki Indexed Labels

| Label              | Cardinality | Value(s)                                                                                                            | Reason                                                                                                                                           | Impact |
| ------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| `app_id`           | 1           | `58`                                                                                                                | Single value—zero selectivity                                                                                                                    | HIGH   |
| `app_key`          | 1           | `109e0418420b89be40f0584a782d733f`                                                                                  | Single value—zero selectivity                                                                                                                    | HIGH   |
| `flags`            | 1           | `F`                                                                                                                 | Always false—never used for filtering                                                                                                            | MEDIUM |
| `source`           | 1           | `kubernetes-events`                                                                                                 | Single value—zero selectivity                                                                                                                    | MEDIUM |
| `k8s_cluster_name` | 3           | `ollie, testing, yasir`                                                                                             | Subset of `cluster` (5: ollie, testing, staging, sandbox-testing-1, yasir). The 3 values are always identical to the same-named `cluster` value. | HIGH   |
| `level`            | 2           | `Info, Warning`                                                                                                     | Duplicates `detected_level` which is already in Structured Metadata. Indexed `level` adds cost with no benefit over SM.                          | MEDIUM |
| `stream`           | 2           | `stdout, stderr`                                                                                                    | Very low cardinality. Useful for filtering but could move to SM with minimal impact.                                                             | LOW    |
| `instance`         | 2           | `cluster_events.feature/loki.source.kubernetes_events.cluster_events, loki.source.kubernetes_events.cluster_events` | Alloy internal—not user-queryable.                                                                                                               | LOW    |

#### Loki Labels That Should Move To Structured Metadata

| Label | Cardinality | Reason | Impact |
|---|---|---|---|
| `pod` | 562 | Very high cardinality. Already known: should be SM per known context (testing cluster missing `pod: null` override). 562 unique pod names explode the index. Move to Structured Metadata. | HIGH |
| `container` | 308 (179 UUID + 129 real) | 58% of values are UUIDs—these are from containers without a proper `container` label in the k8s metadata. High cardinality with low query value. Move to SM. | HIGH |
| `reason` | 64 | Kubernetes event reasons (BackOff, FailedMount, etc.). Useful for filtering event logs but moderate-cardinality label. Consider SM for event streams. | MEDIUM |
| `service_name` | 323 (179 UUID + 144 real) | 55% UUIDs from historical streams (pods without `app.kubernetes.io/name`). The non-UUID values duplicate `app_kubernetes_io_name` (45 values). Move to SM to eliminate UUID index bloat. | HIGH |

#### Prometheus Labels

| Label | Cardinality | Reason | Impact |
|---|---|---|---|
| `container_id` | 47,016 | Unbounded—every container restart gets a new ID. Extreme index explosion. Must be dropped or added to a `drop` rule. | HIGH |
| `name` | 65,145 | Generic kube-state-metrics label. Likely mixed pod names, PVC names, secret names, etc. Extremely high cardinality with no selectivity for any single metric type. | HIGH |
| `pod` | 24,720 | kube-state-metrics `pod` label. Extremely high cardinality. Overlaps with `k8s_pod_name` (289) and `k8s_pod_uid` (289) and `pod_ip` (1,464). | HIGH |
| `uid` | 24,057 | Generic `uid` label from kube-state-metrics—unbounded, never useful for querying. | HIGH |
| `pod_ip` | 1,464 | IP addresses are unbounded resources. | HIGH |
| `workload` | 1,303 | Generic workload name—high cardinality, overlaps with `deployment`, `daemonset`, `statefulset`, etc. | MEDIUM |
| `system_uuid` | 437 | Node system UUID—unbounded per node but node count is small. Duplicates info already in `machine_id` (435). | MEDIUM |
| `machine_id` | 435 | Duplicates `system_uuid` (437). | MEDIUM |
| `image_id` | 286 | SHA256 digests—unbounded, duplicates info in `image` + `image_tag`. | MEDIUM |
| `image_tag` | 74 | High for Prometheus—often duplicates purpose of `image`. | LOW |
| `k8s_pod_name` | 289 | Duplicates `pod` (24,720). Keep `pod`, drop `k8s_pod_name`. | HIGH |
| `k8s_pod_uid` | 289 | Unbounded UUID. Drop entirely. | HIGH |
| `k8s_pod_ip` | 216 | IP addresses. Drop entirely (duplicated by `pod_ip` if kept, but both should go). | HIGH |
| `container_name` | 1 | Single value. Pointless. | MEDIUM |
| `boot_id` | 1 | Single value. Pointless. | MEDIUM |
| `app` | 1 | Single value. Pointless. | MEDIUM |
| `label_kubernetes_azure_com_os_sku` | 1 | Single value. | LOW |
| `label_kubernetes_azure_com_role` | 1 | Single value. | LOW |
| `label_app` (12) / `label_k8s_app` (12) | 12 each | Redundant. Likely identical values from different label sources. Keep one. | LOW |
| `label_kubernetes_*`—SKU, storageprofile, storagetier, etc. | 1–3 | Various Azure node labels with cardinality 1–3. Useful for node-level aggregation but 20+ separate `label_*` dimensions from Azure metadata. Consolidate or drop unused. | LOW |

---

### 2. Labels That Should Move To Structured Metadata

#### Loki

| Candidate | Current | Recommended | Reason |
|---|---|---|---|
| `pod` | Indexed label (562 values) | Structured Metadata | Index bloat—pod names change on every restart |
| `container` | Indexed label (308 values) | Structured Metadata | 58% UUIDs—no query value |
| `service_name` | Indexed label (323 values) | Structured Metadata | 55% UUIDs—duplicates `app_kubernetes_io_name` where meaningful |
| `reason` | Indexed label (64 values) | Structured Metadata | Only used for event filtering, not cardinality-critical |
| `stream` | Indexed label (2 values) | Structured Metadata | Low cardinality, rarely filtered independently |

#### Prometheus

Most Prometheus labels should be dropped, not moved—Prometheus has no structured metadata equivalent. Use `write_relabel_configs` or `drop` rules in the collector.

---

### 3. Fields To PROMOTE to Structured Metadata (Log Body)

Based on log sample analysis across clusters `testing` and `ollie`:

| Field | Found In | Current Location | Candidate For | Reason |
|---|---|---|---|---|
| `component` | ArgoCD logs body | Log JSON body (`.component`) | Structured Metadata | Low cardinality (~10 values across sampled logs), useful for filtering |
| `logger` | Tigera operator logs | Log JSON body (`.logger`) | Structured Metadata | Moderate cardinality, identifies log source |
| `requestID` | Spicedb logs | Log JSON body (`.requestID`) | Structured Metadata | High cardinality per-request—not recommended to promote |
| `grpc.service` | Spicedb logs | Log JSON body (`.grpc.service`) | Structured Metadata | Low cardinality, useful for filtering gRPC calls |
| `grpc.method` | Spicedb logs | Log JSON body (`.grpc.method`) | Structured Metadata | Moderate cardinality |
| `peer.address` | Spicedb logs | Log JSON body (`.peer.address`) | Structured Metadata | IP addresses—high cardinality, not recommended to promote |
| `namespace_name` | n/a | n/a (inferred from `namespace` label) | Already indexed | Already present as `namespace`—no action needed |
| `application` | MongoDB logs | Log JSON body (`.attr.doc.application.name`) | Structured Metadata | Low values (`mongosh 2.5.8`), useful if mongo audit logging is common |

Recommendation: Only promote low-cardinality filters (`component`, `logger`, `grpc.service`, `application`). Avoid promoting `requestID`, `peer.address`, or any UUID/IP field.

---

### 4. Adaptive Telemetry Opportunities

Status: Adaptive Logs and Adaptive Metrics APIs returned `401 Unauthorized`—the Grafana Cloud API token has expired. Re-authentication (`gcx login`) is needed to query adaptive telemetry.

Known opportunities (from observed data):

#### Adaptive Logs

- High-cardinality label drops: Instead of modifying the Alloy config to drop `pod`, `container`, `service_name` indices, use Adaptive Logs drop rules for streams where these labels add no value. This is a quick win without redeploying the collector.
- Pattern-based aggregation: The UUID `service_name` values (179 distinct UUIDs) are ideal adaptive log pattern candidates—they follow UUID patterns that can be aggregated into a single placeholder.

#### Adaptive Metrics

- Container ID and UID drops: `container_id` (47,016) and `uid` (24,057) are the biggest cost drivers. An Adaptive Metrics aggregation rule can drop these labels without touching the collector config.
- `name` label (65,145): Likely the single biggest Prometheus cardinality contributor. Apply a metric aggregation rule to drop `name` from all kube-state-metrics series.

---

### 5. Estimated Impact Summary

| Recommendation | Category | Impact | Effort |
|---|---|---|---|
| Drop `app_id`, `app_key` (Loki) | Label drop | HIGH—reduces index size immediately | Low—single config change |
| Drop `flags` (Loki) | Label drop | MEDIUM | Low |
| Drop `source` (Loki) | Label drop | MEDIUM | Low |
| Drop `k8s_cluster_name` (Loki) | Label drop | HIGH—eliminates redundant label | Low |
| Move `pod` to SM (Loki) | Label → SM | HIGH—biggest single index reduction | Low—fix values.yaml |
| Move `container` to SM (Loki) | Label → SM | HIGH—eliminates UUID index bloat | Low |
| Move `service_name` to SM (Loki) | Label → SM | HIGH—eliminates UUID index bloat | Low |
| Drop `container_id` (Prometheus) | Label drop | HIGH—eliminates 47K series explosion | Medium—relabel config |
| Drop `uid` (Prometheus) | Label drop | HIGH—eliminates 24K series explosion | Medium |
| Drop `pod_ip`, `k8s_pod_ip` (Prometheus) | Label drop | HIGH—eliminates IP-based explosion | Medium |
| Drop `k8s_pod_name`, `k8s_pod_uid` (Prometheus) | Label drop | HIGH—duplicate of `pod` | Medium |
| Drop `name` from kube-state-metrics (Prometheus) | Label drop | HIGH—eliminates 65K series explosion | Medium |
| Drop `image_id` (Prometheus) | Label drop | MEDIUM—286 values, redundant | Low |
| Drop single-value labels (Prometheus) | Label drop | MEDIUM—hygiene | Low |
| Promote `component`, `logger` to SM (Loki) | Body → SM | LOW—nice to have | Low |
| Re-auth for adaptive telemetry | Infrastructure | MEDIUM—enables zero-config changes | Low |

---

### 6. Recommended Alloy / values.yaml Changes

#### Loki—`grafana-k8s-monitoring` values.yaml (Testing cLuster)

```yaml
# Add under `logs` section:
logs:
  pod_logs:
    # Drop zero-selectivity indexed labels
    label_drop:
      - app_id
      - app_key
      - flags
      - source
      - k8s_cluster_name

    # Move high-cardinality labels to structured metadata
    structured_metadata:
      # Already set on testing, but ensure pod is NOT indexed:
      pod: null
      # Additional moves:
      container: {}
      service_name: {}
      reason: {}
      stream: {}
      
    # Confirm: drop indexed `level` (use detected_level from SM instead)
    # Note: `level` may be set by k8s-logging pipeline — override to drop
    label_drop_extra:
      - level
```

Note for testing cluster specifically: The known context says `pod` should already be in SM on testing due to a missing `pod: null` override. Verify by checking the current values.yaml—`pod` still shows 562 values in the label index, which means the override is NOT working or was never applied. This is still indexed and needs attention.

#### Prometheus—`grafana-k8s-monitoring` values.yaml

```yaml
# Add under `metrics` section:
metrics:
  kube-state-metrics:
    metric_relabel_configs:
      # Drop unbounded / high-cardinality labels from ksm
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: container_id
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: uid
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: name
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: pod_ip
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: k8s_pod_ip
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: k8s_pod_name
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: k8s_pod_uid
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: image_id
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: workload
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: system_uuid
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: machine_id
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: container_name
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: boot_id
      - source_labels: [__name__]
        regex: "kube_.*"
        action: labeldrop
        target_label: app

  node-exporter:
    metric_relabel_configs: []
    # Note: node_filesystem_device_error (663 series) and
    # node_filesystem_readonly (663 series) are high — check if
    # these are from the same source and can be deduplicated
```

#### Alloy-specific Loki Processing Stage

If using raw Alloy config instead of the Helm chart abstractions:

```json
loki.process "drop_redundant_labels" {
  stage.label_drop {
    values = ["app_id", "app_key", "flags", "source", "k8s_cluster_name", "level"]
  }
  
  stage.structured_metadata {
    # Move pod from indexed to SM
    pod = null
    
    # Promote log body fields
    component = ""
    logger = ""
  }
}
```

---

### 7. Data Summary Reference

#### Loki Stream Labels—fitfiletest

| Label | Cardinality | Notes |
|---|---|---|
| `app_kubernetes_io_name` | 45 | Meaningful service names—keep |
| `app_id` | 1 | DROP |
| `app_key` | 1 | DROP |
| `cluster` | 5 | Keep—primary cluster selector |
| `container` | 308 (179 UUID) | Move to SM |
| `deployment_environment` | 2 | Keep—useful filter |
| `flags` | 1 (F) | DROP |
| `instance` | 2 | DROP or move to SM |
| `job` | 396 | Keep—primary stream router |
| `k8s_cluster_name` | 3 | DROP—subset of `cluster` |
| `kind` | 4 | Keep for k8s events |
| `level` | 2 | DROP—use `detected_level` SM |
| `namespace` | 35 | Keep—essential filter |
| `pod` | 562 | Move to SM |
| `reason` | 64 | Consider moving to SM |
| `service_name` | 323 (179 UUID) | Move to SM |
| `service_namespace` | 24 | Keep—useful |
| `source` | 1 (kubernetes-events) | DROP |
| `stream` | 2 | Move to SM |

#### Prometheus Labels—fitfiletest

| Label | Cardinality | Recommendation |
|---|---|---|
| `container_id` | 47,016 | DROP |
| `name` | 65,145 | DROP |
| `pod` | 24,720 | Keep but drop from ksm metrics |
| `uid` | 24,057 | DROP |
| `pod_ip` | 1,464 | DROP |
| `workload` | 1,303 | DROP |
| `container` | 4,291 | Keep for cadvisor |
| `k8s_pod_name` | 289 | DROP—duplicate |
| `k8s_pod_uid` | 289 | DROP |
| `image_id` | 286 | DROP |
| `k8s_pod_ip` | 216 | DROP |
| `k8s_node_name` | 85 | Keep—node-level agg |
| `image_tag` | 74 | Keep |
| `system_uuid` | 437 | DROP—redundant |
| `machine_id` | 435 | DROP—redundant |
| `container_name` | 1 | DROP |
| `boot_id` | 1 | DROP |
| `app` | 1 | DROP |
| `host` | 6 | Keep |
| `hostname` | 2 | Keep or drop |
| `host_ip` | 26 | Keep—node IP is useful |
| `cluster` | 7 | Keep |
| `k8s_namespace_name` | 4 | DROP—duplicate of `namespace`? |
| `deployment_environment` | 2 | Keep |
| `level` | 2 | Keep |
| `kind` | 4 | Keep |
| `service_name` | 8 | Keep |
| `k8s_deployment_name` | 8 | Check—likely duplicate |
| `label_app` | 12 | Keep one, drop duplicates |
| `label_k8s_app` | 12 | Keep one, drop duplicates |

#### Top 10 Highest-Cardinality Metric Series

| Metric | Series Count | Driver Label(s) |
|---|---|---|
| `kube_pod_status_reason` | 1,930 | `pod` (24,720), `reason` |
| `kube_pod_status_phase` | 1,930 | `pod` (24,720), `phase` |
| `kube_deployment_status_condition` | 1,140 | `deployment`, `namespace` |
| `trivy_clusterrole_clusterrbacassessments` | 1,068 | Cluster-scoped |
| `node_filesystem_device_error` | 663 | `device`, `fstype` |
| `node_filesystem_readonly` | 663 | `device`, `fstype` |
| `kube_pod_container_resource_requests` | 658 | `pod`, `resource` |
| `kube_replicaset_created` | 531 | `replicaset`, `namespace` |
| `kube_replicaset_metadata_generation` | 531 | `replicaset`, `namespace` |
| `kube_replicaset_owner` | 531 | `replicaset`, `owner_kind` |

---

### 8. Quick Wins (Ordered by Impact)

1. Fix `pod: null` in structuredMetadata—single config line to move 562-cardinality pod label to SM
2. Drop `container_id`, `uid`, `name` from Prometheus ksm metrics—eliminates 136K+ series immediately
3. Drop `app_id`, `app_key`, `k8s_cluster_name` from Loki—three zero-cardinality labels eliminated
4. Re-auth `gcx login` for adaptive telemetry—enables zero-deploy cardinality management
5. Drop `k8s_pod_name`, `k8s_pod_uid`, `k8s_pod_ip`, `pod_ip`—eliminates redundancy in Prometheus
6. Move `container`, `service_name` to SM—eliminates UUID index bloat in Loki
7. Drop `image_id`, `workload`, `system_uuid`, `machine_id`—moderate cardinality reductions in Prometheus

---

### 9. Open Items for Prod

- fitfileprod context was not found in `gcx config`. To audit prod:

  ```bash
  gcx login
  gcx stacks list  # find prod stack
  gcx config set-context fitfileprod --stack fitfileprod
  ```

- Repeat all phases above for the prod context
- Check if `pod` is also accidentally indexed on prod (same `pod: null` missing override issue)
- Compare label cardinality between test and prod—patterns should be similar

---

_Report generated by Mechanical Lead via gcx CLI audit (fitfiletest context). Adaptive telemetry APIs were unreachable due to expired cloud token._
