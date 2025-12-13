---
aliases: []
confidence: 
created: 2025-03-06T02:31:25Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: terraform helm fitfile platform
type: note
uid: 
updated: 
version: 
---

## Identified Hardcoded Data

### 1. Terraform Provider Versions
- File: versions.tf
- Type: String
- Values:
  - kubernetes: "2.35.1"
  - helm: "2.17.0"
  - kubectl: "1.14.0"
  - required_version: ">= 1.8.3"

### 2. Helm Chart Versions
- File: ingress_nginx/main.tf
  - Type: String
  - Value: "4.11.2" (ingress-nginx chart version)
- File: argocd/main.tf
  - Type: String
  - Values:
    - "7.7.5" (argo-cd chart version)
    - "1.4.1" (argocd-apps chart version)
- File: vault_operator/main.tf
  - Type: String
  - Value: "0.8.1" (vault-secrets-operator chart version)
- File: reflector/main.tf
  - Type: String
  - Value: "7.1.288" (reflector chart version)
- File: cluster_autoscaler/main.tf
  - Type: String
  - Value: "9.43.0" (cluster-autoscaler chart version)

### 3. Default Values
- File: variables.tf
  - Type: String
  - Value: "https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/" (vault_address default)
  - Type: String
  - Value: "AZURE" (cloud_provider default)
  - Type: String
  - Value: "eu-west-2" (aws_region default)

### 4. Hardcoded Service Names and Namespaces
- File: locals.tf
  - Type: String
  - Value: "vault-secrets-operator-system" (in unique_namespaces)
- File: argocd-values.yaml
  - Type: String
  - Value: "dev-argocd.fitfile.net" (host name)
- File: vault_operator/main.tf, reflector/main.tf
  - Type: String
  - Values: Various namespace names like "vault-secrets-operator-system", "reflector"

### 5. Repository URLs
- File: Multiple files (ingress_nginx/main.tf, argocd/main.tf, etc.)
  - Type: String
  - Value: "oci://fitfilepublic.azurecr.io" (helm chart repository)

### 6. Resource Configurations
- File: reflector/main.tf
  - Type: String
  - Values:
    - CPU requests: "50m"
    - Memory requests: "64Mi"
    - CPU limits: "100m"
    - Memory limits: "128Mi"
- File: argocd/argocd-values.yaml
  - Type: Various (String, Number)
  - Values: Multiple resource configurations, credentials, annotations, etc.

## Refactoring Plan

### 1. Variable Definition for Provider Versions

```hcl
variable "kubernetes_provider_version" {
  description = "Version of the Kubernetes provider to use"
  type        = string
  default     = "2.35.1"
}

variable "helm_provider_version" {
  description = "Version of the Helm provider to use"
  type        = string
  default     = "2.17.0"
}

variable "kubectl_provider_version" {
  description = "Version of the Kubectl provider to use"
  type        = string
  default     = "1.14.0"
}

variable "terraform_required_version" {
  description = "Minimum required Terraform version"
  type        = string
  default     = "1.8.3"
}
```

### 2. Variable Definition for Helm Chart Versions

```hcl
variable "ingress_nginx_chart_version" {
  description = "Version of the ingress-nginx Helm chart to deploy"
  type        = string
  default     = "4.11.2"
}

variable "argocd_chart_version" {
  description = "Version of the ArgoCD Helm chart to deploy"
  type        = string
  default     = "7.7.5"
}

variable "argocd_apps_chart_version" {
  description = "Version of the ArgoCD Apps Helm chart to deploy"
  type        = string
  default     = "1.4.1"
}

variable "vault_operator_chart_version" {
  description = "Version of the Vault Secrets Operator Helm chart to deploy"
  type        = string
  default     = "0.8.1"
}

variable "reflector_chart_version" {
  description = "Version of the Reflector Helm chart to deploy"
  type        = string
  default     = "7.1.288"
}

variable "cluster_autoscaler_chart_version" {
  description = "Version of the Cluster Autoscaler Helm chart to deploy"
  type        = string
  default     = "9.43.0"
}
```

### 3. Variable Definition for Repository URLs

```hcl
variable "helm_repository_url" {
  description = "URL of the Helm chart repository"
  type        = string
  default     = "oci://fitfilepublic.azurecr.io"
}
```

### 4. Variable Definition for Namespaces

```hcl
variable "vault_operator_namespace" {
  description = "Namespace to deploy the Vault Secrets Operator"
  type        = string
  default     = "vault-secrets-operator-system"
}

variable "reflector_namespace" {
  description = "Namespace to deploy the Reflector"
  type        = string
  default     = "reflector"
}
```

### 5. Variables for Resource Configurations

```hcl
variable "reflector_resources" {
  description = "Resource requests and limits for the Reflector"
  type = object({
    requests = object({
      cpu    = string
      memory = string
    })
    limits = object({
      cpu    = string
      memory = string
    })
  })
  default = {
    requests = {
      cpu    = "50m"
      memory = "64Mi"
    }
    limits = {
      cpu    = "100m"
      memory = "128Mi"
    }
  }
}
```

### Code Modification Strategy

#### 1. Update versions.tf

```hcl
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = var.kubernetes_provider_version
    }
    helm = {
      source  = "hashicorp/helm"
      version = var.helm_provider_version
    }
    kubectl = {
      source  = "app.terraform.io/FITFILE-Platforms/kubectl"
      version = var.kubectl_provider_version
    }
  }

  required_version = ">= ${var.terraform_required_version}"
}
```

#### 2. Update Main Module References

For each of the submodules in main.tf, pass the new variables:

```hcl
module "vault_operator" {
  # ... existing code ...
  source                           = "./vault_operator"
  chart_version                    = var.vault_operator_chart_version
  namespace                        = var.vault_operator_namespace
  repository_url                   = var.helm_repository_url
  # ... existing code ...
}

module "reflector" {
  # ... existing code ...
  source                           = "./reflector"
  chart_version                    = var.reflector_chart_version
  namespace                        = var.reflector_namespace
  repository_url                   = var.helm_repository_url
  resources                        = var.reflector_resources
  # ... existing code ...
}

# Similar updates for other modules
```

#### 3. Update Submodule Files

For each submodule, update the main.tf file to use the passed variables:

Example for reflector/main.tf:

```hcl
resource "helm_release" "vso_helm_release" {
  name             = "reflector"
  namespace        = var.namespace
  create_namespace = true
  chart            = "helm/reflector"
  version          = var.chart_version
  repository       = var.repository_url
  wait             = true

  set {
    name  = "resources.requests.cpu"
    value = var.resources.requests.cpu
  }

  set {
    name  = "resources.requests.memory"
    value = var.resources.requests.memory
  }

  set {
    name  = "resources.limits.cpu"
    value = var.resources.limits.cpu
  }

  set {
    name  = "resources.limits.memory"
    value = var.resources.limits.memory
  }
  
  # ... existing code ...
}
```

#### 4. Update Each Submodule's variables.tf

Add the corresponding variable definitions to each submodule's variables.tf file:

Example for reflector/variables.tf:

```hcl
variable "chart_version" {
  description = "Version of the Reflector Helm chart to deploy"
  type        = string
}

variable "namespace" {
  description = "Namespace to deploy the Reflector"
  type        = string
}

variable "repository_url" {
  description = "URL of the Helm chart repository"
  type        = string
}

variable "resources" {
  description = "Resource requests and limits for the Reflector"
  type = object({
    requests = object({
      cpu    = string
      memory = string
    })
    limits = object({
      cpu    = string
      memory = string
    })
  })
}
```

### Version Variable Focus

The version variables are particularly important for this module as they allow:

1. Consistent Deployments: Using specific versions as defaults ensures consistent deployments across environments
2. Controlled Updates: Module consumers can update versions when ready, rather than having updates forced upon them
3. Rollback Capability: Easy to rollback to previous versions if issues arise with newer versions
4. Environment-Specific Versions: Different environments (dev, staging, prod) can use different versions as needed
5. Compliance: Some environments may need to stay on specific versions for compliance reasons

For version management, I recommend:

- Always use specific versions as defaults (not using 'latest')
- Add clear documentation in variable descriptions about compatibility concerns
- Consider adding validation for version patterns
- Document any interdependencies between component versions

### Output Considerations

Add new outputs to expose the versions being used to consumers:

```hcl
output "deployed_versions" {
  description = "Map of the component versions deployed"
  value = {
    kubernetes_provider     = var.kubernetes_provider_version
    helm_provider           = var.helm_provider_version
    kubectl_provider        = var.kubectl_provider_version
    ingress_nginx           = var.ingress_nginx_chart_version
    argocd                  = var.argocd_chart_version
    argocd_apps             = var.argocd_apps_chart_version
    vault_operator          = var.vault_operator_chart_version
    reflector               = var.reflector_chart_version
    cluster_autoscaler      = var.cluster_autoscaler_chart_version
  }
}
```

This output will be useful for documentation and verification of what has been deployed.

## Usage

```sh
FITFILE/Deployments/Customers/wm-dev-1/platform/main.tf
177:  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
178-  version = "1.0.12"

FITFILE/Deployments/Deploy/Production/private_platform_template/main.tf
187:  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
188-  version = "1.0.29"

FITFILE/Deployments/Deploy/Production/fitfile-production-infrastructure/pentest-cluster/main.tf
34:  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
35-  version = "1.0.38"

FITFILE/Deployments/Deploy/Production/fitfile-production-infrastructure/prod-1-cluster/main.tf
33:  source     = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
34-  version    = "1.0.26"

FITFILE/Deployments/Deploy/Non-Production/fitfile-non-production-infrastructure/ff-hyve-2/main.tf
29:  source     = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
30-  version    = "1.0.38"

FITFILE/Deployments/Deploy/Non-Production/fitfile-non-production-infrastructure/testing-cluster/main.tf
30:  source     = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
31-  version    = "1.1.3"

FITFILE/Deployments/Deploy/Non-Production/fitfile-non-production-infrastructure/examples/public-infrastructure/main.tf
29:  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
30-  version = "1.0.26"

FITFILE/Deployments/Deploy/Non-Production/fitfile-non-production-infrastructure/staging-cluster-2/main.tf
30:  source     = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
31-  version    = "1.1.3"

FITFILE/Deployments/Deploy/Non-Production/fitfile-non-production-infrastructure/ff-hyve-1/main.tf
29:  source     = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
30-  version    = "1.1.3"
```

## Description

This ticket involves refactoring our Terraform module to increase its flexibility and reusability by extracting hardcoded values into variables - with a primary focus on Helm chart versions. Currently, our module has numerous hardcoded values (chart versions, provider versions, resource configurations, etc.) that prevent module consumers from specifying their preferred versions and configurations.

The most critical part of this work is extracting the Helm chart versions from the following components:

- ingress-nginx (currently v4.11.2)
- ArgoCD (currently v7.7.5)
- ArgoCD Apps (currently v1.4.1)
- Vault Secrets Operator (currently v0.8.1)
- Reflector (currently v7.1.288)
- Cluster Autoscaler (currently v9.43.0)

## Rationale

Extracting hardcoded chart versions provides several key benefits:

1. Version Control: Allows module consumers to specify which chart versions to use, essential for controlled rollouts
2. Environment-Specific Configurations: Different environments (dev, staging, prod) can use different chart versions
3. Compatibility Management: Makes it easier to maintain compatibility between different components
4. Predictable Updates: Prevents unexpected behavior changes when the module is updated
5. Rollback Capability: Provides an easy mechanism to roll back to previous versions if issues arise

## Implementation Details

### Phase 1: Chart Version Variables (Priority)
1. Create variables for each Helm chart version:

```hcl
variable "ingress_nginx_chart_version" {
  description = "Version of the ingress-nginx Helm chart to deploy"
  type        = string
  default     = "4.11.2"
}

variable "argocd_chart_version" {
  description = "Version of the ArgoCD Helm chart to deploy"
  type        = string
  default     = "7.7.5"
}

# Add similar variables for other chart versions
```

2. Update all helm_release resources to use these variables
3. Update submodule interfaces to pass version variables down
4. Add version outputs for validation and documentation

### Phase 2: Provider Versions and Other Configurations
1. Extract provider version constraints into variables
2. Extract repository URLs and namespaces into variables
3. Extract resource configurations (CPU/memory) into structured variables

## Acceptance Criteria
- [x] All hardcoded Helm chart versions are extracted into variables with appropriate defaults [completion:: 2025-03-06]
- [x] All provider version constraints are extracted into variables [completion:: 2025-03-06]
- [x] Resources can be deployed using the default variable values (backward compatibility) [completion:: 2025-03-06]
- [x] Module consumers can override any chart version through variables [completion:: 2025-03-06]
- [x] Documentation is updated to describe the new variables and their purpose [completion:: 2025-03-06]
- [x] An output is added that shows the deployed versions for verification [completion:: 2025-03-06]

## Technical Notes
- Some submodules may need their variable interfaces updated to accept the new version parameters
- The default values should match the current hardcoded values to maintain backward compatibility
- All variables should have descriptive documentation explaining their purpose and any version compatibility considerations
- Consider using validation rules for critical variables to prevent incompatible configurations
