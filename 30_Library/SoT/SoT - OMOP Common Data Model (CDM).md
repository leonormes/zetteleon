---
aliases: ["OMOP CDM", "Common Data Model", "OHDSI Schema"]
confidence: "High"
created: 2026-01-06
epistemic: "Standard"
last_reviewed: 
modified: 
purpose: "To define the structural and semantic standards of the OMOP Common Data Model."
review_interval: "1 year"
see_also: 
  - "[[MoC - OHDSI & OMOP Architecture]]"
  - "[[SoT - OHDSI Standardized Vocabularies]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "omop", "data-model", "schema"]
title: SoT - OMOP Common Data Model (CDM)
type: "SoT"
uid: 
updated: 
---

# SoT - OMOP Common Data Model (CDM)

> **Core Principle:** Transform disparate observational data into a common structure (Tables) and common language (Vocabularies) to enable "Write Once, Run Anywhere" analytics.

## 1. Architectural Principles

1.  **Person-Centric:** All clinical event tables (`condition_occurrence`, `drug_exposure`) link back to a central `PERSON` table via `person_id`.
2.  **Design for Analytics (OLAP):** Optimized for cohort generation and statistical analysis, not for point-of-care data entry (OLTP).
3.  **Technology Neutral:** Can be implemented on PostgreSQL, SQL Server, Oracle, Redshift, Snowflake, etc.
4.  **Protection by Design:** Limited PII (no names, shifted dates) to support federated research.

## 2. The Domain Architecture

Data is organized by **Domain** (the nature of the event) rather than the **Source** (where it came from).

| Domain | Description | Example |
|:--- |:--- |:--- |
| **Condition** | Diagnoses and signs/symptoms. | Type 2 Diabetes, Headache. |
| **Drug** | Prescriptions and administrations. | Metformin, Aspirin. |
| **Procedure** | Interventions and surgeries. | Appendectomy, X-Ray. |
| **Measurement** | Lab values and vitals. | HbA1c, Blood Pressure. |
| **Observation** | Facts that don't fit above. | Family History, Social History. |

**The Routing Logic:** The destination table is determined by the **Standard Concept ID**. If a source record says "Family History of Diabetes" (ICD-10 `Z83.3`), the Vocabulary defines this as an `Observation`, so it moves to the `OBSERVATION` table, not `CONDITION_OCCURRENCE`.

## 3. The Dual-Coding System (Crucial for Queries)

To preserve data fidelity while enabling standardization, OMOP uses a **Dual-Coding** pattern for every event.

| Field Name | Type | Purpose | UX/Query Implication |
|:--- |:--- |:--- |:--- |
| `_source_value` | String | **Verbatim.** The raw code from the source (e.g., "I10"). | **Display Only.** Use for validation/audit. Do not query for analytics. |
| `_source_concept_id` | Int | **Foreign Key.** The OHDSI ID for the source code. | **Mapping Trace.** Links back to the source vocabulary. |
| `_concept_id` | Int | **Standard.** The OHDSI ID for the *meaning* (e.g., SNOMED 320128). | **Query Target.** Always filter on this column to find patients. |

## 4. Time and Logic (Themis)

*   **Observation Period:** Defines the span of time a patient is "visible" to the system. No events outside this window are analytically valid.
*   **Themis Conventions:** Binding rules that resolve ambiguity (e.g., "If birth year is missing, drop the person").

## 5. Related Components
*   [[SoT - OHDSI Standardized Vocabularies]] (The Semantic Layer).
*   [[SoT - OHDSI ETL & Data Quality]] (How data gets in).
