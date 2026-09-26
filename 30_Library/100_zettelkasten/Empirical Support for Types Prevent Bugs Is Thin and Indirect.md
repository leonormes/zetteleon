---
conformant: true
contradicts: []
created: 2026-09-19T15:26:23+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-25T16:29:22+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/empirical-support-for-types-prevent-bugs-is-thin-and-indirect
proposition: The strongest available empirical evidence for structure-first design is adjacent rather than direct, since a 2017 study by Gao, Bird and Barr found that static typing via Flow or TypeScript would conservatively have caught only about 15 percent of a sample of 400 fixed public JavaScript bugs, and a 2019 reproduction by Berger et al. of an earlier cross-language study found only four programming languages with a statistically significant, and very small, association with defect rates; neither study isolates domain-faithful data modelling as the variable being tested.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [empirical-evidence, epistemics, evidence-quality, type-systems]
title: Empirical Support for Types Prevent Bugs Is Thin and Indirect
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Empirical Support for Types Prevent Bugs Is Thin and Indirect

The strongest available empirical evidence for structure-first design is adjacent rather than direct: a 2017 study (Gao, Bird & Barr) found that static typing via Flow or TypeScript would conservatively have caught only about 15% of a sample of 400 fixed public JavaScript bugs, and a 2019 reproduction (Berger et al.) of an earlier cross-language study found only four programming languages with a statistically significant, and very small, association with defect rates—neither study isolates domain-faithful data modelling as the variable being tested.

### Scope & Conditions

Concerns the empirical (not mechanistic) case for structure-first design; the mechanism itself is separately well-supported by worked examples, not by controlled studies.

### Evidence

> "Gao, Bird and Barr (ICSE 2017) sampled 400 fixed public JavaScript bugs and found Flow or TypeScript would conservatively have caught about 15%… Berger et al.'s 2019 reproduction of Ray et al. found only four languages with a statistically significant association with defects, and the effect sizes were exceedingly small."

### Implications

- The overall claim should be tagged "corroborated by mechanism and worked examples, but not measured" rather than empirically proven.

### Related

- [[Reproducibility and Replicability Are Distinct Standards of Scientific Reliability]]—shared mechanism: names the same category of evidentiary weakness (adjacent, non-reproduced findings standing in for direct measurement) this atom flags in the type-systems literature.

[supports:: [[Reproducibility and Replicability Are Distinct Standards of Scientific Reliability]], confidence=medium]

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—qualifies: that note's claims about structure reducing bugs/fragility are asserted without acknowledging how thin the direct empirical base actually is.
