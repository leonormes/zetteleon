---
aliases: ["FitFile Smoke Tests", "Release Process", "Release Tagging", "Troubleshooting Guide"]
confidence: "5/5"
created: 2025-12-29T10:26:01+00:00
epistemic: "procedure"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:43+00:00
purpose: "Standard operating procedures for managing releases, performing smoke tests, and troubleshooting cluster issues."
review_interval: "3 months"
see_also: ["[[SoT - FitFile Deployment - Implementation Manual]]", "[[SoT - FitFile Deployment - Networking & DNS]]"]
source_of_truth: []
status: "stable"
tags: ["fitfile", "ops", "release", "troubleshooting"]
title: SoT - FitFile Deployment - Operations & Troubleshooting
type: "SoT"
uid: 
updated: 
---

## 1. Release Process (The Tagging Protocol)

FITFILE uses **Environment Pointers** (tags) in the deployment repository to control versions.

### 1.1 Promotion Workflow

1. **Delete Existing Tag:** Remove the pointer (e.g., `latest-release`) from the repository.
2. **Re-create Tag:** Apply the same tag name to the new target commit (SemVer version).
3. **Propagate:** Wait 10-15 minutes for ArgoCD to detect and sync.
4. **Atomic Promotion:** Staging is promoted to Production as a single unit. No cherry-picking.

### 1.2 Smoke Tests (Happy Path)

Execute on Staging before Production promotion:

- [ ] **Login:** Success via Auth0.
- [ ] **Resource Check:** Run plans `int-test-8` and `int-test-26`. Verify counts.
- [ ] **Ingestion:** Create a File Upload datasource, validate, and assign to a project.
- [ ] **Security:** Verify that removing a permission blocks access immediately.

### 1.3 Secret Rotation Policy

Per [[SoT - FITFILE Secret Management Architecture]], secrets automatically rotate based on the `refreshAfter` interval.

- **Databases:** Every 1 hour (Triggers StatefulSet restart).
- **Apps:** Every 15 minutes (Triggers Deployment restart).
- **Manual Rotation:** If a secret is compromised, update it in Vault UI, then delete the `Secret` in K8s to force an immediate VSO sync.

---

## 2. Common Troubleshooting

### 2.1 Deployment Failures

- **ArgoCD Sync Failed:**
    - _Cause:_ VaultAuth failure or missing secret keys in Phase 1.
    - _Action:_ Check `kubectl describe vaultstaticsecret` in the app namespace.
- **Stale Secrets (No Update):**
    - _Cause:_ Missing `refreshAfter` field or broken `rolloutRestartTargets`.
    - _Action:_ Verify VSO resource status: `kubectl get vss`. Ensure the `VSO` label is present on the target Deployment.
- **Image Pull Error:**
    - _Cause:_ Expired registry credentials or incorrect `imagePullSecrets` name.
    - _Action:_ Verify the `fitfile-image-pull-secret` in the target namespace.

### 2.2 Connectivity & DNS

- **SERVFAIL / NXDOMAIN:**
    - _Cause:_ Pods forwarding to On-Prem DNS which doesn't know Azure Private Link zones.
    - _Action:_ Check CoreDNS ConfigMap for `privatelink` forwarding rules.
- **Hairpin Routing:**
    - _Cause:_ Service fails to call its own public FQDN from inside the cluster.
    - _Action:_ Ensure CoreDNS has a rewrite rule mapping the public FQDN to the internal ClusterIP.

### 2.3 Cloud Infrastructure

- **Terraform State Lock:** Clear the lock in the Terraform Cloud console.
- **Node Readiness:** If nodes are "NotReady," check the NAT Gateway for egress saturation or IMDSv2 enforcement issues.

---

## 3. Operations Resources

- [[Fitfile deployment fixes]] - Collection of rapid patches.
- [[Debugging Internet Connectivity Issues from a Linux Jumpbox in AWS VPC]] - Networking deep dive.
- [[SoT - Azure Backup and Restore]] - Handling state recovery.
