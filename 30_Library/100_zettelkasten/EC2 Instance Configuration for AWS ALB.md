---
aliases: []
created: 2025-10-24T14:25:58+00:00
last_reviewed: ''
modified: 2026-07-13T08:44:55+00:00
permalink: llmeon/30-library/100-zettelkasten/ec2-instance-configuration-for-aws-alb
status: ''
tags: [aws, cloud-computing, ec2, SoftwareEngineering/Networking]
title: EC2 Instance Configuration for AWS ALB
type: ''
updated: null
---

When using EC2 instances as targets behind an AWS Application Load Balancer (ALB), specific configurations are necessary:

- Placement: Launch EC2 instances in different public subnets (and thus different Availability Zones) to ensure high availability and fault tolerance.
- Security Groups: Configure security groups for the EC2 instances to allow:
  - SSH access (port 22) from your IP for management.
  - HTTP/HTTPS access (ports 80/443 or custom application ports like 8080) from the ALB's security group. This ensures the ALB can forward traffic to the instances.
- User Data Scripts: Utilize user-data scripts during launch to automate software installation (e.g., Apache, Nginx) and configuration, making instances ready to serve traffic immediately. This is useful for testing and demonstrating load balancing.

These instances will be registered with an ALB Target Group to receive traffic.

---

Related: What is an EC2 Instance, AWS Security Groups, [[Public Subnets for High Availability in AWS]]
