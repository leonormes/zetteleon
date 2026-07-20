---
aliases: []
conformant: false
created: 2025-10-31T10:15:00+00:00
modified: 2026-07-20T16:34:28+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/layer-3-network-security-protects-ip-routing-and-forwarding
tags: [layer3, SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: Layer 3 Network Security Protects IP Routing and Forwarding
type: claim
---

## Layer 3 Network Security Protects IP Routing and Forwarding

Summary: Layer 3 (Network Layer) security focuses on protecting IP packet routing, filtering, and forwarding operations. It is primarily implemented via Access Control Lists (ACLs) and Network Address Translation (NAT) on routers and firewalls.

Core Mechanisms:

- Access Control Lists (ACLs): Static sets of rules that permit or deny packets based on Source/Destination IP, Port numbers, and Protocols (TCP, UDP, ICMP).
- Network Address Translation (NAT): Obscures internal topology while conserving public IPv4 addresses.
	- Static NAT: One-to-one mapping between private and public IPs (used for internal servers).
	- Dynamic NAT: Temporary mapping from a pool of public IPs.
	- Port Address Translation (PAT / Overload): Maps multiple private IPs to a single public IP using unique source ports.

Key Protection Areas:

- IP Spoofing: Blocking packets with invalid or forged source addresses.
- Boundary Defense: Establishing the "Trusted" vs. "Untrusted" perimeter (though modern systems are shifting toward [[SoT - Zero Trust Architecture|Zero Trust]]).
- DoS Mitigation: Filtering volumetric traffic at the ingress point.

Comparison to Layer 2 security:

While Layer 2 protects data frames (MAC addresses), Layer 3 secures logical addressing (IP) and routing between networks.
