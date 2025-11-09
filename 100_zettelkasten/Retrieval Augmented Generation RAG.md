---
aliases: []
confidence: 
created: 2025-10-10T08:29:35Z
epistemic: 
id: 20251008_Retrieval_Augmented_Generation_RAG
last_reviewed: 
modified: 2025-10-29T19:28:02Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Retrieval Augmented Generation RAG
type:
uid: 
updated: 
version:
---

**Retrieval-Augmented Generation (RAG)** is a [[Context Engineering for LLMs]] technique where an LLM's internal knowledge is supplemented with external, just-in-time information. Instead of relying solely on its training data, the system first retrieves relevant data chunks from a knowledge source (like a vector database) based on the user's query. This retrieved data is then injected into the context window along with the original prompt, grounding the LLM's response in factual, up-to-date information.

RAG is highly effective for tasks requiring deep knowledge of specific documents, such as Q&A over a large dataset.

**Links:**

- [[Context Engineering for LLMs]]
