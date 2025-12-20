---
aliases: []
confidence: 
created: 2025-10-13T10:06:14Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: NNUH Deployment Project Summary & Meeting Preparation
type:
uid: 
updated: 
version:
---

This document synthesizes available information regarding the NNUH Secure Data Environment (SDE) Node Installation kick-off meeting and the ongoing deployment project. It draws upon the provided agenda and historical communications to provide a comprehensive overview for meeting preparation.

**1. Welcome and Introductions**

- While the agenda includes this item, no specific historical details from past meetings regarding the exact content of "Welcome and Introductions" were found in the provided communications. The invitation from Mark Dines-Allen establishes the context for the kick-off meeting.

**2. SDE Update**

- **Historical Context:** Ongoing work and queries related to the East of England Secure Data Environment (SDE) for NNUH are documented, particularly concerning network infrastructure.
- **Key Points:**
  - Outstanding queries on the Network Telecoms questionnaire regarding network speed, bandwidth, user numbers, service usage history, and configuration confirmation dates were raised by Kailesh Devlukia (NNUH) on August 4th, 2025. These are tracked in the NNUH Actions Register.
  - Mike Shemko (NNUH) is tasked with addressing these network-related queries. His involvement in data and network infrastructure discussions is noted across several documents.
  - Jeffrey Mugabe (NNUHFT) approved the RITS 2500006 from the Network side on August 13th, 2025.
  - Susannah Thomas (FITFILE) and others have reviewed network telecommunications requests, including discussions on firewall configurations and IP address provisioning.

**3. NNUH Actions Register Resolution and Outstanding Items**

- **Context:** The NNUH Actions Register details numerous outstanding actions, many overdue as of late September/early October 2025, covering data transition, content, technical infrastructure, and governance. The meeting agenda explicitly includes discussing these items and next steps towards deployment.
- **Key Outstanding Actions & Discussions:**
  - **Data Storage Decisions (Critical Blocker):** A decision is critically needed from Mike Shemko (NNUH) regarding the preferred storage option for harmonised OMOP data. Options discussed include flat files or PostgreSQL (FITFILE Node, Azure PostgreSQL, or NNUH hosted PostgreSQL). Mongo is noted as not being a supported solution. This decision is vital for finalizing the network diagram. Discussions have also focused on NNUH needing to decide on audit trail requirements and the data storage approach.
  - **Pharmacy Data Integration:** Integration of pharmacy data is delayed until March 2026 due to NNUH resource constraints, with a suggestion to postpone until the Trust EPR goes live. The Hyve can perform partial semantic mappings of drug field combinations, but the percentage of record coverage is uncertain without a full list of drug values. Mike Shemko is to verify any changes in medication data format with the pharmacy team.
  - **National Data Opt-Out (NDOO):** Confirmation is pending from Mike Shemko (NNUH) on whether NDOO will be managed locally before data ingestion. Further discussion is needed on the national opt-out implementation for NNUH.
  - **Date of Birth Field:** Mike Shemko needs to confirm the update of the data extract to include the full date of birth (currently only the year is provided).
  - **Audit Trail Requirements:** Confirmation is awaited from NNUH regarding specific audit trail requirements.
  - **Database Credentials:** Mike Shemko is to raise a query with Ben Goss regarding platform support and provisioning for database credentials. The security team is to be consulted on database credential provisioning.
  - **DPIA Progress:** FITFILE/HIE are to check the progress of the Data Protection Impact Assessment (DPIA) with John Mules.
  - **Network Diagram Update:** The NNUH networking diagram update is ongoing but blocked by the data storage decision. Networking information has been received, and NNUH is amenable to a Bastion deploy via FITFILE Terraform. Inbound traffic will route via on-premise firewalls, and outbound traffic will use a NAT Gateway from the Azure vNet. Fitfile is to update the network document and share it with stakeholders.
  - **Separate Credentials:** Confirmation is awaited on whether separate credentials for synthetic and live data will be provided.

**4. Project Team at NNUH**

- **Key Personnel Identified:**
  - **Mike Shemko (NNUH):** Head of Data Science. Key contact for data storage, NDOO, date of birth, audit trails, and network queries.
  - **Ben Goss (NNUH):** Technical Authority - Digital Health. Involved in network security requirements and provisioning.
  - **Jeffrey Mugabe (NNUHFT):** Network Architect.
  - **Kailesh Devlukia (NNUH):** Digital Health Business Partner. Raised network queries.
  - **Mark Kelly (NNUH):** Author of the NNUH Network & Telecommunication Information Request.
  - **Mark Dines-Allen (Health Innovation East):** Meeting coordination and agenda setting.
  - **Susannah Thomas (FITFILE):** Project Director. Coordinating communications and actions.
  - **Oliver Rushton (FITFILE):** Technical discussions and diagram updates.
  - **Leon Ormes (FITFILE):** Infrastructure and deployment tasks.
  - **Weronika Jastrzebska (FITFILE):** Technical discussions and action tracking.
- **Action:** The agenda item "Re-confirm project team at NNUH" indicates a need to formally confirm current roles, responsibilities, and escalation routes for these individuals and any other involved team members, including identifying deputies.

**5. Timeline of Project at NNUH**

- **Node Installation:** This initial phase involves ongoing network configuration and approvals, with the RITS process for resource requests noted.
- **Synthetic Data Flow:** Discussions have occurred regarding the transition from synthetic to live data. Mike Shemko confirmed the use of the MVP corpus for cardiovascular data and the NOFORC arthritis registry as a secondary source. Synthetic data was provided with 'year of birth' and a placeholder for NHS numbers. Actions are in place to update data files to include full 'date of birth'.
- **Move to Live Data:** Live EPR data is anticipated to be available in March 2026. The current scope focuses on data currently accessible to NNUH. The timeline for moving to live data is dependent on data storage decisions and the availability of live EPR data.
- **Data Provider Tracker:** Timelines are to be confirmed on the 'Data Provider Tracker.' Specific details of this tracker's content or outputs are not available in the historical records.

**6. Weekly Follow-Up Session**

- **Historical Context:** Past meetings have occurred fortnightly, with suggestions to formalize a recurring schedule.
- **Action:** The agenda item "Discuss and agree weekly follow up session - time/date, etc." requires a decision on a formal weekly meeting cadence.

**7. Follow-Up Communication Routes**

- **Historical Context:** Communications have utilized email and Microsoft Teams.
- **Action:** The agenda item "Agree follow up communication routes – via email or Teams? Ensure good communication flow to keep in line with project deadlines" requires a confirmation of preferred channels for ongoing project updates to maintain efficient communication flow and meet project deadlines.

**8. AOB (Any Other Business)**

- No specific historical data regarding items raised under "Any Other Business" for past NNUH meetings was found in the provided communications.

**Overall Status:**
The NNUH deployment project is actively progressing, with significant groundwork laid in network configurations and initial data discussions. However, critical decisions from NNUH regarding data storage and specific data fields (date of birth, pharmacy data) are pending, which currently impede the finalization of architectural diagrams and subsequent deployment steps. The project timeline, particularly for the transition to live data, is contingent on resolving these outstanding items and the availability of live EPR data in March 2026.
