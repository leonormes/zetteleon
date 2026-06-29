---
aliases:
- Azure AD
- Entra ID
- Microsoft Entra Identity
created: 2026-04-05 10:15:00+00:00
last-synthesis: 2026-04-05
last_reviewed: null
modified: 2026-05-26 11:44:18+00:00
status: Active
synthesis-count: 1
tags:
- azure
- iam
- security
- sot
title: SoT - Microsoft Entra Identity
type: SoT
permalink: llmeon/30-library/so-t/so-t-microsoft-entra-identity
---

## Minimum Viable Understanding (MVU)

Microsoft Entra ID (formerly Azure Active Directory) is a cloud-based identity and access management service that serves as the centralized authority for identities in the Microsoft ecosystem. It manages the lifecycle of identities (human and machine), verifies them through robust authentication (MFA, SSO), and enforces access policies through conditional signals.

---

## 1. Core Identity Functions

### A. Identity Management (Establishment)

- Registration & Creation: Generating digital identities and linking them to real-world entities. Entra ID supports a single identity for users across hybrid enterprises.
- Provisioning: Automating the creation, modification, and deletion of user accounts in SaaS applications (SCIM) and between on-premises AD and Entra ID.
- Attributes: Storing unique user/resource information (Roles, Department, Security Clearance) used for access decisions.

### B. Authentication (Verification)

Entra ID implements a "Never Trust, Always Verify" model using multiple methods:

- MFA (Multi-Factor Authentication): Enforces multiple verification steps (Phone, SMS, Mobile App, FIDO2 keys).
- Passwordless: Shifting to phishing-resistant methods like Windows Hello for Business, Microsoft Authenticator, and FIDO2 Security Keys.
- Federated Authentication: Integration with SAML, OIDC, and OAuth 2.0. Entra ID often acts as the Identity Provider (IdP).
- Managed Identities: Providing Azure services with an automatically managed identity to authenticate to Entra-supported services without storing credentials in code.

---

## 2. Advanced Security Features (Entra P2)

Upgrading to Entra P2 is critical for high-compliance environments (e.g., NHS patient data) due to:

| Feature | Function | Business Benefit |
|:--- |:--- |:--- |
| Privileged Identity Management (PIM) | Just-in-Time (JIT) access for admin roles. | Dramatically reduces the risk of "standing" privileged access. |
| Conditional Access (CA) | Risk-based, context-aware access policies. | Tailors security dynamically based on device health, location, and risk. |
| Identity Protection | Real-time threat detection via ML. | Proactively detects unusual sign-in behavior and leaked credentials. |
| Access Reviews | Automated governance & compliance auditing. | Ensures user access remains appropriate over time; streamlines audits. |
| Dynamic Groups | Rule-based group membership. | Reduces manual admin overhead and ensures consistent RBAC. |

---

## 3. Architecture & Operational Protocols

### A. Least Privilege Access Model

- RBAC Structure: Permissions should be scoped to Resource Groups or individual resources rather than the entire subscription.
- Implementation: Use Security Groups for role assignments (not individuals), audit privileges via Access Reviews, and enforce JIT access through PIM.

### B. Securing the Root Identity

- Emergency Accounts (Break-Glass):
  - Create two cloud-only accounts with permanent Global Admin rights.
  - Secure with FIDO2 security keys (2 keys per account).
  - Exclude from standard CA policies but monitor via PIM alerts.
  - Store credentials in a physically secured safe.
- Root Security: Mandatory MFA, no standing privileges (PIM only), and use cloud-only accounts for administrative roles to avoid syncing from on-prem AD.

### C. Team Access Protocol (Daily Workflow)

1. Azure Bastion: Accessing infrastructure via ephemeral, identity-secured hosts.
2. Managed Identities: Production deployments use Managed Identities (no personal credentials in CI/CD).
3. Branch Protections: Require successful `terraform plan` and enforce tagging policies (e.g., NHS data tagging).

### D. AKS Role Analysis

Avoid overly permissive roles in Azure Kubernetes Service:

- Contributor: Often too broad; limit to specific Resource Groups.
- Owner: Use sparingly; strictly for trusted admins with MFA.
- Cluster Admin: Only for full cluster control; use `Azure Kubernetes Service Contributor` for developers.

---

## Related Knowledge

- [[SoT - Digital Identity]]
- [[SoT - Modern Authentication Standards]]
- [[SoT - Microsoft Entra Application Model]]
- [[SoT - Zero Trust Architecture]]
- [[SoT - NHS Identity Compliance]]