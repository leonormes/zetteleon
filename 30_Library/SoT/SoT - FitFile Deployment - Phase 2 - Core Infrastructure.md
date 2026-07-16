---
alias: [AWS/Azure Infrastructure SOP, Phase 2 Infrastructure Guide, Terraform Deployment Guide]
created: 2025-02-07T12:57:53+00:00
modified: 2026-07-13T08:52:47+00:00
permalink: llmeon/30-library/so-t/so-t-fit-file-deployment-phase-2-core-infrastructure
tags: [aws, azure, ff_deploy, sot, terraform]
title: SoT - FitFile Deployment - Phase 2 - Core Infrastructure
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Overview

This guide details Phase 2: Core Infrastructure of the FitFile platform deployment. It focuses on the Terraform-driven provisioning of the foundational cloud resources (Network, Compute, Identity) required before the Platform Layer (ArgoCD) can be installed.

Objective: Transform an empty cloud subscription/account into a "Ready-for-K8s" state.

> [!important] Context
> This is a sub-guide of the master [[SoT - FitFile Deployment - Implementation Manual]]. Ensure you have completed Phase 0: Pre-Flight and Phase 1: Network Provisioning before proceeding.

---

## 2. Prerequisites

### 2.1 Software Toolkit

Ensure your workstation has the approved toolchain:

```bash
# Core Tools
brew install terraform  # Must be >= 1.9.0
brew install git

# Cloud CLIs (Install as needed)
brew install aws-cli    # AWS
brew install azure-cli  # Azure
```

### 2.2 Access Requirements

| Provider | Requirement |
|:---|:---|
| AWS | `AdministratorAccess` (or strict `terraform-policy` role). Access Key/Secret. |
| Azure | `Contributor` role on Subscription. `User Access Administrator` for RBAC assignments. |

---

## 3. Terraform Cloud (TFC) Configuration

Infrastructure state is managed remotely via Terraform Cloud.

1. Create Project:
   - Naming convention: `<customer-name>-infrastructure`
2. Create Workspace:
   - Type: `Version Control Workflow`
   - Name: `<deployment-key>` (e.g., `lca-prd-01`)
   - Repository: Link to the customer's GitLab infrastructure repo.
3. Configure Variables (TFC UI):

   AWS Variables:

   ```bash
   AWS_REGION = "eu-west-2"
   AWS_ACCESS_KEY_ID = "..."      # Sensitive
   AWS_SECRET_ACCESS_KEY = "..."  # Sensitive
   ```

   Azure Variables:

   ```bash
   ARM_CLIENT_ID = "..."
   ARM_CLIENT_SECRET = "..."
   ARM_SUBSCRIPTION_ID = "..."
   ARM_TENANT_ID = "..."
   ```

---

## 4. Repository Initialization

Structure your customer infrastructure repository (`customers/<deployment-key>`) as follows:

```bash
.
├── main.tf       # Module invocation
├── variables.tf  # Input definitions
├── outputs.tf    # Critical data exports
├── versions.tf   # Provider locking
└── providers.tf  # Provider configuration
```

### 4.1 Standard Configuration (AWS Example)

`main.tf`:

```hcl
module "eks_cluster" {
  source = "app.terraform.io/FITFILE-Platforms/eks-private/aws"
  version = "1.0.0"

  deployment_key = var.deployment_key
  environment    = var.environment
  vpc_cidr       = "10.0.0.0/16"

  # Security Hardening
  enable_private_endpoints = true
  enable_private_nodes     = true
}
```

`outputs.tf`:

```hcl
output "cluster_endpoint" {
  value = module.eks_cluster.cluster_endpoint
  sensitive = true
}

output "generated_password" {
  description = "Jumpbox local admin password"
  value = module.eks_cluster.generated_password
  sensitive = true
}
```

---

## 5. Deployment Execution

Execute the standard Terraform lifecycle:

1. Init: `terraform init -upgrade`
2. Validate: `terraform validate`
3. Plan: `terraform plan` (Review strict resource creation)
4. Apply: `terraform apply`

> [!check] Success Criteria
> - Terraform completes with "Apply complete".
> - State file is locked in TFC.
> - Outputs (Cluster Endpoint, Passwords) are visible.

---

## 6. Jumpbox Access & Validation

Direct access to the cluster API is blocked from the public internet. You must tunnel through the Jumpbox.

### 6.1 AWS SSM Tunneling

1. Retrieve Instance ID:

   ```bash
   aws ec2 describe-instances \
     --filters "Name=tag:Name,Values=FITFILEJumpbox" \
     --query 'Reservations[].Instances[].[InstanceId]' --output text
   ```

2. Start Port Forwarding:

   ```bash
   aws ssm start-session \
     --target <instance-id> \
     --document-name AWS-StartPortForwardingSession \
     --parameters "localPortNumber=55679,portNumber=3389"
   ```

3. Connect via RDP:
   - Host: `localhost:55679`
   - User: `awsadmin`
   - Pass: (From Terraform Output `generated_password`)

### 6.2 Cluster Verification (From Jumpbox)

Once inside the Jumpbox, verify the Kubernetes control plane:

```bash
# Update Kubeconfig
aws eks update-kubeconfig --region <region> --name <cluster-name>

# Check Node Health
kubectl get nodes

# Check System Pods
kubectl get pods -n kube-system
```

---

## 7. Troubleshooting

| Issue | Resolution |
|:---|:---|
| Terraform Init Fails | Delete `.terraform` folder and retry. Check TFC token validity. |
| AWS Auth Failure | Run `aws sts get-caller-identity` to verify local credentials match TFC variables. |
| SSM Connection Refused | Ensure the Jumpbox Security Group allows outbound 443 to SSM endpoints. |
| RDP Timeout | Verify `localPortNumber` matches your RDP client config. |

---

## 8. Next Steps

Proceed to Phase 3: Platform Deployment in the [[SoT - FitFile Deployment - Implementation Manual]].
