---
aliases: [FitFile Secrets SoT, Secrets Management Source of Truth, VSO Secrets Management]
created: 2026-03-14T12:00:00Z
last_synthesis: 2026-03-28
modified: 2026-03-30T11:20:20+00:00
source_of_truth: true
status: evergreen
synthesis-count: 2
tags: [argocd, fitfile, kubernetes, secrets, security, sot, vault, vso]
title: SoT - FitFile VSO Secrets Management
trust-level: stable
type: SoT
---

## Minimum Viable Understanding (MVU)

FitFile uses HCP Vault as the encrypted source of truth for all secrets. The Vault Secrets Operator (VSO) syncs secrets into Kubernetes via a linked chain of declarative CRDs. Authentication uses JWT (OIDC) for remote HCP Vault, bound to the cluster's OIDC issuer. **Critical Rule**: `spec.destination.overwrite: true` is mandatory for dynamic secrets. **Verification**: `status.conditions[0].status == "True"` in the CRD.

---

## Working Knowledge

### 1. Architecture Overview: The Linked Chain

VSO operates through a chain of dependencies. If any link is broken, the produced Kubernetes Secret becomes stale or empty.

```
VaultConnection (Where) ← VaultAuth (Who) ← VaultStaticSecret/VaultDynamicSecret (What)
```

- **VaultConnection**: Cluster-wide (`default` in `vault-secrets-operator-system`), links to the HCP Vault endpoint.
- **VaultAuth**: Per-namespace; defines the authentication method and targets a specific Vault Namespace (e.g., `admin/deployments/lca-prd-2`).
- **VaultStaticSecret (VSS)**: Syncs static KV-v2 data.
- **VaultDynamicSecret (VDS)**: Syncs dynamic, lease-based data (e.g., Azure ACR credentials).

### 2. Identity Types & Mappings

| Identity Concern | Mechanism | Vault Source | ArgoCD / K8s Context |
|:---|:---|:---|:---|
| **ArgoCD Server** | VSS | `secrets/argocd` | `argocd-secret` (admin pw, signing key) |
| **GitLab Deploy** | VSS | `secrets/argocd` | `repository` label (per-repo deploy token) |
| **GitLab Group** | VSS | `central/gitlab/token` | `repo-creds` label (Template for `fitfile/*`) |
| **ACR Registry** | VDS | `central/azure/creds/acr-pull` | `repository` label (Helm OCI registry) |
| **Image Pull** | VDS | `central/azure/creds/acr-pull` | `dockerconfigjson` (kubelet scheduling) |

### 3. ArgoCD Credential Resolution Priority

ArgoCD matches repo URLs against secrets in this priority:
1. **`repository` secrets**: Exact URL match (Highest Priority).
2. **`repo-creds` secrets**: Prefix match (Fallback/Template).

> [!warning] The Shadowing Trap
> A `repository` secret with empty or stale credentials will block a perfectly valid `repo-creds` template from working. Ensure `repository` secrets are only created when per-repo tokens are explicitly required.

### 4. Authentication: JWT Vs AppRole

| Method | Mechanism | Use Case |
|:---|:---|:---|
| **JWT (OIDC)** | ServiceAccount token; Vault verifies via JWKS. | **Standard** for HCP Vault + private AKS. No callback required. |
| **AppRole** | Static RoleID + SecretID in K8s Secret. | **Legacy**; used for non-AKS clusters or "Secret Zero" bootstrap. |

Why JWT: No static credentials in cluster; ephemeral tokens; Vault validates JWT signature against cluster OIDC issuer. See [[SoT - VSO Authentication (JWT vs AppRole)]] for full rationale.

### 5. The "Double Namespace" Gotcha
The platform module often prepends `admin/` to the `vault_namespace` variable. If your local config already includes `admin/`, VSO will attempt to target `admin/admin/deployments/...`, resulting in `Permission Denied`.
- **Correct Local**: `deployments/lca-prd-2`
- **Correct VSO Path**: `admin/deployments/lca-prd-2`

### 6. Secret Inventory (Key Mappings)

| K8s Secret | Vault Path | Purpose | Transformation Logic |
|:---|:---|:---|:---|
| `mongodb` | `application` | DB Auth | Maps `mongodb_password` → `mongodb-root-password` |
| `postgresql` | `application` | DB Auth | Maps `postgresql_password` → `postgres-password` |
| `argocd-group-creds` | `gitlab/token` | Git Auth | `oauth2` username + `glpat-*` token |
| `fitfile-image-pull` | `azure/creds/acr-pull` | Pod Scheduling | Template builds `.dockerconfigjson` |

---

## Current Understanding

### Known Issues & Anti-Patterns

- **OIDC Issuer Mismatch**: Cluster recreation changes the OIDC URL. Vault's JWT auth backend must be updated or VSO will fail to authenticate (`role not found`).
- **HCP Admin Limit**: Multiple namespaces requesting dynamic Azure credentials simultaneously can trigger `Server admin limit exceeded`.
- **KCH Hardcoded Secrets**: `vault-replacement-secrets.yaml` contains base64 credentials in git—priority debt.
- **VSO Finalizers**: VSO adds finalizers to CRDs; ArgoCD interprets this as drift, causing noisy `autoHeal` attempts.

### Improvement Roadmap

- **Phase 1 (Security)**: Rotate KCH secrets; migrate to VSO; enforce `refreshAfter` policy (5m app, 1h infra).
- **Phase 2 (DevEx)**: Implement `docs/secret-registry.yaml`; deploy `secret-debug.sh` script.
- **Phase 3 (Hardening)**: VaultAuth as code; `ignoreDifferences` for VSO status fields in ArgoCD.
- **Phase 4 (Observability)**: VSO metrics panel in Grafana; Vault audit log forwarding to Loki.

---

## Operational Protocols

| Need                                | Document                                               |
| :---------------------------------- | :----------------------------------------------------- |
| Troubleshooting stuck/stale secrets | [[Protocol - VSO Secret Management & Troubleshooting]] |
| VSO Debugging playbook              | [[playbook_vso_secret_debugging]]                      |
| Vault KV structure                  | [[SoT - Vault KV Data Structure]]                      |

---

## Related Documentation

- [[MoC - FitFile Secrets Management]]
- [[SoT - VSO Authentication (JWT vs AppRole)]]