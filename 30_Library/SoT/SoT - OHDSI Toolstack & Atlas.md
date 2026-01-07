---
aliases: ["OHDSI Stack", "Atlas", "WebAPI", "HADES"]
confidence: "High"
created: 2026-01-06
epistemic: "Technical"
last_reviewed: 
modified: 
purpose: "To define the standard software architecture of the OHDSI ecosystem, specifically the 'Write-to-Read' pattern of Atlas and WebAPI."
review_interval: "1 year"
see_also: 
  - "[[SoT - OHDSI Read-Only Architecture]]"
  - "[[SoT - OMOP Common Data Model (CDM)]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "software", "atlas", "SoftwareEngineering/Architecture"]
title: SoT - OHDSI Toolstack & Atlas
type: "SoT"
uid: 
updated: 
---

# SoT - OHDSI Toolstack & Atlas

> **The Standard Architecture:** A "Write-to-Read" pattern where analysis definitions (JSON) are compiled into SQL that **materializes results** into scratchpad tables.

## 1. The Core Components

### A. ATLAS (The Frontend)
*   **Role:** The GUI for designing cohorts and analyses.
*   **Data Model:** Reactive JavaScript objects (`CohortExpression`).
*   **Output:** Serializes logic into **Circe-compliant JSON**.

### B. WebAPI (The Service Layer)
*   **Role:** The REST API that manages state and orchestration.
*   **Function:** Receives JSON from Atlas, calls the library layer to generate SQL, and executes it against the CDM.
*   **Dependency:** Requires a writeable `OHDSI` schema to store definitions and a `RESULTS` schema to store cohort tables.

### C. The Library Layer (Java/R)
1.  **Circe:** The Compiler.
    *   *Input:* JSON Cohort Definition.
    *   *Output:* Abstract OHDSI-SQL (Standard Dialect).
    *   *Logic:* Template-based injection (`conceptSetQuery.sql`, `conditionOccurrence.sql`).
2.  **SqlRender:** The Transpiler.
    *   *Input:* OHDSI-SQL.
    *   *Output:* Dialect-specific SQL (Postgres, Oracle, Redshift).
    *   *Mechanism:* Token replacement (`@cdm_schema` -> `public`).

## 2. The Execution Pattern ("Write-to-Read")

Standard OHDSI tools assume a **Stateful Execution Model**.

1.  **Definition:** User clicks "Generate".
2.  **Compilation:** Logic is converted to `INSERT INTO #cohort SELECT ...`.
3.  **Materialization:** The database engine executes the query and writes the result (Subject ID, Date) to the `COHORT` table.
4.  **Analysis:** Downstream tools (HADES, R packages) query the `COHORT` table directly.

**Constraint Implication:** This architecture **fails** in read-only environments. See [[SoT - OHDSI Read-Only Architecture]] for the solution.

## 3. HADES (Analytics)
**Health Analytics Data-to-Evidence Suite.** A library of R packages for advanced analytics.
*   **CohortMethod:** Population-level estimation.
*   **PatientLevelPrediction (PLP):** Machine learning.
*   **DataQualityDashboard:** Validation.

## 4. Architectural Data Flow

`User (Atlas) -> JSON -> WebAPI -> Circe (Compile) -> SqlRender (Transpile) -> JDBC -> DBMS`
