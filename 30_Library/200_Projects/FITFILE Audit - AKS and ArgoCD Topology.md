---
created: 2026-08-27T10:30:00+00:00
date: 2026-08-27
modified: 2026-08-29T09:36:12+00:00
permalink: llmeon/30-library/200-projects/fitfile-audit-aks-and-argocd-topology
project_category: refined_deployment
project_name: Pipeline
project_status: active
tags: [aks, argocd, audit, gitops, infrastructure/azure, kubernetes, trivy]
title: FITFILE Audit - AKS and ArgoCD Topology
type: audit
---

## AKS / ArgoCD Deployment Topology

Section of [[FITFILE Delivery Pipeline Audit 2026-08-27]]. Verified live 2026-08-27 via `az aks list` and `kubectl` against three contexts.

---

### 1. Cluster Inventory

| Cluster | Subscription | K8s | API server | State | ArgoCD | Trivy Operator |
|---|---|---|---|---|---|---|
| `fitfile-cloud-prod-1-aks-cluster` | FITCloud Production | 1.35.7 | Public | Running | v3.5.1 | 0.25.0 |
| `fitfile-cloud-staging-aks-cluster` | FITCloud Non-Production | 1.36.3 | Public | Running | v3.5.1 | 0.33.0 |
| `fitfile-cloud-testing-aks-cluster` | FITCloud Non-Production | 1.36.3 | Public | Running |—| Absent |
| `aks-ff-uks-gp-1` | Testing | 1.35.7 | Private | Running |—|—|
| `aks-ffsts{2,3,4,5}-ukw-gp-1` | Testing | 1.34.7 | Private | Stopped ×4 |—|—|

The newer `aks-ff-*` pattern uses private API servers; the three long-standing `fitfile-cloud-*` clusters, including production, do not. The better pattern is already established internally but has not been retrofitted.

Production also trails non-production by a minor Kubernetes version (1.35.7 vs 1.36.3)—staging tests on a version production does not run.

Four stopped ukwest clusters carry residual cost and cleanup debt.

---

### 2. Customer Environments Run in Customer Tenants, via a Per-tenant ArgoCD

The customer production environments named in `Deployment/Clusters/`—NNUH-DP, LCA-DP, MCNFT, mkuh-prd-4—are not in FitFile's subscriptions, and have no ArgoCD Application in either of the two FitFile-run instances (staging, prod-1) audited directly. That is a fact about _visibility_, not architecture: confirmed directly with the platform owner, Terraform provisions the customer's AKS cluster and bootstraps a third ArgoCD instance inside that tenant, seeded with the same `deployment.git` app-of-apps used by staging and production—tracking a customer-specific tag rather than `master` or `latest-release`.

The mechanism is the `terraform-argo-argocd` module (present in `Deployment/TFC-Modules/`); the workspace-naming pattern splits cluster provisioning from platform/ArgoCD bootstrap, visible directly in the TFC workspace list for four customers:

| Customer | Infra workspace | Platform / ArgoCD-bootstrap workspace |
|---|---|---|
| NNUH | `nnuh-prod-1` | `nnuh-prod-1-platform` (never-run, 53 resources) |
| MKUH | `mkuh-prd-4` | `mkuh-prd-4-platform` (never-run, 46 resources) |
| CUH | `cuh-prod-1` | `cuh-prod-1-platform` (never-run, 49 resources) |
| HIE |—| `hie-prod-34-platform` (never-run, 53 resources) |

LCA (`lca-prd-2`) and MCNFT (`mcnft-prod-1`) have no matching `-platform` workspace in the enumerated 54. Either an older environment bootstrapped differently, or the platform layer lives inside the main workspace—not confirmed either way, worth asking rather than assuming.

`az account list` shows `NNUHFT-SDE` under a different tenant (`d2a06081-…`), and `NNUH-DP/config/customer.yaml` sets `resource_prefix: "NNUHFT-SDE"` with a private VNet range (`192.168.200.0/24`)—consistent with a fully separate tenant running its own ArgoCD.

Customer deployments are therefore provisioned by Terraform, bootstrapped with ArgoCD by Terraform, then reconciled continuously by that ArgoCD instance against `deployment.git`—the same GitOps mechanism as staging and production, just additional (per-tenant) instances each tracking their own tag. None of it is reachable with this audit's credentials, so sync status, drift, and tag-currency per customer are unverified. This also multiplies the S-13 finding (no immutable revision pinning) across every customer tag, not just two branches—see [[FITFILE Audit - Security Findings and Remediation]].

The cross-reference of "every customer environment has a corresponding ArgoCD app" is satisfied architecturally, just not verifiable from FitFile's own two clusters. Five `customer.yaml` files exist (NNUH-DP, mkuh-prd-4, LCA-DP, MCNFT, ff-test-1); their matching TFC workspaces all exist, and—for at least NNUH, MKUH, CUH and HIE—so does a distinct platform-bootstrap workspace.

| Customer config | Region / env | Matching TFC workspace |
|---|---|---|
| `eoe/Production/NNUH-DP` | uks / live | `nnuh-prod-1` (last run discarded) |
| `eoe/Production/mkuh-prd-4` | uks | `mkuh-prd-4` (applied 2026-08-18) |
| `nwsde/Production/LCA-DP` | uks / live | `lca-prd-2` (errored 2026-04-13) |
| `nwsde/Production/MCNFT` | uks | `mcnft-prod-1` (applied 2026-02-25) |
| `eoe/Test/ff-test-1` | uks / test |—|

---

### 3. ArgoCD Applications

| Cluster | Apps | Target revision | Sync | Health |
|---|---|---|---|---|
| `prod-1` | 39 | `latest-release` | 38 Synced · 1 OutOfSync (`ff-a`) | 38 Healthy · 1 Progressing |
| `staging` | 32 | `master` | 27 Synced · 4 OutOfSync · 1 Unknown | 29 Healthy · 3 Degraded |

Production namespaces: `barts`, `ff-a`, `ff-b`, `ff-c`, `thehyve`, `thehyve-cuh`, `thehyve-mkuh`, `spicedb`, `argo`, `cert-manager`, `monitoring`.

Staging carries a `cuh-prod-1` namespace—a production-named customer namespace on non-production infrastructure. Either the name is misleading or the placement is.

`thehyve-mkuh` is the only production app with automated sync disabled.

---

### 4. Environment Parity Gap

Staging is not testing what production runs:

| Component | Production | Staging | Divergence |
|---|---|---|---|
| `argo-workflows` | `0.45.*` | `2.0.*` | Major version |
| `cert-manager` | `v1.18.2` | `v1.21.1` | 3 minor |
| `trivy-operator` | `0.25.0` | `0.33.0` | 8 minor |
| Git revision | `latest-release` | `master` | Different gate |

---

### 5. Nothing is Pinned to an Immutable Revision

No ArgoCD Application pins an immutable revision. Staging tracks `master`, production tracks the movable tag `latest-release`, one app (`stress-testing-omop-vocab`) tracks `HEAD`, and Helm sources use floating ranges `2.0.*` and `0.45.*`.

A redeploy can therefore change what runs with no corresponding commit—the deployed state is not reproducible from a revision. Combined with force-push permitted on `fitfile/deployment` master (S-09), there is no revision that reliably reconstructs a past deployment.

[[FTFL-512_CICD_Incident_Report]] reached this independently:

> Only `sandbox-testing-1` pins to a release tag. Every other environment—including the one that self-labels staging (`ff-test-a`)—defaults to `targetRevision: master` with self-heal, so it deployed the bad commit the instant it hit `master`.

---

### 6. Vulnerability Scanning Coverage

| Cluster | Trivy Operator | VulnerabilityReports | SBOMReports | Notes |
|---|---|---|---|---|
| staging | 0.33.0 + EPSS/KEV exporter + VEX cache proxy | 102 | 340 | Newest stack |
| prod-1 | 0.25.0 | 64 | 148 | No EPSS/KEV, no VEX proxy |
| testing | none running | 27 (Nov 2024) | 30 (stale) | CRDs present, operator removed |

The testing cluster has CRDs and 27 VulnerabilityReports, which makes it look scanned. The reports are dated November 2024—21 months old—and `trivy-system` contains no running workload. A dashboard reading these shows reassuring, meaningless data.

Production runs the weakest prioritisation signal of the three.

#### Live CVE Counts (2026-08-27T10:25Z)

| Cluster | Report type | Reports | Critical | High | Medium | Low |
|---|---|---|---|---|---|---|
| staging | Vulnerability | 102 | 203 | 1,544 | 1,646 | 535 |
| staging | Config audit | 290 | 0 | 357 | 766 | 1,117 |
| prod-1 | Vulnerability | 64 | 189 | 1,563 | 1,654 | 565 |
| prod-1 | Config audit | 236 | 0 | 199 | 402 | 802 |

These supersede the previously circulated figures (741 Critical / 1233 High / 2320 config-audit), which do not match current state and should be retired.

The ArgoCD control plane is among the worst-affected workloads: `argoproj/argocd:v3.5.1` carries 2 Critical / 22 High, and `dexidp/dex:v2.45.1`—the authentication component—carries 5 Critical / 43 High.

Trivy images are pulled from `mirror.gcr.io` rather than the internal ACR, despite ACR holding `aquasec/trivy-operator` mirrors—an inconsistent supply chain.

---

### 7. How CI Reaches the Cluster

`Deployment/deployment/staging.gitlab-ci.yml`:

```bash
az login --service-principal -u $AZ_CLIENT_ID -p $AZ_CLIENT_SECRET --tenant $TENANT_ID
az aks get-credentials --name Fitfile-cloud-testing-aks-cluster \
  --resource-group Fitfile-cloud-testing-rg --subscription $SUBSCRIPTION_ID --admin
```

The `--admin` flag takes clusterAdmin credentials, bypassing Azure AD RBAC entirely. The file's own TODO acknowledges this. Combined with unprotected group variables, this is step 3 of the S-01 chain in [[FITFILE Audit - Security Findings and Remediation]].

Note also the naming: a file called `staging.gitlab-ci.yml` deploys to `Fitfile-cloud-testing-aks-cluster` and `testing-argocd.fitfile.net`. [[FTFL-512_CICD_Incident_Report]] cites the same confusion as contributing to an outage.

---

### Related

- [[FITFILE Delivery Pipeline Audit 2026-08-27]]—hub
- [[FITFILE Audit - Security Findings and Remediation]] · [[FITFILE Audit - Terraform and IaC State]]
- [[FTFL-512_CICD_Incident_Report]] · [[aks-ff-uks-gp-1-wiki]]
- [[Missing Grafana Monitoring in Testing Cluster]] · [[Azure Backup for AKS]]
