---
aliases: []
confidence: 
created: 2025-10-26T17:06:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, networking, scalability, tech]
title: A Load Balancer Distributes Traffic for Reliability and Scale
type: permanent
uid: 
updated: 
version: 1
---

A Load Balancer is a core infrastructural component that distributes incoming network traffic across multiple backend servers to ensure high availability, scalability, and fault tolerance.

Its primary purpose is to prevent any single server from becoming a bottleneck, thereby improving application responsiveness and reliability.

There are two main types:

- **Network Load Balancer (Layer 4)**: Operates at the transport layer (TCP/UDP). It is protocol-agnostic and provides ultra-low latency and high throughput, making it ideal for performance-sensitive applications like gaming or financial services.
- **Application Load Balancer (Layer 7)**: Operates at the application layer (HTTP/HTTPS). It is content-aware and can make intelligent routing decisions based on URL paths, HTTP headers, or query parameters, which is highly effective for microservices-based architectures.

## Related Concepts

- [[An API Gateway is a Central Management Layer for APIs]]
- [[Architectural Patterns for API Gateways and Load Balancers]]
- [[What is an AWS Application Load Balancer (ALB)]]
- [[AWS ALB Target Groups]]

## Use Cases

- **Enterprise Applications**: Distributing traffic for web applications, APIs, and other services to ensure high availability and scalability.
- **Home Networks**: In a home lab, a load balancer can expose multiple internal services (like Plex, NAS, or development servers) securely through a single public IP and port (typically 443). This improves security by minimizing the number of open ports on a router.
