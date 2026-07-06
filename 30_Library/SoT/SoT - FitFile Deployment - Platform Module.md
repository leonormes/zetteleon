---
aliases: [FITFILE Platform Deployment]
created: 2026-02-01T19:26:00+00:00
modified: 2026-07-04T10:50:58+00:00
permalink: llmeon/30-library/so-t/so-t-fit-file-deployment-platform-module
status: active
tags: [deployment, ff_deploy, kubernetes, SoT, terraform]
title: SoT - FitFile Deployment - Platform Module
type: SoT
---

## Source of Truth: FitFile Platform Deployment

### Minimum Viable Understanding (MVU)

The FITFILE Platform Terraform Module (`terraform-helm-fitfile-platform`) is the canonical infrastructure-as-code (IaC) solution for deploying the FITFILE Kubernetes platform. It orchestrates the deployment of essential cluster components—Ingress, GitOps (ArgoCD), Secrets (Vault), and Monitoring—in a strict dependency order. It serves as the bridge between raw infrastructure (Azure/AWS) and application workloads.

### Core Architecture

The module employs a dependency-driven architecture to ensure a stable platform foundation. Components are deployed in the following sequence:

```mermaid
graph TD
    A[Namespaces] --> B[Vault Secrets Operator]
    A --> C[Reflector]
    B --> D[NGINX Ingress Controller]
    C --> D
    D --> E[ArgoCD]
    A --> F[Cluster Autoscaler (AWS Only)]
```

#### 1. Vault Secrets Operator (VSO)

- Purpose: Bridges HashiCorp Vault with Kubernetes for secure secret injection.
- Function: Authenticates via AppRole, synchronizes secrets to native Kubernetes `Secret` resources, and manages dynamic secrets (e.g., ACR credentials).
- Key Config: Configured via `vso_helm_values`. Requires valid `app_role_secrets_map`.

#### 2. Reflector

- Purpose: Information radiator for secrets and ConfigMaps.
- Function: Automatically mirrors secrets (like image pull secrets or TLS certificates) across namespaces based on annotations.
- Dependency: Essential for distributing the `fitfile-image-pull-secret` to application namespaces.

#### 3. NGINX Ingress Controller

- Purpose: The cluster's traffic gateway.
- Function: Provides HTTP/HTTPS load balancing and TLS termination.
- Configuration: Typically configured with an Internal Load Balancer (`ingress_load_balancer_type = "internal"`) for private clusters.
- Hard Constraint: Requires VSO and Reflector to be healthy first.

#### 4. ArgoCD (GitOps)

- Purpose: The Continuous Delivery engine.
- Function: Syncs application state from the GitLab Helm Chart Repository to the cluster.
- Workflow: Once deployed, ArgoCD takes over the lifecycle management of business applications (`ffnode`, etc.).
- Configuration: Custom applications defined in `argocd_applications`.

#### 5. Cluster Autoscaler

- Purpose: Dynamic resource elasticity.
- Condition: Deployed only when `cloud_provider = "AWS"`. (Azure AKS manages this natively).

### Implementation & Configuration

#### Module Usage (v2.0.0+)

Version 2.0.0 enforces strict version pinning for stability.

```hcl
module "platform" {
  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
  version = "2.0.0"

  # Core Networking
  ingress_ip_address = "10.0.1.100" # Static IP from Infrastructure outputs
  argocd_host        = "argocd.fitfile.com"

  # Component Version Pinning (Mandatory)
  ingress_nginx_chart_version      = "4.12.1"
  argocd_chart_version            = "7.8.8"
  argocd_apps_chart_version       = "1.4.1"
  vault_operator_chart_version    = "0.8.1"
  reflector_chart_version         = "7.1.288"
  cluster_autoscaler_chart_version = "9.43.0"
  helm_repository_url            = "oci://fitfilepublic.azurecr.io"

  # Vault Integration
  vault_address = "https://vault.example.com:8200/"
  app_role_secrets_map = {
    argocd = {
      namespace       = "argocd"
      secret_name     = "vault-secret"
      role_id         = "var.vault_role_id"
      secret_id       = "var.vault_secret_id"
      vault_namespace = "admin"
      vault_backend   = "secret"
    }
  }

  cloud_provider = "AZURE"
}
```

#### Security & Secret Management Flow

1. Auth: VSO authenticates to Vault using AppRole credentials.
2. Sync: Secrets (ACR credentials, PKI certs) are pulled into the `vault-secrets-operator-system` namespace.
3. Distribution: Reflector detects annotated secrets and copies them to application namespaces.
4. Consumption: Pods use these secrets for image pulling and configuration injection.

### Troubleshooting & Operations

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Chart Version Missing | `Error: Chart version not found` | Verify `_chart_version` variables match available charts in `oci://fitfilepublic.azurecr.io`. |
| Ingress Pending | `LoadBalancer IP not assigned` | Ensure `ingress_ip_address` is valid and not in use within the subnet. |
| Vault Auth Fail | `Failed to authenticate` | Validate `app_role_secrets_map` IDs against Vault. Check Vault reachability. |

#### Verification Commands (Jumpbox)

```bash
# 1. Check Platform Health
kubectl get pods -n vault-secrets-operator-system
kubectl get pods -n ingress-nginx
kubectl get pods -n argocd

# 2. Verify Secret Sync
kubectl get vaultauth -A
kubectl get vaultdynamicsecret -A

# 3. Access ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Key Repositories

- Platform Module: `TFC-Modules/terraform-helm-fitfile-platform`
- Deployment Template: `private_platform_template`
- Vault Config: `central-services/hcp/vault`
