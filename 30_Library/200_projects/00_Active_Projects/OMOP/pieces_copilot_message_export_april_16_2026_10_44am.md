---
created: 2026-04-16T09:44:27+00:00
modified: 2026-04-19T18:30:38+00:00
title: pieces_copilot_message_export_april_16_2026_10_44am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Apr 16, 2026 - 10:44 AM_
---

## OMOP Data Generation Process via Omop-cli

You're correct about the high-level flow. Based on your recent work (particularly the [omop-cli implementation from March 21](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/omop/omop-cli)), here's the detailed end-to-end process as it currently stands:

---

### Phase 1: Synthea Native CSV Generation

Tool: `swpc_synthea` (UK-adapted fork of Synthea)

1. Bootstrap Infrastructure
   - The CLI downloads/verifies the Synthea JAR file
   - Generates UK-specific geography files (GB postcodes, demographics)
   - Creates SDOH (Social Determinants of Health) resources matching UK regions

2. Configure Synthea Properties

   ```
   exporter.csv.export = true
   exporter.fhir.export = false
   generate.geography.country_code = GB
   ```

3. Parallel Generation (if using `--workers N`)
   - Splits the target population across multiple JVM workers
   - Each worker gets a cryptographically distinct seed (from `os.urandom(8)`)
   - Seeds offset by prime 1,000,003 to guarantee independence
   - Output written to separate batch directories: `.omop-workdir/synthea-output/batch-0/`, `batch-1/`, etc.

4. Synthea Native Output Format
   The tool generates ~13 CSV files in Synthea's native schema:
   - `patients.csv` (demographics, NHS identifiers after post-processing)
   - `encounters.csv` (clinical visits)
   - `conditions.csv` (diagnoses - SNOMED CT codes)
   - `medications.csv` (prescriptions - dm+d codes)
   - `procedures.csv`, `observations.csv`, `immunizations.csv`
   - `allergies.csv`, `careplans.csv`, `devices.csv`
   - `claims.csv`, `payer_transitions.csv`, etc.

5. NHS Post-Processing (England mode only)
   After generation completes:
   - NHS Number Injection: `process_patients_csv()` replaces SSN with valid Modulo-11 NHS Numbers
   - Geography Relabeling: `relabel_gb_state_columns()` changes STATE from "MA" to "England"
   - These modifications happen in-place on `patients.csv`

---

### Phase 2: Validation & Quality Checks

Automated by the CLI:

- Duplicate check: Ensures all patient IDs are unique across parallel batches
- Patient count verification: Confirms alive + deceased patients sum to expected total
- FK integrity: Validates that all clinical tables reference valid patient UUIDs

Output Example (from your March 21 test):

```
Total rows: 1,193
Unique patients: 1,193
✓ 0 duplicates found
✓ All 1,193 patients have conditions, encounters, observations
```

---

### Phase 3: OMOP ETL (Harmonization)

Tool: ETLSyntheaBuilder R package (from OHDSI)

This is the critical transformation step that maps Synthea's native CSV schema → OMOP CDM v5.4 tables.

#### 3.1 Prerequisites (Handled by `omop etl-export`)

1. Spin up MSSQL Container

   ```bash
   docker run -d -p 1433:1433 \
     -e ACCEPT_EULA=Y -e SA_PASSWORD=... \
     mcr.microsoft.com/mssql/server:2022-latest
   ```

   - Container name: `omop-mssql-<timestamp>`
   - Creates a throwaway database just for ETL processing

2. Deploy OMOP CDM Schema
   - Runs `OMOPCDM_sql_server_5.4_ddl.sql` to create all CDM tables
   - Tables created: `PERSON`, `OBSERVATION_PERIOD`, `VISIT_OCCURRENCE`, `CONDITION_OCCURRENCE`, `DRUG_EXPOSURE`, `PROCEDURE_OCCURRENCE`, `MEASUREMENT`, `OBSERVATION`, etc.

3. Load Athena Vocabulary
   - Vocabulary files from [files/OMOP_CDM_vocab/](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/omop/omop-cli/files/OMOP_CDM_vocab/)
   - Bulk inserts: `CONCEPT`, `CONCEPT_RELATIONSHIP`, `CONCEPT_ANCESTOR`, `VOCABULARY`, `DOMAIN`, `CONCEPT_CLASS`
   - Critical for mapping: SNOMED CT → `concept_id`, dm+d → RxNorm equivalents

#### 3.2 The ETL Mapping Process

Script: [r/run_etl_synthea.R](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/omop/r/run_etl_synthea.R)

The R script uses `ETLSyntheaBuilder::CreateEventTables()` which:

1. Reads Synthea CSVs
   - Loads all 13 CSV files into memory
   - Parses dates, SNOMED codes, dm+d medication codes, etc.

2. Maps to OMOP Concepts
   For example:
   - Synthea `conditions.csv` CODE (SNOMED) → OMOP `CONDITION_OCCURRENCE.condition_concept_id`
   - Synthea `medications.csv` CODE (dm+d) → OMOP `DRUG_EXPOSURE.drug_concept_id`
   - Lookup via `CONCEPT` and `CONCEPT_RELATIONSHIP` vocabulary tables

3. Generates OMOP Event Tables
   - `PERSON` (from `patients.csv`): NHS Number → `person_source_value`
   - `OBSERVATION_PERIOD`: Calculates continuous observation windows per patient
   - `VISIT_OCCURRENCE`: Maps Synthea encounters to OMOP visit types
   - `CONDITION_OCCURRENCE`: All diagnoses with start/end dates
   - `DRUG_EXPOSURE`: Medication prescriptions with quantities and days supply
   - `PROCEDURE_OCCURRENCE`: Clinical procedures (e.g., immunizations, surgeries)
   - `MEASUREMENT`: Lab results, vital signs (height, weight, BP, etc.)
   - `OBSERVATION`: Pain scores, social history, etc.

4. Writes Back to MSSQL
   - Bulk inserts into the temporary OMOP CDM database
   - All 1,193 patients from your test yielded ~12 billion clinical rows at 12M patient scale

#### 3.3 Timing Breakdown (from April 3, 2026)

Based on your documented phase timing:

- `mssql_container`: 28.4s (2%)
- `ddl_and_optional_reset`: 4.8s (0%)
- `etl_r_maps_and_load_event_tables`: ~18.5 min (83%) ← The harmonization step
- `archive`: ~2m 48s (13%)

The R ETL is the computational bottleneck—your 1,000-patient test took ~18 minutes.

---

### Phase 4: Export & Distribution

Current Capabilities:

1. CSV Archive (via `--archive` flag, default enabled)
   - Exports all OMOP CDM tables from MSSQL → CSV files
   - Compresses into `.tar.gz` archive
   - Output location: `.omop-workdir/synthea-output/omop_cdm_<timestamp>.tar.gz`
   - For rapid validation: Use `--no-archive` to skip this step

2. Azure Blob Upload (via `omop upload`)
   - Pushes the archive to blob storage (e.g., `omop-synthetic-data` container)
   - Makes data accessible to staging/testing environments
   - Supports versioning for reproducibility

3. Direct Database Seeding (planned, per FTFL-475 ticket)
   - Load CSVs directly into PostgreSQL or fresh MSSQL instance
   - Reapply against existing database (truncate + reload)
   - Supports "multi-silo" scenarios where different NHS trusts hold different subsets

---

### The Commands You Actually Run

Based on your [omop-cli implementation](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/omop/omop-cli/src/omop_cli/commands/):

#### Standard Workflow:

```bash
# 1. Generate 1,000 patients with 4 parallel workers
uv run omop generate --population 1000 --workers 4

# 2. Run ETL to convert Synthea CSV → OMOP CDM (includes MSSQL container + R script)
uv run omop etl-export --archive

# 3. Upload to Azure Blob
uv run omop upload --container omop-synthetic-data
```

#### For 12 Million Patients (per Your April work)

```bash
# Distributed generation across Azure Batch workers
uv run omop generate --population 12000000 --workers 64 --jvm-heap 16G

# ETL would be parallelized across multiple R sessions (work in progress)
```

---

### Key Technical Details from Your Implementation

#### NHS-Specific Customizations:

- NHS Number Generation: Modulo-11 algorithm with check digit validation ([services/nhs_post_process.py](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/omop/omop-cli/src/omop_cli/services/nhs_post_process.py))
- UK Geography: Suffolk county demographics, English postcodes (not US Zip codes)
- Vocabularies: SNOMED CT (not ICD-10), dm+d (not NDC drug codes)

#### Data Quality Guarantees:

From your March 21 validation:

> "Codes are SNOMED CT (410620009 = well child visit, 314529007 = medication review due) - standard for OMOP ETL. The data is coherent end-to-end: NHS number links the patient, all encounters/conditions/observations reference the same patient UUID."

#### Known Cosmetic Issues:

- `location.state` may still show "MA" in some records—this is an ETLSyntheaBuilder limitation, not a data integrity problem
- Does not affect OMOP query logic (no code keys off `location.state`)

---

### Next Steps (from FTFL-475 ticket)

You're currently working on:

1. Decoupling database technology: Generate once, seed into PostgreSQL or MSSQL
2. Sub-cohort injection: Ensuring specific clinical profiles (e.g., diabetic patients) via Synthea disease modules
3. Concept distribution statistics: DISTINCT counts per vocabulary in each OMOP table
4. Controlled patient overlap: Providing a list of `person_source_value` identifiers to link across datasets

---

Does this match your understanding of the current pipeline? Are you looking for specific details on any phase (e.g., the R ETL logic, or the parallel generation coordination)?
