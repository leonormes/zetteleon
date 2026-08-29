---
aliases: []
created: 2025-10-24T15:00:00+00:00
modified: 2026-08-29T09:36:29+00:00
permalink: llmeon/30-library/mo-c/moc-container-networking-model
tags: [k8s, kubernetes, SoftwareEngineering/Containers, SoftwareEngineering/Linux, SoftwareEngineering/Networking]
title: MOC - Container Networking Model
---

Links:

- Up: [[MOC - Containerisation]]
- Related: [[SoT - Linux Networking Primitives]], [[SoT - Linux Container Primitives]], [[SoT - Kubernetes Networking & DNS]]

## Summary

A comprehensive Map of Content (MOC) connecting the low-level Linux networking primitives (Veth, Bridges, IPTables) defined in [[SoT - Linux Networking Primitives]] to their high-level Kubernetes abstractions (Services, Ingress, CNI) defined in [[SoT - Kubernetes Networking & DNS]].

## Context / Problem

Kubernetes networking appears magical—Pods communicate seamlessly across nodes without manual NAT configuration. This abstraction hides critical Linux primitives that CNI plugins automate. Without understanding these building blocks (network namespaces, veth pairs, bridges, routing, iptables), debugging container connectivity issues or designing custom network policies becomes impossible.

## Model

### Core Linux Primitives

Container networking relies on the "Trinity of Containerisation" and specific networking constructs defined in our Source of Truth notes:

Isolation & Environment:

1. [[SoT - Linux Container Primitives#A. Namespaces (Isolation)|Network Namespace]] - Isolated network stack per container.
2. [[SoT - Linux Container Internals|Mount Namespace]] - The primary security gatekeeper.

Connectivity Mechanics (See [[SoT - Linux Networking Primitives]]):

1. Veth Pair: The virtual cable tunneling traffic from Host to Container.
2. Linux Bridge: The virtual Layer 2 switch (`cni0`) connecting Pods on the same node.
3. IPTables/NAT: The mechanism for Masquerading (Source NAT) for egress and DNAT for Services.
4. IP Forwarding: The kernel flag (`net.ipv4.ip_forward`) permitting packet routing.

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

- Connectivity Breaks: Most "Kubernetes Networking" issues are actually Linux networking issues.
    - Check IP Forwarding on the host.
    - Check IPTables chains for dropped packets.
    - Check Bridge FDB (Forwarding Database) for MAC learning issues.
- Security: Network Policies are often implemented as IPTables chains or eBPF programs (Cilium).

### Cross-Domain Connections

- [[MOC - OSI Model]]: Container networking operates across OSI Layers 2-4.
- [[SoT - Linux Container Internals]]: Security implications of sharing the host network namespace.

---

## Child Notes (Key Sources of Truth)

Foundations:

- [[SoT - Linux Networking Primitives]] (Veth, Bridge, IPTables)
- [[SoT - Linux Container Primitives]] (Namespaces, Cgroups)
- [[SoT - Linux Container Internals]] (Security)

Orchestration:

- [[SoT - Kubernetes Networking & DNS]] (Services, Ingress, CNI)
- [[SoT - Cloud Networking Core Components]] (Cloud Integration)

## ## Model

### Core Source of Truth (SoT)

- [[SoT - Kubernetes Networking Model]] - flat address space, invariants, and node bridges.
- [[SoT - Calico CNI Architecture]] - Felix, eBPF, VXLAN vs IP-in-IP.
