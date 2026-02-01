---
aliases: ["Pre-specification", "Reproducible Research", "Scientific Best Practices"]
created: 2026-01-06T19:31:01+00:00
last_reviewed: 
modified: 2026-02-01T15:08:01+00:00
status: "Active"
tags: ["ethics", "methodology", "ohdsi", "science"]
title: SoT - Best Practices for Real-World Analysis
type: "SoT"
updated: 
---

## SoT - Best Practices for Real-World Analysis

> The Core Thesis: Scientific integrity in observational research relies on a strict separation of Design and Execution to prevent bias.

### 1. The Three Pillars of Reliability

#### A. Transparency (Code as Spec)

- Principle: The study package _is_ the protocol.
- Requirement: Every analytical decision (cohort definitions, R versions, parameters) must be fully executable and public.

#### B. Pre-specification (No Fishing)

- The Anti-Pattern: Running a study, seeing a "bad" p-value, tweaking a covariate, and re-running it. (P-hacking).
- The Best Practice:
    1. Define the protocol.
    2. Execute Diagnostics only (check covariate balance, sample size). Do NOT look at the outcome.
    3. Finalize the protocol.
    4. Unblind the result.

#### C. Validation (Empirical Proof)

- Negative Controls: Exposure-Outcome pairs where we _know_ there is no causal link.
- Calibration: If your method finds a risk for a Negative Control, your p-values are wrong. You must calibrate the distribution.

### 2. The Evidence Quality Model

- Data Quality: Proven by Data Quality Dashboard.
- Clinical Validity: Proven by PheValuator (Probabilistic Gold Standards).
- Method Validity: Proven by Control Experiments across the network.
