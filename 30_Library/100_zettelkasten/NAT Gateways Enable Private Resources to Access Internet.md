---
aliases: []
created: 2025-10-31T10:34:00+00:00
modified: 2026-07-13T08:52:29+00:00
permalink: llmeon/30-library/100-zettelkasten/nat-gateways-enable-private-resources-to-access-internet
tags: [cloud, SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: NAT Gateways Enable Private Resources to Access Internet
type: claim
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## NAT Gateways Enable Private Resources to Access Internet

Summary: NAT gateways allow private cloud resources to initiate outbound internet connections while blocking unsolicited inbound traffic.

Key functions:

- Source NAT (SNAT) - replaces private IP with public IP
- Maintains translation table
- Enables outbound-only internet access

Example packet flow:

1. Private IP 10.0.2.50 → vendor API 198.51.100.10
2. NAT replaces source with 203.0.113.1
3. Tracks connection in translation table
4. Routes response back to 10.0.2.50

Kubernetes Context:

In EKS clusters, NAT gateways handle:

1. Secondary translation after kube-proxy SNAT
2. Private subnet worker node egress
3. Return traffic routing to correct node

Limitations:

- No inbound access to private resources
- No VPN functionality
- Basic security through obscurity
