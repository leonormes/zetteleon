---
aliases: []
confidence: 
created: 2025-09-09T10:31:01Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: PKI Engine Implementation Summary
type:
uid: 
updated: 
version:
---

## ✅ **Work Completed**

Successfully implemented optional PKI engine support for cert-manager integration across all deployments, based on the successful [pki_testing.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/pki_testing.tf:0:0-0:0) proof-of-concept.

## 🔧 **Implementation Details**

### **1. Configuration Structure**

Extended [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/locals.tf:0:0-0:0) with optional PKI configuration per deployment:

```hcl
# Example: Testing deployment with PKI enabled
"testing" = {
  secrets = { /* existing secrets */ }
  auto_create = true
  pki = {
    enabled                   = true
    allowed_domains           = ["testing.fitfile.net"]
    role_name                 = "testing"
    cert_manager_approle_name = "cert-manager-testing-cluster"
  }
}
```

### **2. Modular PKI Resources**

Created [pki.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/pki.tf:0:0-0:0) with production-ready resources based on the successful test:

**Test Implementation** → **Production Implementation**

```hcl
# TEST: Hardcoded for "testing" deployment
resource "vault_mount" "testing_pki_intermediate" {
  namespace = vault_namespace.namespace["testing"].path_fq
  path      = "pki_int_testing"
}

# PRODUCTION: Dynamic for all PKI-enabled deployments
resource "vault_mount" "pki_intermediate" {
  for_each  = local.pki_enabled_deployments
  namespace = vault_namespace.namespace[each.key].path_fq
  path      = "pki_int_${each.key}"
}
```

### **3. Cert-Manager Integration**

Replicated the successful cert-manager policy pattern:

**Test Policy** → **Production Policy**

```hcl
# TEST: Single policy for testing
resource "vault_policy" "testing_cert_manager" {
  namespace = vault_namespace.namespace["testing"].path_fq
  name      = "cert_manager"
  policy    = "path pki_int_testing/sign/testing { capabilities = [\"update\"] }"
}

# PRODUCTION: Dynamic policies per PKI deployment
resource "vault_policy" "cert_manager" {
  for_each  = local.pki_enabled_deployments
  namespace = vault_namespace.namespace[each.key].path_fq
  name      = "cert_manager"
  policy    = "path pki_int_${each.key}/sign/${each.value.pki.role_name} { capabilities = [\"update\"] }"
}
```

### **4. Output Integration**

Extended `outputs.tf` to include PKI AppRoles in terraform output scripts:

```hcl
output "deployments_approle_roles" {
  value = merge(
    tomap(vault_approle_auth_backend_role.auth_role),
    tomap(vault_approle_auth_backend_role.deployment_gitops_auth_role),
    tomap(vault_approle_auth_backend_role.cert_manager)  # ← New PKI AppRoles
  )
}
```

## 🎯 **Key Features Delivered**

- ✅ **Optional per deployment** - Only deployments with `pki.enabled = true` get PKI resources
- ✅ **Namespace isolation** - Each deployment gets intermediate CA in its own namespace
- ✅ **Domain flexibility** - Each deployment specifies allowed domains via `allowed_domains` list
- ✅ **Backward compatible** - Existing deployments unaffected
- ✅ **Output integration** - PKI AppRoles included in terraform output scripts

## 📊 **Current Status**

- **PKI-enabled deployments**: `testing`, `hie-prod-34`
- **Terraform validation**: ✅ Passing
- **Resource conflicts**: ✅ Resolved (test file commented out)
- **Ready for deployment**: ✅ Yes

The implementation successfully scales the proven [pki_testing.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault/pki_testing.tf:0:0-0:0) approach to support all deployments with optional PKI configuration.
