---
aliases: ["Azure Org Architecture", "FITFILE Deployment Architecture", "FITFILE Platform Overview", "Terraform Design Principles"]
confidence: "5/5"
created: 2025-12-14T18:04:39Z
epistemic: "theory"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:43+00:00
purpose: "The canonical architectural reference for the FITFILE Platform deployment, covering the cloud hierarchy, security model, and GitOps design."
review_interval: "6 months"
see_also: ["[[SoT - FitFile Deployment - Implementation Manual]]", "[[SoT - FitFile Deployment - Networking & DNS]]", "[[SoT - FITFILE Secret Management Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["azure", "deployment", "fitfile", "gitops", "kubernetes", "SoftwareEngineering/Architecture"]
title: SoT - FitFile Deployment - Strategy & Architecture
type: "SoT"
uid: 
updated: 
---

## 1. Executive Summary

The FITFILE platform utilizes a **Three-Tier Deployment Architecture** optimized for security, scalability, and high-velocity updates via GitOps.

- **Infrastructure Layer:** Private cloud bedrock (EKS/AKS) managed via Terraform.
- **Platform Layer:** The "Cluster OS" (ArgoCD, Vault Secrets Operator, Ingress).
- **Application Layer:** FITFILE microservices deployed as a unified unit (FFNode).

**The Deployment Key:** A unique identifier (e.g., `WM-Prod`) serves as the primary namespace and prefix for all resources, from Vault paths to Azure Management Groups.

---

## 2. Cloud Hierarchy (Azure Landing Zone)

FITFILE follows the **Enterprise-Scale Landing Zone** pattern, separating platform governance from customer workloads.

### 2.1 Management Group Structure

- **FITFILE Root Group:** Top-level governance.
- **Platform Subscriptions:** Shared services (DNS, Identity, Management/Monitoring).
- **Landing Zone Subscriptions:** Isolated environments for **Production** (Customer COGS) and **Non-Production** (R&D).

### 2.2 Security Invariants

- **Zero Public Access:** No public endpoints for cluster APIs or Jumpboxes.
- **Identity-Centric:** Managed Identities (Azure) or IAM Roles (AWS) for infrastructure operations.
- **Least Privilege:** Terraform Service Principals are constrained to specific Resource Groups and required Actions (Network, Compute, Identity).

---

## 3. GitOps & CI/CD Strategy

The deployment process is a hybrid **CI-Driven GitOps** workflow.

1. **CI (GitLab):** Builds Docker images, lints Helm charts, and runs integration tests.
2. **GitOps (ArgoCD):** Orchestrates the cluster state by reconciling the deployment repository with the live environment.
3. **The Umbrella Pattern:** We use the `ffnode` umbrella chart to manage all microservices (MongoDB, APIs, etc.) as a single logical commit.

---

## 4. Terraform Design: Data-Centric Infrastructure

Our IaC logic separates the **Logical Model** (what we want) from the **Physical Implementation** (how the provider builds it).

- **The Config Pattern:** All environment metadata, networking CIDRs, and EKS/AKS specs are defined in a structured `config.tf` map.
- **Implicit Mapping:** Subnet identifiers (`Jumpbox`, `Eks_az_1`) tie the configuration to the module logic via name-based lookups.
- **Zero Hardcoding:** Derived data (CIDRs, AZ slices) ensures the code is portable across regions.

---

## 5. Security Architecture

- **Private Networking:** Clusters reside in private subnets with strictly controlled NAT/Internet egress.
- **Vault-Backed Secrets:** Zero secrets in Git. The **Vault Secrets Operator (VSO)** synchronizes encrypted data from HCP Vault into Kubernetes native secrets at runtime.
- **Auth0 Offloading:** Application-level authentication is handled by Auth0, decoupled from the infrastructure identity.
