---
aliases: ["Split-Brain DNS", "Split-View DNS"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2026-01-03T10:19:35+00:00
purpose: "To explain the architecture where a single domain name resolves to different IPs based on the client's network location."
review_interval: "1 year"
see_also: ["[[Private DNS Zones Provide Internal Network Name Resolution]]"]
source_of_truth: ["[[SoT - The Data Architecture of DNS]]"]
status: "stable"
tags: ["topic/technology/networking/dns", "hybrid-cloud", "security"]
title: Split-Horizon DNS Decouples Service Names from Network Topology
type: "concept"
uid: 
updated: 
---

## Split-Horizon DNS

**Split-Horizon DNS** is a configuration where a DNS server provides different answers to queries for the same domain name depending on the source IP or network location of the client.

### 🧩 The Use Case

Managing a service (e.g., `app.mycorp.com`) that exists on both public and private networks:

- **External Clients:** Resolve to a **Public IP** (Public Load Balancer).
- **Internal Clients (VPC/VPN):** Resolve to a **Private IP** (Internal Load Balancer).

### 🚀 Cloud-Native Implementations

- **AWS Route 53:** Created using **Public** and **Private Hosted Zones** with identical names. The Route 53 Resolver prioritises the Private Zone for requests originating within associated VPCs.
- **Azure DNS:** Implemented via **Public** and **Private DNS Zones**. Private zones are "linked" to specific VNets.

### 🔐 Strategic Importance

This pattern allows hardcoded logical service names in application code to remain constant across all environments. The infrastructure transparently provides the context-aware network location, eliminating environment-specific configuration logic.
