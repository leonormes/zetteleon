---
aliases: [Deployment Master Guide, FitFile Deployment Playbook, Start Here - Deployment]
confidence: 5/5
created: 2025-12-21T09:34:38Z
epistemic: synthesis
last_reviewed: 2025-12-23
modified: 2025-12-27T20:40:58+00:00
purpose: The primary entry point and Master Guide for the FitFile platform deployment process.
review_interval: 3 months
Reviewed: true
see_also: ["[[SoT - FITFILE Platform Deployment]]", "[[SoT - FITFILE Secret Management Architecture]]"]
source_of_truth: []
status: stable
tags: [ff_deploy, index, process]
title: MOC - FitFile Deployment
type: MOC
uid: 
updated: 
---

## MOC - FITFILE Deployment Playbook

> [!abstract] Executive Summary
> This document orchestrates the end-to-end deployment of the FitFile platform. It routes engineers through four distinct execution phases, architectural principles, and troubleshooting protocols.

---

### 1. Core Architecture (Knowledge)

Understand the *Why* before the *How*. These notes define the stable logic of the system.

- **[[SoT - FITFILE Platform Deployment]]**—**The Master Map.** High-level GitOps flow, Three-Tier architecture, and "App of Apps" pattern.
- **[[SOT - CI-CD Pipelines]]**—The engine documentation for GitLab pipelines.
- **[[SoT - FITFILE Secret Management Architecture]]**—The canonical model for Vault and VSO. *(Updated with Oct 2025 Audit & Security Standards)*

---

### 2. Execution Roadmap (The Phases)

Follow these phases sequentially to transform an empty cloud account into an operational node.

#### Phase 1: Foundation & Tooling

Establish the central control plane (HCP, Vault, Auth0, Monitoring). [[HEAD - Auth0 is not part of control plane]]

- **Guide:** [[SoT - FitFile Deployment - Phase 1 - Foundation and Tooling]]

#### Phase 2: Core Infrastructure

Provision the private network, cluster bedrock, and Jumpbox via Terraform.

- **Guide:** [[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]

#### Phase 3: Platform Services

Install the "Cluster OS" (ArgoCD, Ingress, VSO) from within the network.

- **Guide:** [[SoT - FitFile Deployment - Phase 3 - Platform Services]]

#### Phase 4: Application Layer

Deploy microservices and perform post-deploy database/RBAC configuration.

- **Guide:** [[SoT - FitFile Deployment - Phase 4 - Application Layer]]

---

### 3. Specialized Guides & Protocols

- **[[SoT - FitFile Deployment - Networking and Security]]**—Detailed breakdown of private link architecture and Calico policies.
- **[[SoT - FitFile Deployment - Troubleshooting and Known Issues]]**—Rapid recovery steps for common failure modes.

---

### 4. Operational Maintenance

- **[[Kubernetes Backup and Disaster Recovery for AWS and Azure]]**—Data protection strategies.

---

**Navigation Hubs:**
- [[SoT.base|All Source of Truth Notes]]
- [[MOCx.base|All Maps of Content]]
