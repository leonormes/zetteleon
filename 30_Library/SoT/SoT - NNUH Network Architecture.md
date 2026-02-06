---
created: 2026-02-06T00:00:00+00:00
modified: 2026-02-06T12:31:44+00:00
source_of_truth: true
status: growing
tags: [customer/nnuh, domain/infrastructure, provider/azure, type/SoT]
title: SoT - NNUH Network Architecture
trust-level: stable
---

## Minimum Viable Understanding (MVU)

The NNUH Node networking is a hub-and-spoke Azure architecture. All outbound traffic is gated via a NAT Gateway (`NNUHFT-SDE-nat`), while inbound traffic from the Central HIE is preferred to route through NNUH on-premise firewalls via a static public IP (currently the project blocker).

## Working Knowledge

### 1. VNet & Subnet Segmentation

- VNet Address Space: `192.168.200.0/24`
- System Subnet: `192.168.200.32/27` (AKS Nodes)
- Workflows Subnet: `192.168.200.64/27` (Argo Workflows)
- Jumpbox Subnet: `192.168.200.128/29`
- Bastion Subnet: `192.168.200.192/26` (AzureBastionSubnet)

### 2. Known IP Addresses

| Resource | IP Address | Type |
| --- | --- | --- |
| NNUH-HUB Firewall | `192.168.208.4` | Private |
| NNUH Jumpbox | `192.168.200.132` | Private |
| NNUH Bastion PIP | `20.162.252.26` | Public |
| NNUH NAT Gateway | `NNUHFT-SDE-nat-ip` | Public (Pending Allocation) |

### 3. Routing Logic

- Outbound: Routed via NAT Gateway attached to the Azure VNet for a single whitelisable egress point.
- Inbound (HIE -> NNUH): Must pass through NNUH on-prem firewalls. Requires a static public IP to be provisioned by NNUH Network Team.
- Next Hop: Ben Goss (NNUH) to provide the "next hop" IP for the network route table once provisioned.

## Tensions & Gaps

- Critical Blocker: Static Public IP for FTP/Inbound connection has been with the NNUH network team since Jan 2026.
- HIE Egress: Verify if `hie-prod-34` is using the fixed egress IP from [[FFAPP-4008]].

## Related Knowledge

- [[SoT - Network Debugging - Cross-Cloud & Hybrid]]
- [[Protocol - Kubernetes Network Debugging]]
- [[2026-02-05-Debugging-HIE-NNUH]]
