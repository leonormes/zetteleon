---
aliases: []
confidence: 
created: 2025-12-18T12:53:18Z
epistemic: 
last_reviewed: 
modified: 2025-12-18T12:53:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Fitfile Bootstrap Debugging Resolution
type: 
uid: 
updated: 
---

## Resolution Summary: Fitfile Bootstrap Debugging

### Overview

We successfully debugged and deployed the `fitfile-bootstrap` Terraform project. This session resolved multiple blocking issues across Auth0, Grafana Cloud, and HCP Vault integrations.

### Key Resolutions

#### 1. Vault `403 Permission Denied`
**Issue:** Terraform failed to create the namespace `deployments/lca-prd-2` because `VAULT_NAMESPACE` was defaulting to root, but the token was for HCP.
**Root Cause:** HCP Vault requires operations to be contextually rooted in the `admin` namespace. Additionally, trying to create `deployments/child` directly from `admin` failed manual validation.
**Fix:**

1. **Environment:** Set `export VAULT_NAMESPACE="admin/deployments"` to target the parent directly.
2. **Code:** Updated `modules/vault-state/main.tf` to create a namespace with relative path `lca-prd-2` instead of absolute path `deployments/lca-prd-2`.
3. **State:** Manually created the namespace via CLI and used `terraform import` to align state.

#### 2. Grafana `409 Conflict` (Resource Not Found)
**Issue:** The `grafana_cloud_access_policy_token` resource failed with "Resource not found" even after adding a 60s sleep.
**Root Cause:** The Terraform Provider was passing the compound ID (`region:uuid`) to the API, but the API endpoint only expected the UUID.
**Fix:** Updated `modules/observability/main.tf` to use `.policy_id` (UUID only) instead of `.id`.

```hcl
access_policy_id = grafana_cloud_access_policy.bootstrap.policy_id
```

#### 3. Grafana `401 Unauthorized`
**Issue:** Terraform failed to destroy/replace the Access Policy.
**Root Cause:** The generated Grafana Cloud API token lacked the `accesspolicies:delete` scope.
**Fix:** Regenerated the token with the correct scopes.

#### 4. Grafana Race Condition
**Issue:** Token creation attempted before the Access Policy was fully propagated.
**Fix:** Added a `time_sleep` resource with `triggers`.

```hcl
resource "time_sleep" "wait_for_policy" {
  depends_on = [grafana_cloud_access_policy.bootstrap]
  create_duration = "60s"
  triggers = {
    # Forces sleep to reset if policy changes
    policy_id = grafana_cloud_access_policy.bootstrap.policy_id
  }
}
```

### Useful Commands (Reference)

For future debugging:

```bash
# Vault Diagnostics
vault token lookup
vault namespace list
# Targeted Creation
vault namespace create -namespace=admin/deployments <name>

# Terraform Import (Syntax)
terraform import -var-file="customers/wm-prod.tfvars" <resource_address> <id>
```
