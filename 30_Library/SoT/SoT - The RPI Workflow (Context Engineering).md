---
aliases: [Context Economics, Context Engineering Workflow, Research Plan Implement, Research-Plan-Implement Workflow, RPI Protocol]
conformant: false
created: 2026-01-09T21:52:07+00:00
modified: 2026-08-13T10:53:50+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-the-rpi-workflow-context-engineering
status: permanent
supersedes: ["[[Research-Plan-Implement Workflow]]"]
tags: [ai/architecture, mental-model, prodos, system/protocol, workflow]
title: SoT - The RPI Workflow (Context Engineering)
type: sot
---

## Minimum Viable Understanding (MVU)

Context Engineering is the discipline of optimising the Information Density fed into an LLM's context window. The RPI (Research, Plan, Implement) workflow is the operational framework for applying this discipline.

It treats the context window as a scarce resource (Context Economics) to prevent the model from entering the "Dumb Zone" (the degradation of reasoning capabilities when context > 40% or signal-to-noise ratio is low).

---

## 1. The Core Principles

### A. The "Smart Zone" vs. The "Dumb Zone"

- The Dumb Zone: Streaming raw files, entire folder structures, or "stream of consciousness" chat history into the context. This forces the model to spend compute on _retrieval_ rather than _reasoning_.
- The Smart Zone: Providing only the "Computed Truth" (compressed summaries, dependency maps, and specific logic). This frees up the model's "cognitive budget" for complex architectural tasks.

### B. Greenfield vs. Brownfield

- Greenfield (New Context): New features, notes, or ideas. These are easy for LLMs to generate.
- Brownfield (Existing Context): Your legacy codebase or existing Obsidian Vault. This is where LLMs fail. They hallucinate because they do not know the "Ground Truth".
- Rule: You must _Audit_ the Brownfield (Research) before you _Build_ the Greenfield (Implement).

---

## 2. The RPI Phases

### Phase 1: Research (The Audit)

- Goal: Establish Ground Truth. Stop the LLM from hallucinating variables, file paths, or existing knowledge.
- Mechanism: Use tools (`search_vault`, `grep`, `context-engine`) to map dependencies.
- Context Strategy: High Context / Read-Only.
- Output: A "Dependency Map" or "Gap Analysis". _No code or content is generated yet._
- Prompt Pattern:

 > "Audit the vault for existing notes on [Topic]. Map the conflict between Note A and Note B. Do not write the new note yet."

### Phase 2: Plan (Compression of Intent)

- Goal: Define the Architecture. Solve the logic errors _before_ they become syntax errors.
- Mechanism: Synthesise the Research into a strict Specification (Spec).
- Context Strategy: High Context (Research Output) + Reasoning.
- Output: A Markdown Specification (The "Plan").
    - For Code: A list of files to edit and the specific pseudo-code logic.
    - For Notes: A "Schema" (Header structure, Frontmatter tags) for the new Source of Truth.
- The Review Gate: This is the high-leverage human intervention point. Verify the plan before committing tokens to execution.

### Phase 3: Implement (Reliable Execution)

- Goal: High-Fidelity Generation and "Surgical" integration.
- Mechanism: Execute the Plan using specific "Write" tools.
- Context Strategy: Low Context (Stateless).
    - The model does not need the entire research history. It only needs: The Plan + The Specific Target File.
- Output: Production-ready Code or structured Markdown notes.

---

## 3. Operational Models

### Model A: Codebase Refactoring

1. Research: Map `variables.tf` (Consumer) vs `outputs.tf` (Producer) to find mismatches.
2. Plan: Write the `locals` block logic to bridge the gap. Simulate the `terraform plan`.
3. Implement: Generate the exact HCL syntax. Run `terraform validate`.

### Model B: Knowledge Management (Obsidian)

1. Research: `search_vault_smart` to find "Ghost Data" (buried mentions in Daily Notes) and "Clusters" (duplicate notes).
2. Plan: Design a `SoT` (Source of Truth) structure that merges the clusters. Define the `aliases` and `tags`.
3. Implement: Use `create_vault_file` to write the SoT, then `delete_vault_file` to remove the debt.

---

## 4. Context Caching (Advanced)

For massive contexts (e.g., full documentation sets or large codebases), use Context Caching (Google Gemini / Vertex AI).

- Freeze: Upload the "Research" context (Phase 1) to the server once.
- Query: Run the "Plan" (Phase 2) against the cached ID.
- Benefit: Reduces cost by ~90% and keeps the model in the Smart Zone by removing the tokenisation overhead from the active inference loop.

---

%%[implements:: [[SoT - Context Engineering]]]%%

See Also: [[SoT - Context Engineering]]
