---
aliases: []
confidence: 
created: 2025-09-22T14:56:19Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/mkuh]
title: MKUH-ONBOARDING-GUIDE
type:
uid: 
updated: 
version:
---

## MKUH Customer Onboarding Guide

**Milton Keynes University Hospital - East of England SDE Node**

> **Customer**: Milton Keynes University Hospital (MKUH)
> **Type**: NHS Trust - Data Provider
> **Hub**: East of England (EOE)
> **Target Go-Live**: October 2025
> **Meeting Reference**: 4th September 2025

### 🏥 **Customer Overview**

**Milton Keynes University Hospital** is joining the FITFILE platform as a data provider under the East of England Secure Data Environment (EOE SDE). They will be providing healthcare data for research through the HDR UK National Data Portal.

#### **Key Requirements from Meeting Notes**

- DPIA approved, funding secured ✅
- Azure subscription provided by MKUH ✅
- Monthly data updates using NHS Number as unique identifier
- National Data Opt-Out (NDOO) filtering via MESH API
- VNet peering to existing SQL VM
- TLS 1.2 connection to MKUH database
- Target: Synthetic data flowing by early October 2025

---

### 🚀 **Automated Customer Onboarding Process**

Using our umbrella module, the onboarding process creates resources across all central services:

#### **Step 1: Resources Created Automatically**

When you run:

```bash
terraform apply -var="customer_name=mkuh" -var="hub_customer=eoe"
```

The following resources are automatically provisioned:

##### **🔧 GitLab (Repository Management)**

```sh
✅ Repository: mkuh-prod
   └── Location: fitfile/customers/eoe/mkuh-prod
   └── Purpose: Infrastructure code for MKUH node deployment
   └── Features: Push rules, merge request templates, CI/CD integration
```

##### **☁️ Terraform Cloud (Infrastructure Management)**

```sh
✅ Workspace: mkuh-prod-workspace
   └── Project: central-services
   └── Purpose: Terraform execution environment for MKUH infrastructure
   └── Features: Auto-apply disabled, VCS integration, team access
   └── Variables: customer_name=mkuh, hub_customer=eoe, environment=production
```

##### **🔐 Auth0 (Authentication)**

```sh
✅ Client: mkuh-production-client
   └── Domain: fitfile-prod.eu.auth0.com
   └── Purpose: MKUH staff authentication to FITFILE platform
   └── Callback URLs: https://mkuh.production.fitfile.com/auth/callback
   └── Integration: Azure AD (via MS365)
```

##### **📊 Grafana (Monitoring)**

```sh
✅ Dashboard: MKUH - Production Dashboard
   └── Stack: fitfile-production-stack
   └── Purpose: Monitor MKUH node health and performance
   └── Features: Service health panels, request rate monitoring, alerts
   └── Folder: mkuh-production (organized monitoring)
```

##### **☁️ Azure (Infrastructure Integration)**

```sh
✅ AD Group: mkuh-production-users
   └── Purpose: MKUH user access management
   └── Members: MKUH staff who need platform access

✅ Resource Group: rg-mkuh-production
   └── Location: West Europe (or MKUH preference)
   └── Purpose: Container for MKUH-specific Azure resources

✅ Service Principal: mkuh-production-acr-access
   └── Purpose: Container registry access for MKUH node
   └── Permissions: AcrPull role assigned
```

##### **🌐 Cloudflare (DNS Management)**

```sh
✅ DNS Records:
   └── mkuh.fitfile.net → MKUH node endpoint
   └── mkuh-argocd.fitfile.net → MKUH ArgoCD interface
   └── mkuh-argo-workflows.fitfile.net → MKUH Workflows interface
   └── mkuh-auth.fitfile.net → MKUH authentication subdomain
```

##### **🔐 Vault (Secrets Management)**

```sh
✅ Namespace: mkuh-production
   └── Purpose: Isolated secrets storage for MKUH

✅ KV Store: kv/mkuh/*
   └── Purpose: MKUH-specific secrets (DB credentials, API keys)

✅ Policy: mkuh-production-policy
   └── Purpose: Secure access control for MKUH secrets

✅ AppRole: mkuh-production-role
   └── Purpose: Automated authentication for MKUH deployments
```

---

### 🛠️ **Step-by-Step Onboarding Process**

#### **Phase 1: Infrastructure Preparation**

##### **1.1 MKUH Prerequisites (From Meeting Action Items)**

- [ ] **MKUH (OC)**: Create Azure subscription for FITFILE
- [ ] **MKUH (OC)**: Grant contributor roles and create service principal
- [ ] **MKUH (OC)**: Provide specific IP address for API connection (NSG rules)
- [ ] **MKUH (OC)**: Confirm default route for outbound traffic
- [ ] **MKUH (CW)**: Provide data structure for ETL process
- [ ] **MKUH (CW)**: Provide unique list of drug and dose combinations

##### **1.2 FITFILE Prerequisites**

- [ ] **Complete**: Set up TFC workspace variables with MKUH Azure credentials
- [ ] **Complete**: Configure Vault with MKUH database connection secrets
- [ ] **Complete**: Set up Grafana monitoring for MKUH endpoints

#### **Phase 2: Execute Customer Onboarding**

##### **2.1 Planning Phase**

```bash
# Navigate to central services
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/central-services

# Preview what will be created for MKUH
terraform plan -var="customer_name=mkuh" -var="hub_customer=eoe"
```

##### **2.2 Execution Phase**

```bash
# Create all MKUH resources across all services
terraform apply -var="customer_name=mkuh" -var="hub_customer=eoe"
```

##### **2.3 Verification Phase**

```bash
# Verify customer resources were created
terraform output customer_resources

# Check service integrations
terraform output service_integrations
```

#### **Phase 3: Service-Specific Configuration**

##### **3.1 GitLab Repository Setup**

1. **Repository created**: `mkuh-prod` in `fitfile/customers/eoe/`
2. **Access configured**: MKUH team members added to EOE group
3. **CI/CD pipeline**: Automatically configured for MKUH node deployment
4. **Integration**: Linked to TFC workspace for infrastructure deployment

##### **3.2 Terraform Cloud Workspace**

1. **Workspace created**: `mkuh-prod-workspace`
2. **Variables configured**: Customer-specific settings injected
3. **VCS integration**: Linked to MKUH GitLab repository
4. **Team access**: Infrastructure team permissions assigned

##### **3.3 Auth0 Authentication**

1. **Client created**: MKUH-specific authentication client
2. **Azure integration**: Connected to MKUH's Azure AD tenant
3. **Callback URLs**: Configured for MKUH subdomain
4. **Users**: MKUH staff can authenticate via existing MS365 accounts

##### **3.4 Grafana Monitoring**

1. **Stack created**: MKUH-specific monitoring stack
2. **Dashboard configured**: Service health and performance monitoring
3. **Alerts**: Automated notifications for MKUH node issues
4. **Data sources**: Connected to MKUH infrastructure metrics

##### **3.5 Azure Integration**

1. **AD group**: MKUH user access management
2. **Service principals**: Secure access to shared resources (ACR)
3. **Resource group**: Container for MKUH-specific resources
4. **Permissions**: Least-privilege access model

##### **3.6 DNS Management**

1. **Primary domain**: `mkuh.fitfile.net` → MKUH node
2. **Management interfaces**: ArgoCD, Argo Workflows subdomains
3. **Authentication**: Dedicated auth subdomain
4. **SSL certificates**: Wildcard certificate support

##### **3.7 Vault Secrets Management**

1. **Isolated namespace**: Secure MKUH-specific secrets storage
2. **Database credentials**: Secure storage for MKUH SQL connection
3. **API keys**: Management of MKUH-specific integration keys
4. **Automated access**: AppRole authentication for deployments

---

### 📋 **Post-Onboarding Checklist**

#### **Immediate Actions**

- [ ] **Verify DNS resolution**: `mkuh.fitfile.net` resolves correctly
- [ ] **Test authentication**: MKUH users can log in via Auth0
- [ ] **Check monitoring**: Grafana dashboard shows MKUH node metrics
- [ ] **Validate repository**: GitLab repository accessible to MKUH team
- [ ] **Confirm TFC workspace**: Infrastructure deployments working

#### **MKUH-Specific Setup**

- [ ] **Database connection**: Configure secure connection to MKUH SQL VM
- [ ] **Network peering**: Set up VNet peering to existing MKUH infrastructure
- [ ] **Firewall rules**: Configure NSG rules for API connectivity
- [ ] **Certificate management**: Install wildcard certificate for MKUH domains
- [ ] **Change management**: Submit CAB request for infrastructure changes

#### **Data Flow Preparation**

- [ ] **ETL scripts**: Deploy scripts provided by The Hyve to MKUH GitLab
- [ ] **Data mapping**: Configure medication/drug data mappings
- [ ] **NDOO integration**: Set up National Data Opt-Out filtering
- [ ] **Synthetic data**: Configure synthetic data pipeline for testing
- [ ] **OMOP CDM**: Prepare for OMOP training (delayed until late October)

---

### 🎯 **Expected Outcomes**

After successful onboarding, MKUH will have:

#### **✅ Complete Infrastructure**

- Dedicated GitLab repository for infrastructure code
- TFC workspace for automated deployments
- Monitoring dashboard for node health
- DNS entries for all MKUH services
- Secure secrets management

#### **✅ Authentication & Access**

- MKUH staff can log in using existing MS365 accounts
- Role-based access to FITFILE platform
- Integration with MKUH's existing MFA system

#### **✅ Security & Compliance**

- Isolated secrets storage in Vault
- Secure service-to-service communication
- Compliance with NHS data protection requirements
- Integration with MKUH's change management process

#### **✅ Data Pipeline Ready**

- Infrastructure ready for synthetic data (early October)
- Database connection configured and secured
- ETL processes ready for deployment
- NDOO filtering capabilities in place

---

### 📞 **Next Steps & Contacts**

#### **FITFILE Team Actions**

1. **Leon Ormes (LO)**: Execute customer onboarding automation
2. **Oliver Roberts (OR)**: Configure Azure networking and certificates
3. **Will Jones (WJ)**: Set up NDOO filtering process
4. **Sophie Thompson (ST)**: Schedule platform showcase session

#### **MKUH Team Actions**

1. **Owen Cooper (OC)**: Azure subscription setup and networking
2. **Chris Wilson (CW)**: Data structure and ETL preparation
3. **MKUH IT Team**: Change management and security approval

#### **Timeline Coordination**

- **Week 1-2**: Infrastructure setup and automation
- **Week 3-4**: Network integration and testing
- **October**: Synthetic data flow testing
- **Late October**: OMOP training and go-live preparation

---

This automated onboarding process significantly reduces the manual effort required to set up new customers while ensuring consistency, security, and proper integration across all FITFILE central services. The umbrella module handles the complexity of coordinating multiple services while maintaining the flexibility for customer-specific requirements like MKUH's Azure subscription and NHS compliance needs.
