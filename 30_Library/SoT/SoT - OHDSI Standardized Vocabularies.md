---
aliases: ["Athena", "OMOP Vocabularies", "Standard Concepts"]
created: 2026-01-06T18:52:00+00:00
last_reviewed: 
modified: 2026-05-26T11:44:18+00:00
status: "Active"
tags: ["ohdsi", "ontology", "semantics", "vocabulary"]
title: SoT - OHDSI Standardized Vocabularies
type: "SoT"
updated: 
---

## SoT - OHDSI Standardized Vocabularies

> Core Principle: The "Rosetta Stone" of the network. While the CDM standardizes the _structure_, the Vocabularies standardize the _content_, enabling a query for "Diabetes" to find records coded in ICD-9, ICD-10, SNOMED, or Read codes.

### 1. The Concept Architecture

The vocabulary is a unified ontology built from over 130 source vocabularies (SNOMED, RxNorm, LOINC, etc.).

#### A. Concept Types

1. Standard Concepts: The "One Truth." For any clinical idea, exactly one concept is designated as Standard.
    - _Conditions:_ SNOMED.
    - _Drugs:_ RxNorm.
    - _Measurements:_ LOINC.
2. Source Concepts: The "Many Dialects." Codes from local systems (ICD-10, NDC) are ingested but marked as Non-Standard.
3. Classification Concepts: Hierarchical groupers (e.g., MedDRA, ATC) used for broad queries.

#### B. The Mapping Relationship (`Maps to`)

This is the engine of interoperability.

- Input: Source Code (e.g., ICD-10 `E11` "Type 2 Diabetes").
- Relationship: `Maps to` (Relationship ID).
- Target: Standard Concept (e.g., SNOMED `44054006` "Diabetes mellitus type 2").

Analytic Implication: Researchers write queries using Standard Concepts. The ETL process handles the translation.

### 2. The Hierarchy (`CONCEPT_ANCESTOR`)

The vocabulary flattens complex poly-hierarchies into a simple lookup table: `CONCEPT_ANCESTOR`.

- Logic: If you query for "Heart Disease" (Ancestor), the system automatically includes "Myocardial Infarction," "Heart Failure," and "Atrial Fibrillation" (Descendants).
- UX Pattern: "Explode" or "Include Descendants" in cohort builders uses this table.

### 3. Domain-Specific Logic

#### A. Drugs (RxNorm)

- Attribute-Based: Drugs are defined by Ingredient, Strength, and Dose Form.
- Granularity: Analyses are usually run at the Ingredient level (e.g., "Metformin") to capture all brands and formulations.

#### B. Conditions (SNOMED)

- Subsumption: The hierarchy relies on "Is-A" relationships. A specific disease implies all its parent categories.

### 4. Maintenance & Update Cycle

The vocabularies are updated on a regular cadence, typically twice a year (February and August). These updates reflect changes from upstream sources (ICD, SNOMED, etc.).

#### A. Maintenance Workflow

- Data Ingestion: The OHDSI Vocabulary Team pulls updates from the Unified Medical Language System (UMLS) and prunes them for CDM suitability.
- Athena: The central portal to search, browse, and download the finalized vocabulary files.
- Tantalus: An analytical package used to run a "diff" between vocabulary versions to identify changed, deprecated, or orphan codes.

#### B. Update Protocol

1. Align with Biannual Schedule: Schedule maintenance around the February/August major releases.
2. Review Release Notes: Consult the "What's New" file and ATHENA to identify concept changes.
3. ETL Refresh: Vocabulary updates often require a full re-run of the ETL process to ensure local data reflects current standard concept mappings.

### 5. Tools

- Athena: Web portal for browsing and downloading.
- Usagi: Mapping local/custom codes to Standard Concepts.
- Phoebe: Recommender system for concept selection.
