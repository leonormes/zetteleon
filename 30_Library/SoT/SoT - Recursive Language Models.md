---
aliases: [Agentic REPL, RLM]
created: 2026-01-31T00:00:00+00:00
last_reviewed: null
modified: 2026-07-04T10:50:51+00:00
permalink: llmeon/30-library/so-t/so-t-recursive-language-models
status: evergreen
tags: [agents, architecture, research, rlm]
title: SoT - Recursive Language Models
type: SoT
updated: null
---

## The Core Problem: Context Rot & Complexity

"Context Rot" is not just about document length; it is about Task Complexity.

Complex documents (codebases, legal contracts) are not linear stories. They have high internal self-reference (functions calling functions, clauses referencing clauses).

### Failure of Current Methods

1. Context Stuffing: Simply adding more text to the prompt leads to performance deterioration (Attention Dilution) and higher costs.
2. Summarisation: This is "lossy"; vital context is often discarded, causing the agent to drift off-task.
3. RAG (Retrieval Augmented Generation): Good for simple Q&A, but brittle for multi-hop reasoning because it relies on semantic similarity rather than logical relationships.

## The Solution: Recursive Language Models (RLMs)

The solution involves using a REPL (Read-Evaluate-Print Loop) environment combined with Recursion.

How it works: Instead of feeding the text directly into the model, the document/codebase is assigned to a variable or accessible via a tool. The AI then uses code execution to:

1. Read: Access specific parts of the data.
2. Evaluate: Perform functions on the data (e.g., keyword match, slice, AST lookup).
3. Print: Return the result to the loop.
4. Recursion: The model can "hand off" sub-tasks or query itself, effectively creating a dependency graph of information.

## New Mental Model: Dependency Graphs

Stop treating complex data as a linear book. Model it as a dependency graph:

- Nodes: Functions, Classes, Clauses.
- Edges: Calls, Imports, References.

This allows the agent to "intelligently search" and traverse the structure.

## Operational Implementation: The Agentic Loop

To implement this, one must move from a "Linear Reader" architecture to a "Recursive Agent" architecture.

Linear (Old):

1. Scan files.
2. Dump everything into `CONTEXT.md`.
3. LLM reads huge file -> Guesses Plan.

Recursive (New):

1. Agent receives Task.
2. Agent starts with Zero Context.
3. Loop:
    - _Thought:_ "I need to find class X."
    - _Action:_ `Scout.lookup("X")`
    - _Observation:_ "X is in file Y."
    - _Thought:_ "I need to see who calls X."
    - _Action:_ `Scout.refs("X")`
    - …
4. Agent synthesizes Plan.

This shifts the computational load from "Memory" (Context Window) to "Compute" (Reasoning Loop).
