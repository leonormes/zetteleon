---
tags:
- axiom:FTFL-799
- infrastructure/azure
- permissions
- terraform
- typed-edge
permalink: llmeon/30-library/ftfl-799-azure-phase2-permissions-inventory
---

# FTFL-799: Azure Phase 2 — Terraform SP & Developer Permissions Inventory

**Status**: Phase 2 complete (Azure). Phase 3 (unified doc) next.
**Evidence base**: Azure CLI (tenant `fitfile.com`, 8 visible subscriptions), Terraform (`central-services`, `terraform-azure-private-infrastructure`), Confluence (3 overlapping permission docs), git history.
**Companion doc**: [[FTFL-799_AWS_Phase1_Permissions_Inventory]]

---

## Key finding up front: three Confluence docs disagree, and the most authoritative one isn't the most prominent one

I found three separate Azure permission pages, and their custom-role JSON is **not the same document copy-pasted around** — each is a different snapshot:

| Doc | Last modified | Completeness |
|---|---|---|
| "Deployment Permissions" | Jul 9, 2025 | Itemized actions (Compute/Network/ManagedIdentity/ContainerService/Resources/OperationalInsights) + separate section on the **AKS cluster's own managed identity** permissions |
| "Azure Permissions for Private AKS Deployment via Terraform" | Nov 24, 2025 | Cleanest presentation (role/scope/reason table + troubleshooting) but **narrowest** action list — missing Key Vault, Log Analytics, Insights, RouteTables, Routes, LoadBalancers |
| **"Node Installation - Azure Account/Subscription setup"** | **Feb 16, 2026** | **Most complete** — includes everything above plus `Microsoft.KeyVault/*`, `Microsoft.OperationalInsights/workspaces/*`, `Microsoft.Insights/diagnosticSettings/*`, `roleDefinitions/read`, `routeTables/*`, `routes/*`, `loadBalancers/*` |

**Use the Feb 2026 doc's role definition as the baseline for the unified deliverable** — it's the most recent and the most complete, despite not having "Permissions" in the title (which is likely why it's hard to find via search).

Additionally: **the live Terraform test copy of this role in `central-services/azure/ad/main.tf` (`azurerm_role_definition.private_aks`, scoped to the non-prod subscription) is itself a subset of the Feb 2026 doc** — missing the same Key Vault/Insights/RouteTables/LoadBalancers actions. FITFILE's own internal reference/validation environment hasn't been synced to the latest documented requirements.

---

## Table B1: Azure Terraform SP

**App registration**: "FITFILE Terraform Cloud Provisioner" (per-customer, created by the customer in their own tenant, single-tenant)
**Auth method**: **Client secret** — confirmed via the live customer setup guide (Node Installation - Azure Account/Subscription setup). This is *not* OIDC, unlike the AWS side.

> ⚠️ Contrast with AWS: AWS's `tfc-role` uses OIDC federation with **no static keys** (Table A1 in the AWS doc). Azure customers are still instructed to generate and hand over a **client secret**. FITFILE does have an OIDC example (`Tools/terraform-dynamic-credentials-setup-examples/azure/`) and several `tfc-application` App registrations exist live in the tenant (created 2023–2024) suggesting OIDC has been *tested*, but the live, current customer-facing instructions still use client secret. **Recommend migrating Azure to the same OIDC pattern as AWS** for FTFL-799 — reduces standing secret exposure and would resolve an inconsistency between the two cloud onboarding experiences.

### Permissions granted to the customer's SP

| Permission | Scope | Purpose | Source |
|---|---|---|---|
| `Contributor` (built-in) | Subscription | Deploy AKS, disks, VMs, storage, networking | Live customer setup guide (step-by-step walkthrough) |
| `User Access Administrator` **with a condition constraining it to only assign "Network Contributor"** | Subscription | Lets the SP assign Network Contributor to the AKS cluster's own managed identity, without granting the SP the ability to assign *any* role to *any* principal | Live customer setup guide — **this is exactly the least-privilege "constrained role-assignment" pattern the brief asked to look for, and it's already in production use** |
| Resource provider registrations: `Microsoft.ContainerService`, `Microsoft.ManagedIdentity`, `Microsoft.Network`, `Microsoft.Storage`, `Microsoft.Compute` | Subscription | Required before AKS/networking/storage/compute resources can be created | Live customer setup guide |
| `EncryptionAtHost` feature flag | Subscription (`Microsoft.Compute` namespace) | Enables host-level encryption for VM/AKS node disks | Live customer setup guide |
| Custom role `private-aks-provisioner` (alternative to blanket Contributor) | Subscription | See full action list below | Feb 2026 doc (most complete) |

**Full custom-role action list (Feb 2026 doc — canonical, most complete version found):**
```
Microsoft.Authorization/roleAssignments/*
Microsoft.Authorization/roleDefinitions/read
Microsoft.Compute/disks/*
Microsoft.Compute/virtualMachines/*
Microsoft.ContainerService/managedClusters/*
Microsoft.ManagedIdentity/userAssignedIdentities/*
Microsoft.Network/networkInterfaces/*
Microsoft.Network/networkSecurityGroups/*
Microsoft.Network/privateDnsZones/*
Microsoft.Network/publicIPAddresses/*
Microsoft.Network/virtualNetworks/*
Microsoft.Network/routeTables/*
Microsoft.Network/routes/*
Microsoft.Network/loadBalancers/*
Microsoft.Resources/subscriptions/providers/read
Microsoft.Resources/subscriptions/resourcegroups/*
Microsoft.Resources/subscriptions/resourcegroups/resources/read
Microsoft.OperationalInsights/workspaces/*
Microsoft.Insights/diagnosticSettings/*
Microsoft.KeyVault/vaults/read
Microsoft.KeyVault/vaults/accessPolicies/*
Microsoft.KeyVault/vaults/secrets/*
Microsoft.Resources/subscriptions/locations/read
Microsoft.Resources/providers/read
```

⚠️ **Internal inconsistency within the same Confluence page**: the step-by-step walkthrough tells the customer to grant blanket subscription **Contributor**, while the code block at the bottom of the *same page* offers this much narrower **custom role** as an apparent alternative. The two are never reconciled — the doc doesn't say which one FITFILE actually recommends. Needs a decision before the unified pack goes out.

### Live custom roles found (FITFILE's own non-prod subscription, `249df46b-f75d-4492-8e78-b33a00473548`)
```
ResourceGroupManager
RoleAssignmentProvisioner
AKSProvisioner
AKSPowerManager
private-aks-provisioner   ← the test copy of the customer role, now stale (see above)
hub-provisioner
```
The existence of separate `RoleAssignmentProvisioner` and `AKSProvisioner` roles suggests FITFILE's own internal landing zone already uses a **more granular split** than the single blanket role given to customers — worth reviewing as a possible better least-privilege template for the customer-facing doc, though I did not pull their full action lists this session (**UNVERIFIED — pull via `az role definition list --name <role> --scope /subscriptions/249df46b-f75d-4492-8e78-b33a00473548`**).

Live custom roles in Shared Services subscription (`a085dd04-19aa-4d2b-9a35-e438097d84fc`): `SharedServicesProvisioner`, `Resource group Locker`, `AcrImport` — internal only, not customer-facing.

---

## Table B2: Role assignments the Azure SP must create

| Target identity | Role assigned | Scope | Why |
|---|---|---|---|
| AKS cluster's own user-assigned managed identity (`azurerm_user_assigned_identity.aks_identity`) | Network Contributor | Target resource group | AKS identity needs to manage LBs/NICs/route tables in the VNet — live Terraform: `azurerm_role_assignment.cluster_network_contributor` in `modules/aks/main.tf` |
| Same AKS identity | Network Contributor | **VNet's own resource group**, only when the customer supplies a VNet in a separate RG (e.g. NNUH) | Live Terraform: `azurerm_role_assignment.vnet_network_contributor`, conditional on `var.vnet_resource_group_name != null` — confirmed via git commit `f291d33 FTFL-654 "Adding additional network contributor role needed by aks submodule for when the vnet is in a different group"` |
| AKS cluster's own managed identity (background/context, not a Terraform-created role assignment) | Operational permissions Azure/AKS itself expects: LoadBalancer config, Disk config, Storage account (AzureFile/AzureDisk), RouteTables, VM read/write, VM Scale Sets, NetworkInterfaces read, Snapshots | — | Documented in "Deployment Permissions" Confluence page, citing `azure-aks.pdf` — this is Azure's own AKS-identity requirement, not something FITFILE's Terraform explicitly grants beyond the single Network Contributor assignment above (Network Contributor is broad enough to cover it) |

---

## Table B3: Azure Developer permissions

| Role/Group | Type | Key actions | Used by | Notes |
|---|---|---|---|---|
| FITFILE DevOps human user | Entra guest/member user, **Contributor @ subscription** | Full subscription Contributor | FITFILE engineers | Live customer setup guide has FITFILE invite a named engineer and grant **subscription-wide Contributor** — broader than AWS's per-instance-role model. Flag for least-privilege review. |
| Jumpbox VM login | `azurerm_linux_virtual_machine` (Ubuntu 22.04) — SSH public key **or** password (mutually exclusive via `disable_password_authentication`) | Direct OS-level login | FITFILE operators | **Materially different from AWS**: AWS jumpbox access is IAM+SSM (no local credentials at all); Azure jumpbox access is credential-based VM login, optionally fronted by Azure Bastion (per the newer "Node Installation - Infrastructure" guide's `bastion.tf`) for no-public-IP access |
| PIM (Privileged Identity Management) | Operational, not Terraform-codified | Eligible-role activation | FITFILE engineers accessing customer tenants | Documented as a manual step in "Node Installation - FITFILE Checklist" ("search PIM... Activate under Eligible assignments") — **no Terraform/live evidence gathered this session; UNVERIFIED** |
| Live cross-tenant guest access confirmed | `az account list` from my own session shows visibility into `NNUHFT-SDE` (subscription `4ae8fd93-d084-481f-ba6e-370b7d4d8d0d`, **separate tenant** `d2a06081-6719-4548-bdc7-fff8bfd24f56`) | — | Real evidence the "add FITFILE DevOps user to customer tenant" pattern is live in production for at least one real customer (NNUH) |
| "Infra Entra Users" GitLab project (`central-services/gitlab/infra_entra_users.tf`) | Pointer only | — | The actual Entra user/group Terraform resources live in a **separate GitLab repo** not cloned locally — could not inspect contents this session |

---

## 2C — Azure customer-facing narrative (draft)

1. **Before FITFILE deploys**, the customer creates (in their own tenant): an App registration + client secret ("FITFILE Terraform Cloud Provisioner"), grants it `Contributor` @ subscription, and grants `User Access Administrator` @ subscription **constrained by a role-assignment condition to "Network Contributor" only** — not blanket UAA. This condition pattern is the least-privilege approach already in production; lead with it in the customer pack rather than presenting blanket UAA as the default.
2. Registers 5 resource providers, enables the `EncryptionAtHost` feature, and requests an Esv5 vCPU quota increase (UK South by default).
3. **What FITFILE developers need from the customer**: a named Entra guest/member user with Contributor @ subscription, plus VM login credentials (SSH key preferred over password) to the jumpbox — optionally via Azure Bastion to avoid a public IP.
4. **Not required**: `Owner` @ subscription on an ongoing basis (only needed transiently by whoever performs the one-time setup steps); unconditional `User Access Administrator`.
5. **Recent additions (FTFL-799) — Azure has a gap, not a delta**: unlike AWS, there is **no AWS-Backup-equivalent implemented on Azure yet**. The `backup_vault_name` Terraform variable exists (`vars.tf`) but is **dead code** — never referenced by any resource (grep-confirmed). The newer "Node Installation - Infrastructure" Confluence guide shows an `aks_backup` module block explicitly **commented out** with "`<needs work!>`". **Azure private-cluster backup permissions cannot be documented yet because the feature doesn't exist in Terraform.** This needs to be called out explicitly — FTFL-799 may need a companion ticket to build the Azure backup module before this half of the customer pack can be completed.

---

## 2D — Azure verification checklist (commands run this session)

```bash
# Identity + subscription topology
az account show
az account list -o table
# => 8 subscriptions visible: FITCloud Production, FITCloud Non-Production, Shared Services,
#    Management, Identity, Testing (default), FitFile (separate tenant), NNUHFT-SDE (separate tenant, real customer)

# Known service principals
az ad sp list --display-name "Private AKS Provisioner" -o table
az ad sp list --display-name "tfc" -o table
az ad sp list --display-name "terraform" -o table

# Custom role definitions (MUST scope to the right subscription — default scope returns almost nothing)
az role definition list --custom-role-only true --scope /subscriptions/249df46b-f75d-4492-8e78-b33a00473548  # non-prod
az role definition list --custom-role-only true --scope /subscriptions/a085dd04-19aa-4d2b-9a35-e438097d84fc  # shared services

# Federated credentials (OIDC adoption check) — MUST use the Application's own object id, not the Service Principal's
az ad app federated-credential list --id <application-object-id>   # NOT the SP object id — this failed when I used the SP id

# AKS cluster identity (when a live cluster exists)
az aks show -g <rg> -n <cluster> --query identity

# EncryptionAtHost feature status
az feature show --namespace Microsoft.Compute --name EncryptionAtHost
```

---

## Gaps & Open Questions

1. **Which Azure permission model does FITFILE actually want to recommend?** Blanket Contributor (walkthrough) vs. the narrower `private-aks-provisioner` custom role (code block) — same Confluence page presents both without reconciling.
2. **Sync FITFILE's internal test copy** of the `private-aks-provisioner` role (`central-services/azure/ad/main.tf`) to match the more complete Feb-2026 documented version (Key Vault, OperationalInsights, Insights, RouteTables, Routes, LoadBalancers actions are all missing from the live Terraform copy).
3. **OIDC for Azure** — confirm whether any of the `tfc-application` App registrations are actually used with federated credentials in production, or whether they're abandoned experiments. Re-run the federated-credential check with the correct (Application, not SP) object id.
4. **`RoleAssignmentProvisioner` / `AKSProvisioner`** custom roles in the non-prod subscription — pull their full action lists; they may represent a better-factored least-privilege model than what's given to customers today.
5. **Azure Backup is not implemented** — confirm whether building it is in scope for FTFL-799 or needs a follow-up ticket. Until then, Azure customer discovery packs cannot include backup permissions (there's nothing to grant).
6. **PIM usage** — operationally documented but not Terraform-codified; no live evidence gathered.
7. **Human developer access is subscription-wide Contributor** — broader than AWS's per-instance jumpbox-role model. Worth a least-privilege pass (e.g., scope to resource group instead of subscription).

---

## Doctrine Notes

- **Auth asymmetry between clouds**: AWS = OIDC (no static keys, proven in production). Azure = client secret (static, standard practice today despite an existing OIDC example). This asymmetry should be resolved — recommend Azure adopt OIDC to match AWS.
- **Azure's UAA-with-condition pattern is the right model** — don't let the unified doc default to describing blanket `User Access Administrator`; the constrained-to-Network-Contributor condition is what's actually deployed and is the least-privilege story to tell customers.
- **Backup is asymmetric across clouds**: AWS has a working (if not-yet-Terraform-codified) implementation with fresh, still-evolving permissions (`aws-backup-role-policy` v1). Azure has **nothing built** — only a dead variable and a commented-out module block. The unified doc's "change log" section must not imply parity between the two clouds on this point.

---

**See also**: [[FTFL-799_AWS_Phase1_Permissions_Inventory]] · Jira FTFL-799 · Confluence "Deployment Permissions", "Azure Permissions for Private AKS Deployment via Terraform", "Node Installation - Azure Account/Subscription setup" (canonical baseline).

**Next**: Phase 3 — unified customer deliverable combining both clouds.