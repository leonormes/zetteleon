---
aliases: ["Elastic Network Interfaces"]
confidence: 0.9
created: 2025-10-31T11:52:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T11:52:00Z
purpose: "Explain AWS ENIs in EKS networking."
review_interval: 90
see_also: ["AWS Networking MOC.md", "Kubernetes Performs SNAT for Pod Egress Traffic.md"]
source_of_truth: []
status: seedling
tags: [aws, eks, networking]
title: AWS ENIs Connect EKS Worker Nodes to VPC Networks
type: concept
uid: 
updated: 
---

## AWS ENIs Connect EKS Worker Nodes to VPC Networks

**Summary:** Elastic Network Interfaces (ENIs) provide VPC connectivity for EKS worker nodes by:
- Assigning private IPs from subnet
- Enabling security group attachment
- Supporting multiple IP addresses

**EKS Usage:**
- Primary ENI for node communication
- Additional ENIs for pod networking (when using certain CNIs)
- Traffic passes through ENI to reach VPC routes
