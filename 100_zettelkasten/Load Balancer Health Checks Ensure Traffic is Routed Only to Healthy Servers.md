---
aliases: []
confidence: 0.9
created: 2025-10-31T09:25:27Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T09:31:41Z
purpose: "Explain the role and importance of health checks in load balancing."
review_interval: 90
see_also: ["AWS ALB Target Groups.md"]
source_of_truth: []
status: seedling
tags: [load-balancing, networking, reliability]
title: Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers
type: concept
uid: 
updated: 
---

## Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers

**Summary:** Health checks are automated tests that a load balancer performs to determine if a backend server is available and operating correctly before sending traffic to it.

**Details:** The load balancer periodically sends a request (e.g., a network ping, a TCP connection attempt, or an HTTP request to a specific endpoint) to each server in its pool. If a server fails to respond correctly within a defined timeout or returns an error status, it is marked as unhealthy. The load balancer temporarily removes the unhealthy server from the routing pool, redirecting traffic to the remaining healthy servers. This process is fundamental to achieving automatic failover and high availability.
