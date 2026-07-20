---
aliases: [Calico Architecture, eBPF Data Plane, Felix, Project Calico]
conformant: false
created: 2026-02-05T00:00:00+00:00
modified: 2026-07-20T16:33:52+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-calico-cni-architecture
tags: [calico, ebpf, kubernetes, networking, sot]
title: SoT - Calico CNI Architecture
type: sot
---

## Minimum Viable Understanding (MVU)

Project Calico is a high-performance networking and security solution for Kubernetes. Unlike basic plugins, Calico treats the cluster as a pure L3 network, avoiding the overhead of L2 bridges where possible and leveraging BGP or Overlay encapsulation (VXLAN/IP-in-IP) for cross-node traffic.

---

## 1. Core Components

| Component | Role | Function |
|:--- |:--- |:--- |
| Felix | The Agent | Runs on every node. Programs routes, ACLs, and interfaces. Talks directly to K8s API. |
| BIRD | The BGP Speaker | Distributes routing information between nodes. |
| Confd | Configuration | Watches the datastore for changes and triggers Felix updates. |
| Typha | Scalability | Acts as a proxy/cache between Felix and the API server for large clusters. |

---

## 2. Data Planes: Iptables vs. eBPF

Calico supports multiple data planes to enforce NetworkPolicies:

### Standard (Iptables)

- Mechanism: Felix programs standard Linux `iptables` chains.
- Constraint: Performance degrades as the number of rules increases (linear scan).

### eBPF (Modern/High Performance)

- Mechanism: Programs are injected directly into the Linux Kernel.
- Benefit: Bypasses `kube-proxy`. Massive throughput improvements and lower latency for Service load-balancing.

---

## 3. Encapsulation Modes (Overlay)

Used when the underlying cloud network is unaware of Pod IPs.

### VXLAN (Azure Standard)

- Mechanism: Encapsulates L2 in UDP.
- BGP: Does not require BGP.
- Overhead: Slightly higher due to larger headers.

### IP-in-IP (AWS/On-Prem)

- Mechanism: Wraps the IP packet in another IP packet.
- BGP: Typically uses BGP between nodes to learn routes.

---

## 4. Policy Engine (Calico NetworkPolicy)

Calico extends the standard Kubernetes `NetworkPolicy` with advanced features:

- GlobalNetworkPolicy: Applied cluster-wide (e.g., "Deny all to port 22").
- Labels on Nodes: Allows policies to target Node-level traffic.
- Actions: Supports `Log`, `Pass`, and `Deny` (Standard K8s only has `Allow`).

---

## Related Knowledge

- [[SoT - Kubernetes Networking Model]] (The foundational rules Calico enforces).
- [[MOC - Container Networking Model]] (Architecture Index).
