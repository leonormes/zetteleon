---
aliases: []
confidence:
created: 2025-08-22T09:57:05Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:19Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/cloud-networking]
title: Nginx Ingress Controller Configuration
type:
uid:
updated:
version:
---

The nginx ingress controller is **not directly configured within the helm chart deployment repository**. Instead, it's deployed and managed by the **private_platform_template** infrastructure. Here's where it's configured:

## **Ingress Controller Deployment**

**Location**: [/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/ingress_nginx/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/private_platform_template/.terraform/modules/platform/ingress_nginx/main.tf:0:0-0:0)

The nginx ingress controller is deployed via Terraform as part of the platform infrastructure:

```hcl
resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  namespace  = "ingress-nginx"
  chart      = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx"

  set {
    name = "imagePullSecrets[0].name"
    value = "fitfile-image-pull-secret"
  }
}
```

## **How Applications Use Nginx**

In the helm chart deployment, applications reference nginx through:

### **1. IngressClassName**

```yaml
spec:
  ingressClassName: nginx # References the deployed nginx controller
```

### **2. Annotations**

```yaml
annotations:
  kubernetes.io/ingress.class: nginx
  nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  nginx.ingress.kubernetes.io/ssl-passthrough: "true"
```

### **3. Key Usage Examples**

- **ArgoCD**: [charts/argo/cd/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/argo/cd/values.yaml:0:0-0:0) - Uses `ingressClassName: nginx`
- **FitConnect**: [charts/fitconnect/templates/fitconnect-ingress.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/fitconnect/templates/fitconnect-ingress.yaml:0:0-0:0) - Uses annotation approach
- **Frontend**: [charts/frontend/templates/ingress.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/frontend/templates/ingress.yaml:0:0-0:0) - Multiple nginx-specific annotations
- **SpiceDB**: [charts/spicedb/templates/ingress.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/spicedb/templates/ingress.yaml:0:0-0:0) - GRPC backend protocol

## **Configuration Flow**

1. **Infrastructure Layer**: private_platform_template deploys nginx ingress controller
2. **Application Layer**: helm charts reference the deployed controller via `ingressClassName: nginx` or annotations
3. **Certificate Integration**: Uses the PKI certificates we just configured for TLS termination

The nginx controller itself is managed as infrastructure, while the helm charts define how applications should route traffic through it.
