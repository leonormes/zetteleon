---
aliases: [6 Dimensions of Code Understanding, AI Code Quality Framework, Structural vs Causal Code]
created: 2026-01-30T07:55:00+00:00
modified: 2026-07-04T10:51:01+00:00
permalink: llmeon/30-library/so-t/so-t-dimensions-of-code-understanding
tags: [code-quality, framework, llm-evaluation, software-architecture]
title: SoT - Dimensions of Code Understanding
---

## Dimensions of Code Understanding

True "understanding" in AI Coding Agents is not defined by syntax recall or pass/fail on unit tests. It is defined by the ability to navigate six distinct cognitive dimensions. To generate non-parochial code, an LLM must satisfy the following:

### The 6-Dimensional Framework

| Dimension | Question | Definition | Success Criteria |
|:--- |:--- |:--- |:--- |
| 1. Structural | Where? | Spatial awareness of the code's location within the module, layer, and service hierarchy. | Adherence to [[Separation of Concerns]]. No leaky abstractions. |
| 2. Causal | So What? | Simulation of 2nd and 3rd order effects. Counterfactual reasoning ("If I remove this check, what breaks downstream?"). | Low [[SoT - Temporal Projection|Blast Radius]]. Prediction of side effects. |
| 3. Idiomatic | How? | Adherence to the project's specific "dialect" (e.g., [[SoT - Data-Oriented Design|Data-Oriented Design]]) rather than generic textbook patterns. | Consistency with existing code style and patterns. |
| 4. Constraint | What Not? | Awareness of the "Negative Space"—what is forbidden (e.g., circular dependencies, raw SQL in views). | Zero violation of architectural invariants. |
| 5. Intent | Why? | Alignment with the user's _actual_ problem, not just the literal text of the prompt. | Solving the root cause, not just the symptom. |
| 6. Temporal | When? | Prediction of future friction. How easy will this code be to change in 6 months? | High maintainability. Low [[SoT - Temporal Projection|Blast Radius]]. |

### Measuring Understanding: Behavioral vs. Declarative

We must reject Declarative Recall (the ability to restate definitions or explain code) as a metric for understanding. Understanding is a Behavioral Outcome.

| Metric Type | Definition | Why it Fails/Succeeds |
|:--- |:--- |:--- |
| Declarative (Recall) | Restating facts, summarizing notes, or reproducing comments. | NOISE. LLMs are excellent at "hallucinating" understanding by repeating definitions without applying them. |
| Behavioral (Audit) | The fitness, coherence, and architectural alignment of generated code. | SIGNAL. High-quality output is the only verifiable proof of architectural grounding. |

#### The Behavioral Audit Criteria

- Temporal Projection: Does this code survive the next feature request?
- Coupling Awareness: Does it respect the [[SoT - Parochial Code|Parochial Barrier]]?
- Negative Capability: Did the agent refuse to write code that violates a constraint?

---

See Also: [[SoT - Parochial Code]], [[SoT - Macro-Micro Unification]], [[SoT - Temporal Projection]]
