---
aliases: []
confidence: 
created: 2025-10-24T14:25:58Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, route-tables, topic/technology/networking, topic/technology/networking/cloud-networking]
title: Route Tables for Internet Access in AWS
type:
uid: 
updated: 
version:
---

A **route table** contains a set of rules, called routes, that determine where network traffic from your subnet or gateway is directed.

To enable internet access for resources in public subnets:

- Create a route table and associate it with your public subnets.
- Add a default route: `0.0.0.0/0` (representing all IPv4 destinations) pointing to the **Internet Gateway (IGW)**. This route directs all traffic destined for outside the VPC to the IGW, allowing it to reach the internet.

Each subnet in a VPC must be associated with a route table. If you don't explicitly associate a subnet with a route table, it's implicitly associated with the main route table.

---

**Related:** [[Internet Gateway in AWS Networking]], [[VPC Setup for AWS ALB]]
