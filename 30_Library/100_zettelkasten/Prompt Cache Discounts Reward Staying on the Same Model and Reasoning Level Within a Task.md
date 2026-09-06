---
axiom: true
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:04+00:00
permalink: llmeon/30-library/100-zettelkasten/prompt-cache-discounts-reward-staying-on-the-same-model-and-reasoning-level-within-a-task
proposition: Staying on the same model and the same reasoning level for the duration
  of a single feature, bug, or enhancement keeps prior turns cached, giving a cost
  discount on subsequent requests within that task. Switching models or switching
  reasoning level mid-task breaks that cache, forfeiting the discount and paying full
  price on the next request as if starting fresh.
tags: [domain/llm, topic/cost-optimization]
title: Prompt Cache Discounts Reward Staying on the Same Model and Reasoning Level Within a Task
  Within a Task
type: claim
---

## Prompt Cache Discounts Reward Staying on the Same Model and Reasoning Level Within a Task

Prompt caching works by reusing previously-processed context rather than reprocessing it from scratch on every call—which is only possible if the request landing on the cache matches closely enough with what's already cached. Changing the model mid-task, or changing the reasoning level (e.g. low to high effort) on the same model, invalidates that match: the next call can no longer benefit from the cached prior context and has to be processed fresh, at full cost.

The practical consequence is a specific, easy-to-violate discipline: pick a model and reasoning level for a task at the outset, and stick with it for that task's duration, rather than switching mid-stream for a perceived quality improvement—the switch itself has a hidden cost in forfeited cache discounts, on top of whatever price difference exists between the two configurations.

### Scope & Conditions

Applies to providers/APIs that implement prompt caching keyed on model and reasoning-level consistency. The specific mechanics (what counts as a cache-breaking change, how long a cache persists) vary by provider and aren't detailed in the source—treat this as a general discipline (avoid switching model/reasoning level mid-task without reason) rather than a precisely quantified saving.

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "I recommend using a medium-sized model, such as GPT 5.6 Terra or Claude Sonnet, on medium reasoning for most work. I also recommend you stick with whatever model you choose here for the duration of this particular feature, bug, or enhancement. Prompt caching will save you tokens. As long as you don't switch to a different model or reasoning level, your previous chats remain cached with the model, giving you a discount on future requests."

### Implications

- This is a distinct, mechanistic cost-optimization lever from the vault's existing tiering and quota notes: [[Token Smarter Concentrates Human Oversight at Architectural Leverage Points While Tiering Models by Task]] and [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]] both concern _which_ model to route work to; this note concerns cost incurred by _switching_ between models or configurations mid-task, independent of which specific tiering strategy is chosen—the two considerations can be in tension (switching to a more appropriate model tier for a sub-task breaks the cache benefit of staying put).
- It adds a practical constraint to the topical-session-scoping practice from the same source: staying on one model/reasoning level and starting a new session per topic are both about maintaining a stable, cacheable working context for the duration of a coherent unit of work, rather than churning configuration or context mid-task.
- It's a controllable, deliberate-choice countermeasure to the vault's rising-cost-of-newer-models trend: [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]] documents an external cost pressure; avoiding unnecessary model/reasoning-level switches is a direct, low-effort lever an individual engineer can pull to reduce their own exposure to that pressure.

### Related

- [[Token Smarter Concentrates Human Oversight at Architectural Leverage Points While Tiering Models by Task]]—related: tiering strategy and cache-preservation discipline can be in tension when appropriate tiering would require a mid-task switch.
- [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]]—related: another cost/resource-constraint consideration for the same tiering decisions.
- [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]]—supports: a controllable, individual-level countermeasure to that note's broader cost-inflation trend.

### See Also

- [[Adversarial Review Loops Can Stop on Mutual Diminishing-Returns Agreement Rather Than a Fixed Condition]]

[supports:: [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]], strength=2, confidence=medium]
