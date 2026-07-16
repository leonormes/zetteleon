---
aliases: [Cohort Generation, Evidence Generation, OHDSI Analytics]
created: 2026-01-06T18:52:01+00:00
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-ohdsi-analytics
tags: [analytics, evidence, ohdsi, sot]
title: SoT - OHDSI Analytics
---

## 1. Definitive Statement

> [!definition] Definition
> OHDSI Analytics are based on the principle of Methodological Standardization. Instead of writing bespoke analysis code for every question, researchers utilize pre-validated Analysis Packages (HADES) configured via a Study Specification (JSON).

---

## 2. The Three Primary Use Cases

OHDSI categorizes all observational research into three distinct pillars.

| Type | Question | Method/Tools |
|:--- |:--- |:--- |
| Characterization | _"What happened to them?"_ | Descriptive Statistics. Counts, distributions, incidence rates. <br>_(Tool: Achilles, CohortDiagnostics)_ |
| Population-Level Estimation (PLE) | _"What is the causal effect?"_ | Causal Inference. Propensity score matching, negative controls. Comparative safety/effectiveness. <br>_(Tool: CohortMethod, SelfControlledCaseSeries)_ |
| Patient-Level Prediction (PLP) | _"What will happen to me?"_ | Machine Learning. Training predictive models on historical data to predict future risk. <br>_(Tool: PatientLevelPrediction)_ |

---

## 3. The Cohort: The Unit of Analysis

In OHDSI, almost all analysis begins with the Cohort.

> [!definition] Cohort Definition
> A set of Persons who satisfy specific Inclusion Criteria for a Duration of Time.
>
> _Key Components:_
> 1.  Entry Event: What triggers entry? (e.g., First diagnosis of Diabetes).
> 2.  Inclusion Rules: Additional logic (e.g., Must have >365 days observation prior).
> 3.  Exit Strategy: When do they leave? (e.g., End of observation, death, or fixed duration).

### 3.1 The "Read-Only" Challenge

Standard OHDSI analytics assume the ability to Materialize (write) these cohorts into a `COHORT` table in the database.

- The Workaround: For read-only environments, the cohort logic must be "transpiled" into ephemeral Common Table Expressions (CTEs) that generate the population on-the-fly during query execution.

---

## 4. Evidence Quality Framework

Just because code runs doesn't mean the evidence is valid. OHDSI enforces quality via:

- Software Validity: Unit testing the HASES packages.
- Clinical Validity: Using PheValuator to probabilistically estimate the sensitivity/specificity of a cohort definition against a gold standard.
- Method Validity: Using Negative Controls (outcomes known _not_ to be caused by the exposure) to calibrate p-values and detect systematic error/bias.

---

## Related

- [[SoT - OHDSI Evidence Generation]] — _Systematically applying best-practice methods across a federated network._
- [[SoT - OHDSI Ecosystem]] — _Global collaborative dedicated to generating reliable evidence from observational data._
