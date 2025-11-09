---
aliases: []
confidence: 
created: 2025-08-26T09:26:38Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [information]
title: "Shannon's Information Theory - Information as Uncertainty"
type:
uid: 
updated: 
version:
---

💡 In Claude Shannon's formal information theory, **information** is a measure of **uncertainty** or **surprise**. The information content of a message is quantified by how much it reduces the receiver's uncertainty.

Key principles:

1. **Information equals uncertainty**: The more unpredictable or surprising a message is, the more information it contains.
2. **Maximum randomness = maximum information**: A sequence with a uniform probability distribution (i.e., completely random) has the highest possible uncertainty and therefore the maximum information content, or **entropy**. The formula for entropy is $H(X)=−∑p(x)log2​p(x)$.
3. **Patterns reduce information**: Predictability, rules, and repetition introduce redundancy, which *decreases* the Shannon information content. A perfectly predictable message (e.g., "AAAAA") has zero entropy and contains no information in this technical sense.

This definition directly contradicts the common-sense notion of [[Information as Perceivable Pattern]].

- **Links**: [[The Conflict Between Semantic and Shannon Information]], [[Kolmogorov Complexity - Information as Compressibility]]
