---
aliases: []
confidence:
created: 2025-10-24T15:00:00Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:27Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [container, k8s, kubernetes, linux, topic/technology/networking, type/model]
title: MOC - Container Networking Model
type: map
uid:
updated:
version: 1
---

**Links:**

- Up: [[MOC - Containerisation]]
- Related: [[What is a network namespace]], [[What is a veth pair]], [[What is a Linux bridge]], [[What is iptables NAT MASQUERADE]]

## Summary

A comprehensive Map of Content (MOC) for understanding how Linux networking primitives (namespaces, veth pairs, bridges, iptables) form the foundation of container networking and map to Kubernetes CNI plugins and network policies.

## Context / Problem

Kubernetes networking appears magical—Pods communicate seamlessly across nodes without manual NAT configuration. This abstraction hides critical Linux primitives that CNI plugins automate. Without understanding these building blocks (network namespaces, veth pairs, bridges, routing, iptables), debugging container connectivity issues or designing custom network policies becomes impossible. This MOC serves as the entry point for building a mental model from first principles.

## Model

### Core Linux Primitives

Container networking AND isolation is built on these fundamental Linux constructs:

**Namespace Types:**

1. **[[What is a network namespace|Network Namespace]]** - Isolated network stack per container
2. **[[What is a mount namespace|Mount Namespace]]** - Isolated file system mount points
3. **[[What is a PID namespace|PID Namespace]]** - Isolated process ID space
4. **[[What is a UTS namespace|UTS Namespace]]** - Isolated hostname and domain name

**Networking Primitives:**

5. **[[What is a veth pair|Veth Pair]]** - Virtual Ethernet cable connecting namespaces
6. **[[What is a Linux bridge|Linux Bridge]]** - Virtual Layer 2 switch for multi-container connectivity
7. **[[What is iptables NAT MASQUERADE|iptables MASQUERADE]]** - Source NAT for container egress traffic
8. **[[What is IP forwarding|IP Forwarding]]** - Kernel packet routing between interfaces

**Supporting Infrastructure:**

9. **[[What is the Linux VFS (Virtual File System)|Linux VFS]]** - Abstraction layer for file systems

### Key Mechanisms

How these primitives work together:

**Namespace Management:**

- **[[How to create and connect network namespaces]]** - Building isolated Pod-like environments
- **[[How namespaces interact without mount namespace]]** - Understanding incomplete isolation scenarios

**Network Connectivity:**

- **[[How a veth pair connects two network namespaces]]** - Point-to-point Pod communication
- **[[How to set up a Linux bridge for container networking]]** - Multi-Pod same-node networking
- **[[How a packet exits a container via NAT]]** - Container-to-internet egress flow
- [[How Linux bridge learns MAC addresses]] - Layer 2 forwarding mechanics

### Architecture Layers

```sh
┌─────────────────────────────────────────┐
│         Application Layer               │
│      (Pod-to-Pod communication)         │
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
│  - Network namespaces                   │
│  - veth devices                         │
│  - Linux bridges (cni0)                 │
│  - iptables rules                       │
│  - Routing tables                       │
└─────────────────────────────────────────┘
```

### Mapping to Kubernetes

See **[[Model - Linux to Kubernetes Networking Mapping]]** for the complete translation table between Linux primitives and Kubernetes components.

| Linux Primitive | K8s Equivalent | Managed By |
|-----------------|----------------|------------|
| Network namespace | Pod network namespace | kubelet |
| veth pair | Pod eth0 ↔ Node bridge | CNI plugin |
| Linux bridge (cni0) | Node bridge | CNI plugin |
| IP address assignment | Pod CIDR allocation | IPAM plugin |
| iptables rules | Service routing, NetworkPolicy | kube-proxy, CNI |

## Connections / Implications

### What This Model Enables

- **Debugging**: Trace packet flows from Pod through veth → bridge → iptables → external network
- **Design**: Understand trade-offs between CNI plugins (overlay vs native routing)
- **Troubleshooting**: Identify where connectivity breaks (namespace isolation, bridge config, NAT rules)
- **Security**: Implement network policies by understanding underlying iptables mechanics

### What Breaks If Components Fail

- **No network namespace**: Pods share host network, losing isolation
- **Veth pair missing**: Pod cannot communicate even on same node
- **Bridge misconfigured**: Pods cannot discover each other locally
- **iptables NAT broken**: Pods cannot reach external services
- **IP forwarding disabled**: Packets cannot route between interfaces

### Cross-Domain Connections

- **[[MOC - OSI Model]]**: Container networking operates across OSI Layers 2-4

## Questions / To Explore

### Factual Gaps

- [[What is the CNI specification?]]
- [[What is IPAM in CNI?]]
- [[What is the cni0 bridge?]]
- [[What is kube-proxy?]]
- [[What are iptables chains and tables?]]

### Mechanism Gaps

- [[How does kubelet invoke CNI plugins?]]
- [[How does kube-proxy generate iptables rules for Services?]]
- [[How does Calico implement network policies with iptables?]]
- [[How does Flannel VXLAN encapsulate packets for cross-node traffic?]]
- [[How does CoreDNS resolve Service names to ClusterIPs?]]

### Debugging Scenarios

- [[DEBUG - Pod cannot ping other Pods on same node]]
- [[DEBUG - Pod can reach same-node Pods but not cross-node]]
- [[DEBUG - Pod cannot resolve DNS names]]
- [[DEBUG - Service ClusterIP unreachable from Pods]]

### Applied Learning

- [[Lab - Build Container Network from Scratch]] (hands-on tutorial)
- [[INSIGHT - Networking is data labeling not wires]]
- [[INSIGHT - CNI plugins are just automation of manual ip commands]]

---

## Child Notes (Generated from This MOC)

### Facts
**Namespaces:**

- [[What is a network namespace]]
- [[What is a mount namespace]]
- [[What is a PID namespace]]
- [[What is a UTS namespace]]
- [[What is the Linux VFS (Virtual File System)]]

**Networking:**

- [[What is a veth pair]]
- [[What is a Linux bridge]]
- [[What is iptables NAT MASQUERADE]]
- [[What is IP forwarding]]
- [[What is ARP]]

### Mechanisms

- [[How to create and connect network namespaces]]
- [[How namespaces interact without mount namespace]]
- [[How a veth pair connects two network namespaces]]
- [[How to set up a Linux bridge for container networking]]
- [[How a packet exits a container via NAT]]
- [[How Linux bridge learns MAC addresses]]

### Models

- [[Model - Linux to Kubernetes Networking Mapping]]
- [[Pods communicate across cluster using CNI-provided networking]] - CNI network models
- [[CNI plugins provide different network models and features]] - Plugin comparison
- [[MOC - OSI Model]] (related)

### Insights

- [[Lab - Build Container Network from Scratch]]
- [[INSIGHT - Networking is data labeling]]
- [[Namespace Isolation Is Incomplete Without Mount Namespace]]
- [[DEBUG - Common veth and bridge setup issues]]

### Kubernetes Orchestration

- [[30_Library/200_projects/Containerisation/Containers within a pod share network namespace and IP address]] - Pod communication
- [[Network policies control traffic flow between pods using labels and namespaces]] - Security policies
- [[kube-proxy implements Services using iptables or IPVS]] - Service implementation
- [[Kubernetes provides NodePort and LoadBalancer for external service access]] - External access
- [[Container runtime configures pod networking through CNI plugins]] - Runtime responsibilities
- [[etcd stores cluster network state and service configuration]] - State management
- [[Service mesh provides advanced traffic management and security for service communication]] - Advanced communication
- [[Kubernetes networking components coordinate through a defined workflow]] - Component coordination
