---
created: 2026-02-24T14:30:43+00:00
modified: 2026-03-14T11:10:51+00:00
title: lca-prd-2-vault-vso-audit
---

## LCA-PRD-2 Vault / VSO / ArgoCD Credential Audit

Date: 2026-02-24

Cluster: lca-prd-2 (AKS, UK South)

---

### Current State

#### Vault Structure

| Namespace | Mount | Path | Keys | Purpose |
|-----------|-------|------|------|---------|
| `admin/central` | `gitlab/` (kv-v2) | `token` | `description`, `expires_at`, `scopes`, `value` | GitLab Group Access Token (expires 2027-01-25) |
| `admin/central` | `azure/` (azure) | `creds/acr-pull` | `client_id`, `client_secret` (dynamic) | ACR service principal |
| `admin/deployments/lca-prd-2` | `secrets/` (kv-v2) | `argocd` | `admin_password`, `server_secret_key`, `unhashed_admin_password` | ArgoCD server secrets |

#### Vault Auth

| Field | Value |
|-------|-------|
| Auth mount | `admin/auth/jwt-lca-prd-2` |
| Role | `lca-prd-2` |
| Method | `jwt` |
| OIDC Issuer | `https://uksouth.oic.prod-aks.azure.com/…/102b5853-a8d1-4ced-9d5e-d72787b21dfa/` |
| Bound SA | `system:serviceaccount:*:default` (glob) |
| TTL | 1h |

#### Vault Policies (namespace: admin)

| Policy | Path | Capabilities |
|--------|------|-------------|
| `argocd-secrets-lca-prd-2` | `deployments/lca-prd-2/secrets/data/*` | read, list |
| `acr-reader` | `central/azure/creds/acr-pull` | read |
| `gitlab-reader` | `central/gitlab/data/token` | read |

#### VSO Resources in `argocd` Namespace

##### VaultAuth

| Name | Method | Mount | Namespace | Status |
|------|--------|-------|-----------|--------|
| `default` | jwt | `jwt-lca-prd-2` | `admin` | ✅ Valid |

##### VaultStaticSecrets

| Name | Mount | Path | Vault NS | Destination | Status |
|------|-------|------|----------|-------------|--------|
| `argocd-secret` | `secrets` | `argocd` | `admin/deployments/lca-prd-2` | `argocd-secret` | ✅ Synced |
| `argocd-group-creds` | `gitlab` | `token` | `admin/central` | `argocd-group-creds` | ✅ Synced |

##### VaultDynamicSecrets

| Name | Mount | Path | Vault NS | Destination | Status | Notes |
|------|-------|------|----------|-------------|--------|-------|
| `argocd-pull` | `azure` | `creds/acr-pull` | `admin/central` | `argocd-acr-pull-secret` | ⚠️ Ownership conflict | From platform module |
| `argocd-pull-test` | `azure` | `creds/acr-pull` | `admin/central` | `argocd-acr-pull-secret` | ⚠️ Ownership conflict | Test leftover, same dest |
| `argocd-repo-creds-acr` | `central` | `azure/creds/acr-pull` | `admin` | `argocd-repo-creds-acr` | ✅ Working | From main.tf |
| `fitfile-image-pull-secret` | `azure` | `creds/acr-pull` | `admin/central` | `fitfile-image-pull-secret` | ✅ Working | For image pulling |

#### ArgoCD Credential Secrets

| Secret | Type Label | URL | Auth Working |
|--------|-----------|-----|-------------|
| `argocd-group-creds` | `repo-creds` | `https://gitlab.com/fitfile` | ✅ username=oauth2, password=glpat-… |
| `argocd-acr-pull-secret` | `repository` | `fitfileregistry.azurecr.io` | ✅ |
| `argocd-repo-creds-acr` | `repository` | `https://fitfileregistry.azurecr.io` | ✅ |

---

### Issues Found

#### 🔴 Critical (fixed during This session)

1. OIDC issuer mismatch—Vault JWT auth had stale OIDC issuer URL from previous cluster. Fixed via `vault write` on auth config.
2. Double `admin/` namespace—Platform module prepended `admin/` to `vault_namespace` which already included it. VaultStaticSecrets pointed at `admin/admin/deployments/lca-prd-2`. Fixed in Terraform locals.
3. Missing VaultAuth CRDs—`default` VaultAuth not created in namespaces by Terraform before VSO tried to reconcile. Terraform ordering issue in platform module.

#### 🟡 Medium (to Be Cleaned up)

1. `argocd-pull` / `argocd-pull-test` ownership conflict—Both target the same destination secret `argocd-acr-pull-secret`. The `-test` resource is a leftover and should be deleted.
2. Duplicate ACR repository secrets—`argocd-acr-pull-secret` and `argocd-repo-creds-acr` both provide ACR credentials to ArgoCD. Only one is needed.
3. `argocd-repo-fitfile-deployment-repo` in Helm extraObjects—Still defined in the platform module's Helm values. Points at `secrets/argocd` which doesn't have GitLab deploy token keys. Should be removed—the group-creds template covers all fitfile repos.
4. Raw Vault data leaking into secrets—`argocd-group-creds` has 10 keys instead of 5. Missing `excludeRaw: true` and `excludes: [".*"]` in the VaultStaticSecret transformation.
5. HCP Vault admin limit errors—`Server admin limit exceeded` when generating dynamic Azure creds. Likely too many concurrent credential requests across namespaces.

#### 🟢 Low (future improvements)

1. Missing namespaces—`monitoring` and `spicedb` don't exist yet, causing VaultAuth and image pull secret creation failures.
2. Vault policy/role management not in Terraform—The `gitlab-reader` policy and role update were done manually. Should be codified.

---

### Target State (Best Practice)

#### Principle: One Credential Per Concern

| Concern | Mechanism | VSO Type | Vault Source | ArgoCD Label |
|---------|-----------|----------|-------------|-------------|
| All fitfile Git repos | Group credential template | VaultStaticSecret | `admin/central` → `gitlab/token` | `repo-creds` |
| ACR Helm/OCI registry | Repository credential | VaultDynamicSecret | `admin/central` → `azure/creds/acr-pull` | `repository` |
| ArgoCD server config | Server secret | VaultStaticSecret | `admin/deployments/lca-prd-2` → `secrets/argocd` | (none) |
| Container image pull | Per-namespace dockerconfig | VaultDynamicSecret | `admin/central` → `azure/creds/acr-pull` | (none) |

#### What to Remove

```
# VaultDynamicSecrets to delete
argocd-pull-test        # test leftover, conflicts with argocd-pull
argocd-pull             # duplicate of argocd-repo-creds-acr (pick one pattern)

# Helm extraObjects to remove from platform module
argocd-repo-fitfile-deployment-repo  # group-creds template covers all repos
```

#### Recommended `argocd-group-creds` VaultStaticSecret

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: argocd-group-creds
  namespace: argocd
spec:
  type: kv-v2
  mount: gitlab
  path: token
  namespace: admin/central
  vaultAuthRef: default
  refreshAfter: 30m
  destination:
    name: argocd-group-creds
    create: true
    overwrite: true
    labels:
      argocd.argoproj.io/secret-type: repo-creds
    transformation:
      excludeRaw: true
      excludes:
        - ".*"
      templates:
        name:
          text: fitfile-group
        type:
          text: git
        url:
          text: "https://gitlab.com/fitfile"
        username:
          text: oauth2
        password:
          text: "{{ .Secrets.value }}"
```

#### Recommended `argocd-repo-creds-acr` VaultDynamicSecret

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: argocd-repo-creds-acr
  namespace: argocd
spec:
  mount: azure
  path: creds/acr-pull
  namespace: admin/central
  vaultAuthRef: default
  destination:
    name: argocd-repo-creds-acr
    create: true
    overwrite: true
    labels:
      argocd.argoproj.io/secret-type: repository
    transformation:
      excludeRaw: true
      excludes:
        - ".*"
      templates:
        name:
          text: ACR
        type:
          text: helm
        url:
          text: "https://fitfileregistry.azurecr.io"
        enableOCI:
          text: "true"
        username:
          text: "{{ .Secrets.client_id }}"
        password:
          text: "{{ .Secrets.client_secret }}"
```

---

### Cleanup Checklist

- [ ] Delete `argocd-pull-test` VaultDynamicSecret
- [ ] Delete `argocd-pull` VaultDynamicSecret (if keeping `argocd-repo-creds-acr` pattern)
- [ ] Remove `argocd-repo-fitfile-deployment-repo` from Helm extraObjects in platform module
- [ ] Add `excludeRaw: true` and `excludes: [".*"]` to `argocd-group-creds` transformation
- [ ] Codify `gitlab-reader` Vault policy in Terraform
- [ ] Codify Vault JWT auth role policy attachment in Terraform
- [ ] Codify OIDC issuer URL update process (runbook for cluster recreation)
- [ ] Resolve HCP Vault admin limit (check tier/concurrent cred limits)
- [ ] Create `monitoring` and `spicedb` namespaces (or ensure ArgoCD apps create them)
