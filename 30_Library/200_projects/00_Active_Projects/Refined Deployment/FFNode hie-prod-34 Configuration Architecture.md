---
aliases: []
confidence: 
created: 2025-09-06T10:32:10Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [architecture, configuration, ffnode, hie-prod-34, hyve, project/work/deployment]
title: FFNode hie-prod-34 Configuration Architecture
type:
uid: 
updated: 
version:
---

## **1. Directory Structure**

```sh
ffnodes/eoe/hie-prod-34/
├── values.yaml           # Main FFNode configuration
├── thehyve_values.yaml   # TheHyve integration overrides
├── hutch_values.yaml     # Hutch/Bunny relay overrides
└── README.md            # Documentation and setup instructions
```

## **2. ArgoCD Application Structure**

The hie-prod-34 node consists of **3 separate ArgoCD Applications**:

1. **Main FFNode Application** ([values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/values.yaml:0:0-0:0))
   - **Chart**: [charts/ffnode](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode:0:0-0:0)
   - **Namespace**: [hie-prod-34](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34:0:0-0:0)
   - **Target Revision**: `eoe-latest-release` git tag

2. **TheHyve Integration** ([thehyve_values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/thehyve_values.yaml:0:0-0:0))
   - **Chart**: `charts/integrations/thehyve`
   - **Namespace**: `thehyve`
   - **Target Revision**: `eoe-latest-release` git tag

3. **Hutch/Bunny Relay** ([hutch_values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/hutch_values.yaml:0:0-0:0))
   - **Chart**: `charts/hutch`
   - **Namespace**: `hutch`
   - **Target Revision**: `eoe-latest-release` git tag

## **3. Values.yaml File Referencing**

**Main FFNode Configuration ([values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/values.yaml:0:0-0:0)):**

- **Deployment Key**: [hie-prod-34](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34:0:0-0:0)
- **Namespace**: [hie-prod-34](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34:0:0-0:0)
- **Host**: `app.eoe-sde-codisc.privatelink.fitfile.net`
- **Git Tracking**: `eoe-latest-release` tag
- **FIT Connect Code**: "EOE SDE CODISC"

**Key Configuration Elements:**

```yaml
namespace: hie-prod-34
deploymentKey: hie-prod-34
argocdApp:
  targetRevision: "eoe-latest-release"
global:
  fitConnectCode: "EOE SDE CODISC"
```

## **4. Helm Chart Integration**

**Base Chart**: The main application uses the [charts/ffnode](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode:0:0-0:0) Helm chart, which is an umbrella chart that deploys multiple FITFILE components as ArgoCD Applications:

- **Core Services**: ffcloud-service, fitconnect-ftc, frontend
- **Data Stores**: MongoDB, PostgreSQL, MinIO
- **Infrastructure**: ArgoCD Workflows, Vault, Certificates
- **Monitoring**: Grafana, Prometheus
- **Security**: Cert-Manager, SpiceDB, Mutating Proxy Webhook

## **5. ArgoCD Application Templates**

Each component is deployed via ArgoCD Application templates in `charts/ffnode/templates/`:

- [ffcloud-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/ffcloud-application.yaml:0:0-0:0)
- [fitconnect-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/fitconnect-application.yaml:0:0-0:0)
- [frontend-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/frontend-application.yaml:0:0-0:0)
- [mongodb-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/mongodb-application.yaml:0:0-0:0)
- [postgresql-application.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/templates/postgresql-application.yaml:0:0-0:0)
- etc.

## **6. Terraform Configuration**

**Infrastructure Deployment**: The ArgoCD Applications are configured via Terraform in the jumpbox configuration, referencing the values files:

```hcl
# From private_platform_template/main.tf
source = {
  release_name = "thehyve"
  type         = "helm"
  value_files  = ["/ffnodes/eoe/hie-prod-34/thehyve_values.yaml"]
}

source = {
  release_name = "hutch"
  type         = "helm"
  value_files  = ["/ffnodes/eoe/hie-prod-34/hutch_values.yaml"]
}
```

## **7. Vault Integration**

All three applications use HashiCorp Vault for secrets management:

- **Vault Namespace**: `admin/deployments/hie-prod-34`
- **Secrets Mount**: `secrets`
- **Authentication**: Kubernetes service account based

## **8. Service Interconnection**

**Internal Service URLs** (configured in [values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/values.yaml:0:0-0:0)):

```yaml
fitConnectHosts:
  - fitConnectCode: "EOE SDE CODISC"
    fitConnectUri: http://hie-prod-34-fitconnect-ftc/fitconnect
    coordinatorUri: http://hie-prod-34-ffcloud-service/ffcloud
```

## **9. Deployment Workflow**

1. **Git Tag Management**: All applications track the `eoe-latest-release` git tag
2. **Values Override**: Each application uses its specific values file for configuration
3. **ArgoCD Sync**: ArgoCD automatically syncs when the git tag is moved
4. **Namespace Isolation**: Each component deploys to its designated namespace

This architecture provides a modular, GitOps-driven deployment where the main FITFILE node, TheHyve integration, and Hutch relay service are managed as separate but coordinated ArgoCD applications, all sharing the same git revision tracking for synchronized deployments.
