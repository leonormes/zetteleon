---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-07-28T09:12:54+00:00
permalink: llmeon/30-library/100-zettelkasten/ai-speedup-confined-to-the-build-phase-is-absorbed-by-surrounding-sdlc-bottlenecks
proposition: The traditional SDLC (Requirements → Design → Build → Test → Release
  → Operate) contains substantial human waiting time between stages. Applying AI acceleration
  only to the Build (coding) phase does not translate into overall productivity gains,
  "because the surrounding stages' friction absorbs the time saved. Productivity gains"
  require redesigning the whole pipeline around AI, not just speeding up one stage
  of an unchanged pipeline.
tags: [domain/llm, topic/productivity, topic/sdlc, topic/software-engineering, topic/systems-thinking]
title: AI Speedup Confined to the Build Phase Is Absorbed by Surrounding SDLC Bottlenecks
type: claim
---

## AI Speedup Confined to the Build Phase Is Absorbed by Surrounding SDLC Bottlenecks

A team adopts an AI coding assistant. Code gets written faster. Yet the team's overall delivery speed barely improves. The reason: coding was never the bottleneck in the first place.

The traditional SDLC—Requirements, Design, Build, Test, Release, Operate—is full of human-to-human waiting: developers waiting on product teams for clarity, QA waiting on developers to finish a build, release waiting on sign-offs. If AI only accelerates the Build stage, the saved time simply shows up as _more waiting_ at the next handoff, because Requirements, Test, Release, and Operate are still running at their pre-AI pace.

This is a specific instance of theory-of-constraints reasoning: optimizing a non-bottleneck stage does not improve system throughput.

### Scope & Conditions

Applies to any organization treating "give developers an AI coding tool" as a complete productivity strategy. The effect is strongest in teams with heavy cross-functional handoffs (product → engineering → QA → release management) and weakest in small, tightly-integrated teams where handoff friction was already low.

### Evidence

Source: "AI in the SDLC: Rethinking AI Coding Tools & AI Agents" (IBM Technology). Quote: "The traditional SDLC… involves massive amounts of human waiting… When AI is used purely to speed up the 'Build' (coding) phase, those gains are absorbed by the friction in the surrounding stages" [00:16–02:22].

### Implications

- Local optimization is a trap: teams measuring "lines of code per hour" or "PRs merged" as a productivity proxy will see gains that don't propagate to actual delivery speed.
- The redesign must be pipeline-wide: AI applied to Requirements synthesis, Test generation, and Deployment automation is what converts Build-phase speedup into real throughput gains.
- Organizational bottlenecks are often non-technical: sign-off processes, stakeholder availability, and review queues can dominate delivery time regardless of how fast code gets written.

### Related

- [[Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers]]—related: both describe a mismatch between "more code, faster" and actual organizational value.
- [[Shift to Architectural Oversight]]—context: as Build-phase friction drops, the argument for redirecting human effort toward judgment and oversight (across the whole pipeline, not just code) strengthens.
- [[Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding]]—related: both are failure patterns from applying AI narrowly rather than redesigning the workflow around it.

### See Also

- [[SoT - Flow Engineering]]

%%[supports:: [[Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers]], strength=3, confidence=medium]%%
