---
created: 2026-01-23T19:57:30+00:00
modified: 2026-03-14T11:10:51+00:00
title: VAULT_IAC_ASSESSMENT
---

## HCP Vault Terraform Configuration Analysis

Date: 2026-01-23

Author: Principal DevOps Engineer Assessment

Repository: `central-services/hcp/vault`

Status: Draft for Review

---

## Executive Summary

The Vault Terraform codebase manages HCP Vault configuration only - it does NOT manage the full AKS/ArgoCD/VSO integration stack. Based on analysis, approximately 60-70% of the critical GitOps workflow is defined as IaC, but there are significant gaps between Vault configuration and cluster integration.

Critical Finding: The codebase uses AppRole authentication exclusively, but evidence exists (in `LCA-DP/vault_k8s_auth.tf`) that newer deployments are moving to Kubernetes/JWT authentication for VSO - this migration is not reflected in the central Vault configuration.

---

## 1. Current State Summary

### What IS Managed in Terraform

#### ✅ Vault Configuration (Comprehensive)

- Namespaces: `central` and `deployments/` hierarchy for 17 deployment environments
- Secret Engines:
  - KV-v2 per deployment namespace
  - Azure secrets backend (ACR authentication)
  - PKI Root CA + Intermediate CAs (for 3 PKI-enabled deployments)
  - Terraform Cloud secrets engine (GitLab token management)
- Authentication:
  - AppRole per deployment namespace
  - JWT auth for Terraform Cloud workspaces
  - ⚠️ NO Kubernetes auth backend definitions (see Gap Analysis)
- Policies: App-specific read policies, ArgoCD policies, cert-manager PKI policies
- Identities: Vault entities, entity aliases, group memberships for cross-namespace secret sharing

#### ✅ Deployment Bootstrap (Separate Module)

From `terraform-helm-fitfile-platform`:

- VSO Helm deployment with default `VaultConnection`
- ArgoCD Helm deployment + App of Apps bootstrap
- Reflector for secret/ConfigMap replication
- Ingress-NGINX controller

### What is NOT Managed (Manual/Drift Risk)

#### ❌ Vault-Kubernetes Integration

- Kubernetes auth backend configuration (only found in `LCA-DP` deployment, not centralized)
- `vault_kubernetes_auth_backend_role` resources for VSO
- Per-namespace `VaultAuth` and `VaultConnection` manifests (created via platform module templates, but not in central Vault config)

#### ❌ Manual Configuration Steps

From `README.md`, these require manual setup:

1. Root namespace `group_policy_application_mode = "any"` (API call required)
2. JWT auth method for Terraform Cloud trust relationship (manual HCP portal setup)
3. Vault root token management (not in Terraform, obviously)

#### ⚠️ Secrets Data Management

- All `vault_kv_secret_v2` resources use `lifecycle { ignore_changes = [data_json] }`
- Secret _values_ are managed out-of-band (correct for security, but creates drift in secret _structure_)

---

## 2. Gap Analysis: The "Drift" List

### 🔴 Critical Gaps (High Drift Risk)

#### Gap 1: Kubernetes Authentication Backend

- Issue: No `vault_auth_backend` resource for Kubernetes auth method in central Vault config
- Evidence: LCA-DP deployment creates `vault_jwt_auth_backend.jwt` with OIDC issuer pointing to AKS
- Impact: VSO currently uses AppRole (less secure, requires secret distribution). Migration to K8s auth is partially implemented in deployments but not standardized
- Drift: New deployments (like LCA-DP) are diverging from the AppRole pattern

#### Gap 2: Vault Kubernetes Auth Roles

- Missing Resources:

```hcl
# EXPECTED but MISSING
resource "vault_kubernetes_auth_backend_role" "vso" {
  for_each = local.deployments
  # Configuration for VSO ServiceAccount authentication
}
```

- Current Workaround: AppRole credentials stored as Kubernetes Secrets (`kubernetes_secret.ns_approle_secrets` in platform module)
- Security Risk: AppRole secrets are static and stored in cluster; K8s auth uses ephemeral tokens

#### Gap 3: Per-Namespace VaultConnection/VaultAuth CRDs

- Issue: VSO custom resources are templated in `vault_operator/vault_auth.tftpl` but not managed centrally
- Impact: Each deployment relies on module templating; changes to auth strategy require module updates across all clusters
- Drift: Template changes don't propagate to existing deployments without re-apply

#### Gap 4: Reflector Configuration

- No Secrets/ConfigMaps with Reflector Annotations in Vault Terraform code
- Expected Pattern:

```yaml
metadata:
  annotations:
    reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
    reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
```

- Current State: Reflector is deployed (`terraform-helm-fitfile-platform/reflector`) but Vault-generated secrets don't include these annotations
- Workaround: Likely added manually or via VSO templates (not visible in Vault TF)

### 🟡 Medium Gaps (Code Quality/Hygiene)

#### Gap 5: Hardcoded Values

| File | Line | Issue | Recommendation |
|------|------|-------|----------------|
| `auth.tf` | 9 | Hardcoded Object ID `f845a7ad-5e98-467b-9c92-495d36608468` | Use data source or variable |
| `variables.tf` | 13 | Hardcoded Tenant ID | Already has default, but no description of what tenant this is |
| `variables.tf` | 44 | Hardcoded Vault address `https://vault.fitfile.co.uk` | Acceptable for single-tenant, but document |

#### Gap 6: Provider Version Currency

- `versions.tf`: Vault provider `~>4.3.0` (released mid-2024)
- Status: Not latest, but acceptable. Current is `~>4.6.0`
- Risk: Low - minor versions unlikely to break, but missing newer resources (e.g., `vault_identity_oidc_`)

#### Gap 7: PKI Deployment Coverage

- Only 3 of 17 deployments have PKI enabled (`testing`, `hie-prod-34`, `cuh-prod-1`)
- Question for stakeholders: Is this intentional, or should more environments use internal PKI?

#### Gap 8: Namespace Strategy Inconsistency

- AppRole auth: Uses `approle` backend per deployment namespace
- Kubernetes auth (LCA-DP): Uses JWT backend in root namespace, not deployment namespace
- Conflict Risk: If you add K8s auth to central Vault config, it may clash with existing LCA-DP configuration

---

## 3. Remediation Plan

### Phase 1: Import & Inventory (No Code Changes)

Objective: Discover what exists in Vault that isn't in Terraform

#### Task 1.1: Audit Existing Auth Backends

```bash
# For each deployment namespace, check for Kubernetes auth mounts
vault auth list -namespace=deployments/<deployment-name> -format=json
```

Action: Document any `jwt` or `kubernetes` mounts not in Terraform state

#### Task 1.2: Inventory Manual Policies

```bash
vault policy list -namespace=deployments/<deployment-name>
```

Action: Compare against `policies.tf` output; identify drift

#### Task 1.3: Check for Unmanaged Secrets Engines

```bash
vault secrets list -namespace=deployments/<deployment-name> -format=json
```

Action: Look for PKI mounts, KV engines, or other backends not in `secret_engines.tf`

#### Task 1.4: Import LCA-DP Kubernetes Auth Resources

If you want to manage LCA-DP's K8s auth centrally:

```bash
# Example import (adjust namespace/paths)
terraform import vault_jwt_auth_backend.jwt_lca_dp jwt-lca-dp
terraform import vault_jwt_auth_backend_role.vso_lca_dp auth/jwt-lca-dp/role/lca-dp
terraform import vault_policy.acr_reader acr-reader
```

---

### Phase 2: Refactor & Standardize (Code Improvements)

#### Task 2.1: Create Kubernetes Auth Module

Objective: Centralize K8s auth backend configuration for all deployments

```hcl
# New file: k8s_auth.tf
resource "vault_jwt_auth_backend" "k8s_auth" {
  for_each = {
    for name, deployment in local.deployments : name => deployment
    if try(deployment.k8s_auth_enabled, false)
  }
  
  namespace          = vault_namespace.namespace[each.key].path_fq
  path               = "jwt-${each.key}"
  oidc_discovery_url = each.value.k8s_oidc_issuer  # From AKS OIDC endpoint
  bound_issuer       = each.value.k8s_oidc_issuer
}

resource "vault_jwt_auth_backend_role" "vso" {
  for_each = vault_jwt_auth_backend.k8s_auth
  
  backend   = each.value.path
  role_name = "vso-${each.key}"
  
  bound_audiences = [
    "https://kubernetes.default.svc.cluster.local",
    each.value.oidc_discovery_url
  ]
  
  bound_claims = {
    sub = "system:serviceaccount:vault-secrets-operator-system:"
  }
  
  token_policies = [
    vault_policy.read_policy["${each.key}.application"].name,
    vault_policy.argocd_read_policy[each.key].name
  ]
}
```

Migration Note: This would replace AppRole for new deployments. Existing deployments should migrate gradually.

#### Task 2.2: Add Reflector Annotations to VSO-Generated Secrets

Challenge: VSO creates secrets dynamically; Terraform doesn't manage them directly.

Solution Options:

1. Template-based: Update `vault_operator/vault_auth.tftpl` to include Reflector annotations in `VaultDynamicSecret` definitions
2. Mutation Webhook: Deploy a Kubernetes admission controller to inject annotations (advanced)
3. Document Manual Process: Accept that Reflector annotations are added post-deployment via GitOps (ArgoCD manifests)

Recommendation: Option 1 - update platform module templates.

#### Task 2.3: Parameterize Hardcoded Values

```hcl
# variables.tf additions
variable "acr_pull_app_object_id" {
  description = "Azure AD Application Object ID for HCP Vault ACR Pull identity"
  type        = string
  default     = "f845a7ad-5e98-467b-9c92-495d36608468"
}

# auth.tf update
resource "vault_azure_secret_backend_role" "acr_pull_role" {
  application_object_id = var.acr_pull_app_object_id  # Changed
}
```

#### Task 2.4: Upgrade Provider Versions

```hcl
# versions.tf
required_providers {
  vault = {
    source  = "hashicorp/vault"
    version = "~>4.6.0"  # Update from 4.3.0
  }
}
```

Test Plan: Run `terraform plan` in non-prod; validate no breaking changes

---

### Phase 3: Automate Manual Steps

#### Task 3.1: Automate Group Policy Application Mode

Current: Manual API call to set `group_policy_application_mode = "any"`

Solution: Use Vault provider's `vault_generic_endpoint` resource (requires admin namespace token):

```hcl
resource "vault_generic_endpoint" "group_policy_mode" {
  namespace           = "admin"
  path                = "sys/config/group-policy-application"
  disable_read        = true
  disable_delete      = true
  write_fields        = ["group_policy_application_mode"]

  data_json = jsonencode({
    group_policy_application_mode = "any"
  })
}
```

Caveat: Requires Terraform to authenticate with admin namespace token (security review needed)

#### Task 3.2: Document/Script JWT Auth Setup for TFC

Current: Manual HCP portal setup (README steps 23-36)

Can't Fully Automate: HCP admin namespace requires root token (not practical for Terraform)

Mitigation: Create a shell script wrapper:

```bash
#!/bin/bash
# scripts/setup-tfc-jwt-auth.sh
vault login -method=token token=$VAULT_ROOT_TOKEN
vault write -namespace=admin auth/jwt-terraform/role/tfc-role @vault-jwt-auth-role.json
```

Include in CI/CD pipeline or runbook.

---

### Phase 4: GitOps Alignment

#### Task 4.1: Define ArgoCD Applications in Terraform

Current: `argocd/app-values.tftpl` creates App of Apps, but bootstrap application definition isn't in central repo

Recommendation: Add `argocd_application` resource (using Kubernetes provider):

```hcl
resource "kubernetes_manifest" "argocd_root_app" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "fitfile-platform"
      namespace = "argocd"
    }
    spec = {
      project = "default"
      source = {
        repoURL        = "https://gitlab.com/fitfile/..."
        targetRevision = "main"
        path           = "apps"
      }
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "argocd"
      }
    }
  }
}
```

#### Task 4.2: Migrate Deployment-Specific Vault Config to Cluster Repos

Rationale: `LCA-DP/vault_k8s_auth.tf` shows deployment-specific Vault config living in cluster repos

Decision Point:

- Centralized Model: All Vault auth backends managed in `central-services/hcp/vault`
- Distributed Model: Each cluster manages its own Vault auth configuration

Recommendation: Centralized - move `vault_k8s_auth.tf` logic into central repo's `k8s_auth.tf` (Task 2.1)

---

## 4. Code Quality & Security Observations

### ✅ Strengths

1. Namespace Isolation: Clean separation between `central` (shared services) and `deployments/` (tenant isolation)
2. Dynamic Resource Generation: Excellent use of `for_each` and `locals` for DRY code
3. Secret Lifecycle Management: Proper use of `ignore_changes` for secret data
4. PKI Implementation: Well-structured PKI hierarchy (Root → Intermediate → cert-manager roles)
5. Terraform Cloud Integration: JWT auth for dynamic GitLab tokens is a modern pattern

### ⚠️ Security Considerations

1. AppRole Secret Distribution: Static secrets stored in Kubernetes (`kubernetes_secret.ns_approle_secrets`) - migrate to K8s auth
2. Overly Permissive Policy: `deployment_operator_policy` allows `update, patch, list` on `secrets/data/` (consider scoping down)
3. PKI Certificate Issuer Policy (lines 61-95 in `policies.tf`): Grants `sudo` on `pki` paths - extremely powerful, review necessity
4. No CIDR Restrictions: Comments in `identities.tf` mention `cidr_list` for AppRoles but not implemented

### 🔧 Code Hygiene Recommendations

1. Consolidate PKI Files: `pki_testing.tf` is commented out but still in repo - remove or archive
2. Output Sensitivity: All AppRole outputs marked `sensitive = true` ✅ Good
3. Dependency Management: Proper use of `depends_on` throughout ✅
4. Variable Descriptions: Most variables well-documented, but add descriptions for deployment-specific locals

---

## 5. Prioritized Action Plan

### Immediate (Sprint 1-2)

- [ ] Audit existing Vault state vs. Terraform (Phase 1 tasks)
- [ ] Import LCA-DP's K8s auth resources into state or document divergence
- [ ] Parameterize hardcoded values (Task 2.3)

### Short-Term (Sprint 3-5)

- [ ] Create centralized K8s auth module (Task 2.1)
- [ ] Update `terraform-helm-fitfile-platform` module to support K8s auth mode
- [ ] Upgrade Vault provider to `~>4.6.0` (Task 2.4)
- [ ] Pilot K8s auth on 1 non-production deployment

### Medium-Term (2-3 Months)

- [ ] Migrate all deployments from AppRole → K8s auth
- [ ] Automate group policy application mode setup (Task 3.1)
- [ ] Add ArgoCD root application to Terraform (Task 4.1)
- [ ] Enable PKI for additional deployments (if needed)

### Long-Term (Continuous)

- [ ] Implement CIDR restrictions on auth roles
- [ ] Review and scope down overly permissive policies
- [ ] Establish Vault state drift detection in CI/CD

---

## 6. Metrics for Success

| Metric | Current | Target (6 Months) |
|--------|---------|-------------------|
| % of Vault config in Terraform | ~70% | >95% |
| Deployments using K8s auth | 1 (LCA-DP) | 17 (all) |
| Manual setup steps in README | 7 | ≤2 |
| Terraform provider versions | 6 months old | <3 months old |
| Unmanaged auth backends | Unknown | 0 |

---

## 7. Questions for Stakeholders

1. Authentication Strategy: Do you want to mandate K8s auth for all new deployments, or keep AppRole as an option?
2. PKI Rollout: Should all production deployments use internal PKI, or is external PKI (e.g., Let's Encrypt) preferred for some?
3. Ownership Model: Should deployment-specific Vault config live in `central-services` or in each cluster's repo?
4. Vault Root Token Management: How is the root token currently managed? (For automating admin namespace tasks)
5. Reflector Necessity: Are you actively using Reflector, or can namespace-local VSO `VaultDynamicSecret` resources replace it?

---

## Appendix: File Inventory

### Core Terraform Files

- `main.tf` - Vault provider configuration (minimal)
- `versions.tf` - Terraform Cloud backend, provider versions
- `variables.tf` - Input variables for Azure/Vault configuration
- `locals.tf` - Deployment definitions (17 environments)
- `namespaces.tf` - Vault namespace hierarchy
- `auth.tf` - AppRole authentication configuration
- `policies.tf` - Vault policies for apps, ArgoCD, PKI
- `secret_engines.tf` - KV-v2, Azure backend, Root PKI
- `pki.tf` - Intermediate PKI per deployment
- `identities.tf` - Vault entities and aliases
- `groups.tf` - Cross-namespace group sharing
- `terraform_cloud_integration.tf` - TFC JWT auth + GitLab secrets
- `output.tf` - AppRole IDs, PKI outputs

### Supporting Files

- `pki_testing.tf` - Commented-out PKI test (candidate for removal)
- `README.md` - Setup instructions (includes manual steps)
- `TERRAFORM_CLOUD_INTEGRATION_SETUP.md` - TFC integration guide
- `vault-jwt-auth-role.json` - JWT role definition for TFC

---

Next Step: Review this assessment with your team, prioritize the remediation tasks based on risk/impact, and determine implementation timeline.
