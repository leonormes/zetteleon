---
aliases: []
confidence: 
created: 2025-11-01T19:59:32Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Clarify if one NAT gateway can serve multiple subn
type: 
uid: 
updated: 
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Clarify if One NAT Gateway Can Serve Multiple Subnets within the Same VNet

Yes, a single NAT gateway in Azure can be attached to multiple subnets within the same VNet to provide outbound internet connectivity for those subnets. The limit is up to 800 subnets per NAT gateway within a VNet. All associated subnets will share the NAT gateway's IPs and SNAT port inventory for outbound connections.[^1][^2]

- You do not need separate NAT gateways for each subnet, unless you want different outbound IPs or unique egress paths.
- NAT gateways cannot span multiple VNets, and cannot be attached to gateway subnets.[^2][^1]

This allows central management and efficient scaling of outbound traffic for large deployments.[^1][^2]

<span style="display:none">[^3][^4][^5][^6][^7][^8]</span>

<div align="center">⁂</div>

[^1]: <https://learn.microsoft.com/en-us/azure/nat-gateway/nat-gateway-resource>

[^2]: <https://learn.microsoft.com/en-us/azure/nat-gateway/faq>

[^3]: <https://www.reddit.com/r/AZURE/comments/1dfnoy6/nat_gateway_only_on_a_single_subnet/>

[^4]: <https://stackoverflow.com/questions/60574735/aws-can-two-private-subnets-in-two-azs-share-the-same-nat-gateway>

[^5]: <https://www.alibabacloud.com/help/en/nat-gateway/use-cases/deploy-multiple-internet-nat-gateways-in-one-vpc>

[^6]: <https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html>

[^7]: <https://aws.amazon.com/blogs/networking-and-content-delivery/using-nat-gateways-with-multiple-amazon-vpcs-at-scale/>

[^8]: <https://docs.azure.cn/en-us/nat-gateway/tutorial-hub-spoke-route-nat>
