---
created: 2026-04-29T12:26:15+00:00
modified: 2026-04-29T12:29:25+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 1:26 PM*
---
Here is a detailed, structured summary of the Azure Backup for AKS configuration and testing process. It is formatted to be directly copied and pasted into Jira (likely for [FTFL-599](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-599.md) or [FTFL-596](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-596.md)).

***

### **Testing Summary: Azure Backup for AKS Configuration**

**Environment:** `aks-ff-uks-gp-1` (Pentest/Sandbox)
**Resource Group:** `pentest-1-backup-rg`
**Snapshot Resource Group:** `pentest-1-backup-snapshots-rg`
**Vault Name:** `aksbackupvault`
**Status:** ✅ **Success - Protection Configured**

#### **1. Objective & Outcomes**
Successfully validated the end-to-end CLI provisioning flow for Azure Backup on AKS. This establishes the exact infrastructure sequence, payload requirements, and RBAC permissions necessary to update our backup runbooks and prepare the Terraform modules for the EoE Data Providers (NNUH & MKUH).

**Final State:** 
The backup instance (`aks-ff-uks-gp-1-backup`) was successfully created, and Azure has completed asynchronous setup.
*   **Provisioning State:** `Succeeded`
*   **Protection State:** `ProtectionConfigured`
*   **Targeted Namespaces:** `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`, `thehyve`, `thehyve-cuh`, `thehyve-mkuh`
*   **Policy Attached:** `dailyaksbackups` (Ad-hoc rule: `BackupDaily`)

#### **2. Execution Timeline & Blockers Resolved**
During testing, we identified and resolved three critical configuration blockers that must be reflected in our IaC/runbooks moving forward:

*   **11:51 AM - AKS Backup Extension:** Installed `azure-aks-backup` successfully.
*   **12:31 PM - Payload Generation (Blocker 1 - JSON Shape):** Hand-crafted JSON for the `--backup-instance` payload fails due to missing `DatasourceSet` objects. **Resolution:** We must use `az dataprotection backup-instance initialize-backupconfig` (with `--included-namespaces`) and `initialize` to dynamically generate the correct payload before validation.
*   **12:50 PM - Snapshot RBAC (Blocker 2 - Missing Permissions):** Validation failed due to missing permissions on the snapshot resource group. **Resolution:** Verified the exact role assignments required:
    *   **AKS Cluster Managed Identity** requires `Contributor` on the Snapshot RG.
    *   **Backup Vault Managed Identity** requires `Reader` (or `Contributor`) on the Snapshot RG.
    *   **Extension MSI** requires `Storage Blob Data Contributor` on the target Storage Account (`stffuksgp1backup`).
*   **1:12 PM - Trusted Access Binding (Blocker 3 - AKS/Vault Trust):** Validation rejected due to missing Trusted Access role bindings between the cluster and the vault. **Resolution:** Created the binding successfully using strict naming rules:
    *   *Binding Name Constraint:* Must be under 24 characters (used `azbkup-trust`).
    *   *Role Constraint:* Must use the fully qualified source resource type: `Microsoft.DataProtection/backupVaults/backup-operator`.
*   **1:21 PM - Instance Creation:** Executed `az dataprotection backup-instance create`. The instance transitioned from `ConfiguringProtection` to `ProtectionConfigured`.

#### **3. Next Steps for Implementation**
1.  **Runbook Update:** Update the Azure Backup restore runbook (FTFL-599) with the verified `az dataprotection` CLI command sequences for initializing config, validating, and checking job status.
2.  **IaC / Terraform (FTFL-596 & FTFL-615):** Ensure our Terraform modules programmatically handle the three dependencies identified above: 
    *   Storage/Snapshot RG role assignments for the Vault, AKS, and Extension MSIs.
    *   The Trusted Access Role Binding resource.
    *   The private endpoint subnet for the storage container.
