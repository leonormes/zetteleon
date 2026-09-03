---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:35:58+00:00
permalink: llmeon/30-library/100-zettelkasten/auto-regressive-generation-reprocesses-the-entire-context-on-every-token
proposition: LLMs generate text auto-regressively, predicting one token at a time.
  Because each new token depends on everything before it, the entire input—user query,
  system prompt, and all previously generated output—is fed back through the model
  to predict the next single token. This is the root mechanism behind LLM token cost,
  not an implementation inefficiency layered on top.
tags: [domain/llm, topic/architecture, topic/cost-optimization, topic/llm-behavior, topic/tokenization]
title: Auto-Regressive Generation Reprocesses the Entire Context on Every Token
type: claim
---

## Auto-Regressive Generation Reprocesses the Entire Context on Every Token

A token is a whole word, a word-piece, or a character (space, punctuation, symbol)—the model's tokenizer maps roughly 100,000 possible tokens, with common words typically mapping to a single token and rarer constructs splitting into several. Tokens become embeddings—mathematical vectors—before the model processes them.

The cost driver is not tokenization itself but what happens _between_ tokens. An LLM predicts the next token from everything that came before it. To predict token N+1, the model reprocesses tokens 1 through N in full. Every single new word requires feeding the growing input back through the entire model.

This means a conversation that has produced 500 tokens of output has, cumulatively, reprocessed far more than 500 tokens of input—each of the 500 generation steps re-ran the model over an input that was one token shorter than the step after it.

### Scope & Conditions

Applies to standard auto-regressive transformer decoding (the architecture underlying essentially all current commercial LLMs). Techniques like KV-caching mitigate the _recomputation_ cost within a single generation but do not eliminate the fundamental scaling: longer context still costs more per step regardless of caching strategy.

### Evidence

Source: "Why AI Tokens are so Expensive" (Computerphile). Quote: "LLMs are auto-regressive, meaning they predict the very next token based on everything that came before it… every time the model predicts a new token, the entire input… is fed back into the model to predict the subsequent one. This means the input context continually grows with every new word, driving up computational and electrical costs significantly" [04:22–05:23].

### Implications

- Cost is structural, not incidental: This isn't a bug that better engineering fixes—it's the mechanism by which auto-regressive models work at all.
- Every mitigation (RAG, structured output, selective retrieval, context caching) is ultimately fighting this one constraint: reduce what has to be reprocessed, because reprocessing is unavoidable for whatever remains.
- Linear conversation growth produces superlinear cost: a conversation twice as long is not twice as expensive; the compounding reprocessing makes cost growth worse than linear in practice.

### Related

- [[Context Volume Plateau]]—related: describes a _quality_ consequence (reasoning degrades past 50% context); this note describes the _cost_ mechanism driving the same underlying growth.
- [[Context Caching Freezes Large Static Datasets for Efficient Inference]]—mitigates: caching avoids re-tokenizing static content, directly targeting this reprocessing cost.
- [[Continuous Autonomous Agent Loops Incur Significant API Cost]]—grounds: this note explains the mechanism behind the dollar figures that claim states.
- [[Agentic Tool Calls Compound Context Growth Multiplicatively]]—extends: applies this mechanism specifically to tool-calling agent loops.

### See Also

- [[SoT - Context Engineering]]

[supports:: [[Continuous Autonomous Agent Loops Incur Significant API Cost]], strength=4, confidence=high]

[supports:: [[Context Volume Plateau]], strength=3, confidence=medium]
