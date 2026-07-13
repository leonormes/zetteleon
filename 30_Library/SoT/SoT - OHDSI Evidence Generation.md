---
aliases: [OHDSI Analytics, Patient-Level Prediction, Population-Level Estimation]
created: 2026-01-06T19:30:51+00:00
last_reviewed: null
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-ohdsi-evidence-generation
status: Active
tags: [analytics, ohdsi, science, statistics]
title: SoT - OHDSI Evidence Generation
type: SoT
updated: null
---

## SoT - OHDSI Evidence Generation

> The Goal: To generate reliable evidence by systematically applying best-practice methods across a federated network.

### 1. The Three Use Cases

#### A. Clinical Characterization ("What Happened?")

- Goal: Descriptive statistics.
- Questions:
    - "What is the prevalence of Diabetes?"
    - "What drugs are used after a diagnosis?" (Treatment Pathways).
- Method: Simple aggregation (`COUNT`, `GROUP BY`).
- Feasibility: Highly viable in Read-Only architectures.

#### B. Population-Level Effect Estimation ("What is the Causal Effect?")

- Goal: Causal inference (Safety/Efficacy).
- Questions:
    - "Does Drug A cause more bleeding than Drug B?"
- Method:
    - Propensity Score Matching: To balance cohorts.
    - Negative Controls: Calibrating for residual bias.
- Feasibility: Hard in Read-Only (requires creating matched cohorts).

#### C. Patient-Level Prediction ("What Will Happen to Me?")

- Goal: Personalized risk scoring.
- Questions:
    - "What is my risk of Sepsis in the next 30 days?"
- Method: Machine Learning (LASSO, Random Forest, Deep Learning) on large feature sets.
- Feasibility: Hard in Read-Only (requires extracting massive feature matrices).

### 2. Evidence Quality Framework

Generating numbers is easy; generating truth is hard.

- Clinical Validity: Are we finding the right patients? (Phenotyping).
- Software Validity: Is the code correct? (Unit Tests).
- Method Validity: Is the math right? (Diagnostics).
- Data Quality: Is the source reliable? (DQD).

### 3. Large-Scale Analytics

OHDSI moves away from "One-Off" studies to Systematic Evidence Generation.

- Example: Instead of testing 1 drug vs 1 outcome, test _all_ drugs against _all_ outcomes to generate a background rate distribution.
