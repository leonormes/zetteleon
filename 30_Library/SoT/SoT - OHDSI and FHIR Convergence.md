---
aliases: [FHIR Facade, OMOP on FHIR, Vulcan Accelerator]
conformant: false
created: 2026-01-06T19:30:40+00:00
last_reviewed: null
modified: 2026-08-29T09:36:40+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-ohdsi-and-fhir-convergence
status: Active
tags: [fhir, interoperability, ohdsi, SoftwareEngineering/Architecture]
title: SoT - OHDSI and FHIR Convergence
type: sot
updated: null
---

## SoT - OHDSI and FHIR Convergence

> The Convergence: FHIR and OMOP are complementary, not competing.
> -  FHIR: Optimized for Exchange and Transactional access (OLTP). Moving data _between_ systems (EHR to App).
> -   OMOP: Optimized for Analytics and Population queries (OLAP). Asking questions _across_ the system.

### 1. The Integration Patterns

#### A. The FHIR Facade (OMOP as Backend)

Scenario: You have an OMOP database, but you want to support modern apps that speak FHIR.

- Architecture: Wrap the OMOP Relational DB in a "Translation Layer."
- Mechanism:
    - _Request:_ `GET /Patient/123` (FHIR).
    - _Translation:_ Query `SELECT * FROM person WHERE person_id = 123`.
    - _Response:_ Map columns to FHIR JSON and return.
- Benefit: Enables interoperability without migrating data.

#### B. OMOP-on-FHIR (FHIR as Source)

Scenario: You have a FHIR repository (e.g., Azure Health Data Services) and want to run OHDSI analytics.

- Architecture: An ETL pipeline transforms FHIR resources into OMOP Tables.
- Mechanism:
    - `FHIR Condition` -> `OMOP CONDITION_OCCURRENCE`.
    - `FHIR Observation` -> `OMOP OBSERVATION`.
- Challenge: Semantic Mapping. FHIR uses local codes (or LOINC/SNOMED directly). OMOP requires strict mapping to Standard Concept IDs.

### 2. The "Vulcan" Accelerator

A formal HL7/OHDSI collaboration to standardize these mappings.

- Goal: To make the translation "lossless" and bidirectional where possible.
- Use Case: Clinical Trial Scoping. Use FHIR to find patients in the EHR, use OMOP to calculate feasibility.

### 3. Developer Implications

If you are building a Query Builder:

1. Transport vs. Storage: You might receive data via FHIR (Transport), but you must query it using OMOP logic (Storage) to get performance at scale.
2. Vocabulary: Even if the source is FHIR, you must use the OMOP Vocabulary to perform hierarchical queries (e.g., "Find all Heart Diseases"), as FHIR servers often lack deep ontological reasoning capabilities compared to the OMOP `CONCEPT_ANCESTOR` table.
