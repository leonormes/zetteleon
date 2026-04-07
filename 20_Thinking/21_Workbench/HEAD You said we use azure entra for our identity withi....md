---
title: "You said we use azure entra for our identity withi..."
source: "https://gemini.google.com/app/90721765fb79ed7a"
captured: "2026-04-06T18:12:56+01:00 2026-04-06T18:12:56+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

we use azure entra for our identity within the company. Find the latest best practices from microsoft for IAM and how we should be managing things

---

**Gemini**

Managing identity in a modern landscape requires moving beyond simple password resets. As of 2026, Microsoft’s guidance for **Microsoft Entra** (formerly Azure AD) focuses heavily on **AI-powered protection**, **phishing-resistant MFA**, and **identity governance**.

Here are the latest best practices for managing your Entra environment:

## 1\. Strengthen Authentication (The "Must-Haves")

- **Phishing-Resistant MFA:** Move away from SMS and voice calls. Microsoft now strongly recommends **FIDO2 security keys** (like YubiKeys), **Windows Hello for Business**, or **Microsoft Authenticator (certificate-based/Passkeys)**.
- **Eliminate Legacy Auth:** Block outdated protocols (IMAP, POP3, SMTP) via **Conditional Access**. These bypass MFA and are the primary entry point for credential stuffing.
- **Enforce Security Defaults:** If you are a smaller organisation without complex needs, ensure "Security Defaults" are enabled. For larger enterprises, use granular Conditional Access policies.

## 2\. Implement Zero Trust Access

- **Conditional Access (CA) is the Engine:** Your policies should now be "risk-based." Integrate **Microsoft Entra ID Protection** to automatically block or require MFA when a "high-risk" sign-in is detected (e.g., impossible travel or leaked credentials).
- **Continuous Access Evaluation (CAE):** Ensure CAE is enabled so that if a user’s account is disabled or their location changes significantly, their session is revoked in near real-time, rather than waiting for the token to expire.
- **Unified Identity & Network:** 2026 guidance suggests unifying identity with network security (Entra Internet Access and Private Access) to create a single "Access Fabric" that monitors both the user and the network path.

## 3\. Privileged Access Management (PIM)

- **Zero Standing Access:** No one should have permanent "Global Administrator" or "Security Administrator" rights. Use **Microsoft Entra Privileged Identity Management (PIM)** to grant "Just-In-Time" (JIT) access that expires automatically.
- **The "Rule of 5":** Microsoft recommends having fewer than **five** Global Administrators.
- **Break-Glass Accounts:** Maintain two "Emergency Access" accounts that are excluded from MFA and Conditional Access. These should be cloud-only, have 20+ character passwords, and be monitored for *any* login activity.

## 4\. Governance and Lifecycle

- **Access Reviews:** Set up automated, quarterly reviews for all privileged roles and guest users. If a manager doesn't explicitly "approve" the access, Entra should automatically revoke it.
- **Entitlement Management:** Use "Access Packages" for onboarding. Instead of manually adding users to groups, create a package that includes the Teams, Apps, and SharePoint sites a specific role needs, with a built-in expiration date.
- **Machine Identity & AI Agents:** New for 2026, you must govern **AI agents** and **Workload Identities** (Service Principals) with the same rigour as humans. Assign "Human Sponsors" to all non-human identities to prevent "orphaned" permissions.

## 5\. Hybrid Security (If applicable)

- **Block "SyncJacking":** If you sync from on-premises AD, ensure you have enabled the latest **Hard-Match protection** in Entra Connect (enforced as of March 2026). This prevents attackers from "matching" an on-prem account to a high-privileged cloud account to take it over.
- **Disable Soft Matching:** Unless strictly required for migration, disable "BlockSoftMatch" to close a common lateral movement path.

---

### Summary Checklist for Admins

| Action Item | Tooling | Priority |
| --- | --- | --- |
| **Enable Phishing-Resistant MFA** | Authentication Methods | Critical |
| **Configure Risk-Based CA Policies** | Conditional Access / ID Protection | High |
| **Move Admins to JIT Access** | Privileged Identity Management (PIM) | High |
| **Automate Guest Cleanup** | Access Reviews | Medium |
| **Audit Workload Identities** | Workload ID Premium | Medium |

Would you like me to draft a specific Conditional Access policy template for your administrators or help you set up an Access Review?

---

**You**

review the added sources in notebooklm and update the plan to meet our pentest results remediations

---

**Gemini**

Based on the specific findings from the **Azure & Entra Configuration Review** and the **NCSC CAF Compliance Review**, the following updated remediation plan prioritises the most critical security gaps identified in your environment.

### 1\. Immediate High-Priority Remediations (Week 1)

These actions address **Critical** and **High** severity vulnerabilities that currently allow for a total environment takeover.

- **Secure Global Administrator Accounts:**
	- Immediately remove the **Global Administrator** role from the **Tech Ahoy** contractor account and enforce phishing-resistant MFA if any access is still required.
		- Reduce the total number of Global Administrators from six to **two or three**.
		- Implement **Microsoft Entra Privileged Identity Management (PIM)** to convert remaining permanent admin assignments into "eligible" roles that require time-limited activation.
- **Enforce MFA & Disable Shared Access:**
	- Enable MFA for all human accounts, specifically **bob.jones**, **eric.lin**, and **techahoy**.
		- Disable interactive sign-in for all service or shared accounts (e.g., **fitfile-service**, **support**, **appleid**).
- **Restrict Excessive Service Principal Permissions:**
	- Remove the **User Access Administrator** role from the **FITFILE Terraform Cloud Provisioner** and the **DevOpsEngineers** group to prevent unauthorized role assignments.
- **Establish Baseline Visibility:**
	- Register the `microsoft.insights` resource provider and create diagnostic settings to export all Activity Logs to a **Log Analytics workspace**.

### 2\. Medium-Term Operational Hardening (Weeks 2–4)

These steps focus on closing common attack vectors and improving system security.

- **Hardening Directory Settings:**
	- Restrict the ability for non-admin users to create security groups, register applications, create new tenants, or consent to third-party applications.
- **Infrastructure & Network Security:**
	- **AKS Hardening:** Disable AKS local accounts and ensure consistent host-level encryption across all node pools.
		- **Jumpbox VM:** Disable password authentication and enforce **SSH key-only** access.
		- **Network Filtering:** Implement outbound NSG rules to restrict data egress to only required destinations.
- **Audit & Cleanup:**
	- Conduct a full audit of all **39 application registrations**, deleting stale entries like `azure-cli-*` and `TEMP-PrivateTerraformCluster`.

### 3\. Long-Term Governance and Resilience (Months 2+)

These actions aim to maintain a secure posture and ensure regulatory compliance.

- **Advanced Monitoring:** Configure all 11 CIS-recommended activity log alerts and integrate logs with a **SIEM** for real-time threat detection.
- **Resilience & Recovery:** Enable **Trusted Launch** (Secure Boot + vTPM) and **Azure Backup** for the Jumpbox VM.
- **Governance Framework:** Establish a formal quarterly review for privileged access and an automated rotation program for application credentials.
- **Continuous Improvement:** Schedule annual Azure security assessments and develop specific incident response playbooks for identity-based breaches.
