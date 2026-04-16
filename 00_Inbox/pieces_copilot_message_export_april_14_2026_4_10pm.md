*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 14, 2026 - 4:10 PM*
---
# Secure M2M Credential Management with HCP Vault and VSO

Based on your existing infrastructure (I can see you've been actively working with Vault namespaces, JWT auth, and VSO patterns in [lca-prd-2](https://app.terraform.io/app/FITFILE-Platforms/workspaces/lca-prd-2/runs)), here are the main options and best practices for receiving external credentials from partners like the Eastern England SDE.

---

## Options Overview

| Approach | Security | Automation | Flexibility | Complexity |
|----------|----------|------------|-------------|------------|
| **Static KV Secrets + VSO** | Medium | High | Medium | Low |
| **Vault GitHub Secrets Engine** | High | Very High | Medium | Medium |
| **GitHub App + Dynamic Tokens** | Very High | Very High | High | Medium-High |
| **Partner-Push to Shared Namespace** | High | High | Very High | Medium |

---

## Option 1: Static KV Secrets with VSO (Current Pattern)

This is essentially what you're already doing with GitLab credentials. EoE provides a GitHub PAT or deploy token, you store it in Vault, and VSO syncs it to K8s.

```yaml
# VaultStaticSecret pattern (similar to your gitlab-repository-credentials)
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: eoe-github-credentials
  namespace: argocd
spec:
  type: kv-v2
  mount: secrets
  vaultAuthRef: default
  path: external/eoe/github-credentials  # Suggest a clear namespace for external partner secrets
  destination:
    name: eoe-github-credentials
    create: true
  refreshAfter: 60s
```

**Pros:** Simple, you understand it well already.  
**Cons:** Long-lived static tokens, manual rotation burden on EoE.

---

## Option 2: Vault GitHub Secrets Engine (Dynamic Credentials)

This was mentioned in your call earlier today (~1:33 PM) — someone referenced "a Vault plugin that works with GitHub secrets engine."

Vault's [GitHub Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/github) can generate **short-lived installation tokens** for a GitHub App, eliminating static PATs entirely.

### How It Works:
1. EoE creates a **GitHub App** in their org and installs it on the target repo(s)
2. EoE provides you with the **App ID** and **Private Key**
3. You configure the GitHub secrets engine in Vault:

```bash
# Enable the secrets engine
vault secrets enable -namespace=admin/deployments/lca-prd-2 -path=github github

# Configure with the GitHub App credentials
vault write -namespace=admin/deployments/lca-prd-2 github/config \
  app_id=<APP_ID> \
  private_key=@github-app-private-key.pem
```

4. Workloads request tokens dynamically:

```bash
vault read -namespace=admin/deployments/lca-prd-2 github/token
# Returns a 1-hour token with only the permissions granted to the App
```

### VSO Integration for Dynamic Secrets:
```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: eoe-github-token
  namespace: argocd
spec:
  mount: github
  path: token
  vaultAuthRef: default
  destination:
    name: eoe-github-token
    create: true
  renewalPercent: 67  # Renew when 67% of TTL has elapsed
```

**Pros:** Short-lived tokens (1 hour default), automatic rotation, no static credentials.  
**Cons:** Requires EoE to create and maintain a GitHub App; App private key is still sensitive.

---

## Option 3: Partner-Push Pattern (Recommended for Flexibility)

This is the most flexible pattern for **multiple external partners** providing credentials. You establish a **trust boundary** via a shared Vault namespace that partners can write to.

### Architecture:
```
┌─────────────────────────────────────────────────────────────────────┐
│                         HCP Vault                                   │
├─────────────────────────────────────────────────────────────────────┤
│  admin/external/eoe/                 ← EoE writes here              │
│    └─ secrets/                                                      │
│        ├─ github-credentials         (KV secret from EoE)           │
│        └─ s3-credentials             (Future: other creds)          │
│                                                                     │
│  admin/deployments/lca-prd-2/        ← You read from here via VSO   │
│    └─ VSO syncs from external/eoe/*                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Terraform Configuration:
```hcl
# Create a namespace for the external partner
resource "vault_namespace" "eoe" {
  path      = "external/eoe"
  namespace = "admin"
}

# Create a KV mount in their namespace
resource "vault_mount" "eoe_secrets" {
  namespace = vault_namespace.eoe.path_fq
  path      = "secrets"
  type      = "kv-v2"
}

# Policy allowing EoE to write (but not read back or delete)
resource "vault_policy" "eoe_writer" {
  namespace = "admin"
  name      = "eoe-external-writer"
  policy    = <<-EOT
    path "external/eoe/secrets/data/*" {
      capabilities = ["create", "update"]
    }
    path "external/eoe/secrets/metadata/*" {
      capabilities = ["list"]
    }
  EOT
}

# Policy allowing your workloads to read
resource "vault_policy" "eoe_reader" {
  namespace = vault_namespace.customer_ns[0].path_fq  # Your deployment namespace
  name      = "eoe-secrets-reader"
  policy    = <<-EOT
    path "admin/external/eoe/secrets/data/*" {
      capabilities = ["read", "list"]
    }
  EOT
}
```

### Auth Method for EoE:
You could provide EoE with:
- **AppRole credentials** (role_id + secret_id) scoped to the `eoe-external-writer` policy
- **OIDC/JWT auth** if they have an identity provider
- **Userpass** (simplest, least secure)

```hcl
# AppRole for EoE to authenticate and write secrets
resource "vault_approle_auth_backend_role" "eoe" {
  namespace       = "admin"
  backend         = "approle"
  role_name       = "eoe-external"
  token_policies  = ["eoe-external-writer"]
  token_ttl       = 3600
  token_max_ttl   = 86400
}
```

**Pros:** 
- Clear separation of concerns (they write, you read)
- Scales to multiple partners (create `external/partner-b/`, etc.)
- Audit trail shows who wrote what

**Cons:** Requires EoE to interact with Vault (may be unfamiliar for them)

---

## Best Practice Recommendations

1. **Use the GitHub Secrets Engine if possible** — eliminates static PATs entirely
2. **Namespace isolation** — keep external partner secrets in `admin/external/<partner>/`
3. **Least privilege policies** — EoE should only be able to write, not read or delete
4. **Audit everything** — HCP Vault's audit logs will capture all read/write operations
5. **Rotate the bootstrap credentials** — if using AppRole for partner auth, rotate `secret_id` periodically
6. **Document the handoff** — create a runbook for EoE explaining how to authenticate and push secrets

---

## Quick Start Recommendation

Given that EoE may not be familiar with Vault, I'd suggest a **hybrid approach**:

1. **Short-term:** Use **Option 1** (Static KV + VSO) — EoE gives you a GitHub App private key or PAT, you store it
2. **Medium-term:** Migrate to **Option 2** (GitHub Secrets Engine) using that same GitHub App
3. **Long-term:** Establish **Option 3** (Partner-Push) as the standard pattern for all external credential handoffs

Would you like me to draft a specific Terraform module or a handoff document for EoE?