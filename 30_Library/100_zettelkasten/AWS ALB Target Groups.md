---
aliases: []
created: 2025-10-24T14:25:58+00:00
last_reviewed: 'null'
modified: 2026-08-29T09:35:57+00:00
permalink: llmeon/30-library/100-zettelkasten/aws-alb-target-groups
status: 'null'
tags: [aws, health-checks, load-balancing, SoftwareEngineering/Networking, target-groups]
title: AWS ALB Target Groups
type: 'null'
updated: null
---

An ALB Target Group is a logical grouping of targets (e.g., EC2 instances, IP addresses, Lambda functions) that an Application Load Balancer (ALB) routes requests to.

Key aspects of Target Groups:

- Registration: You register your backend instances (e.g., EC2 instances) with a target group.
- Health Checks: Target groups are crucial for configuring health checks. The ALB continuously monitors the health of registered targets. If a target fails health checks, the ALB stops routing traffic to it, ensuring reliable failover.
- Routing: Each listener rule on an ALB specifies a target group to which traffic should be forwarded.

Different target groups can be used for different types of traffic or different versions of an application, enabling advanced routing strategies.

---

Related: [[What is an AWS Application Load Balancer (ALB)]]
