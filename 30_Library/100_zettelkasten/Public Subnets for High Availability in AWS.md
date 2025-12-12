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
tags: [aws, high-availability, subnets, topic/technology/networking, topic/technology/networking/cloud-networking]
title: Public Subnets for High Availability in AWS
type:
uid: 
updated: 
version:
---

**Public subnets** are subnets within a VPC that have a route to an Internet Gateway, allowing resources launched within them to communicate directly with the internet.

For high availability, it is a best practice to:

- Create at least two public subnets.
- Place these subnets in **different Availability Zones (AZs)** within the same AWS Region. This ensures that if one AZ experiences an outage, your application remains accessible through resources in another AZ.
- Assign appropriate IP ranges (e.g., `10.0.1.0/24`, `10.0.2.0/24`) from the VPC's CIDR block to each subnet.

ALBs are typically deployed across multiple public subnets to achieve fault tolerance.

---

**Related:** [[VPC Setup for AWS ALB]], AWS Availability Zones, High Availability Concepts
