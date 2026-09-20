---
aliases: [Compounding Knowledge Base, LLM Wiki, Persistent Knowledge Architecture, RAG Limitation]
conformant: false
created: 2026-04-06T18:00:00+00:00
last-synthesis: 2026-04-06
modified: 2026-09-19T15:45:22+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-llm-wiki-pattern
source_of_truth: true
tags: [ai-engineering, architecture, knowledge-management, llm, rag, sot]
title: SoT - LLM Wiki Pattern
type: sot
---

## Minimum Viable Understanding (MVU)

Standard RAG is stateless: every query rediscovers knowledge from scratch, nothing accumulates, and there are no persistent cross-references. The LLM Wiki Pattern (attributed to Andrej Karpathy) flips this: the LLM _maintains_ a structured, interlinked wiki as a persistent middle layer between raw sources and queries. Knowledge compounds over time instead of being discarded after each session.

---

## Working Knowledge

### The Core Failure of Standard RAG

Standard RAG has a structural flaw: each query triggers a fresh retrieval cycle. There is no persistent understanding, no cross-referencing between retrieved fragments, and no mechanism for the system to "learn" from prior sessions. The AI must re-piece together the same relationships every time.

Symptoms of this failure:

- Repeated synthesis of identical connections across sessions
- No awareness of contradictions between source documents (discovered once, forgotten)
- Orphan knowledge: insights surface in chat but are never recorded

### The LLM Wiki Pattern

Instead of querying sources at runtime, the LLM is used to build and maintain a wiki upfront, incrementally, as new sources arrive. The wiki acts as a distilled, interlinked, human-navigable knowledge base that grows in fidelity over time.

Division of Labour:

- Human: Curates raw sources, asks insightful questions, directs analysis.
- LLM Agent: Handles all "grunt work"—writes summaries, maintains cross-references, flags contradictions, keeps the index current.

### The Three-Layer Architecture

| Layer | Owner | Rule |
|---|---|---|
| Raw Sources | Human | Immutable inputs (articles, papers, transcripts). LLM reads, never edits. |
| The Wiki | LLM | Directory of Markdown files (concept pages, entity pages, summaries). LLM owns entirely. |
| The Schema | Human | Config file (e.g., `claude.md`) defining conventions, structure, and style. Acts as the LLM's editorial policy. |

### The Three Core Operations

1. Ingest: New source dropped into the raw folder → LLM writes a summary page → automatically updates and cross-links all relevant existing wiki pages.
2. Query: Question answered by synthesising from the wiki. If external lookup is required, the new knowledge is filed back into the wiki as permanent pages—the act of answering _expands_ the knowledge base.
3. Lint: Maintenance pass across the entire wiki—identifies contradictions, stale claims, orphan pages without links, and knowledge gaps that need addressing.

### Four Design Principles

| Principle | Meaning |
|---|---|
| Explicit Knowledge | The wiki is navigable—you can see exactly what the AI "knows" and what it doesn't. No opaque vector stores or black-box memory. |
| Total Ownership | All files are local Markdown. No provider lock-in. |
| File Over App | Universal format—interoperable with any tool (Obsidian, grep, git). |
| Model Agnostic | Any LLM (Claude, GPT, local) can run the operations. The wiki outlives any specific model. |

---

## Current Understanding

### Structural Isomorphism with ProdOS

This vault _is_ an LLM Wiki Pattern implementation:

| LLM Wiki Layer | ProdOS Equivalent |
|---|---|
| Raw Sources | `00_Inbox/` capture, HEAD notes |
| The Wiki | `30_Library/SoT/`, `30_Library/100_zettelkasten/` |
| The Schema | `CLAUDE.md`, `GEMINI.md`, templates in `10_System/` |
| Ingest operation | Chronos Synthesis ritual (HEAD → SoT) |
| Query operation | Semantic search via MCP proxy → answer → update SoT |
| Lint operation | Knowledge Consolidation Agent protocol (deduplication, orphan detection) |

The "nothing accumulates" failure of standard RAG is precisely what ProdOS is designed to prevent via the HEAD→SoT synthesis pipeline.

### Relationship to Standard RAG

The LLM Wiki Pattern does not replace retrieval—it changes _when_ and _what_ is retrieved. Retrieval at query time still happens, but the target is the structured wiki (high signal, pre-synthesised) rather than raw source fragments (low signal, unprocessed). This is the distinction [[SoT - The RPI Workflow (Context Engineering)]] calls "Computed Truth" vs. raw context.

### Relationship to ML Agent Persistent Memory

[[SoT - ML Engineering for AI Agents]] describes the same pattern at the experiment level: an agent maintains a persistent "Experiment Log" and "Battle-Tested Defaults" across sessions. The LLM Wiki Pattern is the generalised architecture; persistent ML experiment memory is a domain-specific instance of it.

---

## Practical Application

### Minimum Setup (Any Repo or Project, not just This Vault)

1. Three folders/artefacts, not more: `raw/` (immutable inputs), `wiki/` (LLM-owned pages), and one schema file (`CLAUDE.md`, `AGENTS.md`, or equivalent) defining naming conventions, page skeleton, and cross-link syntax. Skipping the schema file is the most common failure—without it, every Ingest reinvents structure and pages stop being comparable.
2. Reuse one page skeleton for every wiki entry rather than inventing structure per-topic. This vault's own [[Template - SoT]] (MVU → Working Knowledge → Current Understanding → Tensions & Gaps → Related Knowledge) is a working instance—copy that shape rather than designing a new one from scratch.
3. Decide the granularity rule up front: one canonical page per concept/entity, never one page per source. A page-per-source wiki just recreates unprocessed fragments with extra steps and defeats the "high signal, pre-synthesised" property the whole pattern depends on (see [[#Relationship to Standard RAG]] above).

### Running the Three Operations, Concretely

| Operation | Generic mechanic | This vault's instance |
|---|---|---|
| Ingest | New source → agent drafts/updates the matching wiki page → agent cross-links it into neighbouring pages | [[Prompt - ProdOS Chronos Synthesizer]] (the Chronos ritual): HEAD note → SoT artefact |
| Query | Answer from the wiki first; only touch raw sources if the wiki doesn't cover it; if it didn't, file the new answer back as a permanent wiki page—don't let it evaporate in chat | Semantic search via the MCP proxy → answer → the answer gets written back into the relevant SoT/claim note, not left in scrollback |
| Lint | Sweep the wiki for orphan pages (no inbound links), contradictions, and stale claims | [[Knowledge Consolidation Agent]] (Triad discovery + dedup + typed edges) plus `edge_lint.py --audit` for structural validation ([[AGENTS.md]] §9.2) |

### Heuristics for the Open Questions Below

- Lint cadence: trigger-based beats calendar-based. Run a lint pass after every ~10 Ingests, or whenever the orphan-page ratio crosses ~5% of the wiki—whichever comes first. A fixed calendar cadence either fires when nothing changed (wasted pass) or misses a burst of ingestion (debt accumulates silently in between). These two numbers are starting points, not measured optima—recalibrate after a few cycles of real data.
- Write authority / hallucination risk: require every wiki claim to carry a traceable pointer back to the raw source it came from (this generalises the evidence requirement in [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]). An unsourced wiki claim is the highest-risk artefact in the system—flag it explicitly (this vault's mechanism: `conformant: false` + `non_conformance_reason`) rather than let it stand as trusted knowledge with no way to check it. Reserve a human review gate for exactly that case, not for every Ingest—gating everything reintroduces the friction the pattern exists to remove.

### Failure Modes to Watch For

- Wiki bloat—pages proliferate faster than links compound. Symptom: rising orphan-page ratio. Mitigation: the lint trigger above, and the one-page-per-concept granularity rule.
- Sync drift—a raw source is corrected or retracted after Ingest, but the wiki page built from it isn't updated, so the wiki now asserts something the raw layer no longer supports. Mitigation: raw sources stay immutable (Three-Layer Architecture above); a correction is a _new_ raw input that triggers a fresh Ingest, never a silent wiki edit with no paper trail back to why it changed.
- Summary-of-summary decay—re-synthesising an already-synthesised page (rather than going back to the original raw source) gradually drops nuance, hedges, and caveats each pass. Mitigation: Ingest should cite the original raw source when updating a page, not just the current wiki text.

### When It's Worth Setting Up

Worth it: recurring sessions over the same domain or corpus, sources arriving incrementally over weeks or months, and a real chance of asking overlapping questions more than once.

Not worth it: one-off Q&A over a static corpus, or a corpus small enough to fit entirely in context in one shot—the wiki-maintenance overhead (schema, linting, cross-referencing) has nothing to amortise against in a single session.

---

## Tensions & Gaps

- Lint cadence: partially resolved above with a trigger-based heuristic (N≈10 Ingests or 5% orphan ratio)—but those two numbers are unvalidated guesses, not measured thresholds. No data yet on whether they're too tight or too loose in practice.
- Write authority: Giving the LLM full ownership of the wiki layer creates a risk of confident hallucinations being permanently encoded. The source-citation requirement above (Practical Application) and a human review gate scoped to unsourced claims mitigate this but don't eliminate it—an LLM can still misread a correctly-cited source.

---

## Related Knowledge

- [[SoT - Agentic AI Design Patterns]]—RAG as a retrieval pattern; the LLM Wiki is its stateful evolution
- [[SoT - The RPI Workflow (Context Engineering)]]—"Computed Truth" as the right context strategy; the wiki is that computed truth made persistent
- [[SoT - Context Engineering]]—Signal density; the wiki maximises signal by pre-synthesising source material
- [[SoT - ML Engineering for AI Agents]]—Persistent memory / experiment log as a domain-specific instance
- [[10_System/prompts/Knowledge Consolidation Agent.md]]—The Lint operation formalised as an agent protocol
- [[Prompt - ProdOS Chronos Synthesizer]]—The Ingest operation formalised as an agent protocol (HEAD → SoT)
- [[Template - SoT]]—The page skeleton this pattern's wiki layer reuses per-concept
- [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—The source-citation discipline the Write Authority mitigation generalises from
- [[MOC - AI Software Engineering]]

## Tensions

### Long Context Vs Retrieval

The LLM Wiki Pattern rejects stateless RAG as structurally flawed. [[Retrieval-Augmented Generation (RAG)]] and the Qdrant notes treat retrieval as a working mechanism. The wiki pattern resolves this by changing _when_ and _what_ is retrieved—the target becomes the structured wiki (high signal, pre-synthesised) rather than raw source fragments—but both approaches still depend on the retrieval mechanism for the initial locate step.
