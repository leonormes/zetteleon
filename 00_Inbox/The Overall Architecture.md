---
created: 2026-03-13T19:00:37+00:00
modified: 2026-03-14T11:10:51+00:00
title: The Overall Architecture
---

## The Overall Architecture

Your setup follows this pattern: HCP Vault Cloud → VSO (on-cluster) → Kubernetes Secrets → consumed by ArgoCD and application workloads.

---

## 1. HCP Vault (the Secrets backend)

- Instance: `vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200`
- Namespace hierarchy: `admin/deployments/<cluster-name>` (e.g. `admin/deployments/mkuh-prd-4`, `admin/deployments/hie-test-34`)
- Secrets engine: KV-v2 mounted at `secrets/` within each deployment namespace
- Secret paths: e.g. `secrets/argocd` (ArgoCD credentials), `secrets/application` (app-level secrets like MongoDB)
- Azure secrets engine: Mounted at `azure/`—used for dynamic ACR pull credentials via `azure/creds/acr-pull`

### Auth Methods in Vault (per Deployment namespace)

|Method|Mount path|Used by|Notes|
|---|---|---|---|
|JWT|`jwt-<cluster-name>/`|VSO on AKS clusters|Bound to the AKS OIDC issuer URL. Role bound to `system:serviceaccount:*:default` (the `default` SA in any namespace)|
|AppRole|`approle/`|VSO on EKS/non-AKS clusters|Used on clusters like `hie-test-34`|

### Vault Policies Attached to Auth Roles

Policies like `default`, `acr-reader`, and `operator` grant access to KV paths and the Azure secrets engine. The `acr-reader` policy needs `read` on `azure/creds/acr-pull`.

---

## 2. Vault Secrets Operator (VSO)—the On-cluster Bridge

Helm chart: `vault-secrets-operator` v0.10.0, installed in `vault-secrets-operator-system`

### Key CRDs (the Component chain)

Think of it as a linked chain—each CR references the one before it:

```
VaultConnection  ←──  VaultAuth  ←──  VaultStaticSecret / VaultDynamicSecret
   (where)            (who)              (what)
```

VaultConnection (`default` in `vault-secrets-operator-system`)

- Points at the HCP Vault address
- `skipTLSVerify: false`
- Shared across all namespaces via cross-namespace reference

VaultAuth (`default` in each application namespace—`argocd`, `mkuh-prd-4`, etc.)

- References VaultConnection as `vault-secrets-operator-system/default`
- On AKS: `method: jwt`, `mount: jwt-<cluster-name>`, with `audiences` set to the AKS OIDC issuer URL
- On EKS: `method: appRole` with `roleId` and `secretRef`
- Sets the Vault `namespace` (e.g. `admin/deployments/mkuh-prd-4`)
- Created by Terraform via `kubectl_manifest.vault_auth` with a `for_each` map keyed by namespace name (e.g. `"argocd"`, `"spicedb"`, `"monitoring"`)
- The VSO Helm chart's `defaultAuthMethod.enabled` is `false`—auth is explicitly _not_ created by the Helm chart

VaultStaticSecret (for KV-v2 secrets)

- References `vaultAuthRef: default`
- Points at a KV path (e.g. `mount: secrets`, `path: argocd`)
- Uses `secretTransformation` with `excludes: [".*"]` + named `templates` to map Vault key names → Kubernetes Secret key names
- `refreshAfter: 30m` (or `null` in some cases—meaning no periodic re-fetch)
- Created by Helm charts, rendered through the ArgoCD app-of-apps chain

VaultDynamicSecret (for rotating Azure credentials)

- Used for ACR image pull secrets
- Points at `mount: azure`, `path: creds/acr-pull`
- Uses a `secretTransformation` template to build a `.dockerconfigjson` from `client_id` and `client_secret`
- `renewalPercent: 67`

---

## 3. How ArgoCD Accesses GitLab

ArgoCD authenticates to GitLab using two separate repository secrets, both sourced from a single Vault KV path (`secrets/argocd`):

### Secret 1: `argocd-repo-fitfile-deployment-repo`

- Purpose: Access to the main deployment chart repo (`https://gitlab.com/fitfile/deployment.git`)
- Credential type: GitLab deploy token (project-scoped, read-only)
- Labels: `argocd.argoproj.io/secret-type: repository`
- VSO template maps:
    - `username` ← `gitlab_deploy_token_username` (e.g. `gitlab+deploy-token-10151641`)
    - `password` ← `gitlab_deploy_token_password` (a `gldt-` prefixed token)
    - `url` ← hardcoded `https://gitlab.com/fitfile/deployment.git`

### Secret 2: `argocd-values-repo-creds`

- Purpose: Access to the per-customer values repo (e.g. `https://gitlab.com/fitfile/customers/eoe/mkuh-prd-4.git`)
- Credential type: GitLab group access token (broader scope, covers the `customers/` subgroup)
- Labels: `argocd.argoproj.io/secret-type: repository`
- VSO template maps:
    - `username` ← `gitlab_values_access_username` (e.g. `argocd-mkuh-prd-4`)
    - `password` ← `gitlab_values_access_token` (also `gldt-` prefixed)
    - `url` ← hardcoded to the specific customer values repo

### The Multi-source App Pattern

The ArgoCD Application `ff-mkuh-prd-4` uses two sources:

1. Chart source: `https://gitlab.com/fitfile/deployment.git` at `targetRevision: mkuh-prod-latest-release`, path `charts/ffnode`
2. Values source: `https://gitlab.com/fitfile/customers/eoe/mkuh-prd-4.git` at `targetRevision: main`, referenced as `$values/generated/values.yaml`

ArgoCD matches the repo URL in each source against the `url` field in the repository secrets to find the right credentials.

---

## 4. The App-of-Apps Propagation Chain

This is the part that caught us out with the MongoDB `secretTransformation` keys:

```
values.yaml in Git (customer values repo)
     ↓  read by
Root ArgoCD Application (ff-mkuh-prd-4)
     ↓  Helm renders → produces
Child Application CRs (e.g. ff-mkuh-prd-4-mongodb-b17ef)
     ↓  ArgoCD syncs each child
VaultStaticSecret on cluster (e.g. mongodb in mkuh-prd-4 namespace)
     ↓  VSO reconciles
Kubernetes Secret
     ↓  consumed by
Application pods (e.g. MongoDB)
```

Changes to `values.yaml` don't directly affect VSO—they must propagate through the parent app sync first, which re-renders the child Application specs, which then gets synced by ArgoCD.

---

## 5. Known Pain Points / Outstanding Items

- Vault KV key naming mismatch: Terraform seeds keys as `gitlab_values_token_*` but Helm templates expect `gitlab_deploy_token_*` and `gitlab_values_access_*`. The manual fix was to patch the extra keys into Vault. The permanent fix is to align either the Terraform seeding workspace or the Helm chart templates to a single naming convention.
- ArgoCD ↔ VSO reconciliation loops: VSO adds a finaliser to `VaultStaticSecret` objects, which ArgoCD interprets as drift, triggering self-heal cycles. This stabilises eventually but causes noisy `autoHealAttemptsCount` spikes.
- `refreshAfter: null` on some VaultStaticSecrets: Means VSO will never re-fetch from Vault unless the spec changes or you manually annotate a force-sync.

---

Relevant past chats if you want to revisit the raw troubleshooting:

- [ArgoCD deployment troubleshooting](https://claude.ai/chat/a4a49b2f-4cae-4879-ba37-c4a233db7669)
- [VSO permission denied troubleshooting](https://claude.ai/chat/d9e79240-b133-4f17-9e3f-46a5cdeca928)
- [ArgoCD reconciliation loops and app-of-apps](https://claude.ai/chat/2b2fa7a9-c769-44a6-88b1-586d95a91444)
