---
aliases: []
created: 2025-10-24T14:25:58+00:00
last_reviewed: ''
modified: 2026-07-20T16:34:31+00:00
permalink: llmeon/30-library/100-zettelkasten/creating-an-aws-application-load-balancer-alb
status: ''
tags: [aws, load-balancing, SoftwareEngineering/Networking, SoftwareEngineering/networking/cloud-networking]
title: Creating an AWS Application Load Balancer (ALB)
type: ''
updated: null
---

The process of creating an AWS Application Load Balancer (ALB) involves several key configurations:

1. Type: Choose "Application Load Balancer".
2. Scheme: Select "Internet-facing" for public applications or "Internal" for private applications within your VPC.
3. VPC and Subnets: Specify the VPC where the ALB will operate and select at least two public subnets in different Availability Zones. The ALB will deploy components in these subnets.
4. Security Groups: Attach a security group to the ALB that allows inbound HTTP (port 80) and/or HTTPS (port 443) traffic from the internet (`0.0.0.0/0`).
5. Listeners and Routing:
    - Configure a listener (e.g., HTTP on port 80).
    - Define listener rules to forward incoming requests to a specific [[AWS ALB Target Groups]]. This is where you link the ALB to your backend instances.

Once created, the ALB provides a DNS name that acts as the single entry point for your application.

---

Related: [[What is an AWS Application Load Balancer (ALB)]], AWS Security Groups, [[Public Subnets for High Availability in AWS]]
