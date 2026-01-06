---
aliases: []
tags: []
title: The Book of OHDSI
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-06T07:49:52+00:00
modified: 2026-01-06T07:50:37+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

**The Book of OHDSI** serves as the central knowledge repository for the OHDSI community, documenting the collaborative’s foundational principles. A significant portion of this text, specifically "Part II: Uniform Data Representation," is dedicated to **Data Standards**. These standards are the prerequisite for OHDSI’s mission, enabling the transformation of disparate observational databases into a common format that facilitates large-scale, reproducible analytics,.

The sources detail three primary pillars of Data Standards within the OHDSI ecosystem: the OMOP Common Data Model (CDM), Standardized Vocabularies, and the conventions (Themis) that govern them.

### 1. The OMOP Common Data Model (CDM)

The OMOP CDM is an open community data standard designed to harmonize the structure and content of observational data, enabling the execution of standardized analysis code across a distributed network,.

- **Person-Centric Architecture:** The CDM is a relational database model optimized for analysis rather than healthcare operations. It is "person-centric," meaning all clinical event tables (such as drug exposures or condition occurrences) link back to a central `PERSON` table,. This allows for a longitudinal view of a patient’s healthcare experience.
- **Design Principles:** _The Book of OHDSI_ outlines key design principles for the CDM, including **technology neutrality** (it can be implemented in PostgreSQL, SQL Server, Oracle, etc.) and **suitability for purpose** (it is optimized for analytics rather than reimbursement or point-of-care entry).
- **Domain Organization:** Data is organized into "Domains" based on the nature of the clinical event (e.g., Condition, Drug, Procedure, Measurement) rather than the source file it came from,. For example, a "Family History of Diabetes" might appear in a diagnosis field in a source electronic health record (EHR), but in the OMOP CDM, it is mapped to the "Observation" domain because it represents a patient fact rather than a clinical condition currently affecting the patient.
- **Privacy and Security:** The model is designed to protect patient privacy by limiting data elements like names and precise birth dates, supporting the federation of research where patient-level data stays local,.

### 2. OHDSI Standardized Vocabularies

While the CDM standardizes the _structure_ of the data (tables and fields), the OHDSI Standardized Vocabularies standardize the _content_ (the actual medical concepts). _The Book of OHDSI_ describes the vocabulary as the "Rosetta Stone" of the network, enabling semantic interoperability.

- **Concept-Based System:** All clinical events are expressed as "Concepts" stored in a `CONCEPT` table. This system harmonizes over 9 million concepts from more than 130 vocabularies (e.g., SNOMED, RxNorm, LOINC, ICD-10),,.
- **Standard vs. Source Concepts:** A crucial convention in OHDSI data standards is the distinction between **Source Concepts** (the code used in the raw data, e.g., an ICD-10 code for "Type 2 Diabetes") and **Standard Concepts** (the mandatory OHDSI standard, typically SNOMED for conditions or RxNorm for drugs). The CDM stores _both_, allowing researchers to trace back to the original source while performing analyses on the standard version.
- **Concept Ancestry:** The vocabulary includes a `CONCEPT_ANCESTOR` table that defines hierarchical relationships. This allows researchers to query for a high-level concept (e.g., "Diabetes mellitus") and automatically include all specific descendants (e.g., "Type 2 diabetes with renal complications"), simplifying cohort definition.
- **Mapping Challenges:** The sources acknowledge that mapping is "lossy" and technically demanding. For instance, mapping UK-specific drug codes (dm+d) to the US-centric RxNorm standard involves translating complex hierarchies (Virtual Therapeutic Moiety to Ingredient), which is critical for international interoperability,.

### 3. Conventions and Themis

To ensure consistency across the network, OHDSI established **THEMIS**, a workgroup dedicated to developing standard conventions that go beyond the basic structural requirements of the CDM. Documented in the _Themis Repository_, these conventions dictate how to handle ambiguous data scenarios—such as how to record a patient with a missing birth year—to ensure that an ETL (Extract, Transform, Load) process at one site produces data comparable to another site,.

### 4. Implementation and Tooling

_The Book of OHDSI_ and the provided sources emphasize that Data Standards are the foundation for the entire OHDSI software ecosystem.

- **ETL Processes:** Converting data to the OMOP CDM is a rigorous undertaking involving design, mapping, and quality control. Tools like **WhiteRabbit** (for profiling source data) and **Rabbit-in-a-Hat** (for mapping structure) are standard parts of this workflow. Newer tools like **SQLMesh** are being adopted to improve the efficiency and versioning of these pipelines.
- **Data Quality:** Adherence to standards is verified using the **Data Quality Dashboard (DQD)**, which runs thousands of checks against the CDM to ensure conformance (adherence to formats) and plausibility (believability of values),.
- **Interoperability with Other Standards:** The community is actively working on harmonizing OHDSI standards with other global standards. This includes a collaboration with **HL7** to integrate FHIR (Fast Healthcare Interoperability Resources) with OMOP to support both clinical care and observational research,. Furthermore, projects like **Bridge2AI** are extending the OMOP CDM to handle multimodal data, such as waveforms and imaging.

### 5. FAIR Principles and Metadata

The sources highlight a growing focus on making OHDSI data standards compliant with **FAIR principles** (Findable, Accessible, Interoperable, Reusable).

- **RO-Crate:** The **Research Object Crate (RO-Crate)** model is being used to package OHDSI research artifacts (code, data specifications, results) with rich metadata. This allows for a "research crate" that encapsulates the entire lifecycle of a study, ensuring transparency and reproducibility,.
- **Metadata Management:** Initiatives are underway to extend the CDM to better capture dataset provenance and vocabulary versions using semantic web standards like Schema.org and JSON-LD, improving the findability of datasets after they have been harmonized,.

In summary, _The Book of OHDSI_ frames Data Standards not merely as a technical formatting exercise, but as a "team sport" and a necessary prerequisite for generating reliable real-world evidence,. The combination of the OMOP CDM, Standardized Vocabularies, and Themis conventions creates a uniform language that allows a federated network of over 800 million patient records to function as a cohesive research instrument.
