---
created: 2025-02-07T12:57:55Z
modified: 2026-02-01T15:07:47+00:00
Reviewed: false
status: stable
tags:
  - architecture
  - deployment
  - fitfile
  - helm
  - kubernetes
  - sop
title: SoT - FitFile Deployment - Helm Architecture & Operations
type: SoT
---

## 1. Overview

FITFILE deployments utilize a GitOps-compatible Helm architecture. The core principle is "Configuration as Code," where a generic chart architecture is specialized for each environment (e.g., `ff-a`, `prod-1`) via specific `values.yaml` overrides.

This architecture orchestrates the deployment of:

- Core Application Services: `frontend`, `ffcloud-service`, `ffnode`, `fitconnect`
- Data Persistence: `databases` (PostgreSQL, MongoDB, MinIO)
- Infrastructure Services: `certs`, `shared-secrets`, `spicedb`
- Control Plane: `argo` (ArgoCD and Workflows)

---

## 2. Repository & Chart Architecture

The repository follows a monolithic chart structure with functional decomposition.

### 2.1 Global Directory Structure

```sh
charts/
├── argo/              # CI/CD Control Plane
│   ├── cd/            # ArgoCD (v6.11.1)
│   └── workflows/     # Argo Workflows
├── certs/             # Certificate Management
├── databases/         # Persistence Layer (Bitnami Wrappers)
├── ffnode/            # The Application Umbrella Chart
├── frontend/          # Application UI
├── ffcloud-service/   # Core API
├── fitconnect/        # Interconnectivity Service
└── shared-secrets/    # Secret Injection Layer
```

### 2.2 Key Components

1. The Application Umbrella (`ffnode`):
   - Acts as the parent chart deploying the core stack (`frontend`, `fitconnect`, `keycloak` legacy).
   - Uses `_names.tpl` for canonical naming conventions.

2. GitOps Control Plane (`argo/cd`):
   - Role: Active reconciliation agent.
   - Authentication: OIDC via Azure AD.
   - RBAC: Defined in `policy.csv` (e.g., `role:org-admin`, `role:readonly`).

3. Persistence Layer (`databases`):
   - Wraps upstream Bitnami charts for PostgreSQL (12.7.3), MongoDB (12.1.31), and MinIO (12.13.2).
   - Backups: Automated logic embedded in templates (configurable cron schedules, retention policies, PVC management).
   - Management: Includes configured ingress for MongoDB web interfaces.

---

## 3. Configuration Management

### 3.1 The Values Hierarchy

Configuration is layered to ensure stability while allowing specificity:

1. Chart Defaults: `charts/ffnode/values.yaml` (Base configuration).
2. Environment Overrides:
   - `values.yaml`: Default/Base configuration.
   - `values-prod.yaml`: Production overrides.
   - `values-sh.yaml`: Staging/QA overrides.
3. Secrets: Injected at runtime via Vault (See [[SoT - FITFILE Secret Management Architecture]]).

### 3.2 Key Configuration Parameters

| Parameter | Description | Example |

|:--- |:--- |:--- |

| `namespace` | Target K8s namespace. | `ff-a` |

| `deploymentKey` | Unique ID for resource tagging. | `prod-1` |

| `host` | Public ingress domain. | `app.fitfile.net` |

| `applicationVaultPath` | Path to secrets in Vault. | `deployments/prod-1/application` |

| `global.sleuth` | Distributed tracing config. | `enabled: true` |

---

## 4. Operational Workflows

### 4.1 Modifying a Chart

1. Edit: Modify `charts/<component>/templates/*.yaml`.
2. Bump: Increment `version` in `Chart.yaml` (Semantic Versioning).
3. Test: Run `helm template.` locally to verify manifest generation.

### 4.2 Manual Deployment (Testing)

For local testing or manual overrides (outside ArgoCD):

```bash
# Syntax
helm upgrade --install <release-name> ./charts/ffnode \
  --namespace <namespace> \
  --values environments/<env>/values.yaml

# Example (FF-A Demo)
helm upgrade --install ff-a ./charts/ffnode \
  --namespace ff-a \
  --values ffnodes/fitfile/ff-a/values.yaml
```

### 4.3 New Customer Onboarding

1. Clone Config: Copy `values/template/values.yaml` to `values/customers/<new-customer>/values.yaml`.
2. Configure: Update Ingress hostnames, resource quotas, and Vault secret references.
3. Deploy: Apply the ArgoCD application manifest (`kubectl apply -f applications/<new-customer>.yaml`).

### 4.4 Troubleshooting

- Immutable Tags: Never redeploy a chart with the same image tag if the code changed.
- Secret Absence: If pods fail to start, check `applicationVaultPath` in Vault.
- Database Backups: Verify PVC binding and retention policy matching in the `databases` subchart.
- Sync Failures: Validate `values.yaml` syntax and Git credentials in ArgoCD.

---

## 5. Strategic Roadmap (Architecture Evolution)

To improve multi-tenancy and maintainability, the following evolution is planned:

### 5.1 Separation of Concerns (The "Data-Driven" API)

Critique (Current State):
The current chart suffers from "Pass-Through Complexity" and a "Boolean Swamp" (`deploy.persistence`, `deploy.monitoring`), requiring users to manually wire dependencies (e.g., `vaultSecrets` templating).

Target State (Proposed API):
We are shifting to a strict Intent-Based Data Model enforced by JSON Schema.

```typescript
interface FFNodeValues {
  // 1. Meta-Architecture (Replaces Booleans)
  profile: 'local-dev' | 'prod-ha' | 'edge-airgapped';
  
  // 2. Identity & Access (Global Truth)
  tenant: {
    key: string; // e.g., "barts"
    displayName: string;
  };
  
  // 3. Service Graph (The Glue)
  services: {
    database: 'managed' | 'external'; // Chart decides topology based on profile
    auth: AuthService;
  };
}
```

### 5.2 ApplicationSets (App of Apps)

Adopt the ApplicationSet pattern to automate tenant onboarding:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  generators:
    - git:
        repoURL: https://gitlab.com/fitfile/customer-config.git
        files:
        - path: "values/customers/*/values.yaml"
  template:
    spec:
      source:
        path: charts/ffnode
        helm:
          valueFiles:
          - values/customers/{{customer}}/values.yaml
```
