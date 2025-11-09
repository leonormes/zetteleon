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
tags: [iptables, ipvs, kube-proxy, load-balancing, service, topic/technology/containers, topic/technology/kubernetes, type/fact]
title: kube-proxy implements Services using iptables or IPVS
type: Fact
uid: 
updated: 
version: 1
---

## Summary

kube-proxy runs on each Kubernetes node and implements Services by configuring iptables or IPVS rules to provide stable IP addresses and load balancing for pods, operating in different modes with varying performance characteristics.

## Details

### Kube-proxy Role
- **Node-Level Proxy**: Runs on every node in the cluster
- **Service Implementation**: Provides stable IP addresses for pod groups
- **Load Balancing**: Distributes traffic across healthy pod endpoints
- **Service Discovery**: Enables reliable service-to-service communication

### Operating Modes

**Userspace Mode (Legacy):**
- Acts as Layer 4 proxy in userspace
- Forwards traffic to appropriate pods
- Higher latency and resource usage
- Largely deprecated in modern clusters

**iptables Mode:**
- Uses iptables rules to redirect traffic
- Better performance than userspace
- Can have scalability issues with many services
- Default mode in many Kubernetes versions

**IPVS Mode:**
- Uses IPVS (IP Virtual Server) for load balancing
- Best performance and scalability
- Supports multiple load balancing algorithms
- Recommended for large-scale deployments

### Service Types Handled
- **ClusterIP**: Internal service access
- **NodePort**: External access via node ports
- **LoadBalancer**: External load balancer integration
- **ExternalName**: DNS alias for external services

### Monitoring and Updates
- **Watches API Server**: Monitors Service and Endpoint changes
- **Dynamic Updates**: Automatically updates rules when pods/services change
- **Health Checking**: Only routes traffic to healthy endpoints

## Related

- [[MOC - Container Runtime & Orchestration]] - kube-proxy in orchestration context
- What are iptables chains and tables? - Underlying networking mechanism
- [[Kubernetes provides NodePort and LoadBalancer for external service access]] - Service types implemented
