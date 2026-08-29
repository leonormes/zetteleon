---
created: 2026-08-27T10:30:00+00:00
date: 2026-08-27
modified: 2026-08-29T09:36:13+00:00
permalink: llmeon/30-library/200-projects/fitfile-audit-terraform-and-iac-state
project_category: refined_deployment
project_name: Pipeline
project_status: active
tags: [audit, infrastructure/aws, infrastructure/azure, terraform, terraform-cloud]
title: FITFILE Audit - Terraform and IaC State
type: audit
---

## Terraform / IaC State

Section of [[FITFILE Delivery Pipeline Audit 2026-08-27]]. Verified live 2026-08-27 via the HCP Terraform API.

54 workspaces in the `FITFILE-Platforms` organisation. Three structural problems dominate: unpinned Terraform versions, workspaces driven outside VCS, and a long tail of failed applies nobody has returned to.

---

### 1. Structural Signals

| Signal | Count | of 54 | Why it matters |
|---|---|---|---|
| `terraform-version: "latest"` | 27 | 50% | CLI version floats. A new Terraform release can break an apply with no code change. |
| No VCS repo attached | 20 | 37% | Applies driven from a laptop or API—no commit, no review, no audit trail. |
| Last run errored | 11 | 20% | State and reality have diverged, in several cases for months. |
| No run recorded, yet holds resources | 5 | 9% | 45–53 live resources each with no recorded apply. |
| Auto-apply enabled | 1 | 2% | Only `global-version-manager`. Everything else is manual. |

A second organisation, `FITFILE`, exists on the same account but returned no workspaces.

---

### 2. Workspaces whose Last Apply Failed

| Workspace | Backing repo | Provider | Last run | Resources | Status |
|---|---|---|---|---|---|
| `hie-prod-35` | NO-VCS | Azure | 2026-07-30 | 144 | errored |
| `lca-prd-2` | `customers/nwsde/lca-infrastructure-prd` | Azure | 2026-04-13 | 73 | errored |
| `fitfile-entra-id` | `central-services` | Azure AD | 2026-04-15 | 68 | errored |
| `Gitlab` | `production/central-services` | GitLab | 2026-07-09 | 43 | errored |
| `uhb-prod-aks` | `customers/uhb-wmsde-prod` | Azure | 2026-04-15 | 27 | errored |
| `ff-central-private-acr` | `central-services` | Azure | 2026-04-15 | 11 | errored |
| `fitfile-production-primary-care` | `production/fitfile-production` | Azure | 2025-11-03 | 10 | errored |
| `nnuh-prod-1` | `customers/eoe/NNUH-DP` | Azure | 2026-08-18 | 52 | discarded |
| `mkuh-prd-4-test` | `customers/eoe/mkuh-prd-4` | Azure | 2026-08-19 | 0 | errored |
| `sandbox-testing-2` / `-4` | `customers/sandbox-testing-1` | Azure | 2026-07 |—| errored |

Production customer environments are affected. `hie-prod-35` (144 resources) has been failing since 2026-07-30; `lca-prd-2` (73 resources) since 2026-04-13.

The `ff-central-private-acr` failure is directly relevant to [[FITFILE Audit - ACR and Identity]]: the workspace that should manage registry configuration has not applied successfully since April, consistent with the registry's drifted settings.

`fitfile-entra-id`—68 identity resources—has also been failing since April.

---

### 3. Healthy Workspaces (Most rEcent aPplies)

| Workspace | Last run | Source |
|---|---|---|
| `staging-cluster-v2` | 2026-08-27 applied | tfe-configuration-version |
| `aws-sb-test-1-cgw` | 2026-08-27 applied | terraform+cloud |
| `aws-sandbox-testing-1` | 2026-08-26 applied | terraform+cloud |
| `hcp-vault` | 2026-08-24 applied | tfe-configuration-version |
| `auth0-prod` / `auth0-non-prod` / `grafana` / `global-version-manager` | 2026-08-21 applied | mixed |
| `prod-1-cluster` / `mkuh-prd-4` / `test-cluster` | 2026-08-18 applied | mixed |

`hcp-vault` holds 1,047 resources in a single workspace—a large blast radius for one apply.

---

### 4. Module Inventory

Fourteen modules present locally. Only three declare a `cloud {}` block; the rest are correctly backend-free reusable modules.

| Module | Providers | Backend |
|---|---|---|
| `terraform-azure-private-infrastructure` | `azurerm` | `cloud {}` |
| `fitfile-version-manager` |—| `cloud {}` |
| `vault` | `vault` | `cloud {}` |
| `terraform-fitfile-central-services-consumer` | `auth0, azurerm, cloudflare, gitlab, grafana, tfe, vault` | module |
| `terraform-fitfile-unified-deployment` | `auth0, gitlab, tfe` | module |
| `terraform-aws-private-infrastructure` | `aws, random, tls` | module |
| `terraform-azure-database-servers` | `azurerm` | module |
| `terraform-azure-aks-backup` | `azurerm` | module |
| `terraform-azure-public-infrastructure` | `azurerm` | module |
| `terraform-helm-fitfile-platform` | `helm, kubectl, kubernetes` | module |
| `terraform-auth0-tenant` / `-fitfile-auth0-consumer` | `auth0` | module |
| `terraform-argo-argocd`, `platform-defaults`, `terraform-azure-aks-automation` | none declared | module |

A `cloud {}` block inside `terraform-azure-private-infrastructure` is unusual for a module—worth confirming it is not consumed as a child module anywhere, since a module carrying its own backend cannot be reused cleanly.

---

### 5. AWS Vs Azure Split

Azure is the delivery platform for all customer and FitFile-run environments. AWS appears only in sandbox and experimental workspaces—`aws-sandbox-testing-1`, `aws-sandbox-testing-1-platform`, `aws-sb-test-1-cgw`, `eks-private-sandbox`, `terraform-aws-eks-private`—plus the `terraform-aws-private-infrastructure` and `terraform-aws-eks` modules.

No production AWS workload was found. The AWS modules are exploratory, not a second production estate.

---

### 6. Local State Files

49 `.tfstate` files exist under the local repo root, including for production customer environments. Terraform state stores provider attributes in plaintext. Full finding as S-06 in [[FITFILE Audit - Security Findings and Remediation]].

```
Deployment/Clusters/nwsde/fitfile-bootstrap/terraform.tfstate
  72K · serial=86 · 23 resources · modified 2025-12-18
  sensitive attribute keys present: client_secret, encryption_key,
  import_url_password, allowed_managed_keys, audit_non_hmac_request_keys

Deployment/terraform-sandbox-state/terraform.tfstate
  136K · serial=76 · 16 resources · modified 2026-07-09
  sensitive attribute keys present: repository_password, image_pull_secret,
  secret, keyring, repository_key_file

Deployment/Clusters/nwsde/Production/LCA-DP/terraform.tfstate  → 0 bytes (empty)
```

Only attribute _names_ were enumerated; no values read.

---

### 7. The `-platform` Workspaces Bootstrap ArgoCD, not just Helm

Several customers have a second workspace alongside their infra one—`nnuh-prod-1-platform`, `mkuh-prd-4-platform`, `cuh-prod-1-platform`, `hie-prod-34-platform`—all `never-run` per the TFC API despite holding 46–53 resources each. These are the ArgoCD-bootstrap layer: Terraform installs ArgoCD into the customer's cluster via the `terraform-argo-argocd` module, seeded with the same `deployment.git` app-of-apps that staging and production use, tracking a customer-specific tag. Confirmed directly with the platform owner—see [[FITFILE Audit - AKS and ArgoCD Topology]] §2 for the full mechanism. LCA and MCNFT have no matching `-platform` workspace in the enumerated 54; not established whether they bootstrap differently or the platform layer sits inside their main workspace.

---

### Related

- [[FITFILE Delivery Pipeline Audit 2026-08-27]]—hub
- [[FITFILE Audit - ACR and Identity]] · [[FITFILE Audit - AKS and ArgoCD Topology]]
- [[Tickets for GitOps Azure Tenant Management with Terraform]]
- [[FTFL-799_Unified_Customer_Cloud_Permissions]]
