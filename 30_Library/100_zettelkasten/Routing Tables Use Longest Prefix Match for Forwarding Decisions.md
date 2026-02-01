---
aliases: []
created: 2025-10-31T10:17:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:27+00:00
status: "seedling"
tags: ["routing", "SoftwareEngineering/Networking"]
title: Routing Tables Use Longest Prefix Match for Forwarding Decisions
type: "concept"
updated: 
---

## Routing Tables Use Longest Prefix Match for Forwarding Decisions

Summary: Network routers forward packets by selecting the most specific (longest prefix) route that matches the destination IP address.

Matching algorithm:

1. Perform bitwise comparison between destination IP and route prefixes
2. Select the route with the longest matching prefix (largest subnet mask)
3. If no match, use default route (0.0.0.0/0)

Benefits:

- Enables hierarchical routing
- Handles overlapping networks unambiguously
- Supports both general and specific routing policies

Example:

For IP 192.168.1.5:

- 192.168.1.0/24 is preferred over
- 192.168.0.0/16
