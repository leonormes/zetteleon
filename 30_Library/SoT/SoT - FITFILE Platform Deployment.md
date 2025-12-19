---
aliases: [FITFILE Deployment SoT, FITFILE Platform Architecture]
confidence: 5/5
created: 2025-12-14T20:00:00Z
epistemic: theory
last_reviewed: 2025-12-14
modified: 2025-12-19T10:12:36Z
purpose: To provide the canonical reference for the FITFILE Platform deployment, architecture, security, and operational procedures.
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: [architecture, aws, azure, deployment, fitfile, kubernetes, security]
title: SoT - FITFILE Platform Deployment
type: SoT
uid: 2025-12-14-FITFILE-DEPLOY
updated: 
version: 1
---

## 1. Definitive Statement

> [!definition] Definition
> The **FITFILE Platform** is a secure, cloud-agnostic data processing system designed for healthcare environments. Its deployment architecture utilizes **Infrastructure as Code (Terraform)**, **GitOps (ArgoCD)**, and **Helm Charts** to ensure reproducible, scalable, and compliant infrastructure across Azure and AWS.

---

## 2. Infrastructure & Cloud Platforms

The platform supports a multi-cloud strategy, primarily focused on Azure and AWS.

### 2.1 Azure Infrastructure

- **Core Tooling:** [[Azure Tooling Configuration Guide]] provides the overview of Azure infrastructure configuration.

- **Identity Management:** Uses [[TFC Service Principle for Azure]] for Terraform Cloud deployments.

- **Customer Onboarding:** Follows the [[Azure Customer Checklist]].

- **Troubleshooting:** Common issues are documented in [[Errors Encountered During Azure Deployment]].

### 2.2 AWS Infrastructure

- **Networking:** Based on a [[SoT - Cloud Networking Core Components|Cloud Network]] design, utilizing a [[SoT - Cloud Networking Core Components|Hub-and-Spoke Architecture]] for centralized management.

- **VPC Resources:** Detailed in [[AWS resources associated with the hie sde VPC]].

---

## 3. Deployment Strategy (GitOps & IaC)

Deployment is managed via a strict GitOps workflow.

### 3.1 Infrastructure as Code (Terraform)

- **Configuration:** Managed via [[terraform-helm-fitfile-platform]].

- **Module Management:** Uses a [[Create a Central Version Catalog Module]] for dependency standardization.

### 3.2 Application Management (Helm & ArgoCD)

- **GitOps Controller:** [[ArgoCD App of Apps Architecture]] manages the application lifecycle.

- **Chart Architecture:** Utilizes [[FFNODE as Umbrella Chart]] pattern for aggregating services.

- **Lifecycle Management:** Governed by the [[Helm Chart Management Tool]] design.

---

## 4. Security & Secrets Management

Security is a first-class citizen, leveraging Vault for dynamic secrets and PKI.

### 4.1 Vault & PKI

- **Infrastructure:** [[Vault PKI Infrastructure Documentation]] details the Public Key Infrastructure setup.

- **Integration:** [[Vault to Kubernetes Secrets Management Guide]] explains how secrets are injected into pods.

- **Troubleshooting:** See [[Errors Encountered During Azure Deployment|VaultClientConfigError]] for client configuration issues.

### 4.2 Network Security

- **Encryption:** Moves beyond basic HTTPS to advanced patterns ([[Why HTTPS is not good enough]]).

- **Access Control:** strict [[Calico Cloud vs Kubernetes Network Policies in GitOps|Network Policies]] and [[Proxy Allow list]] configuration.

---

## 5. Platform Components & Data Flow

### 5.1 Architecture

- **Overview:** [[FITFILE Platform Components]] defines the core services.

- **Data Pipeline:** [[FITFILE Platform Components|FITFILE Patient Data Transformation]] details the processing logic.

### 5.2 Storage

- **Database:** MongoDB configured via [[Mongo Helm Config]].

- **Object Storage:** MinIO managed via standard image import processes.

### 5.3 Connectivity

- **Ingress:** Managed by [[Nginx Ingress Controller Configuration]].

- **DNS:** Architecture defined in [[Core DNS Components and Environments]].

---

## 6. Standards & Operations

### 6.1 Naming Conventions

- Resources must adhere to [[Cloud Resource Naming Convention - FITFILE - Confluence|Platform Naming Conventions]] and [[Resource Naming Convention]].

### 6.2 Prerequisites

- Deployments require meeting the [[Prerequisities]] and following the [[Deployment Configuration Guide]].

---

## 7. Related Components

- [[repo_structure_suggestions]] - Repository organization.
- [[Fitfile deployment fixes]] - Operational fixes.
- [[FITFILE Node Deployment Guide]] - Comprehensive guide for deploying FITFILE nodes.
- [[Phase 2 Infrastructure Deployment]] - Detailed infrastructure setup for AWS and Azure.
- [[FITFILE Deployment Docs]] - High-level deployment dependency graph and process.
- [[Azure Deployment Readiness Checklist]] - Readiness checklist.
- [[Kubernetes Backup and Disaster Recovery for AWS and Azure]] - Backup strategies.
