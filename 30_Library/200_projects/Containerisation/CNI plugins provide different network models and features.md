---
aliases: []
confidence: 
created: 2025-10-26T17:19:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, cni, flannel, overlay, topic/technology/containers, topic/technology/kubernetes, type/fact, underlay, weave]
title: CNI plugins provide different network models and features
type: Fact
uid: 
updated: 
version: 1
---

## Summary

Different CNI plugins offer varying network models (overlay/underlay) and feature sets, allowing Kubernetes clusters to choose networking solutions based on performance, security, and operational requirements.

## Popular CNI Plugins

### Calico

- **Network Model**: Overlay and Underlay support
- **Key Features**: Policy enforcement, BGP routing, IPAM
- **Security**: Advanced network policy support
- **Performance**: High performance with BGP routing
- **Use Case**: Enterprise environments requiring strong security and performance

### Flannel

- **Network Model**: Overlay only
- **Key Features**: VXLAN encapsulation, simple configuration
- **Configuration**: Uses Kubernetes API or etcd for backend
- **Simplicity**: Easy to set up and maintain
- **Use Case**: Development, testing, simple production deployments

### Weave

- **Network Model**: Overlay
- **Key Features**: Encrypted traffic, cross-cluster connectivity
- **Security**: Built-in encryption for data in transit
- **Flexibility**: Works across multiple clusters
- **Use Case**: Multi-cluster deployments, security-focused environments

### Selection Criteria

**Performance Requirements:**

- Calico (underlay) for highest performance
- Flannel for moderate performance with simplicity
- Weave when encryption is needed

**Security Needs:**

- Calico for advanced network policies
- Weave for built-in encryption
- Flannel for basic security

**Operational Complexity:**

- Flannel for simplest setup
- Calico for enterprise features
- Weave for multi-cluster scenarios

## Implementation Considerations

- **Network Policy Support**: Not all plugins support NetworkPolicy
- **IPAM Integration**: IP address management varies by plugin
- **Monitoring**: Different observability capabilities
- **Upgrade Path**: Consider long-term maintenance

## Related

- What is the Container Network Interface (CNI)? - CNI specification
- [[Pods communicate across cluster using CNI-provided networking]] - How CNI enables cluster networking
- [[MOC - Container Runtime & Orchestration]] - CNI in orchestration context
