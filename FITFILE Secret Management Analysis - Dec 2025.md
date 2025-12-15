---
aliases: []
confidence: 
created: 2025-12-15T14:37:49Z
epistemic: 
last_reviewed: 
modified: 2025-12-15T14:38:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Secret Management Analysis - Dec 2025
type: 
uid: 
updated: 
---

## 1. Executive Summary

The deployment architecture is currently split between a "clean", modern approach using **Vault Secrets Operator (VSO)** (exemplified by `ffnodes/fitfile/ff-test-a`) and legacy/messy environments using **hardcoded Kubernetes Secrets** (`vault-replacement-secrets.yaml` in `stg` and `kch`).

The `charts/ffnode` is the canonical, VSO-ready chart. The presence of `vault-replacement-secrets.yaml` in other environments is a technical debt "hack" that bypasses the intended VSO architecture.

## 2. Architecture Analysis

### The Canonical Path (`ffnodes/fitfile` & `charts/ffnode`)
- **Mechanism**:
  - Uses `values.yaml` to define `vaultSecrets` and `extraVaultSecrets`.
  - The `ffnode` chart's `_helpers.tpl` automatically generates `VaultStaticSecret` and `VaultDynamicSecret` CRDs from these values.
  - **Status**: **Functioning/Ready**. `ff-test-a/values.yaml` explicitly configures secrets like `sleuth-secret` and `emis-secrets` to map directly to Vault paths.
- **Example Pattern**:

  ```yaml
  # ffnodes/fitfile/ff-test-a/values.yaml
  extraVaultSecrets:
    - secretName: "sleuth-secret"
      vaultPath: "ff-test-a-application"
      templates:
        apiKey: '{{`{{get .Secrets "sleuth_api_key"}}`}}'
  ```

### Infrastructure Layer
- **Vault**: Terraform provisions the necessary Vault namespaces and mounts.
- **VSO**: The Operator is assumed to be installed and working in the canonical environments (`fitfile`), but failing or unconfigured in the legacy ones (`stg`, `kch`).

---

## 3. Detailed Customer Deployment Analysis

**Scope**: `cuh-prod-1`, `hie-prod-34`, `nnuh-prod-1`. (Legacy environments excluded).

### Configuration Mechanism & Components

The secret management strategy across these deployments follows a standard, automated pattern defined in the **Canonical Chart** (`charts/ffnode`).

#### Components Identified
1.  **HashiCorp Vault**: The central source of truth for all secret data.
2.  **Vault Secrets Operator (VSO)**: The Kubernetes operator responsible for syncing secrets from Vault into Kubernetes Secrets.
3.  **Helm / ArgoCD**: The delivery mechanism that configures VSO resources.

#### How Secrets Are Configured

The configuration flow is entirely data-driven via `values.yaml` files:

1.  **Definition**: Secrets are defined in `values.yaml` arrays (e.g., `mongodb.vaultSecrets`, `global.vaultSecrets`).
2.  **Generation**: The Helm chart (`charts/ffnode`) uses a template helper called `generateVaultDynamicSecrets` (found in `_helpers.tpl`).
3.  **Injection**: This helper dynamically generates `VaultStaticSecret` Custom Resources (CRDs).
4.  **Deployment**: These CRDs are injected into the ArgoCD `Application` manifest or directly applied to the cluster.

**Key Distinction**: Unlike legacy environments, these deployments do **not** use hardcoded `Secret` manifests. They rely 100% on VSO to fetch data at runtime.

### Secret Inventory by Deployment

#### A. Deployment: `cuh-prod-1`
**Vault Namespace**: `admin/deployments/cuh-prod-1` (Implied via VSO config)
**Base Vault Path**: `cuh-prod-1-application`

**1. Custom/Explicit Secrets** (from `cuh-prod-1/values.yaml`)

| Secret Name | Component | Vault Path | Vault Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `cloudflare-issuer-api-token` | Cert Manager | `cloudflare` | `api_token` | API token for Cloudflare DNS challenges. |

**2. Inherited Standard Secrets** (from `charts/ffnode/values.yaml`)

| Secret Name | Component | Vault Path | Vault Keys |
| :--- | :--- | :--- | :--- |
| `mongodb` | MongoDB | `cuh-prod-1-application` | `mongodb_password`, `mongodb_replica_set_key` |
| `postgresql` | PostgreSQL | `cuh-prod-1-application` | `postgresql_password` |
| `minio` | MinIO | `cuh-prod-1-application` | `s3_access_key_id`, `s3_secret_access_key` |
| `argo-postgres-config` | Argo Workflows | `argo-workflows` | `postgresql_password`, `postgresql_username` |
| `spicedb` | SpiceDB | `spicedb` | `postgresql_username/password`, `spicedb_preshared_key` |
| `fitconnect` | FitConnect | `cuh-prod-1-application` | `auth0_client_id/secret`, `mongodb_creds`, `s3_creds` |
| `ffcloud` | FFCloud | `cuh-prod-1-application` | `auth0_client_id/secret`, `cli_auth0_creds` |
| `workflows-secrets` | Workflows | `cuh-prod-1-application` | `s3_creds`, `auth0_creds` |
| `fitfile-rsa-private-key`| Workflows | `cuh-prod-1-application` | `fitfile_tenant_pkcs8.key`, `fitfile_tenant_public.crt` |

#### B. Deployment: `nnuh-prod-1`
**Vault Namespace**: `admin/deployments/nnuh-prod-1`
**Base Vault Path**: `nnuh-prod-1-application`

**1. Custom/Explicit Secrets** (from `nnuh-prod-1/values.yaml`)

| Secret Name | Component | Vault Path | Vault Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `cloudflare-issuer-api-token` | Cert Manager | `cloudflare` | `api_token` | API token for Cloudflare DNS challenges. |

**2. Inherited Standard Secrets**
*Same pattern as `cuh-prod-1` targeting `nnuh-prod-1-application`.*

#### C. Deployment: `hie-prod-34`
**Vault Namespace**: `admin/deployments/hie-prod-34`
**Base Vault Path**: `hie-prod-34-application` (Default)

**1. Custom/Explicit Secrets** (from `hie-prod-34/values.yaml`)

| Secret Name | Component | Vault Path | Vault Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `s3-export-secret` | Workflow Templates | `application` | `hie_s3_export_*` | Credentials for exporting data to an external S3 bucket. |

**2. Inherited Standard Secrets**
*Same standard set inherited from `charts/ffnode` targeting `hie-prod-34-application`.*

---

## 4. Live Cluster Verification: `hie-prod-34`

We correlated the active `kubectl get secrets` output with the configuration code. Every application secret is accounted for in the Helm values.

### A. Namespace: `hie-prod-34` (Main Application)

| Live Secret Name | Type | Config Source | Mechanism | Keys |
| :--- | :--- | :--- | :--- | :--- |
| `fitfile-eoe-tls` | `kubernetes.io/tls` | `values.yaml` (`tls.existingSecret`) | Manually created/Cert-Manager | TLS Certs |
| `s3-export-secret` | `Opaque` | `values.yaml` (`workflowTemplates.extraVaultSecrets`) | VSO (Dynamic Path) | `hie_s3_export_*` |
| `mongodb` | `Opaque` | Chart Defaults (`charts/ffnode`) | VSO (Inherited) | `mongodb_password` |
| `postgresql` | `Opaque` | Chart Defaults | VSO (Inherited) | `postgres_password` |
| `minio` | `Opaque` | Chart Defaults | VSO (Inherited) | `s3_keys` |
| `workflows-secrets`| `Opaque` | Chart Defaults | VSO (Inherited) | `auth0`, `s3` |

### B. Namespace: `hutch` & `hutch-prod` (Hutch Integration)

| Live Secret Name | Type | Config Source | Mechanism | Keys |
| :--- | :--- | :--- | :--- | :--- |
| `bunny` | `Opaque` | `hutch[_prod]_values.yaml` (`extraDeploy`) | VSO (Explicit Resource) | `bunny_postgresql_*` |
| `relay` | `Opaque` | `hutch[_prod]_values.yaml` (`extraDeploy`) | VSO (Explicit Resource) | `relay_postgresql_*` |
| `hutch-postgresql` | `Opaque` | `hutch[_prod]_values.yaml` (`extraDeploy`) | VSO (Explicit Resource) | `postgres_admin_password` |

### C. Namespace: `thehyve` (Analysis Integration)

| Live Secret Name | Type | Config Source | Mechanism | Keys |
| :--- | :--- | :--- | :--- | :--- |
| `thehyve` | `Opaque` | `thehyve_values.yaml` (`extraDeploy`) | VSO (Explicit Resource) | `omop_db`, `airflow_db` |
| `thehyve-postgresql`| `Opaque` | `thehyve_values.yaml` (`extraDeploy`) | VSO (Explicit Resource) | `postgres_admin_password`|

### D. Infrastructure & Other
- **`fitfile-image-pull-secret`**: Global pull secret (likely bootstrapped or synced via a separate process).
- **`sh.helm.release.*`**: Standard Helm release tracking secrets.
- **`tigera-*`, `calico-*`**: Kubernetes networking & security components (Infrastructure layer).

---

## 5. Strategic Proposal: Standardization

We should not introduce new tools (like ESO). Instead, we must **bring all environments up to the standard of `ffnodes/fitfile` and `eoe` deployments**.

### Action Plan
1.  **Verify VSO in Legacy Envs**: Ensure `vault-secrets-operator` is running in `kch` and `stg` clusters.
2.  **Fix Connectivity**: The root cause of the "hack" is likely network/auth related. Verify `VaultAuth` config in these clusters matches the working `fitfile` deployment.
3.  **Migrate Configuration**:
    - Take the matching key/values from `vault-replacement-secrets.yaml`.
    - Move them into the `values.yaml` `extraVaultSecrets` block (following the `ff-test-a` pattern).
    - Populate the actual values into the Vault (HCP).
4.  **Delete the Hack**: Remove `templates/vault-replacement-secrets.yaml` from `stg` and `kch`.
