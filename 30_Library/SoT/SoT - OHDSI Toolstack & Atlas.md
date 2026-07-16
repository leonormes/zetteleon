---
aliases: [Atlas, HADES, OHDSI Stack, WebAPI]
created: 2026-01-06T19:27:09+00:00
last_reviewed: null
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-ohdsi-toolstack-atlas
status: Active
tags: [atlas, ohdsi, SoftwareEngineering, SoftwareEngineering/Architecture]
title: SoT - OHDSI Toolstack & Atlas
type: sot
updated: null
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## SoT - OHDSI Toolstack & Atlas

> The Standard Architecture: A "Write-to-Read" pattern where analysis definitions (JSON) are compiled into SQL that materializes results into scratchpad tables.

### 1. The Reference Architecture

The OHDSI stack is structured into distinct layers: Standards, ETL, Web Platform, and Analytics (HADES).

#### A. Data Standards Layer

_The schema and semantic framework._

| Repository | Description |
|:--- |:--- |
| [CommonDataModel](https://github.com/OHDSI/CommonDataModel) | The Kernel. DDLs for the OMOP CDM (Oracle, SQL Server, Postgres, etc.). |
| [Vocabulary-v5.0](https://github.com/OHDSI/Vocabulary-v5.0) | Build process for Standardized Vocabularies. (Users typically use Athena). |

#### B. ETL & Data Engineering Layer

_Tools to profile, map, and validate source data._

| Repository | Description |
|:--- |:--- |
| [WhiteRabbit](https://github.com/OHDSI/WhiteRabbit) | Profiler. Scans source DBs to report on structures and value frequencies. |
| [RabbitInAHat](https://github.com/OHDSI/WhiteRabbit) | Design Tool. Graphical UI for drawing mappings from Source to CDM. |
| [Usagi](https://github.com/OHDSI/Usagi) | Semantic Mapper. Maps source codes to OMOP concepts using text similarity. |
| [DataQualityDashboard](https://github.com/OHDSI/DataQualityDashboard) | Validator. R package running unit tests (conformance, plausibility) against the CDM. |
| [Achilles](https://github.com/OHDSI/Achilles) | Characteriser. Computes descriptive statistics (counts, treemaps) for Atlas/Ares. |

#### C. The Web Platform (Application Layer)

_User-facing tools for cohort design and analysis._

| Repository | Description |
|:--- |:--- |
| [Atlas](https://github.com/OHDSI/Atlas) | The Frontend. SPA (Knockout.js) for designing cohorts and analyses. |
| [WebAPI](https://github.com/OHDSI/WebAPI) | The Backend. Java (Spring Boot) REST service. Manages state and SQL translation. |
| [Ares](https://github.com/OHDSI/Ares) | Data Catalog. Static site generator for network data characterization. |

#### D. HADES (Analytics Engine)

_Health Analytics Data-to-Evidence Suite. The "Standard Library" of R packages._

- Drivers: `DatabaseConnector` (JDBC wrapper), `SqlRender` (Cross-dialect translation).
- Core Analytics:
    - `CohortMethod`: Propensity score matching/outcome estimation.
    - `PatientLevelPrediction`: ML pipeline (Lasso, Gradient Boosting).
    - `CirceR` / `Capr`: Programmatic cohort definition.

### 2. Component Deep Dive

#### A. The Repository Status (Circe)

There is a critical distinction between the UI and the Engine:

| Repository | Status | Role |
|:--- |:--- |:--- |
| OHDSI/Circe | 🔴 Archived | Legacy standalone UI. Replaced by ATLAS. |
| OHDSI/circe-be | 🟢 Active | The Java library ("Backend") that compiles cohort logic into SQL. |

#### B. WebAPI Documentation

WebAPI uses Miredot to generate static HTML documentation from Java source code.

- No OpenAPI: There is no machine-readable Swagger/OpenAPI definition available.
- Reference: The `ROhdsiWebApi` R package is often the most accurate "client definition" available.

#### C. The Compiler Stack

1. Circe (`circe-be`): The Compiler.
    - _Input:_ JSON Cohort Definition.
    - _Output:_ Abstract OHDSI-SQL.
2. SqlRender: The Transpiler.
    - _Input:_ OHDSI-SQL.
    - _Output:_ Dialect-specific SQL (Postgres, Oracle, Redshift).
    - _Mechanism:_ Token replacement (`@cdm_schema` -> `public`).

### 3. The Execution Pattern ("Write-to-Read")

Standard OHDSI tools assume a Stateful Execution Model.

1. Definition: User clicks "Generate" in Atlas.
2. Compilation: Logic is converted to `INSERT INTO #cohort SELECT…`.
3. Materialization: The database engine executes the query and writes the result (Subject ID, Date) to the `COHORT` table.
4. Analysis: Downstream tools query the `COHORT` table directly.

### 4. Architectural Data Flow

`User (Atlas) -> JSON -> WebAPI -> Circe-be (Compile) -> SqlRender (Transpile) -> JDBC -> DBMS`

### 5. Resources

2024 Global Symposium Highlights

- [State of the Community](https://www.youtube.com/watch?v=Iz-jMxrgUCM)
- [Value Proposition (LEGEND-T2DM)](https://www.youtube.com/watch?v=o19SSkEDKIg)
- [Clinical Insights](https://www.youtube.com/watch?v=QLyFaEuIlPc)
- [Plenary Panel](https://www.youtube.com/watch?v=N-663a-8898)
- [Collaborating on Evidence at Scale](https://www.youtube.com/watch?v=LZ0WaUcRQLM)
