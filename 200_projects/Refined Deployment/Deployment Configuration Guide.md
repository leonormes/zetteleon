---
aliases: []
confidence: 
created: 2025-08-14T02:42:49Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [config, documentation, guide, project/work/deployment, setup]
title: Deployment Configuration Guide
type:
uid: 
updated: 
version:
---

## Table of Contents

1. [EKS Cluster Configuration](#eks-cluster-configuration)
2. [VPC and Networking](#vpc-and-networking)
3. [Load Balancers and DNS](#load-balancers-and-dns)
4. [Security and Access Control](#security-and-access-control)

## EKS Cluster Configuration

**Configuration File**: `main.tf` (EKS Module)

Key Configuration Points:

- Cluster version: Defined in `local.eks.kubernetes_version`
- Node groups: Configured in `local.eks.node_groups`
- Private subnet access: Defined in `eks_private_subnet_access_cidr_blocks`
- IAM Access: Configured in `iam_user_access_config`

**Action Required**:

- Update node group configurations in `local.eks.node_groups`
- Add/remove IAM users in `var.cluster_admin_users`

## VPC and Networking

**Configuration Files**:

- `main.tf` (VPC Module)
- `./modules/vpc/*`

Key Components:

- VPC CIDR: Defined in `local.vpc_cidr`
- Subnets: Configured in `local.network.subnets`
- Route Tables: Managed in the `gateway` module

**Action Required**:

- Update VPC CIDR in `local.vpc_cidr`
- Modify subnet configurations in `local.network.subnets`

## Load Balancers and DNS

**Configuration File**: `main.tf`

Components:

1. **Public ALB for Relay Service**

- Security Group: `aws_security_group.relay_alb`
- ALB: `aws_lb.relay_public`
- Target Group: `aws_lb_target_group.relay`
- Listener: `aws_lb_listener.relay_https`

2. **Route53 DNS**

- Hosted Zone: Managed in `module.codisc_eoe_sde_domain_setup`
- DNS Records: Configured in `aws_route53_record` resources

**Action Required**:

- Update ALB security group rules for new IP ranges
- Modify health check settings in target group configuration
- Update certificate ARN if using custom SSL certificates

## Security and Access Control

**Configuration Files**:

- `main.tf`
- `./modules/eks/*`

Key Components:

- Security Groups: Defined for ALB and other resources
- IAM Policies: Managed through EKS module
- Network ACLs: Configured in VPC module

**Action Required**:

- Review and update security group rules as needed
- Audit IAM policies and roles periodically
- Update network ACLs for new security requirements
