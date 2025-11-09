---
aliases: []
confidence: 0.9
created: 2025-10-31T11:50:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T11:50:00Z
purpose: "Explain Kubernetes pod networking."
review_interval: 90
see_also: ["NAT Gateways Enable Private Resources to Access Internet.md"]
source_of_truth: []
status: seedling
tags: [kubernetes, networking]
title: Containers Within a Pod Share Network Namespace and IP Address
type: concept
uid: 
updated: 
---

## Containers Within a Pod Share Network Namespace and IP Address

**Summary:** Kubernetes pods implement shared networking between containers via Linux namespaces, allowing:
- Single IP address per pod
- Localhost communication between containers
- Shared network interfaces

**Implementation:**
- Each pod gets its own network namespace
- Containers share pod's virtual ethernet interface
- CNI plugins configure pod networking

**Benefits:**
- Simplified service discovery
- Efficient resource usage
- Consistent networking model
