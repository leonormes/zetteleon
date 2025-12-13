---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy]
title: AWS Deployment Index
type: documentation
uid: 
updated: 
version:
---

## AWS Deployment Documentation Index

### Core Deployment Process

### Infrastructure Setup

### Additional Resources

### Quick Access Sections

#### Prerequisites

- AWS Account setup
- Terraform service account
- API credentials
- Region selection
- DevOps engineer access

#### Key Components

1. Tooling Phase:
   - Grafana
   - Vault
   - Auth0
   - AWS Extra

2. Infrastructure Phase:
   - Kubernetes
   - Virtual Machines
   - IP Configurations
   - SSH Keys

3. Platform Phase:
   - Ingress Controller
   - Vault Secret Operator
   - ArgoCD
   - ACR secrets

4. Application Phase:
   - Application manifests
   - Deployment configurations

### Main Components

1. VPC Configuration
   - Private VPC with CIDR `10.0.0.0/16`
   - Multiple subnet tiers:
     - Firewall subnet
     - VPC Endpoints subnet
     - EKS subnets (2 AZs)
     - Jumpbox subnet
     - NAT subnet (public)
   - Uses 2 Availability Zones for high availability

2. Network Gateway Setup
   - NAT Gateway for outbound internet access
   - Firewall Gateway for controlled traffic flow
   - Route tables configured for secure network isolation

3. VPC Endpoints
   - Gateway endpoint for S3
   - Interface endpoints for critical AWS services:
     - ECR (API and Docker registry)
     - Systems Manager (SSM)
     - CloudWatch Logs
     - EC2 API
     - STS
     - Elastic Load Balancing

4. EKS Cluster
   - Private cluster (no public endpoint access)
   - Node groups configuration:
     - SystemNodeGroup: General purpose nodes
     - WorkflowsNodeGroup: Dedicated nodes for workflows
   - Uses Amazon Linux 2 AMI
   - m5.xlarge instance types

5. Jumpbox
   - Secure access point for cluster management
   - Located in dedicated subnet
   - Used for cluster administration

### Main Variables

1. Core Variables
   - `name`: Cluster name prefix (ff-eoe-sde)
   - `region`: AWS region (eu-west-2)
   - `vpc_cidr`: VPC CIDR block

2. EKS Configuration
   - `cluster_version`: Kubernetes version
   - `authentication_mode`: Set to "API"
   - `node_groups`: Configuration for different node groups
   - `subnet_ids`: Private subnets for EKS nodes

3. Security Variables
   - `eks_private_subnet_access_cidr_blocks`: Allowed CIDR blocks for API access
   - `cluster_admin_users`: IAM users with cluster admin access
   - `eks_elb_security_group_inbound_rules`: Load balancer access rules

### Security Features Implemented

1. Network Security
   - Fully private cluster with no public endpoint
   - Network segmentation with dedicated subnets
   - Firewall Gateway for traffic control
   - NAT Gateway for controlled outbound access

2. Access Control
   - IAM roles and policies for cluster management
   - OIDC provider integration for pod IAM roles
   - Private API endpoint with restricted access
   - Jumpbox as the sole entry point

3. Service Security
   - VPC endpoints for secure AWS service access
   - Security groups with minimal required access
   - Private subnets for worker nodes
   - ELB security group with restricted access

### Potential Security Enhancements

1. Encryption
   - Enable EKS secrets encryption with KMS (currently commented out)
   - Enable EBS volume encryption by default
   - Enable CloudWatch logs encryption

2. Monitoring and Logging
   - Enable EKS control plane logging (currently disabled)
   - Implement AWS GuardDuty for threat detection
   - Add AWS Config rules for compliance monitoring

3. Network Security
   - Implement Network Firewall rules
   - Add Web Application Firewall (WAF) for ingress protection
   - Network access analyzer for security validation

4. Access Control
   - Implement AWS Organizations SCPs
   - Add role-based access control (RBAC) with finer granularity
   - Implement AWS IAM Access Analyzer

5. Compliance and Auditing
   - Enable AWS CloudTrail for API auditing
   - Implement regular security assessments
   - Add compliance validation tools

6. Container Security
   - Implement container image scanning
   - Add pod security policies
   - Implement runtime security monitoring

This infrastructure follows AWS best practices for a private EKS deployment with strong security controls. The modular approach allows for easy maintenance and updates while maintaining security standards.

I'll analyze the current structure and suggest how it could be modularized more flexibly for different customer requirements.

### Current Structure Analysis

The infrastructure is currently organized with these main modules:

- VPC
- Gateway
- VPC Endpoints
- Jumpbox
- EKS

### Suggested Modular Architecture

1. Base Infrastructure Module

```hcl
module "base_infrastructure" {
  source = "./modules/base-infrastructure"
  
  # Core configuration
  environment         = var.environment
  customer_name       = var.customer_name
  region             = var.region
  
  # Network configuration (with defaults that can be overridden)
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  subnet_structure   = var.subnet_structure  # Map of subnet configurations
  
  # Tags
  custom_tags        = var.custom_tags
}
```

2. Security Layer Module

```hcl
module "security_layer" {
  source = "./modules/security-layer"
  
  # Base dependencies
  vpc_id             = module.base_infrastructure.vpc_id
  subnet_ids         = module.base_infrastructure.subnet_ids
  
  # Security configurations
  enable_firewall    = var.enable_firewall
  enable_jumpbox     = var.enable_jumpbox
  jumpbox_config     = var.jumpbox_config
  firewall_rules     = var.firewall_rules
  
  # VPC Endpoints configuration
  vpc_endpoints      = var.required_vpc_endpoints
}
```

3. EKS Platform Module

```hcl
module "eks_platform" {
  source = "./modules/eks-platform"
  
  # Cluster configuration
  cluster_name       = var.cluster_name
  cluster_version    = var.cluster_version
  
  # Network references
  vpc_id            = module.base_infrastructure.vpc_id
  subnet_ids        = module.base_infrastructure.subnet_ids
  
  # Node groups with flexible configuration
  node_groups       = var.node_groups
  
  # Access configuration
  auth_config       = var.auth_config
  admin_roles       = var.admin_roles
}
```

### Key Improvements

1. Variable Configuration Files
Create template configuration files for different customer profiles:

```hcl
# small-business.tfvars
cluster_size = "small"
node_groups = {
  system = {
    instance_types = ["t3.medium"]
    min_size = 1
    max_size = 3
  }
}

# enterprise.tfvars
cluster_size = "large"
node_groups = {
  system = {
    instance_types = ["m5.xlarge"]
    min_size = 2
    max_size = 6
  }
  workflows = {
    instance_types = ["c5.xlarge"]
    min_size = 1
    max_size = 10
  }
}
```

2. Flexible Network Configuration

```hcl
variable "subnet_structure" {
  type = map(object({
    cidr_offset     = number
    type            = string  # private/public
    purpose         = string  # eks/endpoints/management
    enable_natgw    = bool
    enable_endpoints = bool
  }))
}
```

3. Conditional Features

```hcl
variable "feature_flags" {
  type = object({
    enable_jumpbox          = bool
    enable_firewall        = bool
    enable_vpc_endpoints   = bool
    enable_cluster_autoscaling = bool
    enable_monitoring      = bool
  })
  default = {
    enable_jumpbox          = true
    enable_firewall        = true
    enable_vpc_endpoints   = true
    enable_cluster_autoscaling = false
    enable_monitoring      = false
  }
}
```

4. Security Profile Templates

```hcl
variable "security_profile" {
  type = string
  validation {
    condition     = contains(["basic", "standard", "enhanced"], var.security_profile)
    error_message = "Security profile must be one of: basic, standard, enhanced"
  }
}
```

### Implementation Strategy

1. Root Module Structure

```sh
.
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
│   ├── base-infrastructure/
│   ├── security-layer/
│   ├── eks-platform/
│   └── addons/
├── profiles/
│   ├── small-business/
│   ├── medium-business/
│   └── enterprise/
└── examples/
    ├── basic-setup/
    ├── multi-tenant/
    └── high-availability/
```

2. Customer-Specific Configuration

```sh
customers/
├── customer1/
│   ├── main.tf
│   ├── terraform.tfvars
│   └── backend.tf
└── customer2/
    ├── main.tf
    ├── terraform.tfvars
    └── backend.tf
```

### Benefits of This Approach

1. Customization
- Customers can enable/disable features as needed
- Network architecture can be adjusted per requirements
- Security controls can be tailored to compliance needs

2. Maintainability
- Core modules remain stable
- Customer-specific configurations are isolated
- Easier to implement updates and patches

3. Scalability
- Support for different sized deployments
- Easy to add new features as modules
- Flexible node group configurations

4. Standardization
- Consistent base infrastructure
- Standardized security controls
- Reusable patterns across customers

5. Cost Optimization
- Customers only pay for enabled features
- Right-sized infrastructure based on profiles
- Efficient resource utilization

To implement this modular approach:

1. Create a migration plan for existing infrastructure
2. Develop and test new modules independently
3. Create documentation for each module and configuration option
4. Implement validation and compliance checks
5. Create example configurations for common use cases
6. Develop testing frameworks for different configurations

This modular approach would make the infrastructure more flexible and reusable while maintaining security and best practices across different customer deployments.
