---
aliases: []
confidence: "null"
created: 2025-10-26T17:22:00Z
epistemic: "null"
last_reviewed: "null"
modified: 2025-12-31T23:08:47+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["cluster-state", "configuration", "etcd", "service-discovery", "topic/technology/containers", "topic/technology/kubernetes"]
title: etcd stores cluster network state and service configuration
type: "Fact"
uid: 
updated: 
version: "1"
---

## Summary

etcd serves as Kubernetes' distributed key-value store, maintaining cluster state and network configuration data to ensure all nodes have a consistent view of services, endpoints, and network policies.

## Details

### Core Responsibilities

- **State Storage**: Stores cluster-wide configuration and state data
- **Service Discovery**: Maintains Service definitions and Endpoint information
- **Consistency**: Ensures all nodes have identical network configuration view
- **Configuration Source**: Acts as single source of truth for network settings

### Network-Related Data Stored

- **Service Definitions**: ClusterIP, ports, selector information
- **Endpoint Information**: Pod IPs and ports for service backends
- **Network Policies**: Traffic control rules and pod selectors
- **Configuration**: Cluster network settings, CIDR blocks, plugin configs

### Consistency Mechanisms

- **Distributed Consensus**: Raft algorithm for data consistency across nodes
- **Watch API**: Components watch for changes in real-time
- **Event Propagation**: Network changes propagate to all cluster components
- **Recovery**: Cluster state recovery from etcd backups

### Component Integration

- **kube-apiserver**: Reads/writes network configuration via etcd
- **kube-proxy**: Watches service/endpoint changes for rule updates
- **CNI Plugins**: May read network configuration from etcd
- **Controllers**: Use etcd for desired vs actual state reconciliation

## High Availability Considerations

- **Cluster Size**: Typically 3 or 5 nodes for quorum
- **Backup Strategy**: Regular snapshots for disaster recovery
- **Network Latency**: Critical for cluster responsiveness
- **Storage Performance**: Impacts overall cluster performance

## Related

- [[MOC - Container Runtime & Orchestration]] - etcd in orchestration architecture
- [[Kube-Proxy Implements Services Using Iptables or IPVS]] - How kube-proxy uses etcd data
- [[Pods communicate across cluster using CNI-provided networking]] - Network configuration storage
