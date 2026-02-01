---
aliases: []
created: 2025-10-31T09:25:27Z
last_reviewed: ""
modified: 2026-02-01T15:08:31+00:00
status: "seedling"
tags: ["load-balancing", "reliability", "SoftwareEngineering/Networking"]
title: Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers
type: "concept"
updated: 
---

## Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers

Summary: Health checks are automated tests that a load balancer performs to determine if a backend server is available and operating correctly before sending traffic to it.

Details: The load balancer periodically sends a request (e.g., a network ping, a TCP connection attempt, or an HTTP request to a specific endpoint) to each server in its pool. If a server fails to respond correctly within a defined timeout or returns an error status, it is marked as unhealthy. The load balancer temporarily removes the unhealthy server from the routing pool, redirecting traffic to the remaining healthy servers. This process is fundamental to achieving automatic failover and high availability.
