---
aliases: []
confidence: 
created: 2025-09-03T11:22:41Z
epistemic: 
last_reviewed: 
modified: 2025-11-01T15:08:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, dependencies, ffnode, helm, umbrella-chart]
title: FFNODE as Umbrella Chart
type:
uid: 
updated: 
version:
---

## Chart Dependencies Analysis: Ffnode as Umbrella Chart

Based on my analysis of your current architecture, I have mixed recommendations about using [Chart.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/Chart.yaml:0:0-0:0) dependencies for the ffnode umbrella chart.

### Current Architecture

**ffnode currently uses ArgoCD Applications approach:**

- 20 separate [-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/postgresql-application.yaml:0:0-0:0) templates in ffnode
- Each creates an ArgoCD Application for components (postgresql, mongodb, spicedb, etc.)
- Components deployed as separate Helm releases
- Managed through GitOps workflow

**Other charts DO use dependencies:**

- [databases/Chart.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/databases/Chart.yaml:0:0-0:0) - has postgresql, mongodb, minio dependencies
- [spicedb/Chart.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/spicedb/Chart.yaml:0:0-0:0) - has postgresql dependency with version `15.5.15`

### Recommendation: **Hybrid Approach**

**Keep ArgoCD Applications for most components** but consider [Chart.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/Chart.yaml:0:0-0:0) dependencies for:

#### ✅ **Good Candidates for Chart.yaml dependencies:**

- **Core databases** (postgresql, mongodb, minio) - tightly coupled, shared across services
- **Infrastructure components** (cert-manager, vault) - foundational requirements
- **Monitoring stack** - cohesive unit

#### ❌ **Keep As ArgoCD Applications:**

- **Application services** (ffcloud, fitconnect, frontend) - business logic, independent lifecycles
- **Integration components** - may need separate deployment timing
- **Optional components** - controlled by feature flags

### Benefits of This Approach

**Chart.yaml dependencies for core components:**

- **Centralized version control** - exactly what you want for PostgreSQL
- **Dependency ordering** - databases deploy before applications
- **Atomic deployments** - core infrastructure as a unit

**ArgoCD Applications for services:**

- **Independent scaling** - services can be updated separately
- **Feature toggles** - easier to enable/disable components
- **GitOps workflow** - maintains your current operational model

### Implementation for PostgreSQL Version Control

```yaml
# ffnode/Chart.yaml
dependencies:
  - name: postgresql
    version: "15.5.15" # This could be templated from version manager
    repository: oci://fitfileregistry.azurecr.io/helm
    condition: deploy.persistence
```

This would give you the centralized version control you want while maintaining flexibility for your application services.

**Would you like to explore this hybrid approach for PostgreSQL version management?**
