---
aliases: []
confidence: 
created: 2025-10-26T17:05:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [api, architecture, tech]
title: An API Gateway is a Central Management Layer for APIs
type: permanent
uid: 
updated: 
version: 1
---

An API Gateway acts as a single, centralized entry point for all API requests, providing a management and security layer that sits in front of backend services.

Its primary responsibilities include:

- **Authentication & Authorization**: Verifying the identity of clients and ensuring they have permission to access the requested resources.
- **Rate Limiting**: Protecting backend services from being overwhelmed by enforcing usage policies.
- **Routing**: Directing incoming API requests to the appropriate backend service or microservice.
- **Protocol & Payload Transformation**: Translating between different protocols or modifying request/response payloads for compatibility.

By handling these cross-cutting concerns, an API Gateway simplifies the architecture of backend services, allowing them to focus solely on their core business logic. Common examples include AWS API Gateway, Kong, and Apigee.

## Related Concepts

- [[A Load Balancer Distributes Traffic for Reliability and Scale]]
- [[Architectural Patterns for API Gateways and Load Balancers]]
- [[Machine-to-Machine Authentication Methods]]
- [[Services]]
