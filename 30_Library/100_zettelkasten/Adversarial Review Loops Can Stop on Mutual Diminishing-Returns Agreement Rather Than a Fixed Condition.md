---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:56:48+00:00
permalink: llmeon/30-library/100-zettelkasten/adversarial-review-loops-can-stop-on-mutual-diminishing-returns-agreement-rather-than-a-fixed-condition
proposition: An adversarial code-review loop — where a completion loop (autopilot)
  and a cross-model reviewer repeatedly iterate on a piece of work — can be given
  a stopping condition defined as mutual agreement between the generating model and
  the reviewing model that remaining issues have diminishing returns, rather than
  a fixed iteration count, a task-completion checklist, or an external test-based
  'gate. The loop repeats review-and-adjust cycles until both models converge on "further'
  changes aren't worth it," at higher token cost than a single pass, in exchange for
  more thoroughly battle-hardened output.
tags: [domain/llm, topic/code-quality, topic/loop-control, topic/workflow-design]
title: Adversarial Review Loops Can Stop on Mutual Diminishing-Returns Agreement Rather Than a Fixed Condition
  Than a Fixed Condition
type: claim
---

## Adversarial Review Loops Can Stop on Mutual Diminishing-Returns Agreement Rather Than a Fixed Condition

Most stopping conditions this vault has documented so far are external and objective: a fixed iteration count, a test suite passing, a checklist item completed. This claim describes a different kind of stopping condition—a subjective, negotiated one, arrived at by two models (the generator and an independent adversarial reviewer) converging on a shared judgment that continuing to iterate isn't worth it anymore. The loop doesn't stop because a metric hit a threshold; it stops because both parties in the review conversation agree the remaining issues are minor enough that further changes have diminishing returns relative to their cost.

This is explicitly framed as a cost/thoroughness trade-off: this pattern "does cost more tokens" than a single adversarial pass, in exchange for genuinely more hardened output—described as "an investment in your future self" rather than a default practice for every change.

### Scope & Conditions

Applies to higher-stakes or complex changes where the extra token cost of repeated adversarial iteration is justified by the value of catching more issues before they reach production. Not presented as a default for routine changes—a single adversarial pass (per the vault's existing cross-model auditing note) remains the baseline; this looped variant is an escalation for cases that warrant it.

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "If you want to take this a step further, you can combine rubber duck with Autopilot to get the models to work together in a loop to improve the final result: '/autopilot rubber duck this date picker implementation. When you have the result, review it carefully and make any necessary adjustments. Repeat the rubber duck review until both you and the reviewing model agree that the only items that remain have diminishing returns.' … This step does cost more tokens, but you are really battle-hardening the code."

### Implications

- This is a new stopping-condition type for the vault's existing loop-control note: [[Reasoning Loops Require Explicit Stopping Conditions (End-Loop Guardrails)]] establishes that loops need explicit stopping conditions generally, but the vault's examples so far have been objective/external (iteration counts, task-completion checks). This note adds a subjective, negotiated stopping condition—mutual model agreement—as a distinct category worth naming.
- It's a repeating, escalated version of the vault's existing single-pass adversarial review notes: [[Cross-Model Adversarial Auditing Uses an Independent LLM to Catch Blind Spots]] and [[Automated CI Pipelines Wire an Adversarial LLM Reviewer Into Branch-and-Rebase Before Human Review]] both describe a single adversarial review pass; this note describes chaining that pass into a repeating loop specifically for cases warranting the extra cost.
- It's a data point for the vault's rising-cost-of-newer-models cluster: [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]] documents rising per-task cost generally; deliberately choosing a more expensive, looped review pattern for high-value work is a concrete instance of accepting that cost trade-off knowingly, rather than it being an unwanted side effect.

### Related

- [[Reasoning Loops Require Explicit Stopping Conditions (End-Loop Guardrails)]]—extends: adds a subjective, mutual-agreement stopping-condition type to that note's general requirement for explicit stopping conditions.
- [[Cross-Model Adversarial Auditing Uses an Independent LLM to Catch Blind Spots]]—extends: chains that note's single-pass mechanism into a repeating, escalated loop.
- [[Automated CI Pipelines Wire an Adversarial LLM Reviewer Into Branch-and-Rebase Before Human Review]]—related: both describe adversarial-review automation; this note's looped variant is a higher-cost, higher-thoroughness escalation of that note's single-pass pipeline.
- [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]]—related: a concrete case of deliberately trading token cost for thoroughness.

### See Also

- [[Prompt Cache Discounts Reward Staying on the Same Model and Reasoning Level Within a Task]]

%%[extends:: [[Reasoning Loops Require Explicit Stopping Conditions (End-Loop Guardrails)]], strength=3, confidence=medium]%%

%%[extends:: [[Cross-Model Adversarial Auditing Uses an Independent LLM to Catch Blind Spots]], strength=3, confidence=medium]%%
