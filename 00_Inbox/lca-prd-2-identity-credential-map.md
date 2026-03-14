---
created: 2026-02-24T16:16:15+00:00
modified: 2026-03-14T11:10:51+00:00
title: lca-prd-2-identity-credential-map
---

## LCA-PRD-2 Identity & Credential Map

Date: 2026-02-24

Cluster: lca-prd-2 (AKS, UK South)

---

### How It All Fits Together

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        HCP Vault Cloud                                  │
│                                                                         │
│  admin/                                                                 │
│  ├── auth/jwt-lca-prd-2          ← K8s service accounts authenticate   │
│  │     role: lca-prd-2              here via OIDC/JWT                   │
│  │     policies: argocd-secrets-lca-prd-2, acr-reader, gitlab-reader   │
│  │                                                                      │
│  ├── central/                                                           │
│  │   ├── azure/creds/acr-pull    ← Dynamic Azure SP for ACR            │
│  │   └── gitlab/token            ← Group Access Token (glpat-...)      │
│  │                                                                      │
│  └── deployments/lca-prd-2/                                             │
│      └── secrets/argocd          ← ArgoCD admin pw + server key         │
│                                     + GitLab deploy token               │
└─────────────────────────────────────────────────────────────────────────┘
          │
          │ JWT auth (OIDC issuer from AKS)
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Vault Secrets Operator (VSO)                          │
│                    Namespace: vault-secrets-operator-system              │
│                                                                         │
│  Watches VaultAuth, VaultStaticSecret, VaultDynamicSecret CRDs          │
│  Authenticates to Vault, syncs secrets into K8s Secrets                 │
└─────────────────────────────────────────────────────────────────────────┘
          │
          │ Creates/updates K8s Secrets
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Kubernetes Secrets                                    │
│                    Namespace: argocd (and others)                        │
│                                                                         │
│  ArgoCD reads secrets with specific labels:                             │
│  - argocd.argoproj.io/secret-type: repo-creds  → credential templates  │
│  - argocd.argoproj.io/secret-type: repository   → specific repo creds  │
│  - (no label) argocd-secret                     → server config         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Identity 1: Vault Authentication

Purpose: How the cluster proves its identity to Vault.

| Property | Value |
|----------|-------|
| What | Kubernetes service account JWT presented to Vault |
| Vault auth mount | `admin/auth/jwt-lca-prd-2` |
| Role name | `lca-prd-2` |
| Method | `jwt` |
| OIDC issuer | `https://uksouth.oic.prod-aks.azure.com/dbb3517b-…/102b5853-…` |
| Bound subject | `system:serviceaccount:*:default` (glob—any namespace, `default` SA) |
| Token TTL | 1 hour |
| Policies | `default`, `argocd-secrets-lca-prd-2`, `acr-reader`, `gitlab-reader` |

#### K8s CRD: VaultAuth

Deployed per-namespace. All identical, all reference the same Vault auth mount.

| K8s namespace | Name | Status |
|---------------|------|--------|
| `argocd` | `default` | ✅ Working |
| `argo` | `default` | ✅ Working |
| `cert-manager` | `default` | ✅ Working |
| `ingress-nginx` | `default` | ✅ Working |
| `vault-secrets-operator-system` | `default` | ✅ Working |
| `lca-prd-2` | `default` | ✅ Working |
| `monitoring` | `default` | ❌ Namespace doesn't exist yet |
| `spicedb` | `default` | ❌ Namespace doesn't exist yet |

#### ⚠️ Gotcha: OIDC Issuer URL

When the AKS cluster is recreated, the OIDC issuer URL changes. The Vault JWT auth config must be updated to match. This was the root cause of the initial failure in this session.

---

### Identity 2: ArgoCD Server Secrets

Purpose: ArgoCD's own admin password and server signing key.

| Property | Value |
|----------|-------|
| What | Static credentials for ArgoCD server operation |
| Vault namespace | `admin/deployments/lca-prd-2` |
| Vault mount | `secrets` (kv-v2) |
| Vault path | `argocd` |
| Vault keys | `admin_password`, `server_secret_key`, `unhashed_admin_password`, `gitlab_deploy_token_username`, `gitlab_deploy_token_password` |

#### K8s CRD: VaultStaticSecret

| Property | Value |
|----------|-------|
| Name | `argocd-secret` |
| K8s namespace | `argocd` |
| Destination secret | `argocd-secret` |
| ArgoCD label | None (consumed directly by ArgoCD server) |
| Refresh | 5 minutes |
| Rollout restart | `Deployment/argocd-server` |

#### K8s Secret Produced

| Key | Source | Purpose |
|-----|--------|---------|
| `admin.password` | `{{get.Secrets "admin_password"}}` | Bcrypt hash for ArgoCD admin login |
| `admin.passwordMtime` | Static: `2006-01-02T15:04:05Z` | Password modification timestamp |
| `server.secretkey` | `{{get.Secrets "server_secret_key"}}` | JWT signing key for ArgoCD sessions |

#### ⚠️ Gotcha: Double `admin/` Namespace

The platform module prepends `admin/` to `vault_namespace`. If the Terraform local already includes `admin/`, you get `admin/admin/deployments/lca-prd-2` which doesn't exist in Vault. The local should be `deployments/lca-prd-2` (without the `admin/` prefix).

---

### Identity 3: GitLab Deploy Token (Per-Repo)

Purpose: Authenticate ArgoCD to the `deployment.git` Helm chart repository.

| Property | Value |
|----------|-------|
| What | GitLab Deploy Token scoped to `fitfile/deployment.git` |
| Vault namespace | `admin/deployments/lca-prd-2` |
| Vault mount | `secrets` (kv-v2) |
| Vault path | `argocd` |
| Vault keys | `gitlab_deploy_token_username`, `gitlab_deploy_token_password` |
| GitLab username | `argocd-test` |
| GitLab scope | Deploy token (read_repository) on the specific project |

#### K8s CRD: VaultStaticSecret

| Property | Value |
|----------|-------|
| Name | `argocd-repo-fitfile-deployment-repo` |
| K8s namespace | `argocd` |
| Destination secret | `argocd-repo-fitfile-deployment-repo` |
| ArgoCD label | `argocd.argoproj.io/secret-type: repository` |
| Refresh | 30 minutes |

#### K8s Secret Produced

| Key | Source | Purpose |
|-----|--------|---------|
| `url` | Static: `https://gitlab.com/fitfile/deployment.git` | Repo URL ArgoCD matches against |
| `name` | Static: `fitfile-deployment` | Display name |
| `type` | Static: `git` | Credential type |
| `username` | `{{get.Secrets "gitlab_deploy_token_username"}}` | GitLab deploy token username |
| `password` | `{{get.Secrets "gitlab_deploy_token_password"}}` | GitLab deploy token password |

#### ⚠️ Gotcha: ArgoCD Credential Priority

ArgoCD matches `repository` secrets (exact URL) before `repo-creds` templates (prefix). If this secret exists with empty username/password, it blocks the group-creds template from matching. This caused the git auth failures until the Vault keys were populated.

---

### Identity 4: GitLab Group Access Token (Template)

Purpose: Credential template for all repos under `https://gitlab.com/fitfile/*`.

| Property | Value |
|----------|-------|
| What | GitLab Group Access Token for the `fitfile` group |
| Vault namespace | `admin/central` |
| Vault mount | `gitlab` (kv-v2) |
| Vault path | `token` |
| Vault keys | `value`, `description`, `expires_at`, `scopes` |
| GitLab scopes | `read_api`, `read_repository` |
| Expires | 2027-01-25 |

#### K8s CRD: VaultStaticSecret

| Property | Value |
|----------|-------|
| Name | `argocd-group-creds` |
| K8s namespace | `argocd` |
| Destination secret | `argocd-group-creds` |
| ArgoCD label | `argocd.argoproj.io/secret-type: repo-creds` |

#### K8s Secret Produced

| Key | Source | Purpose |
|-----|--------|---------|
| `url` | Static: `https://gitlab.com/fitfile` | URL prefix ArgoCD matches against |
| `name` | Static: `fitfile-group` | Display name |
| `type` | Static: `git` | Credential type |
| `username` | Static: `oauth2` | Required for Group Access Tokens |
| `password` | `{{.Secrets.value }}` | The `glpat-…` token value |

#### ⚠️ Gotcha: Token Scope Vs Repo Access

The group access token has `read_repository` scope but was confirmed to not have access to `fitfile/customers/nwsde/lca-infra-prd.git`. This is likely because the token is scoped to the `fitfile` group but the `customers/nwsde` subgroup has restricted access. A separate credential or broader-scoped token is needed for the values repo.

#### ⚠️ Gotcha: excludeRaw

Without `excludeRaw: true` and `excludes: [".*"]` in the transformation, VSO copies all raw Vault keys into the K8s secret, producing 10 keys instead of 5. ArgoCD may ignore the extras, but it's messy.

---

### Identity 5: Azure Container Registry (ACR)—ArgoCD OCI/Helm

Purpose: Authenticate ArgoCD to `fitfileregistry.azurecr.io` for pulling Helm charts stored in ACR.

| Property | Value |
|----------|-------|
| What | Dynamic Azure Service Principal credentials |
| Vault namespace | `admin/central` |
| Vault mount | `azure` (azure secrets engine) |
| Vault path | `creds/acr-pull` |
| Vault keys | `client_id`, `client_secret` (generated dynamically) |

#### K8s CRD: VaultDynamicSecret

| Property | Value |
|----------|-------|
| Name | `argocd-repo-creds-acr` |
| K8s namespace | `argocd` |
| Destination secret | `argocd-repo-creds-acr` |
| ArgoCD label | `argocd.argoproj.io/secret-type: repository` |

#### K8s Secret Produced

| Key | Source | Purpose |
|-----|--------|---------|
| `url` | Static: `https://fitfileregistry.azurecr.io` | Registry URL |
| `name` | Static: `ACR` | Display name |
| `type` | Static: `helm` | Credential type |
| `username` | `{{.Secrets.client_id }}` | Azure SP client ID |
| `password` | `{{.Secrets.client_secret }}` | Azure SP client secret |

#### ⚠️ Gotcha: Duplicate VaultDynamicSecrets

Three VaultDynamicSecrets target ACR credentials in the argocd namespace:

| Name | Origin | Destination | Issue |
|------|--------|-------------|-------|
| `argocd-repo-creds-acr` | `main.tf` | `argocd-repo-creds-acr` | ✅ Working, correct pattern |
| `argocd-pull` | Platform module | `argocd-acr-pull-secret` | ⚠️ Ownership conflict with -test |
| `argocd-pull-test` | Manual/test leftover | `argocd-acr-pull-secret` | ⚠️ Should be deleted |

`argocd-pull` and `argocd-pull-test` both target the same destination secret, causing VSO ownership conflicts. Delete `argocd-pull-test` at minimum.

---

### Identity 6: Azure Container Registry (ACR)—Image Pull

Purpose: Allow Kubernetes pods to pull container images from `fitfileregistry.azurecr.io`.

| Property | Value |
|----------|-------|
| What | Dynamic Azure Service Principal credentials, formatted as `kubernetes.io/dockerconfigjson` |
| Vault namespace | `admin/central` |
| Vault mount | `azure` (azure secrets engine) |
| Vault path | `creds/acr-pull` |
| Vault keys | `client_id`, `client_secret` (generated dynamically) |

#### K8s CRD: VaultDynamicSecret (per namespace)

| Property | Value |
|----------|-------|
| Name | `fitfile-image-pull-secret` |
| K8s namespaces | `argo`, `argocd`, `cert-manager`, `ingress-nginx`, `monitoring`, `spicedb`, `vault-secrets-operator-system`, `lca-prd-2` |
| Destination secret | `fitfile-image-pull-secret` |
| Secret type | `kubernetes.io/dockerconfigjson` |

#### K8s Secret Produced

| Key | Source | Purpose |
|-----|--------|---------|
| `.dockerconfigjson` | Template combining `client_id` and `client_secret` | Docker auth config for `fitfileregistry.azurecr.io` |

#### ⚠️ Gotcha: HCP Vault Admin Limit

Multiple namespaces each requesting dynamic Azure credentials simultaneously can hit HCP Vault's admin/rate limit: `Server admin limit exceeded`. This affects all VaultDynamicSecrets using `azure/creds/acr-pull`.

---

### Vault Policies Summary

All policies are in `admin` namespace, evaluated relative to child namespaces.

#### `argocd-secrets-lca-prd-2`

```hcl
path "deployments/lca-prd-2/secrets/data/*" {
  capabilities = ["read", "list"]
}
```

Grants: Read all kv-v2 secrets under `admin/deployments/lca-prd-2/secrets/`.

Used by: Identity 2 (ArgoCD server secrets), Identity 3 (GitLab deploy token).

#### `acr-reader`

```hcl
path "central/azure/creds/acr-pull" {
  capabilities = ["read"]
}
```

Grants: Generate dynamic Azure SP credentials from `admin/central/azure/`.

Used by: Identity 5 (ACR Helm/OCI), Identity 6 (Image pull).

#### `gitlab-reader`

```hcl
path "central/gitlab/data/token" {
  capabilities = ["read"]
}
```

Grants: Read the GitLab group token from `admin/central/gitlab/`.

Used by: Identity 4 (GitLab group access token).

---

### ArgoCD Credential Matching—How It Works

ArgoCD evaluates credentials in this priority order:

```
1. repository secrets  (exact URL match)     ← highest priority
2. repo-creds secrets  (URL prefix match)    ← fallback / template
```

#### Current Matching for the Application `ff-lca-prd-2`

| Source | Repo URL | Matched Secret | Type | Working |
|--------|----------|---------------|------|---------|
| Source 1 (charts) | `https://gitlab.com/fitfile/deployment.git` | `argocd-repo-fitfile-deployment-repo` | `repository` (exact) | ✅ |
| Source 2 (values) | `https://gitlab.com/fitfile/customers/nwsde/lca-infra-prd.git` | `argocd-group-creds` | `repo-creds` (prefix) | ❌ Token lacks access to this subgroup |

#### The Values Repo Problem

The `argocd-group-creds` template matches the URL prefix but the `glpat-…` token cannot access `fitfile/customers/nwsde/lca-infra-prd.git`. Resolution options:

1. Broaden the group token's access in GitLab to include the `customers` subgroup
2. Create a deploy token on the `lca-infra-prd` project and store it in Vault
3. Create a second group token at the `fitfile/customers` or `fitfile/customers/nwsde` subgroup level

---

### Open Issues Checklist

| # | Severity | Issue | Resolution |
|---|----------|-------|------------|
| 1 | 🔴 | Values repo (`lca-infra-prd.git`) auth failure | Needs token with access to `customers/nwsde` subgroup |
| 2 | 🟡 | `argocd-pull-test` VaultDynamicSecret leftover | Delete from cluster |
| 3 | 🟡 | `argocd-pull` / `argocd-pull-test` ownership conflict | Delete `-test`, potentially `-pull` too |
| 4 | 🟡 | `gitlab-reader` policy created manually | Codify in Terraform |
| 5 | 🟡 | Vault JWT role policy update done manually | Codify in Terraform |
| 6 | 🟡 | OIDC issuer URL requires manual update on cluster recreation | Create runbook or automate |
| 7 | 🟡 | `monitoring` and `spicedb` namespaces don't exist | Create or let ArgoCD apps create them |
| 8 | 🟢 | HCP Vault admin limit on dynamic creds | Review HCP tier / reduce concurrent requests |
