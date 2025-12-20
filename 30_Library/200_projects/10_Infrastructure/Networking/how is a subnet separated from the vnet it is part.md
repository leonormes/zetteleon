---
aliases: []
confidence: 
created: 2025-11-01T19:58:18Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: how is a subnet separated from the vnet it is part
type: 
uid: 
updated: 
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## How is a Subnet Separated from the Vnet it is part Of? So Far, I Am Picturing it as the Vnet is One Set of Ip Address that All in a Range, Which is Divided into Subsets of Ip Ranges. But Can Everything in the Vnet Communicate with Everything Else? Why Can't Something in a Subnet Reach Ips in the Same Vnet but not in Its Own Subnet Range

Within Azure, a Virtual Network (VNet) is an overarching IP address range that is segmented into subnets—each representing a smaller address range fully contained within the VNet’s space. By default, all resources in all subnets of a VNet can communicate with each other, because subnets are logical divisions for security, organization, or routing, but not for connectivity isolation.[^1][^4]

### How Subnets Relate to a VNet

- A subnet is simply a subset of IP addresses carved from the VNet’s overall address range.[^4][^1]
- Example: VNet = 10.0.0.0/16, Subnet1 = 10.0.1.0/24, Subnet2 = 10.0.2.0/24, etc.
- Each VM or resource connects to one subnet, but the default routing within a VNet ensures every IP in the VNet (regardless of subnet) can reach every other IP.[^4]

### Subnet Communication and Isolation

- By default, everything in a VNet—across all subnets—*can communicate* with everything else in that VNet.[^4]
- Subnets do not isolate traffic; they are not firewalls or VLANs. They are used for addressing, grouping, and for applying network security controls.[^1][^4]
- Traffic between subnets flows freely unless restricted by security components (see below).[^2][^4]

### Blocking Intra-VNet Communication

- To *prevent* a resource in one subnet from accessing another subnet (or specific resources within it), you must use Network Security Groups (NSGs) to create allow/deny rules targeting the relevant IP ranges or ports.[^5][^2]
- Without custom NSG rules, there is no built-in segmentation beyond the IP address boundaries.
- NSGs can be scoped to subnets and/or network interfaces for granular control, enabling explicit denial of cross-subnet flows as needed.[^2][^5]

### Why Might Subnets Not Communicate

- If something in a subnet cannot reach other IPs in the VNet, NSG rules or custom routes are blocking the traffic.[^5][^2]
- Check the effective NSG and route tables for the subnet or NIC to diagnose such issues.[^2]

***

In summary: subnets are address segments within a VNet, not default connectivity boundaries. Full VNet communication is the norm unless explicitly restricted by security rules (NSGs) or routing.[^5][^2][^4]

<span style="display:none">[^3][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: <https://learn.microsoft.com/en-us/azure/virtual-network/concepts-and-best-practices>

[^2]: <https://learn.microsoft.com/en-us/azure/virtual-network/network-security-group-how-it-works>

[^3]: <https://learn.microsoft.com/en-us/azure/azure-sql/database/vnet-service-endpoint-rule-overview?view=azuresql>

[^4]: <https://learn.microsoft.com/en-us/azure/virtual-network/network-overview>

[^5]: <https://stackoverflow.com/questions/74818906/azure-network-prevent-subnet-to-subnet-communication>

[^6]: <https://azure.github.io/PSRule.Rules.Azure/en/rules/Azure.VNET.PrivateSubnet/>

[^7]: <https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq>

[^8]: <https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview>

[^9]: <https://www.reddit.com/r/AZURE/comments/14hu0hq/can_someone_explain_to_me_vnet_subnets_nsg_and/>
