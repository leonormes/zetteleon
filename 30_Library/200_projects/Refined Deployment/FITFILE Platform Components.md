---
aliases: []
confidence: 
created: 2025-08-22T11:32:55Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, components, config, helm, platform]
title: FITFILE Platform Components
type:
uid: 
updated: 
version:
---

## **Core Platform Components**

### **1. Nginx Ingress Controller**

**Location**: `TFC-Modules/terraform-helm-fitfile-platform/ingress_nginx/main.tf`
**Configuration**: Deployed via Terraform module from jumpbox
**Description**: Provides HTTP/HTTPS load balancing and SSL termination for all services. Configured with internal load balancer type for private clusters. Uses static IP assignment and supports both Azure and AWS deployments.

### **2. HashiCorp Vault Secrets Operator (VSO)**

**Location**: `TFC-Modules/terraform-helm-fitfile-platform/vault_operator/main.tf`
**Configuration**: Connects to HCP Vault using AppRole authentication
**Description**: Automatically syncs secrets from Vault to Kubernetes secrets. Manages ACR credentials, PKI certificates, and application secrets. Uses VaultAuth and VaultDynamicSecret CRDs for declarative secret management.

### **3. ArgoCD (GitOps)**

**Location**: `TFC-Modules/terraform-helm-fitfile-platform/argocd/main.tf`
**Configuration**: Deployed with SSO integration and custom applications
**Description**: Manages continuous deployment of applications from Git repositories. Monitors helm chart deployment repo and automatically syncs changes to clusters. Configured with deployment-specific applications and SSL certificates.

### **4. Reflector**

**Location**: `TFC-Modules/terraform-helm-fitfile-platform/reflector/main.tf`
**Configuration**: Deployed to replicate secrets across namespaces
**Description**: Automatically copies secrets and configmaps between Kubernetes namespaces based on annotations. Essential for distributing image pull secrets and certificates to all required namespaces.

### **5. PKI Certificate Management**

**Location**: [central-services/hcp/vault/secret_engines.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/secret_engines.tf:0:0-0:0) + `private_platform_template/vault_operator/`
**Configuration**: Vault PKI with per-deployment intermediate CAs
**Description**: Automated certificate issuance using Vault PKI. Each deployment gets its own intermediate CA for issuing certificates. VSO automatically requests and renews certificates for ingress controllers.

## **Deployment Architecture**

### **Stage 1: Infrastructure (Terraform Cloud)**

- AKS clusters, networking, Azure resources
- Runs with public internet access

### **Stage 2: Platform (Jumpbox)**

- Kubernetes platform components
- Uses [terraform-helm-fitfile-platform](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform:0:0-0:0) module v1.0.29
- Requires private cluster access

## **Configuration Flow**

1. **Infrastructure**: Creates AKS cluster and networking
2. **Platform Module**: Deploys core services (nginx, VSO, ArgoCD, Reflector)
3. **Vault Integration**: VSO connects to HCP Vault for secret management
4. **Application Deployment**: ArgoCD syncs applications from helm chart repo
5. **Certificate Management**: PKI certificates automatically issued and renewed

## **Key Repositories**

- **[TFC-Modules/terraform-helm-fitfile-platform](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform:0:0-0:0)**: Reusable platform module
- **[private_platform_template](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template:0:0-0:0)**: Deployment-specific configuration
- **[central-services/hcp/vault](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault:0:0-0:0)**: Vault PKI and policy configuration
- **`helm_chart_deployment`**: Application definitions and values

## **Secret Management**

All secrets flow through Vault → VSO → Kubernetes:

- **ACR credentials**: For private container registry access
- **PKI certificates**: For TLS termination
- **Application secrets**: Database connections, API keys, etc.
- **AppRole credentials**: For Vault authentication
