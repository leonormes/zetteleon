---
aliases: ["ACLs"]
confidence: 0.9
created: 2025-10-31T10:16:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain how Access Control Lists filter network traffic."
review_interval: 90
see_also: ["Layer 3 Network Security Protects IP Routing and Forwarding.md"]
source_of_truth: []
status: seedling
tags: [filtering, networking, security]
title: Access Control Lists Filter Traffic Based on Protocol and Address Rules
type: concept
uid: 
updated: 
---

## Access Control Lists Filter Traffic Based on Protocol and Address Rules

**Summary:** Access Control Lists (ACLs) are sequential rule sets that permit or deny network traffic based on protocol, source/destination IP addresses, and other packet attributes.

**Rule structure:**
- Each rule contains:
  - Action (permit/deny)
  - Protocol (TCP, UDP, etc.)
  - Source address/mask
  - Destination address/mask

**Processing logic:**
1. Only protocol is mandatory - other fields are "don't care" if unspecified
2. Evaluates packets against rules using longest prefix match
3. First matching rule determines action (permit/deny)

**Example (pseudo-Cisco format):**

```sh
block_traffic
  deny tcp 192.168.1.0 255.255.255.0
  permit udp 10.10.10.0 255.255.255.0
```
