---
aliases: [Deployment Troubleshooting, Known Issues, Recovery Procedures]
created: 2026-02-01T15:05:00Z
modified: 2026-02-04T07:27:20+00:00
status: evergreen
tags: [ff_deploy, ops, sot, troubleshooting]
title: SoT - FitFile Deployment - Troubleshooting and Known Issues
type: SoT
---

## 1. Overview

This document catalogs common failure modes during FitFile deployment and provides verified recovery procedures. It acts as the "Emergency Room" manual for Deployment Engineers.

General Rule: Always verify the foundation (DNS, Networking, Identity) before debugging the application.

---

## 2. Infrastructure & Networking Failures

### 2.1 "VNET Peering Connected but No Traffic"

Symptom: Peering status is `Connected`, but `ping` or `curl` from Hub to Spoke times out.

Cause: Route tables in Azure/AWS take up to 5-10 minutes to propagate after the status change.

Fix:

1. Wait 10 minutes.
2. Verify no overlapping CIDRs (Phase 0 check).
3. Check Network Security Groups (NSG) on the subnet level.

### 2.2 "NXDOMAIN" Errors in ArgoCD

Symptom: ArgoCD fails to sync, claiming it cannot resolve internal service names.

Cause: The Private DNS Zone is linked to the Spoke VNET but not the Hub VNET (Split-horizon configuration missing).

Fix:

1. Go to Private DNS Zone in Azure Portal.
2. Add a "Virtual Network Link" to the Hub VNET.

---

## 3. Platform & GitOps Failures

### 3.1 ArgoCD "Sync Failed" / "Hook Failed"

Symptom: Application status is `Degraded` or `Sync Failed`.

Common Causes:

- CRD Missing: Attempting to create a `VaultStaticSecret` before VSO is fully installed.
- Namespace Missing: Helm chart assumes namespace exists.
Fix:
- Use "Sync Waves" (ensure VSO installs in Wave -1 or 0).
- Manually create the namespace: `kubectl create ns <deployment-key>`.

### 3.2 VSO Secrets "Unknown" or Not Syncing

Symptom: `kubectl get vaultstaticsecret` shows status `Unknown` or `False`.

Cause 1 (Cache): `argocd-repo-server` has cached stale Auth credentials.

Fix 1:

```bash
kubectl rollout restart deployment/argocd-repo-server -n argocd
```

Cause 2 (Identity): Workload Identity hasn't propagated (takes 15-30m on new clusters).

Fix 2: Check VSO logs: `kubectl logs -l app.kubernetes.io/name=vault-secrets-operator -n vault-secrets-operator`. If "permission denied" to Vault, wait.

---

## 4. Application & Runtime Failures

### 4.1 Pods Stuck in `CreateContainerConfigError`

Symptom: Pod fails to start.

Cause: Missing Secret. The Pod is trying to mount a secret that VSO hasn't created yet.

Fix:

1. Check `kubectl describe pod <pod-name>`.
2. Verify the `VaultStaticSecret` exists and is `Valid`.
3. Check Vault Path in `values.yaml` vs reality in HCP Vault.

### 4.2 "502 Bad Gateway" on Ingress

Symptom: NGINX returns 502.

Cause: The Service has no healthy endpoints (Pods are crashing or not matching the selector).

Fix:

1. `kubectl get endpoints -n <namespace>` -> Ensure IPs are listed.
2. If empty, check Pod labels match Service selector.
3. Check Pod logs for application crash loops.

---

## 5. Cloud-Specific Known Issues

### 5.1 Azure AKS

- EncryptionAtHost: Deployment fails if this feature isn't enabled on the subscription. (See [[SoT - Azure Kubernetes Service (AKS) Operations]])
- ACR Image Pull: `ErrImagePull` often means the Service Principal lacks `AcrPull` on the central registry.

### 5.2 AWS EKS

- AWS Auth ConfigMap: `unauthorized` errors often mean the user/role mapping in `aws-auth` ConfigMap is missing or incorrect.
- Subnet Tags: ALBs fail to provision if subnets lack `kubernetes.io/role/elb` tags.
# 5.2 AWS EKS

### 5.3 Subscription Creation & Governance

- **"Already exists" Error**: Usually a dangling **Subscription Alias**. Use `az account alias list` to identify and delete.
- **Permission Denied (Creation)**: Ensure you have the **Azure subscription creator** role at the **Billing Invoice Section** level, in addition to Management Group rights.
- **Policy Contamination**: To bypass inherited policies, place the subscription in a parallel Management Group branch directly under the Root.
- **Detailed Guide**: See [[2026-02-09 - Azure Sandbox Subscription Isolation]].
