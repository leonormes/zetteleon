---
aliases: []
confidence: 0.9
created: 2025-10-31T10:49:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain DNS glue records."
review_interval: 90
see_also: ["DNS Delegation Handles Subdomain Authority Transfers.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: Glue Records Solve DNS Chicken-and-Egg Problems
type: concept
uid: 
updated: 
---

## Glue Records Solve DNS Chicken-and-Egg Problems

**Summary:** Glue records are special A records in parent zones that provide the IP addresses of delegated subdomain nameservers, enabling their discovery.

**Problem solved:**
When subdomain nameservers reside within their own subdomain (e.g., ns1.fx.movie.edu serving fx.movie.edu), resolvers cannot find their IPs without these records.

**Implementation:**
- Parent zone includes A records for child nameservers
- Provided during referral responses
- Not part of parent's official zone data

**Example:**
movie.edu zone contains:

```sh
fx.movie.edu. NS ns1.fx.movie.edu.
ns1.fx.movie.edu. A 192.253.253.1
```
