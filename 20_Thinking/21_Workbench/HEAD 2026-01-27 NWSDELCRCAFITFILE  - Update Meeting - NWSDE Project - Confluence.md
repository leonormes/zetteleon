---
title: "2026-01-13: NWSDE/LCRCA/FITFILE  - Update Meeting - NWSDE Project - Confluence"
source: https://fitfile.atlassian.net/wiki/spaces/NP/pages/2561474561/2026-01-13+NWSDE+LCRCA+FITFILE+-+Update+Meeting
captured: 2026-02-03T16:19:47+00:00 2026-02-03T16:19:47+00:00
status: processing
tags:
  - input
type: head
---
## Raw Output / Content
Meeting Date: 27 Jan 2026

## Participants

- **FITFILE:**
- **NWSDE (Arden & GEM CSU):** Helen Duckworth. Richard Johnson
- **LCRCA**: John White, Anthony Mitchell, J Davitt
- Apologies: , Lynn Shelbourne

## Agenda

Discussion on current progress

## Meeting Recording

Meeting not recorded.

## Meeting Summary

### Key Takeaways

- Jamie and J appreciated the FITFILE teams patience with the LCRA systems as there have been some issues while LCRA work through them.
- J mentioned that he had messaged about when they are ready for connection and to ask about the estimated monthly “running costs” of the Azure resources (this can then be used to submit the change request for approval).
- Richard Johnson agreed to check with Jaimie Reeves regarding the final timeline for resources available and get back to those on the call later that same day.
- Discussion about who from FITFILE can and should be able to access the NWSDE, DSCRO and LCRCA Nodes. The team confirmed that FITFILE members of staff can access the Nodes for installation purposes but not to access data. This means that FITFILE cannot run the installation as a managed service. Further discussion required with FITFILE and NWSDE regarding the potential use of API scripts templates that NWSDE can run independently.
- Richard Johnson also agreed to check with Jamie Reeves regarding the above access request and what the DSCRO and/or Arden & Gem can approve. Richard to respond to FITFILE on this.
- will send email with the remaining data questions for the team to fill in. They are not blockers but would be good to have filled in, especially the one about which fields will be used for matching.

## Action Items

<table><colgroup><col></colgroup><tbody><tr><td></td><th rowspan="1" colspan="1"><div><p><strong>Action Item</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Comments</strong></p><figure></figure></div></th></tr></tbody></table>

<table><colgroup><col></colgroup><tbody><tr><td></td><th rowspan="1" colspan="1"><div><p><strong>Action Item</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Comments</strong></p><figure></figure></div></th></tr><tr><td>1</td><td rowspan="1" colspan="1"><div><span><input></span><p>to send data questions to be completed</p></div></td><td rowspan="1" colspan="1"><p>Email sent on <span><span>27 Jan 2026</span></span></p></td></tr><tr><td>2</td><td rowspan="1" colspan="1"><div><span><input></span><p>to provide the the estimated monthly “running costs” of the Azure resources by <span><span>29 Jan 2026</span></span></p></div></td><td rowspan="1" colspan="1"><p>Email sent on <span><span>29 Jan 2026</span></span></p></td></tr><tr><td>3</td><td rowspan="1" colspan="1"><div><span><input></span><p>Richard Johnson to check with Jaimie Reeves regarding the final timeline for resources available and advise all by email</p></div></td><td rowspan="1" colspan="1"><p>Email sent on <span><span>27 Jan 2026</span></span></p></td></tr><tr><td>4</td><td rowspan="1" colspan="1"><div><span><input></span><p>Richard Johnson to check with Jamie Reeves regarding the above access request and what the <span>DSCRO</span> and/or Arden &amp; Gem can approve.</p></div></td><td rowspan="1" colspan="1"><p>Information shared with FITFILE on email on 27/01/2026</p></td></tr></tbody></table>

## Raw Output / Content
Meeting Date: 26 Nov 2025

## Participants

- **FITFILE:** @Susannah Thomas @Helena Ahlfors @Robin Mofakham @Weronika Jastrzebska @danielle.hawley @enric-serra @Ollie Rushton @Leon Ormes
- **NWSDE (Arden & GEM CSU):** Colleen Knight, Lamin Samba, Jamie Reeve, James Richardson

## Agenda

1. Intro and brief overview of project
2. Tech diagram
3. Tech discovery - questions and overview of installation
4. Project management - timelines, communication, regular meetings, project team, Review Boards, change freezes
5. AOB

## Meeting Recording

Link to recording of the meeting: [FITFILE/NWSDE - Tech discovery meeting](https://fathom.video/share/FABMospEJnZ4Rs_H1doBA4KV_Hju4HBA)

## Meeting Summary

### Key Takeaways

- **Deployment Plan:** The FITFILE Node will be deployed via Terraform into a new /24 VNet in the DSCRO subscription. FITFILE will use just-in-time (JIT) access and shut down its Bastion/jump box when not in use to manage costs.
- **Critical Decision:** A choice is needed between private and public UI access. Private access requires distributing a custom certificate chain to user devices (e.g., AVDs), while public access (via Azure Front Door) uses standard, auto-managed certificates.
- **Data Flow Confirmed**: The DSCRO team will generate a "rainbow table" of pseudo-IDs against all NHS numbers. The FITFILE Node will then use this table to map its probabilistically matched cohort to the required pseudo-IDs, which are then passed to the ICB.
- **Scheduling:** The project is paused until the SDE team provides the use case and advises on priority. Deployment is targeted for after 5th January 2026, pending this input.

### Project Overview & Data Flow

- The project objective is to link NHS data with LCA worklessness data without moving identifiable LCA data into the SDE environment.
- **Architecture**: A federated "node and spoke" model.
	- Node A (LCA): Holds ~40k identifiable records.
	- Node B (DSCRO): Holds ~600k PDS records for Cheshire & Mersey.
- **Probabilistic Matching**: Required because LCA data lacks NHS numbers, enabling linkage despite typos.

**Data Flow**

1. SDE sends a query to the LCA node.
2. LCA node hashes identifiable data (name, DOB, postcode).
3. Hashed data is returned to the DSCRO node.
4. DSCRO node probabilistically matches hashes to PDS records.
5. Matched NHS numbers are mapped to pseudo-IDs using the pre-generated "rainbow table."
6. A list of pseudo-IDs is returned for use with ICB data.

### Deployment & Infrastructure

- **Location:** UK South region.
- **Networking:** A new /24 VNet will be created for the node.
- **Outbound Traffic:** FITFILE can route traffic through an existing firewall/NAT gateway if details are provided.
- **Terraform Service Principle**: Requires Contributor role + a specific permission to assign a role to the AKS service principle.
- **FITFILE team**: Will use JIT access via federated accounts.
- **Permissions requested from NWSDE** \- access to resource group, 8 hour window given to FITFILE to do the work.
- **FITFILE Team:** Will use JIT access via federated accounts.
- **Cost Management:** The Bastion and jump box VMs will be shut down when not in use to control costs.
- **Firewall rules** to be provided by FITFILE.
- **Certificates** \- Private DNS zones in Azure. National DNS team for certificates.

### UI Access & Certificate Strategy

- Certificate management needs to be considered to avoid browser warnings, with the target being automated issuance and a robust renewal process; the best solution will depend on where UI access is coming from.
- All of the available options will be detailed in the High Level Design; but the preferred options are a FITFILE managed Public CA through the ACME protocol, or a Hybrid approach where the NWSDE manages their own certificate issuer while leveraging FITFILE’s cert-manager for automated certificate requests and deployments.
- The decision requires input from the SDE team (Helen, Richard, James) on the project's use case and security requirements.

### Project Management & Scheduling

- **Service Desk:** All maintenance and scheduling requests will be routed through the SDE's ServiceNow portal.
- **SDE Contacts**: Lamin Samba (Infrastructure), James Richardson (Data).
- **Scheduling**: Deployment is targeted for after 5th January 2026.
- **Blocker**: The SDE team must define the live use case and priority to enable scheduling.
- **Change Approvals:** All required changes (e.g., firewall rules) are internal to the SDE/DSCRO team, simplifying the approval process.

## Action Items

1

2

3

4

5

6

7

8

| **Action Item** | **By Whom** | **Completed** | **Comments** |
| --- | --- | --- | --- |
| Confirm the project's use case and priority with Helen Duckworth and the SDE team. | Collen Knight |  |  |
| Provide the ServiceNow portal email for maintenance requests. | Collen Knight |  |  |
| Provide the /24 VNet CIDR range for the DSCRO node. | Jamie Reeve |  |  |
| Schedule a follow-up meeting with Helen, Richard, and James to decide on private vs. public UI access. | Colleen Knight / Jamie Reeve |  |  |
| Distribute the "Certificate Options" document to the SDE team for review. | @Robin Mofakham | 05/12/2025 | These will be detailed in the High Level Design Document. |
| Finalise and share the High-Level Design (HLD) document. | @Robin Mofakham | 05/12/2025 |  |
| Provide firewall rules to Jamie Reeve | @Robin Mofakham | 05/12/2025 |  |
| Schedule a data-focused meeting with Colleen's team to detail the pseudo-ID generation process. | @Susannah Thomas @Helena Ahlfors |  |  |

## Raw Output / Content
**Meeting on**: 18 Dec 2025

## Participants

- **FITFILE:**
- **NWSDE (Arden & GEM CSU):** James Richardson, Richard Johnson, Anthony Mitchell
- **LCA**: John White, Phil McHale, Lynn Shelborne, J Davitt, Jamie Wade
- **Apologies:** Lamin Samba, Helen Duckworth, Colleen Knight, Susannah Thomas, Enric Serra

## Agenda

Follow up on outstanding data questions

## Meeting Recording

Link to the meeting recording: [Impromptu Microsoft Teams Meeting](https://fathom.video/share/pegDrTB6ph2mq5scgbLnepsaMyTAtdRV)

## Meeting Summary

### Key Takeaways

- FITFILE will manage the POC query. This simplifies setup by avoiding complex user access provisioning for NWSDE staff.
- The NWSDE Node will likely be on DSCRO infrastructure. This is the most practical option, as DSCRO holds the PDS data needed for the linkage.
- Data will flow from the Node to a pre-existing ARDEN & GEM blob storage. This creates a seamless, end-to-end pipeline for NWSDE staff to provision data for researchers.
- NWSDE will pre-pseudonymise NHS numbers. This simplifies the matching process by removing the need for FITFILE to handle raw NHS data.

### Node Location & Data Flow

- NWSDE ’s Node location was undefined, creating uncertainty about data access and the end-to-end pipeline.
- The Node will likely be on DSCRO infrastructure, as it holds the PDS data.
- PDS data will be output as CSVs into a DSCRO blob storage account.
- The combined dataset will be saved to a pre-existing ARDEN & GEM blob storage account.
- This output location is already accessible to NWSDE, creating a seamless pipeline to researcher workspaces.

### POC Query Execution

- Granting NWSDE direct access to the FITFILE Node for the POC would require complex networking and onboarding.
- FITFILE will run the initial probabilistic matching query as a managed service.
- This simplifies setup by avoiding complex user access provisioning. NWSDE will define parameters, and the FITFILE Node will execute the query and deliver the output.

### Data Matching & Privacy

- **Pseudonymisation**: NWSDE will pre-pseudonymise NHS numbers before inputting them to the Node, simplifying the matching process.
- **Matching Fields:** The initial probabilistic matching will use:
	- Full postcode
	- Date of birth (or derived version)
	- Forename & Surname
	- Gender
- **Privacy:** Only hashes of matching fields leave the Node. The original raw data (e.g., full DOB) remains within its source Node.
- **Future State:** The POC's success could lead to a sustainable, repeatable linkage for data refreshes, pending a formal decision.

## Action Items

<table><colgroup><col> <col> <col> <col> <col></colgroup><tbody><tr><td></td><th rowspan="1" colspan="1"><div><p><strong>Action Item</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>By Whom</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Completed</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Comments</strong></p><figure></figure></div></th></tr><tr><td>1</td><td rowspan="1" colspan="1"><p><span>NWSDE</span> to finalise location of the <span><span><span>SDE</span></span></span> Node</p></td><td rowspan="1" colspan="1"><p>James Richardson</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>2</td><td rowspan="1" colspan="1"><p>Provide FITFILE with specs for the input (<span>DSCRO</span>) and output (ARDEN &amp; GEM) blob storage accounts</p></td><td rowspan="1" colspan="1"><p>James Richardson</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>Send to Weronika</p></td></tr><tr><td>3</td><td rowspan="1" colspan="1"><p>Send <span>LCA</span> ethnicity codes to James for comparison with <span>SDE</span> definitions</p></td><td rowspan="1" colspan="1"><p>John White</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>4</td><td rowspan="1" colspan="1"><p>FITFILE to review the storage account specs to confirm technical feasibility</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>5</td><td rowspan="1" colspan="1"><p>Schedule a follow-up call in the new year to define matching parameters and test field combinations</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>Susannah to set up</p></td></tr></tbody></table>

## Raw Output / Content
Meeting Date: 11 Dec 2025

## Participants

- **FITFILE:**
- **NWSDE (Arden & GEM CSU):** Helen Duckworth, Lamin Samba, James Richardson, Richard Johnson
- **LCA**: John White, Phil McHale

## Agenda

1. Brief overview of project and data aims
2. Data discovery questions

## Meeting Recording

Link to recording of the meeting: [NWSDE / FITFILE - Data Discovery Meeting](https://fathom.video/share/Aq_7cNzyBs2AL3Sm6EWGbZqT2xqRKs-7)

## Meeting Summary

### Key Takeaways

- Link LCA employment data (~40k records) with NWSDE PDS data (~600k records) to add NHS numbers, using FITFILE’s privacy-preserving probabilistic matching.
- The process uses bloom filters and hash embeddings to match encrypted data, achieving a high recall of 96–99.8% with zero false positives in validation tests.
- LCA will provide employment data via Excel; NWSDE will provide PDS data via CSVs in a private Azure Blob Storage, requiring bespoke networking for access.
- Next Steps: NWSDE and LCA will complete the data discovery spreadsheet. A follow-up meeting is scheduled to finalise the pseudonymisation strategy and review the completed spreadsheet.

### Project Goal & Scope

- Add NHS numbers to LCA employment data by linking it with NWSDE PDS data.
- Data Sets:
	- LCA Employment Data: ~40,000 records, 34 columns.
	- NWSDE PDS Data: ~600,000 records from the Cheshire & Merseyside ICB catchment.
- Matching Approach: Probabilistic matching was chosen over deterministic to handle expected data quality issues (typos, variations) and maximise match rates.

### Probabilistic Matching Method

- **Core Technique:** The process uses bloom filters and hash embeddings to compare encrypted data, eliminating the need to expose cleartext identifiers.
- **Bloom Filters**:
	- Identifiers (e.g., name) are split into bigrams (two-letter pairs).
	- Each bigram is hashed and stored in a bit array (the bloom filter).
	- Similarity between records is approximated by comparing their bloom filters.
- **Hash Embeddings:**
	- An extension that learns associations between name variants (e.g., "Catherine" and "Kathy").
	- This significantly improves matching performance for non-obvious variations.
- **Validation Results** (on FERBAL-4 benchmark dataset):
	- Recall: 99.8% (with 10 fields) → 96% (with 4 fields).
	- False Positives: 0%.
- **Matching Score Threshold:**
	- The tool assigns a score to each potential match (default: 0.5).
	- This threshold can be adjusted to balance false positives and negatives, which is a key requirement for the research-based project.

### Data Discovery & Logistics

- **Data Formats:**
	- LCA: Excel file.
	- NWSDE: CSV extract from SQL database for the POC.
		- Future: Parquet or direct SQL connection for production.
- **Data Location & Security:**
	- NWSDE: CSVs will be placed in a private Azure Blob Storage.
	- Access: Requires bespoke networking (private endpoint) and credentials (SAS, service principal).
- **Data Ownership:**
	- LCA: John White.
	- NWSDE: James Richardson.
- **Data Quality:**
	- LCA: Data is pre-validated for performance reporting.
	- NWSDE: Will confirm existing quality checks and potential record duplication.

## Action Items

<table><colgroup><col></colgroup><tbody><tr><td></td><th rowspan="1" colspan="1"><div><p><strong>Action Item</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>By Whom</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Completed</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Comments</strong></p><figure></figure></div></th></tr><tr><td>1</td><td rowspan="1" colspan="1"><p>Complete and return the data discovery spreadsheet</p></td><td rowspan="1" colspan="1"><p><span>NWSDE</span> &amp; <span>LCA</span></p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>2</td><td rowspan="1" colspan="1"><p>Circulate the updated data discovery spreadsheet and presentation</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>12/12/2025</p></td><td rowspan="1" colspan="1"></td></tr><tr><td>3</td><td rowspan="1" colspan="1"><p>Schedule a 30-min follow-up meeting to finalise pseudonymisation strategy for next week</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>4</td><td rowspan="1" colspan="1"><p><span>NWSDE</span> to confirm <span>PDS</span> ingest (live SQL vs <span>CSV</span> /Parquet) w/ John + Helen</p></td><td rowspan="1" colspan="1"><p>Richard Johnson</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>5</td><td rowspan="1" colspan="1"><p>FITFILE to confirm Parquet ingest support</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>6</td><td rowspan="1" colspan="1"><p><span>NWSDE</span> to define Azure Blob networking (private endpoint) + auth (<span>SAS</span> /Entra ID) with FITFILE</p></td><td rowspan="1" colspan="1"><p>James Richardson &amp;</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p><span>NWSDE</span> will need to set up bespoke networking, because the data sits on Blob storage accounts that can't be accessed from the open internet. James and Robin to discuss further</p></td></tr><tr><td>7</td><td rowspan="1" colspan="1"><p><span>NWSDE</span> to confirm <span>PDS</span> resident/registered counts for 6 LAs</p></td><td rowspan="1" colspan="1"><p>Richard Johnson</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>8</td><td rowspan="1" colspan="1"><p>Confirm <span>PDS</span> columns + <span>LCA</span> spec w/ Helen</p></td><td rowspan="1" colspan="1"><p>Richard Johnson</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>Check with Helen Duckworth on what columns are required for the <span>LCA</span> Spec</p></td></tr></tbody></table>

## Shared Documentation

Updated Data Discovery questions

PowerPoint Presentation

## Raw Output / Content
Meeting Date: 13 Jan 2026

## Participants

- **FITFILE:**
- **NWSDE (Arden & GEM CSU):** Helen Duckworth
- **LCRCA**: John White, Anthony Mitchell, J Davitt, Lynn Shelbourne

## Agenda

1. Discuss current progress
2. Review Actions Register
3. AOB

## Meeting Recording

Link to recording of the meeting: [NWSDE <> FITFILE Discussion](https://fathom.video/share/MxGtzJD7bAieiGbxYHS-FsdKPfq1wLE8)

## Meeting Summary

### Key Takeaways

- **Start Date Pending:** The project start date is pending the secondment of a technical resource to the DSCRO team. Helen Duckworth will provide a start date tomorrow (14th Jan).
- **Costs Approved**: John White confirmed LCRCA will cover all Azure consumption costs from an existing budget, removing a potential blocker.
- **Technical Blockers**: Two key technical issues require resolution:
	- VM Size: LCRCA 's standard VM is smaller than FITFILE's recommended size. Robin Mofakham will provide usage data to justify a quota increase.
	- Data Ingestion: FITFILE to confirm support for Parquet files and direct Blob Storage access.
- **Discovery Gaps:** FITFILE will resend the Tech and Data Discovery questions to NWSDE to gather all remaining technical and data requirements.

### Project timeline and start date

- The project start date is pending the secondment of a technical resource to the DSCRO team. This secondment is an Information Governance (IG) process.
- Helen Duckworth will confirm the start date tomorrow (14th Jan) after speaking with Colleen Knight (Associate Director of Data).
- Installation Location: Confirmed as the DSCRO area.

### Budgeting and cost considerations

- **Funding:** John White confirmed LCRCA will cover all Azure consumption costs from an existing budget.
- **Cost Estimate:** Robin Mofakham will provide some high-level estimates on potential Azure consumption costs.
- **Tracking**: Anthony Mitchell confirmed all Azure resources will be tagged to enable precise cost tracking.

### Project team and Governance

- The group discussed the need for a project team and change management process, particularly around any changes required to the Azure environment. It was determined that a formal project team is deemed unnecessary for this proof-of-concept.
- Helen Duckworth (NWSDE) and John White (LCRCA) will serve as primary contacts.
- Engineers will submit change requests, which Project Managers (e.g. Lynn Shelbourne) will monitor.

### Technical and data questions

- Helena advised that FITFILE had previously shared a set of technical and data-related questions with NWSDE and LCRCA. Both parties confirmed they would review what was still outstanding to ensure all necessary information was gathered before the installation could begin.
- **VM size mismatch:** LCRCA 's standard VM size is smaller than FITFILE's recommended size. Robin Mofakham will provide usage data to justify a quota increase, enabling LCRCA to match the standard.
- **Data Ingestion Capabilities**: FITFILE to confirm support for:
	- Parquet data files
	- Direct access to Azure Blob Storage

## Action Items

<table><colgroup><col></colgroup><tbody><tr><td></td><th rowspan="1" colspan="1"><div><p><strong>Action Item</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>By Whom</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Completed</strong></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p><strong>Comments</strong></p><figure></figure></div></th></tr><tr><td>1</td><td rowspan="1" colspan="1"><p>Review technical questions and advise <span>NWSDE</span> and <span>LCRCA</span> what is outstanding</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>Liaise with Jamie Reeve at <span>NWSDE</span> and J Devitt / Jamie Wade at <span>LCRCA</span></p></td></tr><tr><td>2</td><td rowspan="1" colspan="1"><p>Provide VM usage data to <span>LCRCA</span> to justify a quota increase.</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>3</td><td rowspan="1" colspan="1"><p>Confirm support for Parquet files and direct Blob Storage access</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr><tr><td>4</td><td rowspan="1" colspan="1"><p>Review outstanding data questions and advise <span>NWSDE</span> &amp; <span>LCRCA</span> what is outstanding</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"><p>Liaise with John White at <span>LCRCA</span> and James Richardson at <span>NWSDE</span></p></td></tr><tr><td>5</td><td rowspan="1" colspan="1"><p>Confirm propose start date</p></td><td rowspan="1" colspan="1"><p>Helen Duckworth</p></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td></tr></tbody></table>
