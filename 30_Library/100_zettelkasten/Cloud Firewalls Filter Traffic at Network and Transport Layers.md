---
aliases: [Network Security Groups, NSGs]
created: 2025-10-31T10:31:00+00:00
last_reviewed: ''
modified: 2026-07-04T10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/cloud-firewalls-filter-traffic-at-network-and-transport-layers
status: seedling
tags: [cloud, SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: Cloud Firewalls Filter Traffic at Network and Transport Layers
type: concept
updated: null
---

## Cloud Firewalls Filter Traffic at Network and Transport Layers

Summary: Cloud firewalls range from basic Security Groups (NSGs) operating at OSI Layers 3-4 to sophisticated Cloud-Native Firewalls and Firewall-as-a-Service (FWaaS) that provide elastic, managed security across distributed environments.

Deployment Models:

- Security Groups / NSGs: Basic, stateful L3-L4 filtering at the instance or subnet level.
- Cloud-Native Firewalls: Services built specifically for the cloud (e.g., AWS Network Firewall, Azure Firewall) providing deeper inspection and centralized management.
- Firewall-as-a-Service (FWaaS): A managed subscription model where third-party vendors handle the infrastructure, often used in [[SASE]] architectures to secure remote users and branches.

Key functions:

- Elastic Scalability: Automatically adapts to traffic demands without manual infrastructure management.
- Stateful filtering: Tracks connection states to allow return traffic automatically.
- Rule evaluation: Evaluates traffic against static and dynamic policies.
- Global Presence: PoPs (Points of Presence) reduce latency for distributed users.

Limitations:

- Basic SG/NSGs: Lack application-layer (L7) visibility or advanced threat protection.
- FWaaS Latency: Potential latency if traffic must be routed through specific provider PoPs.
- Vendor Lock-in: Integration varies significantly between cloud providers.

Example packet flow:

1. TCP SYN to 10.0.1.5:443 from 203.0.113.99
2. Matches allow rule for 0.0.0.0/0:443
3. Packet permitted
4. Return SYN-ACK automatically allowed (stateful)
