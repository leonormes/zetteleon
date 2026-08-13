---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-13T10:57:01+00:00
permalink: llmeon/30-library/100-zettelkasten/tri-partite-agent-memory-procedural-semantic-and-episodic
proposition: Autonomous agents require three distinct memory stores with different
  access patterns and retention policies. Procedural memory holds instructions (how-to
  guides). Semantic memory holds facts and context (via vector database + RAG). Episodic
  memory holds event logs. Each is optimized for different retrieval patterns and
  retention costs.
tags: [domain/llm, topic/agent-architecture, topic/memory-systems, topic/persistent-memory]
title: Tri-Partite Agent Memory - Procedural, Semantic, and Episodic
type: claim
---

## Tri-Partite Agent Memory - Procedural, Semantic, and Episodic

An agent with a single memory bank—"dump everything in a vector database"—will waste tokens retrieving irrelevant historical data and instructions. Production agent systems separate memory into three specialized stores:

### Procedural Memory (Skills)

- Content: Localized, instructional data (typically Markdown files)
- Retention: Long-term (rarely changes)
- Access: Retrieved when task requires specific skill or workflow
- Example: "How to File a Legal Brief," "Process a Customer Complaint"

### Semantic Memory (Knowledge Base)

- Content: Facts, business context, user profiles, domain knowledge
- Storage: Vector database (embeddings)
- Retrieval: Semantic search via RAG—inject relevant facts into prompt
- Retention: Medium to long-term; regularly updated
- Example: Product catalogs, regulatory summaries, customer profiles

### Episodic Memory (Event Log)

- Content: Chronological record of agent interactions, decisions, tool calls
- Storage: Time-indexed database
- Access: Mostly for logging and auditing; rarely queried directly
- Retention: Short-lived (routinely distilled into semantic memory)
- Example: Chat histories, API call logs, decision trees

### The Distillation Pattern

Problem: Episodic memory grows unbounded. Injecting full chat history into every prompt wastes tokens and exceeds context windows.

Solution: Periodically summarize episodic logs into semantic memory using a secondary, cheaper LLM:

- Secondary model reads episodic logs
- Extracts key facts, decisions, discovered patterns
- Writes summaries into semantic memory
- Primary agent never sees full episodic history; only the distilled facts

### Evidence

Source: "Loop Engineering | LLM". Quotes:

- Procedural: "Localized, instructional data (typically stored as Markdown files) that dictates exactly how an agent should behave" [26:27]
- Semantic: "A vector database storing durable facts, business context… selectively injected via RAG" [46:48]
- Episodic: "A chronological database logging chat histories and past data events" [48:40]
- Distillation: "Secondary, cheaper LLMs routinely summarize episodic logs and distill them into semantic memory" [50:43]

### Implications

- Cost optimization: Using cheaper models for distillation reduces token spend.
- Information fidelity: Summaries lose detail; summarization strategy affects what facts survive.
- Latency: Each distillation cycle adds latency; too-frequent cycles waste compute, too-infrequent cycles allow episodic memory to explode.

### Related

- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—analogous: memory outlives sessions.
- [[Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows]]—implements: semantic retrieval is selective; episodic is summarized.
- [[Context Window Limits Force Iterative Task Decomposition]]—solves: episodic distillation prevents context bloat.
- [[Retrieval-Augmented Generation (RAG)]]—implements: semantic memory + RAG integration.

### See Also

- [[SoT - Memory Systems in Autonomous Agents]]
- [[Episodic Memory Summarization Strategies]]

%%[implements:: [[Persistent Memory Layers Enable Multi-Session Agent Continuity]], strength=5, confidence=high]%%

%%[implements:: [[Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows]], strength=4, confidence=high]%%
