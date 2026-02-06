---
alias: ["AKS CIDR Planning", "Subnet Sizing Standard"]
created: 2026-02-05T00:00:00+00:00
modified: 2026-02-05T19:59:31+00:00
status: stable
tags: ["aks", "azure", "calico", "networking", "sot"]
title: SoT - AKS IP Allocation & Subnet Sizing
trust-level: stable
type: SoT
---

## Minimum Viable Understanding (MVU)

For private FITFILE AKS deployments using Calico Overlay, the standard minimum subnet allocation is a $/27$ (32 IP addresses). While Calico reduces IP pressure by using an overlay for pods, a $/28$ (16 IPs) is mathematically insufficient for stable operations and cluster upgrades.

---

## 1. Technical Justification: The /28 Trap

A standard 3-node private cluster consumes IPs at the VNet level for Nodes and Infrastructure only. However, the overhead is significant:

| Component | IP Consumption | Reason |
|:--- |:--- |:--- |
| Azure Infrastructure | 5 IPs | Reserved by Azure for default gateway, DNS, etc. |
| Private Endpoint (API) | 1 IP | Required for private cluster control plane access. |
| Cluster Nodes | 3 IPs | One IP per VM in the primary node pool. |
| Internal Load Balancer | 1 IP | Required for ingress traffic entry point. |
| Upgrade Surge Buffer | 1+ IPs | Required during node patching/upgrades (Surge nodes). |
| TOTAL MINIMUM | 11 IPs | Baseline for a healthy 3-node cluster. |

### The Risk of /28 (16 IPs)

A $/28$ subnet provides only 11 usable IPs (16 total - 5 Azure reserved). This leaves zero headroom for:

- Scaling the node pool.
- High Availability (adding a 4th node).
- Failure to release IPs immediately during rolling updates.

---

## 2. Standard Recommendation: /27 (32 IPs)

A $/27$ provides 27 usable IPs, which is the FITFILE deployment standard.

### Benefits

1. Operational Safety: Sufficient buffer for upgrade surge and temporary node failures.
2. Future Proofing: Allows scaling up to ~20 nodes without a destructive network rebuild.
3. Internal Services: Capacity to deploy additional Internal Load Balancers for specialized services (e.g., private APIs).

---

## 3. Interaction with CNI

This sizing assumes the use of Calico Overlay (BYO CNI).

- Pod IPs: Carved from a non-routable CIDR (e.g., `192.168.0.0/16`) _inside_ the cluster fabric.
- Node IPs: Carved from the Azure VNet subnet defined above.

_Related Reference:_ [[CNI Explained]]
