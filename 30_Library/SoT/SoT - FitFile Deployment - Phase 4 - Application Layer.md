---
aliases: [FitFile Deployment Phase 4]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T14:57:22Z
purpose: To provide a detailed guide for Phase 4 of the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [application, ff_deploy, phase4]
title: SoT - FitFile Deployment - Phase 4 - Application Layer
type: SoT
uid: 
updated: 
version: 1.0
---

## Phase 4: Application Layer (The Logic)

**Goal:** Deploy the actual FitFile services (FFNode, MongoDB, Frontend) via GitOps.

- **Detailed Guide:** [[Set Up New Deployment]] (See "Deploy the Platform" section).
- **Helm Charts:**
    - [[Helm Charts Deployment]]
    - [[Simplify the helm charts]]
    - [[Helm Chart Management Tool]]
    - [[refactoring_suggestions]]
    - [[FFNODE as Umbrella Chart]]
- **Key Actions:**
    1. **ArgoCD:** Deploy ArgoCD.
    2. **Vault:** Deploy Vault.
    3. **Argo Workflows:** Deploy Argo Workflows.
    4. **Monitoring Stack:** Deploy Prometheus, Grafana, AlertManager.
    5. **Config:** Create the customer-specific `values.yaml` in the `ffnodes/` repository.
    6. **Sync:** In ArgoCD, sync the Root Application (`ff-<deployment_key>`).
    7. **Reconcile:** Watch as ArgoCD hydrates the child applications (MongoDB, FitConnect, etc.).
- **Verification:**
    - [ ] All ArgoCD Apps show `Synced` and `Healthy`.
    - [ ] Frontend accessible via public URL.
    - [ ] Integration tests pass (if configured).
    - [ ] Validate ArgoCD deployment
    - [ ] Test Vault secret management
    - [ ] Confirm workflow execution
    - [ ] Check monitoring data flow
