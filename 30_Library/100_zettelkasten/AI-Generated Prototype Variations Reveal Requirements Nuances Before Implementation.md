---
created: 2026-07-28T10:24:46+00:00
modified: 2026-08-08T10:29:14+00:00
permalink: llmeon/30-library/100-zettelkasten/ai-generated-prototype-variations-reveal-requirements-nuances-before-implementation
title: AI-Generated Prototype Variations Reveal Requirements Nuances Before Implementation
---

---

created: 2026-07-28T00:00:00+00:00
modified: 2026-07-28T00:00:00+00:00
title: AI-Generated Prototype Variations Reveal Requirements Nuances Before Implementation
type: claim
epistemic_status: medium
tags: [domain/llm, topic/workflow-design, topic/requirements-elicitation]
proposition: Generating many quick, low-effort prototype variations with an LLM (e.g. "give me 20 mocks for a date picker, put them in one HTML file") surfaces design and requirement nuances that wouldn't otherwise be considered—because humans process sensory-rich, tangible layouts faster than dense text. This applies beyond visual UI: generating a diagram comparing several implementation approaches for a non-visual task (e.g. an API endpoint) serves the same purpose, letting requirements and constraints become visible before any implementation code is written.
---

## AI-Generated Prototype Variations Reveal Requirements Nuances Before Implementation

The mechanism here is reaction, not derivation: rather than the human enumerating requirements from scratch, the AI generates a spread of concrete variations, and the human's job is to look at them and notice what they like, dislike, or hadn't considered. Seeing one candidate that starts a date picker at the year view (rather than the day view) prompts a requirement ("I want zoom in/out between years, months, and days") that likely wouldn't have surfaced from describing the component in prose alone. The claim generalizes past visual components: generating a diagram comparing five different ways to implement an API endpoint serves the same function for a non-visual design decision—making trade-offs visible and comparable before committing engineering effort to one.

The underlying rationale given is perceptual: humans process sensory-rich, tangible representations (images, shapes, laid-out options) faster than they process the equivalent information in dense prose, so low-effort AI-generated prototypes are a faster nuance-discovery mechanism than describing requirements in text.

### Scope & Conditions

Most valuable early in a task, before a plan or implementation has been committed to, and specifically for decisions with a meaningful design or approach space (multiple genuinely different ways to build the thing). A task with only one reasonable approach gains little from generating variations.

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "Let's say we want to build a date picker web component… Start with a simple prototype and get several variations… one of them is a mock where it starts with the year view. That's interesting… As humans, we process sensory-rich models like images, shapes, and tangible layouts much faster than dense text. Creating low-effort prototypes early on helps make complex concepts immediately intuitive. And this applies to non-visual tasks as well. For instance, if I want to add a new API endpoint, I'll still create a visual prototype to understand the requirements and constraints before diving into the implementation."

### Implications

- This is a distinct requirements-elicitation mechanism from the vault's existing manual-walkthrough note: [[Manual Workflow Walkthrough Before Automation Reveals True Requirements]] has the human derive requirements by doing the work themselves by hand; this note has the AI generate candidate variations for the human to react to—reaction is a lower-effort, faster elicitation mode than derivation, though it may surface a different (narrower, more surface-level) set of nuances.
- It pairs naturally with the vault's existing systematic-questioning elicitation mechanism: [[Systematic AI Clarifying Questions Surface Edge Cases During Planning]] is a second, complementary AI-driven elicitation mechanism from the same source—prototyping surfaces nuances the human notices by seeing, questioning surfaces nuances the human answers when asked directly.
- It's a concrete instance of "do the work yourself first" applied to AI rather than the human: where [[Manual Workflow Walkthrough Before Automation Reveals True Requirements]] has the human prototype the process manually, this note has the AI prototype the output—both share the underlying principle that concrete artifacts reveal what abstract description hides, just with different labor allocated to producing the artifact.

### Related

- [[Manual Workflow Walkthrough Before Automation Reveals True Requirements]]—contrast: human-derives-by-hand vs. this note's AI-generates-for-human-reaction.
- [[Systematic AI Clarifying Questions Surface Edge Cases During Planning]]—related: a complementary, sibling elicitation mechanism from the same source.
- [[AI-Synthesized Requirements Precede Code Generation in a Redesigned SDLC]]—related: both concern AI assisting with requirements before implementation, though that note synthesizes requirements from existing stakeholder text rather than generating novel candidate variations.

### See Also

- [[Prompt Cache Discounts Reward Staying on the Same Model and Reasoning Level Within a Task]]

%%[extends:: [[Manual Workflow Walkthrough Before Automation Reveals True Requirements]], strength=3, confidence=medium]%%
