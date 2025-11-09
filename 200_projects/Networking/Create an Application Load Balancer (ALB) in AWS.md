---
aliases: []
confidence: 
created: 2025-10-28T11:09:34Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:38:21Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: Create an Application Load Balancer (ALB) in AWS
type:
uid: 
updated: 
version:
---

## <https://youtube.com/watch?v=ZGGpEwThhrM>\&si=buQw7FHKHsSQ5JnO

Here is a concise technical summary of the “Create an Application Load Balancer (ALB) in AWS” tutorial presented by Tiny Technical Tutorials, with actionable steps and shell/code examples for reference[^1_1].

### Core Process Overview

The video demonstrates how to:

- Launch two Linux EC2 web servers in different Availability Zones
- Install basic web server software and set up a sample HTML page
- Configure related security groups
- Set up an Application Load Balancer (ALB) for HTTP traffic
- Create and configure a Target Group
- Route and test traffic, including simulating instance failure

***

#### Step-by-Step Process

##### 1. Launch EC2 Instances

- **Launch Two EC2 Instances:** Use different Availability Zones (e.g., `us-east-2a` and `us-east-2b`) for high availability.
- **User Data Script for Web Servers:** Add a launch script via “Advanced Details - user data” to install a web server and set up an HTML file.

##### Example EC2 User Data Script

```bash
#!/bin/bash
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello World from $(hostname)</h1>" > /var/www/html/index.html
```

- Each instance will display a different hostname in its HTML response[^1_1].

***

##### 2. Configure Security Group

- **Create a Security Group (e.g., `ALB-demo-HTTP-open`):**
    - Add HTTP rule: allow inbound traffic on port 80 from anywhere.

***

##### 3. Test EC2 Instances

- **Copy Public IPv4 Address of Each Instance:** Visit directly via browser on port 80 (http://[IP]) to verify that you see “Hello World” and hostname.
- **Tip:** Avoid the console “Open address” shortcut if SSL isn’t set up yet[^1_1].

***

##### 4. Create the Application Load Balancer

- **Choose “Application Load Balancer” in AWS Console**
    - Type: “Internet-facing”
    - Select all available subnets (multi-AZ for HA)
    - Assign new security group (e.g., `ALB-demo-SG`)
    - Listener: Add HTTP port 80

***

##### 5. Create Target Group

- **Create Target Group and Register Instances:**
    - Instances: Add both EC2s to the target group and mark “include as pending.”
    - Basically, ALB will route requests to healthy instances in the target group[^1_1].

***

##### 6. Test Load Balancer and Failover Behavior

- **Use the ALB DNS Endpoint:** Requests should alternate between the two EC2 servers (verified by changing hostnames).
- **Simulate Failure:** Stop one EC2 instance; ALB routes all traffic to the healthy one.
    - Resume the stopped instance to see load balancing resume automatically[^1_1].

***

#### Actionable Checklist

- Launch 2 Linux EC2s, each in a separate AZ, with web server user-data script.
- Add both to a security group with port 80 open for HTTP.
- Verify web server response via direct IP access.
- Create an ALB (internet-facing), configure listeners, and set security group.
- Create a target group and register both EC2s.
- Confirm round-robin traffic via ALB DNS.
- Test failover by stopping one instance, observe ALB’s health checks and routing.

***

#### Useful AWS CLI Commands

*Replace `[instance-id]`, `[security-group-id]`, `[target-group-arn]`, etc. as needed.*

- Attach security group:

```sh
aws ec2 modify-instance-attribute --instance-id [instance-id] --groups [security-group-id]
```

- Register instance to target group:

```sh
aws elbv2 register-targets --target-group-arn [target-group-arn] --targets Id=[instance-id]
```

- Describe ALB DNS:

```sh
aws elbv2 describe-load-balancers
```

***

#### Key Concepts Covered

- Application Load Balancer routes HTTP traffic, supports multiple AZs and high availability.
- Target Groups are required for ALB routing.
- Security groups must be set for both instances and the load balancer.
- AWS automates health checks and instance replacement[^1_1].

***

This tutorial offers a practical, minimal template for setting up highly available web applications in AWS using EC2 and ALB—with real shell steps and configuration pointers included at each stage[^1_1].

<div align="center">⁂</div>

[^1_1]: <https://www.youtube.com/watch?v=ZGGpEwThhrM>\&si=buQw7FHKHsSQ5JnO
