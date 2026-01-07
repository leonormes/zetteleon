---
aliases: []
confidence: "0.9"
created: 2025-10-31T10:15:00Z
epistemic: "fact"
last_reviewed: ""
modified: 2026-01-03T10:19:39+00:00
purpose: "Define Layer 3 network security in the OSI model."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["layer3", "SoftwareEngineering/Security", "SoftwareEngineering/Networking"]
title: Layer 3 Network Security Protects IP Routing and Forwarding
type: "concept"
uid: 
updated: 
---

## Layer 3 Network Security Protects IP Routing and Forwarding

**Summary:** Layer 3 (Network Layer) security focuses on protecting IP packet routing, filtering, and forwarding operations. It is primarily implemented via **Access Control Lists (ACLs)** and **Network Address Translation (NAT)** on routers and firewalls.

**Core Mechanisms:**
- **Access Control Lists (ACLs):** Static sets of rules that permit or deny packets based on Source/Destination IP, Port numbers, and Protocols (TCP, UDP, ICMP).
- **Network Address Translation (NAT):** Obscures internal topology while conserving public IPv4 addresses.
	- **Static NAT:** One-to-one mapping between private and public IPs (used for internal servers).
	- **Dynamic NAT:** Temporary mapping from a pool of public IPs.
	- **Port Address Translation (PAT / Overload):** Maps multiple private IPs to a single public IP using unique source ports.

**Key Protection Areas:**
- **IP Spoofing:** Blocking packets with invalid or forged source addresses.
- **Boundary Defense:** Establishing the "Trusted" vs. "Untrusted" perimeter (though modern systems are shifting toward [[Zero Trust]]).
- **DoS Mitigation:** Filtering volumetric traffic at the ingress point.

**Comparison to Layer 2 security:**
While Layer 2 protects data frames (MAC addresses), Layer 3 secures logical addressing (IP) and routing between networks.
