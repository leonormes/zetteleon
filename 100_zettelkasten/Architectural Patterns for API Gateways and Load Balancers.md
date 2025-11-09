---
aliases: []
confidence: 
created: 2025-10-26T17:08:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, design-patterns, tech]
title: Architectural Patterns for API Gateways and Load Balancers
type: permanent
uid: 
updated: 
version: 1
---

API Gateways and Load Balancers are often used together in layered architectural patterns to combine their respective strengths in reliability and API management.

## 1. Load Balancer → API Gateway

This is a common pattern for public-facing applications where high availability is critical.

- **Flow**: Internet Traffic → Load Balancer → API Gateway Instances → Backend Services
- **Purpose**: The Load Balancer provides DDoS protection, SSL termination, and distributes traffic across multiple instances of the API Gateway, ensuring the management layer itself is fault-tolerant.

## 2. API Gateway → Load Balancer

This pattern is preferred in microservices architectures where centralized control is needed before traffic enters the internal network.

- **Flow**: Internet Traffic → API Gateway → Internal Load Balancer → Backend Microservices
- **Purpose**: The API Gateway acts as the primary entry point, handling authentication, rate limiting, and routing. Once validated, it forwards traffic to an internal Load Balancer that manages the distribution to different backend service clusters.

## 3. Multi-Tier Setup

This advanced pattern provides maximum separation of concerns.

- **Flow**: Internet Traffic → Network Load Balancer (L4) → API Gateway → Application Load Balancer (L7) → Backend Services
- **Purpose**: The NLB handles raw, high-throughput traffic. The API Gateway enforces business and security rules. The internal ALB provides sophisticated, application-aware routing to the microservices.

## Related Concepts

- [[An API Gateway is a Central Management Layer for APIs]]
- [[A Load Balancer Distributes Traffic for Reliability and Scale]]
