---
aliases: [Deployment Master Guide, FitFile Deployment Playbook, Start Here - Deployment]
created: 2025-12-21T09:34:38+00:00
last_reviewed: 2026-02-01
modified: 2026-07-04T10:51:11+00:00
permalink: llmeon/30-library/mo-c/moc-fit-file-deployment
Reviewed: false
status: stable
tags: [ff_deploy, index, process]
title: MOC - FitFile Deployment
type: map
updated: 2026-02-01
---

## MOC - FITFILE Deployment Playbook

> [!abstract] Executive Summary
> This document orchestrates the end-to-end deployment of the FitFile platform. It routes engineers through the six execution phases, architectural principles, and troubleshooting protocols.

---

### 1. Core Architecture (Knowledge)

Understand the _Why_ before the _How_. These notes define the stable logic of the system.

- [[SoT - FitFile Deployment - Strategy & Architecture]] rel:: definition - The Master Map. Cloud hierarchy, GitOps flow, and Security invariants.
- [[SoT - FitFile Deployment - Platform Module]] rel:: definition - The Platform Module (Terraform) Source of Truth.
- [[SoT - FitFile Identity & Access Management (Auth0)]] rel:: security - The canonical guide for Authentication, OAuth2 flows, and Identity configuration.
- [[SoT - FITFILE Secret Management Architecture]] rel:: security - The architectural model for Vault and VSO integration.
- [[SoT - FitFile Secrets Operations (Vault & VSO)]] rel:: operations - The SOP for creating, managing, and debugging secrets.

---

### 2. Execution Roadmap (The 6 Phases)

Follow the [[SoT - FitFile Deployment - Implementation Manual]] for the step-by-step checklist.

#### Phase 0-2: Foundation & Infrastructure

- Phase 0: Pre-Flight: Essential checks before provisioning.
  - CIDR Allocation: Verify no overlapping CIDRs between Customer Spoke and Central Services Hub.
  - Vault Initialization: Create paths in `admin` namespace under `deployments/{deployment-key}/secrets/` (paths: `application`, `argocd`, `monitoring`).
  - Deployment Keys: Generate unique ID (e.g., `lca-prd-01`) for TFC workspaces and resource tagging.
- Phase 1: Network: Establishing the connectivity fabric.
  - VNET/Peering: Provision VNETs and establish Hub-Spoke peering. Verify "Connected" state in Azure/AWS.
  - Split-Horizon DNS: Link `{customer_id}.internal` Private DNS Zone to both VNETs; configure conditional forwarding for `nhs.local`.
  - Firewall Coordination: Provide static LB IP to client for 443 allow-listing.
- Phase 2: Infrastructure: AKS/EKS Cluster provisioning via Terraform.
  - TFC Setup: Configure workspaces naming `<customer-name>-infrastructure` linked to GitLab.
  - Jumpbox Access: Provision secure jumpbox; verify cluster health via SSM/Private Link.
  - Detailed Guide: [[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]
- Prerequisite: [[Protocol - Azure Customer Preparation]]—Customer tenant preparation.

#### Phase 3-4: Platform & Application

- Phase 3: Platform ("Cluster OS"): Bootstrapping the GitOps Control Plane.
  - Dependency Order: Namespaces -> VSO -> Reflector -> Ingress -> ArgoCD.
  - Vault Secrets Operator (VSO): Authenticates via AppRole; syncs `fitfile-image-pull-secret`.
  - Reflector: Mirrors secrets to application namespaces.
  - Ingress: NGINX Controller with Internal Load Balancer (Private Clusters).
  - ArgoCD: The CD engine that takes over lifecycle management.
- Phase 4: Application: Deploying the `ffnode` umbrella chart.
  - Core Services: `ffcloud` (Coordinator), `fitconnect` (Connectivity), `frontend` (UI), `spicedb` (Permissions).
  - Persistence: Stateful sets for PostgreSQL, MongoDB (ReplicaSet), and MinIO (Object Storage).
  - Configuration: Controlled via `deploymentKey` and boolean feature flags (`deploy.persistence`, `deploy.monitoring`).
  - Detailed Guide: [[SoT - FitFile Deployment - Helm Architecture & Operations]]

#### Phase 5-6: Access & Handoff

- Access: TLS Certificates, Ingress, and Public DNS.
- Handoff: Client-side routing validation and Smoke Tests.

---

### 3. Specialized Guides & Protocols

- [[SoT - FitFile Deployment - Networking and Security]] rel:: deep-dive - Detailed breakdown of private link architecture, DNS split-horizon, and Calico policies.
- [[SoT - NHS MESH Integration]] rel:: integration - Sandbox environment and firewall rules for NHS data exchange.
- [[SoT - FitFile Deployment - Troubleshooting and Known Issues]] rel:: troubleshooting - Rapid recovery steps for common failure modes (Sync, VSO, Ingress).
- [[Protocol - Azure Jumpbox Preflight]] rel:: checklist - Customer-facing connectivity verification script.

---

### 4. Operational Maintenance

- [[backing_up_and_restoring_data_in_kubernetes_clusters_on_eks_and_aks]] rel:: operations - Data protection strategies.
- [[How to Reduce Grafana Cloud Costs]] rel:: operations - Observability tuning and cost management.
- [[SoT - Cloud-Native Observability]] rel:: component - Metrics, Logging, and Alerting strategy.

---
