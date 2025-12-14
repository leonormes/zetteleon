---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/569f1f831e92"
author:
  - "[[Gemini]]"
published:
created: 2025-12-14
description: "Created with Gemini"
tags:
  - "clippings"
---
Https://youtube.com/watch?v=hVM8qGRTaOA&si=Vmophf1rHhegwmn7

Analyse this video. Summarise the claims and give me actions or small experiments that prove or demonstrate the claims

This analysis is structured around the core principles of text representation in machine learning, prioritising the underlying logic and framework of Word Embeddings as the definitive solution to the limitations of earlier methods.

The video, **"What Are Word Embeddings?"** by Under The Hood, introduces the need for robust text vectorisation in Natural Language Processing (NLP) models, contrasting simple and sparse methods with the density and semantic richness of word embeddings.

### I. Conceptual Framework and Core Claims

The video presents the evolution of text representation methods as a progression of increasingly sophisticated approaches, each designed to overcome a fatal flaw in its predecessor.

| Framework | Claim (Why it Fails or Succeeds) | Underlying Logic (The 'How') |
| --- | --- | --- |
| **Simple Token Numbers** | **Fails to capture meaning.** It imposes an arbitrary ordinal scale on words. \[[01:12](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=72)\] | Numbers are only suitable for ordinal features (where ranking matters). Proximity in numerical space does not equal proximity in semantic space, leading to misinterpretation of relationships. |
| **One-Hot Encoding (OHE)** | **Fails in efficiency and depth.** It resolves the ordinal issue but is resource-intensive and treats words as isolated entities. \[[03:01](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=181)\] | Each word is represented by a unique, highly sparse vector (size = total vocabulary). This is memory-intensive and computationally expensive (the "Curse of Dimensionality"). It cannot capture semantic relationships (e.g., 'good' and 'great' are similar). |
| **Bag-of-Words (BoW) & N-grams** | **Fails in scaling and semantic breadth.** It captures local context but results in sparse, large vectors for extensive datasets. \[[04:17](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=257)\] | This method counts word/phrase occurrences (unigrams, bigrams, etc.). It is still prone to the curse of dimensionality and cannot capture deeper meanings or long-range dependencies required for advanced NLP tasks. |
| **Word Embeddings (Dense Vectors)** | **Succeeds by encoding meaning and context.** It is an efficient, low-dimensional, and semantically rich representation. \[[06:30](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=390)\] | Words are represented as **dense numerical vectors** in a continuous vector space. The key principle is: **semantic similarity** translates to **vector proximity**, and **relationships** are encoded in **vector direction**. |
| **Positional Encoding** | **Succeeds by preserving sequence.** It overcomes the inherent limitation of parallel processing in Transformer architectures. \[[17:24](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=1044)\] | A positional vector is mathematically added to the word's semantic embedding vector, ensuring the model knows the order of tokens, which is crucial for contextual understanding. |

### II. Demonstrative Actions and Experiments

The claims of the video can be demonstrated through small experiments that isolate and prove the core principles of failure (in the case of earlier methods) or success (in the case of embeddings).

#### A. Demonstrating the Failure of Simple Token Assignment (Claim 1)

**Objective:** To show that numerical proximity does not equate to semantic similarity.

**Experiment: Ordinal Similarity Test**

1. **Define a Set:** Select the words: 'Good' (positive), 'Bad' (negative), and 'Great' (strong positive).
2. **Assign Arbitrary Tokens:** Arbitrarily assign unique numerical tokens, ensuring the semantically unrelated pair is numerically close:
	- Good = 6
	- Bad = 22
	- Great = 21
3. **Action & Observation:**
	- *Semantic Relationship:* 'Good' and 'Great' are semantically closest.
	- *Numerical Relationship:* 'Bad' (22) and 'Great' (21) are numerically closest.
4. **Proof:** The numerical representation (22 and 21) incorrectly suggests 'Bad' and 'Great' are similar, thereby proving the video's assertion that simple tokenisation leads to misrepresentation of word relationships \[[02:01](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=121)\].

#### B. Demonstrating the Semantic Power of Word Embeddings (Claim 4)

**Objective:** To prove that vector space direction encodes meaning, allowing for algebraic analogies.

**Experiment: Vector Analogy Test**

1. **Requirement:** Access a pre-trained word embedding model (e.g., Word2Vec, GloVe).
2. **Action (Vector Arithmetic):** Perform the famous analogy subtraction and addition:
3. **Demonstration & Proof:** Query the model to find the word vector in its vocabulary that has the highest **cosine similarity** to the resulting vector . The model's returned word should be 'Queen'. This demonstrates the fundamental principle that the *difference* vector between 'King' and 'Man' (which encodes 'Royalty') is maintained and transferred when added to the vector for 'Woman' \[[07:51](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=471)\].

#### C. Demonstrating the Clustering Principle (Claim 4)

**Objective:** To prove that semantically similar words are physically closer in the embedding space.

**Experiment: Semantic Proximity Test**

1. **Requirement:** Use the same pre-trained word embedding model.
2. **Action (Similarity Calculation):**
	- Select a seed word, e.g., 'tennis'.
	- Calculate the **Cosine Similarity** score between and:
		- **Related Words:** 'racket', 'court', 'serve'
		- **Unrelated Words:** 'mountain', 'butter', 'cloud'
3. **Demonstration & Proof:** The scores for the related words will be significantly closer to 1 (high similarity), while the scores for the unrelated words will be closer to 0 or negative. This physically demonstrates the claim that the embedding technique clusters similar words together in the n-dimensional space \[[10:03](http://www.youtube.com/watch?v=hVM8qGRTaOA&t=603)\].

Google Account

Leon Ormes

leonormes@gmail.com