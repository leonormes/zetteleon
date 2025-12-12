---
aliases: ["Reverse DNS"]
confidence: 0.9
created: 2025-10-31T10:50:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:50:00Z
purpose: "Explain reverse DNS lookup mechanism."
review_interval: 90
see_also: ["DNS is a distributed database.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: in-addr.arpa Domains Enable IP-to-Name Reverse DNS Lookups
type: concept
uid: 
updated: 
---

## in-addr.arpa Domains Enable IP-to-Name Reverse DNS Lookups

**Summary:** The in-addr.arpa domain provides a hierarchical namespace for mapping IP addresses back to hostnames using PTR records.

**Format:**
- IPv4: Reverse octets + .in-addr.arpa (e.g., 1.253.253.192.in-addr.arpa for 192.253.253.1)
- Queries return PTR records with canonical names

**Uses:**
- Authentication (e.g., mail servers)
- Logging
- Troubleshooting

**Delegation:**
Like forward zones, in-addr.arpa subdomains must be properly delegated to network administrators.
