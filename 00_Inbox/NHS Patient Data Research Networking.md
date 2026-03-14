---
created: 2026-03-13T10:36:05+00:00
modified: 2026-03-14T11:10:52+00:00
title: NHS Patient Data Research Networking
---

## Technical And Regulatory Requirements for Networking and Securing Patient Data for Research within the NHS Ecosystem

The management of National Health Service (NHS) patient data for secondary purposes such as research, population health management, and operational planning is governed by an increasingly complex intersection of strategic policy, technical networking standards, and evolving legislative frameworks. In recent years, the United Kingdom has undergone a fundamental transformation in its approach to health data, shifting from a model centered on data sharing—where datasets are physically transferred to external organizations—to a model based on secure data access.1 This paradigm shift, codified in the government's "Data Saves Lives" strategy and informed by the rigorous technical recommendations of the Goldacre Review, establishes the technical requirements for networking, encryption, and identity management across varying General Data Protection Regulation (GDPR) boundaries.3

The technical architecture underpinning this new ecosystem relies on Secure Data Environments (SDEs) and the Health and Social Care Network (HSCN), which together provide the secure "plumbing" necessary for multi-organizational research while mitigating the privacy risks inherent in large-scale data flows.1 Furthermore, the introduction of the Data (Use and Access) Act 2025 and the accompanying 2026 Information Commissioner's Office (ICO) guidance on international transfers have refined the legal requirements for processing data across jurisdictional boundaries, emphasizing a risk-based approach to data protection.9 This report provides an exhaustive analysis of the technical and regulatory landscape for professionals navigating the complexities of patient data networking for research.

### The Strategic Framework: Data Saves Lives and the Goldacre Paradigm

The foundational strategy for the contemporary use of health data in England is "Data Saves Lives: Reshaping Health and Social Care with Data," published in June 2022\.3 This policy document identifies data as a vital national asset, essential for the direct care of individuals, the proactive targeting of population health services, the improvement of institutional planning, and the research and innovation that powers new medical treatments.4 The strategy was heavily influenced by the independent review led by Professor Ben Goldacre, titled "Better, Broader, Safer: Using Health Data for Research and Analysis," which provided 185 recommendations aimed at modernizing the software infrastructure and working methods of the NHS.5

The Goldacre Review argued that traditional methods of data security, such as simple pseudonymization and the reliance on legal contracts, were insufficient for the scale of modern data science.13 The review characterized bulk flows of pseudonymized data as "outdated techniques" that cannot scale to support a world-leading life sciences sector.14 Instead, it advocated for the adoption of Trusted Research Environments (TREs)—now referred to as Secure Data Environments (SDEs) in NHS terminology—as the default and mandatory route for all analysis of NHS patient records.1

| Strategic Component | Core Objective | Technical Implication |
|:---- |:---- |:---- |
| Shift to Access | Move away from data sharing to data access. 1 | Data remains within NHS-controlled environments; analysts come to the data. 15 |
| SDE Implementation | Establish SDEs as the norm for secondary data use. 1 | Adoption of Virtual Desktop Infrastructure (VDI) and secure computation platforms. 16 |
| Reproducible Analytical Pipelines (RAP) | Standardize coding and analysis methods. 13 | Mandatory use of version control (Git) and open-source tools (Python, R). 14 |
| Transparency & Trust | Build public confidence through auditability. 3 | Publication of data release registers and logs of all analysis activity. 14 |

The "Data Saves Lives" strategy also established a "New Pact" with the public, promising improved transparency and a clear "opt-out" choice for individuals who do not wish their data to be used for research.4 This pact is supported by the National Data Opt-out, which must be technically integrated into any data flow intended for secondary purposes.19

### Secure Data Environments: Technical Specifications and Architecture

The implementation of SDEs represents the primary technical requirement for research networking. An SDE is a highly controlled computing platform that allows approved researchers to access and analyze de-identified patient information without the data ever leaving the environment.2 The NHS Research SDE Network currently consists of a national SDE operated by NHS England and 11 regional (sub-national) SDEs, such as those in the East of England, Wessex, Greater Manchester, and London.8

#### Technical Components of the SDE Workspace

The technical architecture of an SDE is designed to facilitate high-performance computing while maintaining rigid security boundaries. A typical research workspace within the NHS Research SDE Network, such as the East of England SDE, provides a Linux-based Virtual Desktop Infrastructure (VDI) hosted on cloud platforms like AWS.17 These environments are configured with specific compute resources, such as 16GB RAM and 4 vCPUs as a standard baseline, though these can be scaled based on the complexity of the research project.17

| Feature | Technical Specification | Context and Usage |
|:---- |:---- |:---- |
| Access Method | Secure Virtual Desktop Infrastructure (VDI). 16 | Provides a sandboxed environment isolated from the user's local hardware. 16 |
| Analytical Tools | RStudio, JupyterLab, Stata, DataBricks. 16 | Supports standard data science workflows in Python, R, and SQL. 16 |
| Code Management | Integrated GitLab repositories. 16 | Encourages version control and open-source practices within the secure boundary. 14 |
| Data Ingestion | De-identification/Scrubbing Area. 24 | Attributes like names and full addresses are removed before the data enters the SDE. 16 |
| Egress Control | Safe Output Service/Airlock. 16 | Manual and automated checking of analysis results to prevent re-identification. 16 |

The analytical tools provided within these environments are selected to ensure compatibility with modern data science while minimizing the risk of unauthorized data movement. For instance, the use of GitLab within the environment allows researchers to bring in their own code (subject to security review) while ensuring that the resulting scripts remain within the audited SDE.17

#### The Five Safes Framework

The operational governance of SDEs is structured around the "Five Safes" framework, which serves as the international standard for managing data privacy and security.2 Any networking of patient data for research must satisfy these five pillars:

1. Safe People: Researchers and their organizations must undergo a rigorous validation process. This includes verifying credentials, confirming that the organization meets specific security standards (such as the DSPT), and ensuring that individual researchers have completed approved safe researcher training.21
2. Safe Projects: All research must be evaluated by a Data Access Committee (DAC), which assesses whether the project has a clear lawful basis, provides a public benefit, and is feasible given the requested data.8
3. Safe Settings: Data is only accessed within the secure SDE platform, which prevents researchers from taking copies of the raw data or downloading identifiable information to their own devices.15
4. Safe Data: Only the minimum necessary data is provided for each project. This data is de-identified—meaning that direct identifiers like names, exact dates of birth, and full NHS numbers are removed and replaced with artificial "pseudo" identifiers.16
5. Safe Outputs: Every piece of information that a researcher wishes to remove from the environment (e.g., aggregate tables, graphs, or summary statistics) must undergo a manual review by the Safe Output Service to ensure that it does not inadvertently identify any individuals.16

### Networking Infrastructure: The Health and Social Care Network (HSCN)

For organizations that need to connect their internal systems to NHS services or participate in the secure transfer of data to an SDE, the Health and Social Care Network (HSCN) is the mandatory data network infrastructure.7 Replacing the older N3 network, HSCN operates on a disaggregated model, providing a competitive marketplace where healthcare organizations can procure connectivity from various approved suppliers while adhering to a unified set of technical standards.27

#### Technical And Security Standards for HSCN

Compliance with the HSCN is dictated by the HSCN Connection Agreement, which establishes the terms for secure network participation.7 Organizations must satisfy a range of Data Security Standards (DSS) and Technical Security Standards (TSS) to ensure the integrity of the network.28

| Standard ID | Technical Requirement | Implementation Detail |
|:---- |:---- |:---- |
| TSS 201 | Network Security Architecture. 28 | Requires robust segmentation and the monitoring of all network traffic. 28 |
| TSS 202 | Secure Remote Access. 28 | Mandates secure VPN or similar capabilities for clinical and research staff. 28 |
| TSS 203 | Data Encryption. 28 | All data must be encrypted both in transit and at rest. 28 |
| TSS 204 | System Hardening. 28 | Operating systems and applications must be hardened against known vulnerabilities. 28 |
| TSS 205 | Protective Monitoring. 28 | Implementation of intrusion detection and automated incident response. 28 |

The transition from checkbox compliance to continuous security assurance is a hallmark of current HSCN policy.28 This evolution is increasingly aligned with "Zero Trust" architecture, where every user, device, and application is verified before network access is granted.28 For research networking, this means that even after an organization is vetted, every individual connection to a data source is subjected to identity-centric security controls and role-based access management.28

#### Performance And Cloud Connectivity

For large-scale research projects, networking requirements often exceed standard office connectivity. HSCN providers now offer specialized services such as sub-10ms latency to NHS Spine services and native connectivity to major cloud platforms.28 This is critical for research that involves moving massive volumes of de-identified data into an SDE or utilizing high-performance cloud compute resources for AI and machine learning tasks.28 Organizations are encouraged to prioritize "computation near data," where AI models are trained within the cloud environment where the data is hosted, rather than moving petabytes of data across networks.29

### Data Security and Protection Toolkit (DSPT) Compliance

The Data Security and Protection Toolkit (DSPT) is the primary self-assessment tool used by the NHS to measure organizational performance against the National Data Guardian's (NDG) 10 Data Security Standards.30 Any organization that works with NHS patient data—including commercial research entities, academic institutions, and third-party IT suppliers—must complete an annual DSPT submission.30

#### The 10 National Data Guardian Standards

The NDG standards are grouped into three leadership obligations: People, Process, and Technology.33

| Obligation | Standard Description | Key Technical/Process Requirement |
|:---- |:---- |:---- |
| People | Confidentiality, Responsibilities, Training. 33 | Mandatory annual data security training for all staff handling patient data. 31 |
| Process | Managing Access, Reviews, Incidents, Continuity. 33 | Implementation of the principle of least privilege; reporting breaches within 12 hours. 31 |
| Technology | Unsupported Systems, IT Protection, Accountable Suppliers. 33 | Removal of legacy hardware/software; annual review of cybersecurity strategies. 31 |

Compliance with the DSPT is not a "one-time" task but an ongoing cycle of evaluation and improvement.33 Organizations must achieve a "Standards Met" or "Standards Exceeded" status to be considered compliant with the security requirements of the HSCN and the Data Access Request Service (DARS).7 For organizations categorized as "Category 1" (large NHS trusts and ALBs) or "Category 2" (significant independent providers), a mandatory audit of the DSPT submission is required.31 This audit increasingly aligns with the Cyber Assessment Framework (CAF) developed by the National Cyber Security Centre (NCSC), which provides a more granular and risk-based assessment of an organization's cyber resilience.28

#### Specific Requirements for IT Suppliers

Under the DSPT, an organization is considered an "IT Supplier" if it has more than 50 staff, a turnover exceeding £10 million, and provides digital goods or services to the NHS.31 Suppliers in this category face enhanced requirements, particularly regarding the security of their software development lifecycles and their ability to demonstrate that their products are "interoperable by design".31

### Interoperability And Standardized Data Models

As the NHS moves toward a more integrated data landscape, the technical requirements for interoperability have become a central focus. The lack of interoperability—where 70% of health information is historically not shared between providers—has been identified as a major barrier to both patient care and clinical research.35 The "Data Saves Lives" strategy and the Data (Use and Access) Act 2025 address this by mandating the adoption of common information standards.35

#### The Federated Data Platform (FDP)

The NHS Federated Data Platform (FDP) is a national program designed to connect information across trusts and integrated care boards (ICBs) without transferring ownership of that data to a central repository.37 In a federated model, data remains with the local organization, and secure connections allow approved users to access insights across multiple sites.39

Key features of the FDP include:

- Local Instances: Each trust and ICB has its own instance of the platform, for which they are the data controller.37
- Analytical Capabilities: The platform provides unified tools for pattern identification and operational planning, such as "waiting list management" and "discharge planning".37
- Data Flows Transformation: This program automates the movement of data across the system, reducing the manual reporting burden on providers while creating a near-real-time picture of NHS activity for research and planning.40

#### Standardizing Data for Research: OMOP and FHIR

To enable research across the different "nodes" of the SDE Network and the FDP, the NHS is increasingly adopting standardized data models. The Observational Medical Outcomes Partnership (OMOP) Common Data Model is the preferred standard for health data research in the UK.17

The London SDE, for example, is currently engineering and standardizing multi-modal data—including structured clinical records, unstructured text, and radiology imaging metadata—into the OMOP format.25 This standardization allows for "federated analytics," where a researcher can query OMOP databases across multiple hospital sites and receive aggregated results without the patient-level data ever moving between sites.25 This technical approach directly addresses the "privacy and networking" concerns of working across different organizational and GDPR boundaries by minimizing the physical movement of sensitive information.25

### Privacy And GDPR: Navigating Jurisdictional Boundaries

professionals working with patient data must operate within the strict legal framework of the UK GDPR and the Data Protection Act 2018\.2 The landscape has been further complicated by the implementation of the Data (Use and Access) Act 2025, which introduced significant updates to the rules on automated decision-making, the lawful basis for processing, and international data transfers.11

#### Lawful Basis and "Recognised Legitimate Interests"

A significant update in the 2025 Act is the introduction of "recognised legitimate interests" as a lawful basis for processing personal data.11 While many GP and hospital data flows historically relied on "public task" or "legal obligation," the new basis allows for processing without explicit consent when the activity is clearly in the public interest—such as safeguarding, public health protection, and emergency response.11 For researchers, this can simplify the data acquisition process for projects aimed at improving population health, provided that rigorous safeguards are in place and the decision-making process is fully documented.11

#### International Data Transfers: The 2026 ICO Guidance

For research that involves international collaboration, the rules on "restricted transfers" are paramount. In January 2026, the ICO published updated guidance reflecting the changes introduced by the 2025 Act.9 A transfer is restricted if the UK GDPR applies to the processing, the data is sent to an organization outside the UK, and that organization is a separate legal entity.9

The 2026 guidance emphasizes a "Three-Step Test" for identifying restricted transfers:

1. Does the UK GDPR apply? 9
2. Are you "initiating" the transfer? A transfer is initiated by the organization that chooses to make the transfer happen as part of its purposes.9
3. Is the receiver a separate legal entity? Intra-entity transfers (e.g., to an overseas branch of the same company) are not restricted transfers.10

| Transfer Mechanism | Requirement under 2026 Guidance | Context for Research |
|:---- |:---- |:---- |
| Adequacy Regulations | Data flows freely to countries with "substantially similar" protections. 9 | Most efficient for EU/EEA collaborations. 9 |
| Appropriate Safeguards | Use of the International Data Transfer Agreement (IDTA) or the Addendum. 9 | Required for transfers to countries without an adequacy decision (e.g., many US-based services). 9 |
| Transfer Risk Assessment (TRA) | Now referred to as a "Data Protection Test." 10 | Must ensure the protection in the destination is "not materially lower" than in the UK. 10 |
| Derogations | Exceptions for specific cases (e.g., legal claims). 9 | Should be applied narrowly and only when other mechanisms are unavailable. 9 |

A critical nuance for NHS workers is that a UK-based processor "returning" data to an overseas controller is not considered to be initiating a restricted transfer, as they are merely acting on the controller's instructions.10 This interpretation, which diverges from EU GDPR guidance, reduces the regulatory burden on UK-based data centers and service providers.44

### Patient Autonomy and the National Data Opt-out

The National Data Opt-out (NDOO) is a service that enables patients to decide whether their confidential patient information can be used for purposes beyond their individual care, specifically for research and planning.19 Compliance with the NDOO policy became mandatory for all health and adult social care organizations in England by July 2022\.20

#### Technical Implementation of NDOO Compliance

Any organization that uses or discloses identifiable patient data for research must "clean" their dataset to remove records for patients who have registered an opt-out.19 This is achieved through the "Check for National Data Opt-outs" service, which utilizes the MESH (Messaging Exchange for Social Care and Health) to process lists of NHS numbers.19

| Compliance Action | Technical Mechanism | Responsibility |
|:---- |:---- |:---- |
| Record Opt-out | Registered against the patient's NHS number on the Spine. 19 | Individuals via NHS App or online portal. 19 |
| Apply Opt-out | MESH service used to filter datasets before dissemination. 19 | The data controller (e.g., NHS Trust or Research Body). 20 |
| Declare Compliance | Published in privacy notices and DSPT submissions. 20 | All NHS and adult social care organizations. 19 |

The NDOO does not apply in several specific scenarios:

- Anonymized Data: If the data is truly anonymized (where individuals cannot be identified), the opt-out does not apply.46
- Individual Care: Data used for the direct treatment of a patient is exempt.19
- Statutory Requirements: Data collections mandated by law (e.g., Section 259 of the Health and Social Care Act 2012\) may be exempt.46
- Explicit Consent: If a patient has given specific informed consent for a particular research project, their national data opt-out choice is overridden.46

### AI Readiness and Future Technical Directions

As the NHS increasingly adopts artificial intelligence (AI) and machine learning (ML), the technical requirements for "AI-ready" datasets have become a strategic priority.29 An AI-ready dataset is not just a technical format; it is defined by its context, governance, and suitability for specific computational use cases.29

#### Guidelines For AI-Ready Data Infrastructure

Government guidance for making datasets ready for AI emphasizes several key technical capabilities:

- Computation Near Data: To avoid the bottleneck of moving petabytes of data across networks, compute resources (GPUs) should be positioned as close as possible to the data.29
- Tiered Storage: Organizations should implement "Hot Storage" for active training data, "Warm Storage" (Object Store) for entire datasets used during training sessions, and "Cold Storage" for infrequently accessed historical logs.29
- Synthetic Data: The use of synthetic datasets is encouraged for testing and accelerating readiness without exposing real patient information to the risks of early-stage model development.12
- ML-Oriented Metadata: This includes traditional descriptors alongside "bias notes," versioning, and provenance tracking to ensure the ethical and transparent use of AI in healthcare.29

#### The 10-Year Health Plan and the Digital Blueprint

Looking ahead, the NHS is moving toward a "Digital and Data Blueprint" expected in 2026, which will define the next generation of operating standards for technology infrastructure.49 A central component of this future state is the "Single Patient Record," which aims to consolidate information across primary, secondary, and community care.49 For researchers, this signifies a move toward a truly unified national data repository that, while distributed in its architecture, will be accessible through a single point of entry within the SDE Network.23

### Conclusion: A Synthesized Technical Roadmap

Professionals managing patient data networking must align their operations with a multi-layered technical and regulatory architecture. The move to Secure Data Environments (SDEs) is the most critical shift, necessitating the abandonment of bulk pseudonymized data flows in favor of access-based research workspaces. Networking across GDPR boundaries now requires a sophisticated "Three-Step Test" and a rigorous "Data Protection Test" to ensure international compliance under the 2026 ICO guidelines.

Security is maintained through the annual DSPT cycle, which increasingly demands evidence of "Zero Trust" architectures and CAF-aligned audits. Simultaneously, patient autonomy is protected through the technical integration of the National Data Opt-out via MESH and the NHS Spine. As interoperability standards like OMOP and the Federated Data Platform become mainstream, the technical requirements for research will focus on "computation near data" and the curation of AI-ready datasets. By adhering to this framework, organizations can harness the life-saving potential of NHS data while maintaining the highest standards of privacy and public trust.

#### Works Cited

1. Accessing data for research and analysis \- Secure Data Environments (SDEs), accessed on March 13, 2026, [https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/accessing-data-for-research-and-analysis/](https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/accessing-data-for-research-and-analysis/)
2. Secure Data Environments (SDEs) \- Data saves lives \- NHS Transformation Directorate, accessed on March 13, 2026, [https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/](https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/)
3. Data saves lives \- Key tools and information \- NHS Transformation Directorate, accessed on March 13, 2026, [https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/](https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/)
4. Data saves lives: reshaping health and social care with data \- GOV.UK, accessed on March 13, 2026, [https://www.gov.uk/government/publications/data-saves-lives-reshaping-health-and-social-care-with-data/data-saves-lives-reshaping-health-and-social-care-with-data](https://www.gov.uk/government/publications/data-saves-lives-reshaping-health-and-social-care-with-data/data-saves-lives-reshaping-health-and-social-care-with-data)
5. Better, broader, safer: using health data for research and … \- GOV.UK, accessed on March 13, 2026, [https://assets.publishing.service.gov.uk/media/624ea0ade90e072a014d508a/goldacre-review-using-health-data-for-research-and-analysis.pdf](https://assets.publishing.service.gov.uk/media/624ea0ade90e072a014d508a/goldacre-review-using-health-data-for-research-and-analysis.pdf)
6. Goldacre recommendations to improve care through use of data \- GOV.UK, accessed on March 13, 2026, [https://www.gov.uk/government/news/goldacre-recommendations-to-improve-care-through-use-of-data](https://www.gov.uk/government/news/goldacre-recommendations-to-improve-care-through-use-of-data)
7. Health and Social Care Network (HSCN) \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/health-and-social-care-network](https://digital.nhs.uk/services/health-and-social-care-network)
8. How will Secure Data Environments be delivered? \- NHS Transformation Directorate, accessed on March 13, 2026, [https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/how-will-secure-data-environments-be-delivered/](https://transform.england.nhs.uk/key-tools-and-info/data-saves-lives/secure-data-environments/how-will-secure-data-environments-be-delivered/)
9. A brief guide to international transfers | ICO, accessed on March 13, 2026, [https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/a-brief-guide-to-international-transfers/](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/a-brief-guide-to-international-transfers/)
10. The ICO's 2026 updated international transfer guidance: Decoding the new UK regime, accessed on March 13, 2026, [https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-ico-s-2026-updated-international-transfer-guidance-decoding-the-new-uk-regime/](https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-ico-s-2026-updated-international-transfer-guidance-decoding-the-new-uk-regime/)
11. Data Use and Access Act 2025: key changes for GP practices \- Patient.info, accessed on March 13, 2026, [https://patient.info/doctor/information-governance-and-security/data-use-and-access-act-2025](https://patient.info/doctor/information-governance-and-security/data-use-and-access-act-2025)
12. Data saves lives: building trust in NHS data use \- PHG Foundation, accessed on March 13, 2026, [https://www.phgfoundation.org/blog/data-saves-lives-building-trust-in-nhs-data-use/](https://www.phgfoundation.org/blog/data-saves-lives-building-trust-in-nhs-data-use/)
13. Goldacre recommendations for making the most of health data for research \- PHG Foundation, accessed on March 13, 2026, [https://www.phgfoundation.org/blog/goldacre-making-the-most-of-health-data-for-research/](https://www.phgfoundation.org/blog/goldacre-making-the-most-of-health-data-for-research/)
14. Executive summary: better, broader, safer \- using health data for research and analysis \- GOV.UK, accessed on March 13, 2026, [https://assets.publishing.service.gov.uk/media/624ea34cd3bf7f600d4055bc/executive-summary-goldacre-review-using-health-data-for-research-and-analysis.pdf](https://assets.publishing.service.gov.uk/media/624ea34cd3bf7f600d4055bc/executive-summary-goldacre-review-using-health-data-for-research-and-analysis.pdf)
15. Secure Data Environments \- Understanding Patient Data, accessed on March 13, 2026, [https://understandingpatientdata.org.uk/secure-data-environments](https://understandingpatientdata.org.uk/secure-data-environments)
16. Secure Data Environment \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/secure-data-environment-service](https://digital.nhs.uk/services/secure-data-environment-service)
17. For Researchers \- East of England Sub-National Secure Data Environment, accessed on March 13, 2026, [https://www.eoe-securedataenvironment.nhs.uk/researchers.html](https://www.eoe-securedataenvironment.nhs.uk/researchers.html)
18. NHS England as a data safe haven: our 5 data promises, accessed on March 13, 2026, [https://digital.nhs.uk/data-and-information/protecting-and-safely-using-data-in-the-new-nhs-england/our-5-data-promises](https://digital.nhs.uk/data-and-information/protecting-and-safely-using-data-in-the-new-nhs-england/our-5-data-promises)
19. National Data Opt-Out \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/national-data-opt-out](https://digital.nhs.uk/services/national-data-opt-out)
20. Compliance with the national data opt-out \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/national-data-opt-out/compliance-with-the-national-data-opt-out](https://digital.nhs.uk/services/national-data-opt-out/compliance-with-the-national-data-opt-out)
21. Beginner's guide to the SDE Network \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/data-and-information/research-powered-by-data/support-and-resources/beginners-guide](https://digital.nhs.uk/data-and-information/research-powered-by-data/support-and-resources/beginners-guide)
22. Life saving research \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/data-and-information/research-powered-by-data/life-saving-research](https://digital.nhs.uk/data-and-information/research-powered-by-data/life-saving-research)
23. Unlocking NHS data for research: how to improve the regional Secure Data Environment network, accessed on March 13, 2026, [https://www.abhi.org.uk/media/syfigmgj/unlocking-nhs-data-for-research-how-to-improve-the-regional-secure-data-environment-network.pdf](https://www.abhi.org.uk/media/syfigmgj/unlocking-nhs-data-for-research-how-to-improve-the-regional-secure-data-environment-network.pdf)
24. EoE SDE 12 page Booklet \- Secure Data Environment, accessed on March 13, 2026, [https://www.eoe-securedataenvironment.nhs.uk/resources/EoE%20SDE%2012%20page%20Booklet.pdf](https://www.eoe-securedataenvironment.nhs.uk/resources/EoE%20SDE%2012%20page%20Booklet.pdf)
25. Full Stack Multi-Modal Data into a Federated Secure Data Environment for London \- UK Health Data Research Alliance, accessed on March 13, 2026, [https://ukhealthdata.org/wp-content/uploads/2025/09/OHDSI\_fullstack.pdf](https://ukhealthdata.org/wp-content/uploads/2025/09/OHDSI_fullstack.pdf)
26. The Secure Data Environment (SDE) | Health Innovation Manchester, accessed on March 13, 2026, [https://healthinnovationmanchester.com/gms-secure-data-environment-sde-for-health-and-care/](https://healthinnovationmanchester.com/gms-secure-data-environment-sde-for-health-and-care/)
27. HSCN Interoperability | X-on Health \- Surgery Connect, accessed on March 13, 2026, [https://www.x-on.co.uk/knowledge-base/hscn-interoperability/](https://www.x-on.co.uk/knowledge-base/hscn-interoperability/)
28. NHS Network Security & Compliance: HSCN, Zero Trust & Cloud Connectivity, accessed on March 13, 2026, [https://www.cloudgateway.co.uk/knowledge-centre/articles/nhs-network-security-compliance-hscn-zero-trust-cloud-guide/](https://www.cloudgateway.co.uk/knowledge-centre/articles/nhs-network-security-compliance-hscn-zero-trust-cloud-guide/)
29. Guidelines and best practices for making government datasets ready for AI \- GOV.UK, accessed on March 13, 2026, [https://www.gov.uk/government/publications/making-government-datasets-ready-for-ai/guidelines-and-best-practices-for-making-government-datasets-ready-for-ai](https://www.gov.uk/government/publications/making-government-datasets-ready-for-ai/guidelines-and-best-practices-for-making-government-datasets-ready-for-ai)
30. Data Security and Protection Toolkit (DSPT), accessed on March 13, 2026, [https://www.dsptoolkit.nhs.uk/](https://www.dsptoolkit.nhs.uk/)
31. What is the NHS Data Security & Protection Toolkit (DSPT), and how do you remain compliant? | DPAS, accessed on March 13, 2026, [https://www.dataprivacyadvisory.com/what-is-the-nhs-data-security-protection-toolkit-and-how-do-you-remain-compliant/](https://www.dataprivacyadvisory.com/what-is-the-nhs-data-security-protection-toolkit-and-how-do-you-remain-compliant/)
32. Data Security and Protection Toolkit \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/data-security-and-protection-toolkit](https://digital.nhs.uk/services/data-security-and-protection-toolkit)
33. A Practical Guide to the NHS Data Security and Protection Toolkit \- Specops Software, accessed on March 13, 2026, [https://specopssoft.com/blog/nhs-data-security-protection-toolkit-compliance-guide/](https://specopssoft.com/blog/nhs-data-security-protection-toolkit-compliance-guide/)
34. Data Security and Protection Toolkit (DSPT) \- Skills for Care, accessed on March 13, 2026, [https://www.skillsforcare.org.uk/Support-for-leaders-and-managers/Managing-a-service/Digital-technology-and-social-care/Data-Security-Protection-Toolkit-DSPT.aspx](https://www.skillsforcare.org.uk/Support-for-leaders-and-managers/Managing-a-service/Digital-technology-and-social-care/Data-Security-Protection-Toolkit-DSPT.aspx)
35. Data saves lives: Bill S-5 revives interoperability requirements for health-care technology, accessed on March 13, 2026, [https://www.mltaikins.com/insights/data-saves-lives-bill-s-5-revives-interoperability-requirements-for-health-care-technology/](https://www.mltaikins.com/insights/data-saves-lives-bill-s-5-revives-interoperability-requirements-for-health-care-technology/)
36. Impact Assessment (IA), accessed on March 13, 2026, [https://bills.parliament.uk/publications/56552/documents/5225](https://bills.parliament.uk/publications/56552/documents/5225)
37. Federated Data Platform \- NHS England Digital, accessed on March 13, 2026, [https://digital.nhs.uk/services/federated-data-platform](https://digital.nhs.uk/services/federated-data-platform)
38. NHS Federated Data Platform \- NHS England, accessed on March 13, 2026, [https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/](https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/)
39. Federated Data Platform: What It Means for the NHS in England, accessed on March 13, 2026, [https://telefonicatech.uk/articles/federated-data-platform/](https://telefonicatech.uk/articles/federated-data-platform/)
40. Data Flows Transformation \- NHS England, accessed on March 13, 2026, [https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/data-flows-transformation/](https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/data-flows-transformation/)
41. International review to inform the development of an interoperability framework \- HIQA, accessed on March 13, 2026, [https://www.hiqa.ie/sites/default/files/2025-11/International-Review-For-a-National-Interoperability-Framework.pdf](https://www.hiqa.ie/sites/default/files/2025-11/International-Review-For-a-National-Interoperability-Framework.pdf)
42. Data Protection Conference \- Westminster Insight, accessed on March 13, 2026, [https://www.westminsterinsight.com/conferences-and-events/data-protection/](https://www.westminsterinsight.com/conferences-and-events/data-protection/)
43. Updated guidance on international transfers published | ICO, accessed on March 13, 2026, [https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/01/updated-guidance-on-international-transfers-published/](https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/01/updated-guidance-on-international-transfers-published/)
44. UK ICO issues updated guidance on international transfers: Part 1–identifying restricted transfers \- Freshfields Technology Quotient, accessed on March 13, 2026, [https://technologyquotient.freshfields.com/post/102mmbp/uk-ico-issues-updated-guidance-on-international-transfers-part-1-identifying-r](https://technologyquotient.freshfields.com/post/102mmbp/uk-ico-issues-updated-guidance-on-international-transfers-part-1-identifying-r)
45. International transfers | ICO, accessed on March 13, 2026, [https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)
46. How the NHS and care services use your information: the National Data Opt-Out, accessed on March 13, 2026, [https://www.england.nhs.uk/contact-us/privacy-notice/how-the-nhs-and-care-services-use-your-information-the-national-opt-out/](https://www.england.nhs.uk/contact-us/privacy-notice/how-the-nhs-and-care-services-use-your-information-the-national-opt-out/)
47. National data opt-out policy | NHS SBS, accessed on March 13, 2026, [https://www.sbs.nhs.uk/national-data-opt-out-policy/](https://www.sbs.nhs.uk/national-data-opt-out-policy/)
48. New data strategy launched to improve patient care and save lives \- GOV.UK, accessed on March 13, 2026, [https://www.gov.uk/government/news/new-data-strategy-launched-to-improve-patient-care-and-save-lives](https://www.gov.uk/government/news/new-data-strategy-launched-to-improve-patient-care-and-save-lives)
49. Digital transformation in the NHS: a reference guide, accessed on March 13, 2026, [https://www.nhsconfed.org/publications/digital-transformation-nhs-reference-guide](https://www.nhsconfed.org/publications/digital-transformation-nhs-reference-guide)
50. Federated Data Platform Check and Challenge Group–minutes and action notes: 21 November 2025 \- NHS England, accessed on March 13, 2026, [https://www.england.nhs.uk/long-read/fdp-check-challenge-group-minutes-action-notes-21nov2025/](https://www.england.nhs.uk/long-read/fdp-check-challenge-group-minutes-action-notes-21nov2025/)
