---
created: 2026-04-16T11:17:09+00:00
modified: 2026-07-13T08:44:32+00:00
permalink: llmeon/30-library/200-projects/12-million-patient-synthetic-nhs-omop-pipeline
project_category: omop
project_name: OMOP
project_status: active
title: 12 Million Patient Synthetic NHS-OMOP Pipeline
type: null
---

This project structure organises the development of a high-scale, research-ready synthetic environment for the NHS. It prioritises the transition from raw clinical simulation to a structured OMOP Common Data Model (CDM) that handles 12 million patient identities and their associated 12 billion clinical rows.

## Epic: 12 Million Patient Synthetic NHS-OMOP Pipeline (Scale & Fidelity)

Goal: Build a robust, parallelised pipeline to generate a national-scale synthetic dataset (12 million patients) mapped to OMOP CDM v5.4, incorporating UK-specific clinical pathways, demographics, and identity linkage logic.

---

## Task 1: Shared Storage & Asset Management (FTFL-488)

- Description: Provision a central blob storage account to serve as the single source of truth for OMOP vocabularies and generated CDM assets.
- Requirements:
    - Store Athena-downloaded vocabularies with clear versioning and timestamps.
    - Enable access for internal staging and external customer SDE/Atlas instances.
    - Store Achilles reports or distinct concept distribution statistics alongside the CDM data.
- Success Criteria: Stored datasets are accessible to both the `omop-cli` generation workers and the database ingestion scripts.

## Task 2: High-Scale UK-Localized Generation (FTFL-475)

- Description: Implement the `swpc_synthea` (UK-fork) engine to produce 12 million patients worth of longitudinal primary care data.
- Technical Specifications:
    - Localisation: Utilise NICE clinical guidelines, dm+d medication codes, and Suffolk-specific demographics.
    - Scale: Partition the 12 million patients across parallel JVM workers using the `omop-cli`.
    - Storage Efficiency: Standardise on Parquet for intermediate storage to achieve a 13x reduction in footprint (targeting ~2 TiB instead of ~26 TiB FHIR).
- Success Criteria: 12 million unique patient histories generated with valid 10-digit synthetic NHS numbers and English postcodes.

## Task 3: Identity Linkage & Privacy Simulation (MPS Logic)

- Description: Implement the Master Person Service (MPS) logic through `nhs_post_process.py` to ensure consistent patient identity across disparate silos.
- Technical Specifications:
    - Linkage Tiers: Simulate Cross-check, Alphanumeric (Soundex), and Algorithmic tracing.
    - Privacy Flags: Inject "Sensitive" and "Legacy Sensitive" status markers into the synthetic population.
    - Opt-Out Logic: Simulate the National Data Opt-Out (NDOO) by filtering patients via a mock MESH API.
- Success Criteria: The system assigns persistent `Person_ID` values that remain consistent when the dataset is fragmented into GP, A&E, and Mental Health silos.

## Task 4: Multi-Tech Database Ingestion & Seeding (FTFL-479)

- Description: Develop a flexible ingestion script that reads synthetic assets from blob storage and seeds them into target database environments.
- Requirements:
    - Decouple generation from specific database technology.
    - Support both PostgreSQL and MSSQL seeding from a single Parquet/CSV source.
    - Implement "Sub-cohort injection" to ensure specific clinical profiles (e.g., diabetics) are represented in every run.
- Success Criteria: Successfully seed 12 billion rows into a target OMOP schema while maintaining referential integrity across all CDM tables.

## Task 5: Environment Monitoring & Stress Test Setup (FTFL-476)

- Description: Configure additional OMOP databases for performance benchmarking and monitor the resource consumption of the transformation workflows.
- Requirements:
    - Improve the generic workflow monitoring dashboard to surface CPU, memory, and I/O metrics.
    - Enable automated "burn-in" tests for the Hyve ETL and FITFILE transformation engines.
- Success Criteria: Real-time visibility of system performance during the transformation of high-volume (10M+ patient) cohorts.

## Task 6: Automated Stress Test Permutation Runner (FTFL-480)

- Description: Build a script to automate the execution of the OMOP user flow across various stress test variables.
- Permutation Variables:
    - Cohort Size: From 1,000 to 12,000,000 patients.
    - Selection Scope: Varying the number of OMOP tables and fields selected.
    - Privacy Treatment: Toggling k-anonymity and nullification protocols on/off.
    - Linkage Scenarios: Testing the join logic across multiple data sources.
- Success Criteria: Comprehensive test report identifying the "breaking points" of the FITFILE application under extreme data loads.

---

## Orchestration Requirement (RAP Compliance)

All tasks must be delivered as a Reproducible Analytical Pipeline (RAP) using the Kedro framework. This ensures that the transformation from `swpc_synthea` raw output to the final OMOP database is auditable, automated, and maintainable.
