---
aliases: []
confidence: 0.9
created: 2025-10-31T10:45:00Z
epistemic: fact
last_reviewed: 
modified: 2025-11-01T14:53:02Z
purpose: "Explain DNS resolver functionality."
review_interval: 90
see_also: ["DNS is a distributed database.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: DNS Resolvers Translate Domain Requests to IP Queries
type: concept
uid: 
updated: 
---

## DNS Resolvers Translate Domain Requests to IP Queries

**Summary:** A DNS resolver is client-side software that converts domain name requests into DNS queries and interprets the responses to provide IP addresses to applications.

**Key functions:**
- Translates application requests (e.g., <www.google.com>) into DNS queries
- Sends queries to configured nameservers
- Interprets responses and returns IP addresses to applications

**Configuration (Unix):**
- `/etc/resolv.conf` file specifies:
  - `nameserver`: IPs of authoritative nameservers
  - `domain`: Local domain name
  - `search`: List of domains for unqualified names
