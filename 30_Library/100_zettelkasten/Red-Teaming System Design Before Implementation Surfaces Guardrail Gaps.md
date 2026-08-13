---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:51+00:00
permalink: llmeon/30-library/100-zettelkasten/red-teaming-system-design-before-implementation-surfaces-guardrail-gaps
tags: [domain/llm, topic/architecture-pattern, topic/pkm, topic/safety, topic/verification]
title: Red-Teaming System Design Before Implementation Surfaces Guardrail Gaps
type: claim
---

## Red-Teaming System Design Before Implementation Surfaces Guardrail Gaps

Most adversarial review happens after code exists: a second model or human reviews the implementation for flaws. Red-teaming the _plan_ moves this earlier—before a single file is created, an AI is prompted to attack the proposed design: "How would you exfiltrate the sensitive data this system is supposed to protect? Where are the gaps in this privacy boundary?"

This surfaces structural weaknesses (missing tombstones, overly broad canary triggers, unclear ownership boundaries between layers) while they are cheap to fix—before they're baked into folder structure, file conventions, and running automation.

### Scope & Conditions

Most valuable for:

- Systems with a security or privacy dimension (personal knowledge vaults with sensitive data, agent harnesses with tool access)
- Architecture decisions that are expensive to reverse once implemented (folder structure, access control conventions)
- Situations where the designer's own blind spots are the primary risk (a single person designing their own guardrails)

Less critical for:

- Low-stakes systems with no sensitive data or irreversible actions
- Designs already reviewed by an independent human with security expertise

### Evidence

Source: "I Built Karpathy's LLM Wiki in Claude Code (No Vector DB)" (Achuth G. Ramesh). Quote: "The creator used AI as a critic to attack and find flaws in the system's plan before actually implementing it" [05:40].

### Distinction from Code-Level Adversarial Auditing

This extends the pattern already established for reviewing generated code to the design/planning phase. The mechanism is the same (independent adversarial LLM catches blind spots the generating perspective misses), but the object under attack is a plan or architecture rather than a code diff.

### Implications

- Cheaper fixes: A gap found in the design phase costs a sentence edit; the same gap found post-implementation costs a refactor.
- Requires explicit adversarial framing: A model asked "does this look okay?" tends toward agreement; a model asked "how would you break this?" produces useful attack surfaces.
- Single-designer risk mitigation: For solo builders (no team review), this is one of few available mechanisms to catch blind spots before shipping.

### Related

- [[Cross-Model Adversarial Auditing Uses an Independent LLM to Catch Blind Spots]]—extends: same adversarial mechanism, applied one phase earlier (design vs. code).
- [[Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents]]—context: red-teaming is how gaps in the tombstone/canary design would be found before implementation.
- [[Mandatory Manual Code Review Before Deployment]]—complementary: red-teaming the plan and reviewing the code are both quality gates at different phases.

### See Also

- [[SoT - LLM Wiki Pattern]]

%%[extends:: [[Cross-Model Adversarial Auditing Uses an Independent LLM to Catch Blind Spots]], strength=3, confidence=medium]%%
