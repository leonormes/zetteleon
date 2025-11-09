---
aliases: []
confidence: 
created: 2025-10-26T17:22:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [istio, linkerd, observability, security, service-mesh, topic/technology/containers, topic/technology/kubernetes, traffic-management, type/fact]
title: Service mesh provides advanced traffic management and security for service communication
type: Fact
uid: 
updated: 
version: 1
---

## Summary

A service mesh is a dedicated infrastructure layer that controls and monitors service-to-service communication within Kubernetes clusters, providing traffic management, security policies, and observability features beyond basic Kubernetes networking.

## Details

### Core Capabilities
- **Traffic Management**: Advanced routing, load balancing, and traffic splitting
- **Security**: mTLS encryption, certificate management, access policies
- **Observability**: Metrics, tracing, and logging for service communication
- **Resilience**: Circuit breaking, retries, timeouts, and fault injection

### Architecture Components
- **Data Plane**: Sidecar proxies (Envoy) intercepting all service traffic
- **Control Plane**: Manages proxy configuration and policy distribution
- **Ingress/Egress**: Gateway management for cluster edge traffic
- **Certificate Authority**: Automated mTLS certificate lifecycle

### Traffic Management Features
- **Request Routing**: Route based on headers, paths, or weighted percentages
- **Load Balancing**: Multiple algorithms (round-robin, least requests, etc.)
- **Traffic Splitting**: Canary deployments, A/B testing, blue-green deployments
- **Fault Tolerance**: Automatic retries, timeouts, circuit breaking

### Security Features
- **Zero Trust Network**: mTLS encryption for all service communication
- **Identity-Based Access**: Service identity and authorization policies
- **Certificate Management**: Automated rotation and revocation
- **Compliance**: Auditing and policy enforcement

### Popular Implementations
- **Istio**: Full-featured service mesh with extensive ecosystem
- **Linkerd**: Lightweight, Rust-based data plane focused on simplicity
- **Consul Connect**: HashiCorp's service mesh with broader service discovery
- **AWS App Mesh**: AWS-native service mesh integration

### Integration with Kubernetes
- **CNI Integration**: Works with existing CNI plugins
- **Service Discovery**: Enhances Kubernetes service discovery
- **Network Policies**: Complements Kubernetes NetworkPolicy
- **Ingress**: Can replace or enhance Ingress controllers

## Related

- [[Network policies control traffic flow between pods using labels and namespaces]] - Kubernetes-native security
- [[MOC - Container Runtime & Orchestration]] - Service mesh in orchestration context
- [[Pods communicate across cluster using CNI-provided networking]] - Underlying network foundation
