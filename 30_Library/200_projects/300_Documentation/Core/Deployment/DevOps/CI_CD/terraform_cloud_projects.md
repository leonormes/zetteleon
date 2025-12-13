---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
depends_on:
  - name: deployment_phases
    type: documentation
    reason: "Defines the overall deployment structure"
    doc_link: "[deployment_phases](deployment_phases.md)"
  - name: aws_service_principal
    type: tooling
    reason: "Required for AWS authentication and permissions"
    doc_link: "[aws_service_principal](aws_service_principal.md)"
deployment_phase: 1  # Part of Foundation & Tooling phase
description: "Terraform Cloud Projects configuration for infrastructure deployment"
epistemic: 
estimated_duration: "30m"
iac_path:
  - repo: terraform-aws-eks-private
    path: Production/central-services/hcp/tfc
    main_file: tfe_projects.tf
last_reviewed: 
modified: 2025-12-13T11:39:52Z
name: terraform_cloud_projects
phase_order:
  phase: 1
  step: 3  # After AWS service principal setup
  next_steps:
    - vpc_networking_for_private_eks
purpose: 
required_configurations:
  - name: Organization settings
    description: "Terraform Cloud organization configuration"
  - name: VCS provider
    description: "GitLab VCS provider setup"
  - name: Variable sets
    description: "AWS credentials and shared variables"
  - name: AWS authentication
    description: "Service principal credentials and roles"
required_resources:
  - type: external_service
    name: terraform_cloud
    reason: "Required for infrastructure state management and deployment"
  - type: external_service
    name: gitlab
    reason: "Required for VCS integration"
  - type: aws_service
    name: iam
    reason: "Required for AWS authentication"
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: terraform_cloud_projects
type: tooling
uid: 
updated: 
verification_steps:
version:
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
