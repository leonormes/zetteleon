---
aliases: ["OMOP Vocabularies", "Standard Concepts", "Athena"]
confidence: "High"
created: 2026-01-06
epistemic: "Standard"
last_reviewed: 
modified: 
purpose: "To define the semantic layer of OHDSI, explaining how source codes are mapped to Standard Concepts."
review_interval: "1 year"
see_also: 
  - "[[SoT - OMOP Common Data Model (CDM)]]"
  - "[[SoT - OHDSI and FHIR Convergence]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "vocabulary", "semantics", "ontology"]
title: SoT - OHDSI Standardized Vocabularies
type: "SoT"
uid: 
updated: 
---

# SoT - OHDSI Standardized Vocabularies

> **Core Principle:** The "Rosetta Stone" of the network. While the CDM standardizes the *structure*, the Vocabularies standardize the *content*, enabling a query for "Diabetes" to find records coded in ICD-9, ICD-10, SNOMED, or Read codes.

## 1. The Concept Architecture

The vocabulary is a unified ontology built from over 130 source vocabularies (SNOMED, RxNorm, LOINC, etc.).

### A. Concept Types
1.  **Standard Concepts:** The "One Truth." For any clinical idea, exactly **one** concept is designated as Standard.
    *   *Conditions:* SNOMED.
    *   *Drugs:* RxNorm.
    *   *Measurements:* LOINC.
2.  **Source Concepts:** The "Many Dialects." Codes from local systems (ICD-10, NDC) are ingested but marked as Non-Standard.
3.  **Classification Concepts:** Hierarchical groupers (e.g., MedDRA, ATC) used for broad queries.

### B. The Mapping Relationship (`Maps to`)
This is the engine of interoperability.
*   **Input:** Source Code (e.g., ICD-10 `E11` "Type 2 Diabetes").
*   **Relationship:** `Maps to` (Relationship ID).
*   **Target:** Standard Concept (e.g., SNOMED `44054006` "Diabetes mellitus type 2").

**Analytic Implication:** Researchers write queries using **Standard Concepts**. The ETL process handles the translation.

## 2. The Hierarchy (`CONCEPT_ANCESTOR`)

The vocabulary flattens complex poly-hierarchies into a simple lookup table: `CONCEPT_ANCESTOR`.

*   **Logic:** If you query for "Heart Disease" (Ancestor), the system automatically includes "Myocardial Infarction," "Heart Failure," and "Atrial Fibrillation" (Descendants).
*   **UX Pattern:** "Explode" or "Include Descendants" in cohort builders uses this table.

## 3. Domain-Specific Logic

### A. Drugs (RxNorm)
*   **Attribute-Based:** Drugs are defined by Ingredient, Strength, and Dose Form.
*   **Granularity:** Analyses are usually run at the **Ingredient** level (e.g., "Metformin") to capture all brands and formulations.

### B. Conditions (SNOMED)
*   **Subsumption:** The hierarchy relies on "Is-A" relationships. A specific disease implies all its parent categories.

## 4. Maintenance & Tools
*   **Athena:** The web portal to browse and download vocabularies.
*   **Usagi:** The tool for mapping local/custom codes (string matching) to Standard Concepts.
*   **Phoebe:** A recommender system that suggests related concepts based on co-occurrence in the network.