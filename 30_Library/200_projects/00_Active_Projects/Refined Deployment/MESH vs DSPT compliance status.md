---
created: 2026-05-11T09:16:40+00:00
modified: 2026-05-11T09:50:19+00:00
---
## MESH vs DSPT compliance status

**Bottom line:** your MESH setup looks **operationally in progress**, but I would not call it **fully DSPT-evidenced yet**. The strongest signals are that the mailbox is active and the deployment path is being worked through, while the governance, assurance, and operational-control evidence needed to show DSPT-style completeness is still partly open.

### What’s already in place

- Your internal MESH note says integration depends on an active mailbox, ODS code registration, and HSCN technical standards, and it records the **production mailbox as active and accessible**.
- The NHS Service Desk case `CS1214752` explicitly says: “**Your mailbox is still showing as active on MESH. You should be able to access and use it.**”
- The project summary shows the **combined DCA/DSA** has been sent to the Trust board, but feedback is still pending, and there are **outstanding IP queries** awaiting CUH Legal guidance. It also says the **DPIA is not currently required** pending deployment setup.  
  - [NUH - Project Summary (Internal)](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2727673857/NUH-+Project+Summary+Internal)
  - [NUH project summary spreadsheet](https://fitfileltd.sharepoint.com/:x:/s/FitfileTeam/IQBE2wIeWNorT4fDJ2sgI9IGAZMGJHU382XXenavx2lKHuc?e=opaHlI)
- The deployment-prep note shows the remaining technical/security work is still being defined: **cyber sign-off, CAB cadence, secrets/TLS, observability, backup/restore, RTO/RPO, and support escalation**.
  - [Work Required for Deployment NUH](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2726756353/NUH+-+Project+Directory?atl_f=PAGETREE)

### DSPT mapping

| DSPT area | Status | Evidence |
|---|---|---|
| Governance & legal | Partial | DCA/DSA in review; IP queries open |
| Access governance | Partial | MESH mailbox active, but no explicit DSPT access-review evidence found |
| Audit & monitoring | Partial | Platform notes mention auditing, but no explicit SIEM/export evidence for this MESH thread |
| Business continuity | Partial | RTO/RPO, backup frequency, and restore scope still open |
| Assurance / certification | Not evidenced | I did not find a recorded DSPT submission or “Standards Met” attestation |

### Standards check

The official sources I found describe DSPT as the NHS data-security self-assessment against the 10 standards, and they support DSPT as a baseline for secure NHS data access. I **could not verify an official source that says MESH specifically requires “Standards Met”** as a direct prerequisite, even though your internal notes currently treat it that way.  
- [DSPT portal](https://www.dsptoolkit.nhs.uk)
- [NHS England secure email account guidance](https://www.england.nhs.uk/ourwork/clinical-policy/ordering-medication-using-proxy-access/getting-a-secure-email-account-a-guide-for-social-care-organisations/getting-a-secure-email-account/)
- [NHSmail DSPT guidance](https://support.nhs.net/knowledge-base/data-security-and-protection-toolkit/)

### Open actions

1. Close the combined DCA/DSA and resolve the CUH Legal IP queries.
2. Confirm the cyber sign-off owner/date (`Andy Callow` is named in the deployment notes).
3. Finalise the network/VPN, TLS/secrets, logging, backup/restore, and support model.
4. Capture explicit DSPT evidence: self-assessment status, training/access-review evidence, incident-response testing, and audit-log export.
5. Reconcile the internal assumption that “Standards Met” is mandatory for MESH with the official wording you use in compliance docs.

If you want, I can turn this into a **one-page compliance gap log** or a **DSPT evidence checklist** next.