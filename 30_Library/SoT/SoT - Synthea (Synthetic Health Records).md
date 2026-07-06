---
created: 2026-04-02T10:15:00+00:00
last-synthesis: 2026-04-02
modified: 2026-07-04T10:50:50+00:00
permalink: llmeon/30-library/so-t/so-t-synthea-synthetic-health-records
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [ehr, ohdsi, simulation, synthetic-data, type/SoT]
title: SoT - Synthea (Synthetic Health Records)
trust-level: stable
---

## Minimum Viable Understanding (MVU)

Synthea is an open-source simulation engine designed to generate Realistic Synthetic Electronic Health Records (RS-EHRs) without using real patient data. It solves the "data access gap" by creating cradle-to-grave patient histories from birth to death based on publicly available aggregate statistics and clinical guidelines.

## Working Knowledge

### 1. The PADARSER Framework

The _Publicly Available Data Approach to the Realistic Synthetic EHR_ (PADARSER) assumes access to real records is impossible. It ensures absolute privacy by building simulations entirely from:

- Public demographic statistics.
- Clinical practice guidelines.
- Disease prevalence rates.

### 2. State-Transition Behavior Modeling

Synthea models complex patient journeys using state-transition machines (encoded in JSON).

- Control States: Internal logic tracking attributes (e.g., initial, terminal, delay, counter states).
- Output States: Events that write to the final record (e.g., "Encounter," "ConditionOnset").
- Transition Logic:
    - _Direct:_ Sequential flow.
    - _Distributed:_ Probabilistic paths based on percentage distributions.
    - _Conditional:_ Attribute-based branching (e.g., "If Age > 50").

### 3. Longitudinal "Lifespan" Simulation

Simulation proceeds at configurable timesteps (e.g., every 7 days). This continuous tracking ensures highly cohesive, historically accurate data sequences rather than isolated data points.

## Current Understanding

### Implementation & Interoperability

To maximize utility, synthetic data generation must adhere to strict standards:

- Modularity: Rules are stored as standalone JSON modules, allowing domain experts to inspect and modify them without code changes.
- Output Standards: Data is exported directly into industry formats like HL7 FHIR, C-CDA, and the [[SoT - OMOP Common Data Model|OMOP CDM]].
- Validation: Generators are tuned by comparing large-batch population statistics against real-world prevalence data, adjusting transition probabilities until they mirror the target population.

## Related Knowledge

- Semantic Mapping: [[SoT - OHDSI Standardized Vocabularies]]
- Structural Target: [[SoT - OMOP Common Data Model]]
- Validation Tools: [[SoT - OHDSI ETL & Data Quality]]
