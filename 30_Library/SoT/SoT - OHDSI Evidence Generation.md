---
aliases: ["OHDSI Analytics", "Population-Level Estimation", "Patient-Level Prediction"]
confidence: "High"
created: 2026-01-06T19:30:51+00:00
epistemic: "Methodology"
last_reviewed: 
modified: 2026-01-06T19:33:34+00:00
purpose: "To define the three pillars of OHDSI analytics and the scientific rigour required for valid evidence."
review_interval: "1 year"
see_also: 
  - "[[SoT - OHDSI Toolstack & Atlas]]"
  - "[[SoT - Best Practices for Real-World Analysis]]"
source_of_truth: []
status: "Active"
tags: ["ohdsi", "analytics", "statistics", "science"]
title: SoT - OHDSI Evidence Generation
type: "SoT"
uid: 
updated: 
---

# SoT - OHDSI Evidence Generation

> **The Goal:** To generate reliable evidence by systematically applying best-practice methods across a federated network.

## 1. The Three Use Cases

### A. Clinical Characterization ("What happened?")

* **Goal:** Descriptive statistics.
* **Questions:**
    * "What is the prevalence of Diabetes?"
    * "What drugs are used after a diagnosis?" (Treatment Pathways).
* **Method:** Simple aggregation (`COUNT`, `GROUP BY`).
* **Feasibility:** Highly viable in **Read-Only** architectures.

### B. Population-Level Effect Estimation ("What is the causal effect?")

* **Goal:** Causal inference (Safety/Efficacy).
* **Questions:**
    * "Does Drug A cause more bleeding than Drug B?"
* **Method:**
    * **Propensity Score Matching:** To balance cohorts.
    * **Negative Controls:** Calibrating for residual bias.
* **Feasibility:** Hard in Read-Only (requires creating matched cohorts).

### C. Patient-Level Prediction ("What will happen to me?")

* **Goal:** Personalized risk scoring.
* **Questions:**
    * "What is my risk of Sepsis in the next 30 days?"
* **Method:** Machine Learning (LASSO, Random Forest, Deep Learning) on large feature sets.
* **Feasibility:** Hard in Read-Only (requires extracting massive feature matrices).

## 2. Evidence Quality Framework

Generating numbers is easy; generating **truth** is hard.

* **Clinical Validity:** Are we finding the right patients? (Phenotyping).
* **Software Validity:** Is the code correct? (Unit Tests).
* **Method Validity:** Is the math right? (Diagnostics).
* **Data Quality:** Is the source reliable? (DQD).

## 3. Large-Scale Analytics

OHDSI moves away from "One-Off" studies to **Systematic Evidence Generation**.

* **Example:** Instead of testing 1 drug vs 1 outcome, test *all* drugs against *all* outcomes to generate a background rate distribution.
