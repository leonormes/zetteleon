---
aliases: []
confidence: 
created: 2025-11-21T10:30:48Z
epistemic: 
last_reviewed: 
modified: 2025-11-21T10:34:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Lessons Learned EoE CUH Project
type: 
uid: 
updated: 
---

Here is a list of actionable insights for the EoE/CUH lessons learned session, categorized by the specified topics and considerations, with a deeper integration of how the considerations impacted the primary topics:

## Lessons Learned EoE CUH Project

### Contracting

-   **Ambiguity in Contractual Scope and SLAs:** A lack of clarity regarding the precise scope of work and deliverables, exacerbated by a lack of structured vendor management and proactive clarification of responsibilities, led to potential misalignments. This ambiguity was particularly pronounced when direct contractual relationships were absent or indirect (e.g., involving subcontractors like The Hyve), necessitating detailed documentation of roles and responsibilities within agreements like the Data Sharing Agreement (DSA) and Data Centre Agreement.
-   **Lack of Defined Service Level Agreements (SLAs):** The absence of clearly defined and agreed-upon SLAs in contracts made it challenging to manage expectations and measure performance against agreed standards. This directly impacted the ability to enforce timely issue resolution and proactive notifications, as highlighted in the need for sufficient lead times for communications.
-   **Insufficient Lead Time for Notifications:** Communication and approval processes, often influenced by external stakeholder constraints and reactive planning, did not always allow for sufficient lead times. This directly affected adherence to potential SLAs and the ability to proactively manage issues related to IT/IG approvals and node installation timelines.

### IT and IG Approvals

-   **Governance Approval Bottlenecks and Extended Lead Times:** Delays in obtaining necessary IT and Information Governance (IG) approvals (e.g., DPIA, CAB, RITS submission) were significant bottlenecks. These were often prolonged due to insufficient technical context provided to approvers. For instance, Raja Rehman's feedback on the FITFILE software's risk rating (low vs. medium) necessitated detailed technical explanations and risk assessments beyond standard DPIA justifications to satisfy IG concerns.
-   **Insufficient Technical Context for Approvals:** Approvers frequently lacked the granular technical context required to make timely decisions. Concerns often revolved around the security implications of complex cloud-native configurations (e.g., Terraform module security, network access rules, secrets management), demanding detailed explanations and validation beyond initial documentation.
-   **Critical Path Dependencies:** Key approvals, such as the DPIA and RITS submission, were critical path items. Delays in their finalization, often due to pending technical decisions or insufficient stakeholder engagement, directly blocked subsequent project phases like node installation and data integration.

### Node Installation

-   **Complexity of Network Mandates and Reactive Environmental Preparation:** Navigating complex network mandates proved challenging. Environmental preparation was often reactive, making it difficult to configure intricate network requirements such as multi-layered proxy routing, specific firewall rules, and Azure network configurations. This complexity was compounded by late clarification of network requirements (e.g., outbound traffic routing, specific IP for API connection) from data providers like MKUH, impacting installation timelines.
-   **Navigating Formal Change Control and Stakeholder Dependencies:** Adherence to formal change control processes (e.g., MKUH CAB, raising RFCs) required substantial lead time and was sometimes a bottleneck. This was exacerbated by the need for reactive preparation and the dependency on timely technical sign-off from various stakeholders (e.g., MKUH IT/Networking teams, The Hyve for ETL scripts). Clear documentation of required changes (e.g., the "Change pack" for MKUH Node) was essential but sometimes delayed.

### Synthetic Data

-   **Validation Against Live Data and Mapping Uncertainty:** While synthetic data was utilized for initial testing, challenges arose in ensuring its complete fidelity and representativeness of live data scenarios. The communication and documentation between FITFILE, The Hyve (responsible for OMOP transformation and synthetic data), and the data providers (MKUH/CUH) were crucial but sometimes lacked the granularity to fully validate the synthetic data's accuracy against anticipated live data characteristics.
-   **Dependency on Data Provider Input for Fidelity:** The accuracy of synthetic data testing was dependent on clear and timely input from data providers regarding the expected structure and quality of live data. Ambiguities in expected live data characteristics (e.g., "messy string values") made it difficult to fully tune synthetic data generation.

### Live Data

-   **Data Quality and Variability Issues:** Significant challenges were encountered with the quality and variability of live data, including "messy string values" and inconsistencies in fields like "drug values." This highlights a need for more robust data profiling and proactive communication with data providers regarding data quality issues *before* live data integration.
-   **Mapping Uncertainty and Harmonization Effort:** Challenges persisted in accurately mapping and integrating live data from diverse sources. This required substantial effort for harmonization, particularly with complex datasets like medication data, where delays in stakeholder decisions (NNUH) and The Hyve's capacity for partial semantic mappings impacted timelines.
-   **Data Storage and Access Decisions:** Critical decisions regarding data storage (e.g., flat files vs. PostgreSQL) and access methods were often delayed, requiring significant stakeholder engagement (NNUH, Mike Shemko, Ben Goss) to resolve. These decisions directly impacted downstream processing, integration timelines, and the ability to finalize architectural diagrams and RITS submissions.

### Communications (with HIE / Data Providers)

-   **Inconsistent Proactive Documentation and Timeliness:** While comprehensive documentation was produced (e.g., via Obsidian, Confluence), its proactive sharing and availability at critical decision points or to all dependent parties was sometimes lacking. This "drip feed" of information, coupled with delays in stakeholder decisions, led to information silos and reactive planning.
-   **Clarity of Communication Channels and Stakeholder Alignment:** Ensuring consistent and clear communication across all stakeholders (HIE, Data Providers like MKUH/CUH/NNUH, The Hyve, internal teams) required continuous effort. Establishing preferred communication routes (e.g., email vs. Teams channel, as suggested in MKUH meeting preparation) and ensuring alignment on project priorities across diverse stakeholder groups proved challenging.

### Stakeholder Engagement

-   **Broader Stakeholder Alignment and Constraint Management:** While engagement with key technical contacts was often effective, achieving consistent alignment across all stakeholder groups, particularly those with differing priorities or internal processes (e.g., NNUH R&D, MKUH IT/IG teams), proved challenging. The constraints and internal approval timelines of various stakeholders were sometimes underestimated, impacting project timelines.
-   **Impact of Stakeholder Decisions on Project Milestones:** Decisions from key stakeholders (e.g., NNUH on data storage, pharmacy data integration; MKUH on network configurations) directly impacted project timelines and required significant, often iterative, engagement to resolve. Raja Rehman's feedback on the DPIA risk assessment is a prime example of how stakeholder input necessitated detailed technical documentation and communication to proceed.

### Documentation

-   **Timeliness and Proactive Sharing of Comprehensive Documentation:** The proactive sharing and timely availability of comprehensive documentation (e.g., DPIA, DSA, technical specifications, network diagrams) were critical for enabling timely approvals and informed decision-making. A lack of proactive sharing led to information silos and a "drip feed" of information, impacting the ability to finalize critical documents like the network diagram and RITS submission.
-   **Level of Detail in Technical Specifications:** Some technical specifications required more granular detail to fully support implementation and approval processes. For instance, the need for a specific "Change pack" document for MKUH node installation highlights how detailed documentation is crucial for formal change control and IT/IG approvals. The iterative refinement of documents like the DPIA, driven by stakeholder feedback, underscored the need for clear, detailed, and up-to-date technical context.

### Approvals and Sign-off

-   **Governance Approval Bottlenecks and Critical Path Dependencies:** Governance processes (DPIA, CAB, RITS submission) were significant bottlenecks. These were critical path items that, when delayed, blocked subsequent project phases. The iterative nature of approvals, often requiring updated documentation based on feedback (e.g., Raja Rehman's DPIA comments), extended lead times.
-   **Need for Early and Continuous Engagement:** Early and continuous engagement with all approval bodies (e.g., NNUH R&D, MKUH IT/IG, CUH) was crucial to proactively identify and address concerns, thereby mitigating delays. The formal review and sign-off on updated network diagrams and RITS submissions were contingent on confirmed decisions and resolution of pending items.

### Testing

-   **Insufficient Rigor in Certain Testing Phases:** Identified gaps were primarily in integration testing, end-to-end system testing, performance testing, and security testing of the complete solution. Component-level unit tests were performed, but the lack of comprehensive testing earlier in the lifecycle led to issues being discovered late, requiring costly rework.
-   **Impact of Data Quality on Testing:** The uncertainty regarding synthetic data's fidelity to live data, coupled with challenges in live data quality and mapping, meant that testing outcomes might not have fully represented real-world scenarios.
-   **Testing Against SLAs:** Ensuring test cases adequately covered and validated against defined SLAs was not consistently achieved, partly due to the initial lack of clearly defined SLAs.

### Management of Risks and Issues

-   **Reactive Issue Resolution and Inadequate Proactive Risk Identification:** Issues were often addressed reactively as they arose, rather than being proactively identified and mitigated. Specific materialized risks included the exposure of secrets in Git history, CI/CD pipeline failures due to dependency issues, and delays caused by complex network configuration challenges. Proactive identification of technical risks in complex, multi-component environments (like cloud-native deployments) could have been enhanced.
-   **Underestimation of Risk Impact and Stakeholder Feedback:** Raja Rehman's feedback questioning the FITFILE software's risk rating (low vs. medium) highlights a potential gap in proactive risk identification and the need for detailed technical context to satisfy IG requirements. The potential impact of certain identified risks was underestimated, leading to insufficient mitigation planning.

### Project Management

-   **Underestimation of Complexity and Disconnect in Approaches:** The inherent complexity of the technical solution (cloud-native, microservices, complex integrations) was likely underestimated, impacting planning and leading to reactive adjustments. A potential disconnect existed between advanced personal technical tooling/methodologies being explored (e.g., Agent OS, ProdOS) and the formal project management execution for EoE/CUH, potentially hindering a unified approach to planning and execution.
-   **Reactive Planning Due to Information Flow and Evolving Requirements:** Reactive planning was often necessary due to the "drip feed" of information, delayed approvals, and evolving requirements (e.g., pharmacy data integration scope, data storage decisions). This impacted resource allocation, timeline predictability, and the ability to conduct advance planning.

### SLAs

-   **Lack of Defined SLAs and Impact on Expectations:** As mentioned under Contracting, the absence of clearly defined SLAs created ambiguity. This directly impacted the ability to manage expectations regarding service delivery, issue resolution times, and proactive notifications.
-   **Connection to Communication and Approvals:** The effectiveness of communication protocols and the timeliness of approvals were intrinsically linked to SLA adherence. Without defined SLAs, there was less impetus for proactive communication and adherence to notification lead times, contributing to reactive management and potential dissatisfaction.
