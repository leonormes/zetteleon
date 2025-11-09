---
aliases: []
confidence: 
created: 2025-10-20T12:36:41Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [nnuh]
title: Critical Discussion Points and Decisions
type:
uid: 
updated: 
version:
---

## NNUH SDE Node Installation Kick-off Meeting: Critical Discussion Points and Decisions

This report synthesizes information relevant to the NNUH Secure Data Environment (SDE) Node Installation Kick-off Meeting, focusing on critical discussion points, immediate decisions required, network configuration, data storage, compliance requirements, and outstanding action items.

### 1. Project Context and Meeting Purpose

The NNUH SDE Node Installation project aims to establish a secure environment for research using patient data, operating within a stringent regulatory framework. The Kick-off Meeting, most notably documented as occurring on **October 20, 2025**, served as a critical forum to review project progress, address outstanding action items, resolve technical and data discovery questions, and align on future steps. Key objectives included reviewing the updated network diagram, confirming project team roles, and aligning on timelines and communication routes.

### 2. Compliance Requirements: GDPR, ISO 27001, and NHS Policies

The project operates under strict regulations to protect patient data. Adherence to these is paramount:

- **GDPR and Data Protection Act 2018:** Mandate robust data protection, including lawful processing, data subject rights, and security measures. FITFILE's platform is designed for GDPR Article 25 compliance ("Data protection by design and by default").
- **NHS Data Security Standards:** Provide specific guidance for the NHS, covering access management, encryption, incident response, and information governance. FITFILE's platform aligns with these standards.
- **ISO 27001:** FITFILE's technical documentation indicates adherence to ISO 27001 for Information Security Management Systems.

**Core Compliance Objectives:**

- Patient Privacy
- Ethical Data Use
- Risk Mitigation (breaches, unauthorized access, re-identification)
- Trust Maintenance
- **Data Protection Impact Assessment (DPIA):** This is a critical path item, prerequisite for technical sign-off, training, and moving forward with key project milestones. NNUH is awaiting final approval from their R&D department. Feedback from Raja Rehman (MKUH) has prompted FITFILE to update the DPIA, confirming non-use of Java and detailing alternative approaches.

### 3. FITFILE Data Handling Capabilities for NNUH OMOP Data

FITFILE's platform supports OMOP data ingestion and processing, with integrated data linkage and privacy treatments dynamically informed by data sensitivity and research objectives.

- **OMOP Data Ingestion:** Source data will be ingested as **flat files (CSV)**, a preference confirmed by NNUH for speed and MVP setup. FITFILE supports ingestion via UI or API. The Hyve is responsible for harmonizing raw data into the OMOP CDM.
- **Data Linkage:** FITFILE offers **FITanon** (Zero-Knowledge Proof for irreversible anonymization) and **FITtoken** (deterministic pseudonymization for reversible linkage). Linkage can be deterministic or probabilistic.
- **Privacy Treatment Protocol (via Query Plan):**
  - **Sensitive Field Identification:** FITFILE's PII detection identifies sensitive fields (e.g., Date of Birth, NHS Numbers).
  - **Privacy Techniques:** Aggregation, Generalisation, K-anonymity, I-diversity, t-closeness, Perturbation, Rounding, Suppression, Sampling, Differential privacy, Noise addition, Permutation.
  - **Utility vs. Privacy Balancing:** Data elements can be assigned **coefficients ('weights')** to prioritize crucial fields, balancing utility and privacy.
  - **Granular Control:** Supports selective application, type preservation, and proper NULL value handling for OMOP compliance.

#### Pharmacy Data Mapping Challenges

- **Current State:** Medication data is currently "messy" with raw string values. The Hyve has created semantic mappings for synthetic data.
- **New EPMA System:** A new EPMA system is launching, expected to improve data quality but with an unknown impact on format and new drug introductions.
- **Mapping Limitations:** The Hyve can apply existing mappings, but live data may have a wider variety of drug values. Coverage is uncertain without a comprehensive list.
- **Integration Delay:** Pharmacy data integration is delayed until **March 2026** due to NNUH resource constraints and the new EPR system. Postponing integration until the new EPR system goes live is suggested.

### 4. NNUH Network Configuration and Data Storage Decisions

Significant progress has been made in defining the network configuration and data storage.

#### Network Configuration

- **Inbound Traffic:** Routed through **NNUH's on-premise firewalls**.
- **Outbound Traffic:** Routed directly from the **Azure vNet via a NAT Gateway** with a static IP for whitelisting.
- **VNET CIDR Range:** A **/24 VNet CIDR range** has been approved.
- **Engineer Access:** NNUH approved a **Bastion host deployment** via FITFILE Terraform for engineer access to the private VNET.
- **Certificate Management:** NNUH confirmed their preference for **FITFILE to manage certificates via Cloudflare**, with NNUH establishing a **private DNS zone in Azure**. This was reviewed and agreed upon by the NNUH Cyber Team.
- **DNS:** NNUH will establish a **private DNS zone in Azure** for secure internal name resolution.
- **NDOO Management:** NNUH confirmed they will manage the **National Data Opt-Out (NDOO) process locally** on source data *before* ingestion.
- **Network Diagram:** Updated to reflect these configurations and shared with NNUH. The RITS process has seen approval for RITS 2500006 by Jeffrey Mugabe.
- **Bandwidth:** An estimated **50-100 Mbps symmetric VPN connection** was suggested for the secure research environment.

#### Data Storage Decision (Confirmed)

- NNUH, via Mike Shemko, confirmed a preference for **flat files (CSV)** for source data ingestion, citing speed and existing MVP setup. Mongo is not supported by FITFILE. This decision is critical for finalizing the network diagram and RITS submission. The definitive storage location for harmonised OMOP data (FITFILE Node's internal PostgreSQL, Azure PostgreSQL, or NNUH-hosted PostgreSQL) requires further confirmation.

### 5. MESH API Integration (for National Data Opt-Out - NDOO)

While NNUH confirmed they will manage the **NDOO process locally on source data *before* ingestion**, FITFILE has the capability to utilize the MESH API for NDOO filtering. FITFILE's technical conformance certification for the MESH API remains a core capability.

### 6. Critical Discussion Points & Immediate Decisions Required

The kick-off meeting is crucial for confirming implementation details and resolving remaining critical items:

- **Defining Research Objectives for Privacy Treatment Guidance:**
  - **Discussion:** Clarify NNUH's primary research objectives to guide the selection and weighting of privacy treatments within the Query Plan, balancing data utility with GDPR compliance.
  - **Immediate Decision:** Agree on the process for defining and documenting these research objectives.
- **Data Storage Implementation Details:**
  - **Discussion:** Confirm practical implementation of storing OMOP data as flat files, including ingestion methods and management.
  - **Decision:** Formalize the chosen method for flat file ingestion and management. Further confirmation is needed on the final storage option for harmonised OMOP data.
- **Pharmacy Data Integration Scope:**
  - **Discussion:** Pharmacy data integration is delayed until March 2026. The Hyve can perform partial semantic mappings.
  - **Immediate Decision:** Decide whether to proceed with **partial mapping** now or **fully descope** this data source until March 2026.
- **Audit Trail Requirements:**
  - **Discussion:** Define NNUH's specific audit trail requirements for flat file storage, informed by DPIA focus on risk mitigation.
  - **Immediate Decision:** Agree on audit trail requirements and the best option for NNUH. Mike Shemko to confirm internally.
- **Separate Credentials for Synthetic and Live Data:**
  - **Discussion:** Confirm if NNUH will provide separate credentials for synthetic and live data access.
  - **Immediate Decision:** Confirm the provision of separate credentials. Mike Shemko to query Ben Goss regarding platform support and provisioning.
- **Date of Birth Field Inclusion:**
  - **Discussion:** Confirm that the data extract will be updated to include the full date of birth (currently only the year is provided).
  - **Immediate Decision:** Confirm the inclusion of the full date of birth. Mike Shemko is to update and resend files.

### 7. Overdue Action Items: Status and Impact

Several action items from the NNUH Actions Register require resolution:

- **Decided/Confirmed:** Data Storage (Flat Files), NDOO Management (Local), Date of Birth Field (Update confirmed), Network Configuration (largely resolved).
- **Pending Discussion/Confirmation:** Audit Trail Requirements (Action 15), Separate Credentials (Action 19), Database Credentials Provisioning (Action 13).
- **Delayed/Requires Decision:** Pharmacy Data Integration (Actions 9 & 10).
- **Blocked (for Diagram Finalization & RITS Submission):** Finalization of the network diagram and RITS submission depend on confirmed decisions and resolution of pending items (e.g., audit trails, separate credentials, next hop IP address provisioning for FITFILE's route table).

### 8. Key Stakeholders Requiring Input and Action

Successful progression relies on collaboration with key stakeholders:

#### NNUH Stakeholders

- **Mike Shemko (Head of Data Science):** Key contact for data storage, NDOO, date of birth, audit trails, pharmacy data scope, and database credentials. Input needed today on audit trails, pharmacy data scope, and separate credentials.
- **Ben Goss (Technical Authority - Digital Health):** Involved in network routing and credentialing. Input needed to confirm separate credentials and check FITFILE Engineer access to the VNET.
- **NNUH Cyber Security Team / IT/Networking/IG Teams:** Responsible for network approvals and adherence to NHS standards. Crucial for DPIA risk assessment. Formal review and sign-off on the updated network diagram and RITS submission are required.

#### FITFILE Stakeholders

- **Susannah Thomas (Project Director):** Coordinating communications and RITS submission. Facilitate decisions on pharmacy data scope and audit trails.
- **Oliver Rushton / Leon Ormes:** Technical leads responsible for diagram updates and implementation. Document decisions and ensure technical alignment.
- **Weronika Jastrzebska:** Tracking actions and progress. Update Actions Register.

#### The Hyve Stakeholders

- **Liam Glueck, Stefan Payralbe:** Provide expertise on data harmonization and pharmacy data mapping feasibility.
