---
alias: [Alloy Operator Upgrade Guide, Grafana Migration Protocol]
conformant: false
created: 2026-02-05T00:00:00+00:00
modified: 2026-08-13T10:53:39+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-grafana-observability-stack-upgrade
status: stable
tags: [grafana, helm, migration, observability, protocol]
title: Protocol - Grafana Observability Stack Upgrade
type: protocol
---

## Logic Map

- Objective: Migrate Kubernetes monitoring from legacy static pods (`k8s-monitoring` v1.x) to the modern Alloy Operator architecture (`k8s-monitoring` v3.7+).
- Trigger: Grafana repository deprecation (Jan 30, 2026) and architectural obsolescence of static collectors.
- Constraint: Must use OCI-based chart distribution to bypass community index instability.

---

## The Architecture Shift

| Feature | Legacy (v1.5) | Modern (v3.7+) |
|:--- |:--- |:--- |
| Management | Static StatefulSets & DaemonSets | Alloy Operator (Dynamic CRD-based) |
| Configuration | `externalServices` object (rigid) | `destinations` array (flexible, multi-sink) |
| Distribution | `grafana.github.io` (Deprecated) | `oci://registry-1.docker.io/grafanacharts` |
| Secrets | `extraObjects` / Hardcoded | Native Secret references / Env Vars |

---

## The Algorithm

### 1. Repository & Tooling Fix (Immediate)

_Fix the broken update path by switching to OCI._

1. Update Helm Repos:

```bash
helm repo remove grafana-community || true
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo update grafana-community
```

1. Configure OCI Source:
   Update your Chart Manager config to target:
   `oci://registry-1.docker.io/grafanacharts/k8s-monitoring`

### 2. Pre-requisites: Install CRDs

_Helm often fails to upgrade CRDs automatically. Install them manually first._

```bash
# Fetch and apply the Alloy CRDs
helm pull oci://registry-1.docker.io/grafanacharts/k8s-monitoring --version 3.7.0 --untar
kubectl apply -f k8s-monitoring/crds/
```

### 3. Configuration Refactor (`values-v3.yaml`)

_Translate v1 logic to the v3 schema. Do not reuse the old `values.yaml`._

```yaml
# --- GLOBAL ---
cluster:
  name: prod-1

# --- DESTINATIONS (New Flexible Sink Logic) ---
destinations:
  - name: prometheus
    type: prometheus
    url: https://prometheus-prod-05-gb-south-0.grafana.net/api/prom
    auth:
      type: basic
      username: "${PROMETHEUS_USERNAME}"
      password: "${PROMETHEUS_PASSWORD}"
  - name: loki
    type: loki
    url: https://logs-prod-006.grafana.net/loki/api/v1/push
    auth:
      type: basic
      username: "${LOKI_USERNAME}"
      password: "${LOKI_PASSWORD}"

# --- FEATURES (Granular Enablement) ---
clusterMetrics:
  enabled: true
  opencost:
    enabled: false # Optional: Cost monitoring

clusterEvents:
  enabled: true

podLogs:
  enabled: true
  namespaces:
    exclude:
      - dataprotection-microsoft

# --- COLLECTORS (Operator Managed) ---
alloy-metrics:
  enabled: true
  resources:
    limits: { memory: 2Gi }
    requests: { cpu: 500m, memory: 1Gi }

alloy-logs:
  enabled: true
  resources:
    limits: { memory: 2Gi }
    requests: { cpu: 250m, memory: 1Gi }
```

### 4. Image Import Strategy (Private Registry)

_For air-gapped or private ACR setups, import these specific images:_

1. Alloy Operator: `grafana/alloy-operator:v1.x` (The Controller)
2. Alloy: `grafana/alloy:v1.x` (The Collector - mapped via `global.image.*`)
3. Kube State Metrics: `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.x`
4. Node Exporter: `quay.io/prometheus/node-exporter:v1.x`

---

## Unit Test (Verification)

1. Check Operator Status:
   `kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-operator`
   _(Status must be Running)_

2. Verify Collectors:
   `kubectl get alloy -n monitoring`
   _(Should list `alloy-metrics`, `alloy-logs`, etc.)_

3. Validate Data Flow:
   Check Grafana Explore for recent metrics (`up`) and logs (`{cluster="prod-1"}`).

## ## Unit Test (Verification)

### Troubleshooting: Image Path Resolution (Chart Manager)

If your automated tooling (e.g., Rust Chart Manager) fails to resolve image tags in v3:

- Error: `Path not Found: global.image.tag`.
- Cause: v3 often defaults `global.image.tag` to `null`, relying on subchart `appVersion`.
- Fix: Explicitly point your `tag_path` to `alloy-metrics.image.tag` or hardcode your target version in the override `values.yaml`.

## ### Troubleshooting: Image Path Resolution (Chart Manager)

### Common Migration Gotchas

#### 1. Validation Fail: "Values Appear to Be from Version 1.x"

- Cause: The v3 chart detects legacy keys like `externalServices` or `traces` and blocks the template generation.
- Fix: You must explicitly nullify these keys in your environment-specific `values.yaml` to ensure they are removed during the Helm merge process.

```yaml
externalServices: null
traces: null
# ... nullify any other v1 specific top-level keys
```

#### 2. Advanced Secret Mapping (`urlFrom`)

- Problem: The chart may not support simple secret keys for URL fields in the `destinations` block.
- Solution: Manually construct Alloy expressions using `urlFrom`.

```yaml
destinations:
  - name: prometheus
    type: prometheus
    urlFrom: 
      # Reuses existing monitoring secret keys
      expression: 'convert.nonsensitive(remote.kubernetes.secret.monitoring.data["prometheus-host"])'
```
