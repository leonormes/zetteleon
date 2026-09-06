---
axiom: true
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:06+00:00
permalink: llmeon/30-library/100-zettelkasten/systematic-ai-clarifying-questions-surface-edge-cases-during-planning
proposition: A planning step where the AI asks a battery of systematic clarifying
  'questions (e.g. "can the start and end date be the same?", "are partial selections'
  'valid?", "should users be able to clear the date?") surfaces edge cases a human'
  "wouldn't enumerate alone. This planning step only has value if the human deeply"
  "engages with and answers the questions themselves, rather than accepting the AI's"
  own suggested answers by default — accepting every suggestion negates the point
  of the exercise.
tags: [domain/llm, topic/requirements-elicitation, topic/workflow-design]
title: Systematic AI Clarifying Questions Surface Edge Cases During Planning
type: claim
---

## Systematic AI Clarifying Questions Surface Edge Cases During Planning

The value of this step is specifically in the interrogation, not in any answers the AI itself proposes. A planning-mode AI asking "can the start and end date be the same?" forces the human to actually decide something they might otherwise have left implicit until it broke in production. The list of questions an AI can generate this way is long and genuinely useful—humans cannot reliably enumerate every edge case for a moderately complex feature unassisted—but the mechanism only works if the human treats each question as a real decision to make, not a checkbox to wave through.

This can be made more aggressive deliberately: pairing the planning step with a dedicated "ask more, harder questions" instruction increases the volume and difficulty of edge cases surfaced, at the cost of a longer planning phase.

### Scope & Conditions

Most valuable for features with real edge-case surface area (state combinations, boundary conditions, ambiguous user intents)—trivial or fully-specified tasks gain little from a full interrogation pass. Requires the human to actually engage with each question rather than rubber-stamping AI-suggested defaults, or the step becomes theater rather than genuine requirements elicitation.

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "Planning helps you get closer to that ideal, though, by asking all of the questions that you would need to answer yourself along the way if you were to build this out by hand: Can the start and end date be the same? Are partial selections valid? Should users be able to clear the date?… This planning step is critical. The point is not for you to just accept every suggestion from the AI. If you do that, you are negating the value of this planning process. The point is for you to deeply engage with the problem and guide the model."

### Implications

- This is a sibling elicitation mechanism to the vault's new prototype-variation note, from the same source: [[AI-Generated Prototype Variations Reveal Requirements Nuances Before Implementation]] surfaces nuances through seeing candidate outputs; this note surfaces them through being asked direct questions—the two are complementary phases of a single requirements-elicitation workflow (prototype first, then interrogate).
- It shares the same failure mode as other human-in-the-loop mechanisms in this vault: [[Approval Fatigue Undermines the Safety Value of Human-in-the-Loop Review]] describes how repeated rubber-stamping degrades an approval gate's value; this note's caution against "just accept every suggestion from the AI" is the same failure mode applied to a planning/questioning gate rather than a final-approval gate.
- It's a concrete instance of the general requirements-synthesis principle already in the vault: [[AI-Synthesized Requirements Precede Code Generation in a Redesigned SDLC]] establishes AI-assisted requirements synthesis as part of a redesigned SDLC; this note supplies a specific mechanism (systematic clarifying questions) for how that synthesis can be elicited interactively rather than from a static document.

### Related

- [[AI-Generated Prototype Variations Reveal Requirements Nuances Before Implementation]]—related: complementary elicitation mechanism from the same source and workflow.
- [[Approval Fatigue Undermines the Safety Value of Human-in-the-Loop Review]]—related: shares the same underlying failure mode (rubber-stamping AI output defeats the mechanism's purpose), applied to a different stage of the workflow.
- [[AI-Synthesized Requirements Precede Code Generation in a Redesigned SDLC]]—supports: a concrete elicitation mechanism for that note's general requirements-synthesis claim.

### See Also

- [[Transparent Harness-Level Model Tiering Requires No User Configuration]]

[supports:: [[AI-Synthesized Requirements Precede Code Generation in a Redesigned SDLC]], strength=3, confidence=medium]
