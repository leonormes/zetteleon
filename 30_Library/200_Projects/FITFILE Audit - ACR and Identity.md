---
created: 2026-08-27T10:30:00+00:00
date: 2026-08-27
modified: 2026-08-29T09:36:12+00:00
permalink: llmeon/30-library/200-projects/fitfile-audit-acr-and-identity
project_category: refined_deployment
project_name: Pipeline
project_status: active
related_tickets: [FTFL-1015, FTFL-951, FTFL-974]
tags: [acr, audit, identity, infrastructure/azure, permissions, security, supply-chain]
title: FITFILE Audit - ACR and Identity
type: audit
---

## ACR & Identity

Section of [[FITFILE Delivery Pipeline Audit 2026-08-27]]. Verified live 2026-08-27 via `az` 2.89.1 and Microsoft Graph.

---

### 1. Two Registries, not One

Both live in `fitfile-shared-container-registry-rg`, subscription `a085dd04` (Shared Services—not "Testing", which is `7bbc8ae5`). `Fitfileregistry` was created 2020-10-20.

| Registry | SKU | Repos | Admin user | Anon pull | Public net | Trust policy | Retention |
|---|---|---|---|---|---|---|---|
| `Fitfileregistry` | Premium | 178 | Enabled | Disabled | Enabled | Disabled | Disabled |
| `FITFILEPublic` | Standard | 65 | Enabled | Enabled | Enabled | n/a | Disabled |

`Fitfileregistry` holds both FitFile first-party images and mirrored third-party charts/images (bitnami, grafana, hashicorp, argoproj, aquasec). `FITFILEPublic` holds mostly third-party mirrors—calico, trivy, velero, ingress-nginx, vault, and `argoproj/argocd`.

---

### 2. The Network Allowlist that Allows Everything

`Fitfileregistry` carries four IP allow-rules—`51.11.43.42`, `20.90.229.60`, `34.74.226.0/24`, `34.74.90.64/28`—under `defaultAction: "Allow"`.

With the default action set to Allow, the allowlist is inert: it restricts nothing and every source is permitted. This has the shape of a control and the effect of none.

```
az acr show --name Fitfileregistry
  adminUserEnabled: true          trustPolicy:      disabled   (no image signing)
  publicNetworkAccess: Enabled    quarantinePolicy: disabled   (no scan-before-use)
  networkRuleSet.defaultAction:   "Allow"  <- 4 ipRules present but non-binding
  retentionPolicy: disabled       softDeletePolicy: disabled
  zoneRedundancy: Disabled
```

Also absent: content trust (no image signing), quarantine (no scan-before-use gating), retention (untagged manifests accumulate indefinitely), soft delete (no recovery from accidental deletion). Zone redundancy is disabled on a Premium registry that gates all deployments.

---

### 3. Service Principals and Rotation Status

| Principal | App ID | Created | Secret window | Effective rights | Assessment |
|---|---|---|---|---|---|
| `acr-service-principal` | `39cf7fc7…3bab` | 2020-10-27 | 2026-04-21 → 2026-10-18 | AcrPush on FITFILEPublic; Reader on Fitfileregistry | Expires in 7 weeks |
| `fitfile-helm-auth` | `52d6d2e6…fc4c` | 2026-01-06 | 2026-01-06 → 2027-01-06 | AcrPull on Fitfileregistry | 1-year secret |
| `sp-renovate-acr-pull` | `28e917ad…c896` | 2026-08-26 | 2026-08-26 → 2028-08-26 | No role assignments at all | Non-functional |

Secret metadata read via `az ad app show --query passwordCredentials`; role scope confirmed with `az role assignment list --assignee` across all four active subscriptions. No secret values were read.

#### FTFL-974—partially Complete

The credential _was_ rotated: the active secret on `acr-service-principal` is named `GitLabCiCd` and dates from 2026-04-21, not from the app's 2020 creation.

But it expires 2026-10-18—seven weeks out—and expiry will break every image build across all four application repos simultaneously, since they share this one credential (see [[FITFILE Audit - Repo and Pipeline Inventory]]). Treat as a scheduled outage unless diarised.

#### FTFL-951 / FTFL-1015—incomplete

`sp-renovate-acr-pull` was created 2026-08-26 with a two-year secret but holds no role assignment in any subscription. It cannot pull from private ACR. The identity exists; the grant does not.

```
az role assignment list --assignee 28e917ad-… (all 4 subscriptions)
(empty)
```

---

### 4. The Push-path Problem

`acr-service-principal` holds AcrPush on `FITFILEPublic`—the anonymous-pull registry that serves `argoproj/argocd:v3.5.1` to both production and staging clusters.

A compromise of the routine build credential therefore permits publishing a malicious image that both clusters' GitOps controller will pull. This is step 4 of the S-01 chain in [[FITFILE Audit - Security Findings and Remediation]].

Unresolved: `acr-service-principal` holds only _Reader_ on `Fitfileregistry`, which cannot authorise a push—yet pushes to `Fitfileregistry` succeed. The most likely explanation is that `ACR_SERVICE_PRINCIPLE` holds the registry admin username rather than the SP's app ID, which would also explain why admin user must stay enabled. The variable is masked and its value was not read, so this is inference from behaviour, not confirmation.

---

### 5. Orphaned Role Assignments

24 of 35 role assignments scoped directly to `Fitfileregistry` point at principals that no longer exist in the directory—confirmed by resolving each `principalId` through Microsoft Graph, which returns _"does not exist or one of its queried reference-property objects are not present"_.

Only 11 assignments resolve to a live identity:

- `fitfile-cloud-staging-aks-cluster-agentpool`, `…-prod-1-…`, `…-testing-…`—kubelet managed identities (expected)
- `fitfile-cloud-staging-trivy-operator`, `omopbatch12345`—workload identities
- `fitfile-helm-auth`, `acr-service-principal`—application registrations
- Groups: `FITFILEREGISTRY AcrPull`, `AcrPush`, `FITFILE Contributor/Owner/Reader`, `Platform …`

The practical effect is that the registry's access list cannot be read and understood by a human, which is a prerequisite for any access review.

Deleted directory objects cannot be resolved retrospectively; Azure Activity Log retention may still cover some.

---

### 6. Standing Privileged Access

Also visible at or above registry scope: `User Access Administrator` held directly by a named user account, plus `FITFILE Owner` and `Platform Owner` groups. Worth a separate review against the [[Break-Glass Identity The Complete Plan]] model.

---

### Related

- [[FITFILE Delivery Pipeline Audit 2026-08-27]]—hub
- [[FITFILE Audit - Repo and Pipeline Inventory]] · [[FITFILE Audit - Security Findings and Remediation]]
- [[FITFILE Audit - Terraform and IaC State]]—the `ff-central-private-acr` workspace has been failing since April
- [[FTFL-799_Unified_Customer_Cloud_Permissions]] · [[Break-Glass Identity The Complete Plan]]
