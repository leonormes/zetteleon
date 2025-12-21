---
aliases: []
confidence:
created: 2025-09-04T08:33:44Z
epistemic:
last_reviewed:
modified: 2025-12-20T20:28:12Z
purpose: To provide an organized index of all deployment-related documentation.
review_interval:
see_also: []
source_of_truth: []
status:
tags: [deployment]
title: Comprehensive Deployment Index
type: index
uid:
updated: 2025-12-20T11:30:00Z
version:
---

This index provides organized access to all deployment-related documentation, covering infrastructure, platform components, security, networking, and operational procedures.

## 🏗️ Infrastructure & Cloud Platforms

### Azure Infrastructure

- **[[TFC Service Principle for Azure]]** - Terraform Cloud service principal setup for Azure deployments.
- **[[Errors Encountered During Azure Deployment]]** - Common Azure deployment issues and troubleshooting.

### AWS Infrastructure

- **[[Data Architecture Analysis of Terraform AWS]]** - Deep dive into the data architecture of the Terraform AWS infrastructure code.
- **[[Cloud Network]]** - Cloud networking architecture and design.

## 🔧 Deployment Tools & Configuration

### Terraform & Infrastructure as Code

- **[[Data Architecture Analysis of Terraform AWS]]** - Analysis of `config.tf` and `main.tf` for the AWS Terraform setup.
- **[[terraform helm fitfile platform]]** - Details on refactoring the Terraform module to extract hardcoded values.
- **[[Create a Central Version Catalog Module]]** - Centralized version management for Terraform modules.

### CI/CD & Pipelines

- **[[SOT - CI-CD Pipelines]]** - Comprehensive GitLab CI/CD pipeline documentation.
- **[[Staging Pipeline Documentation for Deployment repo]]** - Specific documentation for staging environment pipelines.

### Helm Charts & Application Management

- **[[helm_charts_deployment]]** - Data architecture and domain-driven analysis of the Helm chart deployment.
- **[[Simplify the helm charts]]** - Proposal for reorganizing Helm chart repositories to separate code and configuration.
- **[[Helm Chart Management Tool]]** - Requirements and design for Helm chart lifecycle management.
- **[[refactoring_suggestions]]** - Helm chart refactoring recommendations.
- **[[ArgoCD App of Apps Architecture]]** - GitOps application management with ArgoCD.
- **[[FFNODE as Umbrella Chart]]** - Umbrella chart pattern for application deployment.

## 🔐 Security & Secrets Management

### Vault & PKI

- **[[Vault PKI Infrastructure Documentation]]** - Public Key Infrastructure setup in HashiCorp Vault.
- **[[Vault to Kubernetes Secrets Management Guide]]** - Integration between Vault and Kubernetes secrets.

### Kubernetes Security

- **[[Kubernetes Secrets in Helm Chart Deployment]]** - Secret management patterns in Helm deployments.
- **[[Why HTTPS is not good enough]]** - Advanced security considerations beyond HTTPS.

## 🌐 Networking & Connectivity

### Network Configuration

- **[[Network Policies]]** - Kubernetes network policy configuration.
- **[[Nginx Ingress Controller Configuration]]** - Ingress controller setup and configuration.
- **[[Proxy Allow list]]** - Network proxy and firewall configuration.
- **[[Key Features of AWS-Managed Prefix Lists]]** - Guide to using AWS-managed prefix lists for simplified security group and route table management.

### DNS & Service Mesh

- **[[MESH service firewall allowlist requirements]]** - Service mesh API configuration and usage.

### IP Management
- **[[IP allocation on Azure public deployment PROD]]** - Explanation of IP allocation in AKS clusters (Node, Pod, and Service IPs).
- **[[IPs needed for FITFILE]]** - Guide for planning VPC CIDR ranges for EKS deployments.
- **[[Minimizing IP Addresses for EKS Node Groups]]** - How to analyze and minimize IP address utilization for EKS node groups.
- **[[Minimum IP Requirements for a Firewall Subnet]]** - IP address requirements for a firewall subnet.
- **[[QU - What is the difference between AWS and Azure IP management on K8s clusters]]** - A question about the differences in IP management between AWS and Azure for Kubernetes.

## 📋 FITFILE Platform Specifics

### Platform Components

- **[[SoT - FITFILE Deployment Process]]** - End-to-end deployment narrative and process map.
- **[[FITFILE Platform Components]]** - Overview of FITFILE platform architecture.
- **[[FITFILE Deployment Docs]]** - Comprehensive FITFILE deployment documentation.
- **[[Fitfile deployment fixes]]** - Common deployment issues and solutions.

### Customer Management
- **[[Customer_management]]** - Describes the multi-tenant architecture using ArgoCD ApplicationSets.

### Database & Storage

- **[[Mongo Helm Config]]** - MongoDB Helm chart configuration.

## 📚 Standards & Documentation

### Naming & Conventions

- **[[Resource Naming Convention]]** - Resource naming standards and guidelines.

### Prerequisites & Setup

- **[[Prerequisities]]** - Technical prerequisites for deployment.
- **[[Deployment Configuration Guide]]** - Step-by-step deployment configuration.
- **[[set_up_new_deployment]]** - Guide and developer log for setting up a new deployment.

## 🔧 Repository & Code Organization

### GitLab Structure

- **[[Repository Structure Refactoring for Clarity]]** - Comprehensive GitLab repository refactoring proposals.
- **[[Simplify the helm charts]]** - Proposal for separating Helm chart code from customer configuration data.

## 🐛 Troubleshooting & Issues

### Common Problems

- **[[from the linux jumpbox inside the vpc how do I deb]]** - Debugging guide for internet connectivity issues from a Linux jumpbox in an AWS VPC.
- **[[Why Node Not Work]]** - Node.js application troubleshooting.
- **[[Errors Encountered During Azure Deployment]]** - Azure-specific deployment issues.
- **[[Fitfile deployment fixes]]** - Platform-specific deployment fixes.

---

## Core Process SoTs (Start Here)

These notes provide the high-level narrative and architecture of the deployment system.

1. **[[SoT - FITFILE Deployment Process]]** - **The Master Map.** The end-to-end flow from commit to cloud.
2. **[[SOT - CI-CD Pipelines]]** - **The Engine.** Detailed documentation of the GitLab CI/CD pipelines.
3. **[[SoT - FITFILE Secret Management Architecture]]** - **The Keys.** How Vault and VSO secure the platform.
4. **[[SoT - FITFILE Platform Deployment]]** - Platform-specific deployment details.
