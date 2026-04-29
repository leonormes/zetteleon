---
captured: "2026-04-28T13:28:28+01:00 2026-04-28T13:28:28+01:00"
created: 2026-04-28T12:28:30+00:00
modified: 2026-04-28T12:48:01+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2727673857/NUH-+Project+Summary+Internal"
status: "processing"
tags: ["input"]
title: HEAD NUH- Project Summary (Internal) - EOE SDE project
type: "head"
---

## Raw Output / Content

![1f4dc](https://fitfile.atlassian.net/gateway/api/emoji/2ee8ef16-a5f2-4936-b96e-9aaf3b029707/1f4dc/path?scale=XXXHDPI)

## NUHProject Summary (Internal)

## Current Status

<table><colgroup><col> <col></colgroup><tbody><tr><th rowspan="1" colspan="1"><p><strong>Updated:</strong></p></th><td rowspan="1" colspan="1"></td></tr><tr><th rowspan="1" colspan="1"><p><strong>Information Governance:</strong></p></th><td rowspan="1" colspan="1"><p><strong>Combined DCA/DSA:</strong> SDE met with Phil Quinlan on 20/04/2026 - Phil confirmed that the draft contract has been sent to the Trust board and requested feedback within 2 weeks, on the basis that the Trust will sign if there are no objections.</p><p>There are still outstanding IP queries from the Trust that the SDE are awaiting guidance from CUH Legal team on, however, Phil does not see these as an issue.</p><p><strong>DPIA</strong>: Not currently required. To be reviewed following agreement on how deployment will be set up.</p></td></tr><tr><th rowspan="1" colspan="1"><p><strong>Current Stage:</strong></p></th><td rowspan="1" colspan="1"><p>Stage 1 - Contract Setup</p></td></tr><tr><th rowspan="1" colspan="1"><p><strong>Implementation and Operation:</strong></p></th><td rowspan="1" colspan="1"><p>Keiran spoke with Phil Quinlan NUH on 20/04/2026 who was receptive to the idea of using the EE-SDE as the AWS hosting to support the FITFILE platform. Phil believes the ability to connect to an on-prem DB via VPN will be achievable.</p><p>RM and Keiran to meet on 01/05/2026 to discuss what would need to be provisioned on the SDE side (network, permissions) and what needs to be in place at NUH. Following which, an all parties meeting will be set up with NUH to agree way forward to kick off deployment.</p></td></tr><tr><th rowspan="1" colspan="1"><p><strong>Next Steps:</strong></p></th><td rowspan="1" colspan="1"><p>Await feedback from Phil Quinlan on the combined DCA/DSA.</p><p>RM and Keiran to hold meeting on 01/05/2026.</p></td></tr></tbody></table>

---

## Project Title

EE SNSDE for R&D–Solution to support data harmonisation, cohort discovery, de-identification and linkage

---

## Project Overview

The Sub-National Secure Data Environment for Research and Development (SNSDE for R&D) for Eastern England (EE) has contracted FITFILE to provide a solution which:

- supports a federated approach across NHS Data Providers to data harmonisation, cohort discovery and de-identification and linkage,
- promotes interoperability, scalability and integration with NHS data provider systems, and
- provides advanced yet user-friendly tooling to support research and innovation.

### Process

- A FITFILE Node is deployed into each NHS Data Provider for data access, data harmonisation to OMOP (delivered via subcontractor The Haive), cohort discovery, de-identification and linkage
- The Nodes are connected via the EE SDE Co-ordinating Node which issues queries and collates results before making the results accessible for onward processing
- Nodes can also operate independently within their own NHS Data Provider environments to support research, planning and care

### The Project Has 7 Key Stages

1. Contract Setup
2. IG Approvals
3. IT Approvals and Implementation Preparation
4. FITFILE Node Installation
5. Network Configuration
6. Initial Data Setup and Testing
7. Live Data Setup, Testing and Sign-off

---

## Project Objectives

1. Data Harmonisation: Electronic Patient Record (EPR) and other data from NHS data provider organisations will be mapped to the OMOP common data model and vocabulary to provide researchers with a shared language when using these data.
2. Cohort discovery: To support researchers in exploring whether the Eastern England NHS data providers have enough patients to meet their research requirements.
3. De-identification and linkage: To remove and/or minimise personally identifiable information in the selected/approved cohorts being surfaced on EE-SDE to meet information governance rules and guidelines and provision harmonised data with OMOP schema, original records and transformation scripts within a researcher's Project Research Environment (PRE) on the SDE.

---

## Project Timeline

<iframe src="https://lref.bilith.com/view?id=conf_ref_link_macro&amp;provider=asana&amp;bundle=asana-confluence&amp;key=lref-asana-task&amp;c-ref_link-asana=&amp;url=https%3A%2F%2Fapp.asana.com%2F1%2F1154800657652998%2Fproject%2F1213910424433720%2Ftimeline%2F1213910877925177&amp;page_id=2727673857&amp;output_type=display&amp;xdm_e=https%3A%2F%2Ffitfile.atlassian.net&amp;xdm_c=channel-com.bilith.lref.confluence-asana__lref-asana-task4155425112017376154&amp;cp=%2Fwiki&amp;xdm_deprecated_addon_key_do_not_use=com.bilith.lref.confluence-asana&amp;lic=none&amp;userAccess=true&amp;cv=1000.0.0-c1ae27966171&amp;traceId=b0d999f0b935192d12a34683157e1a2e&amp;spanId=96c9b0d0db6c9f5e&amp;traceSampled=0&amp;jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2MzNhZTJiOWZlZGM2MTY5YWVkOGY2MDEiLCJxc2giOiJjNTAxMzM5ZWI4NzNiOTM5Mzc2M2FlZmFmYzNhYTY4NmI0N2ZmOTkyYmI1N2IyYWVlYzRmMjg1NjljNjQ3YjFmIiwiaXNzIjoiMTNiNjBjZDktYzU0Ny0zZTRlLTgzNzktNDA1ZGI0ZTQxOTgyIiwiY29udGV4dCI6e30sImV4cCI6MTc3NzM3OTQ4NiwiaWF0IjoxNzc3Mzc5MzA2fQ.1aKzXBATVHmGedlX1p19gqrJM1LGN1KNkxouRpTiyiY"></iframe>

Instagantt snapshot view as at 07/04/2026: [Instagantt](https://app.instagantt.com/shared/69d5093390619c223df6e1f1 "https://app.instagantt.com/shared/69d5093390619c223df6e1f1")

---

## Data Provider Tech and Data Requirements

[20260203\_FITFILE\_NUH\_Tech&DataDiscoveryQuestions.xlsx](https://fitfileltd.sharepoint.com/:x:/s/FitfileTeam/IQBE2wIeWNorT4fDJ2sgI9IGAZMGJHU382XXenavx2lKHuc?e=opaHlI)

---

## Meeting Notes

[NUH - Summary of Meetings and Notes](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2727968769)

---

## Key Documents

[NUH - Key Project Documents](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2734292993)

---

## Project Directory

[NUH - Project Directory](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2726756353)

Related content
