---
aliases: []
confidence: 0.9
created: 2025-10-31T10:17:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:17:00Z
purpose: "Explain longest prefix match routing principle."
review_interval: 90
see_also: ["Layer 3 Network Security Protects IP Routing and Forwarding.md"]
source_of_truth: []
status: seedling
tags: [networking, routing]
title: Routing Tables Use Longest Prefix Match for Forwarding Decisions
type: concept
uid: 
updated: 
---

## Routing Tables Use Longest Prefix Match for Forwarding Decisions

**Summary:** Network routers forward packets by selecting the most specific (longest prefix) route that matches the destination IP address.

**Matching algorithm:**
1. Perform bitwise comparison between destination IP and route prefixes
2. Select the route with the longest matching prefix (largest subnet mask)
3. If no match, use default route (0.0.0.0/0)

**Benefits:**
- Enables hierarchical routing
- Handles overlapping networks unambiguously
- Supports both general and specific routing policies

**Example:**
For IP 192.168.1.5:
- 192.168.1.0/24 is preferred over
- 192.168.0.0/16
