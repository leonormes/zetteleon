---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:00+00:00
permalink: llmeon/30-library/100-zettelkasten/evidence-based-pipeline-optimization-vs-cost-based-optimization
proposition: Traditional database optimizers minimize query cost (time, CPU). LLM
  pipeline optimizers should maximize accuracy on real data. Evidence-based optimization
  samples real data, runs candidate pipeline plans, measures output quality using
  an LLM evaluator, and empirically selects the most accurate pipeline.
tags: [domain/llm, topic/measurement, topic/optimization, topic/pipelines]
title: Evidence-Based Pipeline Optimization vs Cost-Based Optimization
type: claim
---

## Evidence-Based Pipeline Optimization Vs Cost-Based Optimization

A classical database optimizer works within a well-defined cost model: "This query plan costs 10 million CPU cycles." It evaluates trade-offs and selects the minimum-cost plan.

LLM pipelines have no such model. The cost of a pipeline (tokens, latency) is predictable; the quality of output is not. A cheaper pipeline might produce worse results. The optimizer must actually run the pipeline and measure output quality.

Evidence-based optimization:

1. Sample real data from the dataset
2. Generate candidate pipeline plans (via 13 rewrite directives)
3. Run each candidate plan on the sample
4. Measure output quality using an LLM evaluator or ground truth labels
5. Select the plan with the highest measured accuracy

### Scope & Conditions

Necessary for:

- Any LLM pipeline where accuracy is the primary metric
- Tasks with ground truth labels or reliable quality metrics
- Scenarios where pipeline structure significantly affects output quality

Cost-based optimization suffices for:

- Tasks where approximate answers are acceptable
- Scenarios where you're willing to trade accuracy for speed/cost
- Highly constrained environments (tight latency budgets)

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "Unlike classical database optimizers that evaluate based on cost, DocETL's optimizer uses an evidence-based search. It samples real data, runs the generated pipeline plans, measures actual output quality using an LLM evaluator, and empirically chooses the most accurate pipeline" [11:05].

### Implications

- Computational overhead: Running candidate plans on sample data is expensive; the optimizer itself consumes tokens and time.
- Measurement fidelity: The quality metric must be reliable (ground truth is ideal; LLM evaluators introduce bias).
- Generalization risk: Optimization on sample data may not generalize to the full dataset.

### Related

- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]]—implements: evidence-based search is core to DocETL.
- [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]—motivation: cost-based optimization fails to improve accuracy.
- [[Model Self-Verification as a Secondary Quality Gate]]—related: LLM evaluators measure output quality.
- [[Structured Output Enforcement (JSON Schema and Function Calling)]]—related: structured output enables automated quality metrics.

### See Also

- [[SoT - Quality Metrics for LLM Pipelines]]

%%[supports:: [[DocETL Framework - Declarative Pipelines with Agentic Optimization]], strength=5, confidence=high]%%
