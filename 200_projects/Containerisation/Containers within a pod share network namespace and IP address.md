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
tags: [container, localhost, network-namespace, pod, topic/technology/containers, topic/technology/kubernetes, type/fact]
title: Containers within a pod share network namespace and IP address
type: Fact
uid: 
updated: 
version: 1
---

## Summary

Containers within the same Kubernetes pod share a network namespace and IP address, allowing them to communicate using localhost or the pod's IP, as if they were processes running on the same machine.

## Details

- **Shared Resources**: Containers in a pod share network namespaces, storage volumes, and process IDs
- **Communication**: Containers can communicate using `localhost:port` or the pod's IP address
- **Example**: A web server on port 80 can access a database on port 3306 using `localhost:3306`
- **Isolation**: Each pod has its own network namespace, separate from other pods and the host
- **Network Stack**: The shared namespace includes network interfaces, routing tables, and firewall rules

## Implications

- **Simplified Development**: No need for service discovery between containers in the same pod
- **Performance**: Local communication avoids network overhead
- **Port Conflicts**: Containers in the same pod cannot use the same port
- **Security**: All containers share the same network security context

## Related

- [[What is a network namespace]] - Linux primitive that enables pod isolation
- [[MOC - Container Networking Model]] - Deeper networking fundamentals
- [[Pods communicate across cluster using CNI-provided networking]] - Cluster-level communication
