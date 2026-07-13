---
created: 2026-05-26T17:22:25+00:00
modified: 2026-07-13T08:52:21+00:00
permalink: llmeon/30-library/200-projects/grafana-alloy-audit-report
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: grafana_alloy_audit_report
type: null
---

## Grafana Alloy Audit & Remediation Report (FTFL-638)

This report investigates the missing `pod` label on Loki log streams in the `testing` cluster and outlines the root causes, live status, and remediation plan.

---

### Chart Version Audit

We audited the Grafana Helm configuration override files across the FITFILE clusters under the `ffnodes/` directory.

#### Comparison Table

| Cluster | Chart Version | `labelsToKeep` | `extraDiscovery` / `extraRelabeling` Key | `cluster.name` | `structuredMetadata` | `discoveryType` |
|:--- |:--- |:--- |:--- |:--- |:--- |:--- |
| testing | `3.7.5` | `[pod, namespace, container, job, instance, app.kubernetes.io/name, k8s.namespace.name, k8s.node.name]` | `extraDiscoveryRules` (configured) | `testing` | `k8s.pod.name`, `pod`, `service.instance.id` | `service` (under `clusterMetrics.kube-state-metrics`) |
| staging (via `ff-test-*`) | `1.5.4` (default) | `["pod", "container", "namespace"]` | N/A (uses v1 schema under `logs.pod_logs`) | `staging` (via `deploymentKey`) | N/A | N/A |
| production (`prod-1`) | `1.5.4` (default) | `["pod", "container", "namespace"]` | N/A | `prod-1` (via `deploymentKey`) | N/A | N/A |
| mcnft-prod-1 | `3.7.5` | Not overridden (uses chart defaults) | N/A | Not set | Not set | Not set |
| cuh-prod-1 | `1.5.4` (default) | Inherited from base chart | N/A | `cuh-prod-1` (via `deploymentKey`) | N/A | N/A |
| nnuh-prod-1 | `1.5.4` (default) | Inherited from base chart | N/A | `nnuh-prod-1` (via `deploymentKey`) | N/A | N/A |
| _Other clusters_ | `1.5.4` (default) | Inherited from base chart | N/A | Derived from `deploymentKey` | N/A | N/A |

_Note: The context `aks-ff-uks-gp-1` was unreachable during testing due to private DNS host lookup failure (`dial tcp: lookup … privatelink.uksouth.azmk8s.io: no such host`)._

---

### Live Cluster State

#### 2a. Alloy Pod & Deployment Health

##### Testing Cluster (`fitfile-cloud-testing-aks-cluster`)

The Alloy pods are healthy and running under the `monitoring` namespace:

```bash
kubectl --context fitfile-cloud-testing-aks-cluster get pods -n monitoring | grep -i alloy
grafana-k8s-monitoring-alloy-logs-llb8j                     2/2     Running            0                3h32m
grafana-k8s-monitoring-alloy-logs-m22vk                     2/2     Running            0                3h32m
grafana-k8s-monitoring-alloy-logs-sdzm5                     2/2     Running            0                3h32m
grafana-k8s-monitoring-alloy-metrics-0                      2/2     Running            0                175m
grafana-k8s-monitoring-alloy-operator-cc5bd5994-7scn4       1/1     Running            0                3h32m
grafana-k8s-monitoring-alloy-singleton-7cfb7fcf97-cxv6z     2/2     Running            0                3h32m
```

##### Staging Cluster (`fitfile-cloud-staging-aks-cluster`)

Alloy is healthy in staging:

```bash
kubectl --context fitfile-cloud-staging-aks-cluster get pods -n monitoring | grep -i alloy
grafana-k8s-monitoring-alloy-0                               2/2     Running   0          21h
grafana-k8s-monitoring-alloy-events-865946d7b8-mtqvm         2/2     Running   0          21h
grafana-k8s-monitoring-alloy-logs-fqdxx                      2/2     Running   0          12h
grafana-k8s-monitoring-alloy-logs-mfc8w                      2/2     Running   0          12h
grafana-k8s-monitoring-alloy-logs-tfl68                      2/2     Running   0          12h
grafana-k8s-monitoring-alloy-logs-tfpk9                      2/2     Running   0          12h
```

---

#### 2b. Rendered Alloy Config

##### Testing (V3.7.5) Config Extract

The rendered Alloy config in the `grafana-k8s-monitoring-alloy-logs` ConfigMap contains the `stage.structured_metadata` block:

```json
    stage.structured_metadata {
      values = {
        "k8s_pod_name" = "k8s_pod_name",
        "pod" = "pod",
        "service_instance_id" = "service_instance_id",
      }
    }

    stage.label_keep {
      values = ["__tenant_id__","pod","namespace","container","job","instance","app_kubernetes_io_name","k8s_namespace_name","k8s_node_name"]
    }
```

##### Staging (V1.5.4) Config Extract

The staging ConfigMap does NOT use `stage.structured_metadata` or `stage.label_keep`. Instead, it simply passes the labels generated from discovery relabeling directly to the write stage:

```json
discovery.relabel "pod_logs" {
  // ...
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    action = "replace"
    target_label = "pod"
  }
  // ...
}
```

---

#### 2c. Live Loki Log Flow Check

Using `gcx` logs query:

- Staging: `pod` label appears correctly as an indexed stream label:

```bash
gcx logs query --context fitfiletest '{cluster="staging", pod=~".+"}' --limit 1
# Returns: log streams successfully indexed by pod
```

- Testing: `pod` label is ABSENT from indexed stream labels:

```bash
gcx logs query --context fitfiletest '{cluster="testing", pod=~".+"}' --limit 1
No data
```

  However, parsing the structured metadata field works, indicating `pod` is in structuredMetadata:

```bash
gcx logs query --context fitfiletest '{cluster="testing"} | pod="coredns-5495c4566-94psx"' --limit 1
# Returns logs for coredns successfully
```

---

#### 2d. Prometheus Metrics Check

Both testing and staging have healthy metrics pipelines:

```bash
gcx metrics query --context fitfiletest 'count by (cluster) (kube_pod_info{cluster="testing"})'
VALUE  TIMESTAMP             SERIES
110    2026-05-26T17:18:47Z  {cluster="testing"}

gcx metrics query --context fitfiletest 'count by (cluster) (kube_pod_info{cluster="staging"})'
VALUE  TIMESTAMP             SERIES
142    2026-05-26T17:18:48Z  {cluster="staging"}

gcx metrics query --context fitfiletest 'count by (cluster) (kube_node_info{cluster="testing"})'
VALUE  TIMESTAMP             SERIES
3      2026-05-26T17:18:49Z  {cluster="testing"}

gcx metrics query --context fitfiletest 'count by (cluster) (kube_node_info{cluster="staging"})'
VALUE  TIMESTAMP             SERIES
4      2026-05-26T17:18:50Z  {cluster="staging"}
```

---

#### 2e. Alloy Pod Logs Spot-Check

Alloy daemonset log checks on both testing and staging clusters confirm no configuration or connection errors. Logs indicate normal tailing operations:

```sh
ts=2026-05-26T17:01:12.305191465Z level=info msg="skipping update of position for a file..."
ts=2026-05-26T17:01:12.305325951Z level=info msg="tail routine: started" ...
```

---

### Root Cause Analysis

1. Chart Version Mismatch: Staging, Production (`prod-1`), and all other clusters run Grafana `k8s-monitoring` Helm chart `1.5.4` (Alloy v1.3.1), which passes all relabeled metadata directly as indexed labels. Testing (and `mcnft-prod-1`) runs chart version `3.7.5` (Alloy v1.12.2).
2. Promotion of `pod` to Structured Metadata: Under version `3.7.5`, if a label is defined under the `structuredMetadata` object in `values.yaml`, the chart generates a `stage.structured_metadata` block in Alloy. In Grafana Loki, any label promoted to structured metadata is automatically dropped from the indexed Loki stream labels, making it unqueryable as `{pod="…"}`.
3. Difference in Key Overrides: Testing explicitly defined:

```yaml
structuredMetadata:
 k8s.pod.name: k8s.pod.name
 pod: pod
 service.instance.id: service.instance.id
```

   By explicitly defining `pod: pod`, it demoted the `pod` label from Loki stream indexing.

---

### Remediation Plan

#### A. The values.yaml Patch

We must remove `pod: pod` from the `structuredMetadata` block in `ffnodes/fitfile/testing/values.yaml` to ensure it is kept as an indexed stream label instead of being demoted.

```diff
diff --git a/ffnodes/fitfile/testing/values.yaml b/ffnodes/fitfile/testing/values.yaml
index d88cd73b..5985b56a 100644
--- a/ffnodes/fitfile/testing/values.yaml
+++ b/ffnodes/fitfile/testing/values.yaml
@@ -332,7 +332,6 @@ grafana:
       - k8s.node.name
     structuredMetadata:
       k8s.pod.name: k8s.pod.name
-      pod: pod
       service.instance.id: service.instance.id
```

#### B. Verification Checklist

Execute the following commands sequentially to apply and verify the remediation:

1. Local Syntax & Template Rendering Check:

```bash
./scripts/render.sh fitfile/testing > /dev/null
```

   Ensure exit code is 0.

1. Commit and Push:

```bash
git add ffnodes/fitfile/testing/values.yaml
git commit -m "FTFL-638: Remove pod from structuredMetadata in testing to restore Loki stream label"
git push origin feature/FTFL-638-add-labels-for-logs
```

1. Deploy & Sync:
Verify that ArgoCD picks up and syncs the changes to `grafana-k8s-monitoring` on the testing cluster.
Monitor the DaemonSet rollout:

```bash
kubectl --context fitfile-cloud-testing-aks-cluster rollout status daemonset/grafana-k8s-monitoring-alloy-logs -n monitoring
```

1. Verify ConfigMap Update:
Dumping the ConfigMap should confirm `pod` has been removed from `stage.structured_metadata`:

```bash
kubectl --context fitfile-cloud-testing-aks-cluster get configmap grafana-k8s-monitoring-alloy-logs -n monitoring -o jsonpath='{.data.config\.alloy}' | grep -A 5 "structured_metadata"
```

_Expected: `"pod" = "pod"` should not be in the list._

1. Verify Loki Logs Stream Index:
Query Loki directly to confirm the `pod` label is queryable:

```bash
gcx logs query --context fitfiletest '{cluster="testing", pod=~".+"}' --limit 5
```

_Expected: Returns log lines successfully._

---

### Go/No-Go Gate

Before upgrading any other FITFILE clusters to Helm chart version `3.7.5`, the following conditions must be GREEN:

1. Loki stream label `pod` is present on testing:

```bash
gcx logs labels --context fitfiletest --label pod
```

Output must include active pods from the `testing` cluster (e.g. `coredns-*`, `spicedb-*`, `workflows-api-*`).

1. Querying log stream by pod works:

```bash
gcx logs query --context fitfiletest '{cluster="testing", pod=~".+"}' --limit 5
```

Output must return 5 log lines with no parser pipes (`|`).

1. Prometheus metrics counts are healthy:

```bash
gcx metrics query --context fitfiletest 'count(kube_pod_info{cluster="testing"})'
```

Output value must match active pod counts (approx. ~110 series).
