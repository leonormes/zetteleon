---
aliases:
- OHDSI ETL
- Rabbit-in-a-Hat
- WhiteRabbit
created: 2026-01-06 18:52:01+00:00
modified: 2026-07-04 10:50:54+00:00
permalink: llmeon/30-library/so-t/so-t-ohdsi-etl-process
tags:
- data_engineering
- etl
- ohdsi
- sot
title: SoT - OHDSI ETL Process
prodos:
  kind: sot
  lifecycle: stable
  review:
    last_reviewed: 2026-01-06
---


## 1. Definitive Statement

> [!definition] Definition
> The OHDSI ETL (Extract, Transform, Load) is the engineering process of converting data from a native schema (Source) to the OMOP CDM (Target). It is not just a format change; it is a Semantic Transformation governed by community conventions.

---

## 2. The Four-Stage Lifecycle

OHDSI promotes a standardized workflow to ensure transparency and quality.

### Phase 1: Design (Scan & Profile)

- Goal: Understand the "shape" of the source data.
- Tool: WhiteRabbit.
- Action: Scans source tables/CSVs. Generates a "Scan Report" detailing table structures and value frequencies (e.g., "Column `Gender`: 'M' (40%), 'F' (40%), 'Unk' (20%)").

### Phase 2: Map (Logical Specification)

- Goal: Define the translation rules without writing code.
- Tool: Rabbit-in-a-Hat.
- Action: A GUI tool where the architect draws lines from Source columns to CDM columns.
- Output: An ETL Specification document.

### Phase 3: Implement (Code)

- Goal: Execute the transformation.
- Tools: SQL, Python, R, dbt, SQLMesh.
- Key Logic:
    - Vocabulary Lookup: Joining source codes against `CONCEPT_RELATIONSHIP` to find `concept_id`s.
    - Themis Conventions: Applying logic rules (e.g., "If birth year is missing, drop the person").
    - Stem Table: Advanced ETLs use a "Stem" staging table to let the Vocabulary Domain drive the final table destination.

### Phase 4: Validate (Quality Assurance)

- Goal: Prove the data is fit for research.
- Tool: Data Quality Dashboard (DQD).
- Framework (Kahn):
    1. Conformance: Does it fit the schema? (Data types, FKs).
    2. Completeness: Is data missing? (Null columns, unmapped concepts).
    3. Plausibility: Does it make sense? (e.g., No males with pregnancy codes; no birth dates in the future).

---

## 3. Strategic Considerations

### 3.1 Unmapped Data (Concept ID 0)

- Rule: If a source code cannot be mapped to a Standard Concept, the `_concept_id` is set to `0`.
- Risk: `0` is a valid integer. Queries must explicitly handle/exclude `0` to avoid polluting cohorts with "unknown" data.

### 3.2 The Observation Period

- Definition: The derived table `OBSERVATION_PERIOD` defines the "trust interval" for a patient.
- Constraint: You cannot query for "absence of disease" outside of these dates. If a patient is not in an observation period, they effectively do not exist.
