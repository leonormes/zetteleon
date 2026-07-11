---
aliases: []
created: 2025-10-31 09:25:27+00:00
modified: 2026-07-04 10:51:49+00:00
permalink: llmeon/30-library/100-zettelkasten/load-balancer-health-checks-ensure-traffic-is-routed-only-to-healthy-servers
tags:
- load-balancing
- reliability
- SoftwareEngineering/Networking
title: Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers
prodos:
  kind: atomic
  atomic:
    form: concept
  lifecycle: seedling
  review:
    last_reviewed: ''
---


## Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers

Summary: Health checks are automated tests that a load balancer performs to determine if a backend server is available and operating correctly before sending traffic to it.

Details: The load balancer periodically sends a request (e.g., a network ping, a TCP connection attempt, or an HTTP request to a specific endpoint) to each server in its pool. If a server fails to respond correctly within a defined timeout or returns an error status, it is marked as unhealthy. The load balancer temporarily removes the unhealthy server from the routing pool, redirecting traffic to the remaining healthy servers. This process is fundamental to achieving automatic failover and high availability.
