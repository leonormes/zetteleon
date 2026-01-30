---
created: 2026-01-28T10:27:32+00:00
modified: 2026-01-30T06:20:36+00:00
title: FF test case
uuid: cfc2c6e0-f994-426c-9814-c91e5163cf15
---
- [ ] make this ff test case a confluence page ^2026-01-30T06-20-23
	- [📱 View in Todoist app](todoist://task?id=6frvg7Wf3xRJ597M) (Created: 📝 2026-01-30T06:20)
This is a perfect use case for testing whether you're really at the irreducible minimum of complexity, because federated medical research forces you to respect hard constraints rather than paper over them.

I'll give you a realistic demo research project that:

- Is ethically plausible in the NHS
- Strongly benefits from data-at-source + de-identification
- Exercises cohort definition, aggregation, linkage, and governance
- Keeps complexity where it belongs (data + invariants)

---

Demo Research Project

Federated Analysis of Post-COVID Cardiovascular Risk Across NHS Trusts

---

1. Why This Is a Good Test Case

This project stresses exactly the things your system is designed for:

Sensitive identifiable data must not leave source systems

Results only make sense across multiple trusts

Cohorts must be defined identically but executed locally

Aggregation must tolerate heterogeneous EHR schemas

De-identification must still allow longitudinal linkage

It mirrors real NHS research patterns without requiring real patients.

---

1. Participating Organisations (Nodes)

NHS Acute Trusts (hospital EPR systems)

NHS GP practices (primary care)

Optional: NHS Digital–style central analytics hub

NHS

Each node:

Holds identifiable patient data

Executes cohort queries locally

Returns only de-identified aggregates

---

1. Stakeholders

Clinical Stakeholders

Cardiologists

GPs

Respiratory physicians

Interest:

Is COVID infection associated with increased long-term cardiovascular risk?

---

Research Stakeholders

Epidemiologists

Public health researchers

Medical statisticians

Interest:

Population-level risk signals, stratified by age, sex, comorbidities.

---

Governance / Compliance

Caldicott Guardians

Data Protection Officers

NHS Trust Information Governance teams

Interest:

No raw patient data leaves site. Clear audit trail.

---

Technical Users (Your System's Audience)

Data engineers

Clinical informaticians

Platform engineers

Interest:

Federated query execution, schema mapping, reproducibility.

---

1. Core Research Question

> Does prior COVID-19 infection increase the incidence of major cardiovascular events within 12 months compared to matched controls?

Secondary questions:

Does severity of COVID matter?

Does risk vary by age, sex, or pre-existing conditions?

Does vaccination status modify risk?

---

1. Primary Outcome Measures

Defined once, executed everywhere:

Myocardial infarction

Stroke

New diagnosis of heart failure

New atrial fibrillation

All defined via:

ICD-10 codes

SNOMED codes

Or local diagnostic mappings

---

1. Cohort Definitions (This Is the Heart of the Demo)

Cohort A: COVID-Positive Patients

Inclusion criteria:

Age ≥ 18

Confirmed COVID-19 diagnosis (PCR or coded diagnosis)

Index date = first positive COVID test

Exclusion criteria:

Prior cardiovascular event in the last 5 years

Missing follow-up data

---

Cohort B: Matched Controls

Inclusion criteria:

No recorded COVID diagnosis

Matched 1:1 or 1:n on:

Age band

Sex

GP practice or region

Major comorbidities (diabetes, hypertension)

Index date:

Synthetic index date aligned to matched COVID case

---

Key Design Win for Your System

Matching logic runs locally, returning:

Counts

Event rates

Time-to-event histograms

No patient identifiers ever leave the node.

---

1. What Each Node Returns (De-Identified)

Examples of allowed outputs:

Cohort sizes

Event counts

Kaplan–Meier survival curves (binned)

Stratified aggregates (age bands, sex, comorbidity flags)

Pseudonymous cohort IDs (rotating salts per study)

❌ No dates of birth

❌ No postcodes

❌ No free text

❌ No direct identifiers

---

1. What the Hub Does

The central hub:

Receives only aggregate datasets

Links cohorts by study-specific pseudonyms

Performs:

Meta-analysis

Cross-site stratification

Sensitivity analysis

Visualization

This is where algorithmic complexity belongs:

Statistical modelling

Bias correction

Confidence intervals

The data complexity stays local.

---

1. Why This Demonstrates Conservation of Complexity

Complexity you cannot remove:

Clinical ambiguity

Coding heterogeneity

Longitudinal risk modelling

Complexity you can relocate:

Complexity	Where it lives

Privacy	Data structures + access boundaries

Matching	Local data models

Governance	Query contracts

Statistics	Central algorithms

This is exactly the principle you're researching.

---

1. Why This Is an Excellent Internal Test

It lets you validate:

Federated cohort definition

Schema translation

Query reproducibility

De-identification correctness

Auditability

Failure isolation (one node down ≠ study dead)

And—critically—it forces you to answer:

> What is the irreducible complexity here, and where does it belong?

---

1. Optional Extensions (If You Want to Push It)

Add vaccination status as a time-varying covariate

Add socioeconomic deprivation deciles (locally derived)

Introduce deliberate schema drift at one node

Simulate partial data loss or delayed reporting

---

Final Framing (This Is the Lesson)

This demo works because:

The data structures encode the invariants

The algorithms operate only on what cannot be frozen

Privacy is enforced structurally, not procedurally

That's the irreducible minimum you're aiming for.

If you want, next I can:

Turn this into a formal study protocol

Define query contracts / schemas

Design a minimal synthetic dataset

Stress-test where complexity leaks back in

This is exactly the right problem to sharpen your instincts.
