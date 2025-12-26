---
aliases: ["FITFILE Azure Org Structure", "Azure Management Groups"]
confidence: "5/5"
created: 2025-10-20T14:05:09Z
epistemic: "fact"
last_reviewed: "2025-12-26"
modified: 2025-12-26T18:03:41+00:00
purpose: "To define the definitive Azure resource organization (Management Groups & Subscriptions) for FITFILE."
review_interval: "3 months"
see_also: ["[[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: []
status: "stable"
tags: ["azure", "governance", "architecture", "fitfile", "sot"]
title: SoT - FitFile Deployment - Azure Organization Architecture
type: "SoT"
uid: 
updated: 
---

## 1. Overview & Hierarchy

This document defines the **Enterprise-Scale Landing Zone** pattern used for FITFILE's Azure tenant. It adheres to Microsoft's recommended practices for governance, security, and operational efficiency.

**Tenant Root:** `45e73aa3-1ee9-47c0-ba25-54eda9da021a`

### Visual Hierarchy

```mermaid
graph TD
    A[Tenant Root Group] --> B[FITFILE Management Group]
    B --> C[Landing Zones (LANDING-ZONES)]
    B --> D[Platform (PLATFORM)]

    C --> E[FITCloud Production]
    C --> F[FITCloud Non-Production]

    D --> G[Identity]
    D --> H[Management]
    D --> I[Shared Services]

    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
    style D fill:#bfb,stroke:#333
```

---

## 2. Management Groups & Subscriptions

### Level 1: Landing Zones (Workloads)

Container for application environments.

- **Path:** `Tenant Root -> FITFILE -> Landing Zones`
- **Access:** Reader (Inherited)

| Subscription | Environment | ID | Purpose |
|:--- |:--- |:--- |:--- |
| **FITCloud Production** | Production | `a448d869-4ec5-4c81-82c5-d6e8fa0ec0df` | Customer-facing applications. |
| **FITCloud Non-Production** | Non-Production | `249df46b-f75d-4492-8e78-b33a00473548` | Dev, Test, Staging. |

### Level 2: Platform (Shared Services)

Container for core infrastructure and governance.

- **Path:** `Tenant Root -> FITFILE -> Platform`
- **Access:** Reader (Inherited)

| Subscription | Environment | ID | Purpose |
|:--- |:--- |:--- |:--- |
| **Identity** | Platform | `c1c459c8-a99f-4f7a-891b-a98d49cf12c0` | IAM, AD Connect, PKI. |
| **Management** | Platform | `a9602426-e496-44d1-ba89-8e5fc756a06b` | Monitoring, Logging, Backup. |
| **Shared Services** | Platform | `a085dd04-19aa-4d2b-9a35-e438097d84fc` | DNS, Networking Hub. |

---

## 3. Governance & Access Control (RBAC)

### 3.1 Scope Model

Permissions are applied via **Inheritance**:

`Tenant Root` -> `Management Group` -> `Subscription` -> `Resource Group`

### 3.2 Access Policies

- **Least Privilege:** Default access is `Reader`.
- **Production Access:** Requires specific Operations Manager approval.
- **Emergency:** "Break-glass" procedures for elevated access.

### 3.3 Cost Allocation

- **Production:** Allocated to Customer COGS.
- **Non-Production:** Allocated to R&D.
- **Platform:** Shared overhead.

---

## 4. Key Design Decisions

1. **Environment Separation:** Strict isolation between `Production` and `Non-Production` to prevent accidental impact.
2. **Centralized Platform:** Shared services (DNS, Identity) are decoupled from workloads to improve consistency.
3. **Policy Inheritance:** Governance rules (tags, regions, security) are applied at the `Management Group` level for uniform enforcement.

---

## 5. Maintenance & Data Source

- **Source:** Generated via `az account management-group list`
- **Last Verification:** Oct 2024
- **Owner:** Platform Engineering Team
