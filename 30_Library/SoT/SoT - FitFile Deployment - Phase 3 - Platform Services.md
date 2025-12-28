---
alias: ["Cluster OS Setup", "FitFile Deployment Phase 3"]
aliases: []
confidence: "5/5"
created: 2025-12-21T10:51:18Z
epistemic: "process"
last_reviewed: "2025-12-23"
modified: 2025-12-28T09:56:10+00:00
purpose: "To provide a detailed guide for Phase 3 of the FitFile deployment process: installing the platform management layer."
review_interval: "3 months"
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: []
status: "stable"
tags: ["argocd", "ff_deploy", "phase3", "platform"]
title: SoT - FitFile Deployment - Phase 3 - Platform Services
type: "SoT"
uid: 
updated: 
---

## 1. Goal: Installing the Cluster OS

Phase 3 transitions from raw infrastructure to a managed platform. We install the tools that handle GitOps, secret sync, and traffic routing from *within* the private network. This phase establishes the platform configuration necessary for application stability.

---

## 2. Platform Installation & Configuration

### A. ArgoCD & VSO Setup

1. Navigate to the platform module on the **Jumpbox**.
2. Update `vars.tfvars` with the Vault AppRoles generated in Phase 2.
3. Run `terraform apply` to install the ArgoCD controller and the Vault Secrets Operator (VSO). This establishes the secure communication link to the Phase 1 Vault instance.

### B. Ingress & Routing

- **Ingress Controller:** Deploy NGINX to handle Layer 7 traffic routing and TLS termination.
- **CoreDNS Rewrites:** Add rewrite rules to CoreDNS to prevent hairpin routing issues when services call themselves via their public FQDN from within the cluster.

### C. Storage & Persistence

- **StorageClass:** Ensure the default storage class (e.g., `gp2` or Azure Disk) has a `ReclaimPolicy` set to `Retain` to prevent accidental data loss during cluster updates.

### D. Namespace Preparation

Create the application namespace and the critical image pull secrets:

```bash
kubectl create namespace <deployment-key>
kubectl create secret docker-registry fitfile-image-pull-secret \
  --docker-server=<acr-name>.azurecr.io \
  --docker-username=<id> \
  --docker-password=<key> \
  -n <deployment-key>
```

---

## 3. Post-Install Configuration

### A. StorageClass

Ensure the default storage class (e.g., `gp2` or Azure Disk) has a `ReclaimPolicy` set to `Retain` to prevent accidental data loss during cluster updates.

### B. CoreDNS Rewrites

Add rewrite rules to CoreDNS to prevent hairpin routing issues when services call themselves via their public FQDN from within the cluster.

---

## 4. Verification Checklist

- [ ] **ArgoCD UI:** Accessible via Jumpbox browser; shows "Healthy."
- [ ] **VSO:** `VaultAuth` and `VaultStaticSecret` CRDs are present.
- [ ] **Secrets:** K8s secrets are being created in the application namespace.
- [ ] **Ingress:** NGINX controller has an internal load balancer IP.
