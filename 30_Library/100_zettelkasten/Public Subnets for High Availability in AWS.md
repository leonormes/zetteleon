---
aliases: []
created: 2025-10-24T14:25:58+00:00
last_reviewed: 'null'
modified: 2026-07-20T16:34:26+00:00
permalink: llmeon/30-library/100-zettelkasten/public-subnets-for-high-availability-in-aws
status: 'null'
tags: [aws, high-availability, SoftwareEngineering/Networking, SoftwareEngineering/networking/cloud-networking, subnets]
title: Public Subnets for High Availability in AWS
type: 'null'
updated: null
---

Public subnets are subnets within a VPC that have a route to an Internet Gateway, allowing resources launched within them to communicate directly with the internet.

For high availability, it is a best practice to:

- Create at least two public subnets.
- Place these subnets in different Availability Zones (AZs) within the same AWS Region. This ensures that if one AZ experiences an outage, your application remains accessible through resources in another AZ.
- Assign appropriate IP ranges (e.g., `10.0.1.0/24`, `10.0.2.0/24`) from the VPC's CIDR block to each subnet.

ALBs are typically deployed across multiple public subnets to achieve fault tolerance.

---

Related: [[VPC Setup for AWS ALB]], AWS Availability Zones, High Availability Concepts
