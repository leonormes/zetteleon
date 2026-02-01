---
aliases: ["Athena", "OMOP Vocabularies", "Standard Concepts"]
created: 2026-01-06T18:52:00+00:00
last_reviewed: 
modified: 2026-02-01T15:07:54+00:00
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

### 4. Maintenance & Tools

- Athena: The web portal to browse and download vocabularies.
- Usagi: The tool for mapping local/custom codes (string matching) to Standard Concepts.
- Phoebe: A recommender system that suggests related concepts based on co-occurrence in the network.
