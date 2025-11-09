---
aliases: ["Network Security Groups", "NSGs"]
confidence: 0.9
created: 2025-10-31T10:31:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain cloud firewall functionality."
review_interval: 90
see_also: ["Data-Centric Networking Focuses on Packet Journey Through Devices.md"]
source_of_truth: []
status: seedling
tags: [cloud, networking, security]
title: Cloud Firewalls Filter Traffic at Network and Transport Layers
type: concept
uid: 
updated: 
---

## Cloud Firewalls Filter Traffic at Network and Transport Layers

**Summary:** Cloud firewalls (Security Groups/NSGs) filter traffic based on IP addresses and ports, operating at OSI Layers 3-4 to protect network segments.

**Key functions:**
- Stateful filtering (track connection state)
- Rule evaluation (allow/deny based on IP/port)
- Instance or subnet-level protection

**Example packet flow:**
1. TCP SYN to 10.0.1.5:443 from 203.0.113.99
2. Matches allow rule for 0.0.0.0/0:443
3. Packet permitted
4. Return SYN-ACK automatically allowed (stateful)

**Limitations:**
- No application-layer inspection
- No DDoS protection
- Basic policy management
