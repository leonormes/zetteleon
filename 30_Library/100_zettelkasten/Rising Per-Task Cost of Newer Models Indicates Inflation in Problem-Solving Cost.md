---
created: 2026-07-28T09:11:42+00:00
modified: 2026-08-08T10:29:23+00:00
permalink: llmeon/30-library/100-zettelkasten/rising-per-task-cost-of-newer-models-indicates-inflation-in-problem-solving-cost
title: Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost
---

---

created: 2026-07-28T00:00:00+00:00
modified: 2026-07-28T00:00:00+00:00
title: Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost
type: claim
epistemic_status: medium
tags: [domain/llm, topic/economics, topic/cost-optimization, topic/benchmarking]
proposition: Newer, more capable models (e.g. Sonnet 5, GLM 5.2) are observed to cost more, not less, to run to completion on benchmark tasks than their predecessors—despite being "better" models. This indicates a form of inflation in the cost of problem-solving: capability gains are being purchased with proportionally larger token consumption per task, not delivered as a fixed-cost improvement.
---

## Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost

The intuitive expectation for a model upgrade is: same task, same or lower cost, better result. What's observed instead is: same task, _higher_ cost, better result—because the newer model reasons longer, calls more tools, or iterates more before arriving at its answer.

This means "the model got better" and "the model got cheaper to use for a given problem" are not the same claim, and can move in opposite directions simultaneously. A benchmark score improving release-over-release can coexist with the dollar cost of clearing that benchmark also increasing release-over-release.

### Scope & Conditions

Observed specifically in benchmark-completion cost comparisons across model generations (Sonnet 5, GLM 5.2 cited). Most relevant for organizations budgeting AI spend based on an assumption that newer models will reduce cost per task—that assumption does not hold in this observed pattern.

### Evidence

Source: "State of Agentic Coding, episode 8, with Mario, Armin, and Ben" (Armin Ronacher). Quote: "newer, supposedly better models… are actually more expensive to run to completion on benchmarks than their predecessors, indicating an inflation in the cost of problem-solving" [45:57].

### Implications

- "Better" and "cheaper" must be evaluated as separate axes: model selection decisions based purely on capability benchmarks risk underestimating deployment cost.
- This compounds with agentic tool-call cost growth: [[Agentic Tool Calls Compound Context Growth Multiplicatively]] already shows agentic loops are token-expensive; if the underlying model itself also trends toward higher per-task consumption, the two effects stack.
- Budgeting AI spend on a "newer model = cheaper" assumption is unsafe: teams should measure actual cost-to-completion per task empirically rather than assuming generational improvement implies cost reduction.

### Related

- [[Agentic Tool Calls Compound Context Growth Multiplicatively]]—related: both describe cost growing faster than naive expectations, at the model-generation level (this note) versus the agentic-loop level (that note).
- [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]]—supports: rising per-task cost is a direct contributor to the pricing-model pressure that note describes.
- [[Auto-Regressive Generation Reprocesses the Entire Context on Every Token]]—context: any model that reasons longer per task incurs proportionally more of this reprocessing cost.

### See Also

- [[Continuous Autonomous Agent Loops Incur Significant API Cost]]

%%[supports:: [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]], strength=3, confidence=medium]%%
