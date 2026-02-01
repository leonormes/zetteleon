---
aliases: ["Common Data Model", "OMOP CDM"]
created: 2026-01-06T18:52:00+00:00
last_reviewed: 2026-01-06
modified: 2026-02-01T15:07:54+00:00
status: "stable"
tags: ["data_model", "ohdsi", "schema", "sot"]
title: SoT - OMOP Common Data Model
type: "SoT"
---

## 1. Definitive Statement

> [!definition] Definition
> The OMOP Common Data Model (CDM) is a person-centric relational database schema designed to standardize the structure of disparate observational health data (EHR, Claims, Registries).
>
> It optimizes for Analysis (reading/querying), not Operations (writing/billing).

### 1.1 Design Principles

- Person-Centric: All clinical events link to a single `PERSON` table.
- Technology Neutral: Can be implemented on Postgres, SQL Server, Oracle, Redshift, etc.
- Domain-Driven: Data is organized by Clinical Domain (Condition, Drug, Procedure), not by source file structure.

---

## 2. Structural Architecture

The CDM partitions the database into logical schemas (conceptually, if not physically).

### 2.1 The Standardized Clinical Data Tables

These tables hold the patient data.

| Table | Purpose | Key Foreign Keys |
|:--- |:--- |:--- |
| PERSON | Demographics (DOB, Gender, Race). The root anchor. | `person_id` |
| OBSERVATION_PERIOD | Critical. Defines the time spans a patient was "visible" to the system. | `person_id` |
| CONDITION_OCCURRENCE | Diagnoses, symptoms, and health states. | `condition_concept_id` |
| DRUG_EXPOSURE | Prescriptions, dispenses, and administrations. | `drug_concept_id` |
| MEASUREMENT | Lab results, vitals, quantitative values. | `measurement_concept_id` |
| VISIT_OCCURRENCE | Encounters (Inpatient, Outpatient, ER). | `visit_concept_id` |

### 2.2 The Standardized Vocabulary Tables

These tables define the "Language" of the data (See [[SoT - OHDSI Standardized Vocabularies]]).

- `CONCEPT`
- `CONCEPT_RELATIONSHIP`
- `CONCEPT_ANCESTOR`

### 2.3 The Results Schema (Writeable)

_Standard OHDSI tools assume this schema exists and is writeable._

- `COHORT`: Stores the subjects and date ranges that satisfy a specific phenotype.
- `ACHILLES_RESULTS`: Stores pre-computed characterization statistics.

---

## 3. Data Representation (The Dual-Coding System)

To maintain data lineage while enabling standardized analysis, the CDM uses a dual-coding pattern for every event.

| Column | Type | Purpose | UX/Query Role |
|:--- |:--- |:--- |:--- |
| `_source_value` | String | Verbatim. The raw code/text from the source system (e.g., "ICD10: I10"). | Audit/Verify. Display to user for confidence. Do not query. |
| `_source_concept_id` | Int | Intermediate. The OHDSI ID for that specific source code. | Traceability. Used to verify mapping logic. |
| `_concept_id` | Int | Standard. The SNOMED/RxNorm ID representing the meaning. | Analysis Target. ALL queries must filter on this column. |

### 3.1 Domain Assignment Logic

A generic source code (e.g., a billing code) is routed to a specific table based on the Domain of its mapped Standard Concept.

- _Example:_ If a "Family History" code appears in a diagnosis file, but maps to an `Observation` domain concept, the ETL moves it to the `OBSERVATION` table, not `CONDITION_OCCURRENCE`.
