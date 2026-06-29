---
aliases:
- TGW
- Virtual WAN
created: 2025-12-24 12:00:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:24+00:00
status: seedling
tags:
- aws
- azure
- SoftwareEngineering/Networking
title: Transit Gateway
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/transit-gateway
---

## Transit Gateway

Summary: A Transit Gateway (or Azure Virtual WAN) acts as a network transit hub that connects VPCs/VNets, on-premises networks, and other hubs, simplifying architecture by eliminating complex peering relationships.

Core Logic:

- Hub-and-Spoke: Networks attach to the central hub.
- Transitive Routing: Allows VPC A to talk to VPC B via the Gateway without a direct peer.
- Segmentation: Multiple route tables within the gateway can isolate traffic (e.g., preventing Dev from reaching Prod).

Comparison:

- AWS: Transit Gateway.
- Azure: Virtual WAN / Route Server.