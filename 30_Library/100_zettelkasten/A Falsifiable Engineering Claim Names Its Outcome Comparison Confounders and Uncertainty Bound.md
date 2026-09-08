---
aliases: []
conformant: true
contradicts: []
created: 2026-09-07T15:00:00+00:00
created_utc: 2026-09-07T15:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-07T15:00:00+00:00
permalink: llmeon/30-library/100-zettelkasten/a-falsifiable-engineering-claim-names-its-outcome-comparison-confounders-and-uncertainty-bound
proposition: Turning a vague engineering causal claim (e.g. "this change reduces latency") into a falsifiable, scientifically testable one requires specifying the exact outcome metric, the comparison baseline, the confounders ruled out, and the uncertainty threshold the effect must clear.
source_title: "I want to learn more about the philosophy of science and how the scientific method works"
status: seed
tags: [epistemology, falsifiability, philosophy-of-science, devops, measurement]
title: A Falsifiable Engineering Claim Names Its Outcome Comparison Confounders and Uncertainty Bound
type: claim
---

## A Falsifiable Engineering Claim Names Its Outcome Comparison Confounders and Uncertainty Bound

"Enabling feature flag X reduces API p95 latency" is not yet a scientific result—it is an unfalsifiable hypothesis until it specifies: the exact **outcome** (p95 over which endpoints, regions, traffic classes, time window), the **comparison** baseline (same version, load, deployment configuration), the **confounders** ruled out (traffic volume, caching, database performance, an unrelated release), the **prediction** the causal story implies (should the effect show consistently in a controlled A/B or repeated on/off comparison), and the **uncertainty** bound (is the difference bigger than normal variation and measurement noise). The result: "under specified conditions, flipping this flag should change this defined metric by approximately this much"—a claim that can lose.

### Scope & Conditions

Applies to operational and infrastructure claims (dashboards, rollouts, incident conclusions), not only laboratory-style experiments—the same falsifiability discipline transfers directly.

### Implications

- A causal claim about a system change should be rewritten in this form before being trusted, regardless of how intuitive the mechanism sounds.
- Reproducibility (same query/dataset/code) and replicability (a separate rollout or environment) are the two checks that follow once the claim is stated this way.

### Related

[extends:: [[Falsifiability Distinguishes Science from Dogma]], confidence=high]

- [[Falsifiability Distinguishes Science from Dogma]]—this note is a concrete, engineering-domain instantiation of that note's demarcation criterion: naming outcome/comparison/confounders/uncertainty is what "state in advance what would prove you wrong" looks like for a system change.

[depends_on:: [[Reproducibility and Replicability Are Distinct Standards of Scientific Reliability]], confidence=high]

- [[Reproducibility and Replicability Are Distinct Standards of Scientific Reliability]]—this note's reproducibility/replicability checks are the specific application of that distinction to operational analysis.
