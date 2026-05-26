---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:53+00:00
title: The Digital Technology Assessment Criteria for Health and Social Care (DTAC)
---

The Digital Technology Assessment Criteria for Health and Social Care (DTAC)

## Table of Contents {#table-of-contents}

The assessment criteria is made up of five core components. Sections A and B will provide the assessors the context required to understand your product and support your evidence. The core assessment criteria is defined in section C1-C4. Section D details the key Usability and Accessibility principles required. Further frequently asked questions are available at the end of the document.

The core criteria in Section C will determine the overall success of the assessment of your product or service. The accompanying score provided from Section D will show the level of adherence to the NHS Service Standard.

[Table of contents    2](#table-of-contents)

[A. Company information - Non-assessed section    3](#a.-company-information---non-assessed-section)

[B. Value proposition - Non-assessed section    5](#b.-value-proposition---non-assessed-section)

[C. Technical questions - Assessed sections    7](#c.-technical-questions---assessed-sections)

[C1 - Clinical safety    7](#c1---clinical-safety)

[C2 - Data protection    14](#c2---data-protection)

[C3 - Technical security    20](#c3---technical-security)

[C4 - Interoperability criteria    23](#c4---interoperability-criteria)

[D. Key principles for success    28](#d.-key-principles-for-success)

[D1 - Usability and accessibility - scored section    28](#d1---usability-and-accessibility---scored-section)

[Supporting documentation    36](#supporting-documentation)

## A. Company Information - Non-assessed Section {#a.-company-information---non-assessed-section}

Information about your organisation and contact details.

| Code | Question | Options |

|---|---|---|

| A1 | Provide the name of your company | FITFILE Group Limited |

| A2 | Provide the name of your product | FITFILE |

| A3 | Provide the type of product | \~\~App |

| A4 | Provide the name and job title of the individual who will be the key contact at your organisation | Susannah Thomas Project Director |

| A5 | Provide the key contact's email address | [susannah.thomas@fitfile.com](mailto:susannah.thomas@fitfile.com) |

| A6 | Provide the key contact's phone number | 07811 349 013 |

| A7 | Provide the registered address of your company | 167-169 Great Portland Street, 5th Floor,London W1W 5PF, United Kingdom |

| A8 | In which country is your organisation registered? | United Kingdom |

| A9 | If you have a Companies House registration in the UK please provide your number | 12492844 |

| A10 | If applicable, when was your last assessment from the Care Quality Commission (CQC)? | \~\~Date |

| A11 | If applicable, provide your latest CQC report. | ~~Provided~~ Not applicable |

## B. Value Proposition - Non-assessed Section {#b.-value-proposition---non-assessed-section}

Please set out the context of the clinical, economic or behavioural benefits of your product to support the review of your technology. This criteria will not be scored but will provide the context of the product undergoing assessment.

Where possible, please provide details relating to the specific technology and not generally to your organisation.

| Code | Question | Options | Supporting information |

|---|---|---|---|

| B1 | Who is this product intended to be used for? | \~\~Patients | Diagnostics |

| B2 | Provide a clear description of what the product is designed to do and of how it is expected to be used | Free text | FITFILE offers a distributed technology platform and associated services through software "Nodes" deployed inside Data Provider/ Controller perimeters (typically in a private cloud) to access and (locally or remotely) query data, privacy treat that data at source (either pseudonymise or anonymise), link data at the record-level and execute computations at source such as structuring of unstructured data, harmonisation to standards such as OMOP and statistical analysis for selected cohorts of interest. FITFILE is expected to be used for pre-approved projects by health researchers and planners within or outside of individual Data Controllers (e.g. approved researchers in a Secure Data Environment) for applications such as cohort discovery and outcome tracking. For the EoE SDE, Data Provider Nodes are connected to a central Node inside the SDE which routes queries and results. Uses are expected to span cohort discovery (identifying patients of interest either via the National Portal or the EoE SDE), cohort validation (confirming cohorts of interest) and Data Access Committee-approved project extracts (sharing record-level data that is privacy treated and OMOP harmonised at source). |

| B3 | Describe clearly the intended or proven benefits for users and confirm if / how the benefits have been validated | Free text | In general, all users of the FITFILE product are expected to benefit from Multi-Source Data Access: for granular record-level querying & results output Identifiable Data Linkage: as a valuable tool for Data Providers themselves and for powering action (e.g. recruiting named individuals once study protocols are approved) Tokenised (Reversible) Linkage: flexible FITFILE or 3rd party de-identification (and re-identification if necessary/ allowed), either deterministic or probabilistic Unique Anonymised (Irreversible) Linkage: safest possible privacy beyond other solutions and GDPR laws Unique Computation at Source: offering powerful federated analytics/ learning for overlapping (not just discrete) populations Flexible Data Structuring, Harmonisation etc.: via Data Controllers' preferred and/ or FITFILE recommended partners whose solutions are seamlessly delivered via FITFILE Nodes for maximum data utility Key benefits for the broader stakeholder group encompass: Anonymisation, computation at source and linked identifiable data make much more data on more people accessible and usable for broadest unlocking of value Fullest privacy preservation range and minimisation of data movement ensure proper compliance with privacy regulation and downside protection Once deployed, multi-purpose and highly scalable decentralised infrastructure and record-level insights can be easily re-used by different stakeholders In other UK projects to date, FITFILE has, for example generated an estimated 20x productivity improvements and established £2m+ of cost savings for one sub-set of patients in one hospital department. For a cardiovascular compassionate use project at a large London teaching hospital, researchers are tracking longer-term outcomes associated with a high cost stem cell procedure. For Data Providers in the EoE SDE, the intended benefits of using FITFILE include: Support data flows to enable new/more research projects for patient/public benefit Help streamline and prioritise datasets to support future research Data Provider research spaces within the platform for own research collaborations Revenue generation and patient benefits of participation in clinical trials Extension of HDRUK participation and collaboration Expand existing academic collaboration potential (UK and global) |

| B4 | Please attach one or more user journeys which were used in the development of this product Where possible please also provide your data flows | Provided \~\~ | Not available\~\~ |

## C. Technical Questions - Assessed Sections {#c.-technical-questions---assessed-sections}

### C1 - Clinical Safety {#c1---clinical-safety}

Establishing that your product is clinically safe to use.

You must provide responses and documentation relating to the specific technology product that is subject to assessment.

The DCB0129 standard applies to organisations that are responsible for the development and maintenance of health IT systems. A health IT system is defined as "product used to provide electronic information for health and social care purposes". DTAC is designed as the assessment criteria for digital health technologies and C1 Clinical Safety Criteria is intended to be applied to all assessments. If a developer considers that the C1 Clinical Safety is not applicable to the product being assessed, rationale must be submitted exceptionally detailing why DCB0129 does not apply.

The DCB0160 standard applies to the organisation in which the health IT is deployed or used. It is a requirement of the standard (2.5.1) that in the procurement of health IT systems the organisation must ensure that the manufacturer and health IT system complies with DCB0129. The organisation must do so in accordance with the requirements and obligations set out in the DCB0160 standard. This includes personnel having the knowledge, experience and competences appropriate to undertaking the clinical risk management tasks assigned to them and organisations should ensure that this is the case when assessing this section of the DTAC.

If the Clinical Safety Officer or any other individual has concerns relating to safety of a medical device including software and apps, this should be reported to the Medicines and Healthcare products Regulatory Agency (MHRA) using the Yellow Card reporting system: [Report a problem with a medicine or medical device - GOV.UK (www.gov.uk)](https://www.gov.uk/report-problem-medicine-medical-device).

| Code | Question | Options | Supporting information | Scoring criteria |

|---|---|---|---|---|

| C1.1 | Have you undertaken Clinical Risk Management activities for this product which comply with DCB0129? | Yes \~\~ | No\~\~ | The [DCB0129](https://digital.nhs.uk/data-and-information/information-standards/information-standards-and-data-collections-including-extractions/publications-and-notifications/standards-and-collections/dcb0129-clinical-risk-management-its-application-in-the-manufacture-of-health-it-systems) standard applies to organisations that are responsible for the development and maintenance of health IT systems. A health IT system is defined as '"product used to provide electronic information for health and social care purposes". |

| C1.1.1 | Please detail your clinical risk management system | Provided \~\~ | No evidence available\~\~ | DCB0129 sets out the activities that must and should be undertaken for health IT systems. An example [clinical risk management system template](https://digital.nhs.uk/services/clinical-safety/documentation#clinical-risk-management) can be downloaded from the NHS Digital website. |

| C1.1.2 | Please supply your Clinical Safety Case Report and Hazard Log | Provided \~\~ | \~\~ ~~No evidence available~~ | Specifically, your DTAC submission should include: A summary of the product and its intended use A summary of clinical risk management activities A summary of hazards identified which you have been unable to mitigate to as low as it is reasonably practicable The clear identification of hazards which will require user or commissioner action to reach acceptable mitigation (for example, training and business process change) It should not include the hazard log in the body of the document - this should be supplied separately. Example [Clinical Safety Case Report and Hazard Log templates](https://digital.nhs.uk/services/clinical-safety/documentation#clinical-risk-management) can be downloaded from the NHS Digital website. |

| C1.2 | Please provide the name of your Clinical Safety Officer (CSO), their profession and registration details | Free Text | The CSO must: Be a suitably qualified and experienced clinician Hold a current registration with an appropriate professional body relevant to their training and experience Be knowledgeable in risk management and its application to clinical domains Be suitably trained and qualified in risk management or have an understanding in principles of risk and safety as applied to Health IT Have completed appropriate training The work of the CSO can be undertaken by an outsourced third party. | FITFILE's Clinical Safety Officer isAlex Christie, provided by clinical safety specialist Safehand Consulting Limited. |

| C1.3 | If your product falls within the UK Medical Devices Regulations 2002, is it registered with the Medicines and Healthcare products Regulatory Agency (MHRA)? | \~\~Yes | \~\~ No \~\~ | Not applicable\~\~ |

| C1.3.1 | If yes, please provide your MHRA registration number | Free text | | Not applicable. |

| C1.3.2 | If the UK Medical Device Regulations 2002 are applicable, please provide your Declaration of Conformity and, if applicable, certificate of conformity issued by a Notified Body / UK Approved Body | Provided | No evidence available | Medical device manufacturers must ensure that their device complies with the relevant Essential Requirements of the legislation and draw up a Declaration of Conformity to declare this. Class I devices with a measuring function and devices in Class IIa, IIb and III must undergo conformity assessment from an EU Notified Body or UK Approved Body which has been designated for medical devices, and be issued a certificate of conformity (commonly referred to as a "CE certificate" or "UKCA certificate"). |

| C1.4 | Do you use or connect to any third-party products? | ~~Yes I~~ No | If no, continue to section C2. [DCB0129](https://digital.nhs.uk/services/clinical-safety/documentation#clinical-risk-management) contains the requirements in relation to third party products. | |

| C1.4.1 | If yes, please attach relevant Clinical Risk Management documentation and conformity certificate | Provided | No evidence available | |

### C2 - Data Protection {#c2---data-protection}

Establishing that your product collects, stores and uses data (including personally identifiable data) compliantly.

This section applies to the majority of digital health technology products however there may be some products that do not process any NHS held patient data or any identifiable data. If this is the case, the Data Protection Officer, or other suitably authorised individual should authorise this data protection section being omitted from the assessment.

| Code | Question | Options | Supporting information | Scoring criteria |

|---|---|---|---|---|

| C2.1 | If you are required to register with the Information Commissioner, please attach evidence of a current registration. If you are not required to register, please attach a completed self-assessment showing the outcome from the Information Commissioner and your responses which support this determination. | Provided \~\~ | Not provided\~\~ | There are some instances where organisations are not required to register with the Information Commissioner. This includes where no personal information is being processed. The Information Commissioner has a [registration self-assessment tool](https://ico.org.uk/for-organisations/data-protection-fee/self-assessment/) to support this decision making. |

| C2.2 | Do you have a nominated Data Protection Officer (DPO)? | Yes \~\~ | No | We do not need one\~\~ |

| C2.2.1 | If you are required to have a nominated Data Protection Officer, please provide their name. If you are not required to have a DPO please attach a completed self-assessment showing the outcome from the Information Commissioner and your responses which support this determination. | Free text | Provided | |

| C2.3 | Does your product have access to any personally identifiable data or NHS held patient data? | Yes \~\~ | No\~\~ | The UK General Data Protection Regulation (GDPR) applies to the processing of [personal data](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/key-definitions/what-is-personal-data/). If no, continue to question C2.4 |

| C2.3.1 | Please confirm you are compliant (having standards met or exceeded status) with the annual Data Security and Protection Toolkit Assessment. If you have not completed the current year's assessment and the deadline has not yet passed, please confirm that you intend to complete this ahead of the deadline and that there are no material changes from your previous years submission that would affect your compliance. | Confirmed \~\~ | Unable to confirm\~\~ | The [Data Security and Protection Toolkit](https://digital.nhs.uk/data-and-information/looking-after-information/data-security-and-information-governance/data-security-and-protection-toolkit) allows organisations to measure performance against the National Data Guardian's 10 data security standards. |

| C2.3.2 | Please attach the Data Protection Impact Assessment (DPIA) relating to the product. | Provided \~\~ | Not provided\~\~ | [DPIA’s](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/) are a key part of the accountability obligations under the UK GDPR, and when done properly help organisations assess and demonstrate how they comply with data protection obligations. The Information Commissioner has provided guidance on [how to complete a DPIA](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/how-do-we-do-a-dpia/#how9) and a [sample DPIA template](https://ico.org.uk/media/for-organisations/documents/2553993/dpia-template.docx). |

| C2.4 | Please confirm your risk assessments and mitigations / access controls / system level security policies have been signed-off by your Data Protection Officer (if one is in place) or an accountable officer where exempt in question C2.2. | Confirm \~\~ | Cannot confirm\~\~ | |

| C2.5 | Please confirm where you store and process data (including any third-party products your product uses) | UK only \~\~ | In EU | Outside of EU\~\~ |

| C2.5.1 | If you process store or process data outside of the UK, please name the country and set out how the arrangements are compliant with current legislation | Free text | From 1 January 2021, the UK GDPR applies in the UK in place of the "EU GDPR'. The UK GDPR will carry across much of the existing EU GDPR legislation. The Department for Digital, Culture, Media & Sport has published two [Keeling Schedules](https://www.gov.uk/government/publications/data-protection-law-eu-exit) which show the changes to the Data Protection Act 2019 and EU GDPR. The Information Commissioner has published guidance on [international data transfers](https://ico.org.uk/for-organisations/dp-at-the-end-of-the-transition-period/data-protection-now-the-transition-period-has-ended/the-gdpr/international-data-transfers/) after the UK exit from the EU Implementation Period. | Not applicable. |

### C3 - Technical Security {#c3---technical-security}

Establishing that your product meets industry best practice security standards and that the product is stable.

Dependent on the digital health technology being procured, it is recommended that appropriate contractual arrangements are put in place for problem identification and resolution, incident management and response planning and disaster recovery.

Please provide details relating to the specific technology and not generally to your organisation.

| Code | Question | Options | Supporting information | Scoring criteria |

|---|---|---|---|---|

| C3.1 | Please attach your Cyber Essentials Certificate | Provided \~\~ | No evidence available\~\~ | [Cyber Essentials](https://www.ncsc.gov.uk/cyberessentials/overview) helps organisations guard against the most common cyber threats. The National Cyber Security Centre (NCSC) have published [cyber security guidance for small to medium enterprises](https://www.ncsc.gov.uk/section/information-for/small-medium-sized-organisations) (SME's). |

| C3.2 | Please provide the summary report of an external penetration test of the product that included Open Web Application Security Project (OWASP) Top 10 vulnerabilities from within the previous 12-month period. | Provided \~\~ | No evidence available\~\~ | The NCSC provides guidance on [penetration testing](https://www.ncsc.gov.uk/guidance/penetration-testing). The OWASP Foundation provides guidance on the [OWASP top 10 vulnerabilities](https://owasp.org/www-project-top-ten/). |

| C3.3 | Please confirm whether all custom code had a security review. | Yes - Internal code review \~\~ | Yes - External code review | No |

| C3.4 | Please confirm whether all privileged accounts have appropriate Multi-Factor Authentication (MFA)? | Yes \~\~ | No\~\~ | The NCSC provides guidance on [Multi-Factor Authentication](https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services). |

| C3.5 | Please confirm whether logging and reporting requirements have been clearly defined. | Yes \~\~ | No\~\~ | The NCSC provides guidance on [logging and protective monitoring](https://www.ncsc.gov.uk/collection/mobile-device-guidance/logging-and-protective-monitoring). To confirm yes to this question, logging (e.g., audit trails of all access) must be in place. It is acknowledged that not all developers will have advanced audit capabilities. |

| C3.6 | Please confirm whether the product has been load tested | Yes \~\~ | No\~\~ | Load testing should be performed. |

[C4 - Interoperability criteria  .md](./C4%20-%20Interoperability%20criteria%20%20.md)

## D. Key Principles for Success

The core elements defined in this section will form part of the overall review of the product or service and is a key part to ensuring that the product or service is suitable for use. The assessment will set a compliance rating and where a product or developer is not compliant highlight areas that the organisation could improve on with regards to following the core principles.

This section will be scored in relation to the [NHS service standard](https://service-manual.nhs.uk/service-standard). This will not contribute to the overall Assessment Criteria as set out in Section C.

### D1 - Usability and Accessibility - Scored Section {#d1---usability-and-accessibility---scored-section}

Establishing that your product has followed best practice.

Please note that not all sections of the NHS Service Standard are included where they are assessed elsewhere within DTAC, for example clinical safety.

| Code | Question | Options | Supporting information | Weighted score | Scoring criteria |

|---|---|---|---|---|---|

| D1.1 | Understand users and their needs in context of health and social care Do you engage users in the development of the product? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 1](https://service-manual.nhs.uk/service-standard/1-understand-users-and-their-needs-context-health-and-care) |

| D1.1.1 | If yes or working towards it, how frequently do you consider user needs in your product development and what methods do you use to engage users and understand their needs? | Free text | |  | |

| D1.2 | Work towards solving a whole problem for users Are all key user journeys mapped to ensure that the whole user problem is solved, or it is clear to users how it fits into their pathway or journey? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 2 and Point 3](https://service-manual.nhs.uk/service-standard/2-and-3-work-towards-solving-a-whole-problem-and-provide-a-joined-up-experience) are often dealt with by teams together. |

| D1.2.1 | If yes or working towards it, please attach the user journeys and/or how the product fits into a user pathway or journey | Provided \~\~ | No evidence available\~\~ | |  |

| D1.3 | Make the service simple to use Do you undertake user acceptance testing to validate usability of the system? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 4](https://service-manual.nhs.uk/service-standard/4-make-the-service-simple-to-use) |

| D1.3.1 | If yes or working towards it, please attach information that demonstrates that user acceptance testing is in place to validate usability. | Provided | ~~No evidence available~~ | |  |

| D1.4 | Make sure everyone can use the service Are you international Web Content Accessibility Guidelines (WCAG) 2.1 level AA compliant? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 5](https://service-manual.nhs.uk/service-standard/5-make-sure-everyone-can-use-the-service) The Service Manual provides information on [WCAG 2.1](https://www.gov.uk/service-manual/helping-people-to-use-your-service/understanding-wcag) level AA. The Government Digital Service provides guidance on [accessibility and accessibility statements](https://www.gov.uk/guidance/make-your-website-or-app-accessible-and-publish-an-accessibility-statement), including a sample template. |

| D1.4.1 | Provide a link to your published accessibility statement. | Free text | | 10% | The published FITFILE accessibility statement is available publicly under <https://fitfile.com/wp-content/uploads/2025/05/20250506_FITFILEAccessibilityStatement_Published.pdf>. |

| D1.5 | Create a team that includes multi-disciplinary skills and perspectives Does your team contain multidisciplinary skills? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 6](https://service-manual.nhs.uk/service-standard/6-create-a-team-that-includes-multidisciplinary-skills-and-perspectives) |

| D1.6 | Use agile ways of working Do you use agile ways of working to deliver your product? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 7](https://service-manual.nhs.uk/service-standard/7-use-agile-ways-of-working) |

| D1.7 | Iterate and improve frequently Do you continuously develop your product? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 8](https://service-manual.nhs.uk/service-standard/8-iterate-and-improve-frequently) |

| D1.8 | Define what success looks like and be open about how your service is performing Do you have a benefits case that includes your objectives and the benefits you will be measuring and have metrics that you are tracking? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 10](https://service-manual.nhs.uk/service-standard/10-define-what-success-looks-like-and-be-open-about-how-your-service-is-performing) |

| D1.9 | Choose the right tools and technology Does this product meet with NHS Cloud First Strategy? | Yes \~\~ | No | No because it is not applicable\~\~ | [NHS Service Standard Point 11](https://service-manual.nhs.uk/service-standard/11-choose-the-right-tools-and-technology) [NHS Internet First Policy](https://digital.nhs.uk/services/internet-first). |

| D1.9.1 | Does this product meet the NHS Internet First Policy? | Yes \~\~ | No | No because it is not applicable\~\~ | |

| D1.10 | Use and contribute to open standards, common components and patterns Are common components and patterns in use? | Yes \~\~ | No | Working towards it\~\~ | [NHS Service Standard Point 13](https://service-manual.nhs.uk/service-standard/13-use-and-contribute-to-open-standards-common-components-and-patterns) |

| D1.10.1 | If yes, which common components and patterns have been used? | Free text | |  | |

| D1.11 | Operate a reliable service Do you provide a Service Level Agreement to all customers purchasing the product? | Yes \~\~ | No\~\~ | [NHS Service Standard Point 14](https://service-manual.nhs.uk/service-standard/14-operate-a-reliable-service) | 10% |

| D1.12 | Do you report to customers on your performance with respect to support, system performance (response times) and availability (uptime) at a frequency required by your customers? | Yes \~\~ | No\~\~ | |  |

| D1.12.1 | Please attach a copy of the information provided to customers | Provided \~\~ | No evidence available\~\~ | |  |

| D1.12.2 | Please provide your average service availability for the past 12 months, as a percentage to two decimal places | Free text | |  | |

## Supporting Documentation {#supporting-documentation}

Please ensure that when providing evidence, documents are clearly labelled with the name of your company, the question number and the date of submission.

Possible documents to be provided are:

- A11 - CQC Report
- B4 - User journeys and data flows
- C1.1.1 - Clinical Risk Management System
- C1.1.2 - Clinical Safety Case Report
- C1.1.2 - Hazard Log
- C1.3.2 - UK Medical Device Regulations 2002 Declaration of Conformity and if applicable Certificate of Conformity
- C1.4.1 - Clinical Risk Management documentation and Conformity certificate for third party suppliers
- C2.1 - Information Commissioner's registration or completed Self-assessment Outcome Tool
- C2.2.1 Completed Information Commissioner's Self-Assessment Outcome Tool
- C2.3.2 - Data Protection Impact Assessment (DPIA)
- C3.1 - Cyber Essentials Certification
- C3.2 - External Penetration Test Summary Report
- C4.4.1 - If a wearable, evidence of how the product complies with ISO/IEEE 11073 Personal Health Data (PHD) Standards
- D1.2.1 - User Journeys and/or how the product fits into a user pathway or journey
- D1.3.1 - Supporting information showing user acceptance testing to validate usability
- D1.13.2 - Customer Performance Report
