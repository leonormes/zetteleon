---
aliases: []
confidence: 
created: 2025-10-24T14:25:58Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, health-checks, load-balancing, target-groups, topic/technology/networking]
title: AWS ALB Target Groups
type:
uid: 
updated: 
version:
---

An **ALB Target Group** is a logical grouping of targets (e.g., EC2 instances, IP addresses, Lambda functions) that an Application Load Balancer (ALB) routes requests to.

Key aspects of Target Groups:

- **Registration**: You register your backend instances (e.g., EC2 instances) with a target group.
- **Health Checks**: Target groups are crucial for configuring **health checks**. The ALB continuously monitors the health of registered targets. If a target fails health checks, the ALB stops routing traffic to it, ensuring reliable failover.
- **Routing**: Each listener rule on an ALB specifies a target group to which traffic should be forwarded.

Different target groups can be used for different types of traffic or different versions of an application, enabling advanced routing strategies.

---

**Related:** [[What is an AWS Application Load Balancer (ALB)]]
