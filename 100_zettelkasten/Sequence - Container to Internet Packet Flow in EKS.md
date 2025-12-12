---
aliases: []
confidence: 
created: 2025-10-31T11:53:00Z
epistemic: 
goal: "Understand EKS networking path"
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Trace packet flow from container to internet in EKS."
review_interval: 180
see_also: []
source_of_truth: []
status: 
tags: [eks, networking, sequence]
title: Sequence - Container to Internet Packet Flow in EKS
type: sequence
uid: 
updated: 
---

## Sequence - Container to Internet Packet Flow in EKS

1. [[100_zettelkasten/Containers Within a Pod Share Network Namespace and IP Address]]
2. [[Kubernetes Performs SNAT for Pod Egress Traffic]]
3. [[AWS ENIs Connect EKS Worker Nodes to VPC Networks]]
4. [[NAT Gateways Enable Private Resources to Access Internet]]
5. [[Internet Gateway in AWS Networking]]

**Key Points:**
- Dual NAT (kube-proxy + AWS NAT)
- VPC routing determines path
- Return traffic maintains state
