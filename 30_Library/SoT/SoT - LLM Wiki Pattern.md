---
aliases:
- Compounding Knowledge Base
- LLM Wiki
- Persistent Knowledge Architecture
- RAG Limitation
created: 2026-04-06 19:00:00+01:00
last-synthesis: 2026-04-06
modified: 2026-05-26 11:44:19+00:00
source_of_truth: true
status: stable
synthesis-count: 1
tags:
- ai-engineering
- architecture
- knowledge-management
- llm
- rag
- sot
title: SoT - LLM Wiki Pattern
trust-level: stable
type: SoT
permalink: llmeon/30-library/so-t/so-t-llm-wiki-pattern
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

## Tensions & Gaps

- Lint cadence: How often should the lint operation run? Too frequent adds overhead; too infrequent allows debt to accumulate. No formalised heuristic yet.
- Write authority: Giving the LLM full ownership of the wiki layer creates a risk of confident hallucinations being permanently encoded. The Schema/style-guide layer partially mitigates this but doesn't eliminate it. Human review gates on Ingest would add fidelity at the cost of friction.

---

## Related Knowledge

- [[SoT - Agentic AI Design Patterns]]—RAG as a retrieval pattern; the LLM Wiki is its stateful evolution
- [[SoT - The RPI Workflow (Context Engineering)]]—"Computed Truth" as the right context strategy; the wiki is that computed truth made persistent
- [[SoT - Context Engineering]]—Signal density; the wiki maximises signal by pre-synthesising source material
- [[SoT - ML Engineering for AI Agents]]—Persistent memory / experiment log as a domain-specific instance
- [[10_System/prompts/Knowledge Consolidation Agent.md]]—The Lint operation formalised as an agent protocol
- [[MOC - AI Software Engineering]]