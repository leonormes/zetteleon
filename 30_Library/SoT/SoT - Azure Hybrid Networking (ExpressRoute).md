---
alias:
- Azure ExpressRoute Architecture
- Azure Secure Egress
- ExpressRoute Isolation
- Hybrid Cloud Security
aliases: []
created: 2025-12-30 11:41:24+00:00
last_reviewed: '2025-12-30'
modified: 2026-02-01 15:08:01+00:00
status: stable
tags:
- azure
- hybrid_cloud
- SoftwareEngineering/Architecture
- SoftwareEngineering/Networking
- SoftwareEngineering/Security
title: SoT - Azure Hybrid Networking (ExpressRoute)
type: SoT
updated: null
permalink: llmeon/30-library/so-t/so-t-azure-hybrid-networking-express-route
---

## 1. Core Architecture

> [!definition] Azure ExpressRoute
> A private, dedicated connection between on-premises infrastructure and Microsoft Azure. It bypasses the public internet, offering deterministic latency and enhanced security.
> - Topology: It is NOT a single unified network. It is two distinct administrative domains (On-Prem vs. Azure) interconnected via BGP.
> - Key Constraint: Address spaces must be non-overlapping.

---

## 2. Connectivity Models

| Model | Description | Use Case |
|:--- |:--- |:--- |
| Cloud Exchange | L2/L3 via Colocation Provider (Equinix). | Most common enterprise connection. |
| Point-to-Point | L2 Ethernet direct to Microsoft. | High security/dedicated throughput. |
| IPVPN (Any-to-Any) | Azure acts as another node on existing MPLS. | Seamless WAN integration. |
| ExpressRoute Direct | 10G/100G direct physical port. | Massive data ingestion / Regulatory isolation. |

---

## 3. Peering Types (The Logical Layer)

A single physical circuit supports two distinct logical peerings.

### 3.1 Private Peering (The Extension)

- Scope: Connects On-Prem $\leftrightarrow$ Azure VNets (IaaS/Internal PaaS).
- Addressing: Private IPs (RFC1918).
- Routing: On-prem advertises internal routes; Azure advertises VNet routes.
- Use Case: Extending the datacenter to the cloud (VMs, AKS).

### 3.2 Microsoft Peering (The Public Path)

- Scope: Connects On-Prem $\leftrightarrow$ Microsoft Public Services (Storage, SQL, M365).
- Addressing: Public IPs (owned by customer).
- Routing: On-prem advertises Public NAT IPs; Microsoft advertises Service IPs.
- Critical Note: Does NOT provide internet access for Azure VMs. It is strictly for reaching MS services privately.

---

## 4. Security Patterns: Isolation & Egress

The "Hybrid" nature introduces a massive attack vector: The Cloud pivoting to On-Prem.

### 4.1 Isolating On-Premises (Defense in Depth)

We must treat the Azure environment as "Less Trusted" than the On-Prem Core.

1. Network Security Groups (NSGs): Block outbound traffic from App Subnets to the ExpressRoute Gateway.
2. Route Injection: Do not propagate BGP routes to sensitive subnets.
3. The Inspection Choke Point: Use User Defined Routes (UDRs) to force all On-Prem bound traffic through an Azure Firewall/NVA.
    - `0.0.0.0/0` $\to$ `Firewall` (Internet Egress)
    - `10.0.0.0/8` (On-Prem) $\to$ `Firewall` (Internal Inspection)

### 4.2 Secure Internet Egress Models

| Model | Mechanism | Pros | Cons |
|:--- |:--- |:--- |:--- |
| Centralized (Hub & Spoke) | All Spoke traffic routes to Hub Firewall via UDR. | Single policy point; consistent inspection. | Hub is a bottleneck; extra hop latency. |
| Distributed (NAT Gateway) | NAT Gateway per Spoke Subnet. | High scale; no bottleneck. | Decentralized policy; difficult to audit. |
| Forced Tunneling | Advertise `0.0.0.0/0` from On-Prem via BGP. | Traffic scrubbed by existing On-Prem appliances. | Latency hairpin; creates On-Prem dependency. |

---

## 5. Minimum Viable Understanding (MVU)

1. ExpressRoute is a Bridge, not a Merger: Treat the networks as distinct domains with explicit boundaries.
2. UDR is King: UDRs override BGP. Use them to enforce traffic flow through security appliances.
3. Private vs. Microsoft Peering: Private is for your VMs. Microsoft is for PaaS/Office 365. They are totally different.
4. Identity is the new Perimeter: Even with ExpressRoute, relying solely on IP ACLs is insufficient. Use Private Link and Identity (Entra ID) validation.