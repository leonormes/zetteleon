---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-finding-thoughts
title: 2026-09-24-finding-thoughts
type: note
---

## Investigation and enrichment — [[Finding Thoughts]] — 2026-09-24

> Routed to [[Orphan Note Positioning & Thread Audit]] (a thin note with no inbound links from any note). Lexical search only (1MCP tools were unavailable).

### What the note catalogues

A first-person problem statement: "I don't know how to find things in obsidian... How do I continue from here and not just rewrite this same thought? This is a theme of my PKM." Its own answer, added later: come back through the main index and link things; it is very simple. It is an `axiom: true` claim (`epistemic_status: high`) that `supports` [[SoT - Evolutionary Note System]], and it had **no inbound links at all**, so nothing led back to the answer.

### Do you have answers elsewhere? Yes, for most of it

| Part of the question | Where the vault answers it |
|---|---|
| How do I find things? | [[Hub Notes Provide Entry Points to Idea Clusters]], [[Keyword Index Provides Sparse Entry Points]], [[Semantic Search via Embeddings]], [[Retrieval-Augmented Generation (RAG) Grounds LLM Outputs in External Knowledge]] |
| How do I continue without rewriting? | [[Linking as a Redundancy Reduction Strategy in Zettelkasten]] (the most direct: one canonical note per idea, link instead of restating), [[Key questions when linking notes in the Zettelkasten method]], [[Creating Meaningful Links]], [[Practice - Flat linking and tagging]], [[SoT - HEAD Note Contract (The Workbench)]], [[SoT - Evolutionary Note System]], [[Create a 'Research Hole' Parking Lot]] |
| Why is it a recurring theme? | [[My Main PKM Problem Is the Continuity of Thinking]] (the ADHD explanation), [[Zettelkasten Ain't Easy]], [[MOC - Project Continuity]], [[Documenting Mental Models Enables Project Re-entry]], [[Continuation Rituals Bridge Work Sessions for ADHD]], [[SoT - The Unified Writing to Think Process]], [[Stage 3 Understand (The Writing to Learn Layer)]] |

### Gaps in the vault

1. No note states the **human habit** "search the vault before writing a new note". The ingest prompts do it for agents.
2. No note explains **how to search inside Obsidian** itself.

Both are listed under "Not Yet Answered in the Vault" in the note.

### Changes

| File | Change |
|---|---|
| The note | `evidence_links` → the new Evidence note; new sections: **What the Vault Already Answers** (three sub-questions, 20 links), **Where It Applies in ProdOS** (5 prompts), **Not Yet Answered in the Vault**, **Further Reading** (3 books). Your prose and the existing `supports` edge are untouched |
| **New:** [[Evidence - Ahrens on Luhmann Overview Notes Reached From the Index as Entry Points Into a Topic]] | Verbatim quote from *How to Take Smart Notes* (Calibre 704). Confidence 0.6 |
| My Main PKM Problem Is the Continuity of Thinking | reciprocal bullet |
| Hub Notes Provide Entry Points to Idea Clusters | reciprocal bullet |

The Ahrens passage matches your own answer closely: overview notes are reached from the index and used as entry points, and links can be added to them over time.

### Judgement calls

- **No new typed edges.** Its existing `supports` edge is kept. A `supports` edge from an axiom would let your experience ground claims such as the redundancy note, which is more than a personal observation should carry.
- **`axiom: true` and `epistemic_status: high` left as they are.** The note is an axiom, so it does not need evidence, but the Evidence note now corroborates it. The note's "simplest" and "reliably" are stronger than the evidence, which the Evidence note says.
- **ProdOS links are to prompts**, since the vault's ProdOS machinery for this problem is the ingest and linking prompts, not a protocol.

### Left alone

`Zettelkasten Ain't Easy` is `type: permanent`; I did not retype it or add a link from it.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)`. Resolver: 0 unresolved links in the note and the Evidence note.
