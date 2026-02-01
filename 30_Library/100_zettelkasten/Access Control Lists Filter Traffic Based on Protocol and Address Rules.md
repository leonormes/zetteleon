---
aliases: ["ACLs"]
created: 2025-10-31T10:16:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:37+00:00
status: "seedling"
tags: ["filtering", "SoftwareEngineering/Networking", "SoftwareEngineering/Security"]
title: Access Control Lists Filter Traffic Based on Protocol and Address Rules
type: "concept"
updated: 
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
