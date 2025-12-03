---
aliases: []
confidence: 
created: 2025-11-27T09:38:40Z
epistemic: 
last_reviewed: 
modified: 2025-11-27T10:04:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE_Platform_Wiki
type: 
uid: 
updated: 
---

## FITFILE Platform Terraform Module Analysis & Documentation

### 1. Analysis of Current Implementation

#### Overview

The `terraform-helm-fitfile-platform` module acts as a "platform-in-a-box" installer, orchestrating several key Kubernetes components:

- **Vault Secrets Operator (VSO)** & **Reflector** for secret management.
- **NGINX Ingress Controller** for traffic management.
- **ArgoCD** for GitOps.
- **Cluster Autoscaler** (AWS only).

#### Strengths
- **Opinionated & Standardized**: Enforces a specific architecture (VSO -> Reflector -> Ingress -> ArgoCD), ensuring all clusters look similar.
- **Version Controlled**: Strict version pinning for all Helm charts prevents drift and accidental upgrades.
- **Simplified Consumption**: Consumers only need to provide a few high-level variables (IP, hostnames, Vault auth) to get a full platform.
- **Cloud Agnostic (mostly)**: Abstracts some differences between AWS and Azure.

#### Weaknesses & Flexibility Bottlenecks
- **Rigid Dependencies**: The `depends_on` chains are hardcoded. For example, `ingress_controller` depends on `vault_operator`, meaning you can't easily deploy Ingress without Vault.
- **All-or-Nothing Deployment**: There are no feature flags (e.g., `enable_argocd = false`). You get the whole platform or nothing.
- **Hardcoded Configuration**:
    - `ingress_nginx` submodule has hardcoded `set` blocks for things like `enable-ssl-passthrough` and specific header sizes. Overriding these via `helm_values` can be tricky or impossible if the logic conflicts.
    - `cluster_autoscaler` is strictly tied to `var.cloud_provider == "AWS"`.
- **Boolean Flags**: `use_image_pull_secret` is a simple boolean, but advanced users might want more granular control over *which* secrets to create.

---

### 2. Suggestions for Improvement (Best Practices)

To increase flexibility without sacrificing standardization, consider the following refactoring steps:

#### A. Feature Flags (Component Toggles)

Introduce boolean variables to enable/disable components. This allows the module to be used in environments where some components might already exist or aren't needed.

```hcl
variable "enable_argocd" {
  description = "Enable ArgoCD deployment"
  type        = bool
  default     = true
}

module "argocd" {
  count  = var.enable_argocd ? 1 : 0
  source = "./argocd"
  # ...
}
```

#### B. Decouple Dependencies

Remove strict `depends_on` where possible. If `ingress_nginx` needs a secret from `vault_operator`, use `data` sources or implicit dependencies. If explicit dependency is needed, make it conditional or allow passing in dependency IDs.

#### C. Generic Helm Values Override

While `helm_values` variables exist, ensure they take precedence. In submodules, prefer merging user-provided `values` YAML over hardcoded `set` blocks where possible.

-   **Best Practice**: Use `values = [yamlencode(local.default_values), var.helm_values]` in `helm_release`. This allows the user to override *any* default set by the module.

#### D. Dynamic Submodules / Composition

Instead of hardcoding submodules in `main.tf`, consider breaking them into separate publishable modules if they are reusable. If keeping them monolithic, use the "Feature Flag" approach above.

#### E. Cloud Provider Abstraction

Refactor `cluster_autoscaler` to support Azure (if applicable) or other providers dynamically, or use a separate "addons" module for cloud-specific components.

---

### 3. Wiki Documentation: FITFILE Platform Module

> **Note**: This documentation covers the usage of `terraform-helm-fitfile-platform` v2.0.0+ in the context of NNUH and similar deployments.

#### Module: `terraform-helm-fitfile-platform`

This module deploys the core "Day 0" platform services required for a FITFILE Kubernetes cluster.

##### Architecture

The module deploys components in the following order:

1.  **Namespaces**: Core namespaces (`argocd`, `ingress-nginx`, etc.).
2.  **Vault Secrets Operator**: Authenticates with HashiCorp Vault.
3.  **Reflector**: Replicates secrets (like image pull secrets) across namespaces.
4.  **NGINX Ingress**: Sets up the ingress controller with internal/external load balancers.
5.  **ArgoCD**: Deploys the GitOps engine to manage "Day 1" applications.

##### Usage Guide (NNUH Example)

The NNUH platform consumes this module via the `fitfile-platform/helm` registry source.

**Basic Configuration (`main.tf`):**

```hcl
module "platform" {
  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
  version = "2.1.4"

  # --- Networking ---
  ingress_ip_address         = var.ingress_controller_ip_address
  ingress_load_balancer_type = "internal" # or "external"

  # --- Vault Integration ---
  vault_address        = var.vault_address
  app_role_secrets_map = local.app_role_secrets_map # Maps AppRoles to namespaces

  # --- ArgoCD ---
  argocd_host         = local.argocd_host
  argocd_applications = local.argocd_applications # Bootstrap apps (e.g., ffnode)
  argocd_sso          = { enabled = false }

  # --- Versioning (Pinned via Version Manager) ---
  ingress_nginx_chart_version      = data.terraform_remote_state.version_manager.outputs.ingress_nginx_chart_version
  argocd_chart_version             = data.terraform_remote_state.version_manager.outputs.argocd_chart_version
  # ... other versions
}
```

##### Key Inputs

| Variable | Description | Example |
| :--- | :--- | :--- |
| `ingress_ip_address` | Static IP for the LoadBalancer. | `10.0.1.10` |
| `app_role_secrets_map` | Map of Vault AppRoles to inject into namespaces. | `{ argocd = { ... } }` |
| `argocd_applications` | List of initial ArgoCD apps to deploy. | `[{ name = "ffnode", ... }]` |
| `helm_values` | (Optional) Raw YAML string to override chart values. | `yamlencode({ controller = { replicaCount = 3 } })` |

##### Best Practices for Consumers

1.  **Use the Version Manager**: Always fetch chart versions from the `global-version-manager` remote state to ensure compliance with platform standards.
2.  **Secret Management**: Never hardcode secrets. Pass them via `var.approles` (sensitive) and map them in `app_role_secrets_map`.
3.  **Overrides**: Use `ingress_helm_values` or `argocd_helm_values` sparingly. Only override what is necessary for the specific environment (e.g., specific annotations or resource limits).
4.  **Dependency Awareness**: Remember that ArgoCD depends on Ingress, which depends on Vault. If Vault fails to authenticate, the entire chain may stall. Check Vault Operator logs first if deployments hang.

##### Troubleshooting

-   **"CrashLoopBackOff" in Vault Operator**: Check `vault_address` and AppRole credentials.
-   **Ingress IP Pending**: Verify the IP address is valid in the subnet and not in use. Check cloud provider quotas.
-   **ArgoCD Unreachable**: Verify `ingress_host_network` settings and DNS resolution for `argocd_host`.

---
