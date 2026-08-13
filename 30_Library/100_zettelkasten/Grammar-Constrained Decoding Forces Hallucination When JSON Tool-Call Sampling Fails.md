---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:55:11+00:00
permalink: llmeon/30-library/100-zettelkasten/grammar-constrained-decoding-forces-hallucination-when-json-tool-call-sampling-fails
tags: [domain/llm, topic/llm-behavior, topic/reliability, topic/structured-outputs, topic/tool-use]
title: Grammar-Constrained Decoding Forces Hallucination When JSON Tool-Call Sampling Fails
  Fails
type: claim
---

## Grammar-Constrained Decoding Forces Hallucination When JSON Tool-Call Sampling Fails

Structured output enforcement (grammar-constrained decoding) guarantees the model's output parses as valid JSON—but it guarantees syntactic validity, not semantic correctness. If the model samples a token that puts it in an awkward grammatical position (for example, a comma implying another key-value pair is coming), the constrained decoder has no path back to a clean stop: it must produce _something_ syntactically valid next, which can mean inventing a plausible-sounding key that was never intended.

The result is a hallucinated field inserted purely to satisfy the grammar, not because the model "decided" to add it. That hallucinated content is now part of the context window for every subsequent turn, and it can break later edits that reference the (fabricated) structure.

### Scope & Conditions

Applies to tool-calling architectures that enforce JSON grammar constraints on decoding (a common structured-output technique). The failure is a regression risk specifically in newer models/harness combinations where this interaction hasn't been fully hardened—the presenter frames it as an observed regression, not a universal property of grammar-constrained decoding.

### Evidence

Source: "State of Agentic Coding, episode 8, with Mario, Armin, and Ben" (Armin Ronacher). Mario's account: "a highly technical regression where newer models get trapped by grammar-constrained decoding when outputting JSON for tool calls. If a model incorrectly samples a comma, it is forced to hallucinate a new key to satisfy the JSON grammar, poisoning the context window and breaking subsequent edits" [26:32].

### Implications

- Structured output enforcement is necessary but not sufficient: [[Structured Output Enforcement (JSON Schema and Function Calling)]] prevents conversational filler and malformed structure, but this failure mode shows syntactic validity can still mask semantic corruption.
- Context poisoning compounds silently: unlike a rejected malformed output (which triggers visible retry logic), a grammatically-valid-but-hallucinated key passes structural validation and only surfaces as a downstream edit failure.
- A narrow single-token sampling error has an outsized blast radius: because [[Auto-Regressive Generation Reprocesses the Entire Context on Every Token]], one bad comma early in a tool call's JSON propagates through every subsequent generation step in that context.

### Related

- [[Structured Output Enforcement (JSON Schema and Function Calling)]]—tension: this is a specific failure mode inside a system that structured-output enforcement is supposed to make reliable.
- [[LLM Hallucinations Arise from Probabilistic Prediction Without External Grounding]]—instance: this is a narrow, mechanistic case of hallucination—driven by grammar-constraint pressure rather than knowledge gaps.
- [[Error Handling and Retry Pipelines for LLM Failures]]—related: detecting this failure mode requires validating _semantic_ plausibility of tool-call fields, not just schema conformance, before accepting output.
- [[Auto-Regressive Generation Reprocesses the Entire Context on Every Token]]—depends_on: explains why a single early sampling error compounds across the rest of the generation.

### See Also

- [[Model Self-Verification as a Secondary Quality Gate]]

%%[depends_on:: [[Auto-Regressive Generation Reprocesses the Entire Context on Every Token]], strength=3, confidence=medium]%%

%%[supports:: [[LLM Hallucinations Arise from Probabilistic Prediction Without External Grounding]], strength=3, confidence=medium]%%
