---
created: 2026-04-28T11:23:12+00:00
modified: 2026-04-28T16:26:53+00:00
title: pieces_copilot_message_export_april_28_2026_12_23pm
---

## VNet Analysis: `aks-vnet-32767343` (Staging AKS)

Here's a structured breakdown of this VNet payload for the FITFILE staging AKS cluster.

---

### Identity & Provenance

| Property | Value |
|---|---|
| Name | `aks-vnet-32767343` |
| Resource Group | `MC_fitfile-cloud-staging-rg_…_uksouth` (AKS-managed RG) |
| Location | UK South |
| Created By | Oliver Rushton (`development/main.tf`) |
| Environment | staging |
| Provisioning State | Succeeded |

> Important: This VNet lives in the AKS-managed `MC_*` resource group, meaning AKS owns and created it automatically. This is a system-managed VNet—not a BYO (Bring Your Own) VNet pattern. This restricts your governance control (tagging, lifecycle, peering) unless you've deliberately routed Terraform to manage it.

---

### Address Space

- VNet Supernet: `10.224.0.0/12` → covers `10.224.0.0`–`10.239.255.255` (1,048,576 total IPs)

All three subnets fall cleanly within this /12 supernet:

| Subnet | CIDR | Size | Delegation | Purpose |
|---|---|---|---|---|
| `aks-subnet` | `10.224.0.0/16` | 65,536 IPs | None | AKS nodes + pods (Azure CNI) |
| `aks-appgateway` | `10.238.0.0/24` | 256 IPs | `Microsoft.ServiceNetworking/trafficControllers` | App Gateway for Containers (ALB Controller) |
| `aks-virtualkubelet` | `10.239.0.0/16` | 65,536 IPs | `Microsoft.ContainerInstance/containerGroups` | ACI burst / Virtual Kubelet |

---

### `aks-subnet`—Deep Detail

This is the primary AKS node/pod subnet. Key observations:

- NSG attached: `aks-agentpool-32767343-nsg`
- IP Configurations: The subnet has ~400 `ipConfigurations` from VMSS `AKS-SYSTEM-31071534-VMSS`, across 4 VM instances: `2814`, `2815`, `2816`, `2817`
- Each VM has IPCONFIG1–IPCONFIG99 (99 IPs per NIC)—this is Azure CNI pre-allocation behaviour. Each node pre-claims a chunk of IPs for pod scheduling without waiting for pod creation.

```
4 nodes × 99 pre-allocated IPs = 396 consumed IPs on aks-subnet
```

This is expected and healthy for Azure CNI, but worth tracking as the node pool scales—a `/16` gives you headroom, but dense pre-allocation can consume it faster than pod count alone suggests.

---

### `aks-appgateway`—Notable Delegation

The delegation `Microsoft.ServiceNetworking/trafficControllers` indicates this is Application Gateway for Containers (AGC), not the classic Azure Application Gateway. This is a newer, Kubernetes-native ingress pattern managed via the ALB Controller. Worth confirming this is intentional vs. a classic AGIC deployment if there's any routing ambiguity.

---

### ⚠️ Structural Flags to Review

1. No VNet Peerings (`virtualNetworkPeerings: []`)

This VNet is completely isolated. If you're planning to:

- Attach Private Endpoints that need to be resolved from another VNet (e.g., a hub or shared services VNet)
- Connect to FITFILE's wider Azure network topology

…then the absence of peering is a blocker. This aligns directly with your ongoing Private Endpoints architecture work—this would need a peering to your Shared Services VNet before private DNS resolution can flow correctly.

1. `privateEndpointNetworkPolicies: Disabled` on ALL subnets

This is the default, but it means NSG rules and UDRs do NOT apply to private endpoint NICs within these subnets. If you want to enforce network policy on private endpoints (e.g., restrict which sources can reach a private endpoint), you need to set this to `Enabled` (or `NetworkSecurityGroupEnabled` / `RouteTableEnabled` in the newer API).

1. DDoS Protection: Disabled

`"enableDdosProtection": false`—expected for a staging environment but flag for production parity review.

1. System-Managed RG Risk

Because this lives in the `MC_*` resource group, any `terraform destroy` or AKS cluster deletion will wipe this VNet. If you attach additional resources (Private Endpoints, peerings, DNS zones) to this VNet, they become orphan-risk items. The defensive documentation play here is to log this dependency chain in Confluence explicitly.

---

### Summary Proposition

> The staging AKS VNet is a fully functional but isolated Azure CNI network with no peering, disabled private endpoint policies, and system-managed lifecycle risk—none of which are blockers today, but all three become critical dependencies if Private Endpoints are introduced.
