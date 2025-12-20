---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, helm]
title: Simplify the helm charts
type:
uid: 
updated: 
version:
---

## Current Structure Analysis

From what I can see, the repository currently mixes several concerns:

1. Infrastructure Code (Helm Charts)
2. Configuration Data (Values files)
3. Customer-Specific Settings (ffnodes directory)
4. Deployment Templates (ArgoCD configurations)

Let's explore how we can better organize this.

## Proposed Repository Structure

```sh
├── charts/                    # Core Helm Charts (CODE)
│   ├── ffcloud-service/
│   ├── databases/
│   └── hutch/
│
├── platform/                  # Platform Configuration (CODE)
│   ├── base/                 # Base configurations
│   │   ├── argocd/
│   │   ├── cert-manager/
│   │   └── vault/
│   └── templates/            # Reusable templates
│       ├── deployment/
│       └── service/
│
├── customers/                # Customer Data (DATA)
│   ├── _template/           # Template for new customer onboarding
│   └── instances/           # Customer instances
│       ├── fitfile/
│       ├── barts/
│       └── kch/
│
└── environments/            # Environment Configurations (DATA)
    ├── production/
    ├── staging/
    └── development/
```

## Detailed Breakdown

### 1. Code-Data Separation

#### Code Repositories

```sh
helm-charts/                  # Core Helm Charts Repository
├── charts/
│   ├── ffcloud-service/     # Main application service
│   ├── databases/           # Database configurations
│   └── hutch/              # Other services
├── tests/                   # Helm test suite
└── docs/                    # Documentation
```

#### Data Repository

```sh
customer-configs/            # Customer Configuration Repository
├── _template/              # New customer template
│   ├── values/
│   └── secrets/           # Vault secret templates
├── instances/             # Customer instances
│   ├── fitfile/
│   │   ├── ff-a/
│   │   ├── ff-b/
│   │   └── ff-c/
│   └── barts/
└── environments/          # Environment-specific configurations
    ├── production/
    └── staging/
```

### 2. Improved Organization

Let's create this structure with some example files:

```yaml
# _template/values/base.yaml
# Template for new customer configuration
customer:
  name: CUSTOMER_NAME
  environment: ENVIRONMENT
  domain: DOMAIN

global:
  dbSuffix: DB_SUFFIX
  features:
    enabled: []

# Standard configuration sections follow...
```

```yaml
# _template/argocd/application.yaml
# Template for ArgoCD application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ${CUSTOMER_NAME}-${ENVIRONMENT}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${HELM_CHARTS_REPO}
    targetRevision: ${TARGET_REVISION}
    path: charts/ffcloud-service
    helm:
      valueFiles:
        - values/base.yaml
        - values/customer-specific.yaml
```

### 3. Implementation Steps

1. Create New Repository Structure:

```bash
# Create new repositories
git clone existing-repo helm-charts
git clone existing-repo customer-configs

# Set up template structure
mkdir -p customer-configs/_template/{values,secrets,argocd}
```

2. Move Existing Files:

```bash
# Move Helm charts to helm-charts repo
mv ffcloud-service/ helm-charts/charts/
mv databases/ helm-charts/charts/

# Move customer configs to customer-configs repo
mv ffnodes/ customer-configs/instances/
```

1. Update References:

```yaml
# Update ArgoCD application references
spec:
  source:
    repoURL: git@github.com:your-org/helm-charts.git
    path: charts/ffcloud-service
    helm:
      valueFiles:
        - https://raw.githubusercontent.com/your-org/customer-configs/main/instances/fitfile/ff-a/values.yaml
```

### 4. Benefits and Improvements

2. Clear Separation of Concerns
   - Code (Helm charts) in one repository
   - Configuration (customer data) in another
   - Easier to manage access control
   - Clearer audit trail

3. Standardized Customer Onboarding

   ```bash
   # Script to create new customer
   ./scripts/create-customer.sh \
     --name "new-customer" \
     --environment "production" \
     --domain "customer.fitfile.net"
   ```

4. Improved Documentation

   ```markdown
   # Customer Configuration Guide
   
   ## Directory Structure
   - `values/`: Customer-specific values
   - `secrets/`: Vault secret templates
   - `argocd/`: ArgoCD applications
   
   ## Adding a New Customer
   1. Copy `_template` directory
   2. Update values in `values/base.yaml`
   3. Configure secrets in Vault
   4. Create ArgoCD application
   ```

5. Better Version Control
   - Separate commit history for code and configuration
   - Easier to track configuration changes
   - Simpler rollbacks of configuration changes

6. Enhanced Security
   - Separate access controls for code and configuration
   - Clearer audit trail for configuration changes
   - Better secret management

### 5. Migration Plan

7. Preparation Phase

```bash
# Create new repositories
git clone git@github.com:your-org/helm-charts.git
git clone git@github.com:your-org/customer-configs.git

# Set up template structure
./scripts/setup-template.sh
```

8. Migration Phase

```bash
# Migrate existing customers
for customer in ffnodes/; do
  ./scripts/migrate-customer.sh "$customer"
done

# Update ArgoCD applications
./scripts/update-argocd-apps.sh
```

9. Validation Phase

```bash
# Validate customer configurations
./scripts/validate-configs.sh

# Test deployments in staging
./scripts/test-deployment.sh --environment staging
```

This reorganization will make the codebase more maintainable, easier to understand, and more secure. It separates concerns appropriately and provides a clear path for adding new customers or making changes to existing ones.
