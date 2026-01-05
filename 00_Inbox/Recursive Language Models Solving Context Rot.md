---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/38adad67f95a"
author:
  - "[[Gemini]]"
published:
created: 2026-01-05
description: "Created with Gemini"
tags:
  - "input"
---
https://youtu.be/mtRJmIup3b8?si=QJ2I5zoPNXbUZubC

This video explores a new MIT research paper introducing **Recursive Language Models (RLM)**, a neuro-symbolic inference strategy designed to overcome "context rot" and the failure of traditional transformer architectures in complex reasoning tasks over long contexts.

### The Problem: Context Rot and Phase Transitions

Standard Large Language Models (LLMs) suffer from a "phase transition" where reasoning capabilities degrade as context length increases \[[01:07](http://www.youtube.com/watch?v=mtRJmIup3b8&t=67)\].

- **Needle-in-a-Haystack (O(1) Complexity):** Models perform well at finding single facts even in massive contexts \[[04:35](http://www.youtube.com/watch?v=mtRJmIup3b8&t=275)\].
- **Reasoning Complexity (O(n) to O(n²)):** Performance collapses on tasks requiring cross-referencing or summarising across the entire dataset (e.g., "find all pairs of users with a specific trait") \[[05:38](http://www.youtube.com/watch?v=mtRJmIup3b8&t=338)\].
- **Failure Threshold:** GPT-5 performance reportedly drops significantly at 16k tokens for complex logic and reaches near-zero at 33k tokens for quadratic tasks \[[06:38](http://www.youtube.com/watch?v=mtRJmIup3b8&t=398)\].

### The RLM Framework: A Neuro-Symbolic Approach

RLM shifts the paradigm from treating a prompt as a neural input to treating it as an **external environment** \[[09:18](http://www.youtube.com/watch?v=mtRJmIup3b8&t=558)\]. The system functions like a computer's operating system using virtual memory \[[10:47](http://www.youtube.com/watch?v=mtRJmIup3b8&t=647)\].

**Core Components:**

1. **Environment:** The prompt is loaded as a string variable in a Python REPL (Read-Eval-Print Loop) \[[13:02](http://www.youtube.com/watch?v=mtRJmIup3b8&t=782)\].
2. **Interface:** The LLM is given a system prompt allowing it to interact with the context via symbolic code and a specific function: `lm_query` \[[13:24](http://www.youtube.com/watch?v=mtRJmIup3b8&t=804)\].
3. **The Recursive Trajectory:**
	- **Probing:** The LLM writes Python (regex/slicing) to inspect the data structure \[[13:38](http://www.youtube.com/watch?v=mtRJmIup3b8&t=818)\].
	- **Decomposition:** The model generates code loops to iterate over defined context chunks \[[14:15](http://www.youtube.com/watch?v=mtRJmIup3b8&t=855)\].
	- **Recursion:** Within the loop, the model spawns "child" LLM instances to process specific snippets \[[14:23](http://www.youtube.com/watch?v=mtRJmIup3b8&t=863)\].
	- **Aggregation:** The "root" model synthesises the returned sub-results into a final answer \[[14:45](http://www.youtube.com/watch?v=mtRJmIup3b8&t=885)\].

### Performance and Cost-Efficiency

RLM allows LLMs to effectively handle context windows of **1 million to 10 million tokens** \[[01:23](http://www.youtube.com/watch?v=mtRJmIup3b8&t=83)\].

- **Effectiveness:** In tasks where a baseline model scores 0.04%, the RLM wrapper can achieve 58% \[[15:22](http://www.youtube.com/watch?v=mtRJmIup3b8&t=922)\].
- **Cost Trade-off:** While the cost per query may double (e.g., from $0.16 to $0.33), the jump in reasoning capability is non-linear and massive \[[16:43](http://www.youtube.com/watch?v=mtRJmIup3b8&t=1003)\].

### Philosophical Shift: Probabilistic vs Deterministic

The video posits that **Attention is not all you need** for global reasoning \[[24:02](http://www.youtube.com/watch?v=mtRJmIup3b8&t=1442)\].

- **RAG (Retrieval-Augmented Generation):** Probabilistic and often lossy; relies on vector search "hoping" to find the right data \[[27:37](http://www.youtube.com/watch?v=mtRJmIup3b8&t=1657)\].
- **RLM:** Deterministic and exhaustive; uses symbolic code to guarantee 100% data coverage via programmatic iteration \[[12:40](http://www.youtube.com/watch?v=mtRJmIup3b8&t=760)\].

**Conclusion:** Neural networks are viewed as insufficient for precise, large-scale reasoning without a **symbolic exoskeleton** to support them \[[30:10](http://www.youtube.com/watch?v=mtRJmIup3b8&t=1810)\]. The LLM's role evolves from a primary "reasoner" to a "linguistic architect" that orchestrates deterministic code execution \[[25:21](http://www.youtube.com/watch?v=mtRJmIup3b8&t=1521)\].

**Video URL:**[https://www.youtube.com/watch?v=mtRJmIup3b8](http://www.youtube.com/watch?v=mtRJmIup3b8)

Google Account

Leon Ormes

leonormes@gmail.com