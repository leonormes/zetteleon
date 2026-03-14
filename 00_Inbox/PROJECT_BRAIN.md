---
created: 2026-01-12T16:39:57+00:00
modified: 2026-03-14T11:10:52+00:00
title: PROJECT_BRAIN
---

## 🧠 PROJECT_BRAIN.md: Multi-Repo Orchestration

> SYSTEM INSTRUCTION FOR LLM: This file is the Single Source of Truth.
> Before writing code, you must read this file to establish the "Golden Thread" of context.
> Last Updated: 12 Jan 2026

---

### 🧩 1. The Generative Engine (Core Inputs)

Rule: You are FORBIDDEN from creating hardcoded variables for names, locations, or IP ranges. You must derive them from `customer.yaml` using `locals.tf`.

The Only Manual Inputs (customer.yaml):

- `customer_name` (e.g., `acme`)
- `environment` (e.g., `prod`)
- `region` (e.g., `uk-south`)
- `instance_id` (e.g., `001`)
- `vnet_address_space` (e.g., `10.0.0.0/16`)

Derivation Logic (The "Math"):

- Prefix: `${customer_name}-${environment}-${instance_id}`
- VNET CIDR: `${vnet_address_space}`
- Vault Path: `secret/data/${customer_name}/${environment}/*`
- Tags: Must include `ManagedBy = Terraform`, `Customer = ${customer_name}`.

---

### 📐 2. Gold Master Topology Constraints

Reference: Legacy `CONTEXT.md` (Index 200).

- Subnet Offset Rule:
  - System Subnet is at `Base_IP + 0` (Index 0).
  - App Subnet is at `Base_IP + 32` (Index 2).
- LB IP Rule: Load Balancer IP is `Subnet_Start + 8`.
- Mandatory Egress: System, Jumpbox, and Workflow subnets must bind to the NAT Gateway.
- Identity: The AKS Cluster must use the `User Assigned Identity` created in Stage 1.

---

### 🏗️ 3. Infrastructure Dependency Map

_This maps how data flows between your repositories._

| Stage | Repository | Purpose | Key Output -> Input |
|:--- |:--- |:--- |:--- |
| 1 | `infra-bootstrap` | GitLab Repo, TFC Workspace | Output `tfc_workspace_id` -> Stage 2 |
| 2 | `infra-security` | Vault Policies, AppRoles | Output `vault_role_id` -> Stage 3 |
| 3 | `infra-aks` | Managed AKS, VNET | Output `kube_config` -> Stage 4 |
| 4 | `infra-services` | Helm Charts, K8s Resources | Consumes all previous outputs |

---

### 📊 4. Knowledge Confidence Audit

_LLM: Before answering, rate your understanding of the current task (1-10). If <9, ask for the missing file referenced below._

| Category | Score | Notes / Missing Info |
|:--- |:--- |:--- |
| Architectural Flow | 10/10 | Fully understands the 4-stage deployment logic. |
| Generative Strategy | 10/10 | ACTIVE: Now driven by `customer.yaml`. |
| Gold Master Rules | 10/10 | Resolved: Validated System (+0) and App (+32) logic. |
| Active Resource IDs | 8/10 | Synchronized with current deployment state. |
| Vault Auth Logic | 5/10 | Next step: Implement AppRole/Kubernetes Auth handshake. |

---

### 🚧 5. Current Focus & Context Token

_Copy this token to warm up a new chat session._

> Context Token: Documentation is now synced with Code. Last Action: Verified that locals.tf correctly implements System at Index 0. Next Session Goal: Execute the report.py refactor to remove hardcoded strings and fully implement the Generative Engine in our audit scripts.

---

### 📝 6. Breadcrumbs (Session Log)

_One-line summary of "Definition of Done" for recent tasks._

- [2026-01-12] Initialised `PROJECT_BRAIN.md` and established Generative Logic rules.
- [2026-01-12] Defined Gold Master topology (Offset +32) to ensure deterministic networking.
- [2026-01-12] REFACTOR COMPLETE: Implemented `customer.yaml` ingestion and removed all hardcoded customer locals.
- [2026-01-12] Verified Code is Source of Truth (System @ 0). Aligned Brain and Context files to match reality.

### 🏁 7. Codebase Topology Snapshot

_Last generated: 2026-01-12_

- Engine: `customer.yaml` -> `locals.tf` (yamldecode)
- Identity: `instance_id: 2`
- VNET: `10.0.0.0/16` (Explicitly managed)

### ✅ Gold Master Verification (Definition of Done)

#### Wiring Constraints

> CRITICAL: `azurerm_subnet_nat_gateway_association` resources must be defined at the Root Module, not inside the subnets module.

#### Resource Inventory (Legacy Snapshot)

_Use this inventory to validate refactors. If a refactor removes one of these resources, it is likely a regression._

##### A. Root Level (Wiring & Data)

- `azurerm_subnet.bastion`
- `azurerm_subnet_nat_gateway_association.jumpbox`
- `azurerm_subnet_nat_gateway_association.system`
- `azurerm_subnet_nat_gateway_association.workflows`

##### B. Module: aks_backup (Compliance Layer)

- `module.aks_backup.azurerm_data_protection_backup_instance_kubernetes_cluster.backup_instance`
- `module.aks_backup.azurerm_data_protection_backup_policy_kubernetes_cluster.backup_policy`
- `module.aks_backup.azurerm_data_protection_backup_vault.backup_vault`
- `module.aks_backup.azurerm_kubernetes_cluster_extension.backup_extension`
- `module.aks_backup.azurerm_kubernetes_cluster_trusted_access_role_binding.aks_cluster_trusted_access`
- `module.aks_backup.azurerm_resource_group.backup_rg`
- `module.aks_backup.azurerm_resource_group.backup_rg_snap`
- `module.aks_backup.azurerm_role_assignment.test_cluster_msi_contributor_on_snap_rg`
- `module.aks_backup.azurerm_role_assignment.test_extension_and_storage_account_permission`
- `module.aks_backup.azurerm_role_assignment.test_vault_data_contributor_on_storage`
- `module.aks_backup.azurerm_role_assignment.test_vault_data_operator_on_snap_rg`
- `module.aks_backup.azurerm_role_assignment.test_vault_msi_read_on_cluster`
- `module.aks_backup.azurerm_role_assignment.test_vault_msi_read_on_snap_rg`
- `module.aks_backup.azurerm_role_assignment.test_vault_msi_snapshot_contributor_on_snap_rg`
- `module.aks_backup.azurerm_storage_account.backup_sa`
- `module.aks_backup.azurerm_storage_container.backup_container`

##### C. Module: Private-infrastructure (Core Compute & Network)

- `module.private-infrastructure.module.FITFILEJumpbox.azurerm_linux_virtual_machine.virtual_machine`
- `module.private-infrastructure.module.FITFILEJumpbox.azurerm_network_interface.nic`
- `module.private-infrastructure.module.FITFILEJumpbox.azurerm_network_security_group.nsg`
- `module.private-infrastructure.module.aks_cluster.azurerm_kubernetes_cluster.aks_cluster`
- `module.private-infrastructure.module.aks_cluster.azurerm_role_assignment.cluster_network_contributor`
- `module.private-infrastructure.module.aks_cluster.azurerm_user_assigned_identity.aks_identity`
- `module.private-infrastructure.module.aks_network.azurerm_subnet.subnet["snet-ff-uks-gp-system"]`
- `module.private-infrastructure.module.system_nsg.azurerm_network_security_group.nsg`
- `module.private-infrastructure.module.workflows_nsg.azurerm_network_security_group.nsg`
