---
created: 2026-05-11T08:57:57+00:00
modified: 2026-08-29T09:36:20+00:00
permalink: llmeon/30-library/200-projects/mesh-vs-dspt-compliance-status
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: MESH vs DSPT compliance status
type: null
---

## MESH Vs DSPT compliance Status

Bottom line: your MESH setup looks operationally in progress, but I would not call it fully DSPT-evidenced yet. The strongest signals are that the mailbox is active and the deployment path is being worked through, while the governance, assurance, and operational-control evidence needed to show DSPT-style completeness is still partly open.

### What's Already in place

- Your internal MESH note says integration depends on an active mailbox, ODS code registration, and HSCN technical standards, and it records the production mailbox as active and accessible.
- The NHS Service Desk case `CS1214752` explicitly says: "Your mailbox is still showing as active on MESH. You should be able to access and use it."
- The project summary shows the combined DCA/DSA has been sent to the Trust board, but feedback is still pending, and there are outstanding IP queries awaiting CUH Legal guidance. It also says the DPIA is not currently required pending deployment setup.
  - [NUH - Project Summary (Internal)](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2727673857/NUH-+Project+Summary+Internal)
  - [NUH project summary spreadsheet](https://fitfileltd.sharepoint.com/:x:/s/FitfileTeam/IQBE2wIeWNorT4fDJ2sgI9IGAZMGJHU382XXenavx2lKHuc?e=opaHlI)
- The deployment-prep note shows the remaining technical/security work is still being defined: cyber sign-off, CAB cadence, secrets/TLS, observability, backup/restore, RTO/RPO, and support escalation.
  - [Work Required for Deployment NUH](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2726756353/NUH+-+Project+Directory?atl_f=PAGETREE)

### DSPT Mapping

| DSPT area | Status | Evidence |
|---|---|---|
| Governance & legal | Partial | DCA/DSA in review; IP queries open |
| Access governance | Partial | MESH mailbox active, but no explicit DSPT access-review evidence found |
| Audit & monitoring | Partial | Platform notes mention auditing, but no explicit SIEM/export evidence for this MESH thread |
| Business continuity | Partial | RTO/RPO, backup frequency, and restore scope still open |
| Assurance / certification | Not evidenced | I did not find a recorded DSPT submission or "Standards Met" attestation |

### Standards Check

The official sources I found describe DSPT as the NHS data-security self-assessment against the 10 standards, and they support DSPT as a baseline for secure NHS data access. I could not verify an official source that says MESH specifically requires "Standards Met" as a direct prerequisite, even though your internal notes currently treat it that way.

- [DSPT portal](https://www.dsptoolkit.nhs.uk)
- [NHS England secure email account guidance](https://www.england.nhs.uk/ourwork/clinical-policy/ordering-medication-using-proxy-access/getting-a-secure-email-account-a-guide-for-social-care-organisations/getting-a-secure-email-account/)
- [NHSmail DSPT guidance](https://support.nhs.net/knowledge-base/data-security-and-protection-toolkit/)

### Open Actions

1. Close the combined DCA/DSA and resolve the CUH Legal IP queries.
2. Confirm the cyber sign-off owner/date (`Andy Callow` is named in the deployment notes).
3. Finalise the network/VPN, TLS/secrets, logging, backup/restore, and support model.
4. Capture explicit DSPT evidence: self-assessment status, training/access-review evidence, incident-response testing, and audit-log export.
5. Reconcile the internal assumption that "Standards Met" is mandatory for MESH with the official wording you use in compliance docs.

If you want, I can turn this into a one-page compliance gap log or a DSPT evidence checklist next.

Regarding your case CS1214752, we have provided the below resolution. 

---

Proposed resolution:

Your mailbox is still showing as active on MESH. You should be able to access and use it.

Any issues let us know.

---

Your case description:

Query Regarding Production MESH Mailbox Status - FITFILE Group Ltd (ODS: 8KM90)

|   |
|---|
|We have logged a case for you, reference CS1225473. A member of our service desk team will be in touch.<br><br>---<br><br>Your case description:<br><br>Re: CS1214752 - How Did We Do?  <br>  <br><br>---<br><br>If you would like to close your case early, please click [here](mailto:support.digitalservices@nhs.net?subject=Accept&body=Do%20not%20delete%20the%20following%20message:%0ARef:MSGNHSD25166028_6oR2letUoBNEnMr "here")<br><br>Kind regards,<br><br>National Service Desk  <br>Digital Operations and Service Management  <br>NHS England <br><br>Interact with your case and take advantage of our customer service knowledge base by visiting our [Customer portal](https://www.support.digitalservices.nhs.uk/)<br><br>Want to know how we handle your data? You can read our privacy policy here:[https://www.nhs.uk/our-policies/privacy-policy](https://www.nhs.uk/our-policies/privacy-policy)|

Thank you for contacting us regarding your reference CS1214752.

Unfortunately, the case is  closed. We have logged a new case for you, and you will soon receive an email with the details. Please be aware that any further updates to the original case will not be actioned and should instead refer to the new case reference you will receive.

Kind regards,

National Service Desk

Digital Operations and Service Management

NHS England

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thank you for contacting the National Service Desk.<br><br>Your case has been logged under reference CS1225473 and assigned to the appropriate team, who will be in touch as soon as possible. <br><br>---<br><br>Your case description:<br><br>Re: CS1214752 - How Did We Do?  <br><br>---<br><br>If you would like to close your case early, please click [here](mailto:support.digitalservices@nhs.net?subject=Accept&body=Do%20not%20delete%20the%20following%20message:%0ARef:MSGNHSD25171763_HDrTnMxFH1hggm8 "here"). <br><br>Kind regards,<br><br>National Service Desk  <br>Digital Operations and Service Management  <br>NHS England <br><br>Interact with your case and take advantage of our customer service knowledge base by visiting our [Customer portal](https://www.support.digitalservices.nhs.uk/)<br><br>Want to know how we handle your data? You can read our privacy policy here:[https://www.nhs.uk/our-policies/privacy-policy](https://www.nhs.uk/our-policies/privacy-policy) |

Regarding your case CS1225473, we have provided the below resolution. 

---

Proposed resolution:

Hi Leon,

There is no requirement to provide us with source IPs as MESH does not use a whitelist to restrict access. However, we do use geo-blocking so your IPs must come from the UK.

Kind Regards

Paddy

---

Your case description:

Re: CS1214752 - How Did We Do?

---

Please do not reply to this email. Use the below links to accept or reject this resolution.

If you are satisfied with this resolution, please click the following link to accept it and close your case:

[Accept Solution](mailto:support.digitalservices@nhs.net?subject=Accept%20-%20CS1225473&body=Do%20not%20delete%20the%20following%20message:%0ARef:MSGNHSD25257581_dVBdqGchBQHoWJV).

If you feel that your case has not been answered or addressed, please click the following link to reject the resolution and reopen your case:

[Reject Solution](mailto:support.digitalservices@nhs.net?subject=Reject%20-%20CS1225473&body=Reason%20for%20Rejecting%20CS1225473:%0A%0A%0ADo%20not%20delete%20the%20following%20message:%0ARef:MSGNHSD25257581_dVBdqGchBQHoWJV).

If we do not hear from you within 7 days your case will be closed.

Kind regards,

National Service Desk

Digital Operations and Service Management

NHS England

Regarding your case CS1225473, we have recently provided you a resolution.

We would be delighted if you could share your experience of the service you have received by clicking this link to complete a [Customer Satisfaction Survey](https://nhsdigitallive.service-now.com/assessment_take2.do?sysparm_assessable_type=a0dfbc85c33231001b757bfaa2d3aee7&sysparm_trigger_table=sn_customerservice_case&sysparm_trigger_id=f6a39f91fb70fa90cfc6feceaeefdc5b).

Please do not reply to this email with feedback; only reply if you need further assistance.

---

Your case summary:

Re: CS1214752 - How Did We Do?

---

As we did not hear from you within 7 days, we have closed your case. 

If you still need assistance from us, please respond to this email.
