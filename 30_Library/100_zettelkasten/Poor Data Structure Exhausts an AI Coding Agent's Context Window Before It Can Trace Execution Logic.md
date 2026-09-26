---
conformant: true
contradicts: []
created: 2026-09-19T00:00:00+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-25T16:29:29+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/poor-data-structure-exhausts-an-ai-coding-agents-context-window-before-it-can-trace-execution-logic-1
proposition: When a codebase relies heavily on control flow, shared mutable state, and deep inheritance, an LLM coding agent must read across dozens of files to reconstruct the implicit state and branching before it can safely modify the code, and often exhausts its context window before doing so, producing plausible but incorrect edits; smart data structures, small modules, and explicit interfaces keep the same reasoning within budget.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [ai-code-generation, context-window, llm-agents, software-architecture]
title: "Poor Data Structure Exhausts an AI Coding Agent's Context Window Before It Can Trace Execution Logic"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Poor Data Structure Exhausts an AI Coding Agent's Context Window Before It Can Trace Execution Logic

When a codebase relies heavily on control flow, shared mutable state, and deep inheritance, its logic is diffuse across many files, so an LLM coding agent must read across dozens of files to reconstruct the implicit state and branching before it can safely modify the code—and often exhausts its context window before doing so, producing plausible but incorrect edits; smart data structures, small modules, and explicit interfaces keep the same reasoning within budget.

### Scope & Conditions

Applies specifically to LLM-based code-generation/editing agents operating under a fixed context-window budget.

### Evidence

> "An AI model attempting to understand a deeply nested, procedural architecture must read across dozens of files and thousands of lines of code to track the implicit state and scattered conditional branching. Because the structural representation is poor, the AI exhausts its context window before it can grasp the full execution path, resulting in plausible but dangerously incorrect code generation."

### Implications

- Gives "data dominates" a new, LLM-era justification distinct from the original human-cognition and CPU-cache arguments: it is also what keeps a system inside an agent's context budget.

### Related

- [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]]—direct concept match: makes the near-identical argument explicitly under the same "complexity conservation" framing ("providing an LLM with raw, unstructured code forces it to reconstruct the underlying data model mentally while simultaneously trying to solve the problem… this 'double burden' leads to Hallucination… Context Rot").
