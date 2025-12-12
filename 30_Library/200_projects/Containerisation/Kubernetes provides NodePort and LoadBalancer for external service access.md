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
tags: [external-access, loadbalancer, nodeport, service, topic/technology/containers, topic/technology/kubernetes, type/fact]
title: Kubernetes provides NodePort and LoadBalancer for external service access
type: Fact
uid: 
updated: 
version: 1
---

## Summary

Kubernetes enables external access to cluster services through NodePort and LoadBalancer service types, providing different mechanisms for exposing applications outside the cluster.

## Details

### NodePort Service

- **Static Port Allocation**: Exposes service on same static port on every node
- **Traffic Forwarding**: Any traffic sent to the node's IP on the specified port is forwarded to the service
- **Port Range**: Typically uses ports 30000-32767
- **Use Case**: Simple external access, development, testing
- **Limitation**: Requires knowing node IP addresses, not suitable for production alone

### LoadBalancer Service

- **Cloud Integration**: Provisions external load balancer in underlying cloud environment
- **Stable External IP**: Provides dedicated external IP address that routes to the service
- **Automatic Scaling**: Load balancer handles traffic distribution across multiple nodes
- **Use Case**: Production applications, high availability scenarios
- **Cloud Dependency**: Requires cloud provider support (AWS ELB, GCP Load Balancer, Azure Load Balancer)

## Service Type Selection

**Choose NodePort when:**

- Development or testing environments
- Simple external access needed
- Cloud load balancer not available or required
- Direct node access is acceptable

**Choose LoadBalancer when:**

- Production workloads
- High availability required
- Automatic failover needed
- Cloud-native deployment

## Related

- [[MOC - Container Runtime & Orchestration]] - Service implementation details
- [[kube-proxy implements Services using iptables or IPVS]] - How service routing works
- [[Pods communicate across cluster using CNI-provided networking]] - Internal cluster communication
