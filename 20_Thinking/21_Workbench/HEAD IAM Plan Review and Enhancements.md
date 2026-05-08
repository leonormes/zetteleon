---
captured: "2026-05-07T21:33:45+01:00 2026-05-07T21:33:45+01:00"
created: 2026-05-07T20:33:50+00:00
modified: 2026-05-07T20:34:21+00:00
source: "https://gemini.google.com/app/fe2e2f323009e813"
status: "processing"
tags: ["input"]
title: HEAD IAM Plan Review and Enhancements
type: "head"
---

## Raw Output / Content

You

is this plan complete for a strong IAM

---

Gemini

The provided plan offers a very strong foundation for an Identity and Access Management (IAM) framework, particularly regarding the mitigation of immediate risks. However, to be considered "complete" by modern security standards (such as Zero Trust), there are several advanced areas and administrative processes that should be integrated.

### Core Strengths of the Current Plan

The plan successfully addresses the most critical "quick wins" for securing an environment:

- MFA Enforcement: It directly tackles MFA exclusions for demo and service accounts, proposing more secure alternatives like shared mailboxes.
- Privileged Access Management: The introduction of Privileged Identity Management (PIM) for users requiring elevated permissions is a significant upgrade. This ensures that high-level access is audited, time-bound, and requires justification.
- Least Privilege Principle: There is a clear focus on reducing the number of Global Administrators and move users to more restricted roles like Global Reader or Billing Reader.
- Attack Surface Reduction: Restricting the ability of non-admin users to create security groups or register applications limits the potential for "shadow IT" or malicious persistence.

---

### Gaps to Address for a "Complete" Posture

While the plan is excellent for technical hardening, a "strong" IAM posture typically requires these additional layers:

1\. Formalised Lifecycle Management The plan lists specific individuals to be removed or kept to save on licence costs. However, it does not outline a formalised Joiner-Mover-Leaver (JML) process. A complete plan should define how access is automatically revoked when any staff member leaves, rather than relying on manual audits.

2\. Conditional Access Policies (Beyond MFA) While fixing MFA exclusions is mentioned, a robust IAM strategy uses Conditional Access (CA) to evaluate more than just a password. This includes:

- Device Compliance: Only allowing access from managed, healthy devices.
- Location/Network: Restricting access from unexpected countries or non-corporate IP ranges.
- Risk-Based Sign-ins: Automatically blocking or requiring a password reset if a login appears "atypical" (requires Entra ID P2, which the plan includes).

3\. Access Reviews Since the plan involves purchasing Entra ID P2, you gain access to Access Reviews. A complete plan should schedule these (e.g., quarterly) to force managers or resource owners to formally re-validate that their team members still require the permissions they hold.

4\. Governance for Non-Human Identities The plan focuses heavily on user and developer accounts. A strong IAM strategy must also address Service Principals and Managed Identities. These are often overlooked but can be highly privileged; they should be audited with the same rigour as human users.

5\. Logging and Monitoring Readiness The plan notes that Diagnostic Settings and Activity Log Exports are "TO BE CONFIRMED" by the tech team. Without these logs being exported to a Security Information and Event Management (SIEM) system, you may have "blind spots" where identity-based attacks go undetected even if MFA is active.

---

### Summary Table of Recommended Additions

| Feature | Status in Plan | Recommendation |
| --- | --- | --- |
| Emergency Access | Partial | Ensure "Breakglass" accounts are cloud-only and excluded from CA. |
| External Identities | Not Mentioned | Define how Guest/B2B users are governed and expired. |
| Workload Identities | Not Mentioned | Audit permissions for apps and automated scripts. |
| Audit Logs | TBC | Finalise the export of Entra ID logs to a secure repository. |

Does your organisation currently have a formalised process for offboarding employees, or are these manual licence reviews the primary method for managing departures?

---

You

output the full page with your included suggestions

---

Gemini

This integrated IAM Hardening Plan combines the original recommendations with advanced security layers to ensure a robust and scalable identity posture.

---

## Section 1: Microsoft Entra Identity Hardening

### Privileged Access & MFA

- Fix MFA Exclusions \[EntraFF-05\]: MFA must be enforced for all users. Currently, Demo users are excluded; options include converting them to shared mailboxes with email-based MFA, requiring individual accounts, or maintaining the status quo.
- Reduce Global Administrator Count \[EntraFF-02\]: Decrease high-level access by reducing Jumpcloud connector permissions.
	- Philip: Assigned Global Reader and Billing Reader roles without PIM. Option to add User Admin via PIM if needed.
		- Robin: Retains Global Administrator access via PIM.
		- Breakglass: The breakglass account retains GA status and is managed by Philip.
- DevOps Permissions \[EntraFF-04\]: Remove User Access Administrator roles from the DevOps Engineers group.
- Privileged Identity Management (PIM): Enable PIM for required users (PR, OR, LO, RM). This requires increased licence costs but ensures privilege escalation is audited and requires automated approval.

### User & Application Governance

- User Consent \[EntraFF-06\]: Restrict user consent for applications to require admin approval or limit it to verified publishers.
- Security Group Creation \[EntraFF-07\]: Restrict security group creation to administrators only within Entra ID User Settings.
- Application Registration \[EntraFF-08\]: Disable the ability for non-admin users to register applications.
- \[New Suggestion\] Conditional Access Policies: Beyond MFA, implement policies that require device compliance and restrict access based on sign-in risk levels (leveraging the proposed P2 licences).

---

## Section 2: Licence Management & Lifecycle

### Joiner-Mover-Leaver (JML) Audits

- Microsoft 365 Business Basic: Review the following accounts to identify potential savings of £32.20:
	- Remove: Gokce Civelekoglu, Ihor Zemtsov, Pentester1, Pentester2, Pentester3, Pentester4.
		- Convert: Support account to a shared mailbox.
		- Keep/Review: Adam Gilbert, David Reeves, Doreena Ross, Pavlo Kotov, Ross Law.
- Office 365 E3: Review accounts to save £61.80:
	- Remove: Darren Lee, Jon Bradshaw, Yasir.
		- Retain: 3 spare licences.
- \[New Suggestion\] Access Reviews: Utilise Entra ID P2 to schedule quarterly reviews where resource owners must confirm that the users listed above still require their current level of access.

### Subscription Adjustments

- Unsubscribe Entra ID P1: Remove the unassigned licence (likely from Gareth) to save £4.60.
- Add Entra ID P2: Purchase licences for users requiring Azure permissions to enable PIM and advanced auditing.

---

## Section 3: Infrastructure & Cloud Security

### Technical Resource Constraints

- AKS Local Accounts \[EntraFF-18\]: Disable local accounts on the UKS cluster (`aks-ff-uks-gp-1`) using the Azure CLI. Testing is required before a wider rollout.
- Jumpbox VM \[EntraFF-22\]: Evaluate if SSH access is a viable replacement for password authentication across all installations.
- Activity Logging \[EntraFF-12\]: Finalise diagnostic settings and activity log exports (currently pending confirmation from the tech team).
- \[New Suggestion\] Workload Identities: Conduct a dedicated audit of Service Principals and Managed Identities to ensure non-human entities follow the principle of least privilege.

AWS Infrastructure

- Account Contact Details: Update the contact phone number (Philip or Robin) and review the registered address.
- Alternate Contacts: Populate the currently empty billing, operations, and security contact fields.
- Root Management: Enable root user access management via IAM.

---

## Section 4: Cost Analysis Summary

| Licence Type | Unit Cost | Quantity | Monthly Difference |
| --- | --- | --- | --- |
| Microsoft 365 Business Basic | £4.60 | 7 | \-£32.20 |
| Microsoft Entra ID P1 | £4.60 | 1 | \-£4.60 |
| Office 365 E3 | £20.60 | 3 | \-£61.80 |
| Microsoft Entra ID P2 | £6.90 | 4 | +£27.60 |
| Total Net Change |  |  | \-£71.00 |
