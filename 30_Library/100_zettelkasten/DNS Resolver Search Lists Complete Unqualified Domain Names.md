---
aliases: []
confidence: 0.9
created: 2025-10-31T10:46:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:46:00Z
purpose: "Explain DNS search list functionality."
review_interval: 90
see_also: ["DNS Resolvers Translate Domain Requests to IP Queries.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: DNS Resolver Search Lists Complete Unqualified Domain Names
type: concept
uid: 
updated: 
---

## DNS Resolver Search Lists Complete Unqualified Domain Names

**Summary:** DNS resolvers use a search list to automatically append domains to unqualified names (without dots), attempting resolution through multiple possible FQDNs.

**Operation:**
1. User enters name without dots (e.g., "telnet carrie")
2. Resolver tries:
   - carrie.domain1
   - carrie.domain2
   - etc.

**Configuration:**
- Set via `search` or `domain` in `/etc/resolv.conf`
- Bypassed with trailing dot (e.g., "carrie.movie.edu.")
