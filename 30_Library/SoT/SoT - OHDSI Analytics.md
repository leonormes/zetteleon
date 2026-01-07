---
aliases: ["OHDSI Analytics", "Evidence Generation", "Cohort Generation"]
confidence: "High"
created: 2026-01-06
last_reviewed: 2026-01-06
purpose: "Defines the standard analytical methods and use cases supported by the OHDSI framework."
status: "stable"
tags: ["ohdsi", "analytics", "evidence", "sot"]
type: "SoT"
---

## 1. Definitive Statement

> [!definition] Definition
> OHDSI Analytics are based on the principle of **Methodological Standardization**. Instead of writing bespoke analysis code for every question, researchers utilize pre-validated **Analysis Packages** (HADES) configured via a **Study Specification** (JSON).

---

## 2. The Three Primary Use Cases

OHDSI categorizes all observational research into three distinct pillars.

| Type | Question | Method/Tools |
| :--- | :--- | :--- |
| **Characterization** | *"What happened to them?"* | **Descriptive Statistics.** Counts, distributions, incidence rates. <br>*(Tool: Achilles, CohortDiagnostics)* |
| **Population-Level Estimation (PLE)** | *"What is the causal effect?"* | **Causal Inference.** Propensity score matching, negative controls. Comparative safety/effectiveness. <br>*(Tool: CohortMethod, SelfControlledCaseSeries)* |
| **Patient-Level Prediction (PLP)** | *"What will happen to me?"* | **Machine Learning.** Training predictive models on historical data to predict future risk. <br>*(Tool: PatientLevelPrediction)* |

---

## 3. The Cohort: The Unit of Analysis

In OHDSI, almost all analysis begins with the **Cohort**.

> [!definition] Cohort Definition
> A set of **Persons** who satisfy specific **Inclusion Criteria** for a **Duration of Time**.
>
> *Key Components:*
> 1.  **Entry Event:** What triggers entry? (e.g., First diagnosis of Diabetes).
> 2.  **Inclusion Rules:** Additional logic (e.g., Must have >365 days observation prior).
> 3.  **Exit Strategy:** When do they leave? (e.g., End of observation, death, or fixed duration).

### 3.1 The "Read-Only" Challenge
Standard OHDSI analytics assume the ability to **Materialize** (write) these cohorts into a `COHORT` table in the database.
*   **The Workaround:** For read-only environments, the cohort logic must be "transpiled" into ephemeral **Common Table Expressions (CTEs)** that generate the population on-the-fly during query execution.

---

## 4. Evidence Quality Framework

Just because code runs doesn't mean the evidence is valid. OHDSI enforces quality via:

*   **Software Validity:** Unit testing the HASES packages.
*   **Clinical Validity:** Using **PheValuator** to probabilistically estimate the sensitivity/specificity of a cohort definition against a gold standard.
*   **Method Validity:** Using **Negative Controls** (outcomes known *not* to be caused by the exposure) to calibrate p-values and detect systematic error/bias.
