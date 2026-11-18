---
title: Miro Board — Product Backlog Ideas (2026-11-18)
type: project
status: seed
tags:
- fitfile
- backlog
- miro
conformant: true
created: 2026-11-18 00:00:00+00:00
modified: 2026-11-18 00:00:00+00:00
source: https://miro.com/app/board/uXjVHUdjoto=/
project_name: fitfile
permalink: llmeon/work/miro-board-product-backlog-ideas-2026-11-18
---

## Source

Extracted on 2026-11-18 from the Miro board at <https://miro.com/app/board/uXjVHUdjoto=/> (40 items: one table with 26 populated rows, 37 sticky notes, 2 connectors). Text is verbatim from the board, including typos. Reach, impact, confidence and effort values and the computed RICE scores stay on the board and are not reproduced here.

## Backlog table ("Copy of Product backlog")

Grouped by the table's Champion column. Each item shows priority · status · category where the board has them.

### Leon

- **Release Pipeline** — P2-Medium · Not started · Platform
  - Success metric: Release on-demand without waiting for the clear staging
  - Notes: Leon: List of options (prons and cons) low effort for now
- **Setup alerts on all issues reported by the customer** — P0-Critical · Not started · Platform
  - Success metric: Alerting for all historic failures raised by client
- **STRESS Testing of the Application (12M)**
  - Success metric: Ability to obtain performance metrics, providing customer and business confidence

### Helena

- **Probabilistic Matching UI Interface** — P3-Low · Not started · Product
  - Notes: NWSDE only currently which is not actively progressing
- **CE/CE+ 4 July (HA/RM)** — P0-Critical · Not started · Compliance
  - Success metric: Certification
  - Notes: Helena/Robin to propose increments of work
- **ISO27001 surveillance audit 23-24 June (HA/RM)** — P0-Critical · In Progress · Compliance
  - Success metric: Certification
  - Notes: Helena/Robin to propose increments of work
- **NHS DSPT 30 June (HA/RM)** — P0-Critical · In Progress · Compliance
  - Success metric: Certification
  - Notes: Helena/Robin to propose increments of work
- **Review of current data and coding QC and QA (HA)** — P2-Medium · In Progress · Quality
  - Success metric: Evidence base of validation and verification work

### Pavlo

- **Platform Boundary Architecture *Architecture*** — Platform
  - Notes: PK + OR
- **Runtime Feature Flags** — Platform
- **Operations Outside Project Context**
- **E2E Test Suite (Playwright)** — Platform
  - Notes: Individual item
- **Twin.macro Removal (PK)** — Platform
  - Notes: Individual item

### Robin

- **Frontend Observability (PK + RM)** — Product, Quality
- **Pen-test remediation burn-down & IAM least-privilege** — Compliance
- **Alert handling process**
  - Notes: Process rather then development item
- **CI/CD Deployment Repetition**
  - Success metric: The ability to repeat deployments

### Ollie

- **Kubernetes Resource Allocations**
- **Local developer Environments improvements**
  - Notes: In progress, Individual item
- **Terraform AWS module**
  - Notes: NUH
- **Custom Workflow Builder** — Backlog · Product
  - Success metric: Any compatible tasks/operation composed in a moduler data pipeline way
  - Notes: We have list of tasks that can be run in the FITFILE application

### Weronika

- **Artefacts Viewer (internal)** — P1-High · Not started · Product
  - Success metric: Artefact = anything produced within the operation. 1) List of all possible artefacts and associated item

### No champion

- **Deployment process updates**
- **Next round of highest priorty CV patching**
- **Data Retention Policies** — Product
- **Relational Dataset Archifact**

## Sticky notes — feature ideas (31)

Listed left to right as laid out on the board. The board has no labels or frames, so no grouping is implied beyond the two spatial clusters.

### Left-hand cluster (5)

- Copy Query Plans
- Cancel Query Runs
- Project Tagging
- Migrate QueryPlans to new Workflow architecture
- Data Source Refresh Detection and Monitoring

### Main cluster (26)

- Data Retention Policy
- Dataset Project Encryption
- Notifications
- Add context to OMOP harmonisation (decision behind mapping)
  - Connector: **Depends On** → File Upload
- Data Shield integration? (open source)
- Data Visualisation (Strategus)
- Message Broker / pub sub
- Federated Analytics
  - Connector: **Maybe Depends On** → SQL Query Engine
- Common Aggregate Functions
- Artifact Management
- Relational (multi table) Dataset Artifact
- Terminology Server
- Policy Query Management
- Five Safes
- File Upload
- Schema Improvements (adding metadata)
- SQL Query Engine
- Differential Privacy
- Data Profiling
- Open Data Specification
- Research Object
- Rename Datasets and Outputs
- Linking multiple common data models
- Retrieval of patient files (images, genomics, etc.)
- Migrate Workflows API
- Customer Workflow Builder

## Scoring guide and process sticky notes (6)

Sit above the table.

- **Reach** — estimated/customers affected per quarter. 1, 2, 3 (max)
- **Impact** — based on the customer usage/company objectives (0.25/0.5/1/2/3)
- **Confidence** — development confidence level as a %
- **Effort** — person/months work (0.5/1/2) = number of months it would take a single person to complete the project
- **Define the Success Metric**
- **Select 1 topic for independent champions**

## Possible overlaps (my observation, not on the board)

- "Data Retention Policies" (table) and "Data Retention Policy" (sticky)
- "Relational Dataset Archifact" (table) and "Relational (multi table) Dataset Artifact" (sticky)
- "Custom Workflow Builder" (table, Ollie) and "Customer Workflow Builder" (sticky). One may be a typo of the other.