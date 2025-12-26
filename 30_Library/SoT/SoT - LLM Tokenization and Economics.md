---
aliases: ["Tokenization", "LLM Tokens", "LLM Economics", "Encoding and Decoding"]
confidence: "5/5"
created: 2025-12-26T15:00:00Z
epistemic: "Technical/Mechanical"
last_reviewed: "2025-12-26"
modified: 2025-12-26T10:27:28+00:00
purpose: "Defining the fundamental unit of LLM processing: the Token. Covers architectural trade-offs, encoding/decoding, and economic implications."
review_interval: "6 months"
see_also: ["[[MOC - LLM-Augmented Thinking]]", "[[SoT - ProdOS Cognitive Architecture (Obsidian + Gemini)]]"]
source_of_truth: ["[[LLM Tokens The Core Concept]]"]
status: "stable"
tags: ["ai", "llm", "architecture", "economics", "tokenization"]
title: SoT - LLM Tokenization and Economics
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Tokens** are the fundamental unit of Large Language Models (LLMs). They serve as the intermediary "currency" between human-readable text and the numeric vectors (embeddings) processed by the model's neural network.

## 2. The Tokenization Mechanism

LLMs do not "read" text character-by-character or word-by-word. They process a sequence of **Token IDs**.

1. **Encoding:** Input text is split into chunks (sub-words, words, or characters) based on the model's pre-defined **Vocabulary**. Each chunk is mapped to a unique integer ID.
2. **Processing:** The model's transformer architecture performs high-dimensional vector math on these numeric IDs.
3. **Decoding:** The resulting numeric IDs are mapped back to text chunks and concatenated to form the final output.

## 3. Architectural Trade-offs: Vocabulary Size

The efficiency of an LLM is heavily dictated by its **Vocabulary Size** (the number of unique tokens it recognizes).

- **Small Vocabulary:**
    - *Pros:* Requires less memory to store the embedding matrix.
    - *Cons:* Breaks words into more tokens (e.g., "understanding" becomes `un`+`der`+`stand`+`ing`). This increases the "Context Window" usage and compute cost per word.
- **Large Vocabulary:**
    - *Pros:* Represents complex concepts or long words in fewer tokens (e.g., "understanding" becomes 1-2 tokens). Higher throughput and lower cost per word.
    - *Cons:* Requires a larger model die/memory footprint to store the lookup table.

## 4. Economic Implications (The Currency)

Tokens are the primary billing unit for LLM APIs (OpenAI, Anthropic, Google).

- **Variable Pricing:** Input tokens (context) and output tokens (generation) often have different price points.
- **Context Window:** Every model has a hard limit on the total number of tokens (Input + Output) it can process in a single "glance."
- **Data Scarcity:** Rare words, specific code syntaxes, or low-resource languages are broken into smaller fragments, making them more "expensive" to process than common English text.

## 5. Minimum Viable Understanding (MVU)

> [!check] The Core Logic
> **Tokens are the bridge between strings and math.**
> Efficient AI engineering requires managing **Token Density**—the amount of information conveyed per token. Large vocabularies increase density but demand more powerful hardware.

## 6. Implementation Notes

- **Tooling:** Use libraries like `tiktoken` (OpenAI) or `js-tiktoken` (TypeScript) to count tokens locally before sending requests to manage costs and context limits.
- **Preference:** While Python is the standard for *training* models, **TypeScript** is increasingly preferred for *building* AI-augmented applications due to its superior asynchronous handling and integration with modern web stacks.
