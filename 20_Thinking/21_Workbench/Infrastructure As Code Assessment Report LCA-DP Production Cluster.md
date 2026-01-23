---
created: 2026-01-23T19:16:31+00:00
modified: 2026-01-23T19:21:06+00:00
title: HEAD - 2026-01-23 1916
---

## Infrastructure As Code Assessment Report: LCA-DP Production Cluster

### Executive Summary

The LCA-DP production cluster is in a transitional state following a recent migration from AppRole-based Vault authentication to native Kubernetes JWT authentication. The Terraform code is well-structured and modular, but reveals a two-tier deployment pattern where the main repository provisions the cluster but delegates in-cluster configuration to a separate "jumpbox" deployment process.

Current IaC Coverage Estimate: ~75% managed, 25% manual/generated

---

### 1. Current State Summary

#### What's Fully Managed by Terraform

✅ AKS Infrastructure (private-infrastructure module v1.3.31)

- AKS cluster with OIDC workload identity enabled
- VNet, subnets (system, workflows, app, jumpbox, bastion)
- NAT Gateway and NSGs
- Bastion Host + Linux jumpbox VM

✅ Central Services Integration (central-services-consumer module v0.0.9)

- Auth0 application + service accounts
- GitLab project: `lca-infra-prd`
- TFC workspace: `lca-infra-prd` (imported resource)
- Vault namespace: `deployments/lca-prd-2`
- Vault KV secrets for Auth0, application config, VM admin password

✅ Vault JWT Authentication (`vault_k8s_auth.tf`)

- JWT auth backend at `jwt-lca-prd-2`
- Role binding for VSO service accounts
- Policies: `acr-reader`, `argocd-secrets-lca-prd-2`

✅ Configuration Generation (`jumpbox_generator.tf`, `values_generator.tf`)

- Automated generation of `main.tf` for jumpbox deployment
- CUE-consumable values export

---

#### What's NOT Managed (Manual/Drift Zone)

⚠️ In-Cluster Kubernetes Resources - The platform components are deployed via a generated `main.tf` that runs on the jumpbox, not from the main repository:

Missing from main Terraform state:

- ArgoCD (Helm release + "App of Apps")
- Vault Secrets Operator (VSO)
- Ingress NGINX controller
- Reflector
- Cluster Autoscaler (if on AWS)
- VaultAuth CRDs in multiple namespaces
- VaultDynamicSecret/VaultStaticSecret CRDs
- Kubernetes Secrets/ConfigMaps

Why this creates drift:

1. The jumpbox `main.tf` is generated but not applied by TFC - it's manually deployed
2. No Terraform import for these resources back into the main state
3. If someone edits in-cluster resources directly, the main repo has no visibility
4. The jumpbox deployment is not GitOps-controlled (no ArgoCD managing Terraform)

---

#### Architecture Patterns Observed

##### ✅ Vault Integration

- Primary Method: JWT/OIDC authentication (modern, recommended)
- Legacy Artifacts: AppRole backend still exists in `central_services` module (for backward compatibility)
- Policies: Correctly scoped to deployment key (`lca-prd-2`)
- VSO: Deployed via platform module, configured with `VaultConnection` pointing to HCP Vault

##### ✅ Reflector Pattern

- Implementation: Template correctly includes annotations (`reflector.v1.k8s.emberstack.com/`)
- Usage: ACR image pull secrets are replicated across namespaces
- Gap: No evidence of custom ConfigMaps/Secrets with Reflector annotations in the main TF code

##### ⚠️ ArgoCD Bootstrap

- Deployment: Helm release in jumpbox template (not in main state)
- App of Apps: Defined in `jumpbox_main.tftpl` with multi-source pattern:
  - Source 1: Helm chart from `helm_chart_deployment` repo
  - Source 2: Values from `lca-infrastructure-prd` repo (`generated/values.yaml`)
- Issue: Root application (`ff-lca-prd-2`) not managed by main Terraform state

---

### 2. Gap Analysis: Drift & Missing Pieces

#### Critical Gaps

| Category    | Gap                                        | Impact                                  | Evidence                                                     |
| --------------- | ---------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------- |
| Vault Roles | JWT role exists, but AppRole artifacts remain  | Confusion, potential security overlap       | `vault_auth_backend.approle[0]` in state                         |
| VSO CRDs    | VaultAuth/VaultDynamicSecret not in main state | Can't track changes to secret mappings      | Only in generated jumpbox template                               |
| ArgoCD      | Helm release not in main state                 | Can't version-control ArgoCD config changes | Deployed from jumpbox                                            |
| Reflector   | No custom resources with Reflector annotations | Limited reuse of secrets/ConfigMaps         | Only image pull secret uses it                                   |
| Namespaces  | Only `argocd` created by platform module       | Application namespaces likely manual        | No `kubernetes_namespace` resources for `lca-prd-2` in main code |

---

#### Potential Drift Scenarios

1. Jumpbox Deployment Desync:
   - Generated `main.tf` might be outdated if not regenerated after changes
   - No validation that jumpbox state matches expected config

2. Manual ArgoCD Changes:
   - Users can edit ArgoCD apps via UI without Terraform awareness
   - No drift detection for Application CRDs

3. Vault Policy Changes:
   - Policies defined in TF, but manual edits in HCP UI could override
   - No automated reconciliation

4. Provider Version Skew:
   - Main code: `kubernetes = 2.35.1`, `helm = 2.17.0`, `vault >= 3.0.0`
   - Platform module: Version pinned to `2.2.22` (may have older provider requirements)

---

#### Security Observations

⚠️ Sensitive Data Exposure:

- `vnet_address_space` redacted (`/16`) in YAML but visible in state
- `jumpbox_main_content` output marked sensitive ✅
- No evidence of `SOPS` or `git-crypt` for secret management in repo

✅ Good Practices:

- VM admin password auto-generated via `random_password` in central_services
- Vault secrets used for Auth0, tenant keys
- No hardcoded ACR credentials (dynamic via Vault)

---

### 3. Code Quality & Hygiene

#### ✅ Strengths

1. Modular Design:
   - Clean separation: infrastructure → central services → platform
   - Remote state for version management (`global-version-manager`)

2. Configuration as Code:
   - `config/customer.yaml` drives deployment parameters
   - CUE-based values generation for consistency

3. Naming Conventions:
   - Follows Azure CAF: `rg-lca-uks-prd-net`, `aks-lca-uks-prd-01`
   - Deployment key pattern: `{customer}-{env_prefix}-{instance_id}`

4. Documentation:
   - Jumpbox deployment guide present
   - Verification script for ArgoCD diagnostics

---

#### ⚠️ Areas for Improvement

| Issue                        | Severity | Recommendation                                             |
| -------------------------------- | ------------ | -------------------------------------------------------------- |
| Hardcoded repo URLs in template  | Medium       | Move to variables or config YAML                               |
| No provider version upper bounds | Low          | Pin providers: `version = "~> 4.53"`                           |
| Missing README.md content        | Low          | Add architecture diagram, deployment steps                     |
| Template complexity              | Medium       | Jumpbox template is 320 lines - consider breaking into modules |
| No pre-commit hooks              | Low          | Add `terraform fmt`, `tflint` checks                           |

Example of hardcoded values:

```hcl
lca_repo_url   = "https://gitlab.com/fitfile/customers/nwsde/lca-infrastructure-prd.git"
chart_repo_url = "https://gitlab.com/fitfile/deployment/helm_chart_deployment.git"
```

---

### 4. Remediation Plan

#### Phase 1: Import & State Alignment (Week 1-2)

Goal: Bring in-cluster resources under Terraform control

##### Step 1.1: Import Jumpbox-Deployed Resources

```bash
# On jumpbox, capture current state
cd ~/terraform
terraform state pull > /tmp/jumpbox-state.json

# In main LCA-DP repo, add new file: platform_resources.tf
# Import ArgoCD Helm release
terraform import 'module.platform_jumpbox.helm_release.argocd' argocd/argocd

# Import VSO
terraform import 'module.platform_jumpbox.helm_release.vso' vault-secrets-operator-system/vault-secrets-operator

# Import VaultAuth CRDs
terraform import 'kubernetes_manifest.vault_auth["argocd"]' \
  "apiVersion=secrets.hashicorp.com/v1beta1,kind=VaultAuth,namespace=argocd,name=default"
```

Challenges:

- `kubernetes_manifest` requires exact API version match
- May need `kubectl_manifest` provider for CRDs

---

##### Step 1.2: Refactor Jumpbox Pattern

Current: Jumpbox generates TF, runs it locally

Target: Main repo provisions everything, jumpbox only for access

Actions:

1. Add AKS credentials data source to main TF:

```hcl
# In main.tf
provider "kubernetes" {
  host                   = module.private-infrastructure.aks_cluster_host
  client_certificate     = base64decode(module.private-infrastructure.aks_cluster_client_certificate)
  client_key             = base64decode(module.private-infrastructure.aks_cluster_client_key)
  cluster_ca_certificate = base64decode(module.private-infrastructure.aks_cluster_ca_certificate)
}
```

1. Move platform module call from generated template to main.tf:

```hcl
module "platform" {
  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
  version = "2.2.22"
  
  providers = {
    kubernetes = kubernetes
    helm       = helm
  }
  
  # ... existing config from jumpbox template
}
```

1. Deprecate jumpbox Terraform deployment (keep jumpbox VM for access only)

---

#### Phase 2: Clean Up Vault Configuration (Week 3)

Goal: Remove AppRole artifacts, ensure JWT is sole auth method

##### Step 2.1: Audit Current Vault State

```bash
# Check what auth backends exist
vault auth list

# Verify JWT role permissions
vault read auth/jwt-lca-prd-2/role/lca-prd-2

# Check AppRole usage
vault list auth/approle/role
```

##### Step 2.2: Migrate or Remove AppRole

Option A (Safe): Keep AppRole disabled but in code for rollback

```hcl
# In vault_k8s_auth.tf
resource "vault_auth_backend" "approle" {
  count = 0  # Disabled - using JWT
  type  = "approle"
}
```

Option B (Clean): Remove entirely

1. Delete `vault_auth_backend.approle[0]` from state
2. Remove from `central_services` module config
3. Verify no VSO resources reference it

---

##### Step 2.3: Codify Missing Vault Resources

Currently missing:

- Vault KV secrets in `deployments/lca-prd-2/`
- Cloudflare API token (referenced in values.yaml)
- Grafana admin credentials (referenced in jumpbox template)

Add to vault configuration:

```hcl
# vault_secrets.tf
resource "vault_kv_secret_v2" "cloudflare_token" {
  mount = "secrets"
  name  = "cloudflare"
  
  data_json = jsonencode({
    api_token = var.cloudflare_api_token  # From TFC variable
  })
}

resource "vault_kv_secret_v2" "grafana_admin" {
  mount = "secrets"
  name  = "monitoring"
  
  data_json = jsonencode({
    admin_password = random_password.grafana_admin.result
  })
}
```

---

#### Phase 3: Automate Configuration (Week 4)

Goal: Eliminate manual steps, make all config generated

##### Step 3.1: Modularize Values Generation

Replace CUE templates with Terraform `templatefile`:

```hcl
# values_generator.tf
resource "local_file" "helm_values" {
  filename = "${path.module}/generated/values.yaml"
  content = templatefile("${path.module}/templates/values.yaml.tftpl", {
    namespace           = local.deployment_key
    deployment_key      = local.deployment_key
    host                = local.public_fqdn
    fit_connect_code    = local.customer_full_name
    auth0_base_url      = module.central_services.auth0_domain
    auth0_api_audience  = local.api_audience
    # ... all other values
  })
}
```

---

##### Step 3.2: Add Namespace Management

```hcl
# namespaces.tf
resource "kubernetes_namespace" "deployment" {
  metadata {
    name = local.deployment_key
    labels = {
      environment = local.environment
      managed-by  = "terraform"
    }
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}
```

---

##### Step 3.3: Add Reflector Annotations to Custom Secrets

Example for TLS certificates:

```hcl
resource "kubernetes_secret" "cloudflare_tls" {
  metadata {
    name      = "cloudflare-tls"
    namespace = kubernetes_namespace.deployment.metadata[0].name
    
    annotations = {
      "reflector.v1.k8s.emberstack.com/reflection-allowed"    = "true"
      "reflector.v1.k8s.emberstack.com/reflection-auto-enabled" = "true"
      "reflector.v1.k8s.emberstack.com/reflection-auto-namespaces" = "cert-manager,ingress-nginx"
    }
  }
  
  # ... secret data from Vault
}
```

---

#### Phase 4: GitOps Alignment (Week 5-6)

Goal: Ensure Terraform is the single source of truth

##### Step 4.1: ArgoCD App of Apps in Terraform

```hcl
# argocd_apps.tf
resource "kubectl_manifest" "root_application" {
  yaml_body = templatefile("${path.module}/templates/argocd-root-app.yaml", {
    deployment_key = local.deployment_key
    chart_repo     = local.config.chart_repo_url
    lca_repo       = local.config.lca_repo_url
    values_path    = "generated/values.yaml"
  })
  
  depends_on = [module.platform]
}
```

---

##### Step 4.2: Pre-Commit Hooks & CI/CD

Add `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
```

Add GitLab CI pipeline:

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply

terraform:validate:
  stage: validate
  script:
    - terraform init -backend=false
    - terraform fmt -check
    - terraform validate

terraform:plan:
  stage: plan
  script:
    - terraform init
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - tfplan
```

---

### 5. Priority Matrix

| Task                  | Priority | Effort | Risk if Delayed                  |
| ------------------------- | ------------ | ---------- | ------------------------------------ |
| Import jumpbox resources  | High     | High       | Continued drift, manual toil         |
| Remove AppRole artifacts  | Medium   | Low        | Security confusion, unused resources |
| Add missing Vault secrets | High     | Medium     | Manual secret management             |
| Refactor jumpbox pattern  | High     | High       | Two sources of truth                 |
| Add Reflector annotations | Low      | Low        | Limited secret reuse                 |
| Implement GitOps checks   | Medium   | Medium     | Unvalidated changes                  |

---

### 6. Recommendations Summary

#### Quick Wins (This Sprint)

1. Add provider version upper bounds (`version = "~> 4.53"`)
2. Move hardcoded repo URLs to `config/customer.yaml`
3. Document current jumpbox deployment process in README
4. Import TFC workspace (already done: `imports.tf`)

#### Short Term (1 Month)

1. Import in-cluster resources to main state
2. Consolidate Vault auth to JWT-only
3. Add missing Vault secrets to Terraform

#### Long Term (Quarter)

1. Deprecate jumpbox Terraform pattern
2. Full GitOps: Terraform → TFC → AKS
3. Add drift detection (e.g., Terraform Cloud agents with scheduled runs)

---

### Appendix: File Structure Overview

```
LCA-DP/
├── config/
│   └── customer.yaml          # ✅ Single source of config
├── templates/
│   ├── jumpbox_main.tftpl     # ⚠️  320-line generated TF (needs refactor)
│   └── values.cue             # ✅ CUE-based values
├── generated/
│   ├── main.tf                # ⚠️  Not in Git (generated output)
│   ├── values.yaml            # ✅ Tracked, used by ArgoCD
│   └── infra.json             # ℹ️  Metadata export
├── main.tf                    # ✅ Module orchestration
├── vault_k8s_auth.tf          # ✅ JWT auth (modern)
├── data.tf                    # ✅ Remote state reference
├── locals.tf                  # ✅ Computed values
├── providers.tf               # ⚠️  No K8s/Helm providers (only in jumpbox)
└── docs/
    └── JUMPBOX_DEPLOYMENT.md  # ✅ Deployment guide
```

---

### Conclusion

The LCA-DP infrastructure is well-architected but operationally split. The main Terraform code handles Azure resources excellently, but in-cluster configuration is delegated to a separate deployment process. This creates a GitOps anti-pattern where the source of truth is fragmented.

Critical Next Step: Consolidate the jumpbox-deployed resources into the main Terraform state to achieve true infrastructure-as-code and enable drift detection.

Estimated Effort to Full GitOps: 4-6 weeks with 1 engineer
