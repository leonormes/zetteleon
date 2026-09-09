---
conformant: true
created: 2026-09-07T15:00:00+00:00
created_utc: 2026-09-07T15:00:00+00:00
definition: Reproducibility is getting consistent results from the same data, analysis steps, methods, and code; replicability is getting consistent results from a new, independently collected study or dataset addressing the same question. The two are distinct standards, per the U.S. National Academies of Sciences.
epistemic_status: high
modified: 2026-09-09T12:34:15+00:00
permalink: llmeon/30-library/100-zettelkasten/reproducibility-and-replicability-are-distinct-standards-of-scientific-reliability
source_title: "I want to learn more about the philosophy of science and how the scientific method works"
status: seed
tags: [epistemology, philosophy-of-science, replicability, reproducibility]
title: Reproducibility and Replicability Are Distinct Standards of Scientific Reliability
type: concept
used_in_claims: []
---

## Reproducibility and Replicability Are Distinct Standards of Scientific Reliability

The National Academies of Sciences distinguishes two different reliability checks that are often conflated under "can this be repeated?": reproducibility means rerunning the same analysis on the same data with the same methods and code and getting the same result; replicability means an independent, newly collected study or dataset addressing the same question produces a consistent result. Reproducibility checks whether the original work was done correctly and recorded faithfully; replicability checks whether the finding itself generalises beyond that one dataset.

### Scope & Conditions

Applies to any empirical claim, including operational/engineering analysis, not only laboratory science.

### Implications

- A versioned query, dataset, and analysis script gives you reproducibility; a separate rollout, environment, or independently collected dataset is needed to test replicability.
- A result can be perfectly reproducible (same code, same data, same output every time) while still failing to replicate—meaning the original dataset or setup, not the analysis, was the weak point.

### Related

- [[The Public Paper Trail of Science Makes Its Self-Correction Verifiable Without Firsthand Observation]]—shared mechanism: both concern how a result becomes independently checkable rather than something to be taken on trust.
