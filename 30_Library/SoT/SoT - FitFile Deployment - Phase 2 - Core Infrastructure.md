---
aliases: ["Cloud Bedrock Guide", "Core Infrastructure Setup", "FitFile Deployment Phase 2"]
confidence: "5/5"
created: 2025-12-21T10:51:07Z
epistemic: "process"
last_reviewed: "2025-12-23"
modified: 2025-12-28T09:56:11+00:00
purpose: "To provide a detailed guide for Phase 2 of the FitFile deployment process: provisioning the cloud bedrock."
review_interval: "3 months"
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - Data-Centric Infrastructure (Terraform)]]", "[[SoT - FITFILE Platform Deployment]]", "[[SoT - FitFile Deployment - Azure Organization Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["aws", "azure", "ff_deploy", "infrastructure", "phase2", "terraform"]
title: SoT - FitFile Deployment - Phase 2 - Core Infrastructure
type: "SoT"
uid: 
updated: 
---

## 1. Goal: Provisioning the Bedrock

Phase 2 involves the physical creation of the private cloud network and the Kubernetes cluster (EKS or AKS) using Terraform. This stage transforms the **Control Plane** (Phase 1) into a functional **Compute Environment**.

---

## 2. Infrastructure Architecture

The FitFile infrastructure follows a modular, data-centric design where the logical model is decoupled from the physical implementation.

### 2.1 Core Components

1. **VPC / VNet Module:** Custom virtual network with declarative subnet mapping.
2. **Cluster (EKS/AKS):** Managed Kubernetes service with dedicated node groups for system and workloads.
3. **Jumpbox:** Bastion host for secure administrative access.
4. **Gateway & Routing:** NAT Gateways and Private Links for secure internet and inter-service connectivity.
5. **VPC Endpoints:** Private connectivity to cloud-native services (S3, Vault, etc.).

### 2.2 Security Invariants

- **Zero Public Access:** All cluster endpoints and Jumpboxes are private by default.
- **IMDSv2 Enforcement:** Required on all EC2 instances to mitigate SSRF risks.
- **Volume Encryption:** Mandatory encryption for all EBS/Disk volumes (e.g., gp3).
- **Network Policies:** L3/L4 isolation enforced via Calico.

---

## 3. Infrastructure Code Setup

### A. Repository Preparation

Each customer deployment has a dedicated private GitLab repository created from a standardized template (e.g., `terraform-aws-eks-private` or `terraform-azure-aks-private`).

```bash
# Example local setup
cd customers
mkdir <deployment-key> && cd <deployment-key>
touch main.tf variables.tf outputs.tf versions.tf providers.tf
```

### B. Cloud-Specific Components

| Provider | Core Resources | Security / Identity |
|:--- |:--- |:--- |
| **AWS** | EKS Cluster, VPC, NAT Gateway | IAM Roles, SSM Session Manager |
| **Azure** | AKS Cluster, VNet, NAT Gateway | Managed Identities, Resource Providers |

### C. Azure Prerequisite: Service Principal Configuration

For Azure deployments, Terraform Cloud requires a Service Principal (non-human identity) with specific credentials and role assignments.

#### 1. Creation & Credentials

Create an App Registration in Microsoft Entra ID. The following credentials must be set as **Terraform Cloud Environment Variables**:

| Variable | Source | Sensitive? |
|:--- |:--- |:--- |
| `ARM_CLIENT_ID` | Application (client) ID | No |
| `ARM_ACCESS_KEY` | Client Secret ID | **Yes** |
| `ARM_CLIENT_SECRET` | Client Secret Value | **Yes** |

#### 2. Role Assignments (Standard vs. Least Privilege)

The Service Principal requires permissions to create the cluster and allow the cluster to operate.

**Baseline Roles:**
- **Contributor:** On the Subscription (Broad access).
- **User Access Administrator:** On the Subscription (Required to assign roles to the AKS Managed Identity). *Condition: Constrain to assigning `Network Contributor`.*

**Refined Least Privilege (Custom Role):**
To adhere to strict security standards, replace `Contributor` with a custom role containing only these actions:

- **Compute:**
    - `Microsoft.Compute/diskEncryptionSets/read`
    - `Microsoft.Compute/proximityPlacementGroups/write`
    - `Microsoft.Compute/disks/*`
    - `Microsoft.Compute/virtualMachines/*`
    - `Microsoft.Compute/locations/vmSizes/read`
    - `Microsoft.Compute/locations/operations/read`
- **Network:**
    - `Microsoft.Network/virtualNetworks/joinLoadBalancer/action`
    - `Microsoft.Network/networkInterfaces/*`
    - `Microsoft.Network/virtualNetworks/*`
    - `Microsoft.Network/virtualNetworks/subnets/*`
- **Identity:**
    - `Microsoft.ManagedIdentity/userAssignedIdentities/assign/action` (Critical for assigning Identity to Nodes)
- **Cluster Management:**
    - `Microsoft.ContainerService/managedClusters/*`
- **Monitoring:**
    - `Microsoft.OperationalInsights/workspaces/*`
    - `Microsoft.OperationsManagement/solutions/*`
- **Resource Groups:**
    - `Microsoft.Resources/subscriptions/resourcegroups/*`

> **Note:** The AKS Cluster itself will use a **Managed Identity** for runtime operations (Load Balancers, Storage), distinct from the Terraform Service Principal. The Service Principal essentially bootstraps this identity.

---

## 4. Deployment Execution

1. **Workspace Setup:** Create a new TFC workspace titled `<customer>-infrastructure`. Configure cloud credentials (AWS Access Keys or Azure ARM keys) as sensitive variables.
2. **Variable Configuration:** Set the `deployment_key` and environment-specific variables (VM sizes, network routing type).
3. **Apply:** Execute `terraform apply`. This sequence creates the network first, then the cluster, then the access tools (Jumpbox).

---

## 5. Secure Access & Connectivity

### A. The Jumpbox Protocol

- **SSM-Based Access (AWS):** No SSH keys are used. Access is granted via IAM and managed through SSM Session Manager.
- **Conditional Access (Azure):** Use Serial Console or request IP exceptions for Bastion.

### B. AppRole Bootstrap

Once the cluster is live, you must generate the **AppRole JSON** from the `central-services/vault` directory and inject it into the cluster's TFC workspace. This allows the internal platform tools (ArgoCD, VSO) to authenticate with Vault.

---

## 6. Verification Checklist

- [ ] **Infrastructure HUD:** `terraform output` returns Cluster Endpoint and Jumpbox metadata.
- [ ] **Connectivity:** Jumpbox can reach `kubernetes.default.svc.cluster.local`.
- [ ] **Nodes:** `kubectl get nodes` returns healthy workers in all AZs.
- [ ] **Security:** `kubectl describe node` confirms encrypted volumes and IMDSv2 status.

---

## 7. Related Components

- [[SoT - Data-Centric Infrastructure (Terraform)]]—Detailed analysis of the Terraform data model.
- [[SoT - Cloud Networking Core Components]]—General networking principles.
- [[SoT - Container Isolation (The Namespace Security Model)]]—Low-level security primitives.
