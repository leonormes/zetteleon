---
aliases: []
confidence: 
created: 2025-09-23T08:50:43Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: EOE DNS Hostname Analysis Report
type:
uid: 
updated: 
version:
---

## **1. Infrastructure Level (AWS EKS - hie-sde-v2)**

### **Primary Domain: `codisc-eoe-sde.uk`**

- **Hosted Zone ID**: `Z02437052IKW0ICQZ07XA`
- **Certificate**: ACM certificate with wildcard support (`*.codisc-eoe-sde.uk`)
- **DNS Records**:
  - `argocd.codisc-eoe-sde.uk` → EKS ALB (ArgoCD access)
  - `app.codisc-eoe-sde.uk` → EKS ALB (Application access)
  - `relay.codisc-eoe-sde.uk` → Public ALB (Hutch/Bunny relay service)

### **Relay Service (M2M Communication)**

- **Public Domain**: `relay.codisc-eoe-sde.uk`
- **Purpose**: Hutch/Bunny communication between SDE and CUH nodes
- **Infrastructure**: Dedicated public ALB with HTTPS listener
- **Target**: All EKS worker nodes on port 32080

## **2. Application Level (Helm Deployments)**

### **EOE SDE Main Deployment (`ff-eoe-sde`)**

- **Primary Host**: `app.ff-eoe-sde.privatelink.fitfile.net`
- **Auth0**: `fitfile-test.eu.auth0.com`
- **FitConnect Integrations**:
  - NHS Provider 1: `https://nhs-provider-1.fitfile.net/fitconnect`
  - NHS Provider 2: `https://nhs-provider-2.fitfile.net/fitconnect`

### **HIE Production (`hie-prod-34`)**

- **Primary Host**: `app.eoe-sde-codisc.privatelink.fitfile.net`
- **Auth0**: `fitfile-prod.eu.auth0.com`
- **Certificate**: `fitfile-eoe-tls`

### **NHS Provider Deployments**

- **ff-hyve-1**: `nhs-provider-1.fitfile.net`
  - ArgoCD: `nhs-provider-1-argocd.fitfile.net`
  - Argo Workflows: `nhs-provider-1-argo-workflows.fitfile.net`
- **ff-hyve-2**: `nhs-provider-2.fitfile.net`
  - ArgoCD: `nhs-provider-2-argocd.fitfile.net`
  - Argo Workflows: `nhs-provider-2-argo-workflows.fitfile.net`

### **CUH Production (`cuh-prod-1`)**

- **Primary Hosts**:
  - Public: `cuh-prod-1.fitfile.net`
  - Private: `cuh-poc-1.privatelink.fitfile.net`
- **Auth0**: `fitfile-prod.eu.auth0.com`
- **External Database**: `GBCBGPCISQ001.net.addenbrookes.nhs.uk:60709`
- **Relay Connection**: `https://relay.codisc-eoe-sde.uk/link_connector_api`

## **3. Auth0 Domain Configuration**

### **Production Tenant**: `fitfile-prod.eu.auth0.com`

**Configured Audiences**:

- `https://app.fitfile.net` (FF A)
- `https://app2.fitfile.net` (FF B)
- `https://app3.fitfile.net` (FF C)
- `https://barts.fitfile.net` (Barts)
- `https://fitfile.kingsch.nhs.uk` (KCH)
- `https://pentest.fitfile.net` (Pentest)
- `https://primary-care.fitfile.net` (Primary Care)
- `https://cuh-poc-1.privatelink.fitfile.net` (CUH)
- `https://app.eoe-sde-codisc.privatelink.fitfile.net` (HIE SDE)

### **Test Tenant**: `fitfile-test.eu.auth0.com`

- Used by EOE SDE and NHS Provider deployments

## **4. DNS Pattern Analysis**

### **Current Naming Patterns**

**Public Domains**:

- `*.fitfile.net` (Main FITFILE domain)
- `*.kingsch.nhs.uk` (KCH NHS trust)
- `*.net.stgeorges.nhs.uk` (St George's NHS trust)
- `codisc-eoe-sde.uk` (EOE customer domain)

**Private/Internal Domains**:

- `*.privatelink.fitfile.net` (Private link services)
- `internal.fitfile.net` (CUH internal DNS zone)

**Service-Specific Subdomains**:

- `argocd.*` (GitOps management)
- `*-argo-workflows.*` (Workflow management)
- `relay.*` (M2M communication)
- `app.*` (Main application access)

## **5. Recommended Consistent Naming Structure**

Based on the analysis, I propose this consistent naming convention:

### **For Customer Public Domains** (Human Access)

```sh
Format: {customer-code}.{trust-domain}
Examples:
- cuh-prod-1.fitfile.net (if using FITFILE domain)
- app.codisc-eoe-sde.uk (if using customer domain)
```

### **For Private/Internal Services** (M2M/Internal)

```sh
Format: {service}.{customer-code}.privatelink.fitfile.net
Examples:
- app.cuh-prod-1.privatelink.fitfile.net
- argocd.eoe-sde.privatelink.fitfile.net
- relay.eoe-sde.privatelink.fitfile.net
```

### **For Management Services** (Admin Access)

```sh
Format: {service}-{customer-code}.{domain}
Examples:
- argocd-cuh-prod-1.fitfile.net
- workflows-eoe-sde.fitfile.net
```

### **For M2M Communication**

```sh
Format: {service}.{customer-domain}
Examples:
- relay.codisc-eoe-sde.uk
- api.codisc-eoe-sde.uk
```

## **6. Key Observations**

1. **Mixed Domain Strategy**: Some deployments use customer-provided domains (`codisc-eoe-sde.uk`) while others use FITFILE domains (`*.fitfile.net`)
2. **Private Link Pattern**: Consistent use of `*.privatelink.fitfile.net` for internal services
3. **Auth0 Integration**: Clear separation between prod (`fitfile-prod.eu.auth0.com`) and test (`fitfile-test.eu.auth0.com`) tenants
4. **Certificate Management**: Mix of Let's Encrypt and Cloudflare certificates
5. **NHS Trust Domains**: Some deployments use NHS trust-specific domains (`*.kingsch.nhs.uk`, `*.net.stgeorges.nhs.uk`)

This analysis shows a generally well-organized but somewhat inconsistent naming approach that could benefit from standardization, especially for new deployments.
