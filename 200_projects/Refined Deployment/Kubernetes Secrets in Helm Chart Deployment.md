---
aliases: []
confidence: 
created: 2025-08-22T08:57:28Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:12Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [config, helm, secrets, topic/technology/kubernetes]
title: Kubernetes Secrets in Helm Chart Deployment
type:
uid: 
updated: 
version:
---

## **Primary Secret Locations**

### **1. Shared Secrets Chart (`charts/shared-secrets/templates/`)**

This is the central location for shared secrets across the deployment:

- **[acr-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/shared-secrets/templates/acr-secret.yaml:0:0-0:0)** - Azure Container Registry credentials for image pulling
- **[mongodb-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/shared-secrets/templates/mongodb-secret.yaml:0:0-0:0)** - MongoDB connection details (username, password, host, URIs)
- **[postgresql-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/shared-secrets/templates/postgresql-secret.yaml:0:0-0:0)** - PostgreSQL database credentials and connection strings
- **[sleuth-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/shared-secrets/templates/sleuth-secret.yaml:0:0-0:0)** - Sleuth API key for monitoring/observability

### **2. Application-Specific Secrets**

- **[charts/hutch/templates/bunny-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/hutch/templates/bunny-secret.yaml:0:0-0:0)** - Database and task API authentication for Hutch service
- **[charts/hutch/templates/relay-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/hutch/templates/relay-secret.yaml:0:0-0:0)** - Relay service credentials
- **[charts/integrations/thehyve/templates/secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/secret.yaml:0:0-0:0)** - TheHyve integration secrets
- **[charts/mutating-proxy-webhook/templates/secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/mutating-proxy-webhook/templates/secret.yaml:0:0-0:0)** - Webhook authentication

### **3. Environment-Specific Secrets**

- **[ffnodes/kch/prod/templates/vault-replacement-secrets.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/kch/prod/templates/vault-replacement-secrets.yaml:0:0-0:0)** - Production KCH environment secrets (hardcoded values including MongoDB, PostgreSQL, Auth0, certificates)
- **[ffnodes/stg/sandbox/templates/vault-replacement-secrets.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/stg/sandbox/templates/vault-replacement-secrets.yaml:0:0-0:0)** - Staging environment secrets

### **4. Integration Test Secrets**

- **[workflows/integration-tests/charts/emis/templates/postgres-daemon-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/workflows/integration-tests/charts/emis/templates/postgres-daemon-secret.yaml:0:0-0:0)** - Test database credentials
- **[workflows/integration-tests/charts/integration-test-tools/templates/create-secret.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/workflows/integration-tests/charts/integration-test-tools/templates/create-secret.yaml:0:0-0:0)** - Test tooling secrets

## **Secret Configuration Sources**

Secrets are configured through:

- **Values files** - Most secrets reference `.Values.global.sharedSecrets.*` from values.yaml files
- **Hardcoded values** - Some environments (like KCH prod) have base64-encoded secrets directly in templates
- **External secret references** - Some charts support `existingSecretName` to reference externally managed secrets

## **Key Patterns**

1. **Shared secrets** use helper templates like `{{ include "shared-secret.mongodb" . }}`
2. **Base64 encoding** is handled via `| b64enc` filters
3. **Conditional creation** using `{{- if }}` blocks to avoid creating unnecessary secrets
4. **URI construction** for database connections combining username, password, host, and connection parameters

The secrets cover authentication for databases (MongoDB, PostgreSQL), container registries (ACR), message queues (RabbitMQ), OAuth providers (Auth0), and various service integrations.

## Kubernetes Secrets in Private Platform Template

I've found additional secret definitions in the **private_platform_template** folder. This Terraform-based infrastructure uses a different approach for secret management compared to the Helm charts.

### **Terraform-Managed Secrets**

#### **1. HashiCorp Vault AppRole Secrets ([main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/main.tf:0:0-0:0))**

The main configuration defines **AppRole authentication secrets** for different services:

- **`argocd`** - ArgoCD service authentication (namespace: `argocd`, secret: `role-secrets`)
- **`application`** - Main application authentication (namespace: deployment key, secret: `role-secrets`)
- **`spicedb`** - SpiceDB service authentication (namespace: `spicedb`, secret: `role-secrets`)
- **`argoWorkflows`** - Argo Workflows authentication (namespace: `argo`, secret: `role-secrets`)
- **`monitoring`** - Monitoring services authentication (namespace: `monitoring`, secret: `role-secrets`)

#### **2. Kubernetes Secret Resources ([.terraform/modules/platform/vault_operator/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/main.tf:0:0-0:0))**

Creates actual Kubernetes secrets via Terraform:

```hcl
resource "kubernetes_secret" "ns_approle_secrets" {
  for_each = var.app_role_secrets_map

  metadata {
    namespace = each.value.namespace
    name      = each.value.secret_name
  }

  data = tomap({
    role_id = each.value.role_id
    id      = each.value.secret_id
  })
}
```

#### **3. Vault Dynamic Secrets (Template Files)**

- **[acr_dynamic_secret.tftpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/acr_dynamic_secret.tftpl:0:0-0:0)** - Azure Container Registry pull secrets for ArgoCD
- **[default_image_pull_secret.tftpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/default_image_pull_secret.tftpl:0:0-0:0)** - Default Docker registry credentials with Reflector annotations for cross-namespace replication
- **[vault_auth.tftpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/vault_auth.tftpl:0:0-0:0)** - VaultAuth CRD configuration for Vault Secrets Operator

### **Key Differences from Helm Charts**

1. **Vault Integration** - Uses HashiCorp Vault Secrets Operator for dynamic secret management
2. **AppRole Authentication** - Leverages Vault AppRole method for service authentication
3. **Secret Reflection** - Uses Reflector to automatically replicate image pull secrets across namespaces
4. **Infrastructure as Code** - Secrets are managed through Terraform rather than Helm values

### **Secret Types Managed**

- **Vault AppRole credentials** (role_id, secret_id)
- **Azure Container Registry authentication**
- **Docker image pull secrets** with automatic namespace replication
- **TLS certificates** (referenced in ArgoCD ingress configuration)

The private platform template represents a more enterprise-grade approach to secret management, using Vault for centralized secret storage and dynamic credential generation, while the Helm charts use more traditional static secret definitions.

## PKI Certificate Integration Complete

I've successfully aligned the repos to integrate deployment-specific PKI certificates from your Vault setup into the private_platform_template. Here's what was implemented:

### **Key Changes Made**

#### **HCP Vault Configuration**

- **Added deployment-specific PKI policies** in [policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/policies.tf:0:0-0:0) - Each deployment gets its own policy for certificate issuance
- **Updated GitOps AppRole permissions** in [identities.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/identities.tf:0:0-0:0) - Added PKI certificate access to the `gitops-operator-ro` role

#### **Private Platform Template**

- **Created certificate templates**:
  - [deployment_tls_cert.tftpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/deployment_tls_cert.tftpl:0:0-0:0) - General deployment certificates with Reflector distribution
  - [cloudflare_tls_cert.tftpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/cloudflare_tls_cert.tftpl:0:0-0:0) - ArgoCD-specific certificates
- **Updated Terraform modules** to pass deployment_key and argocd_host variables
- **Added VaultDynamicSecret resources** for automatic certificate provisioning

### **How It Works**

1. **Per-deployment certificates** issued from `pki_int_{deployment}` intermediate CAs
2. **Automatic renewal** every 75 days (before 90-day expiry)
3. **Cross-namespace distribution** via Reflector annotations
4. **Standard Kubernetes TLS secrets** ready for ingress use

### **For CUH-PROD-1 Specifically**

The system will create:

- Certificate from `pki_int_cuh-prod-1` intermediate CA
- Domains: `cuh-prod-1.fitfile.net`, `*.cuh-prod-1.fitfile.net`
- Secrets: `cuh-prod-1-tls-cert` and `cloudflare-tls`
- Policy: `cuh-prod-1-pki-cert-policy`

### **Next Steps**

1. **Apply Vault changes**: `terraform apply` in [central-services/hcp/vault/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault:0:0-0:0)
2. **Deploy updated platform template** with the new certificate integration
3. **Verify certificate issuance** and cross-namespace distribution
4. **Update ingress configurations** to reference the new certificate secrets

The integration maintains your existing PKI hierarchy while automating certificate distribution to each deployment cluster via the Vault Secrets Operator.

## PKI Certificate Integration Guide

This document explains how the PKI certificate system integrates between the HCP Vault configuration and the private platform template deployments.

### Overview

The system automatically provisions deployment-specific TLS certificates using HashiCorp Vault's PKI secrets engine and distributes them to Kubernetes clusters via the Vault Secrets Operator (VSO).

### Architecture

#### Vault PKI Structure

- **Root CA**: `pki_root` - Central root certificate authority
- **Intermediate CAs**: `pki_int_{deployment}` - Per-deployment intermediate CAs
- **Certificate Roles**: `{deployment}-server` - Roles for issuing certificates

#### Certificate Distribution

- **VaultDynamicSecret CRDs**: Automatically request and renew certificates
- **Reflector**: Distributes certificates across namespaces
- **Kubernetes TLS Secrets**: Standard format for ingress controllers

### Deployment-Specific Configuration

For each deployment (e.g., `cuh-prod-1`), the system creates:

1. **Intermediate CA**: `pki_int_cuh-prod-1`
2. **Certificate Role**: `cuh-prod-1-server`
3. **Allowed Domains**: `cuh-prod-1.fitfile.net`, `*.cuh-prod-1.fitfile.net`
4. **Vault Policy**: `cuh-prod-1-pki-cert-policy`

### Generated Certificates

#### 1. Deployment TLS Certificate

- **Name**: `{deployment-key}-tls-cert`
- **Namespace**: `cert-manager`
- **Common Name**: `{deployment-key}.fitfile.net`
- **Alt Names**: `*.{deployment-key}.fitfile.net`
- **Reflection**: Distributed to all namespaces

#### 2. ArgoCD TLS Certificate

- **Name**: `cloudflare-tls`
- **Namespace**: `argocd`
- **Common Name**: ArgoCD host (e.g., `cuh-prod-1-argocd.fitfile.net`)
- **Usage**: ArgoCD ingress TLS termination

### Certificate Lifecycle

- **Initial Issue**: 90 days (2160h)
- **Renewal**: 75 days (1800h) - automatic renewal before expiry
- **Rotation**: Automatic restart of dependent deployments

### Vault Policies

Each deployment gets a dedicated policy allowing:

- Certificate issuance from its intermediate CA
- CA certificate reading
- Lease management for renewals

```hcl
path "pki_int_{deployment}/issue/{deployment}-server" {
capabilities = ["create", "update"]
}
```

### Usage in Helm Charts

Certificates are available as standard Kubernetes TLS secrets:

```yaml
spec:
tls:
  - secretName: cuh-prod-1-tls-cert
hosts:
  - cuh-prod-1.fitfile.net
  - "*.cuh-prod-1.fitfile.net"
```

### Troubleshooting

#### Certificate Not Issued

1. Check VaultAuth CRD status: `kubectl get vaultauth -A`
2. Verify VSO logs: `kubectl logs -n vault-secrets-operator-system`
3. Confirm Vault policy permissions

#### Certificate Not Renewed

1. Check VaultDynamicSecret status: `kubectl get vaultdynamicsecret -A`
2. Verify lease TTL in Vault UI
3. Check VSO renewal logs

#### Cross-Namespace Issues

1. Verify Reflector is running: `kubectl get pods -n reflector-system`
2. Check reflection annotations on source secret
3. Confirm target namespace exists

### Files Modified

#### HCP Vault (`central-services/hcp/vault/`)

- `policies.tf` - Added deployment-specific PKI policies
- `identities.tf` - Updated GitOps roles with PKI permissions

#### Private Platform Template

- `vault_operator/deployment_tls_cert.tftpl` - Deployment certificate template
- `vault_operator/cloudflare_tls_cert.tftpl` - ArgoCD certificate template
- `vault_operator/main.tf` - Added certificate resource creation
- `vault_operator/variables.tf` - Added deployment_key and argocd_host variables
- `platform/variables.tf` - Added platform-level variables
- `platform/main.tf` - Pass variables to vault_operator module

### Next Steps

1. Apply Vault configuration: `terraform apply` in `central-services/hcp/vault/`
2. Deploy platform template with new certificate integration
3. Verify certificates are issued and distributed correctly
4. Update ingress configurations to use new certificate secrets

Looking at the code, Kubernetes is configured to use HCP Vault for secret population through the **Vault Secrets Operator (VSO)** in several key places:

## Kubernetes HCP Vault Integration Configuration

Kubernetes is configured to use HCP Vault for secret population through the **Vault Secrets Operator (VSO)** in these key locations:

### **1. Vault Secrets Operator Deployment**

**File**: [.terraform/modules/platform/vault_operator/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/vault_operator/main.tf:0:0-0:0)

The VSO is deployed as a Helm chart with Vault connection configuration:

```hcl
resource "helm_release" "vso_helm_release" {
  name             = "vault-secrets-operator"
  namespace        = "vault-secrets-operator-system"
  chart            = "helm/vault-secrets-operator"
  repository       = "oci://fitfilepublic.azurecr.io"

  set {
    name  = "defaultVaultConnection.enabled"
    value = "true"
  }

  set {
    name  = "defaultVaultConnection.address"
    value = var.vault_address  # HCP Vault address
  }
}
```

### **2. AppRole Authentication Secrets**

**File**: Same file, lines 1-16

Kubernetes secrets containing Vault AppRole credentials for authentication:

```hcl
resource "kubernetes_secret" "ns_approle_secrets" {
  for_each = var.app_role_secrets_map

  data = tomap({
    role_id = each.value.role_id
    id      = each.value.secret_id  # AppRole secret_id
  })
}
```

### **3. VaultAuth CRDs**

**File**: Lines 90-96

Custom resources that configure Vault authentication per namespace:

```hcl
resource "kubectl_manifest" "acr_pull_vault_auth" {
  for_each = var.app_role_secrets_map

  yaml_body = templatefile("${path.module}/vault_auth.tftpl", each.value)
}
```

### **4. VaultDynamicSecret CRDs**

**File**: Lines 98-145

Custom resources that define which secrets to pull from Vault:

- **ACR credentials**: `acr_pull_vault_dynamic_secret`
- **Image pull secrets**: `docker_pull_vault_dynamic_secret`
- **PKI certificates**: `deployment_tls_cert` and `cloudflare_tls_cert`

### **5. Vault Connection Flow**

1. **VSO connects** to HCP Vault using the configured address
2. **Authenticates** using AppRole method with role_id/secret_id from Kubernetes secrets
3. **Reads VaultAuth CRDs** to understand authentication per namespace
4. **Processes VaultDynamicSecret CRDs** to fetch secrets from Vault
5. **Creates/updates** standard Kubernetes secrets with the fetched data
6. **Automatically renews** secrets based on TTL and refresh intervals

The configuration is passed down from [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/main.tf:0:0-0:0) → `platform module` → `vault_operator module` with the HCP Vault address and AppRole credentials.
