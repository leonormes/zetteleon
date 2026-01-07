---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/e71ae6e8e846"
author:
  - "[[Gemini]]"
published:
created: 2026-01-07
description: "Created with Gemini"
tags:
  - "input"
---
**OHDSI/Circe** is archived because it is a legacy repository that has been superseded by the modern OHDSI technology stack, specifically **ATLAS** and **WebAPI**.

Here is the breakdown of the relationship between the repositories and the architecture:

### 1\. Why OHDSI/Circe is archived

- **Obsolete UI:** The `OHDSI/Circe` repository contained a standalone, Knockout.js-based user interface for creating cohort definitions.
- **Superseded by ATLAS:** This UI functionality was integrated into **ATLAS**, the primary unified interface for the OHDSI platform. ATLAS uses the same underlying technology (Knockout.js) but centralises cohort definitions, data characterisation, and pathway analysis into one tool.
- **Repo Cleanup:** Although the move to ATLAS happened years ago (circa 2015–2016), the `OHDSI/Circe` repository was officially archived on **September 3, 2024**, likely as part of a housekeeping effort to mark it clearly as read-only and deprecated.

### 2\. Is OHDSI/circe-be related?

**Yes, it is the core engine.**

- **Backend Logic:**`circe-be` stands for **Circe Backend**. It is the active Java library that defines the object model for cohorts and compiles the JSON definitions (created in the UI) into the standard SQL required to query the OMOP Common Data Model.
- **Current Architecture:**
	- **Frontend:** Users build cohorts in **ATLAS** (which replaced the old `Circe` repo's UI).
	- **Middle/Backend:** ATLAS sends a JSON object to **WebAPI**.
	- **Library:** WebAPI calls **circe-be** to translate that JSON into executable SQL.

### Summary

| Repository | Status | Role |
| --- | --- | --- |
| **OHDSI/Circe** | 🔴 **Archived** | Old/Legacy standalone UI for cohort definitions. Replaced by ATLAS. |
| **OHDSI/circe-be** | 🟢 **Active** | The Java library ("Backend") that actually compiles cohort logic into SQL. Used by ATLAS and R packages (`CirceR`). |

This is the api docs for webapi. Can you retrieve the full definition of the openAPI? http://webapidoc.ohdsi.org/#home

Based on an analysis of the provided URL and the OHDSI WebAPI source code, **it is not possible to retrieve a machine-readable OpenAPI (Swagger) definition** (such as a `swagger.json` or `openapi.yaml` file) from that location.

Here is the technical explanation for why:

1. **Documentation Tool:** The OHDSI WebAPI uses **Miredot** (specifically the `miredot-plugin`) to generate its documentation, not Swagger or OpenAPI. This is confirmed by the `pom.xml` configuration in the WebAPI repository (specifically the `<miredot.phase>` tag).
2. **Format:** Miredot generates static HTML documentation directly from Java source code and annotations. Unlike Swagger/OpenAPI, which creates a schema file that fuels a UI, Miredot produces the HTML view directly.
3. **No Endpoint:** Because the application is not configured with the `springfox` or `springdoc` libraries (standard tools for exposing OpenAPI specs in Java Spring apps), there is no `/v2/api-docs` or `/swagger.json` endpoint available on the server.

### Available "Definition"

While a raw JSON spec is unavailable, the **endpoints** exposed by the API (based on your provided URL) include the following primary resources:

- **Authentication & Config:**`/info`, `/user`, `/role`, `/permission`
- **Vocabulary & Concepts:**`/vocabulary`, `/conceptset`
- **Cohort Definition:**`/cohortdefinition`, `/cohort`, `/cohortresults`
- **Analysis:**`/cohort-characterization`, `/pathway-analysis`, `/feature-analysis`
- **Evidence & Feasibility:**`/evidence`, `/feasibility`, `/ir` (Incidence Rate)
- **CDM:**`/cdmresults` (Common Data Model statistics)

If you need to generate a client or inspect the contract programmatically, you would currently have to manually map these endpoints or scrape the Miredot HTML, as no official OpenAPI spec is published.

here is the github org for all the ohdsi tools. Create me a list with a description of what each is in markdown

https://github.com/orgs/OHDSI/repositories?type=all

To provide a "software architect" view of the 367+ repositories in the OHDSI GitHub organization, it is best to ignore the noise (forks, student projects, deprecated experiments) and focus on the **Reference Architecture**.

The OHDSI stack is structured into distinct layers: **Standards**, **ETL/Engineering**, **Web Platform**, and **Analytics Engine (HADES)**.

### 1\. Data Standards Layer

These repositories define the schema and semantic framework upon which all other tools rely.

| Repository | Description |
| --- | --- |
| **[CommonDataModel](https://github.com/OHDSI/CommonDataModel)** | **The Kernel.** Contains the definition, DDLs (for Oracle, SQL Server, PostgreSQL, etc.), and documentation for the OMOP Common Data Model. |
| **[Vocabulary-v5.0](https://github.com/OHDSI/Vocabulary-v5.0)** | The build process for the Standardized Vocabularies. *Note: Users typically download the compiled vocabularies from [Athena](https://www.google.com/search?q=http://athena.ohdsi.org) rather than build them from this repo.* |

### 2\. ETL & Data Engineering Layer

Tools designed to profile source data, map it to the standard, and validate quality.

| Repository | Description |
| --- | --- |
| **[WhiteRabbit](https://github.com/OHDSI/WhiteRabbit)** | **Profiler.** Scans your source database (e.g., CSV, SQL) and generates a report on table structures and value frequencies. Essential for understanding source data before mapping. |
| **[RabbitInAHat](https://github.com/OHDSI/WhiteRabbit)** | **Design Tool.** A UI that consumes the scan report from WhiteRabbit and allows you to graphically draw mappings from Source tables to CDM tables. |
| **[Usagi](https://github.com/OHDSI/Usagi)** | **Semantic Mapper.** Aids in mapping source codes (e.g., local proprietary drug codes) to standard OMOP concepts using text similarity search (Lucene-based). |
| **[DataQualityDashboard](https://github.com/OHDSI/DataQualityDashboard)** | **Validator.** An R package that runs thousands of pre-configured unit tests (conformance, plausibility, completeness) against a converted CDM instance and visualises the results. |
| **[Achilles](https://github.com/OHDSI/Achilles)** | **Characteriser.** Runs SQL scripts to compute descriptive statistics (counts, distributions, treemaps) of the entire database. Output is a "Results Schema" used by ATLAS and Ares. |
| **[ETL-LambdaBuilder](https://github.com/OHDSI/ETL-LambdaBuilder)** | A.NET Core application designed to orchestrate the ETL process on AWS Lambda (Serverless). |

### 3\. The Web Platform (Application Layer)

The user-facing tools for defining cohorts and executing analyses.

| Repository | Description |
| --- | --- |
| **[Atlas](https://github.com/OHDSI/Atlas)** | **The Frontend.** A Single Page Application (SPA) facilitating the design of cohorts, characterisations, and incidence rate analyses. It serves as the primary IDE for OHDSI researchers. |
| **[WebAPI](https://github.com/OHDSI/WebAPI)** | **The Backend.** A Java (Spring Boot) RESTful service that manages the database connections, translates OHDSI JSON definitions into SQL, and handles job execution. |
| **[Ares](https://github.com/OHDSI/Ares)** | **Data Catalog.** A newer static site generator that publishes the results from Achilles/DataQualityDashboard to showcase the contents of a data network without exposing patient-level data. |

### 4\. HADES (Analytics Engine)

**H** ealth **A** nalytics **D** ata-to- **E** vidence **S** uite. This is the "Standard Library" of R packages used by the platform to perform heavy statistical lifting.

- **Drivers & Translation:**
	- **[DatabaseConnector](https://github.com/OHDSI/DatabaseConnector):** Unified JDBC wrapper for R.
	- **[SqlRender](https://github.com/OHDSI/SqlRender):** Cross-dialect SQL translation (writes in "OHDSI SQL", compiles to Oracle/Postgres/Redshift/Spark).
- **Core Analytics:**
	- **[CohortMethod](https://github.com/OHDSI/CohortMethod):** Large-scale propensity score matching and outcome estimation.
	- **[PatientLevelPrediction](https://github.com/OHDSI/PatientLevelPrediction):** Machine learning pipeline (Lasso, Gradient Boosting, Deep Learning) for predicting outcomes at the patient level.
	- **[Cyclops](https://github.com/OHDSI/Cyclops):** High-performance cyclic coordinate descent for large-scale regularised regression (C++ backed).
- **Cohort Logic:**
	- **[CirceR](https://github.com/OHDSI/CirceR):** R wrapper for the cohort logic engine (frontend for `circe-be`).
	- **[Capr](https://github.com/OHDSI/Capr):** A programmatic (code-first) way to define cohorts in R, an alternative to the ATLAS GUI.

### 5\. Infrastructure

| Repository | Description |
| --- | --- |
| **[Broadsea](https://github.com/OHDSI/Broadsea)** | **Deployment.** The official Docker container stack. It deploys the full architecture (Atlas, WebAPI, Postgres, R Methods) via Docker Compose. |

... [Developing and Evaluating Your Extract, Transform, Load (ETL) Process to the OMOP CDM](https://www.youtube.com/watch?v=H69dC7f-edQ)

This recent video from the 2024 Global Symposium details the ETL tools (WhiteRabbit, DataQualityDashboard) and how they fit into the broader OHDSI architecture for standardising data.

can you find the api docs/definition for webApi backend?

As of early 2026, **there is no official, machine-readable OpenAPI (Swagger) definition** for the OHDSI WebAPI.

The platform relies on a different documentation generation stack that does not produce standard JSON/YAML specifications.

### 1\. The Source of Truth: Miredot

Instead of Swagger, WebAPI uses **Miredot** to generate static HTML documentation directly from the Java source code (Spring annotations).

- **Documentation URL:**[http://webapidoc.ohdsi.org/](http://webapidoc.ohdsi.org/)
- **Limitation:** This provides a human-readable list of endpoints (GET/POST) and parameters, but it **cannot be imported** into tools like Postman or Swagger UI for automated client generation.

### 2\. Why it is missing (Architectural Context)

- **Legacy Stack:** WebAPI is a legacy Java 8 application built on Spring Boot 1.x (later migrated to 2.x). It pre-dates the widespread adoption of the OpenAPI V3 standard.
- **Build Pipeline:** The Maven build process (`pom.xml`) is configured to run the `miredot-plugin` during the `package` phase. There is no `springdoc` or `springfox` dependency included, which would be required to auto-generate a `/v2/api-docs` or `/swagger.json` endpoint at runtime.

### 3\. Alternative "Definitions"

If you need to understand the contract for integration purposes, these are your best proxies:

**A. The "Client" Definition (ROhdsiWebApi)** The R package `ROhdsiWebApi` acts as the de-facto client SDK. Reviewing its function definitions is often more accurate than the Miredot documentation, as it is actively maintained to support the HADES suite.

- **Repo:**[OHDSI/ROhdsiWebApi](https://github.com/OHDSI/ROhdsiWebApi)

**B. The "Server" Definition (Java Interfaces)** If you need the exact request/response bodies, you must look at the Jersey REST controllers in the source code.

- **Location:**`src/main/java/org/ohdsi/webapi/service`
- **Key Files:**
	- `CohortDefinitionService.java` (Cohort logic)
	- `VocabularyService.java` (Search & Concepts)
	- `DDLService.java` (Schema generation)

### Next Step

Would you like me to extract the JSON payload structure for a specific endpoint (e.g., `POST /cohortdefinition`) from the Java source code for you?

parse this youtube playlist and create a list of the individual videos links https://www.youtube.com/playlist?list=PLpzbqK7kvfeUXjgnpNMFoff3PDOwv61lZ

The YouTube playlist provided (**PLpzbqK7kvfeUXjgnpNMFoff3PDOwv61lZ**) contains the sessions from the **2024 OHDSI Global Symposium**. Below is a list of the primary sessions and presentations included in this collection:

### 2024 OHDSI Global Symposium Videos

- **State of the Community**
	- *Presenter:* George Hripcsak
	- *Link:*[https://www.youtube.com/watch?v=Iz-jMxrgUCM](https://www.youtube.com/watch?v=Iz-jMxrgUCM)
- **Value Proposition for Participating in OHDSI Network Studies like LEGEND-T2DM**
	- *Presenter:* Various (Introduction by Patrick Ryan)
	- *Link:*[https://www.youtube.com/watch?v=o19SSkEDKIg](https://www.youtube.com/watch?v=o19SSkEDKIg)
- **Clinical Insights from LEGEND-T2DM**
	- *Moderator:* Aline Pedroso
	- *Link:*[https://www.youtube.com/watch?v=QLyFaEuIlPc](https://www.youtube.com/watch?v=QLyFaEuIlPc)
- **2024 Global Symposium Plenary Panel: JACC-OHDSI Partnership**
	- *Moderators:* Nicole Pratt, Marc Suchard
	- *Link:*[https://www.youtube.com/watch?v=N-663a-8898](https://www.youtube.com/watch?v=N-663a-8898)
- **Closing Talk: Collaborating on Evidence at Scale**
	- *Presenter:* Patrick Ryan
	- *Link:*[https://www.youtube.com/watch?v=LZ0WaUcRQLM](https://www.youtube.com/watch?v=LZ0WaUcRQLM)

*Note: This playlist also includes a large number of lightning talks, collaborator showcases, and posters from the event. You can view the full interactive list on the [OHDSI 2024 Event Page](https://www.ohdsi.org/ohdsi2024).*

Google Account

Leon Ormes

leonormes@gmail.com