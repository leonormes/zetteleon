---
aliases: [FitFile Secrets SoT, VSO Secrets Management, Secrets Management Source of Truth]
created: 2026-03-14T12:00:00Z
last-synthesis: 2026-03-14
modified: 2026-03-14T12:00:00+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [argocd, fitfile, kubernetes, secrets, security, sot, vault, vso]
title: SoT - FitFile VSO Secrets Management
trust-level: stable
type: SoT
---

## Minimum Viable Understanding (MVU)

FitFile uses HCP Vault as the encrypted source of truth for all secrets. The Vault Secrets Operator (VSO) syncs secrets into Kubernetes via declarative CRDs (`VaultStaticSecret`, `VaultDynamicSecret`, `VaultPKISecret`). Authentication uses JWT (OIDC) for remote HCP Vault—no callback to the cluster required. **Critical rule:** `spec.destination.overwrite: true` is mandatory for dynamic secrets or rotation will silently fail.

---

## Working Knowledge

### 1. Architecture Overview

```
HCP Vault (KV-v2, Azure, GitLab engines)
    ↓ (VaultAuth: JWT or AppRole)
Vault Secrets Operator (vault-secrets-operator-system)
    ↓ (watches CRDs, reconciles)
Kubernetes Secrets
    ↓ (volumeMount / envFrom / imagePullSecrets)
Application Pods
```

**Core components:**
- **VaultConnection**: Cluster-wide (`default` in `vault-secrets-operator-system`), links to HCP Vault URL
- **VaultAuth**: Per-namespace; defines auth method (JWT preferred, AppRole legacy)
- **VaultStaticSecret (VSS)**: Syncs KV-v2 static secrets
- **VaultDynamicSecret (VDS)**: Syncs lease-based secrets (e.g. Azure ACR credentials)
- **VaultPKISecret**: Short-lived TLS certificates
- **Reflector**: Mirrors secrets (e.g. image pull, TLS) across namespaces

### 2. Secret Types & Vault Sources

| Type | Vault Engine | Use Case | Example Path |
|:---|:---|:---|:---|
| **VaultStaticSecret** | KV-v2 (`secrets/`) | App credentials, API tokens, DB passwords | `secrets/argocd`, `secrets/application` |
| **VaultStaticSecret** | KV-v2 (`gitlab/`) | GitLab group access tokens | `gitlab/token` |
| **VaultDynamicSecret** | Azure | ACR image pull, Helm OCI registry | `azure/creds/acr-pull` |
| **VaultPKISecret** | PKI | Short-lived TLS | (cert-manager alternative) |

### 3. Vault Namespace Structure

| Vault Namespace | Purpose |
|:---|:---|
| `admin/deployments/{cluster}` | Per-cluster app secrets (argocd, application, argo-workflows) |
| `admin/central` | Shared infra (Azure ACR, GitLab group token) |

Path examples:
- `admin/deployments/lca-prd-2/secrets/argocd` → ArgoCD server secrets
- `admin/central/azure/creds/acr-pull` → ACR service principal (dynamic)
- `admin/central/gitlab/token` → GitLab group credential (repo-creds template)

### 4. Authentication: JWT vs AppRole

| Method | Mechanism | Use Case |
|:---|:---|:---|
| **JWT (OIDC)** | ServiceAccount token; Vault verifies via JWKS (no callback) | **Preferred** for HCP Vault + private AKS |
| **AppRole** | Static RoleID + SecretID in K8s Secret | Legacy; requires "Secret Zero" bootstrap |

**Why JWT:** No static credentials in cluster; ephemeral tokens; Vault validates JWT signature against cluster OIDC issuer. See [[SoT - VSO Authentication (JWT vs AppRole)]] for full rationale.

### 5. The Overwrite Golden Rule

**CRITICAL:** For any VSO-managed secret, especially dynamic:

```yaml
spec:
  destination:
    overwrite: true
```

If `overwrite: false` (default in older VSO), VSO will create the secret once but **never update it**. Dynamic credentials (ACR tokens) rotate in Vault—the K8s secret stays stale → `401 Unauthorized`.

### 6. ArgoCD Credential Paths (Two Separate Concerns)

| Credential Path | Consumer | K8s Secret Type | Purpose |
|:---|:---|:---|:---|
| **Image Pull Secret** | kubelet | `kubernetes.io/dockerconfigjson` | Pull container images at pod scheduling |
| **ArgoCD Repository Secret** | ArgoCD repo-server | Opaque + `argocd.argoproj.io/secret-type` | `helm registry login` for OCI charts |

Both may source from `azure/creds/acr-pull` but are different VDS CRs → different K8s Secrets. Fixing one does not fix the other.

**ArgoCD secret types:**
- `repo-creds`: Template match; **takes priority** over `repository`
- `repository`: Exact URL match

A stale `repo-creds` will silently override a valid `repository` secret.

### 7. Cross-Namespace Mirroring (Reflector)

When a secret must exist in multiple namespaces (e.g. image pull, TLS):

```yaml
reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "argocd,ohdsi,workflows"
```

Reflector auto-creates and updates mirrored copies.

### 8. Helm Integration (ffnode Chart)

- `renderValuesWithVaultSecretInExtraDeploy` processes `vaultSecrets` and `extraVaultSecrets`
- Renders VSS/VDS CRDs into ArgoCD Application `extraDeploy`
- Path templating: `{{ include "applicationVaultPath" . }}` → e.g. `application`, `ff-a-application`
- **Presets:** `mongodb`, `postgresql`, `auth0` reduce boilerplate

### 9. Secret Inventory (Key Mappings)

| K8s Secret | Vault Path | Component(s) | Injection |
|:---|:---|:---|:---|
| `mongodb` / `postgresql` | `application` | StatefulSets | env (existingSecret) |
| `fitconnect` / `ffcloud` | `application` | Deployments | volume `/secrets/` |
| `argo-postgres-config` | `argo-workflows` | Argo Workflows | env (secretKeyRef) |
| `argocd-secret` | `argocd` | ArgoCD server | env |
| `argocd-group-creds` | `gitlab/token` | ArgoCD repo-creds | ArgoCD label |
| `fitfile-image-pull-secret` | `azure/creds/acr-pull` | Image pull | imagePullSecrets |
| `cloudflare-issuer-api-token` | `cloudflare` | cert-manager | volume |
| `mesh-secrets` | `mesh` | fitconnect optout | volume |

### 10. Golden Path: Adding a New Secret

1. **Write to Vault:** `vault kv put secrets/{path} {key}={value}` (or HCP UI)
2. **Map in Helm:** Add to `vaultSecrets` or `extraVaultSecrets` in `values.yaml`
3. **Transformation:** Use `excludeRaw: true`, `excludes: [".*"]`, and `templates` to map Vault keys → K8s secret keys
4. **Sync:** ArgoCD syncs; VSO reconciles
5. **Verify:** `kubectl get vaultstaticsecret -n <ns>`; check `status.conditions[0].status == True`

---

## Current Understanding

### Known Issues & Anti-Patterns

- **KCH hardcoded secrets:** `vault-replacement-secrets.yaml` contains base64 credentials in git—critical debt
- **Double namespace:** Platform module prepending `admin/` to `vault_namespace` already containing it → `admin/admin/deployments/...`
- **OIDC issuer mismatch:** Cluster recreation can leave Vault JWT auth with stale OIDC issuer URL
- **ArgoCD inline values override:** Application spec `helm.values` can override `generated/values.yaml` → wrong Vault path deployed (see [[ARGO_VSO_ROOT_CAUSE]])
- **Template escaping:** Helm + VSO double-escaping (`'{{"{{`{{get .Secrets \"key\"}}`}}"}}'`) is error-prone
- **HCP Vault admin limit:** `Server admin limit exceeded` when too many concurrent dynamic cred requests

### Improvement Roadmap

- **Phase 1 (Security):** Rotate KCH secrets; migrate to VSO; enforce `refreshAfter` (5m app, 1h infra)
- **Phase 2 (DevEx):** Secret registry YAML; `secret-debug.sh`; local dev override (`global.vault.enabled: false`)
- **Phase 3 (Hardening):** VaultAuth as code; CUE validation in CI; `ignoreDifferences` for VSO status in ArgoCD

---

## Operational Protocols

| Need | Document |
|:---|:---|
| Troubleshooting stuck/stale secrets | [[Protocol - VSO Secret Management & Troubleshooting]] |
| ArgoCD OCI registry 401 | [[playbook_argocd_vso_oci_registry_auth_failure]] |
| VSO secret debugging | [[playbook_vso_secret_debugging]] |
| New deployment bootstrap | [[Protocol - Vault Deployment Secret Management]] |

---

## Related Documentation

- [[MoC - FitFile Secrets Management]]
- [[SoT - VSO Authentication (JWT vs AppRole)]]
- [[ARGO_VSO_ROOT_CAUSE]]
- [[lca-prd-2-vault-vso-audit]]
