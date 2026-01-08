---
aliases: ["Federated Research Model", "OHDSI Network", "OMOP Philosophy"]
confidence: "High"
created: 2026-01-06T18:52:00+00:00
epistemic: ""
last_reviewed: 2026-01-06
modified: 2026-01-08T10:49:42+00:00
purpose: "Defines the high-level mission, architecture, and federated nature of the OHDSI collaborative."
review_interval: ""
see_also: []
source_of_truth: []
status: "stable"
tags: ["ohdsi", "SoftwareEngineering/Architecture", "sot"]
title: SoT - OHDSI Ecosystem
type: "SoT"
---

## 1. Definitive Statement

> [!definition] Definition
> **OHDSI** (Observational Health Data Sciences and Informatics) is a global, open-science collaborative dedicated to improving health by generating reliable evidence from observational data.
>
> It operates on a **Federated Research Network** model: **"The code travels to the data."** Patient-level data remains local and secure; only aggregated evidence is shared.

### 1.1 Core Mission

To resolve the complexity of converting raw patient data into reliable evidence by standardizing:

1. **Data Structure** (OMOP CDM)
2. **Data Content** (Standardized Vocabularies)
3. **Analytics** (Standardized Methods Library)

---

## 2. The Federated Architecture

OHDSI solves the privacy/sovereignty paradox of healthcare data through federation.

| Layer | Responsibility | Details |
|:--- |:--- |:--- |
| **Data Partners** | **Custody** | Hospitals/Insurers convert their local data to OMOP CDM. They retain full control and governance. |
| **Research Network** | **Coordination** | Entities like **ARACHNE** or **EHDEN** coordinate studies across multiple partners. |
| **The Analysis** | **Execution** | A "Study Package" (Container/R-Code) is sent to the partner. It runs locally. |
| **The Evidence** | **Synthesis** | Only non-identifiable summary statistics (counts, hazard ratios) are returned to the study lead. |

---

## 3. Key Entities & Tools

- **OMOP (Observational Medical Outcomes Partnership):** The public-private partnership that originally developed the CDM. Now maintained by OHDSI.
- **ATLAS:** The primary web-based GUI for designing cohorts and analyses.
- **HADES:** The suite of R packages used for statistical execution (Prediction, Estimation).
- **ARACHNE:** The logistics platform for managing distributed network studies and security.

### 3.1 The "Five Safes" Framework

OHDSI infrastructure (often packaged in **RO-Crates**) supports the "Five Safes" of data governance:

1. **Safe Projects:** Is this use of data appropriate?
2. **Safe People:** Are the researchers authorized?
3. **Safe Data:** Is the data treated to limit disclosure risk?
4. **Safe Settings:** Does the access environment prevent unauthorized export?
5. **Safe Outputs:** Are the aggregate results non-disclosive?
