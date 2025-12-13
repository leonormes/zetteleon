---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
ID: FFAPP-3277
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy, networking]
title: aws_firewall_rules
type: config
uid: 
updated: 
version: 1
---

## AWS Firewall Rules

```sh
fd firewall
Terraform Infrastructure/TFC-Modules/terraform-azure-firewall/
Terraform Infrastructure/terraform-azure-firewall/
```

- We use our own custom terraform modules
- We use root terraform repos to use the modules and supply the variables per deployment

FITFILE/Terraform Infrastructure/Deploy/Production/private_platform_template/main.tf

This is the repo we download to the jumpbox and run.

What I am looking for is the azure deployment firewall settings

`FITFILE/Terraform Infrastructure/TFC-Modules/terraform-azure-private-infrastructure`

I'll help analyze the firewall rules from your Azure configuration and categorize them for AWS migration. First, let me read the firewall configuration.

Read file: main.tf

I'll categorize the URLs from your firewall rules into Azure-specific and non-Azure-specific groups, and explain their purposes:

### Azure-Specific URLs

1. Azure Core Services:
- `management.azure.com` - Required for Kubernetes operations against Azure API
- `login.microsoftonline.com` - Microsoft Entra (Azure AD) authentication
- `.monitoring.azure.com` - Azure Monitor metrics data
- `uksouth.ingest.monitor.azure.com` - Azure Monitor Prometheus metrics ingestion
- `uksouth.handler.control.monitor.azure.com` - Cluster data collection rules
- `.ods.opinsights.azure.com`, `.opinsights.azure.com`, `.oms.opinsights.azure.com` - Azure Monitor and Log Analytics
- `dc.services.visualstudio.com` - Azure Monitor Container Agent Telemetry

2. Azure Container Services:
- `mcr.microsoft.com`, `.data.mcr.microsoft.com` - Microsoft Container Registry
- `fitfileregistry.azurecr.io`, `fitfilepublic.azurecr.io` - Your Azure Container Registry
- `acs-mirror.azureedge.net` - Azure CNI and kubenet binaries
- `.azureedge.net` - Azure CDN

3. Azure Storage and Policy:
- `uksmanaged208.blob.core.windows.net` - Azure Blob Storage
- `azurecliprod.blob.core.windows.net` - Azure CLI installation
- `data.policy.core.windows.net` - Kubernetes policies
- `store.policy.core.windows.net` - Gatekeeper policy artifacts

### Non-Azure-Specific URLs

1. HashiCorp Services:
- `releases.hashicorp.com` - HashiCorp releases
- `registry.terraform.io`, `app.terraform.io`, `archivist.terraform.io` - Terraform registry and services
- `vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud` - HashiCorp Vault

2. Ubuntu/OS Updates:
- `azure.archive.ubuntu.com`, `.canonical.com` - Ubuntu package repositories
- `security.ubuntu.com`, `changelogs.ubuntu.com` - Ubuntu security updates
- `ntp.ubuntu.com` - Time synchronization
- `download.opensuse.org` - OpenSUSE packages

3. FITFILE Services:
- `fitfile-prod.eu.auth0.com`, `fitfile-test.eu.auth0.com` - Auth0 authentication
- `cdn.auth0.com` - Auth0 UI components
- `fitfile.com` - FITFILE main domain

4. Monitoring and Logging:
- `logs-prod-008.grafana.net` - Grafana logging
- `tempo-prod-06-prod-gb-south-0.grafana.net` - Grafana Tempo (tracing)

5. Source Control and Package Management:
- `gitlab.com` - Source code repository
- `packages.microsoft.com` - Microsoft package repository

When migrating to AWS, you'll need to:

1. Replace Azure-specific endpoints with AWS equivalents (e.g., ECR instead of ACR)
2. Keep the non-Azure specific endpoints as they are
3. Update monitoring and logging endpoints based on your AWS monitoring strategy
4. Consider using AWS-specific services like

### 1. Container Registry Access

Azure URLs:

- `mcr.microsoft.com`, `.data.mcr.microsoft.com`
- `fitfileregistry.azurecr.io`, `fitfilepublic.azurecr.io`

AWS Equivalents:

- `.dkr.ecr.[region].amazonaws.com` - AWS Elastic Container Registry (ECR)
- `.ecr.[region].amazonaws.com` - AWS ECR API endpoints

### 5. Policy & Security

Azure URLs:

- `data.policy.core.windows.net`
- `store.policy.core.windows.net`

AWS Equivalents:

- `ssm.[region].amazonaws.com` - AWS Systems Manager
- `secretsmanager.[region].amazonaws.com` - AWS Secrets Manager
- `kms.[region].amazonaws.com` - AWS KMS for encryption

### Additional EKS-specific Requirements

For a private EKS cluster, you'll also need to allow these AWS-specific endpoints:

1. `ec2.[region].amazonaws.com` - EC2 API access
2. `autoscaling.[region].amazonaws.com` - For cluster autoscaler
3. `.eks.[region].amazonaws.com` - EKS service endpoints
4. `.eks-endpoints.[region].amazonaws.com` - EKS private endpoint access

### Important Notes for AWS Implementation

1. VPC Endpoints: Unlike Azure, in AWS you should set up VPC endpoints for private communication with AWS services. Common endpoints needed for EKS:
   - Gateway endpoints for S3 and DynamoDB
   - Interface endpoints for ECR, EKS, CloudWatch, etc.

2. Security Groups: Instead of firewall rules, you'll primarily use:
   - Security Groups for pod-to-pod and pod-to-service communication
   - Network ACLs for subnet-level control

3. DNS Resolution: You'll need to enable:
   - DNS hostnames
   - DNS resolution in your VPC
   - Private DNS for interface endpoints

4. Region Specificity: Replace `[region]` in the URLs with your specific AWS region (e.g., `us-east-1`, `eu-west-1`)

We need to maintain access to

### Required

- `fitfileregistry.azurecr.io` - Your primary ACR
- `fitfilepublic.azurecr.io` - Your public ACR
- `.data.mcr.microsoft.com` - Microsoft Container Registry CDN (if you're using any Microsoft base images)
- `mcr.microsoft.com` - Microsoft Container Registry

### Authentication Endpoints Needed for ACR

- `login.microsoftonline.com` - Required for Azure AD authentication to ACR

### Important Implementation Considerations

1. Network Connectivity:
   - Ensure your EKS cluster has outbound internet access to reach ACR (through NAT Gateway or Internet Gateway)
   - Consider using AWS PrivateLink or VPC peering if you want private connectivity to Azure

2. Authentication Options:
   - Create an Azure Service Principal with AcrPull rights
   - Store the credentials securely in AWS Secrets Manager
   - Use

#### Advantages of Using AWS ECR

1. Performance:
   - Reduced latency as images are pulled from the same cloud provider/region
   - Faster container startup times
   - Lower egress costs (no cross-cloud data transfer)

2. Reliability:
   - No dependency on cross-cloud connectivity
   - Reduced points of failure
   - Better availability guarantees within AWS network

3. Cost Efficiency:
   - Lower data transfer costs (free within same AWS region)
   - No Azure egress charges for container pulls
   - Potentially lower operational costs

4. Security:
   - Simplified IAM permissions using AWS native roles
   - No need to manage Azure credentials in AWS
   - Reduced attack surface (no cross-cloud authentication)
