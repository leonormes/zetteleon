---
aliases: []
confidence: 
created: 2025-01-03T12:49:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Phase 2 Infrastructure Deployment
type:
uid: 
updated: 
version:
---

## FitFile Platform Deployment Guide - Phase 2: Infrastructure Deployment

### Overview

This guide details the second phase of deploying the FitFile platform: setting up the infrastructure. We support deployment to both AWS and Azure, and I'll cover both paths in detail. The infrastructure deployment creates the foundational cloud resources needed to run the FitFile platform, including the Kubernetes cluster, networking components, and secure access mechanisms.

### Prerequisites

#### Access Requirements

1. AWS Deployment:
   - AWS Account with administrative access
   - AWS CLI installed and configured
   - Access to the AWS console
   - A service account with the terraform-policy role (full policy provided in documentation)

2. Azure Deployment:
   - Azure Subscription
   - Azure CLI installed and configured
   - Access to the Azure portal
   - Registered resource providers for:
     - Microsoft.ContainerService
     - Microsoft.ManagedIdentity
     - Microsoft.Network
     - Microsoft.Storage

#### Software Requirements

```bash
# Install required tools
# For AWS
brew install aws-cli  # On macOS
aws-cli-2.msi        # On Windows

# For Azure
brew install azure-cli  # On macOS
AzureCLI.msi          # On Windows

# Common requirements
brew install terraform
brew install git

# Verify installations
terraform version  # Should be >= 1.9.0
git version
aws --version     # If using AWS
az --version      # If using Azure
```

#### Initial Setup

```bash
# Create working directory
mkdir fitfile_deployment_phase2
cd fitfile_deployment_phase2

# Clone required repositories
git clone https://gitlab.com/fitfile/customers
```

### AWS Infrastructure Deployment

#### Step 1: Configure Terraform Cloud Workspace

1. Access Terraform Cloud:

```bash
   terraform login
```

2. Create a new project or select existing:
   - Navigate to: <https://app.terraform.io>
   - Select "Projects" in sidebar
   - Click "New Project" or select existing customer project
   - Name format: `<customer-name>-infrastructure`

3. Create workspace:
   - Click "New Workspace"
   - Select "Version Control Workflow"
   - Name: Use your deployment key from Phase 1
   - Connect to your GitLab repository

4. Configure variables:

```sh
   # Environment Variables (mark as sensitive except region)
   AWS_REGION = "eu-west-2"  # Or customer-specified region
   AWS_ACCESS_KEY_ID = "<from-aws-iam>"
   AWS_SECRET_ACCESS_KEY = "<from-aws-iam>"
   ```

#### Step 2: Prepare Infrastructure Code

1. Create new customer repository:

```bash
   cd customers
   mkdir <deployment-key>
   cd <deployment-key>
```

2. Initialize infrastructure files:

```bash
   # Create necessary files
   touch main.tf variables.tf outputs.tf versions.tf providers.tf
   
   # Create and populate .gitignore
   echo ".terraform/
   *.tfstate
   *.tfstate.*
   *.tfvars" > .gitignore
```

3. Configure versions.tf:

```hcl
   terraform {
     cloud {
       organization = "FITFILE-Platforms"
       workspaces {
         name = "<deployment-key>"
       }
     }
     required_version = ">= 1.9.0"
     required_providers {
       aws = {
         source = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
   }
```

4. Configure providers.tf:

```hcl
   provider "aws" {
     region = var.aws_region
     
     # Optional but recommended tags
     default_tags {
       tags = {
         Environment = var.environment
         Project     = var.deployment_key
         ManagedBy   = "terraform"
       }
     }
   }
   ```

5. Configure main.tf (using the private EKS template):

```hcl
   module "eks_cluster" {
     source = "app.terraform.io/FITFILE-Platforms/eks-private/aws"
     version = "1.0.0"  # Use latest version
     
     deployment_key = var.deployment_key
     environment    = var.environment
     
     # Networking configuration
     vpc_cidr = "10.0.0.0/16"  # Adjust based on customer requirements
     
     # Node pool configuration
     node_groups = {
       default = {
         desired_size = 2
         min_size     = 1
         max_size     = 3
         instance_types =
       }
       workloads = {
         desired_size = 2
         min_size     = 1
         max_size     = 5
         instance_types =
       }
     }
     
     # Security configuration
     enable_private_endpoints = true
     enable_private_nodes    = true
     
     # Monitoring configuration
     enable_cluster_logging = true
     cluster_log_types     =
   }
   ```

6. Configure variables.tf:

```hcl
   variable "deployment_key" {
     description = "Unique identifier for this deployment"
     type        = string
   }
   
   variable "environment" {
     description = "Deployment environment (prod, dev, etc)"
     type        = string
   }
   
   variable "aws_region" {
     description = "AWS region to deploy resources"
     type        = string
     default     = "eu-west-2"
   }
   
   # Add other necessary variables based on customer requirements
   ```

7. Configure outputs.tf:

```hcl
   output "cluster_endpoint" {
     description = "EKS cluster endpoint"
     value       = module.eks_cluster.cluster_endpoint
     sensitive   = true
   }
   
   output "cluster_name" {
     description = "EKS cluster name"
     value       = module.eks_cluster.cluster_name
   }
   
   output "generated_password" {
     description = "Generated password for jumpbox access"
     value       = module.eks_cluster.generated_password
     sensitive   = true
   }
   ```

#### Step 3: Deploy Infrastructure

1. Initialize Terraform:

```bash
   terraform init -upgrade
```

2. Validate configuration:

```bash
   terraform validate
```

3. Review planned changes:

```bash
   terraform plan
```

4. Apply changes:

```bash
   terraform apply
```

#### Step 4: Configure Jumpbox Access

1. Get the instance ID from AWS console or CLI:

```bash
   aws ec2 describe-instances \
     --filters "Name=tag:Name,Values=FITFILEJumpbox" \
     --query 'Reservations[*].Instances[*].[InstanceId]' \
     --output text
```

2. Start SSH session:

```bash
   aws ssm start-session \
     --target <instance-id> \
     --document-name AWS-StartPortForwardingSession \
     --parameters "localPortNumber=55679,portNumber=3389"
```

3. Configure RDP access:
   - Open your RDP client
   - Connect to: localhost:55679
   - Username: awsadmin
   - Password: (from terraform output generated_password)

4. Verify cluster access from jumpbox:

   ```bash
   # On the jumpbox
   cloud-init status --wait
   aws eks update-kubeconfig --region <region> --name <cluster-name>
   kubectl get pods -A
   ```

### Azure Infrastructure Deployment

TODO

### Security Considerations

1. Network Security:
   - All cluster endpoints are private by default
   - Jumpbox access is restricted to SSM Session Manager
   - VPC endpoints are used for AWS services
   - Security groups are tightly configured

2. Authentication & Authorization:
   - RBAC is enabled on the cluster
   - AWS IAM authentication is used for cluster access
   - Service accounts use IRSA (IAM Roles for Service Accounts)

3. Monitoring & Logging:
   - CloudWatch logging is enabled for cluster components
   - VPC Flow Logs are enabled
   - AWS CloudTrail is enabled for API activity logging

### Troubleshooting Guide

1. Common Issues:
   - Terraform initialization failures:

     ```bash
     # Clear terraform state
     rm -rf .terraform
     terraform init -upgrade
     ```

   - AWS provider authentication:

     ```bash
     # Verify AWS credentials
     aws sts get-caller-identity
     ```

2. Validation Steps:

   ```bash
   # Verify cluster health
   kubectl get nodes
   kubectl get pods -A
   
   # Check cluster logs
   aws eks describe-cluster --name <cluster-name>
   ```

### Next Steps

After successful infrastructure deployment:

1. Record all sensitive outputs in your secure password manager
2. Update relevant documentation with cluster details
3. Proceed to Phase 3: Platform Configuration

### Missing Information

I notice a few areas where more detail might be helpful:

1. Specific node size requirements for different workload types
2. Backup and disaster recovery configurations
3. Detailed network security group rules
4. Custom AMI requirements if any
