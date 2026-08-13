---
created: 2026-07-28T09:03:46+00:00
modified: 2026-08-13T10:54:50+00:00
permalink: llmeon/30-library/100-zettelkasten/overdelegation-and-underdelegation-are-symmetric-failure-modes-in-ai-assisted-coding
title: Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding
---

---

created: 2026-07-28T00:00:00+00:00
modified: 2026-07-28T00:00:00+00:00
title: Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding
type: claim
epistemic_status: high
tags: [domain/llm, topic/software-engineering, topic/agent-architecture, topic/delegation, topic/vibe-coding]
proposition: Teams applying AI to coding tend to fail at one of two extremes. Overdelegation hands the model a large, ambiguous task, letting it make unstated design decisions humans then struggle to review. Underdelegation restricts AI to small, isolated functions while a senior developer retains all architectural planning, capping productivity gains at the ceiling of manual thinking. Both extremes fail to find the effective middle: AI handling well-specified units of work within a human-set architecture.
---

## Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding

Two opposite mistakes produce the same disappointing result: no real productivity gain.

Overdelegation: a frontier model is asked to "build an e-commerce platform." It generates thousands of lines of code, making dozens of unstated design decisions along the way (data model shape, error handling conventions, dependency choices). A human reviewer now faces a wall of code they didn't design and must reverse-engineer the model's implicit decisions before they can trust or maintain it. Review becomes slower than the original coding would have been.

Underdelegation: a senior developer does 100% of the architectural planning and task breakdown, handing the model only small, isolated functions to implement. The code produced is good—but the intellectual heavy lifting (the part that actually determines quality and maintainability) remains entirely human. AI's contribution is capped at typing speed, not judgment.

The pattern is symmetric: overdelegation gives away too much judgment; underdelegation gives away none. Both waste the model's actual comparative advantage.

### Scope & Conditions

Applies to teams and individuals adopting AI-assisted coding without an explicit theory of what to delegate. The failure modes are not about model capability—they recur across model generations because they are workflow-design failures, not capability gaps.

### Evidence

Source: "AI in the SDLC: Rethinking AI Coding Tools & AI Agents" (IBM Technology). Quotes:

- Overdelegation: "Asking a frontier model to complete a massive, ambiguous project… The model makes unstated design decisions and generates thousands of lines of code that humans struggle to review" [02:47]
- Underdelegation: "A senior developer handles 100% of the architectural planning and task breakdown, only using AI to write small, isolated functions… the intellectual heavy lifting remains entirely human, capping productivity" [03:56]

### Implications

- The productive middle requires explicit specification: neither extreme works; the effective pattern hands AI well-scoped, clearly-specified units of work within an architecture a human has already set.
- Review cost is the hidden tax of overdelegation: code that took the model 30 minutes to write can take a human hours to safely review if it's carrying undocumented design decisions.
- Underdelegation is invisible waste: unlike overdelegation, it produces no obvious failure—just a permanently capped ceiling that looks like "AI just isn't that useful for our codebase."

### Related

- [[LLM Architectural Judgment Gap]]—grounds: overdelegation fails specifically because agents lack the architectural judgment the task requires.
- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]—instance: vibe coding is a specific case of overdelegation applied to entire applications.
- [[Shift to Architectural Oversight]]—resolves: the productive middle is precisely "human retains architectural oversight, AI executes well-specified units"—this note names the two ways teams miss that target.
- [[AI Speedup Confined to the Build Phase Is Absorbed by Surrounding SDLC Bottlenecks]]—related: both are failure patterns from narrow or miscalibrated AI application rather than considered workflow redesign.

### See Also

- [[Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing]]

%%[extends:: [[LLM Architectural Judgment Gap]], strength=4, confidence=high]%%

%%[supports:: [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]], strength=3, confidence=medium]%%
