---
aliases: []
confidence: ""
created: 2025-01-06T13:59:42Z
depends_on: ["name: \"AWS authentication"]
deployment_phase: "1"
description: "Service principal credentials and roles"
doc_link: "[aws_service_principal](aws_service_principal.md)"
epistemic: ""
estimated_duration: "30m"
iac_path: ["repo: \"terraform-aws-eks-private"]
last_reviewed: ""
main_file: "tfe_projects.tf"
modified: 2025-12-27T20:41:05+00:00
name: "iam"
next_steps: ""
path: "Production/central-services/hcp/tfc"
phase: "1"
phase_order: ""
purpose: ""
reason: "Required for AWS authentication"
required_configurations: ""
required_resources: ["type: \"aws_service"]
review_interval: ""
see_also: []
source_of_truth: []
status: ""
step: "3"
tags: []
title: terraform_cloud_projects
type: "tooling"
uid: 
updated: 
verification_steps: ""
version: ""
---

## Terraform Cloud Projects

This document describes the setup and configuration of Terraform Cloud Projects required for infrastructure deployment.

### Prerequisites

Before setting up TFC Projects:

1. AWS service principal with required permissions
2. Terraform Cloud account with organization admin access
3. GitLab access with repository creation permissions
4. AWS credentials configured in variable sets

### Project Structure

The following projects need to be created:

1. Core Infrastructure
   - Purpose: Base networking and security components
   - Workspaces: VPC, Security Groups, VPC Endpoints
   - Variable sets:
     - AWS credentials (from service principal)
     - Environment variables
     - Region configuration

2. Platform Services
   - Purpose: EKS cluster and supporting services
   - Workspaces: EKS, Container Registry, KMS
   - Variable sets:
     - AWS credentials (from service principal)
     - Cluster configuration
     - Network references

3. Platform Applications
   - Purpose: Application layer services
   - Workspaces: ArgoCD, Vault, Monitoring
   - Variable sets:
     - AWS credentials (from service principal)
     - Application configuration
     - Service endpoints

### Configuration Steps

1. Organization Setup

```hcl
resource "tfe_organization" "org" {
 name  = "FITFILE-Platforms"
 email = "platform@fitfile.com"
}
```

2. AWS Variable Set

```hcl
resource "tfe_variable_set" "aws_auth" {
 name         = "AWS-Authentication"
 description  = "AWS authentication for all workspaces"
 organization = tfe_organization.org.name
}

resource "tfe_variable" "aws_access_key" {
 key          = "AWS_ACCESS_KEY_ID"
 value        = var.aws_access_key_id
 category     = "env"
 variable_set_id = tfe_variable_set.aws_auth.id
 sensitive    = true
}

resource "tfe_variable" "aws_secret_key" {
 key          = "AWS_SECRET_ACCESS_KEY"
 value        = var.aws_secret_access_key
 category     = "env"
 variable_set_id = tfe_variable_set.aws_auth.id
 sensitive    = true
}
```

3. Project Creation

```hcl
resource "tfe_project" "infrastructure" {
 organization = tfe_organization.org.name
 name         = "Core-Infrastructure"
}

resource "tfe_project" "platform" {
 organization = tfe_organization.org.name
 name         = "Platform-Services"
}

resource "tfe_project" "applications" {
 organization = tfe_organization.org.name
 name         = "Platform-Applications"
}
```

### Verification Process

1. AWS Authentication
   - Test AWS credentials in variable sets
   - Verify role assumption works
   - Test AWS provider in a workspace

2. Project Setup
   - Confirm project creation
   - Test workspace creation
   - Validate variable set application

3. VCS Integration
   - Test GitLab connection
   - Verify webhook functionality
   - Check repository access

### Next Steps

After TFC Projects setup:

1. Create initial workspaces for Core Infrastructure
2. Apply AWS provider configurations
3. Begin infrastructure deployment
