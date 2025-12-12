---
aliases: ["RRs"]
confidence: 0.9
created: 2025-10-31T11:05:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain DNS resource record structure."
review_interval: 90
see_also: ["DNS is a distributed database.md"]
source_of_truth: []
status: seedling
tags: [data-structures, dns, networking]
title: DNS Resource Records Are Structured Key-Value Pairs
type: concept
uid: 
updated: 
---

## DNS Resource Records Are Structured Key-Value Pairs

**Summary:** DNS resource records (RRs) associate domain names (keys) with structured data (values) in a standardized format.

**Common RR Types:**
- **A/AAAA:** IP addresses
- **CNAME:** Domain aliases
- **MX:** Mail servers with priorities
- **NS:** Delegated nameservers
- **TXT:** Verification strings
- **SOA:** Zone metadata

**Structure:**

```sh
<Name> <TTL> <Class> <Type> <RDATA>
```

- **Name:** Domain key (e.g., example.com)
- **TTL:** Cache duration (seconds)
- **Class:** Typically IN (Internet)
- **Type:** Record type
- **RDATA:** Type-specific payload
