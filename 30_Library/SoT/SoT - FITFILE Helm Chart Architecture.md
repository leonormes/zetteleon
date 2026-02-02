---
aliases: [FITFILE Helm Chart Architecture, Helm Charts Technical Wiki]
created: 2025-02-27T02:44:32Z
deprecated: 2026-02-01
last_reviewed: 2026-02-01
modified: 2026-02-01T15:07:47+00:00
status: archived
superseded_by: "[[SoT - FitFile Deployment - Helm Architecture & Operations]]"
tags: [deprecated, ff_deploy, helm, sot]
title: SoT - FITFILE Helm Chart Architecture
type: SoT
updated: 2026-02-01
---

## DEPRECATED

> [!warning] Deprecated
> This note has been consolidated into [[SoT - FitFile Deployment - Helm Architecture & Operations]]. Please refer to that note for the canonical Source of Truth regarding Helm charts, architecture, and operations.

### I. Overview and Core Functionality

#### 1. Purpose and Architecture

The Helm charts form the GitOps delivery mechanism for the FITFile platform. This architecture orchestrates the deployment of:

- Core Application Services: `frontend`, `ffcloud-service`, `ffnode`, `fitconnect`
- Data Persistence: `databases` (PostgreSQL, MongoDB, MinIO)
- Infrastructure Services: `certs`, `shared-secrets`, `spicedb`
- Control Plane: `argo` (ArgoCD and Workflows)

#### 2. Helm Chart Structure

The repository follows a monolithic chart structure with functional decomposition:

```sh
charts/
├── argo/              # CI/CD Control Plane
│   ├── cd/            # ArgoCD (v6.11.1)
│   └── workflows/     # Argo Workflows
├── certs/             # Certificate Management
├── databases/         # Persistence Layer (Bitnami Wrappers)
├── frontend/          # Application UI
├── ffcloud-service/   # Core API
├── ffnode/            # Node Service
├── fitconnect/        # Interconnectivity Service
└── shared-secrets/    # Secret Injection Layer
```

Key Components:

1. ArgoCD (argo/cd)
   - Role: GitOps Controller
   - Configuration: Managed via `values.yaml` (Base), `values-prod.yaml` (Prod), `values-sh.yaml` (Staging).
2. Databases
   - Components: PostgreSQL (12.7.3), MongoDB (12.1.31), MinIO (12.13.2).
   - Integration: Wrapper charts around upstream Bitnami charts.
   - Customization: Global values inject specific persistence and auth configurations.
3. Templates
   - `_names.tpl`: Canonical naming conventions.
   - `_secrets.tpl`: Logic for secret generation and retrieval.

### II. Multi-Tenancy & Configuration Management

#### 1. Current State (Environment-Based)

Configuration is currently split by environment files within the chart structure:

- `values.yaml`: Default/Base configuration.
- `values-prod.yaml`: Production overrides.
- `values-sh.yaml`: Staging/QA overrides.

Example: Ingress Configuration

```yaml
# values-prod.yaml
argo-cd:
  server:
    ingress:
      hosts:
        - argocd.fitfile.net
```

#### 2. ArgoCD Integration

ArgoCD serves as the active reconciliation agent:

- Authentication: OIDC via Azure AD.
- RBAC: Role definitions in `policy.csv` (e.g., `role:org-admin`, `role:readonly`).
- Ingress: Environment-specific routing rules.

### III. Operational Templates

#### 1. Database Backups

Automated backup logic is embedded in the chart templates:

- Configurable cron schedules.
- Retention policy enforcement.
- PVC management for dump storage.

#### 2. Management Interfaces

- MongoDB Web Interface: Configured ingress for database administration tools.

### IV. Architecture Evolution Plan (Recommendations)

#### 1. Separation of Concerns (Config vs. Code)

Transition from environment files to a strict Config/Code Split:

Target Structure:

```sh
deployment-repo/            # IMMUTABLE CODE
└── charts/
    └── ffnode/

customer-config-repo/       # MUTABLE CONFIG
├── _common/               # Inheritance Base
│   ├── prod.yaml
│   └── staging.yaml
├── barts/                 # Tenant: Barts
│   ├── _defaults.yaml
│   └── prod.yaml
└── eoe/                   # Tenant: EoE
    ├── _defaults.yaml
    └── sde.yaml
```

#### 2. GitOps Pattern: ApplicationSets

Adopt the App of Apps pattern using ApplicationSets for automated tenant onboarding:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: fitfile-customers
spec:
  generators:
    - git:
        repoURL: https://gitlab.com/fitfile/customer-config.git
        files:
        - path: "values/customers/*/values.yaml"
  template:
    spec:
      source:
        repoURL: https://gitlab.com/fitfile/deployment.git
        path: charts/ffnode
        helm:
          valueFiles:
          - values/customers/{{customer}}/values.yaml
```

#### 3. Usage Guide: New Customer Onboarding

Current Protocol:

```bash
# 1. Clone values template
cp values/template/values.yaml values/customers/new-customer/values.yaml

# 2. Configure Tenant Specifics
# - Ingress Hostnames
# - Resource Quotas
# - Secret References

# 3. Apply Argo Application
kubectl apply -f applications/new-customer.yaml
```

Troubleshooting:
- Database Backups: Verify PVC binding and retention policy matching.
- Sync Failures: Validate `values.yaml` syntax and Git credentials in ArgoCD.
