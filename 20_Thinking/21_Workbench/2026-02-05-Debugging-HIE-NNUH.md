---
created: 2026-02-05T10:40:21+00:00
modified: 2026-02-06T12:41:07+00:00
tags:
  - domain/networking
  - status/active
  - task/FTFL-88
  - customer/nnuh
title: 2026-02-05-Debugging-HIE-NNUH
---

## Debugging HIE -> NNUH Networking

### Context

- Workstream: Node Installation NNUH ().
- Specific Task: Configure Inbound Routes ().
- Current Blocker: Static Ingress IP from NNUH Network Team (Target: Ben Goss).
- Architecture: [[SoT - NNUH Network Architecture]]

### Data Collected (2026-02-06)

#### NNUH Network Topology

- Private Firewall IP: `192.168.208.4` (NNUH-HUB)
- Jumpbox IP: `192.168.200.132`
- Public Bastion IP: `20.162.252.26`
- Subnets: System (`.32/27`), Workflows (`.64/27`), Jumpbox (`.128/29`).

#### Connectivity Requirements

1. HIE Egress: Must verify source cluster `hie-prod-34`. Check if it is using the fixed egress NAT configuration ().
2. NNUH Ingress: Cyber preference is for traffic to traverse on-prem firewalls.
3. FTP Connection: Stalled awaiting static IP allocation for end-to-end flow.

### Investigation Plan (The "Next Test")

#### 1. Verification of HIE Egress

- Action: Exec into `hie-prod-34` netshoot pod and test curl to a public reflector (e.g., `ifconfig.me`) to confirm fixed egress IP.
- Reference: [[Protocol - Kubernetes Network Debugging#1. Source Side: Verify Egress (From Netshoot)]]

#### 2. Verify NNUH Routing Path

- Action: Once Static IP is provided, check Route Table at NNUH for "Next Hop" traversal to `192.168.208.4`.
- Reference: [[SoT - Network Debugging Tools & Patterns#2. Layer 3: Reachability & Routing (The Roads)]]

### Related Resources

- [[SoT - NNUH Network Architecture]]
- [[SoT - Network Debugging - Cross-Cloud & Hybrid]]
- [[30_Library/200_projects/20_Development/Debug Wiki/troubleshooting_guide.md|Troubleshooting Guide: Cross-Cloud Connectivity]]
