---
aliases: []
confidence: 
created: 2025-03-13T09:29:09Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [dns]
title: VPC DNS Configuration
type: 
uid: 
updated: 
version: 
---

- DNS Resolution and Hostnames: When you create a VPC, DNS resolution and DNS hostnames must be enabled. This is a prerequisite for EKS, and these features are enabled by default when you create a VPC using the AWS CLI. This ensures that instances within your VPC can resolve domain names.
- Amazon DNS Server (Route 53 Resolver): Each Availability Zone in your AWS Region has a built-in Amazon DNS server (also known as Route 53 Resolver). This service provides a reliable and scalable solution for domain name resolution within your VPC. This resolver is essential for resolving the private DNS names used by resources within your VPC.
- Private Hosted Zones: To use custom domain names (e.g., `example.com`) for resources in your VPC instead of the default private IP addresses or AWS-provided private DNS hostnames, you can create a private hosted zone in Route 53. This private hosted zone will hold information about how traffic should be routed within one or more VPCs. This allows you to manage internal domain names within your EKS cluster and keep your resources private.

[[300_Documentation/FITFILE/Cloud/AWS/VPC DNS Configuration]]
