---
created: 2026-02-06T00:00:00+00:00
modified: 2026-02-06T19:31:09+00:00
source_of_truth: true
status: growing
tags: [customer/nnuh, domain/infrastructure, domain/networking, provider/azure, status/active, task/FTFL-88, type/SoT]
title: 2026-02-05-Debugging-HIE-NNUH
trust-level: stable
---

## Debugging HIE -> NNUH Networking

[[Protocol - AWS HIE Jumpbox Access]]
### Data Collected (2026-02-06)

#### NNUH Network Topology

- Private Firewall IP: `192.168.208.4` (NNUH-HUB)
- Jumpbox IP: `192.168.200.132`
- Public Bastion IP: `20.162.252.26`
- Subnets: System (`.32/27`), Workflows (`.64/27`), Jumpbox (`.128/29`).
- Public ingress IP: `195.171.151.154`
- dns record: nnuh-prod-1.fitfile.net

#### Connectivity Requirements

1. HIE Egress: Must verify source cluster `hie-prod-34`. Check if it is using the fixed egress NAT configuration ().
2. NNUH Ingress: Cyber preference is for traffic to traverse on-prem firewalls.
3. FTP Connection: Stalled awaiting static IP allocation for end-to-end flow.

### Investigation Plan (The "Next Test")

#### 1. Verification of HIE Egress

- Action: Exec into `hie-prod-34` netshoot pod and test curl to a public reflector (e.g., `ifconfig.me`) to confirm fixed egress IP.
- Reference: [[Protocol - HIE--NNUH Network Debugging#1. Source Side: Verify Egress (From Netshoot)]]

#### 2. Verify NNUH Routing Path

- Action: Once Static IP is provided, check Route Table at NNUH for "Next Hop" traversal to `192.168.208.4`.
- [[2026-02-05-Debugging-HIE-NNUH]]g Tools & Patterns#2. Layer 3: Reachability & Routing (The Roads)]]

### Related Resources

- [[SoT - Network Debugging - Cross-Cloud & Hybrid]]
- [[30_Library/200_projects/20_Development/Debug Wiki/troubleshooting_guide.md|Troubleshooting Guide: Cross-Cloud Connectivity]]

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
- HIE Egress: Verify if `hie-prod-34` is using the fixed egress IP from

## Related Knowledge

- [[SoT - Network Debugging - Cross-Cloud & Hybrid]]
- [[Protocol - HIE--NNUH Network Debugging]]
