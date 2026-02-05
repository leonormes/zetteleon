---
created: 2026-02-05T00:00:00+00:00
modified: 2026-02-05T13:34:19+00:00
tags: ["grafana", "helm", "kubernetes", "log", "migration", "rust"]
title: 2026-02-05 - Grafana Helm Chart Upgrade & Repository Migration
---

## Context

The Grafana `k8s-monitoring` stack is currently running a deprecated version (v1.5.4). A migration to v3.7+ is required to align with modern Alloy Operator-based architecture and to restore the update path following Grafana's repository migration on January 30, 2026.

## Investigation Log

### 1. Repository Migration Discovery

- The Shift: Grafana deprecated `https://grafana.github.io/helm-charts` in favor of `https://grafana-community.github.io/helm-charts`.
- The Issue: Local Helm indices and the Rust Chart Manager were failing to resolve the `k8s-monitoring` chart even after repo updates.

### 2. Architectural Gap Analysis

- Old (v1): Static StatefulSets/DaemonSets, rigid `externalServices` configuration.
- New (v3): Alloy Operator-driven, flexible `destinations` array, granular feature flags (`clusterMetrics`, `podLogs`).

### 3. Tooling Refactor (Rust Chart Manager)

- Problem: Rust implementation failed to parse the new community index.
- Solution: Shifted to an OCI-first distribution model.
- Action: Updated `config.yaml` to use `oci://registry-1.docker.io/grafanacharts`.
- Image Mapping: Added `alloy-operator` and updated `alloy` to use `global.image.*` paths for registry overrides (Azure ACR targeting).

## Step-by-Step Commands Used

```bash
# 1. Force update the community repo
helm repo remove grafana-community || true
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo update grafana-community

# 2. Verify chart presence (may show shadowing issues)
helm search repo grafana-community/k8s-monitoring

# 3. Use OCI to bypass index issues (The 2026 Standard)
helm show values oci://registry-1.docker.io/grafanacharts/k8s-monitoring --version 3.7.0
```

### Related Knowledge

- [[Grafana Monitoring Stack Upgrade Report]]: Comprehensive report on the 2024 vs 2026 standard gap.
- [[Grafana Stack Update v1 to v3]]: Technical refactoring details for `values.yaml` and Rust code integration.
- [[SoT - Cloud-Native Observability]]: Canonical strategy for logs, metrics, and tracing.
- [[SoT - FITFILE Secret Management Architecture]]: Related via the integration of Vault secrets for monitoring destinations.
# ## Step-by-Step Commands Used

### Update: 2026-02-05 (ArgoCD Sync Fixes)
- **Environment:** `testing`.
- **Issue:** ArgoCD sync failure due to persistent legacy keys.
- **Resolution:**
    - Nullified `externalServices` and `traces` in `testing/values.yaml`.
    - Implemented `urlFrom` Alloy expressions to bridge existing Vault secrets with the new `destinations` schema.
