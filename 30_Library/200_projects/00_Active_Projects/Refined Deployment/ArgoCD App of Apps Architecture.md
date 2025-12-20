---
aliases: []
confidence: 
created: 2025-09-04T07:55:44Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [config, helm]
title: ArgoCD App of Apps Architecture
type:
uid: 
updated: 
version:
---

Based on my investigation of the FITFILE deployment infrastructure, here's how ArgoCD is organized to manage Helm charts and applications:

## **ArgoCD Architecture Overview**

### **1. Three-Tier Application Management**

**Tier 1: Root ArgoCD Installation**

- **Chart**: `/charts/argo/cd/` - ArgoCD itself deployed via Helm
- **Dependencies**: Uses upstream `argo-cd` chart version 6.11.1
- **Purpose**: Provides the GitOps control plane

**Tier 2: App of Apps Pattern (FFNode Umbrella)**

- **Chart**: `/charts/ffnode/` - The main umbrella chart
- **Purpose**: Generates multiple ArgoCD `Application` CRDs
- **Pattern**: Each component becomes a separate ArgoCD Application

**Tier 3: Individual Applications**

- **Components**: MongoDB, PostgreSQL, FitConnect, FFCloud, Frontend, etc.
- **Management**: Each managed as independent ArgoCD Application
- **Deployment**: ArgoCD renders Helm → Kubernetes manifests

### **2. Application Generation Pattern**

The FFNode umbrella chart generates **20+ ArgoCD Applications**:

```yaml
# Example: MongoDB Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: { { include "mongodbReleaseName" . } }
  namespace: argocd
spec:
  source:
    chart: helm/mongodb
    repoURL: "fitfileregistry.azurecr.io"
    targetRevision: { { .Values.mongodb.targetRevision } }
    helm:
      releaseName: { { include "mongodbReleaseName" . } }
      values: |
        # Helm values merged from multiple sources
```

### **3. Helm Chart Sources**

**Three distinct source patterns:**

1. **OCI Registry (ACR)** - Bitnami charts imported via Chart Manager

```yaml
chart: helm/mongodb
   repoURL: "fitfileregistry.azurecr.io"
```

2. **Git Repository** - Custom FITFILE charts

```yaml
path: charts/fitconnect
repoURL: https://gitlab.com/fitfile/deployment.git
```

3. **External Helm Repositories** - Third-party charts

```yaml
chart: cert-manager
repoURL: https://charts.jetstack.io
```

### **4. ApplicationSet Pattern**

For multi-environment deployments, **ApplicationSets** generate multiple Applications:

```yaml
# /ffnodes/kch/prod/templates/kch-prod-application-set.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  generators:
    - list:
        elements:
          - serviceName: databases
          - serviceName: ffcloud-service
          - serviceName: fitconnect
  template:
    spec:
      source:
        path: charts/{{serviceName}}
        helm:
          valueFiles:
            - "{{values.appConfig}}"
            - "{{values.infraConfig}}"
```

## **Key Architectural Insights**

### **1. ArgoCD Renders Helm, Not Kubernetes**

You're correct that ArgoCD compiles Helm charts into Kubernetes manifests before applying them. This means:

- **No Helm releases** exist in the cluster
- **ArgoCD tracks** the rendered Kubernetes resources
- **Helm templating** happens within ArgoCD's repo-server
- **Values injection** occurs during ArgoCD sync

### **2. Multi-Source Value Composition**

Complex value merging happens in templates:

```yaml
{
  {
    - $values := mergeOverwrite
    (include "fitconnectValues" . | fromYaml)
    .Values.fitconnect
    (dict "global" .Values.global) -
  }
}
```

### **3. Sync Wave Orchestration**

Applications deploy in coordinated waves:

```yaml
annotations:
  argocd.argoproj.io/sync-wave: "0"  # Infrastructure first
  argocd.argoproj.io/sync-wave: "3"  # Applications later
```

### **4. Environment-Specific Patterns**

**Development**: Single Application with embedded values

```yaml
# /charts/local-dev/argocd-apps-values.yaml
applications:
  - name: fitfile
    source:
      path: charts/ffnode
      helm:
        values: |
          # All values embedded inline
```

**Production**: ApplicationSet with external value files

```yaml
# ApplicationSet references external files
helm:
  valueFiles:
    - /ffnodes/kch/prod/values/ffcloud/app-config.yaml
    - /ffnodes/kch/prod/values/ffcloud/infra-config.yaml
```

## **Codebase Organization Around ArgoCD**

### **1. Directory Structure**

```sh
charts/
├── argo/cd/              # ArgoCD installation
├── ffnode/               # App of Apps umbrella
│   └── templates/        # Application CRD generators
├── fitconnect/           # Individual service charts
├── ffcloud-service/
└── databases/

ffnodes/
├── fitfile/testing/      # Environment-specific values
├── kch/prod/
│   ├── values/          # Structured value files
│   └── templates/       # ApplicationSet definitions
```

### **2. Configuration Hierarchy**

1. **Chart defaults** in `charts/*/values.yaml`
2. **Global overrides** in [charts/ffnode/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0)
3. **Environment values** in `ffnodes/*/values.yaml`
4. **ApplicationSet values** in `ffnodes/*/values/*/`

### **3. GitOps Workflow**

1. **Developers** modify charts or values
2. **ArgoCD** detects Git changes
3. **Repo-server** renders Helm templates
4. **Application Controller** applies Kubernetes manifests
5. **Sync waves** ensure proper deployment order

## **Benefits Of This Architecture**

### **1. Separation of Concerns**

- **Infrastructure** (databases, monitoring) vs **Applications** (fitconnect, ffcloud)
- **Chart logic** vs **Environment configuration**
- **Global settings** vs **Service-specific** configuration

### **2. Scalability**

- **ApplicationSets** enable multi-tenant deployments
- **Independent Applications** allow selective updates
- **Parallel deployment** of non-dependent services

### **3. Observability**

- **Per-application** sync status and health
- **Resource-level** drift detection
- **Sync wave** progress tracking

### **4. Flexibility**

- **Mixed source types** (OCI, Git, Helm repos)
- **Value composition** from multiple sources
- **Environment-specific** deployment patterns

This architecture effectively bridges Helm's templating capabilities with ArgoCD's GitOps workflow, providing both the flexibility of Helm charts and the declarative management of ArgoCD Applications.

## FITFILE Deployment Component Inventory

Based on my analysis of the FITFILE deployment infrastructure, here's a comprehensive list of all components and their deployment methods:

### **🔧 Terraform-Deployed Foundational Components**

*Deployed via [terraform-helm-fitfile-platform](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform:0:0-0:0) module - Required before ArgoCD*

| Component                  | Chart Source                        | Namespace                       | Purpose                                        |
| -------------------------- | ----------------------------------- | ------------------------------- | ---------------------------------------------- |
| **Vault Secrets Operator** | `helm/vault-secrets-operator` (ACR) | `vault-secrets-operator-system` | Secret management from HashiCorp Vault         |
| **Reflector**              | `helm/reflector` (ACR)              | `reflector`                     | Secret/ConfigMap replication across namespaces |
| **Ingress NGINX**          | `helm/ingress-nginx` (ACR)          | `ingress-nginx`                 | Load balancer and ingress controller           |
| **ArgoCD**                 | `helm/argo-cd` (ACR)                | `argocd`                        | GitOps deployment platform                     |
| **ArgoCD Apps**            | `helm/argocd-apps` (ACR)            | `argocd`                        | Initial ArgoCD Application definitions         |
| **Cluster Autoscaler**     | `helm/cluster-autoscaler` (ACR)     | `kube-system`                   | AWS EKS node scaling (AWS only)                |

### **🚀 ArgoCD-Managed Applications**

*Deployed via ArgoCD App of Apps pattern from FFNode umbrella chart*

#### **Infrastructure & Platform Services**

| Component              | Chart Source                          | Namespace                                                                                                                                                                           | Deployment Condition                             |
| ---------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Cert Manager**       | `cert-manager` (charts.jetstack.io)   | `cert-manager`                                                                                                                                                                      | `deploy.initialiseCluster && deploy.certManager` |
| **Certificates**       | `charts/certs` (Git)                  | Various                                                                                                                                                                             | `deploy.certManager`                             |
| **Argo Workflows**     | `helm/argo-workflows` (ACR)           | [argo](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/argo:0:0-0:0) | `deploy.initialiseCluster`                       |
| **Blob CSI Driver**    | `blob-csi-driver` (GitHub)            | `kube-system`                                                                                                                                                                       | `deploy.blobCsiDriver`                           |
| **Prometheus CRDs**    | `helm/prometheus-operator-crds` (ACR) | Various                                                                                                                                                                             | `deploy.monitoring`                              |
| **Grafana Monitoring** | `helm/k8s-monitoring` (ACR)           | `monitoring`                                                                                                                                                                        | `deploy.monitoring`                              |
| **Vault**              | `vault` (HashiCorp)                   | `vault`                                                                                                                                                                             | `deploy.vault`                                   |

#### **Database & Storage Services**

| Component              | Chart Source            | Namespace            | Deployment Condition                       |
| ---------------------- | ----------------------- | -------------------- | ------------------------------------------ |
| **MongoDB (Legacy)**   | `helm/mongodb` (ACR)    | Environment-specific | `deploy.persistence`                       |
| **MongoDB (Next-Gen)** | `helm/mongodb` (ACR)    | Environment-specific | `deploy.persistence && deploy.mongodbNext` |
| **PostgreSQL**         | `helm/postgresql` (ACR) | Environment-specific | `deploy.persistence`                       |
| **MinIO**              | `helm/minio` (ACR)      | Environment-specific | `deploy.persistence`                       |
| **SpiceDB**            | `charts/spicedb` (Git)  | `spicedb`            | `deploy.spicedb`                           |

#### **FITFILE Application Services**

| Component                  | Chart Source                          | Namespace            | Deployment Condition          |
| -------------------------- | ------------------------------------- | -------------------- | ----------------------------- |
| **FitConnect**             | `charts/fitconnect` (Git)             | Environment-specific | `deploy.fitconnect`           |
| **FFCloud Service**        | `charts/ffcloud-service` (Git)        | Environment-specific | `deploy.coordinatingStation`  |
| **Frontend**               | `charts/frontend` (Git)               | Environment-specific | `deploy.frontend`             |
| **Workflows API**          | `charts/workflows-api` (Git)          | Environment-specific | `deploy.workflowsApi`         |
| **Mutating Proxy Webhook** | `charts/mutating-proxy-webhook` (Git) | Environment-specific | `deploy.mutatingProxyWebhook` |

#### **Workflow & Testing Services**

| Component                      | Chart Source                        | Namespace            | Deployment Condition               |
| ------------------------------ | ----------------------------------- | -------------------- | ---------------------------------- |
| **Workflow Templates**         | `workflows/src` (Git)               | Environment-specific | Always deployed                    |
| **Integration Test Templates** | `workflows/integration-tests` (Git) | Environment-specific | `deploy.workflowsIntegrationTests` |
| **Seed Data**                  | `charts/local-dev/seed` (Git)       | Environment-specific | `deploy.seedData`                  |

### **🌍 Deployment Environments**

#### **FITFILE Environments** (34 deployments)

- **Development**: `fitfile/development`, `fitfile/acr-test`, `fitfile/wm-dev-1`, [fitfile/testing](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/testing:0:0-0:0)
- **Test**: `fitfile/ff-test-a`, `fitfile/ff-test-b`, `fitfile/ff-test-c`
- **Production**: `fitfile/ff-a`, `fitfile/ff-b`, `fitfile/ff-c`, `fitfile/primary-care`, `fitfile/pentest`
- **Special**: `fitfile/pv-aks-1`, `fitfile/gh-pt-1`

#### **Partner Environments**

- **EOE**: `eoe/cuh-prod-1`, `eoe/ff-eoe-sde`, `eoe/ff-hyve-1`, `eoe/ff-hyve-2`, `eoe/hie-prod-34`
- **BARTS**: `barts/prod`
- **KCH**: `kch/mn4`, `kch/prod` (ApplicationSet pattern)
- **STG**: `stg/sandbox` (ApplicationSet pattern)
- **WMSDE**: `wmsde/ff-wmsde-1`

#### **ApplicationSet Deployments**

Multi-service deployments using ApplicationSet pattern:

**KCH Production & MN4**:

- `databases`, `ffcloud-service`, `fitconnect`, `frontend`, `shared-secrets`

**STG Sandbox**:

- Similar service pattern with staging configurations

### **📊 Deployment Statistics**

| Deployment Method       | Component Count  | Purpose                     |
| ----------------------- | ---------------- | --------------------------- |
| **Terraform Helm**      | 6 components     | Foundational infrastructure |
| **ArgoCD Applications** | 20+ components   | Application workloads       |
| **Total Environments**  | 40+ environments | Multi-tenant deployments    |

### **🔄 Deployment Flow**

1. **Terraform Phase**: Deploy foundational components (VSO, Reflector, Ingress, ArgoCD)
2. **ArgoCD Bootstrap**: ArgoCD deploys initial Applications
3. **App of Apps**: FFNode umbrella generates individual Applications
4. **Environment Sync**: ArgoCD syncs all applications per environment
5. **ApplicationSet**: Multi-environment deployments via generators

This architecture ensures proper dependency ordering while maximizing the benefits of GitOps management through ArgoCD.
