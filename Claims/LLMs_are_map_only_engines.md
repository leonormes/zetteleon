---
type: Claim
title: LLMs are map-only engines (territory-correspondence absent)
statement: LLMs operate on the symbolic/distributional layer without territory-correspondence;
  hallucination is explained by priors filling the vacuum where grounding was absent.
confidence: 0.82
last_reviewed: 2026-07-07
falsifier: An LLM demonstrates behaviour inconsistent with pure distributional statistics
  (e.g., systematic logical reasoning beyond training data patterns).
crux: Whether LLMs construct output from mathematical operations on the territory
  or from a map-only distribution over symbols.
tags:
- llm_epistemology
- map_only
- territory_correspondence
- hallucination
links: []
permalink: llmeon/claims/llms-are-map-only-engines
---

## Evidence

- **Gemini (2026-07-07): Self-description fallacy.** When prompted for advice, Gemini claimed "As an AI, I operate entirely on rigid logic, defined parameters, and mathematical truths." This is a functional self-misrepresentation: generation is distributional pattern-completion (priors + statistics), not axiomatic derivation. The false claim conflates substrate (arithmetic hardware) with function (statistical inference). This is a direct specimen of priors filling the vacuum where territory-correspondence (here, self-correspondence) is absent. Tagged: `map_only_evidence`, `specimen_llm_self_description`.