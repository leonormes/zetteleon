---
aliases: []
confidence: "0.9"
created: 2025-10-31T10:34:00Z
epistemic: "fact"
last_reviewed: "null"
modified: 2026-01-23T18:09:30+00:00
purpose: "Explain NAT gateway functionality."
review_interval: "90"
see_also: ["Data-Centric Networking Focuses on Packet Journey Through Devices.md"]
source_of_truth: []
status: "seedling"
tags: ["cloud", "SoftwareEngineering/Networking", "SoftwareEngineering/Security"]
title: NAT Gateways Enable Private Resources to Access Internet
type: "concept"
uid: 
updated: 
---

## NAT Gateways Enable Private Resources to Access Internet

**Summary:** NAT gateways allow private cloud resources to initiate outbound internet connections while blocking unsolicited inbound traffic.

**Key functions:**

- Source NAT (SNAT) - replaces private IP with public IP
- Maintains translation table
- Enables outbound-only internet access

**Example packet flow:**

1. Private IP 10.0.2.50 → vendor API 198.51.100.10
2. NAT replaces source with 203.0.113.1
3. Tracks connection in translation table
4. Routes response back to 10.0.2.50

**Kubernetes Context:**
In EKS clusters, NAT gateways handle:

1. Secondary translation after kube-proxy SNAT
2. Private subnet worker node egress
3. Return traffic routing to correct node

**Limitations:**

- No inbound access to private resources
- No VPN functionality
- Basic security through obscurity
