---
created: 2026-04-10T13:00:00+00:00
modified: 2026-04-16T11:56:03+00:00
tags: [cosine-similarity, euclidean-distance, similarity-metrics, vector-math]
title: Vector Similarity Metrics Serve Different Retrieval Objectives
---

## Vector Similarity Metrics Serve Different Retrieval Objectives

Three primary distance measures determine similarity in vector space, each suited to a different retrieval objective: Euclidean distance measures the straight-line physical distance between points (preferred for clustering tasks); Dot product measures both direction and magnitude (preferred for recommendation systems where scale matters); Cosine similarity measures the angular relationship only, ignoring magnitude (preferred for orientation-based semantic matching such as text embeddings).

### Scope & Conditions

The correct metric must match the training objective of the embedding model being used—a model optimised with cosine similarity should be queried with cosine similarity. Switching metrics without retraining produces degraded retrieval. Performance and relevance vary significantly depending on the choice.

### Evidence

> "three primary ways to calculate similarity [11:42]: Euclidean Distance… Dot Product… Cosine Similarity"

### Implications

- Metric selection is an architectural decision, not a tuneable parameter; it must be locked in at collection creation time and aligned with the embedding model.
- Cosine similarity is most commonly appropriate for NLP embeddings because semantic direction (meaning) is more important than vector magnitude (frequency of occurrence).
