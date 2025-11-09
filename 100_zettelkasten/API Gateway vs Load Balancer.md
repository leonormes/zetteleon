---
aliases: []
confidence: 
created: 2025-10-26T17:07:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, comparison, tech]
title: API Gateway vs Load Balancer
type: permanent
uid: 
updated: 
version: 1
---

While both API Gateways and Load Balancers manage traffic, they operate at different levels and serve distinct purposes.

| Aspect             | Load Balancer                                       | API Gateway                                                  |
| :----------------- | :-------------------------------------------------- | :----------------------------------------------------------- |
| **Main Function**  | Distributes traffic for reliability and scalability | Manages, secures, and routes API requests                    |
| **OSI Layer**      | Layer 4 (Transport) or Layer 7 (Application)        | Layer 7 (Application) only                                   |
| **Protocol**       | TCP, UDP, HTTP/S (protocol-agnostic at L4)          | HTTP/S, WebSocket, gRPC (protocol-aware)                     |
| **Core Focus**     | Ensures fault tolerance and uptime                  | Enforces security, routing logic, and usage policies for APIs |

In essence, a Load Balancer ensures that traffic *reaches* a server, while an API Gateway ensures that the traffic is *authorized, well-formed, and correctly routed* before it reaches the backend service.

## Related Concepts

- [[An API Gateway is a Central Management Layer for APIs]]
- [[A Load Balancer Distributes Traffic for Reliability and Scale]]
