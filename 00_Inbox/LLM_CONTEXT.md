---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:54+00:00
title: LLM_CONTEXT
---

## LCA-DP Terraform Repository - Complete LLM Context Guide

> Purpose: This document provides comprehensive context about the LCA-DP Terraform repository structure, dependencies, data flow, and architectural patterns for LLM coding assistants.
>
> Last Updated: 2026-01-27
>
> Repository Path: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/nwsde/Production/LCA-DP`

---

### Table of Contents

1. [Repository Overview](#repository-overview)
2. [Architecture & Design Principles](#architecture--design-principles)
3. [File Structure & Key Components](#file-structure--key-components)
4. [Data Flow Pipeline](#data-flow-pipeline)
5. [Module Dependencies](#module-dependencies)
6. [Configuration System](#configuration-system)
7. [Generated Artifacts](#generated-artifacts)
8. [Secrets Management](#secrets-management)
9. [Networking Architecture](#networking-architecture)
10. [Deployment Workflow](#deployment-workflow)
11. [Key Files Reference](#key-files-reference)
12. [Common Operations](#common-operations)
13. [Troubleshooting Guide](#troubleshooting-guide)

---

### Repository Overview

#### Purpose

This Terraform repository automates the complete deployment of a new customer environment for the FITFILE platform. It orchestrates:

1. Central Services (via `central-services-consumer` module)
   - GitLab project creation
   - Terraform Cloud workspace setup
   - Auth0 application configuration
   - HashiCorp Vault namespace and secrets
   - Grafana workspace (optional)

2. Infrastructure (via `private-infrastructure` module)
   - Azure Virtual Network (VNet) and subnets
   - Azure Kubernetes Service (AKS) cluster
   - NAT Gateway and networking components
   - Azure Bastion for secure access
   - Jumpbox VM for private network operations
   - Network Security Groups (NSGs)

3. Generated Configuration
   - Jumpbox `main.tf` for internal deployment
   - Helm `values.yaml` for application deployment
   - Dynamic `providers.tf` with correct workspace name

#### Key Principle: GitOps with Single Source of Truth

The entire infrastructure is derived from `config/customer.yaml`. No hardcoded values are allowed for customer-specific configuration.

---

### Architecture & Design Principles

#### 1. Generative Configuration Strategy

Rule: All customer-specific values MUST be derived from `config/customer.yaml` through `locals.tf`.

Why?:

- Eliminates configuration drift
- Ensures consistency across environments
- Enables rapid customer onboarding
- Simplifies maintenance and auditing

#### 2. Two-Module Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Root Module                           │
│  (Orchestration Layer - This Repository)                   │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌──────────────────────────┐    ┌─────────────────────────────┐
│  central-services        │    │  private-infrastructure     │
│  Consumer Module         │    │  Azure Module               │
│  (TFC Registry)          │    │  (TFC Registry)             │
│  v1.0.4                  │    │  v1.3.31                    │
├──────────────────────────┤    ├─────────────────────────────┤
│ • GitLab Projects        │    │ • Azure VNet                │
│ • TFC Workspaces         │    │ • AKS Cluster               │
│ • Auth0 Apps             │    │ • NAT Gateway               │
│ • Vault Namespaces       │    │ • Azure Bastion             │
│ • Vault Secrets          │    │ • Jumpbox VM                │
│ • Grafana Workspaces     │    │ • Node Pools                │
│ • VM Admin Password      │    │ • NSGs                      │
│   Generation             │    │ • Private DNS Zones         │
└──────────────────────────┘    └─────────────────────────────┘
```

#### 3. Cross-Module Data Flow

The modules have interdependencies:

- `central-services` generates `vm_admin_password` → consumed by `private-infrastructure`
- `private-infrastructure` outputs AKS credentials → injected into TFC workspace by `central-services`
- Both modules depend on data from `config/customer.yaml` processed in `locals.tf`

---

### File Structure & Key Components

#### Root Directory Layout

```
LCA-DP/
├── config/
│   └── customer.yaml           # SINGLE SOURCE OF TRUTH - All customer config
│
├── templates/                  # Generation Templates
│   ├── jumpbox_main.tftpl     # Template for jumpbox Terraform config
│   ├── providers.tftpl         # Template for Terraform Cloud backend config
│   └── values.cue              # CUE schema for Helm values generation
│
├── generated/                  # Auto-generated files (gitignored)
│   ├── main.tf                 # Generated jumpbox Terraform
│   ├── providers.tf            # Generated provider config
│   ├── values.yaml             # Generated Helm values
│   └── infra.json              # Intermediate data for CUE
│
├── scripts/                    # Automation Scripts
│   ├── generate-values.sh      # Automates Helm values generation
│   ├── connect-jumpbox.sh      # Azure Bastion connection helper
│   ├── validate-vault-paths.sh # Vault configuration validator
│   └── verify_argocd.sh        # ArgoCD deployment checker
│
├── docs/                       # Documentation
│   ├── LCA_DP_CONTEXT.md      # Logic and data flow documentation
│   ├── PROJECT_BRAIN.md        # Multi-repo orchestration guide
│   ├── PROVIDER_GENERATION.md  # Provider config generation guide
│   └── JUMPBOX_DEPLOYMENT.md   # Jumpbox setup instructions
│
├── Core Terraform Files
├── main.tf                     # Module invocations and orchestration
├── locals.tf                   # Transformation logic (yaml → locals)
├── variables.tf                # Input variables (secrets, config)
├── outputs.tf                  # Exposed outputs
├── providers.tf                # Provider configurations + TFC backend
├── versions.tf                 # Provider version constraints
├── data.tf                     # Data sources (remote state, Azure)
│
├── Generator Files
├── jumpbox_generator.tf        # Generates jumpbox main.tf
├── values_generator.tf         # Exports data for Helm values
├── providers_generator.tf      # Generates providers.tf
│
├── Vault Configuration
├── vault_k8s_auth.tf          # Vault JWT auth setup for K8s
│
├── Automation
├── Makefile                    # Build automation targets
│
└── State & Config
    ├── secrets.auto.tfvars.json # Sensitive configuration (gitignored)
    ├── terraform.tfvars         # Additional variables
    ├── .terraform.lock.hcl      # Provider lock file
    └── terraform.tfstate        # Terraform state (remote backend)
```

---

### Data Flow Pipeline

#### Complete Pipeline: From YAML to Deployed Application

```mermaid
graph TB
    A[config/customer.yaml] --> B[locals.tf]
    B --> C[module.central_services]
    B --> D[module.private-infrastructure]
    
    C --> E[GitLab Project Created]
    C --> F[TFC Workspace Created]
    C --> G[Vault Namespace + Secrets]
    C --> H[Auth0 Application]
    C --> I[VM Admin Password Generated]
    
    I --> D
    D --> J[VNet + Subnets Created]
    D --> K[AKS Cluster Created]
    D --> L[Jumpbox VM Created]
    D --> M[NAT Gateway + Bastion]
    
    K --> N[AKS Credentials]
    N --> O[Injected into TFC Workspace]
    
    B --> P[values_generator.tf]
    P --> Q[terraform output infra_facts]
    Q --> R[scripts/generate-values.sh]
    R --> S[templates/values.cue]
    S --> T[generated/values.yaml]
    
    B --> U[jumpbox_generator.tf]
    U --> V[templates/jumpbox_main.tftpl]
    V --> W[generated/main.tf]
    
    W --> X[Deployed to Jumpbox]
    X --> Y[ArgoCD Deployed]
    T --> Y
    Y --> Z[Application Pods Running]
```

#### Step-by-Step Flow

1. Configuration Input
   - Engineer edits `config/customer.yaml`
   - Contains: customer name, region, network CIDRs, feature flags

2. Local Transformation
   - `locals.tf` reads YAML using `yamldecode()`
   - Calculates derived values:
     - `deployment_key = "${customer_short_name}-${env_prefix}-${instance_id}"`
     - Subnet CIDRs using `cidrsubnet()` function
     - Resource names following naming conventions
     - DNS names, tags, etc.

3. Module Execution (Parallel)
   - central-services module:
     - Creates GitLab project in specified group
     - Creates TFC workspace in specified project
     - Creates Auth0 application with callbacks
     - Creates Vault namespace: `admin/deployments/${deployment_key}`
     - Generates secrets (MongoDB, PostgreSQL, S3, VM password)
     - Outputs: `gitlab_project_url`, `tfc_workspace_id`, `vm_admin_password`
   - private-infrastructure module:
     - Creates Azure resource group
     - Creates VNet with calculated subnets
     - Creates AKS cluster with OIDC enabled
     - Creates NAT Gateway and associates with subnets
     - Creates Azure Bastion
     - Creates Jumpbox VM (uses `vm_admin_password` from central-services)
     - Outputs: AKS credentials, cluster info

4. Cross-Module Wiring
   - `central-services` injects AKS credentials into TFC workspace as variables
   - Enables the TFC workspace to deploy into the AKS cluster

5. Artifact Generation
   - Providers Config: `providers_generator.tf` creates `generated/providers.tf` with correct workspace name
   - Jumpbox Config: `jumpbox_generator.tf` creates `generated/main.tf` for internal deployment
   - Helm Values: `values_generator.tf` → `generate-values.sh` → CUE → `generated/values.yaml`

6. Deployment to Jumpbox
   - Engineer connects via Azure Bastion
   - Copies `generated/main.tf` to jumpbox
   - Runs Terraform to deploy:
     - ArgoCD application definition
     - Vault Secrets Operator (VSO) configuration
     - Image pull secrets via VSO
     - Kubernetes namespace

7. Application Deployment
   - ArgoCD syncs application from GitLab
   - Uses `generated/values.yaml` for Helm chart
   - VSO injects secrets from Vault
   - Application pods start

---

### Module Dependencies

#### Module: Central-services-consumer

Source: `app.terraform.io/FITFILE-Platforms/central-services-consumer/fitfile`
Version: `1.0.4`
Purpose: Provision SaaS platform services for customer

##### Inputs (from locals.tf)

| Input | Source | Description |
|-------|--------|-------------|
| `customer_name` | `local.customer_short_name` | Short customer identifier (e.g., "lca") |
| `deployment_key` | `local.deployment_key` | Unique deployment identifier (e.g., "lca-prd-2") |
| `environment` | `local.environment` | Environment type (e.g., "live", "dev") |
| `hub_group` | `local.config.hub_group` | Regional hub identifier (e.g., "nwsde") |
| `names` | `local.names` | Map of resource names (gitlab_project, tfc_workspace, vault_namespace) |
| `tfc_project_name` | `local.config.tfc_project_name` | TFC project name (e.g., "NWSDE") |
| `tfc_oauth_token_id` | `var.tfc_oauth_token_id` | GitLab OAuth token for TFC |
| `oidc_issuer_url` | `data.azurerm_kubernetes_cluster.this.oidc_issuer_url` | AKS OIDC issuer URL |
| `auth0_config` | `local.auth0_*` | Auth0 configuration (audience, callbacks, etc.) |
| `aks_host` | `module.private-infrastructure.aks_cluster_host` | AKS API server address |
| `aks_cluster_ca_certificate` | `module.private-infrastructure.aks_cluster_ca_certificate` | AKS CA cert |
| `aks_cluster_client_certificate` | `module.private-infrastructure.aks_cluster_client_certificate` | Client cert |
| `aks_cluster_client_key` | `module.private-infrastructure.aks_cluster_client_key` | Client key |
| `ude_key` | `var.ude_key` | Customer UDE encryption key |
| `tenant_private_key` | `var.tenant_private_key` | PKCS8 private key |
| `tenant_public_key` | `var.tenant_public_key` | Public key certificate |

##### Feature Flags

| Flag | Value | Purpose |
|------|-------|---------|
| `enable_gitlab` | `true` | Create GitLab project |
| `enable_tfc` | `true` | Create TFC workspace |
| `enable_auth0` | `true` | Create Auth0 application |
| `enable_vault` | `true` | Create Vault namespace and secrets |
| `enable_grafana` | `false` | Create Grafana workspace (disabled) |
| `enable_oidc_auth` | `true` | Enable OIDC for Vault K8s auth |

##### Outputs

| Output | Description | Used By |
|--------|-------------|---------|
| `vm_admin_password` | Generated admin password | `private-infrastructure` module |
| `values_repo_url` | GitLab SSH URL | Jumpbox ArgoCD config |
| `auth0_client_id` | Auth0 client ID | Application configuration |
| `auth0_api_identifier` | Auth0 API audience | Application configuration |
| `gitlab_project_url` | GitLab HTTPS URL | Documentation |
| `gitlab_project_ssh_url` | GitLab SSH URL | ArgoCD source |
| `tfc_workspace_id` | TFC workspace ID | Variable injection |

#### Module: Private-infrastructure

Source: `app.terraform.io/FITFILE-Platforms/private-infrastructure/azure`
Version: `1.3.31`
Purpose: Deploy Azure networking and AKS infrastructure

##### Inputs (from locals.tf)

| Input | Source | Description |
|-------|--------|-------------|
| `create_vnet` | `true` | Create new VNet |
| `vnet_resource_group_name` | `local.resource_group_name` | RG name (rg-{workload}-{region}-{env_prefix}-net) |
| `vnet_name` | `local.vnet_name` | VNet name (vnet-{workload}-plat-{region}-01) |
| `deployment_key` | `local.deployment_key` | Deployment identifier |
| `admin_password` | `module.central_services.vm_admin_password` | VM admin password (from central-services) |
| `vm_name` | `local.jumpbox_name` | Jumpbox VM name (vm{workload}jmp01) |
| `vm_size` | `local.vm_size` | Azure VM size (Standard_D2s_v5) |
| `disk_controller_type` | `local.disk_controller_type` | Disk controller (SCSI) |
| `aks_vnet_address_space` | `[local.vnet_address_space]` | VNet CIDR (e.g., /16) |
| `subnets` | `local.subnets` | Map of subnet configurations |
| `kubernetes_version` | `local.kubernetes_version` | AKS version (e.g., 1.34.0) |
| `aks_cluster_outbound_type` | `"userAssignedNATGateway"` | Outbound connectivity method |
| `location` | `local.location` | Azure region (e.g., uksouth) |
| `default_node_pool_vm_size` | `local.vm_size` | Default node pool VM size |
| `node_pools` | Map | Additional node pools (workflows) |
| `bastion_enabled` | `true` | Enable Azure Bastion |
| `bastion_name` | `local.bastion_name` | Bastion name |
| `nat_gateway_enabled` | `true` | Enable NAT Gateway |
| `nat_gateway_idle_timeout` | `10` | NAT idle timeout (minutes) |
| `default_node_pool_subnet_address_prefix` | `[local.subnet_prefixes.system]` | System pool subnet |
| `vm_subnet_address_prefix` | `[local.subnet_prefixes.jumpbox]` | Jumpbox subnet |
| `workload` | `local.workload` | Workload identifier |
| `region` | `local.region` | Region code (e.g., uks) |
| `env_prefix` | `local.env_prefix` | Environment prefix (e.g., prd) |
| `tags` | `local.common_tags` | Azure tags |
| `environment` | `local.environment` | Environment name |
| `private_dns_zone_enabled` | `true` | Enable private DNS zone |
| `oidc_issuer_enabled` | `local.oidc_issuer_enabled` | Enable OIDC issuer |
| `workload_identity_enabled` | `local.workload_identity_enabled` | Enable workload identity |

##### Node Pools Configuration

```hcl
node_pools = {
  workflows = {
    vm_size     = local.vm_size
    subnet_key  = "workflows"
    priority    = "Spot"
    node_taints = [
      "dedicated=workflows:PreferNoSchedule",
      "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"
    ]
    min_count   = 0
  }
}
```

##### Outputs

| Output | Description | Used By |
|--------|-------------|---------|
| `aks_cluster_host` | AKS API server URL | central-services (injected to TFC) |
| `aks_cluster_ca_certificate` | CA certificate | central-services, jumpbox config |
| `aks_cluster_client_certificate` | Client certificate | central-services |
| `aks_cluster_client_key` | Client key | central-services |

---

### Configuration System

#### config/customer.yaml Schema

```yaml
# Customer Identity
customer_name: lca                              # Short name (alphanumeric, lowercase)
customer_full_name: "Liverpool City Region Combined Authority"  # Display name
environment: live                               # Environment type
env_prefix: prd                                 # Short environment code
instance_id: 2                                  # Instance number (for multiple clusters)

# Azure Infrastructure
region: uks                                     # Azure region code
location: uksouth                               # Full Azure region name
vnet_address_space: "/16"              # Base network CIDR
vm_size: "Standard_D2s_v5"                     # Azure VM size
disk_controller_type: "SCSI"                   # Disk controller type
kubernetes_version: "1.34.0"                    # AKS version

# Organizational Context
hub_group: nwsde                                # Regional hub identifier
gitlab_group: "customers/nwsde"                 # GitLab parent group path
tfc_project_name: NWSDE                         # Terraform Cloud project

# AKS Feature Flags
oidc_issuer_enabled: true                       # Enable OIDC issuer for workload identity
workload_identity_enabled: true                 # Enable workload identity federation

# Tags (Applied to all Azure resources)
tags:
  Department: "SDE"
  CreatedWith: "Terraform"
  ManagedBy: "FITFILE"
  Status: "live"
  Application: "LCA-DP"
  Criticality: "Tier1"
  AutoLockExclusion: "true"

# Auth0 Configuration
auth0_enabled_apis: []                          # Additional Auth0 APIs to enable
```

#### locals.tf Transformation Logic

##### Core Identity Calculations

```hcl
locals {
  # Load YAML configuration
  config = yamldecode(file("${path.module}/config/customer.yaml"))
  
  # Extract and compute core identity
  customer_full_name   = local.config.customer_full_name
  customer_short_name  = local.config.customer_name
  environment          = local.config.environment
  workload             = local.customer_short_name
  env_prefix           = local.config.env_prefix
  
  # Composite deployment key (used throughout)
  deployment_key = "${local.customer_short_name}-${local.env_prefix}-${local.config.instance_id}"
  # Example: "lca-prd-2"
}
```

##### Network Calculations

Subnet Slicing Logic (using `cidrsubnet()` function):

```hcl
locals {
  vnet_address_space = local.config.vnet_address_space  # e.g., /16
  
  # Subnet allocation from base CIDR
  subnet_prefixes = {
    system    = cidrsubnet(local.vnet_address_space, 4, 0)   # /20, Index 0
    workflows = cidrsubnet(local.vnet_address_space, 4, 1)   # /20, Index 1
    app       = cidrsubnet(local.vnet_address_space, 4, 2)   # /20, Index 2
    jumpbox   = cidrsubnet(local.vnet_address_space, 4, 3)   # /20, Index 3
    bastion   = cidrsubnet(local.vnet_address_space, 8, 64)  # /24, Index 64
  }
  
  # Load balancer IP calculation
  ingress_ip = cidrhost(local.subnet_prefixes.system, 203)  # System subnet + offset 203
}
```

Example: If `vnet_address_space = "/16"`:

- System subnet: `/20` (can hold 4096 IPs)
- Workflows subnet: `10.150.16.0/20`
- App subnet: `10.150.32.0/20`
- Jumpbox subnet: `10.150.48.0/20`
- Bastion subnet: `10.150.64.0/24`
- Ingress IP: `10.150.0.203`

##### Resource Naming Convention

```hcl
locals {
  # Resource Group
  resource_group_name = "rg-${local.workload}-${local.region}-${local.env_prefix}-net"
  # Example: "rg-lca-uks-prd-net"
  
  # Virtual Network
  vnet_name = "vnet-${local.workload}-plat-${local.region}-01"
  # Example: "vnet-lca-plat-uks-01"
  
  # Bastion Host
  bastion_name = "bastion-${local.workload}-plat-${local.region}-01"
  # Example: "bastion-lca-plat-uks-01"
  
  # Jumpbox VM (truncated naming)
  jumpbox_name = "vm${local.workload}jmp01"
  # Example: "vmlcajmp01"
}
```

##### Auth0 Configuration

```hcl
locals {
  # DNS and URLs
  public_fqdn   = "${local.customer_short_name}.fitfile.io"  # e.g., "lca.fitfile.net"
  api_audience  = "https://${local.public_fqdn}"
  
  # Auth0 callbacks and origins
  auth0_config = {
    audience = local.api_audience
    callbacks = [
      "${local.api_audience}/auth/callback/auth0",
      "https://${local.public_fqdn}/api/v1/auth/callback",
      "https://${local.ingress_ip}/callback"
    ]
    logout_urls = [
      "${local.api_audience}/login",
      "https://${local.public_fqdn}/login"
    ]
    web_origins = [
      local.api_audience,
      "https://${local.public_fqdn}"
    ]
  }
}
```

##### Central Services Naming

```hcl
locals {
  names = {
    gitlab_project  = "${local.customer_short_name}-infra-${local.env_prefix}"
    # Example: "lca-infra-prd"
    
    tfc_workspace   = "${local.customer_short_name}-infra-${local.env_prefix}"
    # Example: "lca-infra-prd"
    
    vault_namespace = local.deployment_key
    # Example: "lca-prd-2"
  }
}
```

##### Tags

```hcl
locals {
  common_tags = merge(local.config.tags, {
    Environment = local.environment
    Owner       = local.customer_full_name
  })
}
```

---

### Generated Artifacts

#### 1. generated/providers.tf

Purpose: Terraform Cloud backend configuration with correct workspace name

Generation Flow:

```
templates/providers.tftpl → providers_generator.tf → generated/providers.tf
```

Template Variables:

- `${deployment_key}`: Injected workspace name

Usage:

```bash
make generate-providers
# Generates file and copies to providers.tf
```

Content Example:

```hcl
terraform {
  cloud {
    organization = "FITFILE-Platforms"
    workspaces {
      name = "lca-prd-2"  # Dynamically generated
    }
  }
}

provider "azurerm" { ... }
provider "gitlab" { ... }
# ... other providers
```

#### 2. generated/main.tf (Jumpbox Config)

Purpose: Terraform configuration for deploying platform services from inside private network

Generation Flow:

```
data.azurerm_kubernetes_cluster.this → locals → templates/jumpbox_main.tftpl → 
jumpbox_generator.tf → generated/main.tf
```

Template Variables:

- `${vault_address}`: HCP Vault URL
- `${deployment_repo_values_file_path}`: Path to values.yaml in GitLab repo
- `${argocd_host}`: ArgoCD FQDN
- `${deployment_key}`: Deployment identifier
- `${ingress_controller_ip_address}`: Calculated ingress IP
- `${oidc_issuer_url}`: AKS OIDC issuer URL
- `${values_repo_url}`: GitLab repo SSH URL
- `${chart_repo_url}`: Helm chart repository URL

Key Resources Deployed:

1. Kubernetes Namespace: `${deployment_key}`
2. Vault Authentication: JWT auth for each namespace
3. Image Pull Secrets: VSO-managed secrets in all namespaces
4. ArgoCD Application: Multi-source app definition
5. Vault Static Secrets: ArgoCD Git credentials

Deployment Instructions:

```bash
# On jumpbox VM (via Azure Bastion)
terraform output -raw jumpbox_main_content > main.tf
terraform init
terraform apply
```

#### 3. generated/values.yaml (Helm Values)

Purpose: Helm values file for FITFILE application deployment via ArgoCD

Generation Flow:

```
config/customer.yaml → locals.tf → values_generator.tf → terraform output infra_facts →
scripts/generate-values.sh → templates/values.cue → generated/values.yaml
```

Automation:

```bash
make generate-values
# Automatically extracts Terraform outputs and runs CUE export
```

CUE Input Schema (`templates/values.cue`):

```cue
#InfraFacts: {
    customer_short_name: string
    deployment_key:      string
    public_fqdn:         string
    fit_connect_code:    string
}
```

Key Sections in Generated YAML:

1. Global Configuration
   - Namespace
   - Deployment key
   - Public FQDN
   - Image pull secrets
   - OAuth configuration

2. ArgoCD Application
   - Multi-source application
   - Chart repository reference
   - Values repository reference

3. Component-Specific Values
   - ArgoCD Workflows (with PostgreSQL credentials from Vault)
   - MongoDB (replica set key, root password)
   - MinIO (S3 credentials)
   - PostgreSQL (password)
   - FITConnect (application secrets)
   - FFCloud (API secrets)
   - Grafana (monitoring credentials)

4. Vault Secret References
   - All secrets use VSO (Vault Secrets Operator)
   - Path: `admin/deployments/${deployment_key}/secrets/data/*`
   - Transformation templates for format conversion

Example Vault Secret Reference:

```yaml
vaultSecrets:
  - secretName: "mongodb"
    vaultPath: "application"
    secretTransformation:
      templates:
        "mongodb-root-password":
          text: "{{`{{get .Secrets \"mongodb_password\"}}`}}"
```

---

### Secrets Management

#### Vault Architecture

Namespace Structure:

```
admin/
├── central/
│   ├── azure/creds/acr-pull  (Azure Container Registry credentials)
│   └── ...
└── deployments/
    └── ${deployment_key}/     (e.g., "lca-prd-2")
        └── secrets/
            └── data/
                ├── application
                ├── monitoring
                ├── auth0_credentials
                └── ...
```

#### Authentication Methods

##### 1. JWT Authentication (Kubernetes Workload Identity)

Configuration: `vault_k8s_auth.tf`

```hcl
resource "vault_jwt_auth_backend" "jwt" {
  path               = "jwt-${local.deployment_key}"
  oidc_discovery_url = data.azurerm_kubernetes_cluster.this.oidc_issuer_url
  bound_issuer       = data.azurerm_kubernetes_cluster.this.oidc_issuer_url
}

resource "vault_jwt_auth_backend_role" "vso" {
  backend   = vault_jwt_auth_backend.jwt.path
  role_name = local.deployment_key
  
  bound_audiences = [
    "https://kubernetes.default.svc.cluster.local",
    data.azurerm_kubernetes_cluster.this.oidc_issuer_url
  ]
  
  bound_claims = {
    sub = "system:serviceaccount:*:default"
  }
  
  token_policies = [
    "default",
    vault_policy.acr_reader.name,
    vault_policy.argocd_secrets.name
  ]
}
```

How It Works:

1. AKS cluster issues JWT tokens via OIDC
2. Pods use service account tokens
3. VSO authenticates to Vault using JWT
4. Vault validates token against OIDC issuer
5. Vault grants access based on policies

##### 2. Vault Policies

ACR Reader Policy (Image Pull Secrets):

```hcl
resource "vault_policy" "acr_reader" {
  name = "acr-reader"
  
  policy = <<EOT
path "central/azure/creds/acr-pull" {
  capabilities = ["read"]
}
EOT
}
```

ArgoCD Secrets Policy:

```hcl
resource "vault_policy" "argocd_secrets" {
  name = "argocd-secrets-${local.deployment_key}"
  
  policy = <<EOT
path "deployments/${local.deployment_key}/secrets/data/*" {
  capabilities = ["read", "list"]
}
EOT
}
```

#### Secret Generation

Central Services Module creates the following secrets:

| Secret | Vault Path | Purpose | Generated By |
|--------|-----------|---------|--------------|
| VM Admin Password | `application/vm_admin_password` | Jumpbox SSH access | `random_password.vm_admin` |
| MongoDB Root Password | `application/mongodb_password` | MongoDB admin | `random_password.mongo_root` |
| PostgreSQL Password | `application/postgresql_password` | PostgreSQL access | `random_password.postgres_pwd` |
| S3 Credentials | `application/s3_access_key_id`, `s3_secret_access_key` | MinIO access | `random_password.s3_secret` |
| SpiceDB Pre-Shared Key | `application/spicedb_pre_shared_key` | SpiceDB auth | `random_password.spicedb_key` |
| Grafana Admin | `monitoring/grafana_admin_password` | Grafana access | `random_password.grafana_admin` |
| Auth0 Credentials | `auth0_credentials/client_id`, `client_secret` | OAuth | Auth0 provider |

#### Sensitive Variables

Supplied via `secrets.auto.tfvars.json`:

```json
{
  "vault_address": "https://vault.example.com",
  "ude_key": "encrypted_data_key",
  "tenant_private_key": "-----BEGIN PRIVATE KEY-----...",
  "tenant_public_key": "-----BEGIN CERTIFICATE-----...",
  "tfc_oauth_token_id": "ot-xxxx",
  "tfe_token": "tfe_token_value"
}
```

Never committed to Git (`.gitignore` entry).

---

### Networking Architecture

#### Subnet Allocation Strategy

Base CIDR: Defined in `config/customer.yaml` as `vnet_address_space`
Allocation Method: `cidrsubnet()` function with consistent indexing

##### Subnet Breakdown

| Subnet | CIDR Calculation | Index | Purpose | NAT Gateway | NSG |
|--------|-----------------|-------|---------|-------------|-----|
| system | `cidrsubnet(base, 4, 0)` | 0 | AKS system node pool | ✅ Yes | ✅ Yes |
| workflows | `cidrsubnet(base, 4, 1)` | 1 | AKS workflows node pool (Spot) | ✅ Yes | ✅ Yes |
| app | `cidrsubnet(base, 4, 2)` | 2 | AKS application node pool | ✅ Yes | ❌ No |
| jumpbox | `cidrsubnet(base, 4, 3)` | 3 | Jumpbox VM | ✅ Yes | ✅ Yes |
| bastion | `cidrsubnet(base, 8, 64)` | 64 | Azure Bastion | ❌ No | ❌ No |

Prefix Length:

- `/16` base → `/20` subnets (4096 IPs each)
- `/16` base → `/24` bastion (256 IPs)

##### NAT Gateway Configuration

Purpose: Provide outbound internet connectivity for private subnets

Associated Subnets:

- system
- workflows
- jumpbox

Configuration:

```hcl
nat_gateway_enabled      = true
nat_gateway_idle_timeout = 10  # minutes
```

Public IP: Single public IP associated with NAT Gateway

##### Network Security Groups (NSGs)

Applied to:

- system subnet
- workflows subnet
- jumpbox subnet

Default Rules: Defined in `private-infrastructure` module

#### IP Address Assignments

##### Static IPs

| Resource | IP Calculation | Example | Purpose |
|----------|---------------|---------|---------|
| Ingress Controller | `cidrhost(system_subnet, 203)` | `10.150.0.203` | Nginx Ingress LoadBalancer |

##### Private DNS Zones

Zone: `${customer_short_name}.fitfile.io.private`
Example: `lca.fitfile.net.private`

A Records:

- `argocd.${customer_short_name}.fitfile.io` → Ingress IP
- `*.${customer_short_name}.fitfile.io` → Ingress IP (wildcard)

VNet Link: Links private DNS zone to VNet for internal resolution

---

### Deployment Workflow

#### Phase 1: Pre-Deployment (One-Time Setup)

##### 1.1 Configure Customer Details

Edit `config/customer.yaml`:

```bash
vim config/customer.yaml
```

Update:

- Customer name and full name
- Network CIDR (coordinate with network team)
- Azure region
- Instance ID (if multiple clusters needed)
- Tags

##### 1.2 Prepare Secrets

Create `secrets.auto.tfvars.json`:

```json
{
  "vault_address": "https://vault-cluster.vault.xxxx.aws.hashicorp.cloud:8200",
  "ude_key": "<provided_by_security_team>",
  "tenant_private_key": "<pkcs8_private_key>",
  "tenant_public_key": "<public_key_certificate>",
  "tfc_oauth_token_id": "ot-xxxxxxxxxxxx",
  "tfe_token": "<tfc_api_token>"
}
```

##### 1.3 Generate Provider Configuration

```bash
make generate-providers
```

This creates `generated/providers.tf` with correct TFC workspace name and copies it to `providers.tf`.

#### Phase 2: Infrastructure Deployment

##### 2.1 Initialize Terraform

```bash
terraform init
```

Connects to Terraform Cloud workspace.

##### 2.2 Plan Infrastructure

```bash
terraform plan -out=tfplan
```

Review:

- Module `central_services` resources
- Module `private-infrastructure` resources
- Generated files
- Vault authentication config

##### 2.3 Apply Infrastructure

```bash
terraform apply tfplan
```

Timeline: ~15-20 minutes

What Happens:

1. ✅ GitLab project created
2. ✅ TFC workspace created
3. ✅ Vault namespace and secrets created
4. ✅ Auth0 application created
5. ✅ Azure resource group created
6. ✅ VNet and subnets created
7. ✅ NAT Gateway provisioned
8. ✅ Azure Bastion deployed
9. ✅ AKS cluster provisioned
10. ✅ Jumpbox VM created
11. ✅ Vault JWT auth configured
12. ✅ `generated/main.tf` created
13. ✅ `generated/providers.tf` created

#### Phase 3: Generate Application Configuration

##### 3.1 Generate Helm Values

```bash
make generate-values
```

What It Does:

1. Extracts `infra_facts` from Terraform output
2. Passes data to CUE template
3. Validates schema
4. Generates `generated/values.yaml`

##### 3.2 Commit Generated Values to GitLab

```bash
git add generated/values.yaml
git commit -m "feat(values): generate helm values for lca-prd-2"
git push
```

Important: This values file will be consumed by ArgoCD.

#### Phase 4: Jumpbox Deployment

##### 4.1 Connect to Jumpbox

```bash
./scripts/connect-jumpbox.sh
```

Or manually via Azure Portal:

1. Navigate to Bastion
2. Select jumpbox VM
3. Connect with username `azureuser` and password from Vault

##### 4.2 Prepare Jumpbox Terraform

On your local machine:

```bash
terraform output -raw jumpbox_main_content > /tmp/jumpbox_main.tf
```

Copy to jumpbox:

```bash
scp -o ProxyCommand="az network bastion ssh ..." /tmp/jumpbox_main.tf azureuser@jumpbox:/home/azureuser/main.tf
```

##### 4.3 Deploy from Jumpbox

On jumpbox:

```bash
# Install Terraform if needed
wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
unzip terraform_1.5.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Initialize and apply
terraform init
terraform plan
terraform apply -auto-approve
```

What Gets Deployed:

1. ✅ Kubernetes namespace: `${deployment_key}`
2. ✅ Vault JWT auth resources in each namespace
3. ✅ VSO VaultAuth resources
4. ✅ Image pull secrets (via VSO)
5. ✅ ArgoCD Application definition

#### Phase 5: Application Deployment (Automated)

##### 5.1 ArgoCD Sync

ArgoCD detects the new Application resource and:

1. Clones Helm chart from `https://gitlab.com/fitfile/deployment.git`
2. Clones values from GitLab project (created in Phase 2)
3. Merges values and renders Helm templates
4. Applies resources to namespace

##### 5.2 VSO Secret Injection

Vault Secrets Operator:

1. Detects `VaultStaticSecret` and `VaultDynamicSecret` resources
2. Authenticates to Vault using JWT
3. Reads secrets from Vault paths
4. Creates Kubernetes Secrets
5. Watches for updates and refreshes

##### 5.3 Application Startup

Components start in order:

1. PostgreSQL StatefulSet
2. MongoDB StatefulSet
3. MinIO Deployment
4. SpiceDB Deployment
5. FITConnect Deployment
6. FFCloud Deployment
7. Ingress resources

#### Phase 6: Verification

##### 6.1 Check Terraform State

```bash
terraform state list | grep module
```

Expected resources: ~50-70 resources

##### 6.2 Validate Vault Configuration

```bash
./scripts/validate-vault-paths.sh
```

Checks:

- JWT auth mount exists
- JWT role configured correctly
- Policies created
- Secrets readable

##### 6.3 Verify ArgoCD Deployment

```bash
./scripts/verify_argocd.sh
```

Checks:

- Application resource exists
- Sync status is "Synced"
- Health status is "Healthy"
- All pods are running

##### 6.4 Test Application

```bash
curl https://lca.fitfile.net/fitconnect/health
curl https://lca.fitfile.net/ffcloud/health
```

---

### Key Files Reference

#### Terraform Core Files

##### main.tf

Purpose: Orchestrates the two main modules

Key Sections:

1. Module `private-infrastructure` invocation
2. Data source for AKS cluster (to fetch OIDC issuer)
3. Module `central_services` invocation

Dependencies:

- `private-infrastructure` must complete before OIDC URL is available
- `central_services` depends on OIDC URL and AKS credentials

##### locals.tf

Purpose: Single source of truth for all derived values

Key Sections:

1. YAML loading: `config = yamldecode(file(…))`
2. Identity calculations: `deployment_key`, `workload`, etc.
3. Network calculations: `subnet_prefixes`, `ingress_ip`
4. Naming conventions: `resource_group_name`, `vnet_name`, etc.
5. Auth0 configuration: `public_fqdn`, `api_audience`, callbacks
6. Central services naming: `names` map
7. Tags: `common_tags`

Critical Logic:

- Never hardcode customer-specific values here
- All values must derive from `config/customer.yaml`
- Use Terraform functions: `cidrsubnet()`, `cidrhost()`, string interpolation

##### variables.tf

Purpose: Define input variables (mostly secrets)

Variables:

- `vault_address`: HCP Vault URL
- `ude_key`: Customer encryption key (sensitive)
- `tenant_private_key`: PKCS8 private key (sensitive)
- `tenant_public_key`: Public certificate
- `tfc_oauth_token_id`: GitLab OAuth token for TFC
- `tfe_token`: TFC API token (sensitive)

Note: `admin_password` variable was removed (now generated by `central_services`).

##### outputs.tf

Purpose: Expose key outputs for external use

Outputs:

- `auth0_client_id`: For application configuration
- `auth0_api_identifier`: For OAuth audience
- `gitlab_project_url`: For documentation
- `gitlab_project_ssh_url`: For ArgoCD source

##### providers.tf

Purpose: Configure Terraform providers and backend

Providers:

- `azurerm`: Azure provider
- `gitlab`: GitLab API
- `auth0`: Auth0 API
- `tfe`: Terraform Cloud API
- `vault`: HCP Vault API
- `grafana`: Grafana Cloud API
- `cloudflare`: Cloudflare API

Backend:

```hcl
terraform {
  cloud {
    organization = "FITFILE-Platforms"
    workspaces {
      name = "lca-prd-2"  # Must match deployment_key
    }
  }
}
```

##### versions.tf

Purpose: Lock provider versions

Critical Versions:

- Terraform: `>= 1.5.0`
- azurerm: `4.53.0`
- gitlab: `>= 16.0.0`
- auth0: `>= 1.0.0`
- vault: `>= 3.0.0`

##### data.tf

Purpose: Define data sources

Data Sources:

- `terraform_remote_state.versions`: Fetches Kubernetes version from global version manager
- `azurerm_client_config.main`: Current Azure client configuration

#### Generator Files

##### jumpbox_generator.tf

Inputs:

- `vault_address` (variable)
- `deployment_key` (local)
- `ingress_ip` (local)
- `oidc_issuer_url` (data source)
- `gitlab_infra_repo_url` (from central_services)
- `chart_repo_url` (local constant)

Output:

- `local_file.jumpbox_main`: Creates `generated/main.tf`
- `output.jumpbox_main_content`: Allows extraction via `terraform output`

##### values_generator.tf

Purpose: Export data structure for CUE consumption

Data Structure:

```hcl
locals {
  infra_facts = {
    customer_short_name = local.customer_short_name
    deployment_key      = local.deployment_key
    public_fqdn         = local.public_fqdn
    fit_connect_code    = local.customer_full_name
  }
}
```

Output:

- `output.infra_facts`: JSON-encoded data for `generate-values.sh`

##### providers_generator.tf

Purpose: Generate dynamic providers.tf with correct workspace name

Template Variables:

- `${deployment_key}`: Injected into workspace name

Output:

- `local_file.providers`: Creates `generated/providers.tf`

#### Vault Configuration

##### vault_k8s_auth.tf

Purpose: Configure Vault JWT authentication for Kubernetes

Resources:

1. `vault_jwt_auth_backend.jwt`: Enable JWT auth mount
2. `vault_jwt_auth_backend_role.vso`: Create role for VSO
3. `vault_policy.acr_reader`: Policy for ACR access
4. `vault_policy.argocd_secrets`: Policy for application secrets

JWT Auth Configuration:

- Mount Path: `jwt-${deployment_key}` (e.g., `jwt-lca-prd-2`)
- OIDC Discovery: AKS OIDC issuer URL
- Bound Audiences: Kubernetes service account tokens
- Bound Claims: `sub = "system:serviceaccount:*:default"`

Policies Attached:

- `default`: Vault default policy
- `acr-reader`: Read ACR credentials
- `argocd-secrets-${deployment_key}`: Read customer secrets

#### Automation Files

##### Makefile

Targets:

- `help`: Show available commands
- `generate-values`: Run `scripts/generate-values.sh`
- `generate-providers`: Generate and copy providers.tf
- `validate-cue`: Validate CUE schema without generating
- `clean`: Remove generated files

Usage:

```bash
make <target>
```

##### scripts/generate-values.sh

Purpose: Automate Helm values generation from CUE

Steps:

1. Extract `infra_facts` from Terraform output
2. Validate data is not null
3. Pass to CUE export command
4. Write output to `generated/values.yaml`

Error Handling:

- Exits if Terraform output is null
- Exits if CUE export fails
- Provides next steps on success

##### scripts/validate-vault-paths.sh

Purpose: Verify Vault configuration

Checks:

- JWT auth backend exists
- JWT role exists and is configured correctly
- Policies exist
- Can read secrets with correct permissions

##### scripts/verify_argocd.sh

Purpose: Verify ArgoCD application deployment

Checks:

- Application resource exists
- Application is synced
- Application is healthy
- All resources deployed
- All pods running

---

### Common Operations

#### Update Customer Configuration

```bash
# 1. Edit config
vim config/customer.yaml

# 2. Apply changes
terraform plan
terraform apply

# 3. Regenerate artifacts
make generate-values
make generate-providers  # Only if workspace name changed

# 4. Commit and push
git add config/customer.yaml generated/values.yaml
git commit -m "chore(config): update customer configuration"
git push
```

#### Add New Subnet

```bash
# 1. Edit locals.tf
vim locals.tf

# Add to subnet_prefixes and subnets maps:
# new_subnet = cidrsubnet(local.vnet_address_space, 4, 4)

# 2. Update private-infrastructure module inputs if needed

# 3. Plan and apply
terraform plan
terraform apply
```

#### Change AKS Version

```bash
# 1. Update customer.yaml
vim config/customer.yaml
# Change: kubernetes_version: "1.35.0"

# 2. Apply (will trigger AKS upgrade)
terraform plan
terraform apply

# 3. Monitor AKS upgrade status
az aks show -n aks-lca-uks-prd-01 -g rg-lca-uks-prd-net --query powerState
```

#### Rotate Secrets

```bash
# 1. Trigger rotation in Vault (manual or automated)

# 2. VSO will automatically detect and update Kubernetes secrets

# 3. For secrets that need pod restart:
kubectl rollout restart deployment/<deployment-name> -n lca-prd-2
```

#### Add New Node Pool

```bash
# 1. Edit main.tf
vim main.tf

# Add to node_pools map in private-infrastructure module:
# new_pool = {
#   vm_size     = "Standard_D4s_v5"
#   subnet_key  = "app"
#   priority    = "Regular"
#   node_taints = []
#   min_count   = 1
# }

# 2. Plan and apply
terraform plan
terraform apply
```

#### Update Helm Values Schema

```bash
# 1. Edit CUE template
vim templates/values.cue

# 2. Add new fields to schema or logic

# 3. Regenerate values
make validate-cue  # Validate first
make generate-values

# 4. Commit and push
git add templates/values.cue generated/values.yaml
git commit -m "feat(values): add new configuration field"
git push
```

#### Troubleshoot Module Errors

```bash
# Check module versions
terraform version
terraform providers

# Update module version
# Edit main.tf:
# version = "1.3.32"

# Refresh lock file
terraform init -upgrade

# Apply
terraform apply
```

---

### Troubleshooting Guide

#### Issue: "Workspace not found"

Symptom: Terraform Cloud error during `terraform init`

Cause: `providers.tf` workspace name doesn't match TFC

Solution:

```bash
# Check deployment_key
terraform console
> local.deployment_key

# Regenerate providers.tf
make generate-providers

# Verify workspace exists in TFC UI
# Organization: FITFILE-Platforms
# Project: NWSDE
# Workspace: lca-prd-2
```

#### Issue: "CIDR Overlap detected"

Symptom: Azure error during VNet creation

Cause: Subnet CIDR conflicts with existing network

Solution:

```bash
# 1. Check existing networks
az network vnet list -g rg-lca-uks-prd-net -o table

# 2. Update vnet_address_space in customer.yaml
vim config/customer.yaml
# Use non-overlapping CIDR

# 3. Reapply
terraform apply
```

#### Issue: "Module `central_services` admin_password cycle"

Symptom: Terraform plan shows cyclic dependency

Cause: `private-infrastructure` needs password before `central_services` completes

Solution:

This should not occur with current design. If it does:

```bash
# Apply in stages
terraform apply -target=module.central_services
terraform apply -target=module.private-infrastructure
terraform apply
```

#### Issue: "VSO Cannot Authenticate to Vault"

Symptom: Pods show "VaultAuthGlobalRef invalid" errors

Cause: JWT auth not configured or OIDC issuer mismatch

Solution:

```bash
# 1. Verify JWT auth exists
vault auth list | grep jwt-lca-prd-2

# 2. Check OIDC issuer URL matches
vault read auth/jwt-lca-prd-2/config

# 3. Verify role
vault read auth/jwt-lca-prd-2/role/lca-prd-2

# 4. Test authentication from pod
kubectl exec -it <vso-pod> -n lca-prd-2 -- sh
# Get service account token
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
# Test Vault login
vault write auth/jwt-lca-prd-2/login role=lca-prd-2 jwt=$TOKEN
```

#### Issue: "ArgoCD Cannot Clone GitLab repository"

Symptom: ArgoCD Application shows "failed to checkout" error

Cause: SSH key not configured or wrong URL

Solution:

```bash
# 1. Verify GitLab project URL
terraform output gitlab_project_ssh_url

# 2. Check ArgoCD secret
kubectl get secret argocd-group-creds -n argocd -o yaml

# 3. Verify SSH key has access
# In GitLab UI: Project → Settings → Repository → Deploy Keys

# 4. Test SSH connection from jumpbox
ssh -T git@gitlab.com
```

#### Issue: "CUE Validation fails"

Symptom: `make generate-values` fails with schema error

Cause: `infra_facts` structure doesn't match CUE schema

Solution:

```bash
# 1. Check Terraform output
terraform output -json infra_facts | jq

# 2. Compare with CUE schema
cat templates/values.cue | grep -A 10 "#InfraFacts"

# 3. Update CUE schema or values_generator.tf to match

# 4. Validate manually
INFRA_JSON=$(terraform output -json infra_facts | jq -c '.value')
cue vet ./templates/values.cue -t "infra=$INFRA_JSON"
```

#### Issue: "Jumpbox SSH Connection refused"

Symptom: Cannot connect to jumpbox via Bastion

Cause: NSG rules blocking, VM not running, or password incorrect

Solution:

```bash
# 1. Check VM status
az vm show -n vmlcajmp01 -g rg-lca-uks-prd-net --query powerState

# 2. Start VM if stopped
az vm start -n vmlcajmp01 -g rg-lca-uks-prd-net

# 3. Verify Bastion is running
az network bastion show -n bastion-lca-plat-uks-01 -g rg-lca-uks-prd-net

# 4. Get VM password from Vault
vault kv get deployments/lca-prd-2/secrets/application | grep vm_admin_password

# 5. Connect via Bastion from Azure Portal
```

#### Issue: "NAT Gateway not Routing traffic"

Symptom: Pods cannot reach internet

Cause: NAT Gateway association missing or misconfigured

Solution:

```bash
# 1. Check NAT Gateway associations
az network vnet subnet show \
  -g rg-lca-uks-prd-net \
  -n snet-lca-uks-prd-system \
  --vnet-name vnet-lca-plat-uks-01 \
  --query natGateway

# 2. Verify NAT Gateway exists
az network nat gateway show \
  -g rg-lca-uks-prd-net \
  -n nat-lca-plat-uks-01

# 3. Check public IP
az network public-ip show \
  -g rg-lca-uks-prd-net \
  -n pip-nat-lca-plat-uks-01

# 4. Re-associate if needed
az network vnet subnet update \
  -g rg-lca-uks-prd-net \
  -n snet-lca-uks-prd-system \
  --vnet-name vnet-lca-plat-uks-01 \
  --nat-gateway nat-lca-plat-uks-01
```

---

### Quick Reference Cards

#### Command Cheat Sheet

```bash
# Configuration
make help                    # Show all make targets
vim config/customer.yaml     # Edit customer config

# Generation
make generate-providers      # Generate providers.tf
make generate-values         # Generate Helm values.yaml
make validate-cue            # Validate CUE without generating

# Terraform Operations
terraform init               # Initialize (connects to TFC)
terraform plan               # Preview changes
terraform apply              # Apply changes
terraform output             # Show all outputs
terraform output -raw <name> # Show specific output

# State Management
terraform state list         # List all resources
terraform state show <resource> # Show resource details
terraform refresh            # Sync state with reality

# Jumpbox
./scripts/connect-jumpbox.sh # Connect to jumpbox via Bastion
terraform output -raw jumpbox_main_content > main.tf  # Extract jumpbox config

# Validation
./scripts/validate-vault-paths.sh  # Check Vault config
./scripts/verify_argocd.sh         # Check ArgoCD status

# Cleanup
make clean                   # Remove generated files
terraform destroy            # Destroy all infrastructure (USE WITH CAUTION)
```

#### File Locations Quick Map

```
config/customer.yaml              → Customer configuration (EDIT THIS)
locals.tf                         → Transformation logic (READ THIS)
main.tf                           → Module orchestration
templates/values.cue              → Helm values schema
generated/values.yaml             → Generated Helm values (COMMIT THIS)
generated/main.tf                 → Jumpbox Terraform (COPY TO JUMPBOX)
providers.tf                      → TFC backend config
secrets.auto.tfvars.json          → Secrets (NEVER COMMIT)
docs/LCA_DP_CONTEXT.md            → Data flow documentation
docs/PROJECT_BRAIN.md             → Architectural overview
```

#### Module Version Matrix

| Module | Version | Source | Purpose |
|--------|---------|--------|---------|
| central-services-consumer | 1.0.4 | TFC Private Registry | SaaS platform services |
| private-infrastructure | 1.3.31 | TFC Private Registry | Azure infrastructure |

#### Provider Version Matrix

| Provider | Version | Purpose |
|----------|---------|---------|
| azurerm | 4.53.0 | Azure resources |
| gitlab | >= 16.0.0 | GitLab API |
| auth0 | >= 1.0.0 | Auth0 configuration |
| tfe | >= 0.50.0 | Terraform Cloud |
| vault | >= 3.0.0 | HCP Vault |
| grafana | >= 2.0.0 | Grafana Cloud |
| cloudflare | >= 4.0.0 | Cloudflare DNS |

---

### Summary

This repository is a GitOps-driven, template-based infrastructure-as-code system that:

1. Centralizes Configuration: All customer-specific values in `config/customer.yaml`
2. Automates Derivation: `locals.tf` calculates all dependent values
3. Orchestrates Modules: Two main modules handle SaaS services and Azure infrastructure
4. Generates Artifacts: Templates produce jumpbox config and Helm values
5. Manages Secrets: HCP Vault with JWT authentication via OIDC
6. Deploys Applications: ArgoCD with Vault Secrets Operator for secret injection

Key Design Principles:

- Single source of truth (customer.yaml)
- No hardcoded values
- Consistent naming conventions
- Automated secret generation
- Infrastructure as code
- GitOps workflows

For LLM Assistants: When working with this codebase:

1. Always reference `config/customer.yaml` for customer-specific values
2. Use `locals.tf` to derive new values (never hardcode)
3. Follow existing naming conventions in `locals.tf`
4. Understand the two-module architecture
5. Respect the data flow pipeline
6. Maintain separation between generated and source files
7. Use Makefile targets for common operations
8. Validate changes with `terraform plan` before applying

---

End of Context Document
