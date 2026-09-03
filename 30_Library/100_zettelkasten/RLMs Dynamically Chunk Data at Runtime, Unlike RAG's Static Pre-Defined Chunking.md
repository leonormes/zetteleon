---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:04+00:00
permalink: llmeon/30-library/100-zettelkasten/rlms-dynamically-chunk-data-at-runtime-unlike-rags-static-pre-defined-chunking
proposition: RAG systems chunk data using hardcoded rules decided in advance (e.g.
  fixed paragraph or character-count splits) and retrieve against those fixed chunks
  with a static query. Recursive Language Models instead chunk data dynamically at
  runtime — the model inspects the actual data through its REPL environment and decides
  on the fly how to slice it and how many Sub-LLM calls to spin up to process it,
  making the chunking strategy itself a runtime decision rather than a pre-defined
  rule.
tags: [domain/llm, topic/agent-architecture, topic/rag, topic/rlm]
title: "RLMs Dynamically Chunk Data at Runtime, Unlike RAG's Static Pre-Defined Chunking"
type: claim
---

## RLMs Dynamically Chunk Data at Runtime, Unlike RAG's Static Pre-Defined Chunking

RAG's chunking strategy is fixed before the query ever arrives: someone decides paragraphs, or 500-character windows, or some other rule, and every document gets sliced the same way regardless of what's actually in it. The retrieval step then matches a query against those pre-existing chunks—the chunk boundaries themselves are never reconsidered at query time.

An RLM inverts this: there is no pre-defined chunking rule at all. The model looks at the actual data through its REPL environment—its shape, its length, its structure—and decides, for this specific dataset and this specific task, how to slice it and how many Sub-LLM calls are warranted. A dataset of short uniform records might get sliced very differently than one of long variable-length records, and the model is the one making that call, informed by what it actually observes about the data rather than a rule written in advance of ever seeing it.

### Scope & Conditions

Applies to the comparison between RAG-style static chunking pipelines and RLM-style dynamic runtime chunking specifically. Both approaches remain valid architectural choices for different situations—RAG's static chunking is cheaper and more predictable; RLM's dynamic chunking trades that predictability for adaptiveness to the actual data at hand. This note does not claim one approach is universally superior.

### Evidence

Source: "From RLMs to Agent Harnesses" (Still Broken AI). "RAG uses hardcoded rules to chunk data (e.g., splitting by paragraphs or character counts) and retrieves them based on a static query" [35:18]. "RLMs do chunking dynamically. The model looks at the data through the REPL environment and decides on the fly how to slice the data and how many Sub-LLMs to spin up to process it" [35:27].

### Implications

- This is a genuinely new point of comparison in the vault's RAG coverage: neither [[Retrieval-Augmented Generation (RAG) Grounds LLM Outputs in External Knowledge]] nor [[Retrieval-Augmented Generation (RAG)]] addresses chunking staticness as a limitation—both focus on grounding and knowledge freshness. This note adds a distinct axis of critique: the rigidity of the chunking decision itself, independent of what's retrieved.
- It depends on the dispatch mechanism established elsewhere: the "how many Sub-LLMs to spin up" decision is only possible because of [[Root LLM Dispatches Generative Subtasks to Sub-LLMs via Code-Mediated Function Calls]]—dynamic chunking and dynamic dispatch are two faces of the same runtime-discretion capability.
- Dynamic chunking is not free: unlike RAG's fixed, cheap, predictable chunking, letting the model decide chunking strategy at runtime consumes additional reasoning (and therefore tokens/latency) before any actual task-processing begins—a cost/adaptiveness trade-off worth flagging explicitly rather than treating dynamic chunking as a strict improvement.

### Related

- [[Retrieval-Augmented Generation (RAG) Grounds LLM Outputs in External Knowledge]]—contrast: this note's critique targets chunking rigidity specifically, a dimension that note doesn't address.
- [[Retrieval-Augmented Generation (RAG)]]—contrast: same relationship.
- [[Root LLM Dispatches Generative Subtasks to Sub-LLMs via Code-Mediated Function Calls]]—depends_on: dynamic chunking is enabled by the same runtime-discretion mechanism that governs sub-LLM dispatch.
- [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]]—depends_on: the model can only inspect the data to decide chunking because the data is accessible in the environment in the first place.

### See Also

- [[RLMs Avoid Context Bloat by Storing Intermediate State as Symbolic Variables, Not Context Tokens]]

[depends_on:: [[Root LLM Dispatches Generative Subtasks to Sub-LLMs via Code-Mediated Function Calls]], strength=3, confidence=medium]
