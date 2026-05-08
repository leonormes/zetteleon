*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday May 8, 2026 - 10:10 AM*
---
## What your LTM says this ticket *actually is* (and why it exists)

In your Jira dashboard yesterday **(Thu May 7, 9:59 AM)** you had **FTFL-479: “Script to setup and install the OMOP data into a target database”** sitting **Selected for Dev**. Over the last ~2 weeks your LTM repeatedly ties this to the *stress testing push* and the *synthetic OMOP dataset workstream*:

- You have **5 OMOP datasets (one per node) ready for stress testing** (captured in your stress-test planning notes and reiterated in the **“HEAD - FFNode Stress Testing Meeting 2026-05-07”** note you created on **Thu May 7, 9:00 AM**).  
  - File: [HEAD FFNode Stress Testing - Meeting 2026-05-07.md](file:///Volumes/DAL/Zettelkasten/LLMeon/20_Thinking/21_Workbench/HEAD%20FFNode%20Stress%20Testing%20-%20Meeting%202026-05-07.md)

- That meeting note explicitly lists the “synthetic OMOP pipeline” tickets as a set:
  - **FTFL-475** (generate datasets)
  - **FTFL-476** (stress testing infra + monitoring)
  - **FTFL-479** (this ticket: *ingest/install into a DB*)
  - **FTFL-480** (script to create test userflows)
  - **FTFL-488** (synthetic OMOP data storage)

- In standup context this morning **(Fri May 8, ~9:07–9:22 AM)** you/others were discussing that tooling like **Achilles** may dictate the ingestion approach, and you also floated using a Hyve module (“Delphine”) as a more generic ingestion mechanism instead of bespoke scripts—i.e., this ticket is a key dependency for “run real analytics/tooling on the large datasets”, not just “have files somewhere”.

- Your repo analysis notes (from the Hermes/Claude Code run) indicate you already have an “omop-cli” style toolchain conceptually supporting:
  - generate → export CSV archive → **seed into Postgres/MSSQL** → upload/store.
  - That suggests FTFL-479 is either (a) the missing implementation of the “seed/install” step, or (b) the hardening + making-it-repeatable of something that exists but isn’t yet “team usable”.
  - Repos/paths visible in your workspace:
    - [FITFILE/Deployment](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment)
    - [FITFILE/Deployment/omop-cli](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/omop-cli)
    - [FITFILE/Deployment/omop_generator](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/omop_generator)

**So, in context:** FTFL-475 produces OMOP synthetic datasets; **FTFL-479 is the reproducible “load it into a real database” step** needed to (1) run **Achilles/Atlas-style** analytics and (2) support **repeatable stress-test runs** where DB state must be reset/seeded reliably.

---

## Copy/paste: a “real” Jira description for FTFL-479 (fits your stress testing context)

### Summary
Create a repeatable script/CLI to **provision an OMOP CDM database** (schema + constraints/indexes) and **bulk-load** OMOP synthetic data into it, supporting both **PostgreSQL and MS SQL Server**. This is required to run **Achilles/Atlas** and other database-backed tooling as part of the **FFNode / OMOP stress testing plan** (multi-node, multi-volume, repeatable runs).

### Background / Why
We are generating large synthetic OMOP datasets (incl. multi-node datasets for stress testing). File-based datasets (CSV/parquet) are not sufficient for:
- Running OHDSI tooling (e.g., **Achilles**) which expects an OMOP database
- Re-running performance tests deterministically (need “truncate + reload” capability)
- Updating vocabularies and re-seeding a shared “Atlas OMOP DB” consistently

This ticket is the “ingestion/install” step linked to:
- FTFL-475 (dataset generation)
- FTFL-476 (stress testing infra + monitoring)
- FTFL-488 (dataset storage/distribution)

### Requirements
1. **DB engines:** PostgreSQL + MS SQL Server
2. **OMOP CDM version:** Use **OMOP v5.4** DDL/constraints/index scripts from OHDSI/CommonDataModel
3. **Input:** Path to a directory of OMOP CDM CSV files *or* a compressed archive produced by our generator pipeline
4. **Modes of operation:**
   - **Fresh install:** create DB/schema + load data + apply constraints/indexes
   - **Reload/refresh:** drop constraints/indexes (as needed), truncate tables, reload, re-apply constraints/indexes
   - **Vocabulary refresh:** targeted workflow to replace vocabulary tables with a newer set (if we store vocab separately)
5. **Performance:** use bulk loading (e.g., Postgres `COPY`, MSSQL `BULK INSERT`) and correct load ordering for FK safety (or load with constraints disabled then re-enable)
6. **Docs:** README that allows any engineer to run it locally and in an environment (staging/testing) without tribal knowledge

### Non-goals (to keep it bounded)
- Not building Achilles automation here (that can be a follow-on ticket)
- Not designing the long-term “standard-agnostic patient-centric model” (separate strategic track)
- Not solving multi-node federation queries directly (this is “single DB install/seed” capability)

### Deliverables
- Script/CLI command(s) committed to the relevant repo (likely under [FITFILE/Deployment/omop-cli](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/omop-cli) or the existing synthetic data tooling location)
- Documentation + examples
- A “known-good” run output (logs + timing + row counts) for:
  - Postgres
  - MSSQL
- Optional but valuable: a small “smoke verification query set” (counts for key tables; confirm vocabulary present; confirm `person` count matches expected)

### Acceptance Criteria (Definition of Done)
- Given a CSV dataset directory (or the canonical archive format), a developer can:
  1) create/install OMOP v5.4 schema into Postgres **and** MSSQL  
  2) load all tables successfully  
  3) end with constraints/indexes applied (or a clearly documented optional step)  
- Reload mode works: it can truncate + reload without manual DB cleanup
- Documented usage in README, including required env vars/connection strings
- Produces a basic summary (row counts per table + total runtime)
- Works for “small dataset” locally and is designed to scale to “large dataset” bulk loads used in stress testing

---

## Suggested implementation shape (so the ticket is actionable)

### Proposed commands (example)
If aligned with your existing “omop-cli” concept, the interface could be:

- `omop db install --engine postgres --conn ... --cdm-version 5.4`
- `omop db load --engine postgres --conn ... --input /path/to/csvs --mode fresh|reload`
- `omop db vocab-refresh ...`
- `omop db verify ...` (row counts + a couple of sanity checks)

### Load strategy (pragmatic and stress-test friendly)
- **Phase A:** Create schema (tables)
- **Phase B:** Bulk-load data with constraints/indexes disabled or not yet applied
- **Phase C:** Apply constraints + indexes (optional toggle for stress testing, because index builds may be part of “failure point discovery”)
- **Phase D:** Output manifest: timings + row counts

This aligns with your stress testing work where known failure points include **reindex OOM** and “database cliffs”—having toggles lets you intentionally test those.

---

## Subtasks you can create under FTFL-479 (concrete breakdown)

1. **Decide canonical input format**
   - CSV directory only vs “CSV tar.gz + manifest.json”
2. **Implement Postgres loader**
   - Schema install + COPY-based load + (optional) constraints/indexes apply
3. **Implement MSSQL loader**
   - Schema install + BULK INSERT + constraints/indexes
4. **Reload workflow**
   - Drop constraints/indexes (or disable), truncate in correct order, reload, reapply
5. **Docs + examples**
6. **Smoke test harness**
   - Local docker-compose for Postgres/MSSQL (if you want it repeatable in CI)
7. **Performance telemetry**
   - Emit timings per table + total runtime (useful for stress test reporting)

---

## Key dependencies / open questions (worth adding to the ticket so it doesn’t stall)

1. **Where will the datasets live?** (FTFL-488)
   - Are we always loading from local disk, or from blob storage (download step)?
2. **Do we need this to run in CI/CD or only manually?**
3. **Which “target DB” is primary?**
   - A shared “Atlas OMOP DB” for analytics tooling, or ephemeral per-test DBs?
4. **Tooling decision:** do we implement this ourselves or adopt Hyve’s “Delphine” ingestion module?
   - If Delphine is viable, FTFL-479 can become “wrap/integrate Delphine + make it fit our archive format + docs”.

If you want, paste the above description into FTFL-479 and I’ll also propose a tight “story points justification” + a sequencing recommendation relative to **FTFL-476 stress testing** (i.e., what must be done before Phase 2 baselines can run).