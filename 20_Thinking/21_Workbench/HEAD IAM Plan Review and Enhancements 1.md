---
title: "You said is this plan complete for a strong IAM"
source: "https://gemini.google.com/app/fe2e2f323009e813"
captured: "2026-05-11T13:11:13+01:00 2026-05-11T13:11:13+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

is this plan complete for a strong IAM

---

**Gemini**

The provided plan offers a very strong foundation for an Identity and Access Management (IAM) framework, particularly regarding the mitigation of immediate risks. However, to be considered "complete" by modern security standards (such as Zero Trust), there are several advanced areas and administrative processes that should be integrated.

### Core Strengths of the Current Plan

The plan successfully addresses the most critical "quick wins" for securing an environment:

- **MFA Enforcement:** It directly tackles MFA exclusions for demo and service accounts, proposing more secure alternatives like shared mailboxes.
- **Privileged Access Management:** The introduction of **Privileged Identity Management (PIM)** for users requiring elevated permissions is a significant upgrade. This ensures that high-level access is audited, time-bound, and requires justification.
- **Least Privilege Principle:** There is a clear focus on reducing the number of **Global Administrators** and move users to more restricted roles like **Global Reader** or **Billing Reader**.
- **Attack Surface Reduction:** Restricting the ability of non-admin users to create security groups or register applications limits the potential for "shadow IT" or malicious persistence.

---

### Gaps to Address for a "Complete" Posture

While the plan is excellent for technical hardening, a "strong" IAM posture typically requires these additional layers:

**1\. Formalised Lifecycle Management** The plan lists specific individuals to be removed or kept to save on licence costs. However, it does not outline a formalised **Joiner-Mover-Leaver (JML)** process. A complete plan should define how access is automatically revoked when any staff member leaves, rather than relying on manual audits.

**2\. Conditional Access Policies (Beyond MFA)** While fixing MFA exclusions is mentioned, a robust IAM strategy uses **Conditional Access (CA)** to evaluate more than just a password. This includes:

- **Device Compliance:** Only allowing access from managed, healthy devices.
- **Location/Network:** Restricting access from unexpected countries or non-corporate IP ranges.
- **Risk-Based Sign-ins:** Automatically blocking or requiring a password reset if a login appears "atypical" (requires Entra ID P2, which the plan includes).

**3\. Access Reviews** Since the plan involves purchasing **Entra ID P2**, you gain access to **Access Reviews**. A complete plan should schedule these (e.g., quarterly) to force managers or resource owners to formally re-validate that their team members still require the permissions they hold.

**4\. Governance for Non-Human Identities** The plan focuses heavily on user and developer accounts. A strong IAM strategy must also address **Service Principals** and **Managed Identities**. These are often overlooked but can be highly privileged; they should be audited with the same rigour as human users.

**5\. Logging and Monitoring Readiness** The plan notes that **Diagnostic Settings** and **Activity Log Exports** are "TO BE CONFIRMED" by the tech team. Without these logs being exported to a Security Information and Event Management (SIEM) system, you may have "blind spots" where identity-based attacks go undetected even if MFA is active.

---

### Summary Table of Recommended Additions

| Feature | Status in Plan | Recommendation |
| --- | --- | --- |
| **Emergency Access** | Partial | Ensure "Breakglass" accounts are cloud-only and excluded from CA. |
| **External Identities** | Not Mentioned | Define how Guest/B2B users are governed and expired. |
| **Workload Identities** | Not Mentioned | Audit permissions for apps and automated scripts. |
| **Audit Logs** | TBC | Finalise the export of Entra ID logs to a secure repository. |

Does your organisation currently have a formalised process for offboarding employees, or are these manual licence reviews the primary method for managing departures?

---

**You**

output the full page with your included suggestions

---

**Gemini**

This integrated IAM Hardening Plan combines the original recommendations with advanced security layers to ensure a robust and scalable identity posture.

---

## Section 1: Microsoft Entra Identity Hardening

### Privileged Access & MFA

- **Fix MFA Exclusions \[EntraFF-05\]:** MFA must be enforced for all users. Currently, Demo users are excluded; options include converting them to shared mailboxes with email-based MFA, requiring individual accounts, or maintaining the status quo.
- **Reduce Global Administrator Count \[EntraFF-02\]:** Decrease high-level access by reducing Jumpcloud connector permissions.
	- **Philip:** Assigned Global Reader and Billing Reader roles without PIM. Option to add User Admin via PIM if needed.
		- **Robin:** Retains Global Administrator access via PIM.
		- **Breakglass:** The breakglass account retains GA status and is managed by Philip.
- **DevOps Permissions \[EntraFF-04\]:** Remove User Access Administrator roles from the DevOps Engineers group.
- **Privileged Identity Management (PIM):** Enable PIM for required users (PR, OR, LO, RM). This requires increased licence costs but ensures privilege escalation is audited and requires automated approval.

### User & Application Governance

- **User Consent \[EntraFF-06\]:** Restrict user consent for applications to require admin approval or limit it to verified publishers.
- **Security Group Creation \[EntraFF-07\]:** Restrict security group creation to administrators only within Entra ID User Settings.
- **Application Registration \[EntraFF-08\]:** Disable the ability for non-admin users to register applications.
- **\[New Suggestion\] Conditional Access Policies:** Beyond MFA, implement policies that require device compliance and restrict access based on sign-in risk levels (leveraging the proposed P2 licences).

---

## Section 2: Licence Management & Lifecycle

### Joiner-Mover-Leaver (JML) Audits

- **Microsoft 365 Business Basic:** Review the following accounts to identify potential savings of £32.20:
	- **Remove:** Gokce Civelekoglu, Ihor Zemtsov, Pentester1, Pentester2, Pentester3, Pentester4.
		- **Convert:** Support account to a shared mailbox.
		- **Keep/Review:** Adam Gilbert, David Reeves, Doreena Ross, Pavlo Kotov, Ross Law.
- **Office 365 E3:** Review accounts to save £61.80:
	- **Remove:** Darren Lee, Jon Bradshaw, Yasir.
		- **Retain:** 3 spare licences.
- **\[New Suggestion\] Access Reviews:** Utilise Entra ID P2 to schedule quarterly reviews where resource owners must confirm that the users listed above still require their current level of access.

### Subscription Adjustments

- **Unsubscribe Entra ID P1:** Remove the unassigned licence (likely from Gareth) to save £4.60.
- **Add Entra ID P2:** Purchase licences for users requiring Azure permissions to enable PIM and advanced auditing.

---

## Section 3: Infrastructure & Cloud Security

### Technical Resource Constraints

- **AKS Local Accounts \[EntraFF-18\]:** Disable local accounts on the UKS cluster (`aks-ff-uks-gp-1`) using the Azure CLI. Testing is required before a wider rollout.
- **Jumpbox VM \[EntraFF-22\]:** Evaluate if SSH access is a viable replacement for password authentication across all installations.
- **Activity Logging \[EntraFF-12\]:** Finalise diagnostic settings and activity log exports (currently pending confirmation from the tech team).
- **\[New Suggestion\] Workload Identities:** Conduct a dedicated audit of Service Principals and Managed Identities to ensure non-human entities follow the principle of least privilege.

AWS Infrastructure

- **Account Contact Details:** Update the contact phone number (Philip or Robin) and review the registered address.
- **Alternate Contacts:** Populate the currently empty billing, operations, and security contact fields.
- **Root Management:** Enable root user access management via IAM.

---

## Section 4: Cost Analysis Summary

| Licence Type | Unit Cost | Quantity | Monthly Difference |
| --- | --- | --- | --- |
| **Microsoft 365 Business Basic** | £4.60 | 7 | \-£32.20 |
| **Microsoft Entra ID P1** | £4.60 | 1 | \-£4.60 |
| **Office 365 E3** | £20.60 | 3 | \-£61.80 |
| **Microsoft Entra ID P2** | £6.90 | 4 | +£27.60 |
| **Total Net Change** |  |  | \-£71.00 |

---

**You**

review the FiL090226JH - API Testing v0.3 Draft.pdf source in the notebook. Update the work recommendations based on Microsoft Entra Recommended Actions Summary.pdf it and the other sources.

---

**Gemini**

Based on the **Microsoft Entra Recommended Actions Summary** and the broader **NCSC Cyber Assessment Framework (CAF)** context, the following updates have been made to the **API Testing v0.3 Draft** work recommendations. These updates integrate identity hardening, technical remediation, and cost-optimisation strategies.

### 1\. Identity & Access Management (IAM) for API Security

- **Enforce MFA for All Identities \[EntraFF-05\]:** Remove all MFA exclusions, including those for service and demo accounts. Convert existing Demo accounts to **Shared Mailboxes** where possible to enable email-based MFA and reduce licensing costs.
- **Implement Privileged Identity Management (PIM):** Purchase **Microsoft Entra ID P2** licences for users requiring administrative access to Azure/API resources (specifically PR, OR, LO, and RM). This ensures that elevated permissions are time-bound, audited, and require justification.
- **Restrict Application Lifecycle \[EntraFF-08\]:** Disable the ability for non-admin users to register applications to prevent unauthorised API integrations. Implement an admin-approval workflow for all user consent requests.
- **Role Rationalisation \[EntraFF-02\]:** Reduce the number of permanent Global Administrators. Philip should transition to **Global Reader** and **Billing Reader** (no PIM), while Robin should maintain GA status via **PIM**.

### 2\. Infrastructure & Technical Hardening

- **Secure AKS Architecture \[EntraFF-18\]:** Disable local accounts on the AKS cluster (`aks-ff-uks-gp-1`) to force integration with Entra ID identities. This aligns with NCSC CAF principles for robust identity protection.
- **Infrastructure Access \[EntraFF-22\]:** Re-evaluate the use of password authentication for Jumpbox VMs. Testing should be conducted to determine if SSH key-based access is viable across all environments.
- **AWS Root Governance:** Enable root access management and update account contact details to ensure secure recovery and billing oversight.

### 3\. Governance, Audit, and Logging

- **Finalise Diagnostic Exports \[EntraFF-12\]:** The technical team must confirm and implement diagnostic settings and activity log exports. This is critical for detecting potential API abuse or identity-based attacks.
- **Security Group Governance \[EntraFF-07\]:** Restrict the creation of security groups to administrators only to prevent the "shadow" expansion of permissions.

### 4\. Operational Efficiency & Licence Optimisation

The following licence removals and conversions should be executed immediately to achieve a total net saving of **£71.00 per month**:

| **Category** | **Recommended Actions** |
| --- | --- |
| **M365 Business Basic** | Remove: Gokce Civelekoglu, Ihor Zemtsov, and all Pentester accounts. Convert Support to shared mailbox. |
| **Office 365 E3** | Remove: Darren Lee, Jon Bradshaw, and Yasir. |
| **Entra ID P1** | Unsubscribe the unassigned P1 licence (Gareth). |
| **Entra ID P2** | Add 4x P2 licences to support PIM for core administrative staff. |

### NCSC CAF Alignment Note

These recommendations ensure compliance with **Objective B (Protecting Against Cyber Attack)** by implementing least privilege and strong authentication, and **Objective C (Detecting Cyber Security Events)** through the finalisation of logging and diagnostic exports.

---

**You**

anser this email question from Robin Hi guys,

Do either of you have anything to add to these recommendations for Cloud/ Entra configs?

We will need to discuss the ones in red but I'd like to send to Helena and Philip to get the work started.

---

**Gemini**

Hi Robin,

This is a great starting point for Helena and Philip. The plan covers the immediate security "holes" effectively.

To ensure we are building a truly resilient posture, I’ve added a few strategic items to the list—particularly around those "red" technical items and how we can best use the new Entra ID P2 features we're proposing.

### 1\. Addressing the "Red" Technical Actions

These are the heavy lifters that Helena and Philip will likely need clear direction on:

- **Logging & Monitoring \[EntraFF-12\]:** This is a priority. Without exporting logs to a SIEM or central storage, we are essentially "flying blind" if an identity-based attack occurs.
- **AKS Local Accounts \[EntraFF-18\]:** Disabling these is the right move for security, but we should ensure the tech team has tested the Entra ID integration thoroughly so we don't accidentally lock out legitimate dev processes.
- **Jumpbox Authentication \[EntraFF-22\]:** Switching from passwords to SSH keys is standard best practice; we just need to confirm it won't break any legacy deployment scripts.

### 2\. Strategic Additions (The "Value-Adds")

Since we are proposing a move to **Entra ID P2** (which is actually saving us money overall), we should take advantage of the advanced features it unlocks:

- **Conditional Access (CA) Evolution:** We should go beyond just "turning on MFA". I recommend adding policies that check for **device compliance** (e.g., "is the laptop healthy?") and **sign-in risk** (e.g., "is this login from an impossible travel location?") before granting access.
- **Quarterly Access Reviews:** We can automate these using P2. This forces managers to formally re-validate that their team still needs their current permissions, preventing "permission creep" over time.
- **Formalised JML Process:** While the current licence cleanup is excellent, we should formalise the **Joiner-Mover-Leaver** process so that when someone leaves, their access is revoked systematically rather than waiting for a manual audit.

### 3\. Operational & Cost Quick Wins

The licence optimisation you’ve drafted is spot on. By removing the redundant M365 Business Basic and E3 seats and swapping Gareth’s P1 for the new P2 seats, we’re looking at a **net saving of approximately £71.00 per month** while significantly increasing our security.

I'm happy to jump on a call to go through the "red" items in more detail before we send this off. Does tomorrow morning work for you?

Best,

\[Your Name\]

---

**Would you like me to draft a more technical version of these additions specifically for Philip and Helena to use as an implementation checklist?**
