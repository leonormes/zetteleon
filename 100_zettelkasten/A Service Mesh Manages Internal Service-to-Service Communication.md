---
aliases: []
confidence: 
created: 2025-10-26T17:09:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, microservices, networking, tech]
title: A Service Mesh Manages Internal Service-to-Service Communication
type: permanent
uid: 
updated: 
version: 1
---

A Service Mesh is a dedicated infrastructure layer that manages communication between services or microservices within a network. Unlike an API Gateway, which handles north-south traffic (client-to-service), a Service Mesh is primarily concerned with east-west traffic (service-to-service).

It works by deploying a lightweight proxy, known as a "sidecar," alongside each service instance. These proxies intercept all network communication, providing powerful features without requiring any changes to the application code itself.

Key functions of a Service Mesh include:

- **Observability**: Gathers detailed metrics, logs, and traces on inter-service communication.
- **Traffic Management**: Provides sophisticated routing, load balancing, and traffic shaping (e.g., canary deployments, A/B testing).
- **Security**: Enforces mutual TLS (mTLS) for secure communication and provides identity-based authorization.
- **Reliability**: Implements automatic retries, circuit breaking, and timeouts to improve fault tolerance.

Common examples include Istio and Linkerd. A Service Mesh complements API Gateways and Load Balancers by providing a granular level of control and visibility over the internal service landscape.

## Related Concepts

- [[An API Gateway is a Central Management Layer for APIs]]
- [[Services]]
