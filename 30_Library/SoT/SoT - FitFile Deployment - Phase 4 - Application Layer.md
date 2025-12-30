---
aliases: ["Application Stack Setup", "FitFile Deployment Phase 4"]
confidence: "5/5"
created: 2025-12-21T10:51:29Z
epistemic: "process"
last_reviewed: "2025-12-23"
modified: 2025-12-30T14:11:35+00:00
purpose: "To provide a detailed guide for Phase 4 of the FitFile deployment process: deploying the application microservices."
review_interval: "3 months"
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: []
status: "stable"
tags: ["application", "ff_deploy", "helm", "phase4"]
title: SoT - FitFile Deployment - Phase 4 - Application Layer
type: "SoT"
uid: 
updated: 
---

## 1. Goal: Deploying the Logic

Phase 4 is the final stage where the actual FITFILE services (FFNode, MongoDB, APIs) are deployed via GitOps. This phase leverages the foundational work of the previous three stages: secrets from Vault (Phase 1), compute resources (Phase 2), and the ArgoCD engine (Phase 3).

---

## 2. Helm & GitOps Configuration (FFNode)

### A. The Deployment Repository

ArgoCD pulls the configuration from the dedicated customer deployment repository. This repository contains the `values.yaml` files that define the state of the cluster.

### B. The Umbrella Chart

The `ffnode` chart aggregates all sub-components. Configuration is managed via customer-specific `values.yaml` files.

```yaml
# Example: ffnodes/fitfile/customer-prod/values.yaml
namespace: "customer-prod"
deploymentKey: "customer-prod"
deploy:
  mongodb: true
  spicedb: true
  fitconnect: true
```

### C. Deployment Trigger

1. Merge the `values.yaml` changes into the `master` branch of the customer repository.
2. ArgoCD will automatically detect the change and reconcile the cluster state, pulling the specified container images using the Phase 3 image pull secrets.
3. The application will consume secrets stored in Vault and authenticate users via the Auth0 configuration established in Phase 1.

---

## 3. Post-Deployment Configuration

### A. Database Initialization

- **MongoDB:** Insert the initial `Tenants` and `Connections` documents required for the platform to recognize the client.
- **SpiceDB:** Create the required project relationships and permissions.

### B. RBAC and Permissions

Assign the `data_source_manager` role to the initial set of administrative users in Auth0 to enable platform configuration.

---

## 4. Verification Checklist

- [ ] **ArgoCD Sync:** All child applications show "Synced" and "Healthy."
- [ ] **Pipeline:** Integration tests in GitLab pass.
- [ ] **Accessibility:** The frontend is reachable via the internal Ingress IP.
- [ ] **Secrets:** Application pods successfully mount Vault-injected secrets.
