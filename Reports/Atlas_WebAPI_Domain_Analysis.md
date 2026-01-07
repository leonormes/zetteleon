---
aliases: []
tags: []
title: "Domain Analysis: OHDSI Atlas & WebAPI"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-07T10:38:15+00:00
modified: 2026-01-07T11:05:26+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Domain Analysis: OHDSI Atlas & WebAPI

## 1. Executive Summary

This document provides a Domain-Driven Design (DDD) analysis of the OHDSI ecosystem, specifically focusing on the relationship between **Atlas** (Frontend/Bounded Context Consumer) and **WebAPI** (Backend/Domain Layer).

The system is architected around the core concept of **Cohort Definitions**—computable phenotypes—which serve as the Foundational Aggregate for all downstream analytics (Characterization, Estimation, Prediction).

## 2. Ubiquitous Language

The following terms constitute the **Ubiquitous Language** shared between the Code (Entities), the UI (Atlas), and the Domain Experts (Researchers).

### Core Entities

| Term | Definition | Key Code Artifacts |
|:--- |:--- |:--- |
| **Cohort Definition** | The specification of criteria (rules) that define a group of persons for a specific duration. This is the **Aggregate Root**. | `CohortDefinition.java` (WebAPI)<br>`CohortDefinition.js` (Atlas) |
| **Cohort** | The *instantiated* result of applied criteria. A list of subjects with start/end dates. | `Cohort` (SQL Table)<br>`CohortGenerationInfo` |
| **Source** | A specific database instance conforming to the OMOP Common Data Model (CDM) against which definitions are executed. | `Source` entity<br>`source_id` |
| **Concept Set** | A collection of standard terminological concepts (SNOMED, RxNorm, etc.) used as building blocks for criteria. | `ConceptSet.js`<br>`CommonConceptSetEntity` |
| **Generation** | The asynchronous *process* of executing a Definition against a Source to materialize a Cohort. | `Job` (Batched execution)<br>`GenerationStatus` |
| **Expression** | The JSON-serialized representation of the Cohort rules. This acts as the "Code as Data" for the phenotype. | `expression` (Field)<br>`CohortExpression` |

### Analytic Contexts

| Term | Definition |
|:--- |:--- |
| **Characterization** | Descriptive statistics (demographics, conditions, drugs) describing a Cohort. |
| **Pathway** | Analysis of the temporal sequence of events (e.g., lines of therapy) within a Cohort. |
| **Estimation** | *Population Level Estimation*. Comparative effectiveness research (Cohort Method, Self-Controlled Case Series). |
| **Prediction** | *Patient Level Prediction*. Machine learning models to predict outcomes within a Cohort. |
| **Incidence Rate** | Analysis of the rate at which an outcome occurs within a target population. |

## 3. Domain Model & Bounded Contexts

The system is clearly divided into several **Bounded Contexts**.

### 3.1. Cohort Definition Context (Core Domain)

This is the heart of the system.

- **Aggregate Root:** `CohortDefinition`
- **Entities:** `CohortDefinitionDetails` (holds the Expression), `CohortGenerationInfo` (State).
- **Value Objects:** `Expression` (The logic), `ConceptSet`.
- **Invariants:** A Definition must have a valid Expression. A Name must be unique.

### 3.2. Vocabulary Context (Supporting Domain)

Handles the complex medical terminology.

- **Entities:** `Concept`, `Vocabulary`, `Domain`.
- **Role:** Provides the "Language" (`ConceptIds`) used inside the `Expression`.

### 3.3. Execution Context (Generic Subdomain)

Handles the asynchronous running of jobs.

- **Entities:** `Job`, `JobExecutionInfo`.
- **Role:** decoupling the "Definition" from the "Result". The UI polls this context for status.

### 3.4. Analytic Subdomains

Each of these consumes `Cohort Definitions` to produce specific scientific outputs.

- **Characterization Context**
- **Estimation Context**
- **Prediction Context**

## 4. Architecture: Atlas vs. WebAPI

- **WebAPI (The Domain Layer):** Enforces the invariants. Encapsulates the OHDSI standard libraries (Circe for cohorts, SqlRender for translation). It exposes the Domain Model via a RESTful API.
- **Atlas (The Presentation Layer):** A "Smart Client" that speaks the Ubiquitous Language. It constructs the `Expression` object (via a UI builder) and sends it to the generic `CohortDefinition` aggregate in WebAPI.

## 5. Domain Model Diagram

```d2
# Core Aggregate
CohortDefinition: {
  "+Integer id"
  "+String name"
  "+String description"
  "+ExpressionType type"
  "+generate(Source)"
}

CohortDefinitionDetails: {
  "+String rules_json"
  "+getExpression()"
}

CohortGenerationInfo: {
  "+Integer source_id"
  "+GenerationStatus status"
  "+Date startTime"
  "+Long personCount"
}

Source: {
  "+String sourceKey"
  "+String sourceName"
  "+String cdmJdbcUrl"
}

# Relationships
CohortDefinition -- CohortDefinitionDetails: contains
CohortDefinition -- CohortGenerationInfo: tracks status for
CohortGenerationInfo -> Source: executes on

# Analytic Consumers
CohortCharacterization: {
  "+String name"
  "+List<CohortDefinition> cohorts"
}

PathwayAnalysis: {
  "+String name"
  "+List<CohortDefinition> targetCohorts"
  "+List<CohortDefinition> eventCohorts"
}

CohortCharacterization -> CohortDefinition: analyzes
PathwayAnalysis -> CohortDefinition: uses
```

### Key Insight: The "Expression" Pattern

The system relies heavily on the **Specification Pattern**. The `CohortDefinition` doesn't contain hardcoded logic; it contains a serialized `Expression` (the Specification) which is interpreted by the engine (Circe/SqlRender) to generate SQL. This allows the Domain Logic to be dynamic and user-defined.
