---
aliases: []
confidence: 
created: 2025-07-10T13:05:06Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Services
type:
uid: 
updated: 
version:
---

- Purpose: Kubernetes Services provide a stable, internal load balancing abstraction for a set of pods, abstracting away their ephemeral nature and fluctuating IP addresses. They ensure that clients can reliably discover and connect to application instances, even as pods are created, deleted, or replaced.
- Precision/Accuracy: Different service types offer various levels of traffic control and exposure:
- ClusterIP: Provides an internal-only virtual IP address that routes traffic to matching, ready pods within the cluster. `kube-proxy` is responsible for making this IP route to the applicable pods. This is the default service type.
- NodePort: Exposes a service on a fixed port across all cluster nodes, allowing external access by knowing any node's IP and the NodePort. This is often used with external load balancers.
- LoadBalancer: Extends NodePort by integrating with a cloud provider's external load balancer, which then handles external traffic routing to the nodes/pods. This type typically handles L4 traffic (TCP/UDP).
- ExternalName: Maps a service to an arbitrary DNS name, providing a CNAME record instead of a cluster IP.
- Strategic Recommendation: Choose the service type that precisely matches the intended accessibility and traffic pattern. For internal microservices, ClusterIP is appropriate. For external exposure, `LoadBalancer` or `Ingress` (discussed next) are preferred, leveraging cloud-native load balancing for performance and scalability.

[[Kubernetes-Native Abstractions for Traffic Control]]
