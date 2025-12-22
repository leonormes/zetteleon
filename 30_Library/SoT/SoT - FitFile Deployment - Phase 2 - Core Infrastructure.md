---
alias: [FitFile Deployment Phase 2]
aliases: []
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T14:57:22Z
purpose: To provide a detailed guide for Phase 2 of the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, infrastructure, phase2]
title: SoT - FitFile Deployment - Phase 2 - Core Infrastructure
type: SoT
uid: 
updated: 
version: 1.0
---

## Phase 2: Core Infrastructure (The Bedrock)

**Goal:** Provision the physical cloud resources (VPC, EKS/AKS, Jumpbox) using Terraform.

- **Detailed Guide:** [[Phase 2 Infrastructure Deployment]] (Covers AWS & Azure)
- **Context:**
    - [[Terraform Cluster Setup Guide]] (Legacy/Specific Azure nuances)
    - [[Data Architecture Analysis of Terraform AWS]]
    - [[Create a Central Version Catalog Module]]
- **Key Actions:**
    1. **EKS Cluster Configuration:**
        - **Configuration File**: `main.tf` (EKS Module)
        - **Cluster version**: Defined in `local.eks.kubernetes_version`
        - **Node groups**: Configured in `local.eks.node_groups`
        - **Private subnet access**: Defined in `eks_private_subnet_access_cidr_blocks`
        - **IAM Access**: Configured in `iam_user_access_config`
    2. **VPC and Networking:**
        - **Configuration Files**: `main.tf` (VPC Module), `./modules/vpc/*`
        - **VPC CIDR**: Defined in `local.vpc_cidr`
        - **Subnets**: Configured in `local.network.subnets`
        - **Route Tables**: Managed in the `gateway` module
    3. **Networking:** Provision VPC/VNET, Subnets, Route tables, Security groups.
    4. **Connectivity:** Provision VPC Endpoints/Private Links.
    5. **Access:** Provision Jumpbox/Bastion Host.
    6. **Workspace:** Create a new TFC workspace linked to the customer repo. Update the `versions/provider` block in the deployment code. See [[TFC Service Principle for Azure]].
    7. **Code:** Create `main.tf` consuming `terraform-helm-fitfile-platform` (or specific EKS/AKS modules). In the deployment repo, create `<deploymentKey>/locals.tf`. See [[terraform helm fitfile platform]].
    8. **Deploy:** Run `terraform apply` to create the VPC, Cluster, and Jumpbox.
    9. **Generate AppRoles:** From the `central-services/vault` directory, generate the `approles` secret for the TFC workspace. This is a sensitive HCL variable.

        ```sh
        terraform output -json | jq --arg prefix "<replace-with-deployment-key>" '
          .deployments_approle_roles.value as $roles |
          .deployments_approle_secret_ids.value |
          to_entries |
          map(select(.key | startswith($prefix)) |
            if .key == $prefix then
              {key: "argocd", value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}}
            else
              {key: (.key | gsub("^" + $prefix + "\\.";"")), value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}}
            end
          ) |
          from_entries
        '
        ```

- **Verification:**
    - [ ] `terraform output` returns Cluster Endpoint and Jumpbox Password.
    - [ ] Successful RDP/SSH connection to Jumpbox.
    - [ ] `kubectl get nodes` from Jumpbox returns healthy worker nodes.
    - [ ] Validate network connectivity
    - [ ] Test VPC endpoint access
