---
aliases: ["Observational Health Data MOC", "OHDSI MOC", "OMOP Architecture MOC"]
confidence: "High"
created: 2026-01-06T19:25:32+00:00
epistemic: "Index"
last_reviewed: 
modified: 2026-01-08T15:03:29+00:00
purpose: "To map the OHDSI/OMOP ecosystem, focusing on the architectural constraints of read-only implementations and the convergence with FHIR."
review_interval: "Quarterly"
see_also:
  - "[[SoT - Data-Centric Software Engineering]]"
  - "[[SoT - Systems Thinking]]"
source_of_truth: []
status: "Active"
tags: ["health-informatics", "moc", "ohdsi", "omop", "SoftwareEngineering/Architecture"]
title: MOC - OHDSI & OMOP Architecture
type: "MoC"
uid: 
updated: 
---

## MoC - OHDSI & OMOP Architecture

> **The Mission:** "To improve health by empowering a community to collaboratively generate the evidence that promotes better health decisions and better care."

### 1. Core Standards (The Schema)

The foundation of the ecosystem is the standardization of structure (CDM) and content (Vocabulary).

- **[[SoT - OMOP Common Data Model (CDM)]]:** The person-centric schema optimized for analytics (OLAP) rather than transactions.
- **[[SoT - OHDSI Standardized Vocabularies]]:** The semantic layer (SNOMED, RxNorm) and the "Dual-Coding" system (Source vs. Standard).
- **[[SoT - OHDSI ETL & Data Quality]]:** The design (Rabbit-in-a-Hat), implementation, and validation (Data Quality Dashboard) lifecycle.

### 2. The Toolstack (The Engine)

The software architecture that drives evidence generation.

- **[[SoT - OHDSI Toolstack & Atlas]]:** The standard stack (Atlas, WebAPI, Circe, SqlRender) and its "Write-to-Read" design pattern.
- **[[SoT - ARACHNE]]:** The distributed execution engine for federated network studies.

### 3. Custom Implementation Architectures

Patterns for implementing OHDSI in constrained or modern environments.

- **[[SoT - OHDSI Read-Only Architecture]]:** **(Critical)** How to query OMOP without write permissions using "Transient CTEs" and a "Definition Store."
- **[[SoT - OHDSI and FHIR Convergence]]:** The bridge between clinical exchange (FHIR/OLTP) and population analytics (OMOP/OLAP).

### 4. Evidence Generation

The scientific output of the system.

- **[[SoT - OHDSI Evidence Generation]]:** The three pillars: Characterization, Population-Level Estimation, and Patient-Level Prediction.
- **[[SoT - Best Practices for Real-World Analysis]]:** Preventing p-hacking via transparency and pre-specification.

### 5. 2025 Strategic Context

- **Stability:** The CDM schema remains stable to support global scale.
- **Execution Gap:** The focus has shifted from "Innovation" to "Operational Capacity" (running studies at scale).
