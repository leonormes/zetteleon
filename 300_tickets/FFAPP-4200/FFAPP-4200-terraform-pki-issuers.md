---
aliases: []
confidence: 
created: 2025-09-09T10:09:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FFAPP-4200-terraform-pki-issuers
type:
uid: 
updated: 
version:
---

## PKI Engine Implementation Plan for Cert-Manager Integration

Based on your successful testing with the [pki_testing.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/pki_testing.tf:0:0-0:0) file, here's a comprehensive plan to implement optional PKI engine support across all deployments:

### 1. Enhanced Locals Configuration Structure

First, I'll extend the [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/locals.tf:0:0-0:0) to support PKI configuration per deployment:

Based on your successful PKI testing and requirements, here's a comprehensive implementation plan:

### **Phase 1: Extend Locals Configuration**

Add PKI configuration support to [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/locals.tf:0:0-0:0):

```hcl
locals {
  deployments = tomap({
    "testing" = {
      secrets = tomap({
        "application"    = {},
        "spicedb"        = {},
        "cloudflare"     = {},
        "monitoring"     = {},
        "argo-workflows" = {},
      })
      auto_create = true
      pki = {
        enabled = true
        allowed_domains = ["testing.fitfile.net"]
        role_name = "testing"
        cert_manager_approle_name = "cert-manager-testing-cluster"
      }
    }
    "staging" = {
      secrets = tomap({
        # ... existing secrets
      })
      auto_create = true
      pki = {
        enabled = true
        allowed_domains = ["staging.fitfile.net", "*.staging.fitfile.net"]
        role_name = "staging"
        cert_manager_approle_name = "cert-manager-staging-cluster"
      }
    }
    # ... other deployments without pki block (disabled by default)
  })

  # Computed locals for PKI-enabled deployments
  pki_enabled_deployments = {
    for name, deployment in local.deployments : name => deployment
    if try(deployment.pki.enabled, false)
  }
}
```

### **Phase 2: Create Modular PKI Resources**

Create new file `pki.tf` with resources based on your successful test:

```hcl
################################################################################
# INTERMEDIATE CA SETUP (Per PKI-Enabled Deployment)
################################################################################

# Enable PKI secrets engine for each deployment's Intermediate CA
resource "vault_mount" "pki_intermediate" {
  for_each = local.pki_enabled_deployments

  namespace             = vault_namespace.namespace[each.key].path_fq
  path                  = "pki_int_${each.key}"
  type                  = "pki"
  description           = "${title(each.key)} Intermediate CA for fitfile.com"
  max_lease_ttl_seconds = var.intermediate_ca_ttl
}

# Generate CSR for each deployment's Intermediate CA
resource "vault_pki_secret_backend_intermediate_cert_request" "intermediate" {
  for_each = local.pki_enabled_deployments

  depends_on  = [vault_mount.pki_intermediate]
  namespace   = vault_namespace.namespace[each.key].path_fq
  backend     = vault_mount.pki_intermediate[each.key].path
  type        = "internal"
  common_name = "${title(each.key)} Intermediate CA"
}

# Sign each intermediate CSR with the Root CA
resource "vault_pki_secret_backend_root_sign_intermediate" "intermediate" {
  for_each = local.pki_enabled_deployments

  depends_on = [
    vault_pki_secret_backend_root_cert.root,
    vault_pki_secret_backend_intermediate_cert_request.intermediate
  ]
  namespace   = vault_namespace.central_ns.path
  backend     = vault_mount.pki_root.path
  csr         = vault_pki_secret_backend_intermediate_cert_request.intermediate[each.key].csr
  common_name = "${title(each.key)} Intermediate CA"
  ttl         = var.intermediate_ca_ttl
  revoke      = true
}

# Import the signed certificate into each Intermediate CA engine
resource "vault_pki_secret_backend_intermediate_set_signed" "intermediate" {
  for_each = local.pki_enabled_deployments

  depends_on  = [vault_pki_secret_backend_root_sign_intermediate.intermediate]
  namespace   = vault_namespace.namespace[each.key].path_fq
  backend     = vault_mount.pki_intermediate[each.key].path
  certificate = vault_pki_secret_backend_root_sign_intermediate.intermediate[each.key].certificate
}

# PKI Role for each deployment
resource "vault_pki_secret_backend_role" "cert_manager" {
  for_each = local.pki_enabled_deployments

  namespace = vault_namespace.namespace[each.key].path_fq
  backend   = vault_mount.pki_intermediate[each.key].path
  name      = each.value.pki.role_name

  allowed_domains                 = each.value.pki.allowed_domains
  allow_subdomains               = true
  allow_bare_domains             = false
  allow_glob_domains             = false
  allow_wildcard_certificates    = true

  use_csr_sans                   = true
  allow_ip_sans                  = false

  key_type                       = "rsa"
  key_bits                       = 2048
  key_usage                      = ["DigitalSignature", "KeyEncipherment"]
  ext_key_usage                  = ["ServerAuth"]

  max_ttl                        = "720h"
  require_cn                     = false
  server_flag                    = true
  client_flag                    = false
}
```

### **Phase 3: Cert-Manager Policies and AppRoles**

Add to `pki.tf`:

```hcl
################################################################################
# CERT-MANAGER POLICIES AND APPROLES
################################################################################

# Policy for cert-manager in each PKI-enabled deployment
resource "vault_policy" "cert_manager" {
  for_each = local.pki_enabled_deployments

  namespace = vault_namespace.namespace[each.key].path_fq
  name      = "cert_manager"
  policy = <<-EOT
    # SIGN mode (recommended)
    path "${vault_mount.pki_intermediate[each.key].path}/sign/${each.value.pki.role_name}" {
      capabilities = ["update"]
    }

    # ISSUE mode (alternative)
    path "${vault_mount.pki_intermediate[each.key].path}/issue/${each.value.pki.role_name}" {
      capabilities = ["update"]
    }

    # Read issuing CA/chain
    path "${vault_mount.pki_intermediate[each.key].path}/ca" {
      capabilities = ["read"]
    }
    path "${vault_mount.pki_intermediate[each.key].path}/ca_chain" {
      capabilities = ["read"]
    }

    # Optional diagnostics
    path "${vault_mount.pki_intermediate[each.key].path}/roles/${each.value.pki.role_name}" {
      capabilities = ["read"]
    }
  EOT
}

# AppRole for cert-manager in each PKI-enabled deployment
resource "vault_approle_auth_backend_role" "cert_manager" {
  for_each = local.pki_enabled_deployments

  namespace      = vault_namespace.namespace[each.key].path_fq
  backend        = vault_auth_backend.auth[each.key].path
  role_name      = each.value.pki.cert_manager_approle_name
  token_policies = [vault_policy.cert_manager[each.key].name]
  token_ttl      = "60"
}

# Generate SecretID for each cert-manager AppRole
resource "vault_approle_auth_backend_role_secret_id" "cert_manager" {
  for_each = local.pki_enabled_deployments

  namespace = vault_namespace.namespace[each.key].path_fq
  backend   = vault_auth_backend.auth[each.key].path
  role_name = vault_approle_auth_backend_role.cert_manager[each.key].role_name
}
```

### **Phase 4: Update Outputs**

Modify [output.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/output.tf:0:0-0:0) to include PKI AppRoles:

```hcl
output "deployments_approle_roles" {
  description = "The approle role objects for each deployment application as a map"
  value = merge(
    tomap(vault_approle_auth_backend_role.auth_role),
    tomap(vault_approle_auth_backend_role.deployment_gitops_auth_role),
    tomap(vault_approle_auth_backend_role.cert_manager)
  )
}

output "deployments_approle_secret_ids" {
  description = "The approle role secret id objects for each deployment application as a map"
  sensitive   = true
  value = merge(
    tomap(vault_approle_auth_backend_role_secret_id.auth_role_secret_id),
    tomap(vault_approle_auth_backend_role_secret_id.deployment_gitops_role_secret_id),
    tomap(vault_approle_auth_backend_role_secret_id.cert_manager)
  )
}

# Dedicated PKI outputs for easier access
output "pki_cert_manager_approles" {
  description = "PKI cert-manager approle role IDs by deployment"
  sensitive   = true
  value = {
    for name, role in vault_approle_auth_backend_role.cert_manager : name => role.role_id
  }
}

output "pki_cert_manager_secret_ids" {
  description = "PKI cert-manager secret IDs by deployment"
  sensitive   = true
  value = {
    for name, secret in vault_approle_auth_backend_role_secret_id.cert_manager : name => secret.secret_id
  }
}
```

### **Implementation Steps**

### **Recommended Implementation Order**

1. **Start with a single deployment** (e.g., "testing") to validate the approach
2. **Extend locals.tf** with PKI configuration for that deployment
3. **Create pki.tf** with the modular resources
4. **Update outputs.tf** to include PKI AppRoles
5. **Test with `terraform plan`** to ensure no conflicts
6. **Gradually enable PKI for other deployments** as needed

### **Key Benefits of This Approach**

- **Optional per deployment**: Only deployments with `pki.enabled = true` get PKI resources
- **Domain flexibility**: Each deployment can specify its own allowed domains
- **Namespace isolation**: Each deployment gets its own intermediate CA in its namespace
- **Output integration**: PKI AppRoles are included in existing output structure
- **Backward compatible**: Existing deployments without PKI configuration remain unchanged

### **Migration From pki_testing.tf**

The new modular approach will replace your hardcoded test with:

- Dynamic resource creation based on configuration
- Consistent naming patterns across deployments
- Centralized domain management per deployment
- Integration with existing Vault namespace and auth structure

Would you like me to start implementing any specific part of this plan, or would you prefer to see the complete [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/locals.tf:0:0-0:0) extension first?
