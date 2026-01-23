---
created: 2026-01-23T14:14:02+00:00
modified: 2026-01-23T14:15:39+00:00
title: LCA-DP_Secret_Automation_Fix
---

## The Gap Analysis

I have identified exactly why your automated secret injection isn't working and how to fix it.

### 1. The Auth Blocker (`vault_k8s_auth.tf`)

Your VSO authentication role is currently hardcoded to **only** allow the `argocd` namespace.

- **Current:** `bound_claims = { sub = "system:serviceaccount:argocd:default" }`
- **Result:** When VSO in the `spicedb` namespace tries to authenticate, Vault rejects it.

### 2. The Missing Resource (`VaultStaticSecret`)

You have manually created the K8s secret, but there is no Terraform/HCL resource defining it. This is why you have to make manual "hotfixes".

### 3. Reflector Strategy

**Verdict:** Stop using Reflector for this. You already have VSO running in multiple namespaces (`spicedb`, `monitoring`, etc.). It is cleaner and more "GitOps" to let VSO directly manage the secret in each namespace.

---

## The Fix

Apply these two changes to your Terraform.

### Step 1: Open up the VSO Authentication

We need to allow the `default` service account in _any_ namespace (or specific ones) to authenticate.

**File:** `LCA-DP/vault_k8s_auth.tf`

```hcl
resource "vault_jwt_auth_backend_role" "vso" {
  # ... (keep existing lines)
  role_type = "jwt"

  # REPLACE THIS:
  # bound_claims = {
  #   sub = "system:serviceaccount:argocd:default"
  # }

  # WITH THIS (Wildcard approach):
  bound_claims_type = "glob"
  bound_claims = {
    sub = "system:serviceaccount:*:default" 
  }
}
```

### Step 2: Define the Secret in HCL

Add this resource to `LCA-DP/main.tf` (or a specific `secrets.tf`). This tells VSO to create the docker-registry secret in the `spicedb` namespace.

**File:** `LCA-DP/main.tf`

```hcl
resource "kubernetes_manifest" "spicedb_pull_secret" {
  manifest = {
    "apiVersion" = "secrets.hashicorp.com/v1beta1"
    "kind"       = "VaultStaticSecret"
    "metadata" = {
      "name"      = "fitfile-image-pull-secret"
      "namespace" = "spicedb"
    }
    "spec" = {
      "type" = "kubernetes.io/dockerconfigjson" # Creates a valid imagePullSecret
      
      "destination" = {
        "name"   = "fitfile-image-pull-secret"
        "create" = true
      }

      "vaultAuthRef" = "default" # Uses the VSO auth we just fixed
      
      "mount" = "central"
      "path"  = "azure/creds/acr-pull" # Matches your existing 'acr-reader' policy
      "refreshInterval" = "60s"
    }
  }
}
```
