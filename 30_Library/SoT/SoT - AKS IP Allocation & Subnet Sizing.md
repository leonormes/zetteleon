---
alias: ["AKS CIDR Planning", "Subnet Sizing Standard"]
created: 2026-02-05T00:00:00+00:00
modified: 2026-02-16T09:40:34+00:00
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
| Upgrade Surge Buffer | 1 IP | Required during node patching/upgrades (Surge nodes). |
| TOTAL MINIMUM | 11 IPs | Baseline for a healthy 3-node cluster. |

### The Risk of /28 (16 IPs)

A $/28$ subnet provides only 11 usable IPs (16 total - 5 Azure reserved). This leaves zero headroom for:

- Scaling: Adding just one High Availability node or a dedicated runner node.
- Failover: If a single node fails to release its IP immediately during an upgrade, the entire cluster will fail to provision the replacement node.

---

## 2. Standard Recommendation: /27 (32 IPs)

A $/27$ provides 27 usable IPs, which is the FITFILE deployment standard.

### Benefits

1. Operational Safety: Sufficient buffer for upgrade surge and temporary node failures.
2. Future Proofing: Allows scaling the cluster up to ~20 nodes if performance requirements change, without needing to rebuild the networking stack.
3. Internal Services: Capacity to deploy additional internal services or Load Balancers without exhausting the subnet.

---

## 3. Interaction with CNI

This sizing assumes the use of Calico Overlay.

- Pod IPs: Carved from a non-routable CIDR (e.g., `10.244.0.0/16`) _inside_ the cluster fabric.
- Node IPs: Carved from the Azure VNet subnet defined above.

---

## Related Knowledge

- [[2026-02-05 - Azure AKS Inbound DNAT and IP Sizing]] - Initial investigation log for CIDR sizing.
- [[SoT - FitFile Deployment - Networking and Security]] - Overall network architecture.
- [[CNI Explained]] - Theory behind Calico Overlay vs. standard CNI.
- [[HEAD What is the Riemann Hypothesis]] — **error term analogy**: the /27 buffer (27 usable IPs) manages variance in IP consumption the way Riemann's error term manages variance in prime density. Both are safety margins for sparse allocation systems.
