---
aliases: [Azure Architecture, Azure Resource Manager, ARM Architecture]
created: 2025-12-10T13:06:37Z
last_reviewed: "2026-03-28"
modified: 2026-03-28T15:40:00+00:00
status: evergreen
tags: [azure, architecture, arm, governance, security, sot]
title: SoT - Azure Resource Manager Architecture
type: SoT
---

## Minimum Viable Understanding (MVU)

Azure Resource Manager (ARM) is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account. FITFILE utilizes a strictly governed ARM structure based on Management Groups and Subscription Vending to ensure tenant isolation and policy enforcement.

---

## Working Knowledge

### 1. Global Naming Convention (The Guardian Protocol)

To ensure consistency and prevent resource collision, FITFILE enforces a strict naming convention.

#### Long Name Pattern (Standard)
`${resource_type}-${workload}-${subscription_purpose}-${region}-${index}`
- **Delimiter**: Hyphens `-`
- **Casing**: Lowercase only.
- **Example**: `vnet-hroracle-plat-uks-01`

#### Short Name Pattern (Constraints)
Used for resources with length limits (Storage Accounts, VMs, Scale Sets).
`${resource_type}${workload}${index}`
- **Delimiter**: None.
- **Example**: `stitsvcavd01`, `vmlcajmp01`

#### Components
| Component | Values |
|:---|:---|
| `subscription_purpose` | `plat` (Platform), `alzp` (App LZ Prod), `alzd` (App LZ Dev), `sand` (Sandbox) |
| `region` | `uks` (UK South), `ukw` (UK West), `glo` (Global) |
| `env` | `prd` (Production), `uat` (Pre-prod), `dev` (Development) |

### 2. Resource-Specific Templates

| Resource | Template | Example |
|:---|:---|:---|
| Resource Group | `rg-${workload}-${purpose}-${index}` | `rg-lca-prd-net` |
| VNet | `vnet-${workload}-${purpose}-${region}-${index}` | `vnet-lca-plat-uks-01` |
| Subnet | `snet-${workload}-${region}-${env}-${index}` | `snet-lca-uks-prd-system` |
| NSG | `nsg-${workload}-${region}-${index}` | `nsg-lca-uks-01` |

---

## Security & Governance (NCSC CAF Audit)

A 2026 security review identified systemic weaknesses that ARM architecture must now mitigate via policy and structure.

### 1. Identity & Access Control (CAF Principle B2)
- **MFA Enforcement**: All human and contractor accounts (Global Admins) MUST have phishing-resistant MFA.
- **Least Privilege**: Terraform Service Principals must not hold `Owner` equivalent permissions. Use scoped `Contributor` roles + `User Access Administrator` only where required.
- **PIM Activation**: Convert permanent Global Admin assignments to Privileged Identity Management (PIM) eligible roles.

### 2. Network Security (CAF Principle B5)
- **NSG vs Hub Firewall**: An NSG is a Layer 4 ACL, not a boundary firewall. For **Special Category Data** (GDPR Art 9), Layer 7 / WAF (Azure Hub Firewall) is **mandatory**.
- **The Trusted Source Fallacy**: Restricting an NSG to a single trusted IP is insufficient. It does not protect against application-layer exploits or compromised source systems.
- **Egress Lockdown**: "Allow-All-Outbound" is prohibited. NSGs must be filtered to allow egress only to required destinations.

### 3. Data Protection (CAF Principle B3)
- **Encryption at Rest**: All disks must use Customer-Managed Keys (CMK) or host-level encryption.
- **Infrastructure Backup**: Critical VMs (Jumpboxes) must be protected by Azure Backup.

---

## Current Understanding

### Known Anti-Patterns
- **Local Accounts**: Local accounts on AKS or Jumpboxes allow bypassing Entra ID RBAC. Always enforce Entra ID-based authentication.
- **Diagnostic Gaps**: Failure to register `microsoft.insights` results in zero observability. All subscriptions must export Activity Logs to a central Log Analytics workspace.
- **Stale Credentials**: Abandoned CLI tools and duplicate SP registrations must be audited quarterly.

## Related Documentation
- [[SoT - Cloud Networking Principles]]
- [[SoT - Microsoft Entra Application Model]]
- [[NSG-vs-Hub-Firewall-Security-Analysis]]
