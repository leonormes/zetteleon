---
aliases: []
confidence: 
created: 2025-09-11T11:07:10Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [applications, argocd, configuration, ff-a, project/work/deployment]
title: FF-A applications
type:
uid: 
updated: 
version:
---

Based on my analysis of the ArgoCD application templates and the ff-a deployment configuration, here are the applications deployed to ff-a and their configured versions:

## **ArgoCD Applications Deployed to ff-a**

### **Third-Party Charts (from ACR)**

| Application                | Chart Source                                               | Version   | Notes                                             |
| -------------------------- | ---------------------------------------------------------- | --------- | ------------------------------------------------- |
| **MongoDB**                | `fitfileregistry.azurecr.io/helm/mongodb`                  | `16.5.*`  | Configured in ff-a values.yaml                    |
| **PostgreSQL**             | `fitfileregistry.azurecr.io/helm/postgresql`               | `15.5.15` | Fixed version                                     |
| **MinIO**                  | `fitfileregistry.azurecr.io/helm/minio`                    | `14.7.8`  | Fixed version                                     |
| **Cert-Manager**           | `fitfileregistry.azurecr.io/helm/cert-manager`             | `v1.18.2` | Fixed version                                     |
| **Argo Workflows**         | `fitfileregistry.azurecr.io/helm/argo-workflows`           | Variable  | Uses `.Values.argoWorkflows.chart.targetRevision` |
| **Grafana K8s Monitoring** | `fitfileregistry.azurecr.io/helm/k8s-monitoring`           | `1.5.4`   | Fixed version                                     |
| **Prometheus CRDs**        | `fitfileregistry.azurecr.io/helm/prometheus-operator-crds` | `8.0.1`   | Fixed version                                     |
| **Blob CSI Driver**        | External repo                                              | `1.21.4`  | Fixed version                                     |

### **FITFILE Internal Charts (from GitLab)**

| Application                    | Source                              | Version          |
| ------------------------------ | ----------------------------------- | ---------------- |
| **FitConnect**                 | `charts/components/fitconnect`      | `latest-release` |
| **FFCloud Service**            | `charts/components/ffcloud-service` | `latest-release` |
| **Frontend**                   | `charts/components/frontend`        | `latest-release` |
| **SpiceDB**                    | `charts/spicedb`                    | `latest-release` |
| **Workflow Templates**         | `workflows/src`                     | `latest-release` |
| **Workflows API**              | `charts/workflows-api`              | `latest-release` |
| **Integration Test Templates** | `workflows/integration-tests`       | `latest-release` |
| **Certificates**               | `charts/certs`                      | `latest-release` |
| **Seed Data**                  | `charts/local-dev/seed`             | `latest-release` |
| **Mutating Proxy Webhook**     | `charts/mutating-proxy-webhook`     | `latest-release` |

### **Key Configuration Details**

- **Target Revision**: Most internal applications use `{{.Values.argocdApp.targetRevision}}` which is set to `"latest-release"` in ff-a
- **Namespace**: All applications deploy to the `ff-a` namespace
- **Host**: Primary host is `app.fitfile.net`
- **MongoDB Version**: Uses `16.5.*` pattern allowing patch updates
- **Custom Deployment**: Includes a custom PgWeb deployment for database UI access

The ff-a deployment represents a production environment with a mix of third-party infrastructure components (databases, monitoring) and FITFILE's custom applications, all managed through ArgoCD.
