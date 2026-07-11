---
created: 2026-07-11T14:29:07+00:00
modified: 2026-07-11T14:29:10+00:00
title: Untitled
---

This is an exceptionally solid approach. The idea of using Typed Answer Contracts (TAC) is practically bulletproof for your use cases because it directly addresses the fundamental flaw of generative models: their infinite degrees of freedom. By treating LLM outputs as strict data extraction tasks rather than creative writing exercises, you eliminate the "hallucination camouflage" that text provides. Whether applied to a production RAG pipeline or your ProdOS Obsidian vault, enforcing a rigid schema ensures that if an LLM cannot definitively answer a prompt or properly format a note, it fails safely and predictably.

Here is a simplified, foundational Markdown wiki to establish the core concepts.

## Wiki: Typed Answer Contracts (TAC)

Typed Answer Contracts (TAC) structurally enforce how Large Language Models (LLMs) interact with your data. Instead of generating free-form prose, the LLM must populate a predefined, strictly typed schema (e.g., JSON or Pydantic).

### The Core Philosophy

- The Schema is the Rule: The LLM is no longer a creative writer; it is a deterministic data extractor.
- Binary Honesty: Ambiguity is eliminated by forcing the model to use programmatic booleans (like `missing_info` or `conformant`) instead of writing "I don't know"".
- Default to NOOP: If the LLM cannot perfectly fill out the required schema, the operation is flagged as false and the system does nothing.

### Why TAC is Necessary

- Standard RAG and unstructured prompts give models unlimited latitude to blend pre-trained knowledge with actual context.
- Fluent, free-form text hides false dates, fabricated clauses, and hallucinations in plain sight.
- Without machine-enforceable rules, LLMs operating on a knowledge vault will cause structural drift by ignoring naming conventions, missing metadata, and collapsing workflow stages.
- Downstream systems and automation cannot easily parse prose without relying on error-prone regex.

### Key Mechanics of a TAC System

- Evidence Enforcement: Schemas must include fields that force the model to provide exact source quotes, chunk IDs, or wikilinks to prove its output.
- Dry Runs by Default: In a read/write environment, all LLM actions default to `dry_run: True`. The LLM proposes a structural diff, which requires explicit human confirmation to execute.
- Workflow Gatekeeping: Progression through defined processes (like a Writing-to-Think pipeline) requires specific schema criteria to be met before the LLM can advance the state.
- Self-Assessment: The schema requires the model to actively self-diagnose its output via confidence scores and conflict flags.

### Implementation Contexts

|Feature|RAG Pipelines|ProdOS Vault Management|
|---|---|---|
|Primary Objective|Prevent factual hallucinations|Stop non-conformant file edits|
|Schema Output|Defined answers, confidence limits, and sources|Specific note types and frontmatter blocks|
|Failure State|`missing_info: True` blocks the user response|`conformant: false` halts the file write|
|System Benefit|Native, programmatic integration with downstream APIs|Maintains strict architecture like a Kubernetes manifest|

### Recommended Tooling Stack

- Libraries: Use `instructor` (Python) to wrap your LLM client, automatically enforcing Pydantic validation and managing retries.
- Self-Hosting: Utilize `vLLM` or `llama.cpp` for constrained decoding, which enforces JSON grammar at the token generation level.
- System Prompts: Explicitly instruct agents (like Hermes) to strictly output the requested JSON object and explicitly forbid prose modifications.
