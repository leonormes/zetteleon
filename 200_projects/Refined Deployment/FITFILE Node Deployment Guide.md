---
aliases: []
confidence: 
created: 2025-09-07T08:50:31Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Node Deployment Guide
type:
uid: 
updated: 
version:
---

## Overview

This guide documents the comprehensive deployment process for FITFILE nodes, covering infrastructure provisioning, cluster configuration, and application deployment using ArgoCD. The FITFILE platform uses a three-tier deployment architecture:

1. **Infrastructure Layer**: Azure Kubernetes Service (AKS) clusters with private networking
2. **Platform Layer**: ArgoCD for GitOps-based application management
3. **Application Layer**: FITFILE components deployed as Helm charts

## Architecture Components

### 1. Infrastructure Module (`terraform-azure-private-infrastructure`)

The foundational Terraform module that provisions Azure infrastructure for FITFILE deployments.

**Key Features:**

- Private AKS clusters with Azure CNI in overlay mode
- Dual node pools (system and workflows)
- Network security with Calico policies
- Forced tunneling through Azure Firewall
- Jumpbox for secure cluster access
- Pod CIDR isolation (`10.244.0.0/16`)

**Module Structure:**

```sh
terraform-azure-private-infrastructure/
├── main.tf              # AKS cluster configuration
├── vars.tf              # Variable definitions
├── networking.tf        # VNet and subnet configuration
├── modules/
│   ├── aks/            # AKS-specific resources
│   ├── bastion_host/   # Jumpbox configuration
│   ├── network_security_group/
│   └── node_pool/      # Additional node pool management
```

**Key Configuration Parameters:**

- `deployment_key`: Unique identifier for the FITFILE client (5-10 chars, alphanumeric)
- `network_plugin_mode`: "overlay" for efficient pod networking
- `pod_cidr`: "10.244.0.0/16" for pod IP allocation
- `network_policy`: "calico" for network security
- `kubernetes_version`: Target Kubernetes version

### 2. Cluster Configuration (Example: CUH-DP)

Each FITFILE deployment has a dedicated cluster configuration that uses the infrastructure module.

**Directory Structure:**

```sh
Clusters/eoe/Production/CUH-DP/
├── main.tf              # Module instantiation
├── locals.tf            # Local values and calculations
├── variables.tf         # Deployment-specific variables
├── dns.tf              # DNS configuration
└── providers.tf        # Terraform providers
```

**Key Configuration Elements:**

#### Network Configuration

```hcl
# Network Configuration for Forced Tunneling
network_policy      = "calico"        # Network security
network_plugin_mode = "overlay"       # CNI overlay mode
pod_cidr            = "10.244.0.0/16" # Pod IP range

# VNet addressing (calculated in locals.tf)
vnet_address_space = "10.250.16.0/24"
```

#### Subnet Allocation

```hcl
# Efficient subnet allocation with overlay networking
default_node_pool_subnet_address_prefix    = [cidrsubnet(local.vnet_address_space, 4, 0)] # /28
additional_node_pool_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 4, 1)] # /28
vm_subnet_address_prefix                   = [cidrsubnet(local.vnet_address_space, 5, 4)] # /29
```

#### HTTP Proxy Configuration

Comprehensive proxy settings for corporate environments:

```hcl
http_proxy_config = {
  http_proxy  = "http://10.252.142.180:8080/"
  https_proxy = "http://10.252.142.180:8080/"
  no_proxy = [
    "localhost", "127.0.0.1",
    # Internal service discovery
    ".svc", ".svc.cluster.local",
    # FITFILE services
    "cuh-prod-1-ffcloud-service",
    "cuh-prod-1-postgresql",
    # ArgoCD services
    "argocd-repo-server", "argocd-server",
    # Network ranges
    "10.2.0.0/24", "10.244.0.0/16", "10.250.16.0/28"
  ]
}
```

### 3. FITFILE Node Helm Chart (`ffnode`)

The main application chart that orchestrates all FITFILE components using ArgoCD Applications.

**Chart Structure:**

```sh
charts/ffnode/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration
└── templates/           # ArgoCD Application templates
    ├── ffcloud-application.yaml
    ├── fitconnect-application.yaml
    ├── frontend-application.yaml
    ├── postgresql-application.yaml
    ├── mongodb-application.yaml
    ├── minio-application.yaml
    ├── cert-manager-application.yaml
    └── [other components...]
```

**Core Configuration:**

```yaml
# Deployment toggles
deploy:
  spicedb: true
  certManager: true
  persistence: true
  messageBroker: true
  monitoring: true
  coordinatingStation: true
  fitconnect: true
  frontend: true
  workflowsApi: true

# ArgoCD configuration
argocdApp:
  targetRevision: master
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - Validate=false
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
```

### 4. ArgoCD Integration

ArgoCD manages the deployment of FITFILE components through a GitOps workflow.

**Platform Integration:**

- Deployed via `terraform-helm-fitfile-platform` module
- Configured with private ACR image pull secrets
- Ingress enabled with TLS termination
- Metrics and monitoring enabled

**Application Management:**
Each FITFILE component is deployed as a separate ArgoCD Application, allowing for:

- Independent versioning and rollbacks
- Granular sync policies
- Component-specific configuration overrides

## Deployment Workflow

### Phase 1: Infrastructure Provisioning

1. **Configure Deployment Parameters**

   ```hcl
   # In locals.tf
   deployment_key = "cuh-poc-1"
   vnet_address_space = "10.250.16.0/24"
   firewall_private_ip = "10.250.1.68"
   ```

2. **Deploy Infrastructure**

   ```bash
   cd Clusters/eoe/Production/CUH-DP
   terraform init
   terraform plan
   terraform apply
   ```

3. **Verify Cluster Access**

   ```bash
   az aks get-credentials --resource-group rg-ff-uks-gp-cuh-poc-1 --name aks-ff-uks-gp-cuh-poc-1
   kubectl get nodes
   ```

### Phase 2: Platform Setup

1. **ArgoCD Installation**
   - Automatically deployed via the platform module
   - Configured with ingress and TLS certificates
   - Image pull secrets configured for private ACR

2. **Namespace Preparation**

   ```bash
   kubectl create namespace cuh-prod-1
   kubectl create secret docker-registry fitfile-image-pull-secret \
     --docker-server=fitfileregistry.azurecr.io \
     --docker-username=$ACR_USERNAME \
     --docker-password=$ACR_PASSWORD \
     --namespace=cuh-prod-1
   ```

### Phase 3: Application Deployment

1. **Configure FFNode Values**

   ```yaml
   # ffnodes/eoe/cuh-prod-1/values.yaml
   namespace: "cuh-prod-1"
   deploymentKey: "cuh-prod-1"

   argocdApp:
     targetRevision: cuh-prod-1-latest-release
   ```

2. **Deploy FFNode Chart**

   ```bash
   helm install cuh-prod-1 charts/ffnode \
     -f ffnodes/eoe/cuh-prod-1/values.yaml \
     --namespace argocd
   ```

3. **Monitor Deployment**

   ```bash
   # Check ArgoCD applications
   kubectl get applications -n argocd

   # Check application pods
   kubectl get pods -n cuh-prod-1
   ```

## Deployment Patterns

### Multi-Tenant Architecture

FITFILE supports multiple deployment patterns:

1. **Single Tenant per Cluster** (Recommended)
   - Each client gets dedicated AKS cluster
   - Complete isolation and security
   - Independent scaling and maintenance

2. **Multi-Tenant per Cluster**
   - Multiple deployments in same cluster
   - Namespace-based isolation
   - Shared infrastructure costs

### Environment Management

**Production Deployments:**

```sh
ffnodes/
├── eoe/
│   ├── cuh-prod-1/     # Cambridge University Hospitals
│   └── hie-prod-34/    # Health Information Exchange
├── kch/
│   └── prod/           # King's College Hospital
└── barts/
    └── prod/           # Barts Health NHS Trust
```

**Development/Testing:**

```sh
ffnodes/fitfile/
├── development/        # Development environment
├── ff-test-a/         # Test environment A
├── ff-test-b/         # Test environment B
└── acr-test/          # ACR testing
```

## Security Considerations

### Network Security

- Private AKS clusters with no public endpoints
- Network policies enforced via Calico
- Forced tunneling through Azure Firewall
- Pod-to-pod communication restricted

### Identity and Access

- Azure RBAC integration
- Workload identity for pod-to-Azure authentication
- Service mesh for inter-service communication
- Certificate management via cert-manager

### Image Security

- Private Azure Container Registry (ACR)
- Image vulnerability scanning with Trivy
- Automated patching with Copa
- Image pull secrets for authentication

## Monitoring and Observability

### Built-in Monitoring

- Prometheus metrics collection
- Grafana dashboards
- ArgoCD application health monitoring
- Azure Monitor integration

### Logging

- Centralized logging via Azure Log Analytics
- Application logs forwarded to monitoring stack
- Audit logging for compliance

## Troubleshooting

### Common Issues

1. **Pod Scheduling Issues**

   ```bash
   # Check node resources
   kubectl describe nodes

   # Check pod events
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. **Network Connectivity**

   ```bash
   # Test DNS resolution
   kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

   # Check network policies
   kubectl get networkpolicies -A
   ```

3. **ArgoCD Sync Issues**

   ```bash
   # Check application status
   kubectl get applications -n argocd

   # View sync details
   argocd app get <app-name>
   ```

### Maintenance Tasks

1. **Cluster Updates**
   - Update Kubernetes version in Terraform configuration
   - Apply infrastructure changes
   - Monitor application health post-update

2. **Application Updates**
   - Update image tags in values files
   - Commit changes to trigger ArgoCD sync
   - Monitor deployment progress

3. **Certificate Renewal**
   - Managed automatically by cert-manager
   - Monitor certificate expiration dates
   - Verify renewal process

## Best Practices

### Infrastructure

- Use overlay networking for efficient IP utilization
- Implement proper subnet sizing for future growth
- Configure appropriate node pool sizing and auto-scaling
- Enable host encryption for compliance requirements

### Application Deployment

- Use semantic versioning for application releases
- Implement proper health checks and readiness probes
- Configure resource requests and limits
- Use horizontal pod autoscaling where appropriate

### GitOps

- Maintain separate branches for different environments
- Use pull requests for deployment approvals
- Implement proper secret management
- Monitor drift detection and auto-remediation

## Support and Documentation

### Key Resources

- Infrastructure module documentation: `terraform-azure-private-infrastructure/README.md`
- Helm chart documentation: `charts/ffnode/README.md`
- ArgoCD configuration: `TFC-Modules/terraform-helm-fitfile-platform/argocd/`
- Deployment examples: `ffnodes/` directory structure

### Contact Information

- Infrastructure issues: Platform Engineering Team
- Application issues: FITFILE Development Team
- Security concerns: Security Team

---

*This documentation is maintained as part of the FITFILE deployment repository. Please keep it updated as the architecture evolves.*
