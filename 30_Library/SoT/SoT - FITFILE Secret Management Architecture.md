---
aliases: [FITFILE Secret Management Architecture, Secret Management SoT, VSO Implementation Guide]
created: 2025-12-15T00:00:00Z
last_reviewed: 2025-12-15
modified: 2026-02-06T10:25:11+00:00
status: stable
tags: ["SoftwareEngineering/Architecture", "SoftwareEngineering/Security", fitfile, kubernetes, vault]
title: SoT - FITFILE Secret Management Architecture
type: SoT
updated:
uuid: d33b2418-260e-4eba-8375-26c545e2792e
---

## 2. The Canonical Architecture

The standard implementation leverages a data-driven approach where secrets are defined in Helm values and materialized by VSO.

### Core Components

1. HashiCorp Vault: The central, encrypted source of truth for all secret data.
2. Vault Secrets Operator (VSO): The Kubernetes operator that authenticates with Vault (via AppRole) and synchronizes secrets into Kubernetes `Secret` resources.
3. Helm / ArgoCD: The delivery mechanism that configures VSO resources via the `ffnode` chart.

### 2.1 Dynamic Infrastructure Secrets (ACR)

Unlike application secrets (static KV), infrastructure credentials like image pull secrets are generated dynamically to ensure short-lived access.

- Mechanism: `VaultDynamicSecret` (via `charts/ffnode/_helpers.tpl`).
- Helm Enhancement: The `generateVaultDynamicSecrets` helper supports a `destinationType` field, allowing the creation of specific Kubernetes Secret types (e.g., `kubernetes.io/dockerconfigjson`).
- Source of Truth: "HCP Vault ACR Pull" Service Principal (`1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a`) in Azure AD.
- Management Mode: Static Role. Vault is configured to rotate/append secrets for this _specific_ singleton Service Principal rather than creating distinct SPs for every request.
    - _Scope_: The generated secret (`fitfile-image-pull-secret`) provides `AcrPull` access.
    - _Refresh_: Automatically rotated every 1 hour (standard) or 10m (aggressive/testing).

### The Configuration Flow

1. Definition: Secrets are declared in `values.yaml` under `vaultSecrets` or `extraVaultSecrets`.
2. Generation: The `charts/ffnode` helper `_helpers.tpl` (specifically `generateVaultDynamicSecrets`) processes these values.
3. Injection: The helper generates `VaultStaticSecret` or `VaultDynamicSecret` CRDs.
4. Sync: VSO detects the CRD, fetches the data from Vault, and creates a native Kubernetes Secret.

Example Pattern:

```yaml
# ffnodes/fitfile/ff-test-a/values.yaml
extraVaultSecrets:
  - secretName: "sleuth-secret"
    vaultPath: "ff-test-a-application"
    templates:
      apiKey: '{{`{{get .Secrets "sleuth_api_key"}}`}}'
```

---

## 3. Deployment Inventory & Status

### A. Canonical Deployments (VSO Enabled)

_Status: Healthy_

These environments purely use VSO and do not rely on hardcoded secrets.

| Deployment | Vault Namespace | Base Path | Key Secrets |
|:--- |:--- |:--- |:--- |
| `cuh-prod-1` | `admin/deployments/cuh-prod-1` | `cuh-prod-1-application` | `cloudflare-issuer-api-token`, `fitconnect`, `fitfile-rsa-private-key` |
| `nnuh-prod-1` | `admin/deployments/nnuh-prod-1` | `nnuh-prod-1-application` | `cloudflare-issuer-api-token`, `mongodb` |
| `hie-prod-34` | `admin/deployments/hie-prod-34` | `hie-prod-34-application` | `s3-export-secret` (Custom export creds) |
| `testing` | `admin/central/azure` | `creds/acr-pull` | `fitfile-image-pull-secret` (Dynamic ACR) |

### B. Legacy Deployments (Technical Debt)

_Status: Remediation Required_

Environments like `stg` and `kch` currently fail to use VSO correctly, relying on `vault-replacement-secrets.yaml`.

Root Cause:

- Likely network connectivity or `VaultAuth` misconfiguration in the specific clusters prevents VSO from authenticating.
- "Hack" solution was applied to bypass the error, embedding secrets directly in git/deployment (Security Risk).
- _Legacy Artifact_: The manual `acr-service-principal` (`39cf7fc7…`) found in these environments is expired/obsolete and superseded by the dynamic `1c2d5c6f…` SP.

---

## 4. Standardization Action Plan

To eliminate the security risk and technical debt, we must migrate Legacy environments to the Canonical standard.

1. Verify VSO Status: Ensure `vault-secrets-operator` is running in `kch` and `stg` clusters.
2. Fix Connectivity/Auth: Debug the `VaultAuth` resource. Verify the cluster can reach the Vault endpoint and that AppRole credentials are valid.
3. Migrate Data:
    - Extract values from `vault-replacement-secrets.yaml`.
    - Move them to `values.yaml` `extraVaultSecrets` configuration.
    - Write the actual secret data into the relevant HashiCorp Vault path.
4. Delete the Hack: Remove `templates/vault-replacement-secrets.yaml` entirely.

---

## 5. Reference Implementation: `hie-prod-34` (Audit & Deep Dive)

The `hie-prod-34` deployment serves as the primary reference implementation for the FITFILE secrets architecture. A comprehensive audit (Oct 2025) confirmed the efficacy of the VSO model while highlighting key areas for optimization.

### 5.1 Secrets Inventory (The Real-World Model)

The deployment manages 19 VaultStaticSecret resources across three logical layers.

#### A. Core Application Layer (FFNode Chart)

_Managed via `extraVaultSecrets` or Standard Chart Values._

| Secret Name | Vault Path | Purpose | Refresh Policy |
|:--- |:--- |:--- |:--- |
| `fitconnect` | `application` | FITConnect Service Creds | ✅ 5m |
| `ffcloud` | `application` | FFCloud Coordinator Creds | ✅ 5m |
| `frontend` | `application` | Auth0 & MongoDB Creds | ✅ 5m |
| `mongodb` | `application` | Root Password & Replica Key | ❌ Manual |
| `postgresql` | `application` | Admin Password | ❌ Manual |
| `fitfile-rsa-private-key` | `application` | PKCS#8 Keypair | ❌ Manual |

#### B. Integration Layer (Hutch & TheHyve)

_Managed via `extraDeploy` pattern._

| Secret Name | Vault Path | Purpose | Refresh Policy |
|:--- |:--- |:--- |:--- |
| `bunny` | `hutch` | ETL DB & Task API | ✅ 10m |
| `relay` | `hutch` | Relay Service & RabbitMQ | ✅ 10m |
| `thehyve` | `thehyve` | Airflow & OMOP DB | ✅ 10m |

### 5.2 VSO Architecture & Data Flow

1. Authentication:
   - Terraform creates an AppRole (RoleID + SecretID).
   - `VaultAuth` resource authenticates VSO against the Vault cluster.
   - VSO obtains a namespace-scoped token.

2. Transformation (The `extraDeploy` Pattern):
   While `ffnode` handles standard secrets, integrations like Hutch use `extraDeploy` to inject raw VSO resources with complex transformations.

```yaml
# Example: Transforming raw credentials into a connection string
transformation:
 templates:
   db_connection_string:
     text: 'Host=postgres;User={{get .Secrets "username"}};Password={{get .Secrets "password"}}'
```

### 5.3 Security Analysis (2025 Audit Findings)

#### ✅ Strengths

- Drift Detection: `hmacSecretData: true` automatically reverts manual tampering.
- Dynamic ACR Credentials: Usage of `VaultDynamicSecret` for short-lived Azure Service Principal tokens.
- TLS Automation: `cert-manager` integrated with Vault PKI.

#### ⚠️ Critical Risks & Remediation

1. Hardcoded Credentials (Legacy):
   - _Risk:_ Plaintext passwords found in legacy `shared-secrets` charts.
   - _Fix:_ Immediate migration to VSO.
2. Stale Secrets (No Refresh):
   - _Risk:_ Database secrets (`mongodb`, `postgresql`) lacked `refreshAfter`, preventing rotation.
   - _Fix:_ Standardized on a 1h Refresh Interval for databases.
3. No Rollout Restart:
   - _Risk:_ Pods holding old connection pools would fail after rotation.
   - _Fix:_ Added `rolloutRestartTargets` to StatefulSets.

### 5.4 Operational Standards (The "Golden Config")

Based on the audit, all new deployments must adhere to these settings:

| Secret Type | Refresh Interval | Rollout Strategy |
|:--- |:--- |:--- |
| Databases | `1h` | `rolloutRestartTargets: StatefulSet` |
| Apps (API) | `15m` | `rolloutRestartTargets: Deployment` |
| Image Pull | `10m-1h` | None (Kubelet handles) |
| Workflows | `30m` | None (Ephemeral Pods) |
| Monitoring | `1h` | None |

---

## 6. Future Improvements & Automation

We are actively improving the developer experience to reduce toil and error.

### 6.1 The Presets Strategy (Simplification)

We are moving away from verbose templates in `values.yaml` towards simple "Presets" defined in the Helm chart.

- Old Way: Manually defining `templates: { apiKey: '{{…}}' }` for every deployment.
- New Way: `preset: mongodb` tells the chart to generate the standard MongoDB secret structure automatically.

### 6.2 Automated Population (UDE/Vault)

Currently, populating Vault is a manual process using the HCP UI.

- Goal: CLI automation to generate and push secrets (e.g., `cargo run -- key-gen`).
- Target: A `make init-secrets` command that generates random passwords and UDE keys and pushes them to the correct Vault path.

### 6.3 Dynamic Database Secrets

- Goal: Move from static KV secrets (long-lived passwords) to Vault's Database Secrets Engine.
- Benefit: Short-lived, automatically rotated credentials (TTL 1h) generated on-the-fly for each pod.
- [ ] R&D how to use vault's dB secrets engine ^2025-12-26T21-58-48
    - [📱 View in Todoist app](todoist://task?id=6fcrF7wgv6cfR48M) (Created: 📝 2025-12-26T21:59)
