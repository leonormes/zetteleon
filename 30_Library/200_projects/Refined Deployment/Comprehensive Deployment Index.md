---
aliases: []
confidence: 
created: 2025-09-04T08:33:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-16T09:36:58Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Comprehensive Deployment Index
type: index
uid: 
updated: 
version:
---

This index provides organized access to all deployment-related documentation, covering infrastructure, platform components, security, networking, and operational procedures.

## 🏗️ Infrastructure & Cloud Platforms

### Azure Infrastructure

- **[[AWS resources associated with the hie sde VPC]]** - Detailed AWS VPC resource inventory and configuration
- **[[TFC Service Principle for Azure]]** - Terraform Cloud service principal setup for Azure deployments
- **[[Errors Encountered During Azure Deployment]]** - Common Azure deployment issues and troubleshooting

### AWS Infrastructure

- **[[Cloud Network]]** - Cloud networking architecture and design

## 🔧 Deployment Tools & Configuration

### Terraform & Infrastructure as Code

- **[[Create a Central Version Catalog Module]]** - Centralized version management for Terraform modules
- **[[terraform-helm-fitfile-platform]]** - Terraform configuration for FITFILE platform deployment

### CI/CD & Pipelines

- **[[SoT - FITFILE CI/CD Pipelines]]** - Comprehensive GitLab CI/CD pipeline documentation
- **[[Staging Pipeline Documentation for Deployment repo]]** - Specific documentation for staging environment pipelines

### Helm Charts & Application Management

- **[[Helm Chart Management Tool]]** - Requirements and design for Helm chart lifecycle management
- **[[refactoring_suggestions]]** - Helm chart refactoring recommendations
- **[[ArgoCD App of Apps Architecture]]** - GitOps application management with ArgoCD
- **[[FFNODE as Umbrella Chart]]** - Umbrella chart pattern for application deployment

## 🔐 Security & Secrets Management

### Vault & PKI

- **[[Vault PKI Infrastructure Documentation]]** - Public Key Infrastructure setup in HashiCorp Vault
- **[[Vault to Kubernetes Secrets Management Guide]]** - Integration between Vault and Kubernetes secrets

### Kubernetes Security

- **[[Kubernetes Secrets in Helm Chart Deployment]]** - Secret management patterns in Helm deployments
- **[[Why HTTPS is not good enough]]** - Advanced security considerations beyond HTTPS

## 🌐 Networking & Connectivity

### Network Configuration

- **[[Network Policies]]** - Kubernetes network policy configuration
- **[[Nginx Ingress Controller Configuration]]** - Ingress controller setup and configuration
- **[[Proxy Allow list]]** - Network proxy and firewall configuration

### DNS & Service Mesh

- **[[MESH service firewall allowlist requirements]]** - Service mesh API configuration and usage

## 📋 FITFILE Platform Specifics

### Platform Components

- **[[SoT - FITFILE Deployment Process]]** - End-to-end deployment narrative and process map
- **[[FITFILE Platform Components]]** - Overview of FITFILE platform architecture
- **[[FITFILE Deployment Docs]]** - Comprehensive FITFILE deployment documentation
- **[[Fitfile deployment fixes]]** - Common deployment issues and solutions

### Database & Storage

- **[[Mongo Helm Config]]** - MongoDB Helm chart configuration

## 📚 Standards & Documentation

### Naming & Conventions

- **[[resource naming convention]]** - Resource naming standards and guidelines

### Prerequisites & Setup

- **[[Prerequisities]]** - Technical prerequisites for deployment
- **[[Deployment Configuration Guide]]** - Step-by-step deployment configuration

## 🏥 Customer-Specific Documentation

### MKUH (Maidstone and Tunbridge Wells NHS Trust)

## 🔧 Repository & Code Organization

### GitLab Structure

- **[[repo_structure_suggestions]]** - Comprehensive GitLab repository refactoring proposals

## 🐛 Troubleshooting & Issues

### Common Problems

- **[[Why Node Not Work]]** - Node.js application troubleshooting
- **[[Errors Encountered During Azure Deployment]]** - Azure-specific deployment issues
- **[[Fitfile deployment fixes]]** - Platform-specific deployment fixes

---

## Core Process SoTs (Start Here)

These notes provide the high-level narrative and architecture of the deployment system.

1.  **[[SoT - FITFILE Deployment Process]]** - **The Master Map.** The end-to-end flow from commit to cloud.
2.  **[[SoT - FITFILE CI/CD Pipelines]]** - **The Engine.** Detailed documentation of the GitLab CI/CD pipelines.
3.  **[[SoT - FITFILE Secret Management Architecture]]** - **The Keys.** How Vault and VSO secure the platform.
4.  **[[SoT - FITFILE Platform Deployment]]** - Platform-specific deployment details.

---

## 🏗️ Infrastructure & Cloud Platforms
