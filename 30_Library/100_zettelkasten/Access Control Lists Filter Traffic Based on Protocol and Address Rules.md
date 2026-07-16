---
aliases: [ACLs]
created: 2025-10-31T10:16:00+00:00
modified: 2026-07-13T08:52:23+00:00
permalink: llmeon/30-library/100-zettelkasten/access-control-lists-filter-traffic-based-on-protocol-and-address-rules
tags: [filtering, SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: Access Control Lists Filter Traffic Based on Protocol and Address Rules
type: claim
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Access Control Lists Filter Traffic Based on Protocol and Address Rules

Summary: Access Control Lists (ACLs) are sequential rule sets that permit or deny network traffic based on protocol, source/destination IP addresses, and other packet attributes.

Rule structure:

- Each rule contains:
  - Action (permit/deny)
  - Protocol (TCP, UDP, etc.)
  - Source address/mask
  - Destination address/mask

Processing logic:

1. Only protocol is mandatory - other fields are "don't care" if unspecified
2. Evaluates packets against rules using longest prefix match
3. First matching rule determines action (permit/deny)

Example (pseudo-Cisco format):

```sh
block_traffic
  deny tcp 192.168.1.0 255.255.255.0
  permit udp 10.10.10.0 255.255.255.0
```
