---
aliases: [Deployment Troubleshooting, Known Issues, Recovery Procedures]
conformant: false
created: 2026-02-01T15:05:00+00:00
modified: 2026-07-20T16:33:50+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-fit-file-deployment-troubleshooting-and-known-issues
tags: [ff_deploy, ops, sot, troubleshooting]
title: SoT - FitFile Deployment - Troubleshooting and Known Issues
type: sot
---

## 1. Overview

This document catalogs common failure modes during FitFile deployment and provides verified recovery procedures. It acts as the "Emergency Room" manual for Deployment Engineers.

General Rule: Always verify the foundation (DNS, Networking, Identity) before debugging the application.

---

## 2. Infrastructure & Networking Failures

### 2.1 "VNET Peering Connected but No Traffic"

Symptom: Peering status is `Connected`, but traffic from Hub to Spoke times out.

Cause: Route tables in Azure/AWS take up to 10 minutes to propagate.

Fix: Wait 10 mins. Verify no overlapping CIDRs (Phase 0 check).

### 2.2 "NXDOMAIN" Errors in ArgoCD

Symptom: ArgoCD fails to sync, claiming it cannot resolve internal service names.

Cause: The Private DNS Zone is linked to the Spoke VNet but not the Hub VNet.

Fix: Add a "Virtual Network Link" from the Private DNS Zone to the Hub VNet.

---

## 3. Platform & GitOps Failures

### 3.1 Argo Vault Path Mismatch

Symptom: ArgoCD deploys `VaultStaticSecret` with wrong path (e.g., `argo-workflows`) despite correct `values.yaml` in Git.

Cause: Stale Application Definition. The ArgoCD Application CR may have hardcoded inline values in its spec that take precedence over the file-based `generated/values.yaml`.

Fix: Run `argocd app get {app} --hard-refresh` or patch the Application CR to remove inline overrides.

### 3.2 VSO "Permission Denied" (Double Namespace)

Symptom: VSO logs show `Permission Denied` when reading secrets.

Cause: Platform module prepending `admin/` to a namespace that already contains it (`admin/admin/deployments/…`).

Fix: Set `vault_namespace` in Terraform to `deployments/{deployment-key}` (omitting the `admin/` prefix).

### 3.3 OIDC Issuer Mismatch

Symptom: VSO fails to authenticate after cluster recreation.

Cause: The OIDC discovery URL changed on the new cluster, but Vault's JWT auth mount is still configured with the old issuer.

Fix: Update the Vault JWT auth backend config with the new OIDC URL from `az aks show`.

---

## 4. Application & Runtime Failures

### 4.1 Pods Stuck in `CreateContainerConfigError`

Symptom: Pod fails to start; `describe` shows missing secret.

Cause: VSO hasn't produced the K8s Secret yet.

Fix: Check `kubectl get vaultstaticsecret`. Verify `overwrite: true` is set in the spec.

### 4.2 Pods Stuck in `CrashLoopBackOff` (DB Auth)

Symptom: Apps like `argo-workflows-server` cannot connect to PostgreSQL.

Cause: Wrong Vault path configuration. DB credentials for all apps typically reside in the `application` path, not per-component paths.

Fix: Update `values.cue` to point `vaultPath` to `application`.

---

## 5. Portability & Maintenance

### 5.1 Hardcoded Values in Templates

Symptom: New customer deployments fail with "lca-prd-2" namespace errors.

Cause: Hardcoded strings in `jumpbox_main.tftpl`.

Fix: Replace literals with `$${local.deployment_key}` interpolation to ensure the template is environment-agnostic.

### 5.2 Subscription Creation & Governance

- "Already exists" Error: Usually a dangling Subscription Alias. Use `az account alias list` to identify and delete.
- Diagnostic Gaps: Ensure `microsoft.insights` provider is registered or observability will fail.

## Related Documentation

- [[aks-cluster-bootstrap-debug-runbook]]
- [[SoT - FitFile VSO Secrets Management]]
- [[ARGO_VSO_ROOT_CAUSE]]
