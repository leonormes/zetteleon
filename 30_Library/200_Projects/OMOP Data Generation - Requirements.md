---
created: 2026-04-16T00:00:00+00:00
modified: 2026-05-26T11:44:31+00:00
tags: [fitfile, omop, requirements]
tickets: [FTFL-475, FTFL-476, FTFL-479, FTFL-480, FTFL-488]
title: OMOP Data Generation - Requirements
type: project
project_category: omop
project_status: active
project_name: "OMOP"
---

## OMOP Data Generation—Project Requirements

This document consolidates requirements from FTFL-475, FTFL-479, FTFL-488, FTFL-476, and FTFL-480 into a logical delivery order: shared storage → synthetic data generation → database ingestion → additional DB setup → stress test automation.

---

### 1. Shared Storage for Vocabularies and CDM Data (FTFL-488)

A central blob storage account to hold all shared OMOP assets, accessible to both internal infrastructure and customer environments (e.g. SDE for Atlas).

#### Requirements

- Store OMOP Vocabularies downloaded from Athena
- Store Synthetic OMOP CDM data
- Design access so it works for:
  - Internal staging/testing deployments
  - Pulling vocabulary into a customer environment (e.g. SDE / Atlas instance)
- Vocabulary downloads must include a clear name and download date in the filename/path
- CDM data stored similarly (may be overwritten on refresh)
- Alongside CDM data, store the OMOP profile—either Achilles reports or a report showing distinct concept distributions across all CDM tables

---

### 2. Synthetic OMOP Data Generation (FTFL-475)

Decouple synthetic data generation from any specific output database technology so that data can be produced regularly with the latest vocabulary and stored/seeded flexibly.

#### Background

An existing script generates synthetic data against MS SQL Server. This needs to be generalised.

#### Pre-requisites

- Download the desired vocabulary from Athena before running

#### Requirements

- Docs (README.md) written so any team member can generate their own synthetic OMOP data—include a script if appropriate
- Variable cohort size—configurable as an input parameter
- Output format—CSVs stored in a compressed archive
- Vocabulary filtering—ability to limit concepts to a chosen set (e.g. ICD10, LOINC, SNOMED)
- Person identifier injection—accept a list of `person_source_value` identifiers that must appear in the output; this controls patient overlap between datasets
- Concept statistics—produce DISTINCT counts of concept columns for each CDM table to show distribution
- Sub-cohort injection _(stretch goal)_—inject sub-cohorts of interest (e.g. large diabetic population); may be too difficult to implement

#### Storage Targets (after generation)

- Blob container
- Docker container

#### Seeding Targets

- New PostgreSQL database
- New MS SQL Server database
- Re-apply against an existing PostgreSQL or MS SQL Server database

---

### 3. Database Ingestion Script (FTFL-479)

A repeatable process for inserting previously generated OMOP synthetic data into a database, and for refreshing vocabulary in an existing Atlas OMOP database.

#### Two Purposes

1. Insert newly generated OMOP synthetic data into a database
2. Truncate and re-insert newer vocabulary sets into the Atlas OMOP database

#### Requirements

- Supports PostgreSQL and MS SQL Server
- Uses the OMOP v5.4 DDL/SQL files (DDL, constraints, indexes) from the [OHDSI CommonDataModel repo](https://github.com/OHDSI/CommonDataModel/tree/main/inst/ddl/5.4)
- User specifies a path to a generated synthetic OMOP CSV directory to insert
- Supports re-insertion of newer OMOP data (including vocabularies) by:
  1. Dropping constraints, primary keys, and indexes
  2. Truncating tables
  3. Inserting new data
  4. Re-applying constraints, primary keys, and indexes

#### Future Use Case

- CLI to accept a FITFILE-generated OMOP extract and insert it into a database so tooling such as Achilles can be run against it

---

### 4. Additional OMOP Database Setup & Monitoring (FTFL-476)

Easily spin up additional OMOP databases in different technologies for stress testing against previously generated synthetic data.

#### Requirements

- Ability to set up OMOP databases in multiple technologies (beyond current single-tech setup)
- Run OMOP stress tests against the synthetic OMOP data generated above
- Monitor resource consumption during OMOP workflow runs
  - Improve the generic workflows monitoring dashboard to surface resource metrics

---

### 5. OMOP User Flow Stress Testing (FTFL-480)

A script that generates permutations of test variables to stress test the OMOP user flow.

#### Variables to Permute

| Variable | Description |
|---|---|
| Cohort size | Number of patients in the dataset |
| Number of tables / fields selected | Scope of the OMOP extract |
| Extract size | Controlled via a `LIMIT` clause |
| Privacy treatment | Boolean—applied or not |
| Number of OMOP data sources to link | Multi-source linkage scenarios |

#### Requirements

- Script generates tests across combinations (permutations) of the above variables
- Executes the OMOP user flow for each permutation

---

### Dependency Order

```
FTFL-488  Blob storage setup
    └── FTFL-475  Synthetic data generation → outputs to blob
            └── FTFL-479  DB ingestion script → reads from blob
                    └── FTFL-476  Additional DB setup + monitoring
                            └── FTFL-480  Stress test permutation script
```
