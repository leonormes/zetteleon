---
aliases: ["Data Quality Dashboard", "DQD", "OMOP ETL", "Rabbit-in-a-Hat"]
created: 2026-01-06T19:27:38+00:00
last_reviewed: 
modified: 2026-02-01T15:07:54+00:00
status: "Active"
tags: ["data-quality", "etl", "ohdsi", "process"]
title: SoT - OHDSI ETL & Data Quality
type: "SoT"
updated: 
---

## SoT - OHDSI ETL & Data Quality

> The ETL Lifecycle: Design -> Map -> Implement -> Evaluate. This is not a one-time script, but a maintained software pipeline.

### 1. The Design Phase (Profiling)

Before mapping, you must understand the "shape" of the source.

- Tool: WhiteRabbit.
- Action: Scans the source database to generate frequency distributions of every column.
- Output: A Scan Report. This tells you that "Gender" contains `M`, `F`, and `NULL`.

### 2. The Mapping Phase (Logic)

Defining the translation rules without writing code.

- Tool: Rabbit-in-a-Hat.
- Action: Visual interface to draw lines from Source Tables to CDM Tables.
- Output: A Design Document (Spec).
- Tool: Usagi.
- Action: Maps source codes (local dictionaries) to Standard Concepts.

### 3. The Implementation Phase (Build)

Translating the spec into executable code.

- Legacy: Custom SQL scripts.
- Modern: dbt or SQLMesh frameworks.
- Logic:
    - Themis Conventions: Binding rules for ambiguity (e.g., "Drop patients with no birth year").
    - Dependency: Build `PERSON` first; `OBSERVATION_PERIOD` is derived from event dates.

### 4. The Evaluation Phase (Quality)

Validation is critical. "It runs"!= "It is correct."

- Tool: Data Quality Dashboard (DQD).
- The Kahn Framework:
    1. Conformance: Does it match the schema? (Data types, FKs).
    2. Completeness: Is data missing? (Null columns).
    3. Plausibility: Does it make sense? (e.g., "Male patient with Pregnancy diagnosis").
- Tool: Achilles. Generates aggregate characterization (The "Health Check" of the DB).

### 5. Metadata & Provenance

- Fair Principles: Making data Findable, Accessible, Interoperable, Reusable.
- RO-Crate: Packaging the analysis code, metadata, and results into a standardized container for reproducible research.
