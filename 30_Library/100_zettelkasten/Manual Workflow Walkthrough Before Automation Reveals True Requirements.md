---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:03+00:00
permalink: llmeon/30-library/100-zettelkasten/manual-workflow-walkthrough-before-automation-reveals-true-requirements
proposition: Before automating a desired workflow with agents, an engineer should
  manually walk through every node of that workflow themselves — by hand — to map
  out the exact conditions, information flows, and functions actually required. This
  "is a more reliable design process than trying to guess the automation's shape upfront"
  without having done the work manually first.
tags: [2, domain/llm, topic/agent-architecture, topic/best-practice, topic/workflow-design]
title: Manual Workflow Walkthrough Before Automation Reveals True Requirements
type: claim
---

## Manual Workflow Walkthrough Before Automation Reveals True Requirements

The instinct when automating a process is to design the automation directly: sketch out the agent's steps, the tools it'll call, the checks it'll run. This advice inverts that instinct—do the work by hand first, as if there were no agent involved at all, and pay attention to every decision point, every piece of information you reach for, and every function or check you find yourself performing along the way. That manual pass is what actually reveals the workflow's true shape: the conditions that need to be checked, the data that needs to flow between steps, and the functions that need to exist—information that's very easy to guess wrong when designing an automation abstractly.

This is essentially a "dogfooding before automating" discipline: you can't automate a process accurately if you don't yet know precisely what the process is, and the fastest way to find out precisely is to do it yourself.

### Scope & Conditions

Applies at the design stage of building a new agent workflow, before writing skills or agent prompts. Most valuable for workflows whose steps aren't already well-documented or well-understood—for a process the engineer already knows cold, the manual walkthrough may be quick, but the advice is to still do it rather than skip straight to automation design.

### Evidence

Source: "FORGET Loop Engineering. Agentic Engineering is about THIS" (IndyDevDan). Advice 2: "Do the Work Yourself First: Before automating, walk through every node of the desired workflow manually to map out the exact conditions, information flows, and functions required" [29:03].

### Implications

- It's a concrete methodology for avoiding overdelegation at the design stage: [[Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding]] describes the failure of handing an agent an ambiguous task; this note is a preventive practice—the manual walkthrough is what removes the ambiguity before the agent is ever involved.
- It complements small-skill design: [[Small Single-Purpose Agent Skills Outperform Monolithic Skill Design]] argues for small, separable skills; a manual walkthrough is exactly the process that reveals _where_ the natural seams for those small skills actually are, rather than guessing at a decomposition abstractly.

### Related

- [[Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding]]—supports: doing the work manually first is a direct preventive measure against overdelegating an under-specified task.
- [[Small Single-Purpose Agent Skills Outperform Monolithic Skill Design]]—related: both are practical design-discipline advice for building an AI Developer Workflow; the walkthrough informs where the skill boundaries should be drawn.
- [[AI-Synthesized Requirements Precede Code Generation in a Redesigned SDLC]]—tension worth noting: that note describes AI _synthesizing_ requirements ahead of code generation; this note argues the human should manually derive workflow requirements first—the two aren't strictly contradictory (one is about product requirements, one about automation-process requirements) but sit in some tension over where synthesis of "what's required" should originate.

### See Also

- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]

[supports:: [[Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding]], strength=3, confidence=medium]
