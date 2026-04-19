---
aliases: [FitFile Secrets SoT, Secrets Management Source of Truth, VSO Secrets Management]
created: 2026-03-14T12:00:00Z
last_synthesis: 2026-04-02
modified: 2026-04-19T18:30:33+00:00
source_of_truth: true
status: evergreen
synthesis-count: 3
tags: [argocd, fitfile, kubernetes, secrets, security, sot, vault, vso]
title: SoT - FitFile VSO Secrets Management
trust-level: stable
type: SoT
---

## Minimum Viable Understanding (MVU)

FitFile uses HCP Vault as the encrypted source of truth for all secrets. The Vault Secrets Operator (VSO) syncs secrets into Kubernetes via a linked chain of declarative CRDs. Authentication uses JWT (OIDC) for remote HCP Vault, bound to the cluster's OIDC issuer. Critical Rule: `spec.destination.overwrite: true` is mandatory for dynamic secrets. Verification: `status.conditions[0].status == "True"` in the CRD.

---

## Working Knowledge

### 1. Architecture Overview: The Linked Chain

VSO operates through a chain of dependencies. If any link is broken, the produced Kubernetes Secret becomes stale or empty.

```
VaultConnection (Where) ← VaultAuth (Who) ← VaultStaticSecret/VaultDynamicSecret (What)
```

- VaultConnection: Cluster-wide (`default` in `vault-secrets-operator-system`), links to the HCP Vault endpoint.
- VaultAuth: Per-namespace; defines the authentication method and targets a specific Vault Namespace (e.g., `admin/deployments/lca-prd-2`).
- VaultStaticSecret (VSS): Syncs static KV-v2 data.
- VaultDynamicSecret (VDS): Syncs dynamic, lease-based data (e.g., Azure ACR credentials).

### 2. Identity Types & Mappings

| Identity Concern | Mechanism | Vault Source | ArgoCD / K8s Context |
|:---|:---|:---|:---|
| ArgoCD Server | VSS | `secrets/argocd` | `argocd-secret` (admin pw, signing key) |
| GitLab Deploy | VSS | `secrets/argocd` | `repository` label (per-repo deploy token) |
| GitLab Group | VSS | `central/gitlab/token` | `repo-creds` label (Template for `fitfile/*`) |
| ACR Registry | VDS | `central/azure/creds/acr-pull` | `repository` label (Helm OCI registry) |
| Image Pull | VDS | `central/azure/creds/acr-pull` | `dockerconfigjson` (kubelet scheduling) |

### 3. Credential Hardening & Tenant Isolation

- Deploy Tokens over PATs: Always opt for GitLab Deploy Tokens (scoped to `read_repository`) or read-only SSH Deploy Keys. Personal Access Tokens (PATs) are tied to humans and break when employees leave.
- Tenant Isolation: Mirror Vault's path partitioning (`admin/deployments/customer-X`) with dedicated GitLab tokens for each customer. This prevents a single compromised token from exposing the entire Git fleet.
- Selective Extraction (Transformation): Use VSO's `transformation.templates` to pull only required fields from multi-value Vault secrets.
    - _Example:_ Pulling `gitlab_token` while leaving `admin_password` and `server_secret_key` securely in Vault.

### 4. ArgoCD Credential Resolution Priority

ArgoCD matches repo URLs against secrets in this priority:

1. `repository` secrets: Exact URL match (Highest Priority).
2. `repo-creds` secrets: Prefix match (Fallback/Template).

> [!warning] The Shadowing Trap
> A `repository` secret with empty or stale credentials will block a perfectly valid `repo-creds` template from working. Ensure `repository` secrets are only created when per-repo tokens are explicitly required.

### 5. Secret Classes & Ownership

| Class | Examples | Ownership / Creation | Delivery |
|:---|:---|:---|:---|
| Shared Platform | `fitfile-image-pull-secret` | Terraform (Global/Core) | VSO syncs to every namespace; required locally by Kubelet. |
| GitOps Plumbing | `gitlab-repository-credentials` | ArgoCD/VSO (System) | Labeled `secret-type: repository` for ArgoCD access. |
| Application | `ffcloud`, `mongodb`, `ude-secret` | ArgoCD/VSO (App) | Injected via env vars or volume mounts; triggers rollout restart. |

### 6. Authentication: JWT Vs AppRole

| Method | Mechanism | Bootstrap Workflow |
|:---|:---|:---|
| JWT (OIDC) | ServiceAccount token; Vault verifies via JWKS. | Modern: Terraform configures Vault JWT backend + roles. No static secrets. |
| AppRole | Static RoleID + SecretID in K8s Secret. | Legacy/Bootstrap: Terraform creates `role-secrets` (K8s) + `VaultAuth` object. |

#### The "Operator Identity" Insight

The VSO operator pod is not a single identity. Instead, it acts as a stateless broker:

1. It watches VSS/VDS resources.
2. It assumes the identity of the `VaultAuth` reference in the target namespace.
3. It requests a token for that specific context to perform the sync.

### 7. The "Two-Namespace" Trap

VSO operations always involve two distinct namespace concepts:

1. Kubernetes Namespace: Where the `VaultAuth`, `VaultStaticSecret`, and destination `Secret` reside.
2. Vault Namespace: (e.g., `admin/deployments/lca-prd-2`) Where the secret data is actually stored in HCP Vault.
_Consistency check_: Ensure `spec.namespace` in VSS/VDS matches the Vault-side path, not the K8s namespace.

### 8. The Bootstrap Chain (AppRole Example)

For namespaces using AppRole (Legacy), the chain of trust is:

1. Terraform: Provisions Vault policies $\to$ Creates AppRole $\to$ Writes `role-secrets` (K8s) $\to$ Deploys `VaultAuth` (Managed by Terraform).
2. ArgoCD: Deploys `VaultStaticSecret` referencing the `VaultAuth`.
3. VSO: Reconciles the secret and manages the workload lifecycle (Rollout Restarts).

---

## Current Understanding

### Known Issues & Anti-Patterns

- OIDC Issuer Mismatch: Cluster recreation changes the OIDC URL. Vault's JWT auth backend must be updated or VSO will fail to authenticate (`role not found`).
- HCP Admin Limit: Multiple namespaces requesting dynamic Azure credentials simultaneously can trigger `Server admin limit exceeded`.
- KCH Hardcoded Secrets: `vault-replacement-secrets.yaml` contains base64 credentials in git—priority debt.
- VSO Finalizers: VSO adds finalizers to CRDs; ArgoCD interprets this as drift, causing noisy `autoHeal` attempts.
- ArgoCD Ghost Deletion: If an ArgoCD `Application` is manually deleted in K8s, Terraform won't redeploy it (as it only tracks the Helm release secret). Use a "Benign Nudge" (e.g., changing `target_revision` from `master` to `HEAD`) to force a reconciliation.

---

## Operational Protocols

| Need                                | Document                                               |
|:---------------------------------- |:----------------------------------------------------- |
| Troubleshooting stuck/stale secrets | [[Protocol - VSO Secret Management & Troubleshooting]] |
| VSO Debugging playbook              | [[playbook_vso_secret_debugging]]                      |
| Vault KV structure                  | [[SoT - Vault KV Data Structure]]                      |

---

## Related Documentation

- [[MoC - FitFile Secrets Management]]
- [[SoT - VSO Authentication (JWT vs AppRole)]]
- [[SoT - Vault Secrets Operator (VSO)]]
