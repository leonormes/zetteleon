---
aliases: [Deployment Master Guide, FitFile Deployment Playbook]
confidence: 5/5
created: 2025-12-20T00:00:00Z
epistemic: synthesis
last_reviewed: 2025-12-21
modified: 2025-12-21T12:00:00Z
purpose: A comprehensive, step-by-step Map of Content (MOC) and guide for deploying the FitFile platform, acting as the primary Source of Truth (SoT) for engineers.
review_interval: 3 months
see_also: ["[[FITFILE Deployment Docs]]", "[[SoT - FITFILE Platform Components]]", "[[SoT - FITFILE Platform Deployment]]", "[[Updated Azure Customer Checklist]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, guide, moc]
title: MOC - FitFile Deployment
type: MOC
uid: 
updated: 
version: 2.0
---

## MOC - FITFILE Deployment Playbook

> [!abstract] Executive Summary
> This document acts as the **Master Deployment Guide** for the FitFile platform. It orchestrates the deployment process across four distinct phases, linking to specific technical guides for detailed execution.
>
> **Goal:** Transform an empty cloud account into a fully operational, compliant FitFile node.

---

### Core SoTs and Architectural Principles (Start Here)

These notes provide the high-level narrative and architecture of the deployment system.

1.  **[[SoT - FITFILE Platform Deployment]]** - **The Master Map.** The end-to-end flow from commit to cloud.
2.  **[[SOT - CI-CD Pipelines]]** - **The Engine.** Detailed documentation of the GitLab CI/CD pipelines.
3.  **[[SoT - FITFILE Secret Management Architecture]]** - **The Keys.** How Vault and VSO secure the platform.
4.  **[[SoT - FitFile Deployment - Architecture and Concepts]]** - The core architectural concepts of the deployment process.

---

### 1. Pre-Flight Checklist

Before initiating any phase, ensure the following prerequisites are met:

- [ ] **Access:** HashiCorp Cloud Platform (HCP), Auth0, GitLab, Cloud Provider (AWS/Azure).
- [ ] **Tooling:** `terraform`, `tfenv`, `aws-cli` / `az-cli`, `kubectl`, `git`. See [[Tooling]] for work index.
- [ ] **Repository:** Cloned `fitfile/terraform-infrastructure` and `fitfile/customers`. See [[Repository Structure Refactoring for Clarity]].
- [ ] **Checklists:** Review the for Azure deployments.
- [ ] **Prerequisites:** [[Prerequisities]]

---

### 2. The Deployment Phases

#### Phase 1: Foundation & Tooling
**Goal:** Establish the central identity, secrets, and monitoring control plane. This is the "Key to the Castle."

- **Detailed Guide:** [[SoT - FitFile Deployment - Phase 1 - Foundation and Tooling]]

#### Phase 2: Core Infrastructure (The Bedrock)
**Goal:** Provision the physical cloud resources (VPC, EKS/AKS, Jumpbox) using Terraform.

- **Detailed Guide:** [[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]

#### Phase 3: Platform Services (The Runtime)
**Goal:** Install the "Operating System" of the cluster (ArgoCD, Vault integration, Ingress) from *within* the private network.

- **Detailed Guide:** [[SoT - FitFile Deployment - Phase 3 - Platform Services]]

#### Phase 4: Application Layer (The Logic)
**Goal:** Deploy the actual FitFile services (FFNode, MongoDB, Frontend) via GitOps.

- **Detailed Guide:** [[SoT - FitFile Deployment - Phase 4 - Application Layer]]

---

### 3. Networking and Security

- **Detailed Guide:** [[SoT - FitFile Deployment - Networking and Security]]

---

### 4. Troubleshooting & Known Issues

- **Detailed Guide:** [[SoT - FitFile Deployment - Troubleshooting and Known Issues]]

---

### 5. Field Notes & Gotchas (From the Trenches)

- **Detailed Guide:** [[SoT - FitFile Deployment - Field Notes and Gotchas]]

---

### 6. Deployment Log (Reference)

For a raw, real-world example of a deployment log including error messages and "gotchas", see the institutional knowledge captured in this MOC.
