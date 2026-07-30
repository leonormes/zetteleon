---
permalink: llmeon/30-library/100-zettelkasten/harness-engineering-splits-into-an-inner-harness-tools-apis-and-an-outer-harness-dev-environment
---

---
created: 2026-07-28T00:00:00+00:00
modified: 2026-07-28T00:00:00+00:00
title: Harness Engineering Splits into an Inner Harness and an Outer Harness
type: claim
epistemic_status: medium
tags: [domain/llm, topic/agent-architecture, topic/harness-design]
proposition: Structuring the external environment around an LLM "raises the floor" of its effective capability, and this harness has two distinct layers — the inner harness (the precise tools and APIs exposed to the model) and the outer harness (the surrounding developer environment: testing frameworks, CI, and custom integrations built around the agent). Both layers do real, distinct work, and conflating them obscures where a given reliability problem actually lives.
---

## Harness Engineering Splits into an Inner Harness and an Outer Harness

A harness isn't one undifferentiated thing wrapped around an LLM — it's two layers with different jobs. The inner harness is what the model directly touches: the specific tools and APIs it can call, their shapes, their error messages, what's exposed versus hidden. Get the inner harness wrong and the model makes bad calls even when it's reasoning correctly, because the affordances it has to work with are poor. The outer harness is everything around that: the test suite that validates the model's output, the CI pipeline that gates it, the custom integrations that connect the agent to the rest of the engineering system. Get the outer harness wrong and even a model making good tool calls produces work that never gets properly checked or safely shipped.

The practical value of the split is diagnostic: when an agent's output is unreliable, the first question is which layer is actually failing — is the model being given the wrong tools/APIs to work with (inner), or is the surrounding validation and integration infrastructure inadequate to catch and correct its output (outer)? These require different fixes.

### Scope & Conditions

Applies as a diagnostic and design framework for any agent harness, particularly useful when troubleshooting reliability issues or planning where to invest engineering effort in improving an existing agent system.

### Evidence

Source: "Context engineering with Dex Horthy" (Gergely Orosz interviewing Dex Horthy, Human Layer). "Structuring the external environment to 'raise the floor' of an LLM's capabilities. This includes the inner harness (the precise tools and APIs exposed to the model) and the outer harness (the developer environment, testing frameworks, and custom integrations built around the agent)" [27:08].

### Implications

- **This is a refinement of the vault's existing, undifferentiated harness concept**: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]] and [[Harness Engineering]] both describe harnessing as a single layer of deterministic control around the LLM; this note adds the inner/outer distinction as a more precise decomposition of what that control layer actually consists of.
- **The outer harness overlaps with existing validation-loop concepts**: the "testing frameworks... built around the agent" described here as outer harness is functionally the same mechanism as the deterministic validation loops in [[Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows]] — the split gives that existing pattern a clearer home within the two-layer harness model.
- **It gives the vault's context-management notes a place to sit structurally**: [[Intentional Compaction Clears History and Reseeds a Fresh Session with One Compressed Artifact]] is arguably an inner-harness concern (it shapes what the model actually sees), while CI/testing infrastructure is squarely outer-harness — useful for classifying future harness-related notes.

### Related

- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]]—extends: adds the inner/outer decomposition to the existing undifferentiated harness concept.
- [[Harness Engineering]]—extends: same relationship.
- [[Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows]]—related: the deterministic validation loops that note describes are an outer-harness mechanism under this note's framework.
- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]]—related: sandbox isolation in that pattern is an outer-harness design decision.

### See Also

- [[Intentional Compaction Clears History and Reseeds a Fresh Session with One Compressed Artifact]]

%%[extends:: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]], strength=4, confidence=medium]%%
%%[extends:: [[Harness Engineering]], strength=4, confidence=medium]%%