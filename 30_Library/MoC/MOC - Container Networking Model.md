---
aliases: []
confidence: "High"
created: 2025-10-24T15:00:00Z
epistemic: "Map"
last_reviewed: "2025-12-30"
modified: 2025-12-30T13:55:01+00:00
purpose: "To map the foundational Linux networking primitives to their Kubernetes abstractions."
review_interval: "1 year"
see_also: ["[[SoT - Linux Networking Primitives]]", "[[SoT - Kubernetes Networking & DNS]]"]
source_of_truth: ["[[SoT - Linux Networking Primitives]]", "[[SoT - Linux Container Primitives]]", "[[SoT - Kubernetes Networking & DNS]]"]
status: "stable"
tags: ["topic/technology/containers", "k8s", "kubernetes", "topic/linux", "topic/technology/networking"]
title: MOC - Container Networking Model
type: "map"
uid: 
updated: 
version: "2"
---

**Links:**

- Up: [[MOC - Containerisation]]
- Related: [[SoT - Linux Networking Primitives]], [[SoT - Linux Container Primitives]], [[SoT - Kubernetes Networking & DNS]]

## Summary

A comprehensive Map of Content (MOC) connecting the low-level Linux networking primitives (Veth, Bridges, IPTables) defined in **[[SoT - Linux Networking Primitives]]** to their high-level Kubernetes abstractions (Services, Ingress, CNI) defined in **[[SoT - Kubernetes Networking & DNS]]**.

## Context / Problem

Kubernetes networking appears magical—Pods communicate seamlessly across nodes without manual NAT configuration. This abstraction hides critical Linux primitives that CNI plugins automate. Without understanding these building blocks (network namespaces, veth pairs, bridges, routing, iptables), debugging container connectivity issues or designing custom network policies becomes impossible.

## Model

### Core Linux Primitives

Container networking relies on the "Trinity of Containerisation" and specific networking constructs defined in our Source of Truth notes:

**Isolation & Environment:**
1. **[[SoT - Linux Container Primitives#A. Namespaces (Isolation)|Network Namespace]]** - Isolated network stack per container.
2. **[[SoT - Container Isolation (The Namespace Security Model)|Mount Namespace]]** - The primary security gatekeeper.

**Connectivity Mechanics (See [[SoT - Linux Networking Primitives]]):**
3. **Veth Pair:** The virtual cable tunneling traffic from Host to Container.
4. **Linux Bridge:** The virtual Layer 2 switch (`cni0`) connecting Pods on the same node.
5. **IPTables/NAT:** The mechanism for Masquerading (Source NAT) for egress and DNAT for Services.
6. **IP Forwarding:** The kernel flag (`net.ipv4.ip_forward`) permitting packet routing.

### Architecture Layers

```sh
┌─────────────────────────────────────────┐
│         Application Layer               │
│      (Pod-to-Pod communication)         │
│  See: [[SoT - Kubernetes Networking & DNS]]
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         CNI Plugin Layer                │
│  (Calico, Flannel, bridge, etc.)        │
│  - Creates veth pairs                   │
│  - Assigns IPs (IPAM)                   │
│  - Configures routes                    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Linux Kernel Networking            │
│  See: [[SoT - Linux Networking Primitives]]
│  - Network namespaces                   │
│  - veth devices                         │
│  - Linux bridges (cni0)                 │
│  - iptables rules                       │
└─────────────────────────────────────────┘
```

### Mapping to Kubernetes

| Linux Primitive | K8s Equivalent | Managed By |
|-----------------|----------------|------------|
| Network namespace | Pod network namespace | kubelet |
| veth pair | Pod eth0 ↔ Node bridge | CNI plugin |
| Linux bridge (cni0) | Node bridge | CNI plugin |
| IP address assignment | Pod CIDR allocation | IPAM plugin |
| iptables rules | Service routing, NetworkPolicy | kube-proxy, CNI |

## Connections / Implications

### Debugging & Troubleshooting

- **Connectivity Breaks:** Most "Kubernetes Networking" issues are actually Linux networking issues.
    - Check **IP Forwarding** on the host.
    - Check **IPTables** chains for dropped packets.
    - Check **Bridge** FDB (Forwarding Database) for MAC learning issues.
- **Security:** Network Policies are often implemented as IPTables chains or eBPF programs (Cilium).

### Cross-Domain Connections

- **[[MOC - OSI Model]]**: Container networking operates across OSI Layers 2-4.
- **[[SoT - Container Isolation (The Namespace Security Model)]]**: Security implications of sharing the host network namespace.

---

## Child Notes (Key Sources of Truth)

**Foundations:**
- [[SoT - Linux Networking Primitives]] (Veth, Bridge, IPTables)
- [[SoT - Linux Container Primitives]] (Namespaces, Cgroups)
- [[SoT - Container Isolation (The Namespace Security Model)]] (Security)

**Orchestration:**
- [[SoT - Kubernetes Networking & DNS]] (Services, Ingress, CNI)
- [[SoT - Cloud Networking Core Components]] (Cloud Integration)
