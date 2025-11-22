---
aliases: []
confidence:
created: 2025-11-21T12:34:26Z
epistemic:
last_reviewed:
modified: 2025-11-21T12:34:39Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags:
  - nnuh
title: Terraform Plan vs EoE HIE & NNUH Network Diagram
type:
uid:
updated:
---

## Comprehensive Report: Terraform Plan Vs EoE HIE & NNUH Network Diagram

This report reviews your latest Terraform plan output alongside the PDF network diagram, summarises what will be created, cross-references against the diagram elements, notes discrepancies, and provides a mapping table.

---

### 1) Summary of What Is Being Created (from the Terraform plan)

#### Main deliverables/components

- Azure networking within existing NNUH VNet
    - Three subnets for the FITFILE Node:
        - System subnet: 192.168.200.32/27
        - Workflows subnet: 192.168.200.64/27
        - Jumpbox subnet: 192.168.200.128/29
    - AzureBastionSubnet: 192.168.200.192/26
    - NAT Gateway associations:
        - NAT Gateway: NNUHFT-SDE-nat (existing) associated to System, Workflows, Jumpbox subnets
    - Route table resource (structure present earlier; not in this latest excerpt) is expected to be used to route on-prem/inbound via firewall
- Secure access
    - Azure Bastion Host (Standard) with public IP (in rg-ff-uks-gp-net)
    - Jumpbox Linux VM (vm-ff-uks-gp-jumpbox) without public IP
    - Jumpbox NSG allowing SSH from Azure Bastion only
- AKS private cluster
    - azurerm_kubernetes_cluster:
        - Private cluster enabled
        - Azure CNI overlay, Calico network policy
        - outbound_type = userDefinedRouting (correct for NAT-GW egress on subnets)
        - Default node pool “system” (VM size Standard_E4s_v5, autoscaling 2–3 nodes)
    - Additional node pool “workflows”:
        - Spot, taints/labels configured, autoscaling 1–3 nodes, VM size Standard_E4s_v5
    - Managed identity, Network Contributor assignment
- Security groups
    - NSGs for jumpbox, system, workflows subnets
    - Bootstrap posture: allow VNet inbound, allow Azure LB inbound (for probes), allow all outbound (to be hardened later)

#### Key features/functionality

- Split routing model:
    - Outbound Internet egress for AKS and Jumpbox via NAT Gateway (static egress IP 20.162.236.86 at the platform level)
    - Inbound/on‑prem flows intended to traverse the hub firewall via specific routes (route entries will be required in the route table)
- Private cluster posture:
    - No public API endpoint for AKS
    - No public IPs on nodes
- Secure admin access:
    - Azure Bastion → SSH to Jumpbox → access private AKS

#### Objectives/goals Supported

- Deliver a private FITFILE Node in NNUH Azure tenant aligned with SDE requirements
- Ensure controlled outbound identity via NAT GW
- Provide secure access path without public exposure
- Lay groundwork for platform services (ingress, DNS, TLS, relay) to be layered later

---

### 2) Cross-reference With Diagram

#### Diagram Elements (key Items extracted)

- VNET with:
    - System subnet
    - Workflows subnet
    - Jumpbox subnet
    - Bastion
- AKS cluster (private)
- Jumpbox for admin access
- NAT Gateway providing public static outbound IP
- Checkpoint Firewall in hub; VNet Peering to Central Services/Hub
- Outbound traffic from FITFILE Node to Central Services, MESH API
- Inbound paths via hub/firewall
- Private DNS zone (split-horizon) for nnuh-prod-1.fitfile.net
- TLS certificates (ACME), Cloudflare, Auth0, ACR (updates), Vault, Grafana
- Relay Server (Cohort Discovery), Hutch Bunny polling
- VPN Gateway for source data upload (depicted)

#### Matching Plan Items to Diagram Elements

- VNET and Subnets:
    - Diagram’s System/Workflows/Jumpbox subnets → Created as 192.168.200.32/27, /27, /29
    - AzureBastionSubnet → Created as 192.168.200.192/26
- AKS cluster:
    - Private AKS, Azure CNI overlay, Calico → Matches diagram intent
- Jumpbox:
    - Created, private only, accessed via Bastion → Matches diagram intent
- Bastion:
    - Created (Standard SKU) with public IP → Matches diagram’s “Bastion” element
- NAT Gateway:
    - Existing NNUHFT-SDE-nat is associated to subnets → Matches “NAT Gateway with public static outbound IP”
- Hub/Firewall/Peering:
    - VNet peering exists outside this plan (per earlier discovery)
    - Route table entries for on-prem to firewall are not in this excerpt; expected to be added → Partially matches the “inbound via firewall” design
- Platform dependencies:
    - Auth0, Cloudflare/DNS+TLS, ACR, Vault, Grafana, Relay Server → Not created in this plan; expected in platform/tooling layers
- Private DNS (split horizon):
    - Not created in this plan; to be implemented later
- Ingress and TLS:
    - Not created here; to be implemented via Kubernetes layer (Ingress controller + cert-manager)

#### Discrepancies and Notes

- Present in plan but not explicitly in diagram:
    - Specific subnet CIDR sizes (/27 for System/Workflows vs earlier notes). Diagram is conceptual; larger /27s are fine. Ensure NNUH firewall/allowlists are updated with final ranges.
    - Resource group names and tags; diagram does not prescribe these; acceptable.
- Present in diagram but not (yet) in plan:
    - Route entries to send on‑prem CIDR(s) to Checkpoint firewall (192.168.208.4). Your plan creates the route table and associations in previous output; ensure the actual route blocks are added.
    - Private DNS zone(s) and records, split-horizon DNS setup
    - Ingress controller, public vs internal ingress IP decision, and TLS automation (ACME via Cloudflare)
    - Relay Server deployment and DNS exposure
    - VPN Gateway (if needed for source data upload)
    - Egress allow-list hardening (NSG or firewall rules referencing SaaS endpoints)
- Risk item:
    - AKS version 1.33.5 may not be available/supported in UK South at deploy time

#### How Diagram Elements Relate to the Written Plan

- The plan establishes the core infrastructure building blocks that the diagram expects: private AKS, subnets, NAT egress, Bastion + Jumpbox, and the structure to add inbound firewall routes. The remaining diagram components (DNS, TLS, ingress, relay, external SaaS dependencies) are application/platform layers to be added after the cluster is up.

---

### 3) Summary Mapping Table

|Diagram Element|Terraform Plan Item|Status|Notes/Actions|
|---|---|---|---|
|VNET (existing, NNUH)|data.azurerm_virtual_network (NNUHFT-SDE-vnet1)|Aligned|Reuse existing VNet|
|VNet Peering to Hub|Pre-existing (not in plan)|Aligned (external)|Confirm stays connected|
|System Subnet|azurerm_subnet snet-ff-uks-gp-system (192.168.200.32/27)|Aligned|Larger /27 is fine|
|Workflows Subnet|azurerm_subnet snet-ff-uks-gp-workflows (192.168.200.64/27)|Aligned|Larger /27 is fine|
|Jumpbox Subnet|azurerm_subnet snet-ff-uks-gp-jumpbox (192.168.200.128/29)|Aligned|Matches diagram|
|AzureBastionSubnet|azurerm_subnet AzureBastionSubnet (192.168.200.192/26)|Aligned|Required for Bastion|
|Bastion|azurerm_bastion_host + public IP|Aligned|Standard SKU; good|
|Jumpbox|azurerm_linux_virtual_machine + NIC + NSG|Aligned|NSG allows SSH from AzureBastion only|
|NAT Gateway|data.azurerm_nat_gateway (NNUHFT-SDE-nat) + subnet associations|Aligned|Outbound via NAT GW|
|Checkpoint Firewall|Route table entries to firewall|Partial|Add on‑prem CIDR routes to 192.168.208.4|
|AKS (Private)|azurerm_kubernetes_cluster (private_cluster_enabled = true)|Aligned|Private API; overlay + Calico|
|AKS outbound egress|network_profile.outbound_type = userDefinedRouting|Aligned|Ensures NAT GW egress|
|Workflows pool (Spot)|azurerm_kubernetes_cluster_node_pool workflows|Aligned|Taints/labels set|
|Private DNS (split-horizon)|Not in plan|Gap|Implement private DNS zones/links/records|
|Ingress + TLS (ACME)|Not in plan|Gap|Ingress controller + cert-manager later|
|Relay Server|Not in plan|Gap|Deploy in platform layer; add DNS|
|VPN Gateway|Not in plan|Gap|Add if required for data upload|
|SaaS deps (Auth0, ACR, Cloudflare, Vault, Grafana)|Not in plan|Gap|Ensure outbound allowed; may use firewall rules/PE|

---

### Recommendations and Next Steps

1. Add inbound routing via firewall:

- In your route table for AKS/jumpbox subnets (in networking RG NNUHFT-SDE-Networking), add routes for on‑prem CIDRs:
    - next_hop_type = VirtualAppliance
    - next_hop_in_ip_address = 192.168.208.4
- Do not add 0.0.0.0/0 to the firewall (would break NAT GW egress).

2. Pin a supported AKS version:

- Replace 1.33.5 with a UK South supported version that supports Azure CNI overlay (e.g., 1.30.x; verify with Azure).

3. Confirm subnet CIDRs with NNUH:

- Ensure firewall/allowlists use final /27 and /29 ranges.

4. Plan the platform layer:

- Private DNS zone(s) for split-horizon nnuh-prod-1.fitfile.net; link to VNet.
- Ingress controller (likely internal ILB) and cert-manager with Cloudflare DNS-01.
- Relay Server deployment and DNS.
- Egress allow-list hardening (move from “Allow-All-Outbound” to explicit allows or rely on hub firewall FQDN rules).

5. Governance/tags:

- Ensure required tags per NNUH policy; diagram mentions naming conventions/tags.

---

### Conclusion

Your current plan delivers the core infrastructure consistent with the diagram:

- Private AKS in existing NNUH VNet
- System/Workflows/Jumpbox subnets
- Outbound via NAT Gateway
- Bastion and Jumpbox access pattern
- Correct AKS outbound_type for NAT-based egress

To fully align with the diagram, add the inbound firewall routes, adjust the AKS version, and schedule the platform/DNS/TLS/relay components in subsequent phases.
