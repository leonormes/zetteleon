---
aliases: [Blast Radius, Future-Proofing Metrics, Strategic Architectural Cost]
created: 2026-01-30T08:15:00+00:00
modified: 2026-07-13T08:45:21+00:00
permalink: llmeon/30-library/so-t/so-t-temporal-projection
tags: [code-quality, maintainability, metrics, software-architecture]
title: SoT - Temporal Projection
---

## Temporal Projection

Temporal Projection is the cognitive act of simulating the future lifecycle of a codebase. It is the counter-metric to "Speed of Implementation." Code quality is not defined by how fast it was written, but by the friction coefficient required to modify it in the future.

### The Core Metric: Blast Radius

Blast Radius is the quantitative measure of Coupling.

- Definition: If I change the requirements for _this_ function/module in 6 months, how many other files must also be edited?
- The Rule: High Blast Radius = Architectural Failure.
- Goal: Optimize for Local Volatility (internals are easy to change) and Global Stability (interfaces are immutable).

### The Language of Cost

We must abandon the term "Trade-off" when it is used as an excuse for laziness.

- Lazy: "I didn't add the interface because it's a trade-off for speed." (False. You created debt.)
- Strategic: "I accepted the Strategic Architectural Cost of writing 50 lines of boilerplate to decouple these modules, securing long-term agility."

> [!tip] The Temporal Test
> Before committing code, ask: "If I delete this feature next year, does the system break cleanly, or does it bleed?"

---

See Also: [[SoT - Dimensions of Code Understanding]], [[SoT - Parochial Code]], [[Technical Debt]]
