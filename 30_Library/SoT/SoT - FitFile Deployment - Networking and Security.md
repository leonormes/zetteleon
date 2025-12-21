---
aliases: [FitFile Deployment Networking and Security]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T12:00:00Z
purpose: To provide a detailed guide of the networking and security for the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, networking, security]
title: SoT - FitFile Deployment - Networking and Security
type: SoT
uid: 
updated: 
version: 1.0
---

## Networking and Security

## Key Actions

- **Load Balancers and DNS:**
  - **Configuration File**: `main.tf`
  - **Public ALB for Relay Service**:
    - **Security Group**: `aws_security_group.relay_alb`
    - **ALB**: `aws_lb.relay_public`
    - **Target Group**: `aws_lb_target_group.relay`
    - **Listener**: `aws_lb_listener.relay_https`
  - **Route53 DNS**:
    - **Hosted Zone**: Managed in `module.codisc_eoe_sde_domain_setup`
    - **DNS Records**: Configured in `aws_route53_record` resources
- **Security and Access Control:**
  - **Configuration Files**: `main.tf`, `./modules/eks/*`
  - **Security Groups**: Defined for ALB and other resources
  - **IAM Policies**: Managed through EKS module
  - **Network ACLs**: Configured in VPC module

---

- **Network Policies:** [[Network Policies]], [[Proxy Allow list]]
- **Ingress:** [[Nginx Ingress Controller Configuration]]
- **DNS & Service Mesh:** [[MESH service firewall allowlist requirements]]
- **IP Management:**
    - [[IP allocation on Azure public deployment PROD]]
    - [[IPs needed for FITFILE]]
    - [[Minimizing IP Addresses for EKS Node Groups]]
    - [[Minimum IP Requirements for a Firewall Subnet]]
    - [[QU - What is the difference between AWS and Azure IP management on K8s clusters]]
- **Advanced Security:** [[Why HTTPS is not good enough]]
