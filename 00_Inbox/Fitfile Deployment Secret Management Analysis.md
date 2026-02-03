---
created: 2026-02-02T14:39:31+00:00
modified: 2026-02-02T15:46:05+00:00
title: Fitfile Deployment Secret Management Analysis
---

## 1. Executive Summary

The secret management strategy uses a Hybrid VSO + Reflector model:

1. VSO (Vault Secrets Operator) is the primary engine. It authenticates with Vault and creates Kubernetes Secrets (via `VaultStaticSecret` or `VaultDynamicSecret` CRDs).
2. Reflector is used specifically for Cluster-Wide Shared Secrets (like `fitfile-image-pull-secret`). VSO creates the "source" secret in a central namespace (e.g., `argocd`), and Reflector replicates it to all consumer namespaces.
3. Application Secrets (e.g., Mongo/Postgres creds) are NOT reflected. They are created directly in the application's namespace by VSO.

---

## 2. Secret Creation (The Source)

Secrets are generated and populated into HCP Vault by Terraform.

- Repository: `terraform-fitfile-central-services-consumer`
- File: `main.tf`
- Mechanism: Terraform `random_password` resources generate credentials, which are then written to Vault using `vault_kv_secret_v2` resources.

### Vault Path Structure

Secrets are stored in the KVv2 engine under a strictly defined hierarchy:

- Namespace: `deployments/<customer_deployment_key>` (e.g., `deployments/lca-prd`)
- Mount: `secrets`

### Key Secrets in Vault

| Secret Name | Configuration Source | Content |
|:--- |:--- |:--- |
| `application` | `terraform-fitfile-central-services-consumer` | The Master Secret. Contains database creds (Mongo/Postgres), S3 keys, Auth0 keys, tenant keys (`fitfile_tenant_pkcs8_key`), and monitoring passwords. |
| `auth0` | `terraform-fitfile-central-services-consumer` | Auth0 ID, Secret, and Audience. |
| `argo-workflows` | `terraform-fitfile-central-services-consumer` | Postgres credentials for Argo Workflows. |
| `spicedb` | `terraform-fitfile-central-services-consumer` | Postgres credentials and Preshared Key for SpiceDB. |
| `monitoring` | `terraform-fitfile-central-services-consumer` | Credentials for Loki, Prometheus, and Tempo. |
| `argocd` | `terraform-fitfile-central-services-consumer` | Admin password and Server Secret Key. |

---

## 3. Management in Kubernetes (The Consumption)

### A. Application Secrets (Direct VSO)

For standard application components (MongoDB, MinIO, FFCloud, etc.), secrets are fetched directly by VSO into the target namespace.

- Repository: `helm_chart_deployment/charts/ffnode`
- Configuration: `values.yaml` defines a `vaultSecrets` list for each component.
- Mechanism:
    1. The Helm chart invokes the `generateVaultDynamicSecrets` helper.
    2. This helper renders a `VaultStaticSecret` CRD.
    3. Transformation Templates are used to extract specific keys from the huge `application` Vault secret and format them into the K8s Secret (e.g., formatting a MongoDB connection string).
    4. No Reflector is involved here.

Example (MongoDB):

1. VSO reads `deployments/<key>/secrets/application`.
2. Extracts `mongodb_password` and `mongodb_replica_set_key`.
3. Creates `mongodb` secret in the app namespace.

### B. Shared/Platform Secrets (VSO + Reflector)

This is where Reflector is critical. The logic is defined in the Platform layer, not the application layer.

- Repository: `terraform-helm-fitfile-platform`
- File: `vault_operator/default_image_pull_secret.tftpl`
- Mechanism:
1. VSO creates a `VaultDynamicSecret` named `fitfile-image-pull` in the `argocd` namespace.
2. This secret pulls ACR credentials from Vault path `admin/central/azure/creds/acr-pull`.
3. Crucially, the destination secret is annotated for Reflector:

```yaml
annotations:
  reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
  reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
```

1. Reflector sees this annotation and automatically copies `fitfile-image-pull-secret` to all other namespaces (or a configured subset).

## 4. Summary of Secret Flow

1. Terraform -> Writes random creds to HCP Vault (`deployments/…`).
2. Platform Helm (Reflector Module) -> Sets up VSO+Reflector for Image Pull Secrets.
3. Application Helm (`ffnode`) -> Sets up VSO to pull App Secrets directly from Vault to Pods.
