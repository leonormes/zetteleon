---
aliases: ["TGW", "Virtual WAN"]
confidence: "0.9"
created: 2025-12-24T12:00:00Z
epistemic: "fact"
last_reviewed: ""
modified: 2025-12-28T09:56:28+00:00
purpose: "Explain central network hub architecture."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["aws", "azure", "topic/technology/networking"]
title: Transit Gateway
type: "concept"
uid: 
updated: 
---

## Transit Gateway

**Summary:** A Transit Gateway (or Azure Virtual WAN) acts as a network transit hub that connects VPCs/VNets, on-premises networks, and other hubs, simplifying architecture by eliminating complex peering relationships.

**Core Logic:**
- **Hub-and-Spoke:** Networks attach to the central hub.
- **Transitive Routing:** Allows VPC A to talk to VPC B via the Gateway without a direct peer.
- **Segmentation:** Multiple route tables within the gateway can isolate traffic (e.g., preventing Dev from reaching Prod).

**Comparison:**
- **AWS:** Transit Gateway.
- **Azure:** Virtual WAN / Route Server.
