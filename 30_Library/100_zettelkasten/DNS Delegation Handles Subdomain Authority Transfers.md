---
aliases: []
confidence: 0.9
created: 2025-10-31T10:48:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:48:00Z
purpose: "Explain DNS delegation mechanism."
review_interval: 90
see_also: ["DNS is a distributed database.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: DNS Delegation Handles Subdomain Authority Transfers
type: concept
uid: 
updated: 
---

## DNS Delegation Handles Subdomain Authority Transfers

**Summary:** DNS delegation allows parent domains to transfer authority for subdomains to different nameservers, enabling hierarchical management.

**Mechanism:**
1. Parent zone (e.g., movie.edu) contains NS records pointing to subdomain nameservers (e.g., fx.movie.edu)
2. Queries for the subdomain are referred to these nameservers
3. Creates separate zone of authority

**Benefits:**
- Enables distributed administration
- Supports organizational boundaries
- Maintains hierarchical structure
