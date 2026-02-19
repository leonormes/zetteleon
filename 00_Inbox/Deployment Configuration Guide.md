---
created: 2026-02-13T13:52:24+00:00
modified: 2026-02-16T11:28:43+00:00
title: Deployment Configuration Guide
---

This document outlines the standard configuration patterns for `ffnode` deployments across the codebase. It generalizes the findings from `cuh-prod-1`, `ff-a`, `testing`, and other deployment profiles.

## Deployment Profiles

| Profile             | Description                                                                                                 | Example           |
|:------------------ |:---------------------------------------------------------------------------------------------------------- |:---------------- |
| Trust Integration   | Production deployments integrated with NHS Trusts. Uses specific `fitConnectCode` and Host Network configs. | `eoe/cuh-prod-1`  |
| Internal Production | Fitfile managed production environments. Full feature set, Sleeuth integration.                             | `fitfile/ff-a`    |
| CI/CD Testing       | Automated testing environments. High parallelism, mocks, resource limits.                                   | `fitfile/testing` |
| Sandbox/Dev         | Experimental or developer-specific environments. Often partial deployments.                                 | `stg/sandbox`     |

## Configuration Structure (`values.yaml`)

### 1. Identity & Scope

Everything starts with defining _where_ and _what_ this deployment is.

```yaml
namespace: "cuh-prod-1" # K8s Namespace
deploymentKey: "cuh-prod-1" # Unique Key (used for naming resources)
host: "app.fitfile.net" # Primary FQDN
```

### 2. Global Settings

Shared configuration across all components.

```yaml
global:
  fitConnectCode: "CUH PROD 1" # Unique Trust/Site Identifier
  oauth:
    baseURL: "https://fitfile-prod.eu.auth0.com"
    managementApiAudience: "https://fitfile-prod.eu.auth0.com/api/v2/"
  deploy: # Feature Flags (Optional override of defaults)
    emis: true
```

### 3. Application Components

Configuration for the core FITFILE applications.

#### `fitconnect` / `ffcloud` / `frontend`

- Ingress & TLS: Define public and private access points.
- Feature Flags: Toggle specific application features (e.g., `exportToS3`).
- Resources: CPU/Memory requests and limits (critical for Testing/Dev profiles).

```yaml
fitconnect:
  tls:
    spec:
      - hosts: ["cuh-prod-1.privatelink.fitfile.net"]
        secretName: fitfile-cuh-private-tls
  ingress:
    hosts:
      - hostname: "cuh-prod-1.privatelink.fitfile.net"
        path: "/fitconnect"
```

### 4. Infrastructure Components

Managed via Helm, often with Vault Secret Operator (VSO) integration.

#### Data Stores (`mongodb`, `postgresql`, `minio`)

- Target Revision: Pin specific chart versions (e.g., `16.5.*`).
- Persistence: Define volume sizes (`size: 64Gi`).
- Vault Secrets: Map Vault paths to K8s secrets using VSO templates.

#### Vault Secret Transformations

A key pattern in `ffnode` is using `secretTransformation` to map Vault secrets into specific Kubernetes secret keys. This is often used to construct connection strings or map generic Vault keys to component-specific keys.

Example (`mongodb`):

```yaml
secretTransformation:
  templates:
    mongodb-root-password:
      text: '{{"{{`{{get .Secrets \"mongodb_password\"}}`}}"}}'
```

_Note: The double curly-braces with backticks are used to escape the template so it's processed by the Vault Secrets Operator (VSO) rather than Helm._

#### Observability (`grafana`, `alloy`)

- External Services: Proxy URLs (common in Trust environments).
- Alloy: Log formats, resource limits.
- VSO: Secrets for remote write (Prometheus/Loki/Tempo).

### 5. Platform Services

#### `argoWorkflows` / `argocdApp`

- SSO: Integration with Auth0/Entra ID for UI access.
- RBAC: Map Azure Groups to ReadOnly/Admin roles.
- Target Revision: Pin deployment versions (e.g., `latest-release`).

#### `certManager`

- DNS Solvers: Configure recursive nameservers (critical for internal Trust networks).
- Vault Issuer: API tokens for Cloudflare or internal PKI.

## Helm Chart Architecture (`ffnode`)

The `ffnode` chart follows an App of Apps pattern. It does not contain the application manifests directly but rather orchestrates the deployment of other Helm charts via ArgoCD Application resources.

### Object Types & Resource Orchestration

The `ffnode` chart manages the creation of several types of Kubernetes and custom resources:

1. ArgoCD Applications (`Application`): The primary mechanism for component deployment. Each component (e.g., `fitconnect`, `mongodb`, `grafana`) is defined as an ArgoCD Application in `templates/*.yaml`. This allows for independent sync policies and revision tracking for each sub-chart.
2. Vault Secrets (VSO):
   - `VaultStaticSecret`: Created for most applications to map Vault KV-v2 secrets to K8s Secrets.
   - `VaultDynamicSecret`: Used when `dynamic: true` is set in the configuration (common for rotating credentials).
   - Orchestration: These are generated via the `generateVaultDynamicSecrets` helper in `_helpers.tpl` and injected into the child app's `extraDeploy` values.
3. Batch Jobs (`Job`):
   - `mongodb-copy-job`: A conditional job used for database migrations or data synchronization during `mongodbNext` deployments.
4. RBAC & Identity:
   - `ServiceAccount`, `ClusterRole`, `ClusterRoleBinding`: Specifically managed for Argo Workflows SSO to map Azure AD/Entra ID groups to granular UI permissions (Admin vs Read-Only).
   - `Secret` (Service Account Tokens): Explicitly created for Argo UI users when SSO is enabled.
5. Extra Deployments (`extraDeploy`): A catch-all pattern that allows users to inject arbitrary Kubernetes objects or Vault secrets into any child application through the `renderValuesWithVaultSecretInExtraDeploy` helper.

### Structure

- Wrapper Chart: `ffnode` acts as the parent.
- Child Apps: Defined in `templates/*.yaml` (e.g., `fitconnect-application.yaml`, `mongodb-application.yaml`).
- Source: Most child apps point to `charts/components/<name>` in the same `deployment` repository.

### Component Inventory

The following components are orchestrated as ArgoCD Applications:

| Category       | Components                                                                      |
|:------------- |:------------------------------------------------------------------------------ |
| Core Services  | `fitconnect`, `ffcloud`, `frontend`, `workflows-api`                            |
| Data Stores    | `mongodb`, `mongodb-next`, `postgresql`, `minio`                                |
| Infrastructure | `cert-manager`, `certificates`, `vault`, `blob-csi-driver`                      |
| Observability  | `grafana`, `prometheus-crds`                                                    |
| Workflows      | `argo-workflows`, `workflow-templates`, `workflows-integration-tests-templates` |
| Utilities      | `seed` (data seeding), `mutating-proxy-webhook`                                 |

### Value Propagation

Values defined in your Deployment's `values.yaml` (e.g., `cuh-prod-1/values.yaml`) are merged and passed down to child charts.

`Deployment Values` + `Global Values` -> Merged -> `Child Chart Values`

Example (`fitconnect`):

```yaml
# In ffnode/templates/fitconnect-application.yaml
values: |
  {{- $values := mergeOverwrite (include "fitconnectValues" . | fromYaml) .Values.fitconnect (dict "global" .Values.global) -}}
  {{- include "renderValuesWithVaultSecretInExtraDeploy" (list . $values) | indent 8 }}
```

## Common Patterns & Anomalies

- Proxy Configuration: Trust deployments (`cuh-prod-1`) heavily rely on `HTTP_PROXY` env vars and `no-http-proxy-vars` annotations to bypass proxies for internal traffic.
- Resource Limits: `testing` profile has very specific, low resource limits to pack workloads efficiently.
- Vault Paths: varied between `application`, `ff-a-application`, or derived paths. Refactoring note: Moving to standard derived paths is recommended.
