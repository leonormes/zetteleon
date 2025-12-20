---
aliases: []
confidence: 
created: 2025-11-01T19:59:08Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: so the nat gateway can be attached to the vnet and
type: 
uid: 
updated: 
---

## So the Nat Gateway Can Be Attached to the Vnet and All Subnets Can Use it

No, the NAT gateway in Azure is *not* attached to the VNet itself—it is always attached at the *subnet* level. Only the subnets explicitly associated with the NAT gateway will use it for outbound connectivity.[^1][^2][^3][^9]

### Key Details

- **Subnet Association:** Each NAT gateway must be explicitly associated with one or more subnets inside a virtual network. There is no option to attach a NAT gateway to the whole VNet—association is per-subnet.[^3][^5][^1]
- **Multiple Subnets:** You can associate the same NAT gateway resource to multiple subnets within a single VNet (but not across VNets). Each associated subnet will use the NAT gateway for outbound traffic.[^3]
- **Unassociated Subnets:** Subnets in the same VNet that are *not* associated with any NAT gateway will not use it—those subnets will have no outbound internet access unless you configure a different outbound method (such as Azure Firewall, or the legacy default outbound access in some scenarios).[^2][^9]

### Practical Example

- Create NAT gateway → Select public IP → Select subnets → Attach.
- Subnets selected in this step get outbound via NAT gateway. Others in the VNet do *not*.
- If you want all subnets in the VNet to use NAT gateway, you must associate each subnet with it during or after deployment.[^7][^1][^3]

***

In summary: NAT gateway *must* be attached per-subnet, not at the VNet level, and only attached subnets get outbound via NAT gateway.[^9][^1][^2][^3]

<span style="display:none">[^10][^4][^6][^8]</span>

<div align="center">⁂</div>

[^1]: <https://learn.microsoft.com/en-us/azure/nat-gateway/manage-nat-gateway>

[^2]: <https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview>

[^3]: <https://learn.microsoft.com/en-us/azure/nat-gateway/nat-gateway-resource>

[^4]: <https://github.com/Azure/bicep/discussions/12817>

[^5]: <https://trendmicro.com/cloudoneconformity/knowledge-base/azure/NatGateway/check-for-private-network-integration.html>

[^6]: <https://docs.azure.cn/en-us/nat-gateway/tutorial-hub-spoke-route-nat>

[^7]: <https://learn.microsoft.com/en-us/azure/nat-gateway/quickstart-create-nat-gateway>

[^8]: <https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Cloud-Clusters-Azure%3Anc2-clusters-azure-configuring-vnets-subnets-and-nat-gateway-t.html>

[^9]: <https://learn.microsoft.com/en-us/azure/nat-gateway/faq>

[^10]: <https://docs.azure.cn/en-us/nat-gateway/troubleshoot-nat>
