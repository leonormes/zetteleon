---
created: 2026-04-15T08:14:01+00:00
modified: 2026-04-16T11:56:03+00:00
title: Creating Realistic OMOP Synthetic Data
---

## Presentation Script: Creating Realistic OMOP Synthetic Data

Based on your work on FTFL-475/476 and the pipeline you've been building, here's a presentation script for your team. I've structured it with slides and speaker notes.

---

### Slide 1: Title

"Generating Realistic Healthcare Data at Scale"

_Synthetic OMOP CDM Data Generation Pipeline_

Speaker Notes:

> "Today I'm going to walk you through how we generate realistic synthetic healthcare data that conforms to the OMOP Common Data Model. I'll explain why we need this, what's involved in creating it, and how we scale it up to millions of patient records."

---

### Slide 2: Why Synthetic Data?

The Problem:

- We can't use real patient data for development and testing (GDPR, patient privacy)
- We need data that _behaves_ like real clinical data
- We need _millions_ of records to test performance at production scale

Speaker Notes:

> "Real healthcare data is incredibly sensitive—we simply cannot use it outside of tightly controlled production environments. But our pipelines, dashboards, and analytics need to be tested against realistic data. That means we need synthetic data that looks and behaves like the real thing—same coding systems, same data relationships, same volumes."

---

### Slide 3: What is OMOP CDM?

OMOP = Observational Medical Outcomes Partnership

CDM = Common Data Model

A standardised schema for healthcare data used globally for research and analytics.

| Table | What It Holds |
|-------|---------------|
| `person` | Demographics (birth year, gender, ethnicity) |
| `condition_occurrence` | Diagnoses (ICD-10, SNOMED codes) |
| `drug_exposure` | Medications prescribed/dispensed |
| `procedure_occurrence` | Clinical procedures performed |
| `measurement` | Lab results, vital signs (LOINC codes) |
| `observation` | Other clinical observations |
| `visit_occurrence` | Hospital visits, GP appointments |

Speaker Notes:

> "OMOP CDM is an international standard for structuring healthcare data. It maps everything—diagnoses, medications, procedures, lab results—into a consistent format using standard vocabularies like SNOMED, ICD-10, and LOINC. This means data from different hospitals or countries can be analysed together. Our synthetic data needs to conform to this exact structure."

---

### Slide 4: The Generation Pipeline—Overview

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Synthea   │ ──▶ │  Staging DB     │ ──▶ │   R ETL      │ ──▶ │  OMOP CDM   │
│  (Patient   │     │  (MSSQL with    │     │  (ETLSynthea │     │  (Final     │
│  Generator) │     │  raw records)   │     │   Builder)   │     │  output)    │
└─────────────┘     └─────────────────┘     └──────────────┘     └─────────────┘
```

Speaker Notes:

> "The pipeline has four main stages. First, we generate synthetic patients using a tool called Synthea. Then we load that data into a staging database. Next, we run an ETL process written in R that transforms the data into OMOP format, applying the correct vocabularies and coding systems. Finally, we export the OMOP CDM tables as our output."

---

### Slide 5: Stage 1—Synthea (Patient Generation)

What is Synthea?

- Open-source synthetic patient generator (developed by MITRE)
- Simulates realistic patient life histories
- Models disease progression, treatments, outcomes

What it produces:

- Demographics, conditions, allergies, medications
- Clinical encounters, procedures, observations
- Realistic timelines (patient born → conditions develop → treatments given)

Speaker Notes:

> "Synthea is the gold standard for synthetic healthcare data. It doesn't just generate random records—it actually _simulates_ patient lives. A patient might be born, develop diabetes at 45, get prescribed metformin, have regular A1C tests, and so on. The clinical pathways are based on real medical literature and statistics. This is what makes the data realistic—it has internal consistency and clinically plausible patterns."

---

### Slide 6: Stage 2—Staging Database

Why a staging database?

- Synthea outputs CSV/FHIR files
- ETL tool expects data in SQL tables
- We use MSSQL as the intermediate staging area

What happens:

1. Synthea CSVs are loaded into MSSQL tables
2. Tables mirror Synthea's native schema
3. Provides a stable input for the ETL process

Speaker Notes:

> "Synthea produces its data in a specific format—CSV files or FHIR bundles. But the ETL tool we use expects the data to be in SQL Server tables. So we spin up a temporary MSSQL database, load the Synthea output into it, and use that as the staging area. This is all automated within our worker containers."

---

### Slide 7: Stage 3—ETL Transformation (ETLSyntheaBuilder)

The Core Transformation:

- Maps Synthea's native codes → OMOP standard concepts
- Applies vocabulary mappings (SNOMED, ICD-10, LOINC, RxNorm)
- Builds relationships between tables (foreign keys)
- Calculates derived fields (age at event, time deltas)

The Vocabulary Challenge:

- OMOP vocabularies are ~3.6 GB of reference data
- Every code in the output must map to a valid concept
- We pre-package a "golden" vocabulary archive

Speaker Notes:

> "This is where the magic happens. The R package ETLSyntheaBuilder takes the raw Synthea data and transforms it into proper OMOP format. It maps every condition, every medication, every lab test to the correct OMOP concept IDs using standardised vocabularies. These vocabularies are huge—about 3.6 gigabytes of reference data. We pre-package them into what we call a 'golden' archive so every worker uses the same consistent vocabulary set."

---

### Slide 8: Stage 4—OMOP CDM Output

Final Output:

- Full set of OMOP CDM v5.4 tables
- Exported as CSV, Parquet, or loaded directly to target database
- Ready for analytics, testing, or loading into production-like environments

Data Quality:

- Referential integrity between tables
- Valid concept codes throughout
- Realistic distributions and patterns

Speaker Notes:

> "The end result is a complete OMOP dataset—all the tables populated with realistic, internally consistent data. Every patient has valid encounters, every diagnosis links to the right visit, every medication ties back to a condition. This is what we use to test our pipelines, benchmark our analytics, and validate our data processing logic."

---

### Slide 9: Scaling Up—The Distributed Architecture

The Challenge:

- Generating 12 million patients on one machine takes _days_
- We need parallel processing across many workers

The Solution: Azure Batch

```
                    ┌─────────────────┐
                    │  Orchestrator   │
                    │  (submits jobs) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Worker 0    │    │   Worker 1    │    │   Worker N    │
│  100K patients│    │  100K patients│    │  100K patients│
│  ID offset: 0 │    │  ID offset: 1B│    │  ID offset: NB│
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│              Azure Blob Storage (outputs)               │
│   batch-0/cdm.tar.gz  batch-1/cdm.tar.gz  ...          │
└─────────────────────────────────────────────────────────┘
```

Speaker Notes:

> "To generate millions of patients in reasonable time, we parallelise the work across many Azure Batch workers. Each worker generates a chunk—say, 100,000 patients. The critical trick is the ID offset rule: Worker 0 starts its patient IDs at 0, Worker 1 starts at 1 billion, Worker 2 at 2 billion, and so on. This means when we combine all the outputs, there are no ID collisions. Each worker uploads its output to Azure Blob Storage, and a final step combines them."

---

### Slide 10: The ID Offset Rule (Critical for Merging)

Why It Matters:

- Every OMOP table uses integer primary keys (`person_id`, `visit_occurrence_id`, etc.)
- If two workers both generate `person_id = 1`, we can't merge them

The Rule:

```
Worker 0: person_id starts at 0
Worker 1: person_id starts at 1,000,000,000
Worker 2: person_id starts at 2,000,000,000
...
```

Applied to all ID columns:

- `person_id`, `visit_occurrence_id`, `condition_occurrence_id`, etc.
- Maintains foreign key relationships within each batch

Speaker Notes:

> "This is the most important technical detail for distributed generation. Every table in OMOP uses integer IDs. If Worker 0 and Worker 1 both create a patient with ID 1, we can't merge those files—we'd have duplicate keys. So we give each worker a billion-wide ID space. Worker 0 uses IDs 0 to 999,999,999. Worker 1 uses 1 billion to 1.99 billion. This way, we can simply concatenate all the output files and the IDs never collide."

---

### Slide 11: What Each Worker Does

Worker Startup:

1. Download code package from Azure Blob Storage
2. Download vocabulary archive ("golden" vocabularies)
3. Extract and set up environment

Worker Execution:

1. Run Synthea → generate N patients
2. Load into MSSQL container (staging)
3. Run ETLSyntheaBuilder (R transformation)
4. Export OMOP CDM tables
5. Apply ID offset to all records
6. Package as `.tar.gz` and upload to Blob Storage

Speaker Notes:

> "Each worker is self-contained. It downloads everything it needs—the code, the vocabulary files—then runs the full pipeline independently. At the end, it uploads a tarball containing all the OMOP tables for its batch. The orchestrator doesn't need to track individual workers—they're fire-and-forget. If one fails, we just resubmit that batch."

---

### Slide 12: Final Assembly (Fan-In)

After Workers Complete:

1. Download all `batch-N/cdm-batch-N.tar.gz` files
2. Extract tables from each batch
3. Concatenate matching tables (`person` + `person` + …)
4. Load into target database or package as final dataset

Result:

- Single unified OMOP CDM dataset
- 12 million patients with full clinical records
- Ready for downstream consumption

Speaker Notes:

> "Once all workers finish, a final consolidation step pulls down all the output files and merges them. Because we used ID offsets, this is just file concatenation—no complex deduplication. The result is a single, massive OMOP dataset ready to load into a test database or ship to wherever it's needed."

---

### Slide 13: Summary

| Phase | What Happens |
|-------|--------------|
| Preparation | Package vocabularies as "golden" archive |
| Fan-Out | Submit N worker tasks to Azure Batch |
| Worker Execution | Each worker: Synthea → MSSQL → R ETL → OMOP output |
| Fan-In | Download and merge all batch outputs |

Key Principles:

- ID offsets prevent collisions
- Workers are stateless and independent
- Vocabularies are pre-packaged for consistency
- Output is standard OMOP CDM v5.4

Speaker Notes:

> "To summarise: we prepare a consistent vocabulary package, fan out the work across many parallel workers, each worker runs the full Synthea-to-OMOP pipeline independently, and finally we merge everything back together. The result is production-scale realistic healthcare data that we can use for testing, benchmarking, and development—without ever touching real patient information."

---

### Slide 14: Questions?

Useful References:

- [OMOP CDM Documentation](https://ohdsi.github.io/CommonDataModel/)
- [Synthea GitHub](https://github.com/synthetichealth/synthea)
- [ETLSyntheaBuilder](https://github.com/OHDSI/ETL-Synthea)
- FTFL-475: Our internal implementation ticket

---

### Presenter Notes—Anticipated Questions

Q: Why not just use pre-generated datasets?

> "Pre-generated datasets exist, but we need control over vocabularies, patient counts, and the ability to regenerate on demand. We also need specific characteristics that match our production data profiles."

Q: How long does it take?

> "With 10-20 parallel workers, we can generate about 1 million patients in a few hours. Scaling to 12 million depends on Azure quota availability."

Q: Why MSSQL? Can we use something lighter?

> "The R ETL package was designed for SQL Server—it's a dependency we inherit. There are alternative approaches using DuckDB that we're exploring to eliminate this requirement."

Q: What about The Hyve?

> "The Hyve are OMOP specialists—we've reached out to understand if there are better approaches or if they could assist directly with large-scale generation."

---

Would you like me to adjust the technical depth, add more diagrams, or expand any particular section?
