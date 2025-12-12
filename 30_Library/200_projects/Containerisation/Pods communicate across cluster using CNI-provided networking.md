---
aliases: []
confidence: 
created: 2025-10-26T17:19:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cluster-networking, cni, overlay, pod, topic/technology/containers, topic/technology/kubernetes, type/fact, underlay]
title: Pods communicate across cluster using CNI-provided networking
type: Fact
uid: 
updated: 
version: 1
---

## Summary

Pods in a Kubernetes cluster communicate across nodes using the Container Network Interface (CNI), which creates a virtual network overlay or underlay that enables seamless IP-to-IP communication regardless of pod location.

## Details

### CNI Plugin Role

- **Standard Interface**: CNI provides a consistent interface between container runtimes and network plugins
- **Network Configuration**: CNI plugins assign IP addresses and set up network interfaces and routing
- **Plugin Invocation**: kubelet invokes CNI plugins when pods are created
- **Popular Plugins**: Calico, Flannel, Weave

### Network Models

**Overlay Networks:**

- Encapsulate traffic within another protocol
- Create virtual network over physical infrastructure
- Allow pods on different nodes to communicate as if on same network
- Examples: VXLAN, Geneve

**Underlay Networks:**

- Operate at physical network layer
- Use routing techniques for cross-node connectivity
- Better performance but more complex configuration
- Examples: BGP routing, direct routing

### DNS Integration

- Kubernetes provides built-in DNS service
- Pods can communicate using service names instead of IP addresses
- Simplifies application development and network management

## Implications

- **Location Independence**: Pods can be scheduled on any node without network reconfiguration
- **Scalability**: Network scales automatically with cluster growth
- **Plugin Flexibility**: Different CNI plugins for different use cases (performance, security, features)

## Related

- [[What is the Container Network Interface (CNI)?]] - CNI specification details
- [[MOC - Container Runtime & Orchestration]] - How CNI fits into orchestration
- [[30_Library/200_projects/Containerisation/Containers within a pod share network namespace and IP address]] - Pod-level communication
