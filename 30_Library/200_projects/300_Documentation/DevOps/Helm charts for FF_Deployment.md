---
aliases: []
confidence: 
created: 2025-02-27T02:44:32Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: Helm charts for FF_Deployment
type: 
uid: 
updated: 
version: 
---

## I. Overview and Core Functionality

### 1. Purpose and Architecture

The Helm charts appear to be part of a FITFile application deployment system that consists of several key components:

The main components include:

- Core application services (frontend, ffcloud-service, ffnode, fitconnect)
- Database services (PostgreSQL, MongoDB, MinIO)
- Infrastructure components (certs, shared-secrets, spicedb)
- CI/CD tooling (ArgoCD)

### 2. Helm Chart Structure

The chart structure follows this organization:

```sh
charts/
├── argo/
│   ├── cd/
│   └── workflows/
├── certs/
├── databases/
├── frontend/
├── ffcloud-service/
├── ffnode/
├── fitconnect/
└── shared-secrets/
```

Key subcharts identified:

1. **ArgoCD (argo/cd)**
   - Purpose: GitOps deployment management
   - Integration: Uses official Argo Helm chart (version 6.11.1)
   - Values: Configured in values.yaml, values-prod.yaml, values-sh.yaml

2. **Databases**
   - Dependencies:
     - PostgreSQL (12.7.3)
     - MongoDB (12.1.31)
     - MinIO (12.13.2)
   - Integration: Uses Bitnami charts
   - Values: Configured through global values and specific database sections

Custom Helm templates found:

- `_names.tpl`: Defines common naming conventions
- `_secrets.tpl`: Handles secret management

## II. Customer Management and Multi-Tenancy

### 1. Current Customer Handling

The codebase shows evidence of multi-environment deployment with separate value files:

- `values.yaml`: Default configuration
- `values-prod.yaml`: Production environment
- `values-sh.yaml`: Staging/QA environment

Example from ArgoCD configuration:

```yaml
# values-prod.yaml
argo-cd:
  server:
    ingress:
      hosts:
        - argocd.fitfile.net
```

```yaml
# values-sh.yaml
argo-cd:
  server:
    ingress:
      hosts:
        - argocd-sh.fitfile.net
```

### 2. ArgoCD Integration

ArgoCD is configured with:

- OIDC authentication with Azure AD
- RBAC policies for different user roles
- Ingress configurations for different environments

Example RBAC configuration:

```yaml
rbac:
  policy.csv: |
     p, role:org-admin, applications, *, */*, allow
     p, role:readonly, applications, get, */*, allow
```

## III. Deep Dive into Key Templates

1. **Database Backup Templates**
   - Purpose: Manages automated database backups
   - Key features:
     - Configurable backup schedules
     - Retention policy
     - Persistent volume management

2. **MongoDB Web Interface**
   - Provides web-based database management
   - Configurable ingress and authentication

## IV. Recommendations for Improvement

### 1. Separation of Data and Implementation

Recommend implementing:

1. Customer-specific values directory:

```sh
values/
├── customers/
│   ├── customer-a/
│   │   ├── values.yaml
│   │   └── secrets.yaml
│   └── customer-b/
│       ├── values.yaml
│       └── secrets.yaml
└── environments/
    ├── prod.yaml
    └── staging.yaml
```

2. Use ApplicationSets for customer management:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: fitfile-customers
spec:
  generators:
    - git:
        repoURL: https://gitlab.com/fitfile/deployment.git
        revision: HEAD
        files:
        - path: "values/customers/*/values.yaml"
  template:
    metadata:
      name: '{{customer}}'
    spec:
      source:
        repoURL: https://gitlab.com/fitfile/deployment.git
        targetRevision: HEAD
        path: charts
        helm:
          valueFiles:
          - values/customers/{{customer}}/values.yaml
```

### 2. Code Reusability

Recommend:

1. Creating shared helper templates
2. Implementing consistent naming conventions
3. Using Helm library charts for common patterns

### 3. ArgoCD Optimization

Recommend:

1. Implementing ApplicationSets for customer management
2. Using sync waves for deployment ordering
3. Implementing automated rollback policies

## V. Usage Guide

### 1. Deployment Instructions

To deploy a new customer:

```bash
# 1. Create customer values file
cp values/template/values.yaml values/customers/new-customer/values.yaml

# 2. Update customer-specific values

# 3. Create ArgoCD application
kubectl apply -f applications/new-customer.yaml
```

### 2. Troubleshooting

Common issues:

1. Database backup failures
   - Check PVC availability
   - Verify backup credentials
2. ArgoCD sync failures
   - Check Git repository access
   - Verify value file syntax

Would you like me to expand on any particular section or provide more specific details about any aspect of the analysis?

Current Structure Analysis:

```sh
ffnodes/
├── barts/
├── eoe/
│   ├── ff-eoe-sde/
│   ├── ff-hyve-1/
│   ├── ff-hyve-2/
│   └── hie-prod-34/
├── fitfile/
│   ├── ff-a/
│   ├── ff-b/
│   ├── ff-c/
│   ├── ff-test-a/
│   ├── ff-test-b/
│   └── ff-test-c/
├── kch/
└── empty-values.yaml
```

Key Observations:

1. Values files are currently organized by customer/environment
2. There's significant duplication across environments (e.g., ff-test-a/b/c share many settings)
3. Some customers have multiple environments (e.g., EOE has multiple deployments)
4. The values contain both customer-specific and environment-specific configurations

Recommendation: I would recommend separating the values into a different repository for several reasons:

1. **Clear Separation of Concerns**

```sh
deployment-repo/
└── charts/                 # Core Helm charts (implementation)
    └── ffnode/
        ├── Chart.yaml
        ├── values.yaml    # Default values
        └── templates/
customer-config-repo/
├── _common/              # Shared configurations
│   ├── prod.yaml
│   └── staging.yaml
├── barts/
│   ├── _defaults.yaml   # Barts-specific defaults
│   └── prod.yaml        # Production overrides
└── eoe/
    ├── _defaults.yaml
    ├── sde.yaml
    └── hyve-1.yaml
```

Benefits:

1. **Cleaner Git History**: Changes to implementation (charts) vs configuration (values) are separate
2. **Access Control**: Can give customers access to only their config repo
3. **Simpler Reviews**: Configuration changes can be reviewed independently
4. **Better Reuse**: Common configurations can be shared more easily
5. **Versioning**: Can version customer configs independently of chart versions

Example of how this would work:

```yaml
# _common/prod.yaml
global:
  environment: production
  monitoring:
    enabled: true
```

```yaml
# barts/_defaults.yaml
global:
  customer: barts
  fitConnectCode: "Barts"

frontend:
  appConfig:
    tenantName: "St Bartholomew's Hospital"
```

```yaml
# barts/prod.yaml
imports:
  - ../_common/prod.yaml
  - ./_defaults.yaml

host: barts.fitfile.net
namespace: barts

# Only override what's specific to this environment
minio:
  persistence:
    size: 64Gi
    existingClaim: pvc-barts-minio
```

ArgoCD ApplicationSet example:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: customer-deployments
spec:
  generators:
    - git:
        repoURL: https://gitlab.com/fitfile/customer-config.git
        revision: HEAD
        files:
        - path: "**/prod.yaml"
  template:
    metadata:
      name: '{{customer}}-{{environment}}'
    spec:
      source:
        repoURL: https://gitlab.com/fitfile/deployment.git
        path: charts/ffnode
        targetRevision: latest-release
        helm:
          valueFiles:
            - https://gitlab.com/fitfile/customer-config.git/{{path}}
      destination:
        server: '{{server}}'
        namespace: '{{namespace}}'
```

This approach would:

1. Make it easier to add new customers (just add a new directory)
2. Reduce duplication through inheritance
3. Keep sensitive customer data separate from implementation
4. Make it easier to track customer-specific changes
5. Allow for better template validation through schemas
