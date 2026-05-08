---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:44+00:00
title: The OMOP Common Data Model (CDM) is a standardised, relational database schema designed to transf
---

The OMOP Common Data Model (CDM) is a standardised, relational database schema designed to transform disparate healthcare data—like hospital records, insurance claims, and pharmacy notes—into a common format. For a developer, it is best understood as a "standardised API" for data; once you write a query for one OMOP database, that same query can run on any other OMOP database in the world.

Here is how the system actually works from a developer's perspective:

## 1\. The Relational Schema (The Tables)

The CDM is organised into several functional groups of tables. Instead of every hospital having its own "Admissions" table with different column names, every OMOP instance uses the same structure:

- Clinical Data Tables: These store the actual patient events. Key tables include `PERSON` (demographics), `CONDITION_OCCURRENCE` (diagnoses), `DRUG_EXPOSURE` (prescriptions), and `PROCEDURE_OCCURRENCE`.
- Health System Tables: These describe the "where" and "who," such as `LOCATION`, `CARE_SITE`, and `PROVIDER`.
- Metadata & Derived Tables: Tables like `OBSERVATION_PERIOD` define the "window" of time during which a person's data was actually being recorded, which is critical for calculating rates and risks.

## 2\. The "Secret Sauce": Standardised Vocabularies

The most important part of OMOP is not the table structure, but the Standardised Vocabularies (found in the `VOCABULARY`, `CONCEPT`, and `CONCEPT_RELATIONSHIP` tables).

In raw health data, a "Heart Attack" might be recorded as an ICD-10 code (`I21.9`), a Read code (`G30..`), or a text string. In OMOP, every one of these "Source Concepts" is mapped to a single Standard Concept (usually from SNOMED-CT).

- Source Concept: What was actually recorded (e.g., the ICD-10 code).
- Standard Concept: The "master" ID that represents that clinical idea. When you write a query, you don't search for "I21.9"; you search for the Standard Concept ID for "Myocardial Infarction."

## 3\. How the Data Flows (ETL)

As a developer, your primary task with OMOP is usually the ETL (Extract, Transform, Load) process. This involves:

1. Mapping: Identifying which source table corresponds to which OMOP table.
2. Terminology Mapping: Using tools like Usagi to find the correct Standard Concept IDs for your local codes.
3. Transformation: Writing the code (SQL, Python, or R) to move the data into the CDM schema.

## 4\. The Domain Concept

OMOP is "domain-oriented," meaning data is stored based on what it is, not where it came from.

- If a source record says a patient was given a vaccine, it might be in a "Procedures" table in the original database.
- In OMOP, the vocabulary system determines that a vaccine is a "Drug." Therefore, the ETL must move that record into the `DRUG_EXPOSURE` table, regardless of where it lived in the source.

## 5\. Why Developers Use It

The primary benefit is Analytic Portability. Because the schema and vocabularies are fixed, the OHDSI community has built a massive suite of open-source tools (like Atlas for cohort building and Hades for R-based analytics) that work out-of-the-box once your data is in the OMOP format.

Instead of spending months cleaning data for a single study, you clean it once (the ETL), and then you can run hundreds of different validated studies instantly.
