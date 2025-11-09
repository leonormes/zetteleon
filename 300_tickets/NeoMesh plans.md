---
aliases: []
confidence: 
created: 2025-10-08T11:44:17Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [mesh]
title: NeoMesh plans
type:
uid: 
updated: 
version:
---

Of course. Based on your project's status and the Jira ticket, here is a plan including a draft email to the NHS MESH team and a breakdown of the work required.

---

## Draft Email to NHS MESH Onboarding Team

This email is designed to get clear answers on how your planned code changes will affect your existing approval and to confirm the next steps for getting production credentials.

To: <ssd.nationalservicedesk@nhs.net>

Cc: <itoc.supportdesk@nhs.net> (Optional, to keep the technical team informed)

Subject: MESH API Production Onboarding & Technical Query - FITFILE Group Ltd (ODS: 8KM90)

---

Dear MESH Onboarding Team,

I hope you are well.

We are writing on behalf of **FITFILE Group Limited (ODS Code: 8KM90)** regarding our MESH API integration. We have successfully completed our witnessed test and have received our **Technical Conformance Certificate**.

We are now preparing to move to the production environment and have two key queries before we proceed:

1. **Impact of Technology Change:** We are planning to migrate our MESH client implementation from TypeScript to Python. Could you please advise if this change in programming language will have any impact on the validity of our existing Technical Conformance Certificate? Our core logic for handling messages, errors, and chunking will remain compliant with the MESH API specification, but the underlying codebase will be different.
2. **Confirmation of Production Steps & IP Whitelisting:** To proceed to the live environment, our understanding is that we need to formally request a production mailbox and submit a new CSR for a production TLS certificate, as per the go-live documentation. Could you please confirm if this is correct? Furthermore, could you let us know if we are required to provide a list of static public IP addresses for whitelisting on the production environment?

We are ready to proceed as soon as we have clarification on these points.

Thank you for your guidance.

Best regards,

Leon Ormes

FITFILE Group Limited

---

---

## Recommended Action Plan

Here is a step-by-step plan to manage the work needed to get to the live environment.

### **Phase 1: External Clarification**

Your first priority is to understand the impact of the planned Python migration.

- [ ] **Send the email** drafted above to the NHS MESH team. The response will determine your next steps.

---

### **Phase 2: Internal Preparation (Concurrent Tasks)**

While you await a response from the NHS, your team can prepare internally.

- [ ] **Review Original Submission:** Locate and review the documents and evidence you originally submitted for the witnessed test. This will give you a clear baseline of the functionality that was approved.
- [ ] **Assess Code Impact:** Analyse the planned Python implementation against the original TypeScript code. Confirm that all required features (e.g., error handling, chunked messages) are covered. This will prepare you for a potential re-test.
- [ ] **Identify Production IPs:** If your production environment will use static IP addresses, compile a list now so you have it ready if the NHS team requires it for whitelisting.

---

### **Phase 3: Execution (Based on NHS Response)**

The path forward depends on their answer regarding the technology change.

#### **Scenario A: Your Conformance Certificate REMAINS VALID**

If the NHS confirms that a change in language doesn't invalidate your certificate, proceed with the standard go-live process.

- [ ] **Request Production Mailbox:** Fill out the online form for a live MESH mailbox, providing your ODS code and workflow details.
- [ ] **Generate Production CSR:** Once you receive your live mailbox credentials, generate a new private key and CSR.
  - **Crucially**, use the correct naming convention for the live certificate: `cn={live_mailbox_id}.{ODS}.api.mesh-client.nhs.uk`.
  - Send the CSR and a copy of your conformance certificate to `ssd.nationalservicedesk@nhs.net`.
- [ ] **Sign Connection Agreement:** The connection agreement should be sent to you following the witnessed test. Sign and upload it via the onboarding portal.
- [ ] **Go Live:** Once you have the production TLS certificate and the agreement is signed, you can configure your application to use the live MESH API endpoint and begin operating.

#### **Scenario B: Your Conformance Certificate is INVALIDATED**

If the NHS advises that the code migration requires re-certification, you will need to repeat the conformance step.

- [ ] **Arrange New Witnessed Test:** Contact the MESH team to schedule a new witnessed test for your Python application.
- [ ] **Complete Witnessed Test:** Demonstrate the functionality of your new Python client in the 2-3 hour session.
- [ ] **Follow Scenario A:** Once you receive your new conformance certificate, you can proceed with the steps outlined in Scenario A.
