---
aliases: [Deployment Master Guide, FitFile Deployment Playbook]
confidence: 5/5
created: 2025-12-20T00:00:00Z
epistemic: synthesis
last_reviewed: 2025-12-20
modified: 2025-12-21T10:19:09Z
purpose: A comprehensive, step-by-step Map of Content (MOC) and guide for deploying the FitFile platform, acting as the primary Source of Truth (SoT) for engineers.
review_interval: 3 months
see_also: ["[[SoT - FITFILE Deployment Process]]", "[[SoT - FITFILE Platform Components]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, guide, moc]
title: MOC - FitFile Deployment
type: MOC
uid: 
updated: 
version: 1.0
---

## MOC - FitFile Deployment Playbook

> [!abstract] Executive Summary
> This document acts as the **Master Deployment Guide** for the FitFile platform. It orchestrates the deployment process across four distinct phases, linking to specific technical guides for detailed execution.
>
> **Goal:** Transform an empty cloud account into a fully operational, compliant FitFile node.

---

### 1. Pre-Flight Checklist

Before initiating any phase, ensure the following prerequisites are met:

- [ ] **Access:** HashiCorp Cloud Platform (HCP), Auth0, GitLab, Cloud Provider (AWS/Azure).
- [ ] **Tooling:** `terraform`, `tfenv`, `aws-cli` / `az-cli`, `kubectl`, `git`.
- [ ] **Repository:** Cloned `fitfile/terraform-infrastructure` and `fitfile/customers`.

---

### 2. The Deployment Phases

#### Phase 1: Foundation & Tooling
**Goal:** Establish the central identity, secrets, and monitoring control plane. This is the "Key to the Castle."

- **Detailed Guide:** [[Phase 1 Tooling Configuration]]
- **Key Actions:**
    1. **Generate Identity:** Run `short_name.sh` to create the unique `deployment_key` (e.g., `ff-hyve-1`).
    2. **Vault Setup:** Update `central-services/hcp/vault/locals.tf` to allocate secret storage.
    3. **Auth0 Config:** Update `central-services/auth0/prod/locals.tf` to provision the tenant.
    4. **Secret Population:** Manually populate critical secrets (DB passwords, UDE keys) into Vault.
- **Verification:**
    - [ ] Vault secrets populated in `deployments/<key>`.
    - [ ] Auth0 Tenant accessible.

#### Phase 2: Core Infrastructure (The Bedrock)
**Goal:** Provision the physical cloud resources (VPC, EKS/AKS, Jumpbox) using Terraform.

- **Detailed Guide:** [[Phase 2 Infrastructure Deployment]] (Covers AWS & Azure)
- **Context:** [[terraform_cluster_setup_guide]] (Legacy/Specific Azure nuances)
- **Key Actions:**
    1. **Workspace:** Create a new TFC workspace linked to the customer repo.
    2. **Code:** Create `main.tf` consuming `terraform-helm-fitfile-platform` (or specific EKS/AKS modules).
    3. **Deploy:** Run `terraform apply` to create the VPC, Cluster, and Jumpbox.
    4. **Access:** Establish SSH/SSM access to the Jumpbox (the "Cockpit" for Phase 3).
- **Verification:**
    - [ ] `terraform output` returns Cluster Endpoint and Jumpbox Password.
    - [ ] Successful RDP/SSH connection to Jumpbox.
    - [ ] `kubectl get nodes` from Jumpbox returns healthy worker nodes.

#### Phase 3: Platform Services (The Runtime)
**Goal:** Install the "Operating System" of the cluster (ArgoCD, Vault integration, Ingress) from *within* the private network.

- **Detailed Guide:** [[FItfile deployment ArgoCD Style]] (Explains the "App of Apps" pattern)
- **Key Actions:**
    1. **Jumpbox:** All actions must be performed from the Jumpbox (Private Access).
    2. **Bootstrap:** Clone the `private_platform_template` to the Jumpbox.
    3. **Configure:** Update `vars.tfvars` with the `deployment_key` and values file path.
    4. **Apply:** Run the internal Terraform to deploy ArgoCD and the Root App.
- **Verification:**
    - [ ] ArgoCD UI accessible via Ingress.
    - [ ] Vault Operator pods running.
    - [ ] Ingress Controller has an external IP/DNS.

#### Phase 4: Application Layer (The Logic)
**Goal:** Deploy the actual FitFile services (FFNode, MongoDB, Frontend) via GitOps.

- **Detailed Guide:** [[Set Up New Deployment]] (See "Deploy the Platform" section)
- **Key Actions:**
    1. **Config:** Create the customer-specific `values.yaml` in the `ffnodes/` repository.
    2. **Sync:** In ArgoCD, sync the Root Application (`ff-<deployment_key>`).
    3. **Reconcile:** Watch as ArgoCD hydrates the child applications (MongoDB, FitConnect, etc.).
- **Verification:**
    - [ ] All ArgoCD Apps show `Synced` and `Healthy`.
    - [ ] Frontend accessible via public URL.
    - [ ] Integration tests pass (if configured).

---

### 3. Architecture & Concepts

- **"App of Apps" Pattern:** We do not deploy services manually. We deploy *one* Root Application, which points to the `ffnode` Chart. This chart acts as a manifest, spawning all other services (MongoDB, API, etc.).
    - *Reference:* [[FItfile deployment ArgoCD Style]]
- **Secret Flow:** Secrets are never in Git.
    - Path: `Vault (HCP)` -> `External Secret Operator` -> `K8s Secret` -> `Pod Mount`.
- **Private Access:** Direct access to the cluster API is blocked. All `kubectl` commands must tunnel through the Jumpbox or SSM.

---

### 4. Troubleshooting & FAQ

- **"ArgoCD Sync Failed":** Check `VaultAuth` status. Often caused by missing Vault secrets in Phase 1.
- **"Image Pull Error":** Check ACR/ECR credentials in the `imagePullSecrets`.
- **"Terraform State Lock":** Check TFC console for hanging runs.

---

### 5. Deployment Log (Reference)

For a raw, real-world example of a deployment log including error messages and "gotchas", see:

- [[Set Up New Deployment]]
