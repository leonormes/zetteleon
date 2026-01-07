---
aliases: ["OMOP ETL", "Data Quality Dashboard", "DQD", "Rabbit-in-a-Hat"]
confidence: "High"
created: 2026-01-06T19:27:38+00:00
epistemic: "Process"
last_reviewed: 
modified: 2026-01-06T19:35:55+00:00
purpose: "To define the lifecycle of transforming source data into OMOP CDM and validating its quality."
review_interval: "1 year"
see_also: 
  - "[[SoT - OMOP Common Data Model (CDM)]]"
  - "[[SoT - OHDSI Standardized Vocabularies]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "etl", "data-quality", "process"]
title: SoT - OHDSI ETL & Data Quality
type: "SoT"
uid: 
updated: 
---

# SoT - OHDSI ETL & Data Quality

> **The ETL Lifecycle:** Design -> Map -> Implement -> Evaluate. This is not a one-time script, but a maintained software pipeline.

## 1. The Design Phase (Profiling)

Before mapping, you must understand the "shape" of the source.

- **Tool:** **WhiteRabbit**.
- **Action:** Scans the source database to generate frequency distributions of every column.
- **Output:** A Scan Report. This tells you that "Gender" contains `M`, `F`, and `NULL`.

## 2. The Mapping Phase (Logic)

Defining the translation rules without writing code.

- **Tool:** **Rabbit-in-a-Hat**.
- **Action:** Visual interface to draw lines from Source Tables to CDM Tables.
- **Output:** A Design Document (Spec).
- **Tool:** **Usagi**.
- **Action:** Maps source codes (local dictionaries) to Standard Concepts.

## 3. The Implementation Phase (Build)

Translating the spec into executable code.

- **Legacy:** Custom SQL scripts.
- **Modern:** **dbt** or **SQLMesh** frameworks.
- **Logic:**
    - **Themis Conventions:** Binding rules for ambiguity (e.g., "Drop patients with no birth year").
    - **Dependency:** Build `PERSON` first; `OBSERVATION_PERIOD` is derived from event dates.

## 4. The Evaluation Phase (Quality)

Validation is critical. "It runs"!= "It is correct."

- **Tool:** **Data Quality Dashboard (DQD)**.
- **The Kahn Framework:**
    1. **Conformance:** Does it match the schema? (Data types, FKs).
    2. **Completeness:** Is data missing? (Null columns).
    3. **Plausibility:** Does it make sense? (e.g., "Male patient with Pregnancy diagnosis").
- **Tool:** **Achilles**. Generates aggregate characterization (The "Health Check" of the DB).

## 5. Metadata & Provenance

- **Fair Principles:** Making data Findable, Accessible, Interoperable, Reusable.
- **RO-Crate:** Packaging the analysis code, metadata, and results into a standardized container for reproducible research.
