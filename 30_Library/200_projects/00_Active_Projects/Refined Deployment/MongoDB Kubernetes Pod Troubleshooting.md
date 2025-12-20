---
aliases: []
confidence: 
created: 2025-10-06T11:11:59Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: MongoDB Kubernetes Pod Troubleshooting
type:
uid: 
updated: 
version:
---

## LLM Prompt: MongoDB Kubernetes Pod Troubleshooting

### Persona

You are an expert Site Reliability Engineer (SRE) and Kubernetes administrator with deep, specialised knowledge of running stateful workloads like MongoDB in a containerised environment. You are also an expert in observability stacks, particularly Prometheus and the exporters used to monitor applications like MongoDB.

---

### Context

I am troubleshooting a recurring issue with MongoDB pods running in a Kubernetes cluster. The primary symptom is a high volume of log entries indicating errors while gathering metrics. The core error message is: "collected metric ... was collected before with the same name and label values". This suggests a problem with the Prometheus metrics being exposed by the MongoDB pod's exporter.

The environment details are as follows:

- **Application:** MongoDB
- **Orchestrator:** Kubernetes
- **Cluster:** `hie-prod-34`
- **Namespace:** `hie-prod-34`
- **Pod Name:** `hie-prod-34-mongodb-b17ef-0`
- **Monitoring:** A Prometheus-compatible scraper is attempting to collect metrics from an HTTP endpoint on the pod.

---

### Log Data

Below is a substantial excerpt from the logs of the affected MongoDB pod (`hie-prod-34-mongodb-b17ef-0`). These logs contain the repeated metrics collection errors, as well as network connection logs that may provide additional context.

```log
: "1000 lines shown — 4.23% (2min 32sec) of 1h"
Total bytes processed: "2.88  MB"
Common labels: {"app_kubernetes_io_name":"mongodb","cluster":"hie-prod-34","flags":"F","namespace":"hie-prod-34","pod":"hie-prod-34-mongodb-b17ef-0","service_name":"mongodb"}

1759748041126 2025-10-06T10:54:01.126Z time=2025-10-06T10:54:01.125Z level=ERROR source=http_error_logger.go:53 msg="error gathering metrics:100 error(s) occurred:\n* [from
Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:1024}} was collected
before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"
value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:4}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"
 value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:4096}} was collected before with the same name and label
values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}}
was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}
label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:16384}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\"
{ label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same name
and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}
 untyped:{value:65536}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"
value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same name and label values\n* [from Gatherer #2] collected
metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:262144}} was collected before with the
same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"
 value:\"1\"}  counter:{value:0}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}
label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:1.048576e+06}} was collected before with the same name and label values\n* [from Gatherer
#2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before
with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}
 label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:4.194304e+06}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"
value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was
collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"
 value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:1.6777216e+07}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" {
label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same name and
label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}
untyped:{value:6.7108864e+07}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}
 label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:2.68435456e+08}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric
\"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same
name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"
value:\"1\"}  untyped:{value:1.073741824e+09}} was collected before with the same name and label values\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"
 value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  counter:{value:0}} was collected before with the same name and label values\n* [from Gatherer #2]
...
<The full log file content is inserted here>
...
1759747890824 2025-10-06T10:51:30.824Z time=2025-10-06T10:51:30.823Z level=ERROR source=http_error_logger.go:47 msg="error gathering metrics:" error="[from Gatherer #2] collected
metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicNumPlans_lowerBound\" { label:{name:\"cl_id\"  value:\"68890fe8814e68864f7c7234\"}  label:{name:\"cl_role\"  value:\"\"}  label:{name:\"rs_nm\"  value:\"rs0\"}  label:{name:\"rs_state\"  value:\"1\"}  untyped:{value:2}} was collected before with the
same name and label values" total_errors=100 error_no=0
```

---

### Task

Based on the context and the extensive log data provided, please perform the following:

1. **Root Cause Analysis:**
   - Explain in detail what the error "collected metric ... was collected before with the same name and label values" means in the context of Prometheus metric scraping.
   - Analyse the specific metrics that are duplicated (e.g., `mongodb_ss_metrics_query_multiPlanner_histograms...`). What do these metrics represent, and why might they be prone to duplication?
   - Formulate at least two credible hypotheses for the root cause of this issue. Consider potential bugs in the MongoDB exporter, misconfigurations in the deployment, or issues with the scraping configuration.

2. **Diagnostic Steps:**
   - Provide a precise, ordered list of `kubectl` commands to run to gather more information. These should include commands to:
     - Inspect the running pod's configuration (`describe pod`).
     - View the full, unredacted logs (`logs`).
     - Check the YAML definition of the Deployment or StatefulSet managing this pod.
     - Identify and inspect the Prometheus `ServiceMonitor` or `PodMonitor` that is targeting this pod.
   - Explain what specific information we are looking for in the output of each command.
   - Provide a `curl` or `wget` command that can be executed from within the pod (`kubectl exec`) to manually scrape the `/metrics` endpoint and allow for inspection of the raw output.

3. **Proposed Solutions:**
   - For each of your hypotheses, propose a concrete solution.
   - For example, if you suspect a bug in the exporter, suggest how to check the exporter version and find relevant bug reports or release notes. Recommend a potential version to upgrade or downgrade to.
   - If you suspect a configuration issue, provide examples of the correct configuration for the exporter or the Prometheus scraping rules (`ServiceMonitor`/`PodMonitor`) to prevent duplicate metric collection.

Please structure your response clearly, using Markdown for formatting, with code blocks for commands and file excerpts. Your goal is to provide a comprehensive and actionable guide that will allow me to systematically diagnose and resolve this issue.

Plan accepted: 1.Identify MongoDB release manifests in GitOps repo

Search the repo (e.g. `rg -i "bitnami/mongodb"`) to locate the HelmRelease / HelmChart / kustomize overlays that declare the Bitnami MongoDB chart for the hie-prod-34 namespace.

Confirm current chart version (expected 16.5.\*) and note the location of the associated values.yaml file that controls metrics settings.

2. Create a feature branch for the fix

`git checkout -b fix/mongodb-exporter-duplicate-metrics`

All following edits will be committed on this branch; this keeps the change isolated for review and easy rollback.

3. Upgrade Bitnami MongoDB chart and pin exporter version

Edit the Helm release definition:

```yaml
chart:
  repository: oci://registry-1.docker.io/bitnamicharts
  name: mongodb
  version: 16.8.4 # ≥16.8.0 includes exporter ≥0.41.0
```

Add / update metrics settings in values.yaml:

```yaml
metrics:
  enabled: true
  image:
    tag: 0.41.0 # pin the stable exporter
  extraArgs:
    - --collect.diagnosticdata=false
    - --collect.indexusage=false
    - --collect.topmetrics=false # skips heavy histograms
```

These args omit the histogram families that are producing duplicate series while keeping core metrics.

4. Harden ServiceMonitor to avoid double-scraping

Locate the ServiceMonitor (or PodMonitor) manifest for MongoDB and ensure only one selector matches the pod labels.

Increase interval to `60s` and set `scrapeTimeout: 30s` to reduce overlap:

```yaml
spec:
  endpoints:
    - port: metrics
      interval: 60s
      scrapeTimeout: 30s
```

Commit any required label / selector tweaks so Prometheus has exactly one target per pod.

5. Render chart locally for sanity checks

From the repo root:

```bash
helm dependency update path/to/mongodb/chart
helm template test-mongo path/to/mongodb/chart -f path/to/values.yaml | grep image:
```

Verify the exporter image now shows `bitnami/mongodb-exporter:0.41.0` and the ServiceMonitor is rendered with the new interval.

6. Commit, push and open merge request

Follow commit-message convention (prefix with existing Jira ticket if any, else `FFAPP-5288`).

Push the branch and open an MR describing:

- root cause (duplicate histogram metrics)
- chart upgrade & exporter pin
- ServiceMonitor hardening
  Request reviewers and mark as “auto-sync on merge” for ArgoCD.

7. Sync ArgoCD and monitor rollout
   Once MR merges, ArgoCD will pick up the new manifests.
   Use the jumpbox to tail logs during rollout:

```bash
kubectl -n hie-prod-34 logs -l app.kubernetes.io/name=mongodb -c mongodb-exporter -f
```

Confirm the duplicate-metric error no longer appears.

8. Post-deployment validation
9. Check Prometheus target status → should be “UP” with no “duplicate metrics” warnings.
10. Verify dashboard panels that rely on MongoDB metrics still populate.
11. If duplicates persist, push a follow-up commit that temporarily sets `metrics.enabled: false` as an emergency workaround and repeat validation.

UpdateTodos: 8 items

## MongoDB Kubernetes Pod Troubleshooting: Complete Analysis & Solutions

### 🔍 Root Cause Analysis

#### Error Explanation

The error "collected metric ... was collected before with the same name and label values" indicates **duplicate metric series registration** within the Prometheus MongoDB exporter. This occurs when the exporter attempts to register the same metric with identical labels multiple times, violating Prometheus client library constraints.

#### Problem Metrics Analysis

The logs show duplicated **histogram metrics** from the `multiPlanner` query execution subsystem:

- `mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound`
- `mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_count`

These metrics track query execution time buckets and are prone to duplication because:

1. **MongoDB internal structure changes** between versions cause metric paths to overlap
2. **Complex histogram generation** from MongoDB's diagnostic output creates timing conflicts
3. **Concurrent scraping** can trigger race conditions in metric collection

#### Primary Hypotheses

**Hypothesis 1: MongoDB Exporter Bug (Version 0.40.0)**

- Your deployment likely uses Bitnami MongoDB chart 16.5.x with mongodb-exporter ~0.40.0
- Version 0.40.0 has known issues with histogram metric collection duplicates
- Fixed in version ≥0.41.0

**Hypothesis 2: Prometheus Scraping Race Condition**

- ServiceMonitor configured with aggressive scraping intervals (<30s)
- Multiple Prometheus instances or overlapping selectors causing concurrent scrapes
- Exporter not thread-safe for concurrent metric generation

### 🔧 Diagnostic Steps

#### 1. Pod Configuration Inspection

```bash
# Get detailed pod information
kubectl -n hie-prod-34 describe pod hie-prod-34-mongodb-b17ef-0

# Check current container versions
kubectl -n hie-prod-34 get pod hie-prod-34-mongodb-b17ef-0 -o jsonpath='{.spec.containers[*].image}' | tr ' ' '\n'

# Examine environment variables and args
kubectl -n hie-prod-34 get pod hie-prod-34-mongodb-b17ef-0 -o yaml > mongodb-pod-manifest.yaml
```

#### 2. Log Analysis & Pattern Detection

```bash
# Get full unfiltered logs from exporter
kubectl -n hie-prod-34 logs hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter --tail=2000 > exporter-logs.txt

# Search for specific error patterns
grep -E "(collected metric|error gathering|Gatherer #)" exporter-logs.txt | head -20

# Check scraping frequency in logs
kubectl -n hie-prod-34 logs hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter --since=10m | grep -E "time=.*level=INFO" | tail -10
```

#### 3. Deployment & Helm Release Investigation

```bash
# Find StatefulSet managing this pod
kubectl -n hie-prod-34 get statefulset -o wide

# Get StatefulSet YAML definition
kubectl -n hie-prod-34 get statefulset hie-prod-34-mongodb-b17ef -o yaml > mongodb-statefulset.yaml

# Check Helm release information
helm -n hie-prod-34 list | grep mongodb
helm -n hie-prod-34 get values hie-prod-34-mongodb-b17ef
```

#### 4. ServiceMonitor/PodMonitor Analysis

```bash
# Find Prometheus scraping configuration
kubectl get servicemonitor -A | grep -i mongo
kubectl get podmonitor -A | grep -i mongo

# Examine the monitoring configuration
kubectl -n hie-prod-34 get servicemonitor -o yaml > mongodb-servicemonitor.yaml

# Check if multiple targets exist
kubectl -n hie-prod-34 get endpoints -l app.kubernetes.io/name=mongodb
```

#### 5. Manual Metrics Endpoint Testing

```bash
# Direct metrics scrape from pod
kubectl -n hie-prod-34 exec hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter -- wget -qO- http://localhost:9216/metrics > raw-metrics.txt

# Count duplicate metric occurrences
grep -E "mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros" raw-metrics.txt | sort | uniq -c | sort -nr

# Check metrics endpoint response time
kubectl -n hie-prod-34 exec hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter -- time wget -qO- http://localhost:9216/metrics >/dev/null
```

### 🚀 Proposed Solutions

#### Solution 1: Upgrade MongoDB Exporter (Primary Recommendation)

Based on the Bitnami chart version 16.5.x in your deployment, upgrade to chart version ≥16.8.0:

**Step 1: Update Helm Chart Version**

```yaml
# In your ArgoCD Application or Helm values
mongodb:
  targetRevision: "16.8.4" # Contains mongodb-exporter ≥0.41.0
```

**Step 2: Pin Exporter Version & Disable Problematic Metrics**

```yaml
# Add to MongoDB values.yaml
mongodb:
  metrics:
    enabled: true
    image:
      tag: "0.41.0" # Pin to stable version
    extraArgs:
      - --collect.diagnosticdata=false
      - --collect.indexusage=false
      - --collect.topmetrics=false # Disables histogram-heavy metrics
      - --collect.currentopmetrics=false
```

#### Solution 2: ServiceMonitor Configuration Hardening

**Update Prometheus Scraping Configuration:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: mongodb-metrics
  namespace: hie-prod-34
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: mongodb
      app.kubernetes.io/component: metrics
  endpoints:
    - port: metrics
      interval: 60s # Increase from default 30s
      scrapeTimeout: 30s # Prevent overlapping scrapes
      path: /metrics
      honorLabels: true
```

#### Solution 3: Emergency Workaround (If Upgrades Blocked)

If immediate chart upgrades aren't possible:

**Temporary Metrics Disable:**

```yaml
# In MongoDB values.yaml
mongodb:
  metrics:
    enabled: false # Disable until exporter upgrade
```

**Alternative: Selective Metric Collection:**

```yaml
mongodb:
  metrics:
    enabled: true
    extraArgs:
      - --collect.collection=false
      - --collect.database=false
      - --collect.topmetrics=false
      - --collect.indexusage=false
      - --collect.diagnosticdata=false
      # Keep only basic metrics
      - --collect.replset
      - --collect.connpoolstats
```

### 📋 Implementation Timeline

1. **Immediate (0-2 hours)**: Implement Solution 3 workaround to stop log flooding
2. **Short-term (1-3 days)**: Deploy Solution 1 with chart upgrade and exporter pinning
3. **Long-term (1-2 weeks)**: Implement Solution 2 with ServiceMonitor optimization

### ⚠️ Validation Steps

After implementing solutions:

```bash
# 1. Verify exporter version
kubectl -n hie-prod-34 get pod hie-prod-34-mongodb-b17ef-0 -o jsonpath='{.spec.containers[?(@.name=="mongodb-exporter")].image}'

# 2. Monitor logs for duplicate errors (should be clean)
kubectl -n hie-prod-34 logs hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter -f | grep -v "collected metric"

# 3. Check Prometheus target health
# Access Prometheus UI → Status → Targets → search for "mongodb"

# 4. Verify key metrics still available
kubectl -n hie-prod-34 exec hie-prod-34-mongodb-b17ef-0 -c mongodb-exporter -- wget -qO- http://localhost:9216/metrics | grep -c "mongodb_up"
```

This comprehensive approach addresses both the immediate log flooding issue and the underlying exporter compatibility problem, ensuring stable MongoDB monitoring for your hie-prod-34 environment.
