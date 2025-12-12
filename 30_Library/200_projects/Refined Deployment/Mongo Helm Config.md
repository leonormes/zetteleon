---
aliases: []
confidence: 
created: 2025-09-03T04:57:08Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [configuration, database, helm, mongodb, storage]
title: Mongo Helm Config
type:
uid: 
updated: 
version:
---

## MongoDB Configuration Analysis

Based on my analysis of the FITFILE deployment infrastructure, here's a comprehensive trace of MongoDB configurations and recommendations for consolidating Helm config handling:

### MongoDB Configuration Locations

#### **1. Testing Deployment ([/ffnodes/fitfile/testing/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/testing/values.yaml:0:0-0:0))**

```yaml
mongodb:
  targetRevision: "16.5.*"
  replicaCount: 1
```

#### **2. FFNode Umbrella Chart ([/charts/ffnode/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0))**

**Two MongoDB configurations exist:**

**Legacy MongoDB (lines 129-163):**

```yaml
mongodb:
  global:
    security:
      allowInsecureImages: true
  releaseName: ""
  persistence:
    enabled: true
  architecture: replicaset
  replicaCount: 2
  auth:
    existingSecret: mongodb
  vaultSecrets:
    - secretName: "mongodb"
      vaultPath: '{{ include "applicationVaultPath" . }}'
```

**Next-Gen MongoDB (lines 95-128):**

```yaml
mongodbNext:
  global:
    security:
      allowInsecureImages: true
  targetRevision: "16.5.*"
  persistence:
    enabled: true
  architecture: replicaset
  replicaCount: 2
  # No secrets as uses the mongodb secret
  vaultSecrets: []
```

#### **3. Databases Chart ([/charts/databases/Chart.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/databases/Chart.yaml:0:0-0:0) & [values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0))**

```yaml
# Chart.yaml dependency
- name: mongodb
  version: 16.5.0
  condition: global.deployMongo
  repository: https://charts.bitnami.com/bitnami

# values.yaml configuration
mongodb:
  persistence:
    enabled: true
  architecture: replicaset
  replicaCount: 2
  auth:
    rootPassword: fitconn5766  # Hardcoded password!
```

#### **4. MongoDB Host Resolution ([/charts/ffnode/templates/\_mongodb.tpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/_mongodb.tpl:0:0-0:0))**

Complex templating logic handles both legacy and versioned MongoDB deployments:

- `mongodbHost` - Legacy host resolution
- `newMongodbHost` - Next-gen versioned host resolution
- Version-based switching logic using semantic versioning

#### **5. Connection String Usage**

MongoDB connection strings appear in **77 files** across:

- **Vault secrets** (fitconnect, ffcloud, frontend, workflows)
- **Integration test templates**
- **Backup configurations**
- **Web UI configurations**

### Current Helm Configuration Issues

#### **1. Configuration Fragmentation**

- **Multiple MongoDB versions** managed simultaneously (legacy vs next-gen)
- **Inconsistent patterns** across different charts
- **Hardcoded secrets** in databases chart vs Vault integration in ffnode
- **Duplicate configurations** between umbrella and sub-charts

#### **2. Complex Template Logic**

- **Version-based switching** in [\_mongodb.tpl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/_mongodb.tpl:0:0-0:0) creates maintenance overhead
- **Multiple host resolution functions** for different MongoDB versions
- **Conditional deployment logic** scattered across templates

#### **3. Security Inconsistencies**

- **Hardcoded passwords** in databases chart (`fitconn5766`)
- **Mixed secret management** (Vault vs hardcoded vs existing secrets)
- **Inconsistent image security settings**

### Consolidation Recommendations

#### **1. Centralized Chart Management**

Based on the existing **Chart Manager** infrastructure and the memories about PostgreSQL centralization:

```yaml
# Extend helm_chart_list.yaml
charts:
  - chart_name: mongodb
    repo_url: oci://registry-1.docker.io/bitnamicharts
    repo_name: bitnami
    acr_name: fitfileregistry
    chart_dir: helm/mongodb
    tfc_chart_name: mongodb
    # Add version management
    default_version: "16.5.*"
    environments:
      - testing
      - staging
      - production
```

#### **2. Unified MongoDB Configuration Pattern**

Create a single MongoDB configuration approach:

```yaml
# Standardized mongodb section
mongodb:
  # Version management through Chart Manager
  targetRevision: "16.5.*"

  # Consistent deployment settings
  architecture: replicaset
  replicaCount: 2
  persistence:
    enabled: true

  # Standardized security
  global:
    security:
      allowInsecureImages: true
  auth:
    existingSecret: mongodb

  # Unified Vault integration
  vaultSecrets:
    - secretName: "mongodb"
      vaultPath: '{{ include "applicationVaultPath" . }}'
      secretTransformation:
        templates:
          mongodb-replica-set-key:
            text: '{{get .Secrets "mongodb_replica_set_key"}}'
          mongodb-root-password:
            text: '{{get .Secrets "mongodb_password"}}'
```

#### **3. Template Simplification**

Replace complex version switching with a single pattern:

```yaml
# Simplified _mongodb.tpl
{{- define "mongodbHost" -}}
{{- $releaseName := include "mongodbReleaseName" . -}}
{{- $namespace := include "coordinatorNamespace" . -}}
{{- $replicaCount := int .Values.mongodb.replicaCount -}}
{{- $mongoHosts := list -}}
{{- range $index := untilStep 0 $replicaCount 1 -}}
{{- $mongoHosts = append $mongoHosts (printf "%s-%d.%s-headless.%s.svc.cluster.local:27017" $releaseName $index $releaseName $namespace) -}}
{{- end -}}
{{- join "," $mongoHosts }}
{{- end -}}
```

#### **4. Configuration Hierarchy**

Establish clear precedence:

1. **Chart Manager** - Version and image management
2. **FFNode umbrella** - Deployment and infrastructure settings
3. **Environment-specific** - Overrides in ffnodes/\*/values.yaml
4. **Databases chart** - Remove MongoDB, focus on PostgreSQL/MinIO

#### **5. Migration Strategy**

1. **Phase 1**: Standardize on `mongodbNext` pattern across all deployments
2. **Phase 2**: Remove legacy `mongodb` configuration and templates
3. **Phase 3**: Integrate with Chart Manager for centralized version control
4. **Phase 4**: Remove MongoDB from databases chart, make it ffnode-only

#### **6. Security Standardization**

- **Remove hardcoded passwords** from databases chart
- **Standardize on Vault integration** across all environments
- **Consistent secret naming** and transformation patterns

### Summary

The current MongoDB configuration is fragmented across multiple charts with inconsistent patterns, security approaches, and complex version management. Following the successful PostgreSQL centralization pattern from the memories, consolidating MongoDB configuration through the Chart Manager infrastructure would significantly simplify maintenance while improving security and consistency across all FITFILE deployments.

**Key Benefits:**

- **Single source of truth** for MongoDB versions
- **Consistent security patterns** across all environments
- **Simplified template logic** and reduced maintenance overhead
- **Centralized version control** through Terraform Cloud integration
- **Improved deployment reliability** through standardized configurations
