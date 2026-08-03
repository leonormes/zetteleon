---
title: HEAD - Should the LLM have write authority over the wiki layer?
type: question
tension: Full LLM ownership of the wiki risks permanently encoding confident hallucinations;
  human review gates add fidelity at the cost of friction I may not sustain.
candidate_answers:
- Full LLM write authority with periodic lint
- Human review gate on ingest only
- Write authority scoped by note type
related_claims:
- '[[SoT - LLM Wiki Pattern]]'
- '[[SoT - AI Sycophancy]]'
- '[[SoT - Typed Answer Contract (TAC) for LLM Output]]'
sources:
- '[[SoT - LLM Wiki Pattern]]'
tags:
- state/thinking
- prodos/head
conformant: true
status: open
prodos:
  kind: head
  lifecycle: active
created: 2026-08-03 13:20:30+01:00
modified: 2026-08-03 13:20:30+01:00
permalink: llmeon/20-thinking/21-workbench/head-should-the-llm-have-write-authority-over-the-wiki-layer
AoL: System
closing_condition: true
---

## The Question

[[SoT - LLM Wiki Pattern]] gives the LLM full ownership of the wiki layer, and names the risk: confident hallucinations get permanently encoded. The schema/style-guide layer mitigates but does not eliminate it. A human review gate on ingest would add fidelity at the cost of friction. Which trade do I take — and separately, how often should the lint run?

## Why It Matters

The Hermes vault now runs on this pattern, so the answer is already live in production whether or not I have decided it. Every unreviewed write compounds; an error encoded six months ago is indistinguishable from a fact by now.

## What I Currently Think

A blanket review gate will not survive contact with my executive function — I will skip it, and then I will have friction *and* unreviewed writes. Scoping authority by note type looks more durable: let the LLM own `evidence` and summary layers freely, gate anything that becomes a `claim` or an `axiom:`. That matches where the epistemic weight actually sits.

## What Would Settle It

Check whether the Hermes vault's existing wiki layer contains a claim I now believe that I cannot trace to a source. One found instance settles this in favour of gating; a clean sample after ten spot-checks settles it in favour of leaving it open. Ten spot-checks is an hour.

## Sources

- [[SoT - LLM Wiki Pattern]]