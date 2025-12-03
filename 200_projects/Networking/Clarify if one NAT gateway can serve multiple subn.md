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

## Clarify if One NAT Gateway Can Serve Multiple Subnets within the Same VNet

Yes, a single NAT gateway in Azure can be attached to multiple subnets within the same VNet to provide outbound internet connectivity for those subnets. The limit is up to 800 subnets per NAT gateway within a VNet. All associated subnets will share the NAT gateway's IPs and SNAT port inventory for outbound connections.[^1][^2]

- You do not need separate NAT gateways for each subnet, unless you want different outbound IPs or unique egress paths.
- NAT gateways cannot span multiple VNets, and cannot be attached to gateway subnets.[^2][^1]

This allows central management and efficient scaling of outbound traffic for large deployments.[^1][^2]
