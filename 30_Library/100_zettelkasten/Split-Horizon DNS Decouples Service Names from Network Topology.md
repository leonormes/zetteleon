---
aliases:
- Split-Brain DNS
- Split-View DNS
created: 2025-12-24 12:00:00+00:00
last_reviewed: 2025-12-24
modified: 2026-02-01 15:08:27+00:00
status: stable
tags:
- hybrid-cloud
- SoftwareEngineering/networking/dns
- SoftwareEngineering/Security
title: Split-Horizon DNS Decouples Service Names from Network Topology
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/split-horizon-dns-decouples-service-names-from-network-topology
---

## Split-Horizon DNS

Split-Horizon DNS is a configuration where a DNS server provides different answers to queries for the same domain name depending on the source IP or network location of the client.

### 🧩 The Use Case

Managing a service (e.g., `app.mycorp.com`) that exists on both public and private networks:

- External Clients: Resolve to a Public IP (Public Load Balancer).
- Internal Clients (VPC/VPN): Resolve to a Private IP (Internal Load Balancer).

### 🚀 Cloud-Native Implementations

- AWS Route 53: Created using Public and Private Hosted Zones with identical names. The Route 53 Resolver prioritises the Private Zone for requests originating within associated VPCs.
- Azure DNS: Implemented via Public and Private DNS Zones. Private zones are "linked" to specific VNets.

### 🔐 Strategic Importance

This pattern allows hardcoded logical service names in application code to remain constant across all environments. The infrastructure transparently provides the context-aware network location, eliminating environment-specific configuration logic.