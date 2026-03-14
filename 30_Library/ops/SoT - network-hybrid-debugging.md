---
aliases: ["Cross-Cloud Troubleshooting", "DirectConnect Debugging", "ExpressRoute Debugging", "Hybrid Networking Debugging"]
created: 2026-02-04T00:00:00+00:00
modified: 2026-03-14T11:10:11+00:00
tags: ["aws", "azure", "hybrid-cloud", "networking", "sot", "troubleshooting"]
title: SoT - network-hybrid-debugging
type: sot
---

## 1. The Hybrid Connectivity Stack

When debugging EKS (AWS) $\leftrightarrow$ AKS (Azure), the failure usually exists in the Interconnect or the Route Propagation.

| Layer       | Component                    | Diagnostic Command                                                            |
|:---------- |:--------------------------- |:---------------------------------------------------------------------------- |
| Physical/VC | ExpressRoute / DirectConnect | `az network express-route show` / `aws directconnect describe-connections`    |
| Routing     | BGP / UDR / TGW              | `az network nic show-effective-route-table` / `aws ec2 describe-route-tables` |
| Policy      | NSG / Security Groups        | `az network nsg rule list` / `aws ec2 describe-security-groups`               |
| DNS         | Private DNS Resolver         | `dig +trace <internal-fqdn>`                                                  |

---

## 2. Common Failure Modes

### 2.1 "VNET Peering Connected but No Traffic"

- Symptom: Peering status is `Connected`, but traffic times out.
- Cause: Route tables take 5-10 minutes to propagate, or Overlapping CIDRs prevent the route from being installed.
- Check: `ip route get <remote-ip>` from a node. If it goes out the default gateway instead of the peering/VPN, the route is missing.

### 2.2 Split-Horizon DNS Failures (NXDOMAIN)

- Symptom: Pods can ping IPs but cannot resolve names across clouds.
- Cause: The Private DNS Zone is linked to the destination VNET but not the source VNET (or vice-versa).
- Fix: Ensure "Virtual Network Links" exist for _all_ involved VNets in Azure, and "Route53 Resolver Endpoints" are configured in AWS.

### 2.3 Asymmetric Routing

- Symptom: `tcpdump` shows SYN entering the network, but no response leaves.
- Cause: The return path for the traffic is different from the entry path (e.g., enters via VPN, tries to exit via Internet Gateway).
- Check: Verify that the destination has a route _back_ to the source Pod CIDR (not just the Node CIDR).

---

## 3. Tooling for Hybrid Debugging

- Network Watcher (Azure): Use "Next Hop" and "IP Flow Verify" to prove where an NSG or Route is dropping traffic.
- Reachability Analyzer (AWS): Proves if a path exists between two ENIs across VPCs/Peering.
- MTR: Vital for seeing where a packet "goes dark" in the carrier network (if not using private links).
