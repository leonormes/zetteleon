---
aliases: []
confidence: 
created: 2025-03-05T09:58:39Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Addressing Excessive Privileged Role Assignments in Azure Entra ID
type: 
uid: 
updated: 
version: 
---

## Statement of Intent and Plan: Addressing Excessive Privileged Role Assignments in Azure Entra ID

### 1. Problem Statement

Our organisation, a UK-based data company handling sensitive NHS patient data, currently faces a critical security concern within our Azure Entra ID environment. The Azure portal, within the 'Roles and administrators' blade, has flagged an important recommendation:

> "There are currently **19 privileged role assignments**. It is recommended to not exceed **10**."

This indicates a significant deviation from security best practices, as we currently have almost double the recommended number of privileged roles assigned within our Azure Entra ID. This situation elevates our risk profile and necessitates immediate and decisive action to rectify.

### 2. Reasons for Reducing Privileged Role Assignments

Maintaining a lean number of privileged role assignments is not merely a best practice suggestion; it is a fundamental security principle, particularly crucial for organisations like ours that handle highly sensitive data and operate under stringent regulatory frameworks such as those governing NHS patient data. The key reasons for addressing this over-elevation of privileges are as follows:

#### 2.1. Enhanced Security Risk & Increased Attack Surface

-   **Expanded Attack Surface:** Each privileged account represents a potential entry point for malicious actors. With 19 privileged roles, we significantly broaden the attack surface. Should any of these accounts be compromised, attackers gain immediate high-level access to our Azure environment and the sensitive data it contains.
-   **Increased Risk of Lateral Movement:** If a standard user account is compromised, attackers often attempt to escalate privileges to gain broader access. However, with an already elevated number of privileged accounts, the initial compromise of even a seemingly less critical account can quickly lead to severe breaches if lateral movement is achieved to a legitimately privileged account.

#### 2.2. Mitigation of Insider Threats (Accidental or Malicious)

-   **Reduced Accidental Misconfiguration:** A larger number of administrators increases the likelihood of accidental misconfigurations or errors with significant security implications. The principle of least privilege minimizes the impact of such errors by limiting the scope of potential damage.
-   **Discouraging Malicious Activity:** While we trust our personnel, the risk of insider threats, whether malicious or unintentional, is a reality for all organisations. Limiting privileged roles reduces the number of individuals who could potentially misuse elevated permissions for unauthorized data access, modification, or exfiltration.

#### 2.3. Compliance and Regulatory Requirements

-   **NHS Data Security Standards:** As a company dealing with NHS patient data, we are bound by stringent data security and privacy regulations. Overly broad privileged access can be seen as a failure to adhere to the principle of least privilege, potentially leading to compliance violations and associated penalties.
-   **General Data Protection Regulation (GDPR):** GDPR mandates that organisations implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk. Excessive privileged roles can be interpreted as a lack of appropriate security measures, especially when best practice guidelines recommend a significantly lower number.
-   **ISO 27001 and Cyber Essentials Plus:** Achieving and maintaining certifications like ISO 27001 and Cyber Essentials Plus, which are often essential for organisations working within the UK public sector, requires demonstrating robust security practices. Managing and minimizing privileged access is a key component of these frameworks.

#### 2.4. Principle of Least Privilege

-   **Core Security Tenet:** The principle of least privilege (PoLP) dictates that users should be granted only the minimum levels of access permissions needed to perform their job functions. Over-assigning privileged roles directly violates this principle.
-   **Operational Efficiency and Clarity:** Adhering to PoLP not only enhances security but also simplifies access management and auditing. A clear and concise assignment of roles makes it easier to understand who has access to what and why, streamlining security reviews and incident response.

### 3. Plan to Remediate Excessive Privileged Role Assignments

To address the identified issue, we propose a phased approach to systematically reduce and manage privileged role assignments within our Azure Entra ID. This plan is designed to be thorough, minimizing disruption to operations while significantly enhancing our security posture.

#### Phase 1: Assessment and Discovery (Timeline: 2 weeks)

1.  **Comprehensive Audit of Current Privileged Role Assignments:**
    -   **Action:** Utilize the Azure portal and PowerShell scripting to generate a detailed report of all 19 current privileged role assignments. This report will include:
        -   Role Name (e.g., Global Administrator, User Administrator, etc.)
        -   Assigned Principal (User or Group Name)
        -   Assignment Type (Permanent or Eligible - if using PIM, although currently we are not)
        -   Date of Assignment
        -   Justification (if documented - currently likely missing and needs to be established)
    -   **Tool:** Azure Portal, Azure AD PowerShell Module.

2.  **Justification and Necessity Review for Each Assignment:**
    -   **Action:** For each privileged role assignment identified, conduct a review with relevant team leads and role holders to determine:
        -   **Business Justification:** Why was this privileged role assigned? What specific tasks and responsibilities necessitate this level of access?
        -   **Necessity:** Is the current privileged role truly necessary, or could the user's responsibilities be fulfilled with a less privileged, more granular role?
        -   **Least Privilege Alignment:** Does the current assignment align with the principle of least privilege? Are there any permissions granted that are not actively used or required?
    -   **Documentation:** Meticulously document the justification, necessity assessment, and review outcomes for each privileged role assignment. This documentation will be crucial for audit trails and ongoing governance.

3.  **Identify Potential Role Optimisation and Granularity Opportunities:**
    -   **Action:** Based on the justification review, identify opportunities to:
        -   **Replace broad roles with granular roles:** For example, instead of Global Administrator for tasks that can be achieved with more specific roles like Exchange Administrator, SharePoint Administrator, or Intune Administrator.
        -   **Utilise built-in Azure AD roles effectively:** Ensure we are leveraging the extensive library of built-in roles and not over-relying on overly permissive custom roles (if any are in use).
        -   **Categorise administrative responsibilities:** Group administrative tasks into functional categories (e.g., user management, device management, security management, application management) to better align with more specific Azure AD roles.

#### Phase 2: Role Remediation and Implementation (Timeline: 4 weeks)

1.  **Implement Granular Role Assignments:**
    -   **Action:** Based on the optimisation opportunities identified in Phase 1, begin to implement changes. This will involve:
        -   **Creating or Identifying Specific Roles:** Assigning more granular built-in Azure AD roles that align precisely with the documented responsibilities.
        -   **Careful Testing:** Before making changes in the production environment, thoroughly test role changes in a staging or test environment to ensure no disruption to essential services or administrative functions.
        -   **Phased Rollout:** Implement role changes in a phased manner, starting with less critical roles and progressing to more impactful changes, allowing for monitoring and rollback if necessary.

2.  **Revoke Unnecessary Privileged Role Assignments:**
    -   **Action:** Once granular roles are in place and tested, systematically revoke the broader, less specific privileged role assignments that are no longer justified or necessary.
    -   **Communication:** Communicate role changes clearly and proactively to affected users, providing guidance and support as needed.

3.  **Implement Privileged Identity Management (PIM):**
    -   **Action:** Deploy Azure AD Privileged Identity Management (PIM) to move from permanent privileged role assignments to just-in-time (JIT) elevation.
    -   **Configuration:** Configure PIM policies to:
        -   Require justification for role activation.
        -   Set time limits for role activation.
        -   Require multi-factor authentication for role activation.
        -   Implement approval workflows for certain highly privileged roles.
    -   **Training:** Provide comprehensive training to administrators on how to use PIM to activate roles when needed and understand the new privileged access management process.

#### Phase 3: Ongoing Monitoring and Governance (Ongoing)

1.  **Establish Continuous Monitoring of Privileged Role Assignments:**
    -   **Action:** Implement automated monitoring and alerting to track privileged role assignments. Utilize Azure Monitor and Azure Sentinel to:
        -   Continuously monitor the number of privileged role assignments.
        -   Alert on any new privileged role assignments or deviations from the established baseline.
        -   Log all privileged role activations (especially when using PIM).

2.  **Regular Privileged Access Reviews:**
    -   **Action:** Establish a recurring schedule (e.g., quarterly or bi-annually) for reviewing all privileged role assignments.
    -   **Review Process:** The review process will involve:
        -   Re-validating the justification and necessity for each privileged role assignment.
        -   Ensuring roles are still aligned with the principle of least privilege.
        -   Identifying any opportunities for further role optimisation or reduction.
        -   Updating documentation as needed.

3.  **Document and Enforce New Role Assignment Processes and Security Policies:**
    -   **Action:** Formalize the new processes for requesting, reviewing, approving, and assigning privileged roles.
    -   **Policy Updates:** Update security policies and procedures to reflect the new privileged access management approach, including the use of PIM and the principle of least privilege.
    -   **Training and Awareness:** Provide ongoing security awareness training to all staff, emphasizing the importance of least privilege and responsible use of privileged access.

### 4. Statement of Intent

This document serves as our statement of intent to proactively and decisively address the issue of excessive privileged role assignments within our Azure Entra ID. We are committed to significantly reducing the number of these assignments to align with security best practices and recommendations, thereby strengthening our security posture and ensuring the continued protection of sensitive NHS patient data. We understand the critical importance of this undertaking and are dedicated to implementing the outlined plan diligently and effectively.

By following this plan, we will not only reduce the number of privileged roles but also establish a more robust, secure, and manageable Azure Entra ID environment, better suited to meet the stringent security demands of handling NHS patient data and maintaining compliance with relevant regulations.

The following table shows the frequency of each role assignment.

|   |   |
|---|---|
|**roleDisplayName**|**Count**|
|Groups Administrator|10|
|User Administrator|9|
|Exchange Administrator|8|
|Teams Administrator|8|
|SharePoint Administrator|8|
|Service Support Administrator|8|
|Office Apps Administrator|8|
|License Administrator|8|
|Global Administrator|4|
|Directory Readers|3|
|Global Reader|3|
|Security Reader|2|
|Security Administrator|2|
|Reports Reader|2|
|Privileged Role Administrator|2|
|Application Administrator|2|
|Billing Administrator|2|
|Conditional Access Administrator|2|
|Edge Administrator|1|
|Power Platform Administrator|1|
|Attack Simulation Administrator|1|
|Authentication Administrator|1|
|Authentication Policy Administrator|1|
|Azure AD Joined Device Local Administrator|1|
|Security Operator|1|
|Cloud App Security Administrator|1|
|Cloud Device Administrator|1|
|Compliance Administrator|1|
|Privileged Authentication Administrator|1|
|Printer Administrator|1|
|Permissions Management Administrator|1|
|Exchange Recipient Administrator|1|
|Compliance Data Administrator|1|
|Network Administrator|1|
|Intune Administrator|1|
|Identity Governance Administrator|1|
|Hybrid Identity Administrator|1|
|Helpdesk Administrator|1|
|Application Developer|1|
|Domain Name Administrator|1|
|Dynamics 365 Administrator|1|
|Fabric Administrator|1|
|External Identity Provider Administrator|1|
|Windows Update Deployment Administrator|1|

The table shows that there are 19 privileged role assignments. It is recommended to not exceed 10.

There are several ways to reduce the number of privileged role assignments:

- **Use built-in roles.** Azure AD has several built-in roles that can be used to manage different aspects of the directory. These roles have predefined permissions that are appropriate for most organizations.
- **Create custom roles.** If the built-in roles do not meet your needs, you can create custom roles with specific permissions. This allows you to give users only the permissions they need to do their job.
- **Use role-based access control (RBAC).** RBAC is a security feature that allows you to control access to resources based on the user's role. This can help you to reduce the number of privileged role assignments by giving users only the permissions they need to access the resources they need.

By following these recommendations, you can reduce the number of privileged role assignments in your Azure AD directory and improve the security of your organization.

The following are the markdown reports for each user, listing their roles:

**00000014-0000-0000-c000-000000000000 (1 role)**

- Directory Readers

**0000001a-0000-0000-c000-000000000000 (1 role)**

- Directory Readers

**aa9d88df-26fd-4239-a48a-19068e0502c5 (1 role)**

- Groups Administrator

**al.vanstone.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**ghailes@fitfile.com (6 roles)**

- Global Administrator
- Global Reader
- Privileged Role Administrator
- Reports Reader
- Security Administrator
- Security Reader

**jono.whitewick.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**jumpcloudconnector@fitfile.com (1 role)**

- Global Administrator

**leon.ormes@fitfile.com (4 roles)**

- Application Administrator
- Global Reader
- Groups Administrator
- Permissions Management Administrator

**luke.scammell.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**matt.hill.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**mike.hill.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**philip.russmeyer@fitfile.com (3 roles)**

- Billing Administrator
- Global Administrator
- User Administrator

**sarah.povey@fitfile.com (1 role)**

- Billing Administrator

**scott.bevan.ta@fitfile.com (8 roles)**

- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**stephen.povall.ta@fitfile.com (9 roles)**

- Conditional Access Administrator
- Exchange Administrator
- Groups Administrator
- License Administrator
- Office Apps Administrator
- Service Support Administrator
- SharePoint Administrator
- Teams Administrator
- User Administrator

**techahoy@fitfileltd.onmicrosoft.com (1 role)**

- Global Administrator
