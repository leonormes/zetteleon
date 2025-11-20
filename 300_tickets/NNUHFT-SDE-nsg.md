---
aliases: []
confidence:
created: 2025-11-19T02:16:11Z
epistemic:
last_reviewed:
modified: 2025-11-19T14:53:10Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
title: NNUHFT-SDE-nsg
type:
uid:
updated:
---

This JSON represents an **Azure Network Security Group (NSG)** configuration. It acts as a firewall that filters network traffic to and from Azure resources in an Azure Virtual Network (VNet).

Here is the analysis of the configuration formatted for your notes.

***

## NNUHFT-SDE-nsg

### Metadata

- **Resource Name:** `NNUHFT-SDE-nsg`
- **Region:** `uksouth` (London)
- **Environment:** `live`
- **Department:** `SDE` (Likely Secure Data Environment)
- **Status:** `Provisioned / Succeeded`

### Rule Configuration Overview

> [!IMPORTANT] No Custom Rules Defined
> The `securityRules` array in this JSON is empty (`[]`). This means this NSG is currently operating **solely on Azure Default Security Rules**. There are no custom "Allow" or "Deny" rules specific to your application yet.

The default behaviour is defined by the `defaultSecurityRules` section. These rules cannot be deleted, but they can be overridden by creating higher-priority custom rules (priorities 100-4096).

#### 1. Inbound Rules (Ingress)
*Traffic coming **into** the subnet or network interface.*

| Priority | Name | Action | Explanation |
| :--- | :--- | :--- | :--- |
| **65000** | `AllowVnetInBound` | **Allow** | Allows traffic from any resource inside the same Virtual Network (or peered VNets). Machines in this subnet can talk to each other. |
| **65001** | `AllowAzureLoadBalancerInBound`| **Allow** | Allows traffic from Azure's infrastructure Load Balancer. This is required for Load Balancer health probes to check if your VMs are alive. |
| **65500** | `DenyAllInBound` | **Deny** | **The "Catch-All" Rule.** If traffic does not match the two rules above, it is blocked. Effectively, this blocks all traffic from the public internet unless you add a custom rule. |

#### 2. Outbound Rules (Egress)
*Traffic going **out** of the subnet or network interface.*

| Priority | Name | Action | Explanation |
| :--- | :--- | :--- | :--- |
| **65000** | `AllowVnetOutBound` | **Allow** | Resources can send traffic to any other resource within the Virtual Network. |
| **65001** | `AllowInternetOutBound` | **Allow** | **Security Note:** Resources are allowed to initiate connections to the public Internet. For a "Secure Data Environment" (SDE), this is often considered a security risk (data exfiltration) and is usually restricted using Azure Firewall or a custom "Deny" rule. |
| **65500** | `DenyAllOutBound` | **Deny** | Blocks traffic to anywhere that isn't the VNet or the Internet. |

### Summary of Current Posture

- **Internal Communication:** Open. All devices in the VNet can communicate on all ports.
- **Public Access (Inbound):** Closed. No one from the internet can reach these resources.
- **Internet Access (Outbound):** Open. The servers can download updates or connect to external APIs, but this also allows potential data exfiltration paths.

***
