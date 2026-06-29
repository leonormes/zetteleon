---
tags:
- azure
- iam
- terraform
- fitfile
- central-services
date: 2026-05-30
source: terraform-central-services-repo
permalink: llmeon/wiki/2026-05-11-terraform-central-services-azure-iam
---

# Terraform Central Services — Azure IAM Current State
*Generated: 2026-05-11*

## Repo Overview
- **Root path**: `/Volumes/DAL/Fitfile/gitlab/FITFILE/central-services`
- **Provider versions**: azurerm, azuread (see `.terraform.lock.hcl` files per module)
- **Backend**: Terraform Cloud (FITFILE-Platforms organisation)
- **Workspaces**: `hcp-vault`, `gitlab`, `azure/ad`, `azure/acr`, `azure/sonarqube`
- **Applied by**: Terraform Cloud runners (organisation: FITFILE-Platforms)

## Directory Map
```
central-services/
├── azure/
│   ├── ad/           # Entra ID: users, groups, apps, service principals, role definitions
│   ├── acr/          # Container Registry + managed identities
│   └── sonarqube/    # SonarQube infrastructure
├── gitlab/           # GitLab Terraform configuration
├── Experiments/      # Sandbox/experimental modules
└── templates/        # Reusable templates
```

## Role Assignments
| Label | Principal | Role | Scope | File |
|-------|-----------|------|-------|------|
| `private_aks_assignment` | `private_aks_sp` | `private-aks-provisioner` (custom) | non_prod subscription | `azure/ad/main.tf:163` |
| `hub_provisioner_assignment` | `private_aks_sp` | `hub-provisioner` (custom) | non_prod subscription | `azure/ad/main.tf:169` |
| `vault_role_assignment` | `vault_sp` | `User Access Administrator` (built-in) | shared_services_sub | `azure/ad/main.tf:175` |
| `vault_acr_pull_assignment` | `vault_acr_pull_sp` | `AcrPull` (built-in) | shared_services_sub | `azure/ad/main.tf:198` |

## Custom Role Definitions
| Label | Name | Actions | Not-Actions | Assignable Scopes |
|-------|------|---------|-------------|-------------------|
| `private_aks` | `private-aks-provisioner` | AKS, VM, network, DNS, role assignments (20 actions) | `[]` | non_prod subscription |
| `hub_provisioner` | `hub-provisioner` | Network interfaces, NSGs, VNets, firewalls, route tables (10 actions) | `[]` | non_prod subscription |

### private-aks-provisioner Key Permissions
- `Microsoft.ContainerService/managedClusters/*`
- `Microsoft.Compute/virtualMachines/*`
- `Microsoft.Network/*` (interfaces, NSGs, VNets, private DNS)
- `Microsoft.Authorization/roleAssignments/*`
- `Microsoft.ManagedIdentity/userAssignedIdentities/*`

### hub-provisioner Key Permissions
- `Microsoft.Network/virtualNetworks/*`
- `Microsoft.Network/azureFirewalls/*`
- `Microsoft.Network/firewallPolicies/*`
- `Microsoft.Network/networkSecurityGroups/*`
- `Microsoft.Network/routeTables/*`

## Managed Identities
| Label | Name | Type | Resource Group | Used By |
|-------|------|------|----------------|---------|
| `acr_identity` | `FitfileregistryIdentity` | User-assigned | ACR RG | Azure Container Registry |
| `public_acr_identity` | `FITFILEPublicRegistryIdentity` | User-assigned | ACR RG | Public Azure Container Registry |

Both identities have `lifecycle { prevent_destroy = true }` protection.

## Azure AD Objects

### Service Principals
| Name | Purpose | Assigned Roles |
|------|---------|----------------|
| `vault_sp` | HCP Vault dedicated instance | User Access Administrator (shared_services_sub) |
| `vault_acr_pull_sp` | Vault Azure Secrets Engine dynamic credentials | AcrPull (shared_services_sub) |
| `private_aks_sp` | Private AKS provisioner testing | private-aks-provisioner, hub-provisioner (non_prod) |
| `argocd_non_prod` / `argocd_prod` | ArgoCD SSO authentication | None (group-based access) |
| `argo_workflows_non_prod` / `argo_workflows_prod` | Argo Workflows SSO authentication | None (group-based access) |
| `msgraph` | Microsoft Graph API access | N/A (well-known app) |

### Applications (App Registrations)
| Name | Description | Owners |
|------|-------------|--------|
| `vault_app` | HCP Vault access to central services | current user |
| `auth0_email_app_prod` | Auth0 M365 email provider (prod) | current user |
| `auth0_email_app` | Auth0 M365 email provider (non-prod) | current user |
| `private_aks_provisioner` | Testing private AKS provisioner role | current user |
| `vault_acr_pull_app` | Vault ACR pull dynamic credentials | vault_sp, current user |
| `argocd_non_prod` / `argocd_prod` | ArgoCD SSO | current user, oliver.rushton |
| `argo_workflows_non_prod` / `argo_workflows_prod` | Argo Workflows SSO | current user, oliver.rushton |

### Managed Users (7)
| UPN | Display Name | Job Title | Groups |
|-----|--------------|-----------|--------|
| `leon.ormes@fitfile.com` | Leon Ormes | Software Engineer | Developers, DevOpsEngineers, Argo/ArgoWf Admin |
| `oliver.rushton@fitfile.com` | Oliver Rushton | Senior Software Engineer | Developers, DevOpsEngineers, Argo/ArgoWf Admin |
| `enric.serra@fitfile.com` | Enric Serra | Senior Data Engineer | Developers, ArgoWf Admin |
| `pavlo.kotov@fitfile.com` | Pavlo Kotov | — | Developers |
| `yasir.mansoor@fitfile.com` | Yasir Mansoor | Senior Engineer | Developers |
| `gareth.hailes@fitfile.com` | Gareth Hailes | DevSecOps Engineer | DevOpsEngineers |
| `oliver.rushton_hotmail.co.uk#EXT#@fitfileltd.onmicrosoft.com` | Oliver Rushton (personal) | — | Developers (test) |

### Groups (12 total)
**Base Org Groups:**
- `Developers` — 6 members (all devs)
- `DevOpsEngineers` — 3 members (Leon, Oliver, Gareth)

**ArgoCD Groups:**
- `ArgoCD Non-Production Users` — Developers + DevOpsEngineers nested
- `ArgoCD Non-Production Admins` — Oliver, Leon
- `ArgoCD Production Users` — Developers + DevOpsEngineers nested
- `ArgoCD Production Admins` — Oliver, Leon

**Argo Workflows Groups:**
- `Argo Workflows Non-Production Users` — Developers + DevOpsEngineers nested
- `Argo Workflows Non-Production Admins` — Oliver, Leon, Enric
- `Argo Workflows Production Users` — Developers + DevOpsEngineers nested
- `Argo Workflows Production Admins` — Oliver, Leon, Enric

## Policy Assignments
**None identified.** No `azurerm_policy_assignment`, `azurerm_policy_definition`, or `azurerm_management_group_policy_assignment` resources found in the codebase.

## Variable Inputs & Remote State Dependencies
| Source | Purpose | Referenced By |
|--------|---------|---------------|
| `data.azurerm_subscription.shared_services_sub` | Shared services subscription (`a085dd04-...`) | vault_role_assignment, vault_acr_pull_assignment |
| `data.azurerm_subscription.non_prod` | Non-prod subscription (`249df46b-...`) | private_aks/hub_provisioner roles |
| `data.tfe_organization.fitfile_platform` | Terraform Cloud org: FITFILE-Platforms | hcp-vault workspace lookup |
| `data.tfe_workspace.hcp_vault_workspace` | HCP Vault workspace | — |
| `data.azuread_client_config.current` | Current tenant/user context | owners, tags, identity owner |

### tfvars Files
- `azure/ad/var.tfvars` — empty
- `gitlab/terraform.tfvars` — contains TODO placeholders for approver IDs
- Other tfvars in `Experiments/` and `templates/` not IAM-relevant

## Open Questions / Observations
1. **No policy assignments** — Azure Policy enforcement may be handled outside this repo (platform-level management groups)
2. **Broad custom roles** — `private-aks-provisioner` has wildcard permissions on AKS, VMs, and network resources at subscription scope
3. **Unresolved principal references** — All principal_ids resolved cleanly to local resources; no external dependencies
4. **Identities defined but never assigned Azure roles** — `acr_identity` and `public_acr_identity` have no `azurerm_role_assignment` in this repo (may be assigned elsewhere)
5. **Secret rotation commented out** — `time_rotating` for vault_sp_secret is commented; manual rotation currently
6. **CI/CD identity unknown** — Terraform Cloud runner identity not documented; likely uses OIDC or service principal stored in TF Cloud variables
7. **Production vs non-prod separation** — Only `non_prod` and `shared_services_sub` subscriptions referenced; production subscription not in this codebase

## Lock Files (Provider Versions)
- `azure/ad/.terraform.lock.hcl`
- `azure/acr/.terraform.lock.hcl`
- `azure/sonarqube/.terraform.lock.hcl`
- `gitlab/.terraform.lock.hcl`

(Exact provider versions require reading lock files — not extracted in this pass)

## Related

- [[SoT - Microsoft Entra Identity]] _Foundational reference for Azure AD / Entra ID identity concepts underpinning the IAM role assignments and service principals audited in this note._
- [[Workload Identity Governance]] _Governance framework for managing workload identities (managed identities, service principals) in Azure — directly relevant to the `private-aks-provisioner` and `hub-provisioner` managed identities configured by this Terraform codebase._
- [[SoT - Data-Centric IAM in Zero Trust]] _Zero Trust IAM architecture framework that contextualises the least-privilege RBAC model enforced through Terraform-managed custom role assignments._