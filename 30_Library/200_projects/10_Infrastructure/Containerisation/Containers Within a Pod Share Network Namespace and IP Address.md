---
aliases: []
confidence: "null"
created: 2025-10-26T17:19:00Z
epistemic: "null"
id: "Containers within a pod share network namespace and IP address"
last_reviewed: "null"
modified: 2026-01-03T10:19:27+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["SoftwareEngineering/Containers", "localhost", "network-namespace", "pod", "SoftwareEngineering/Containers", "SoftwareEngineering/Kubernetes"]
title: Containers Within a Pod Share Network Namespace and IP Address
type: "Fact"
uid: 
updated: 
version: "1"
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
