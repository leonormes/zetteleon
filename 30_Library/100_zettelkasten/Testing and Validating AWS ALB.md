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
tags: [aws, load-balancing, testing, topic/technology/networking/cloud-networking]
title: Testing and Validating AWS ALB
type:
uid: 
updated: 
version:
---

After deploying an AWS Application Load Balancer (ALB), it's crucial to test and validate its functionality to ensure traffic is being distributed correctly and the application is accessible.

**Validation Steps:**

1. **Access via DNS Name**: Use the ALB's provisioned DNS name (e.g., `my-alb-123456789.us-east-1.elb.amazonaws.com`) in a web browser or `curl` command.
2. **Verify Load Distribution**: If your backend instances are configured to display unique identifiers (e.g., instance ID, private IP), repeatedly refresh the page. You should observe traffic alternating between the different EC2 instances, confirming the ALB is distributing requests.
3. **Health Check Status**: Monitor the health status of your targets in the ALB Target Group. All registered instances should show as "healthy".

Successful validation confirms that the ALB is correctly routing traffic to healthy backend instances, providing load balancing and high availability.

---

**Related:** [[Creating an AWS Application Load Balancer (ALB)]], [[AWS ALB Target Groups]]
