---
created: 2026-02-01 15:35:00+00:00
modified: 2026-02-01 20:50:52+00:00
status: growing
tags:
- calico
- grafana
- kubernetes
- observability
title: SoT - Calico Observability
type: SoT
permalink: llmeon/30-library/so-t/so-t-calico-observability
---

## 1. Core Distinction: Engine vs. Dashboard

It is critical to distinguish between the Calico CNI and the proprietary Tigera management tools.

### Calico CNI (The Engine)

- Role: Data Plane & Policy Enforcement.
- Components: `felix` (per-node agent), `bird` (BGP routing).
- Criticality: Essential. Without it, pod-to-pod communication fails.
- State: Policies are enforced via `iptables`/`eBPF` on the node. It does not require a dashboard to function.

### Tigera Enterprise Webapp (The Dashboard)

- Role: Management Plane & Visualization.
- Capabilities: Flow Visualizer, Policy Builder UI, Tier Management.
- Criticality: Non-essential. Removing it causes loss of _visibility_, not _functionality_.

## 2. Migration Strategy: Tigera to Grafana

The visibility provided by Tigera Enterprise can be largely replicated using a standard Prometheus/Grafana stack.

### Required Configuration

1. Enable Metrics: Patch `felixconfiguration` to set `prometheusMetricsEnabled: true` (default port `9091`).
2. Scrape Config: Create a Prometheus `ServiceMonitor` targeting `calico-felix`.

### Key Metrics to Monitor

| Capability | Metric Name | Purpose |
|:--- |:--- |:--- |
| Policy Hits | `calico_felix_policy_hits_total` | Identify active security rules (Allowed vs. Denied). |
| Throughput | `container_network_transmit_bytes_total` | Track bandwidth usage per Pod/Namespace. |
| Health | `calico_felix_agent_up` | Monitor Felix and BGP peer status. |
| Drops | `calico_felix_denied_packets_total` | Visualize drops caused by policy violations (The "Why"). |

### Limitations

- Visuals: Grafana "Node Graphs" are less interactive than Tigera's Flow Visualizer.
- Management: Grafana is read-only; it cannot modify Network Policies.