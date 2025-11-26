---
aliases: []
confidence:
created: 2025-11-25T14:27:21Z
epistemic:
last_reviewed:
modified: 2025-11-25T14:27:39Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags:
  - nnuh
title: FITFILE Platform Module - Complete Analysis
type:
uid:
updated:
---

## Overview

The [terraform-helm-fitfile-platform](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform:0:0-0:0) module is the **core platform infrastructure** that deploys all essential Kubernetes components needed to run FITFILE applications. It's consumed by the NNUH-Platform terraform you'll run from the jumpbox.

## Architecture & Deployment Order

The module deploys components in a specific dependency order:

```sh
1. Namespaces Creation
   ↓
2. Vault Secrets Operator (VSO) + Reflector (parallel)
   ↓
3. Ingress NGINX Controller
   ↓
4. ArgoCD + ArgoCD Applications
   ↓
5. Cluster Autoscaler (AWS only)
```

## Core Components Deployed

### 1. **Vault Secrets Operator (VSO)**
**Purpose**: Integrates Kubernetes with HCP Vault for secrets management

**What it does**:
- Deploys VSO Helm chart to `vault-secrets-operator-system` namespace
- Creates AppRole secrets in each namespace (argocd, application, spicedb, argo-workflows, monitoring)
- Sets up VaultAuth CRDs for each namespace to authenticate with Vault
- Creates dynamic secrets for ACR image pull authentication
- Enables automatic secret injection from Vault into Kubernetes

**Key Configuration**:

```hcl
vault_address = "https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/"
app_role_secrets_map = {
  argocd = { role_id, secret_id, vault_namespace }
  application = { ... }
  argo-workflows = { ... }
  spicedb = { ... }
  monitoring = { ... }
}
```

### 2. **Reflector**
**Purpose**: Replicates secrets and configmaps across namespaces

**What it does**:
- Watches for secrets/configmaps with special annotations
- Automatically copies them to other namespaces
- Useful for TLS certificates, shared credentials, etc.

**Chart Version**: `7.1.288` (default)

### 3. **Ingress NGINX Controller**
**Purpose**: Provides HTTP/HTTPS ingress to cluster services

**What it does**:
- Deploys NGINX ingress controller
- Creates internal load balancer (for private clusters)
- Binds to specified IP address (`10.0.1.10` typically)
- Handles TLS termination and routing

**Key Configuration**:

```hcl
ingress_ip_address = "10.0.1.10"
ingress_load_balancer_type = "internal"  # No public exposure
```

**Chart Version**: `4.12.1` (default)

### 4. **ArgoCD**
**Purpose**: GitOps continuous deployment platform

**What it does**:
- Deploys ArgoCD server and controllers
- Creates ingress for ArgoCD UI (accessible at `argocd_host`)
- Deploys ArgoCD Applications that point to your GitLab repo
- Automatically syncs Helm charts from GitLab to cluster
- Manages application lifecycle through GitOps

**Key Configuration**:

```hcl
argocd_host = "argocd.nnuh-prod.internal"
argocd_applications = [{
  name = "ff-nnuh-prod"
  target_revision = "master"
  source = {
    release_name = "nnuh-prod"
    value_files = ["ffnodes/eoe/nnuh-prod/values.yaml"]
  }
}]
```

**Chart Versions**:
- ArgoCD: `7.8.8` (default)
- ArgoCD Apps: `1.4.1` (default)

### 5. **Cluster Autoscaler** (AWS Only)
**Purpose**: Automatically scales cluster nodes based on workload

**What it does**:
- Only deployed when `cloud_provider = "AWS"`
- Not used for Azure AKS (Azure has built-in autoscaling)
- Monitors pod scheduling and scales nodes up/down

**Chart Version**: `9.43.0` (default)

## Namespace Management

The module automatically creates and manages namespaces:

**Core Namespaces**:
- `vault-secrets-operator-system` - VSO components
- [argocd](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform/argocd:0:0-0:0) - ArgoCD server and controllers
- `ingress-nginx` - Ingress controller
- `argo` - Argo Workflows
- `cert-manager` - Certificate management
- `spicedb` - Authorization service
- `monitoring` - Monitoring stack
- `<deployment_key>` - Your application namespace (e.g., "nnuh-prod")

**Features**:
- All namespaces labeled with `managedBy = "terraform"`
- Default service accounts configured with image pull secrets
- ACR authentication automatically injected

## Image Pull Secret Management

**Purpose**: Enables pulling images from private Azure Container Registry

**What it does**:
1. VSO creates a VaultDynamicSecret that fetches ACR credentials from Vault
2. Credentials automatically rotated and synced to Kubernetes secret `fitfile-image-pull-secret`
3. Secret replicated to all namespaces via Reflector
4. Default service accounts configured to use the secret

**Configuration**:

```hcl
use_image_pull_secret = true  # Enable ACR authentication
```

## Helm Chart Repository

All charts are pulled from the FITFILE Azure Container Registry:

```hcl
helm_repository_url = "oci://fitfilepublic.azurecr.io"
```

This ensures:

- Version-controlled chart deployments
- No external dependencies on public Helm repos
- Consistent chart versions across environments

## Key Variables You Need to Provide

### Required Variables
1. **AKS Cluster Credentials** (from NNUH-DP outputs):
   - `aks_cluster_host`
   - `aks_cluster_client_certificate`
   - `aks_cluster_client_key`
   - `aks_cluster_ca_certificate`

2. **Network Configuration**:
   - `ingress_controller_ip_address` - Static IP for ingress (e.g., `10.0.1.10`)

3. **Vault Configuration**:
   - `vault_address` - HCP Vault URL (already set to default)
   - `app_role_secrets_map` - AppRole credentials for 5 services

4. **ArgoCD Configuration**:
   - `argocd_host` - DNS name for ArgoCD UI
   - `argocd_applications` - Application definitions pointing to GitLab

5. **Deployment Metadata**:
   - `deployment_key` - Unique identifier (e.g., "NNUH-PROD")
   - `deployment_repo_values_file_path` - Path to Helm values in GitLab

### Optional Variables with Defaults
- Chart versions (all have sensible defaults)
- `ingress_load_balancer_type = "internal"` (good for private clusters)
- `use_image_pull_secret = true` (needed for ACR)
- `argocd_sso.enabled = false` (SSO disabled by default)

## What Happens After Deployment

1. **VSO authenticates to Vault** using AppRole credentials
2. **Secrets are synced** from Vault to Kubernetes
3. **Ingress controller starts** and binds to internal IP
4. **ArgoCD deploys** and becomes accessible at `argocd_host`
5. **ArgoCD syncs your application** from GitLab automatically
6. **Application pods start** with ACR authentication working

## Security Features

- **No public endpoints** - Internal load balancer only
- **Vault integration** - All secrets stored in Vault, not in Git
- **AppRole authentication** - Service-specific Vault access
- **Automatic credential rotation** - VSO handles secret updates
- **TLS everywhere** - Ingress handles TLS termination
- **RBAC** - Kubernetes RBAC enforced throughout

## Troubleshooting from Jumpbox

Once deployed, you can verify components:

```bash
# Check all pods are running
kubectl get pods -A

# Check VSO is working
kubectl get vaultauth -A
kubectl get vaultdynamicsecret -A

# Check ArgoCD applications
kubectl get applications -n argocd

# Access ArgoCD UI (port-forward)
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## Summary

This module is the **foundation** of your FITFILE deployment. It:

- ✅ Connects Kubernetes to Vault for secrets
- ✅ Provides ingress for external access
- ✅ Sets up GitOps with ArgoCD
- ✅ Handles ACR authentication automatically
- ✅ Creates all necessary namespaces
- ✅ Configures internal networking

Once this is deployed from the jumpbox, ArgoCD will take over and deploy your actual FITFILE application based on the values file in GitLab.
