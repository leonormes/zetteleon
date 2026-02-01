---
aliases: [Deployment Master Guide, FitFile Deployment Playbook, Start Here - Deployment]
created: 2025-12-21T09:34:38Z
last_reviewed: 2026-02-01
modified: 2026-02-01T15:35:00+00:00
Reviewed: true
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
- [[SoT - FitFile Identity & Access Management (Auth0)]] rel:: security - The canonical guide for Authentication, OAuth2 flows, and Identity configuration.
- [[SoT - FITFILE Secret Management Architecture]] rel:: security - The architectural model for Vault and VSO integration.
- [[SoT - FitFile Secrets Operations (Vault & VSO)]] rel:: operations - The SOP for creating, managing, and debugging secrets.

---

### 2. Execution Roadmap (The 6 Phases)

Follow the **[[SoT - FitFile Deployment - Implementation Manual]]** for the step-by-step checklist.

#### Phase 0-2: Foundation & Infrastructure
- **Pre-Flight**: CIDR checks, Vault paths, Deployment Keys.
- **Network**: VNETs, Peering, DNS, and Firewall coordination.
- **Infrastructure**: AKS/EKS Cluster provisioning via Terraform.
  - Detailed Guide: [[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]
- **Prerequisite:** [[Azure Customer Checklist]]—Customer tenant preparation.

#### Phase 3-4: Platform & Application
- **Platform**: "Cluster OS" (ArgoCD, VSO, Ingress) installation.
- **Application**: Deploying the `ffnode` umbrella chart (Microservices, Persistence).
  - Detailed Guide: [[SoT - FitFile Deployment - Helm Architecture & Operations]]

#### Phase 5-6: Access & Handoff
- **Access**: TLS Certificates, Ingress, and Public DNS.
- **Handoff**: Client-side routing validation and Smoke Tests.

---

### 3. Specialized Guides & Protocols

- [[SoT - FitFile Deployment - Networking and Security]] rel:: deep-dive - Detailed breakdown of private link architecture, DNS split-horizon, and Calico policies.
- [[SoT - FitFile Deployment - Troubleshooting and Known Issues]] rel:: troubleshooting - Rapid recovery steps for common failure modes (Sync, VSO, Ingress).

---

### 4. Operational Maintenance

- [[Kubernetes Backup and Disaster Recovery for AWS and Azure]] rel:: operations - Data protection strategies.

---

Navigation Hubs:

- [[SoT.base|All Source of Truth Notes]]
- [[MOCx.base|All Maps of Content]]