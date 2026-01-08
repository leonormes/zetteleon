---
aliases: ["Ephemeral Cohort Generation", "Read-Only OMOP", "Transient CTE Pattern"]
confidence: "High"
created: 2026-01-06T19:27:24+00:00
epistemic: "Pattern"
last_reviewed: 
modified: 2026-01-08T10:49:42+00:00
purpose: "To define the architectural pattern for querying OMOP in environments where write access to the database is prohibited (blocking standard Atlas workflows)."
review_interval: "6 months"
see_also:
  - "[[SoT - OHDSI Toolstack & Atlas]]"
  - "[[SoT - OMOP Common Data Model (CDM)]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "read-only", "SoftwareEngineering/Architecture", "sql"]
title: SoT - OHDSI Read-Only Architecture
type: "SoT"
uid: 
updated: 
---

## SoT - OHDSI Read-Only Architecture

> **The Constraint:** Standard OHDSI tools require `CREATE TABLE` and `INSERT` permissions to materialize cohorts. In strict read-only environments, this workflow breaks.
> **The Solution:** Treat the database as a **Calculation Engine**, not a **Storage Engine**.

### 1. The Core Pattern: Store & Stream

Since we cannot persist the _Result_ (The Cohort Table) in the DB, we must persist the _Definition_ (The Logic) in the App and stream the result on demand.

1. **Definition Store (App DB):** A Postgres/Mongo database owned by the application stores the Circe JSON. This is the "State."
2. **Transient Execution (OMOP DB):** The JSON is transpiled into a massive, single-transaction SQL query using **Common Table Expressions (CTEs)**.

### 2. The Transpilation Strategy (Interception)

Do not use Regex to strip `CREATE TABLE` from standard OHDSI SQL (fragile). Instead, implementing a **Functional SQL Builder**.

#### The "CTE Chain" Algorithm

Transform the imperative steps of cohort generation into a declarative chain of data frames.

1. **Vocabulary CTE:** Inject Concept Sets as a `VALUES` or `UNION ALL` block.
    - _Standard:_ `INSERT INTO #Codesets...`
    - _Read-Only:_ `WITH Codesets AS (SELECT 1 as id, 1234 as concept_id...)`
2. **Primary Events CTE:** Query the domain table (`condition_occurrence`) filtering by the Vocabulary CTE.
3. **Inclusion CTEs:** Apply filters using `SEMI JOIN` or `INTERSECT`.
4. **Projection:** `SELECT count(*) FROM FinalCTE`.

### 3. Performance & Guardrails

Running complex logic without materialization is computationally expensive.

#### A. The "Count-First" Guardrail

- **UX:** Disable "Get Data" buttons initially. Only allow "Get Count."
- **Logic:** `SELECT COUNT(*)` allows the optimizer to prune joins that aren't needed for existence checks.
- **Threshold:** If Count > 50k, refuse to download the line-list.

#### B. SQL Optimization

- **Predicate Pushdown:** Ensure date filters are applied in the _innermost_ CTEs.
- **Avoid `NOT IN`:** Use `LEFT JOIN... WHERE id IS NULL` for exclusion criteria (performance killer on Redshift/Postgres).
- **Limit:** Always append `LIMIT 1000` for preview queries.

### 4. UI Implications (Dual-Coding)

The UI must handle the **Dual-Coding** system locally.

- **Search:** User types "Heart Attack."
- **Lookup:** App queries `CONCEPT` table (Read-only) to find IDs.
- **State:** App stores `[312327, 4329847]` in the JSON.
- **Execution:** App injects these IDs into the CTE.
