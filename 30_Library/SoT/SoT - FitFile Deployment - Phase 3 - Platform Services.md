---
aliases: [FitFile Deployment Phase 3]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T12:00:00Z
purpose: To provide a detailed guide for Phase 3 of the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, phase3, platform, services]
title: SoT - FitFile Deployment - Phase 3 - Platform Services
type: SoT
uid: 
updated: 
version: 1.0
---

## Phase 3: Platform Services (The Runtime)

**Goal:** Install the "Operating System" of the cluster (ArgoCD, Vault integration, Ingress) from *within* the private network.

- **Detailed Guide:** [[FItfile deployment ArgoCD Style]] (Explains the "App of Apps" pattern). See also [[ArgoCD App of Apps Architecture]].
- **Key Actions:**
    1. **Kubernetes Cluster:** Provision EKS/AKS cluster, node groups, and system services.
    2. **Container Registry:** Provision container registry.
    3. **KMS:** Provision Key Management Service.
    4. **Monitoring & Logging:** Provision monitoring and logging infrastructure.
    5. **Jumpbox:** All actions must be performed from the Jumpbox (Private Access).
    6. **Bootstrap:** Clone the `private_platform_template` to the Jumpbox.
    7. **Configure:** Update `vars.tfvars` with the `deployment_key` and values file path.
    8. **Apply:** Run the internal Terraform to deploy ArgoCD and the Root App.
- **Verification:**
    - [ ] ArgoCD UI accessible via Ingress.
    - [ ] Vault Operator pods running.
    - [ ] Ingress Controller has an external IP/DNS.
    - [ ] Confirm cluster is operational
    - [ ] Test container registry pushes/pulls
    - [ ] Verify KMS encryption/decryption
