---
aliases: ["NHS Compliance", "DSPT", "NHS England Blueprints"]
created: 2026-04-05T10:45:00Z
last_reviewed: 
modified: 2026-04-05T10:45:00Z
status: "Active"
tags: ["compliance", "nhs", "healthcare", "iam", "sot"]
title: SoT - NHS Identity Compliance
type: "SoT"
synthesis-count: 1
last-synthesis: 2026-04-05
---

## Minimum Viable Understanding (MVU)
NHS Identity Compliance requires a "multi-factor, time-locked system" to protect sensitive patient data (PHI). Compliance is primarily measured against the **NHS Data Security and Protection Toolkit (DSPT)** and UK GDPR.

---

## 1. Core Mandatory Protections

To handle NHS patient data securely, organizations must implement:
- **Zero Standing Privileges:** Admin access must be Just-in-Time (JIT) through Privileged Identity Management (PIM).
- **Mandatory MFA:** Multi-Factor Authentication for all users, especially those with privileged access.
- **Private Connectivity:** Use **Azure Private Link** for all NHS data services to prevent public exposure.
- **NHS England Blueprints:** Enforce organizational standards using **Azure Policy** with NHS England-specific blueprints.
- **Confidential Computing:** Utilize **Azure Confidential Computing** for processing Protected Health Information (PHI) in isolated enclaves.
- **Data Anonymization:** Use NHS Privacy Enhancing Technology (PET) patterns to ensure data minimization.

---

## 2. DSPT Control Mapping

| DSPT Requirement | Azure Feature Mapping |
| :--- | :--- |
| **AC1.1.3 Privileged Access Management (PAM)** | Privileged Identity Management (PIM) |
| **AC1.1.4 Multi-Factor Authentication (MFA)** | Conditional Access Policies with MFA |
| **IM1.1.1 Security Monitoring & Alerting** | Azure AD Identity Protection, Azure Sentinel |
| **AC1.1.5 Access Review Processes** | Azure AD Access Reviews |

---

## 3. Auditing & Monitoring Requirements

### A. Centralized Logging
- **Log Analytics Workspace:** Must collect Azure Activity Logs, Entra ID Sign-In Logs, and Key Vault Access Logs.
- **Azure Sentinel:** Used for proactive threat hunting and real-time alerts.

### B. Proactive Threat Detection
Use Kusto queries to detect high-risk sign-ins:
```kusto
AADSignInEvents 
| where RiskLevelDuringSignIn == "high"
| where UserType == "Member"
```

### C. Continuous Governance
- **Weekly Access Reviews:** Documented in NHS Data Protection Impact Assessments (DPIA).
- **NHS England Data Tagging:** Enforce strict tagging of all resources containing NHS data to ensure consistent policy application.

---

## Related Knowledge
- [[SoT - Microsoft Entra Identity]]
- [[SoT - Zero Trust Architecture]]
- [[SoT - NIST Cybersecurity Framework]]
