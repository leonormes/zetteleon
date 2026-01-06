---
aliases: []
tags: []
title: Briefing on Observational Health Data Sciences and Informatics (OHDSI)
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-06T07:39:01+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2026-01-06T07:38:50+00:00
---

# Briefing on Observational Health Data Sciences and Informatics (OHDSI)

## Executive Summary

Observational Health Data Sciences and Informatics (OHDSI) is a global, open-science collaborative established to improve health outcomes by empowering a community to collaboratively generate reliable evidence from observational health data. The core mission addresses the significant challenge that the journey from raw, patient-level data to trustworthy evidence is complex, requiring a diverse range of expertise in informatics, epidemiology, statistics, and clinical science.

To overcome these challenges, OHDSI has developed a comprehensive ecosystem built on three foundational pillars:

1. **Uniform Data Standards:** At the heart of OHDSI is the Observational Medical Outcomes Partnership (OMOP) Common Data Model (CDM), which standardizes the structure of disparate observational databases (e.g., electronic health records, claims data). Paired with the OMOP Standardized Vocabularies, which harmonize the content by mapping source codes to a common set of concepts, the CDM enables the execution of the same analysis code across a distributed network of databases, fostering reproducible and generalizable research.
2. **Open-Source Analytics Tools:** OHDSI provides a robust library of open-source software to support the entire research lifecycle. Key tools include **ATLAS**, a web-based platform for designing analyses, and the **Methods Library**, a collection of R packages for executing large-scale analytics. These tools support OHDSI's three primary analytical use cases: **Clinical Characterization** (describing populations), **Population-Level Effect Estimation** (assessing causal effects of interventions), and **Patient-Level Prediction** (predicting future health outcomes for individuals).
3. **A Collaborative Community:** OHDSI functions as a distributed research network where data partners retain full control over their data, running standardized analysis packages locally and sharing only aggregate, non-identifiable results. This federated model facilitates global collaboration among data holders, methodologists, software developers, and clinical researchers, who work together openly to establish scientific best practices and generate high-quality evidence.

The OHDSI framework holistically addresses evidence quality by incorporating rigorous checks for data quality, clinical validity of definitions, software validity, and methodological validity, often through empirical calibration using negative and positive controls. This systematic approach aims to produce evidence that is not only repeatable and reproducible but also replicable and generalizable across diverse patient populations and healthcare systems worldwide.

## 1. The OHDSI Initiative: Addressing the Data-to-Evidence Challenge

The generation of reliable evidence from observational health data is an arduous journey. The process begins with diverse patient-level data captured in various source systems and aims to produce evidence that can inform clinical practice and health policy.

### 1.1. The Complexity of Observational Data and Evidence

The journey is complicated by the inherent heterogeneity of both the data sources and the desired evidence.

- **Diverse Observational Data:** Patient-level data originates from systems that vary significantly across multiple dimensions:
    - **Populations:** Pediatric vs. elderly; socioeconomic disparities.
    - **Care Setting:** Inpatient vs. outpatient; primary vs. secondary care.
    - **Data Capture Process:** Administrative claims, electronic health records (EHRs), clinical registries.
    - **Health System:** Insured vs. uninsured; differing country policies.
- **Varied Types of Evidence:** The analytical use cases for observational data are broadly categorized into three types:
    - **Clinical Characterization:** Describing populations to understand clinical trial feasibility, treatment utilization, disease natural history, and quality improvement.
    - **Population-Level Effect Estimation:** Applying causal inference methods for safety surveillance and comparative effectiveness.
    - **Patient-Level Prediction:** Using machine learning for precision medicine and disease interception.

### 1.2. A Multidisciplinary, Collaborative Solution

Successfully navigating from data to evidence requires a rare combination of skills, making individual efforts exceptionally difficult. The necessary competencies include:

- **Health Informatics:** Understanding data provenance from patient interaction to the final repository.
- **Epidemiology and Statistics:** Translating clinical questions into valid observational study designs.
- **Data Science:** Implementing computationally efficient algorithms on large-scale datasets.
- **Clinical Knowledge:** Synthesizing findings and determining their impact on health policy and practice.

Recognizing that no single individual or organization possesses all requisite skills, OHDSI was formed as an open-science collaborative. It builds upon the foundation of the Observational Medical Outcomes Partnership (OMOP), a public-private partnership that advanced the science of active medical product safety surveillance. OHDSI fosters collaboration across a global network, with collaborators spanning North America, Europe, Asia, and other regions.

The OHDSI model is a **distributed network**, where each data partner retains full autonomy and governance over their patient-level data. Instead of pooling data, standardized analytical code is sent to each partner to be executed locally. Only aggregate summary statistics, which do not contain patient-level information, are shared back for synthesis.

## 2. Foundational Standards: The OMOP Common Data Model and Vocabularies

To enable standardized analytics across a distributed network, OHDSI relies on a uniform representation of data through the OMOP Common Data Model and its associated vocabularies.

### 2.1. The OMOP Common Data Model (CDM)

The CDM is a person-centric relational data model designed to harmonize observational health data from disparate sources into a common format. Its purpose is to create a structure optimized for analysis rather than the operational needs of healthcare delivery or payment.

**Key Design Principles of the CDM:**

|   |   |
|---|---|
|Principle|Description|
|**Suitability for Purpose**|Data is organized for optimal analysis, not operational needs.|
|**Data Protection**|Patient-identifying information is limited or omitted.|
|**Person-Centric Model**|All clinical event tables link back to a person and include a date.|
|**Standardized Vocabularies**|Content is standardized using a comprehensive set of healthcare concepts.|
|**Maintaining Source Codes**|Original source codes are stored alongside standard concepts for full traceability.|
|**Technology Neutrality**|The model can be implemented in any relational database system (e.g., Oracle, SQL Server, PostgreSQL).|
|**Scalability**|The model is optimized for processing and analysis of very large databases.|

The CDM organizes data into a series of standardized tables, including tables for patient demographics (PERSON), observation periods (OBSERVATION_PERIOD), and clinical events such as visits, conditions, drug exposures, and procedures.

### 2.2. The OMOP Standardized Vocabularies

The Standardized Vocabularies are a mandatory component of the CDM, serving to standardize the _content_ of the data. They provide a common repository and a mapping mechanism for the hundreds of medical coding systems used worldwide (e.g., ICD-9-CM, SNOMED-CT, RxNorm, NDC, CPT4).

**Core Components of the Vocabularies:**

- **Concepts:** The fundamental building blocks representing the semantic meaning of a clinical event. Every concept has a unique ID, a name, a domain, and the vocabulary it originates from.
- **Domains:** Each concept is assigned a domain (e.g., "Condition," "Drug," "Procedure"), which directs where data associated with that concept should be stored in the CDM tables.
- **Concept Types:** Concepts are categorized to facilitate standardized analysis:
    - **Standard Concepts:** A single concept designated to uniquely represent a specific clinical meaning across all databases. Only Standard Concepts are used in the primary `_CONCEPT_ID` fields of the CDM tables. For example, SNOMED-CT is the standard for conditions.
    - **Source Concepts (Non-Standard):** Concepts from various coding systems that are found in the source data. These are mapped to Standard Concepts.
    - **Classification Concepts:** Non-standard concepts that can be used for hierarchical queries to group Standard Concepts. For example, MedDRA concepts are used to classify condition concepts.

This system ensures that a query for "Atrial fibrillation" will retrieve the relevant patients regardless of whether their original record used an ICD-9, ICD-10, or SNOMED code.

## 3. Data Transformation: The Extract, Transform, Load (ETL) Process

The ETL process is the technical undertaking of converting native, raw data into the OMOP CDM format. This involves restructuring the data, mapping local codes to the Standardized Vocabularies, and loading the transformed data into the CDM tables.

**Best Practices for ETL Development:**

The OHDSI community has developed a four-step best practice for creating a repeatable and high-quality ETL:

1. **Design the ETL:** Data experts and CDM experts collaborate to design the mapping from source tables and fields to the CDM.
2. **Create Code Mappings:** Individuals with medical knowledge create the mappings from source vocabulary codes to standard concepts.
3. **Implement the ETL:** A technical person implements the design as automated scripts (e.g., in SQL).
4. **Perform Quality Control:** All stakeholders are involved in iterative testing and quality control of the transformed data.

**OHDSI Tools for ETL Support:**

- **White Rabbit and Rabbit-in-a-Hat:** A software suite for designing the ETL. White Rabbit scans the source database to profile its structure and content. Rabbit-in-a-Hat provides a graphical interface for collaboratively designing the table-to-table and field-to-field mappings.
- **Usagi:** A tool that aids in the manual mapping of source codes to standard vocabulary concepts. It uses textual similarity to suggest mappings, which a domain expert then reviews, approves, or corrects.

To ensure consistency across the network, the **THEMIS** initiative works to establish and document conventions for handling common ETL scenarios, such as how to manage records with missing birth years.

## 4. Analytical Framework and Use Cases

Once data is in the CDM format, it can be used for three primary analytical purposes.

- **Characterization:** Describes what happened to a population of interest, answering questions about baseline characteristics, treatment patterns, and outcome rates. This includes:
    - **Database-level Characterization:** High-level summary statistics of an entire database.
    - **Cohort Characterization:** Descriptive statistics of a specific group of people (a cohort).
    - **Treatment Pathways:** Analysis of the sequence of treatments patients receive over time.
    - **Incidence Rate Analysis:** Measuring the rate of new outcomes in a population.
- **Population-Level Effect Estimation:** Estimates the causal effect of an exposure on an outcome, answering questions about comparative effectiveness and safety. It aims to emulate a target trial by comparing outcomes between a target and a comparator cohort while adjusting for confounding. Outputs are typically measures like hazard ratios or relative risks.
- **Patient-Level Prediction:** Develops models to predict the probability of a future outcome for an individual patient, answering the question "What will happen to me?". This use case applies machine learning algorithms to historical patient data to create risk scores for applications like precision medicine and disease interception.

## 5. Core OHDSI Analytics Tooling

OHDSI provides a suite of open-source tools to implement these analytical use cases. These tools are designed to be used against any database in the OMOP CDM format.

### 5.1. ATLAS

ATLAS is a free, publicly available, web-based platform for the design and execution of observational analyses. It provides a user-friendly interface for researchers to perform complex tasks without needing to write code directly. Key features include:

- **Cohort Definition:** A graphical tool to define patient populations based on complex inclusion and exclusion criteria.
- **Concept Set Creation:** An interface to search the standardized vocabularies and create sets of concepts for use in cohort definitions.
- **Characterization:** A module to generate descriptive statistics for defined cohorts.
- **Population-Level Estimation:** A guided workflow to design and execute comparative cohort studies.
- **Patient-Level Prediction:** A module to design, train, and evaluate prediction models.

Analyses designed in ATLAS can be executed against a local CDM, and the platform can also generate R packages for execution in environments without an ATLAS installation.

### 5.2. OHDSI Methods Library

The Methods Library is a collection of open-source R packages that provide the underlying statistical and computational engines for OHDSI analyses. These packages can be used directly by R programmers for custom studies or are called by ATLAS to execute analyses.

**Key Packages in the Methods Library:**

|   |   |   |
|---|---|---|
|Category|Package Name|Description|
|**Supporting Packages**|`DatabaseConnector`|Connects to a wide range of database platforms.|
||`SqlRender`|Translates a standard OHDSI SQL dialect to platform-specific SQL.|
||`FeatureExtraction`|Automatically extracts large sets of features (covariates) for specified cohorts.|
||`Cyclops`|A highly efficient implementation for large-scale regularized regression.|
|**Prediction & Estimation**|`CohortMethod`|Implements the new-user cohort method design for comparative effect estimation.|
||`SelfControlledCaseSeries`|Implements the SCCS design for population-level effect estimation.|
||`PatientLevelPrediction`|Implements a framework to build and validate predictive models.|
|**Method Characterization**|`EmpiricalCalibration`|Uses negative and positive controls to calibrate p-values and confidence intervals.|

## 6. A Framework for Evidence Quality

OHDSI emphasizes that generating reliable evidence requires a holistic view of quality that extends beyond the source data. The goal is to produce evidence that is **reproducible**, **replicable**, **generalizable**, and **calibrated**. This is achieved by assessing four key components of evidence quality.

|   |   |   |
|---|---|---|
|Component|Question Addressed|OHDSI Tools & Methods|
|**Data Quality**|Are the data complete, plausible, and conformant to the CDM structure?|**ACHILLES** for database characterization; **Data Quality Dashboard (DQD)** for systematic conformance checks.|
|**Clinical Validity**|Does the analysis accurately reflect the clinical intent?|Cohort validation via source record verification or the **PheValuator** package, which creates a probabilistic gold standard.|
|**Software Validity**|Does the analysis software perform as expected?|Rigorous software development lifecycle for the Methods Library, including version control, documentation, and automated unit testing.|
|**Method Validity**|Is the study design valid for answering the research question?|Use of study diagnostics (e.g., covariate balance) and empirical evaluation using **negative and positive controls** to assess operating characteristics like bias, precision, and error rates.|

## 7. Conducting OHDSI Studies

The OHDSI framework provides a structured approach for conducting observational studies, from initial conception to final dissemination.

### 7.1. General Study Steps

1. **Develop Research Question:** Clearly define the study question.
2. **Write Protocol:** Fully specify the study design, populations, and analytical approach in a formal protocol before execution.
3. **Review Data Quality:** Use tools like ACHILLES and DQD to assess data feasibility.
4. **Define Cohorts:** Use ATLAS to create detailed, reusable definitions for all study populations (e.g., target, comparator, outcome cohorts).
5. **Perform Diagnostics:** Execute study-specific checks to ensure the validity of the design.
6. **Create a Study Package:** Bundle all code, cohort definitions, and analysis specifications into a self-contained, reproducible package, typically in R.
7. **Execute and Disseminate:** Run the study package and share results, often through publications and interactive web applications.

### 7.2. OHDSI Network Studies

A study becomes a network study when it is executed across multiple databases at different institutions. Open OHDSI network studies adhere to principles of full transparency:

- All study documentation, code, and aggregate results are made publicly available, typically on GitHub.
- The study protocol is published before the study begins.
- Collaboration is open to any institution with an OMOP CDM-compliant database.
- Data stewards execute the study package locally and share only aggregate, non-identifiable results, ensuring patient privacy and data security.

This approach leverages the power of the global OHDSI network to produce evidence that is robust and generalizable across diverse populations and healthcare contexts.
