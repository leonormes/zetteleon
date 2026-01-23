---
aliases: ["Continuous Vector Spaces", "Dense Vectors", "Semantic Similarity", "Vector Embeddings"]
confidence: "5/5"
created: 2026-01-09T21:53:52+00:00
epistemic: "Technical/Mechanical"
modified: 2026-01-23T18:09:16+00:00
purpose: "Defining the continuous representation of text in high-dimensional vector spaces. Covers the transition from discrete tokens to semantic vectors."
see_also: ["[[MOC - LLM-Augmented Thinking]]", "[[SoT - LLM Tokenization and Economics]]"]
status: "permanent"
tags: ["ai", "embeddings", "llm", "machine-learning", "vector-math"]
title: SoT - Word Embeddings and Vector Spaces
type: "SoT"
---

## SoT - Word Embeddings and Vector Spaces

### 1. Definitive Statement

> [!definition] Definition
> **Word Embeddings** are dense, low-dimensional numerical vectors that represent text in a continuous coordinate space. Unlike discrete token IDs, embeddings encode **semantic meaning** through spatial relationships: proximity in the vector space implies similarity in meaning.

---

### 2. The Representational Shift

The transition from discrete to continuous representation solves three critical limitations of traditional NLP:

1. **Ordinality:** Unlike assigning arbitrary integers (e.g., Good=1, Bad=500), embeddings represent semantic distance mathematically.
2. **Sparsity:** Replaces "One-Hot Encoding" (massive, mostly-zero matrices) with dense vectors (e.g., 300–1000 dimensions), which are computationally efficient.
3. **Semantic Arithmetic:** High-dimensional spaces allow for logical vector operations.
    - _Example:_ `Vector(King) - Vector(Man) + Vector(Woman) ≈ Vector(Queen)`.

---

### 3. Embedding Architectures

#### 3.1 Static Embeddings (Word2Vec)

- **CBOW (Continuous Bag of Words):** Predicts a target word based on its surrounding context.
- **Skip-gram:** Inverts CBOW; predicts the surrounding context from a single target word.
- _Limitation:_ Static. The word "bank" has the same vector regardless of whether the context is financial or geographical.

#### 3.2 Transformer-Based (Dynamic)

- **Trainable Lookup:** The embedding layer is a weight matrix that evolves during model training to optimize for specific tasks.
- **Contextualization:** Transformers use the **Attention Mechanism** to modify embedding vectors based on surrounding tokens, allowing for polysemy resolution.
- **Positional Encoding:** Since Transformers process tokens in parallel, a positional vector is added to the embedding to preserve sequence and word order.

---

### 4. Minimum Viable Understanding (MVU)

> [!check] The Core Logic
> **Spatial Proximity = Semantic Similarity.**
> In a well-trained embedding space, words with similar meanings "clump" together. This allows AI agents to perform **Semantic Search** (finding relevant context based on meaning rather than keyword matching).

---

### 5. Implementation Notes

- **Search:** Modern RAG (Retrieval-Augmented Generation) systems rely on "Embedding Models" (like `text-embedding-3-small`) to convert user queries into vectors for comparison against a vector database.
- **Context Engineering:** To prevent "Context Rot," ensure that the embedding model used for indexing documentation matches the model used for querying.
