---
aliases: []
created: 2025-08-26T09:26:38Z
last_reviewed: ""
modified: 2026-04-22T20:59:44+00:00
status: ""
tags: ["information"]
title: "Shannon's Information Theory - Information as Uncertainty"
type: ""
updated: 
---

💡 In Claude Shannon's formal information theory, information is a measure of uncertainty or surprise. The information content of a message is quantified by how much it reduces the receiver's uncertainty.

Key principles:

1. Information equals uncertainty: The more unpredictable or surprising a message is, the more information it contains.
2. Maximum randomness = maximum information: A sequence with a uniform probability distribution (i.e., completely random) has the highest possible uncertainty and therefore the maximum information content, or entropy. The formula for entropy is $H(X)=−∑p(x)log2​p(x)$.
3. Patterns reduce information: Predictability, rules, and repetition introduce redundancy, which _decreases_ the Shannon information content. A perfectly predictable message (e.g., "AAAAA") has zero entropy and contains no information in this technical sense.

This definition directly contradicts the common-sense notion of [[Information as Perceivable Pattern]].

- Links: [[The Conflict Between Semantic and Shannon Information]], [[Kolmogorov Complexity - Information as Compressibility]]

## Critique: "Shannon's Information Theory - Information as Uncertainty"

### 1. Frontmatter Issues (mechanical)

- Empty strings vs bare `null`: `last_reviewed: ""`, `status: ""`, `type: ""`—better than the previous note's `"null"` string, but still populated. If these are meant to be absent, use bare `null` or omit the keys. Dataview will treat empty strings as non-empty values in some comparisons.
- `modified` / `updated` duplication—same issue as the other note. Pick one. You have `updated:` (bare empty) and `modified: 2026-02-01…` side by side.
- Tags are anaemic: `["information"]` alone is too flat. Compare with the other note's `TheHuman/Psychology` hierarchy. Candidates: `mathematics/information-theory`, `epistemology`, `concepts/counterintuitive`. Pick a tagging convention and apply it across your vault.
- Title/filename mismatch: filename has `Shannon_s_Information_Theory_-_Information_as_Uncertainty` (underscore-apostrophe, hyphen-colon). The frontmatter title should almost certainly be `Shannon's Information Theory: Information as Uncertainty` (proper colon), not an em-dash substitute.

### 2. Technical Issues (substantive—this is the Important section)

The note commits several small-but-meaningful conflations that a permanent note on this topic needs to resolve.

#### 2a. "Information Equals uncertainty" is Sloppy Shorthand

Shannon's framework distinguishes at least three quantities the note is treating as one:

| Quantity | Symbol | What it measures |
|---|---|---|
| Self-information (surprisal) | $I(x) = -\log_2 p(x)$ | Information content of one specific outcome |
| Entropy | $H(X) = \mathbb{E}[I(x)]$ | _Expected_ surprisal of a source/distribution |
| Mutual information | $I(X;Y)$ | _Reduction_ in uncertainty about $X$ given $Y$ |

The opening sentence says "information is a measure of uncertainty" and the next says it's quantified by "how much it reduces the receiver's uncertainty." Those are two _different_ quantities (entropy vs mutual information). The note treats them as the same thing.

#### 2b. "Maximum Randomness = Maximum information" Needs a Constraint

Entropy is maximised by the uniform distribution _relative to a given support_. A uniform distribution over {A, B} has H = 1 bit; over 256 symbols, H = 8 bits. There is no absolute "maximum information"—it scales with the alphabet size (or, in the continuous case, the known moments—see Jaynes's _maximum entropy principle_). The note presents max entropy as an absolute ceiling.

#### 2c. The "AAAAA Has Zero entropy" Example is the Crux Misconception

This is the most important issue. Shannon entropy is a property of distributions, not of strings.

- If the source only ever emits A (i.e. $P(A)=1$), then yes, $H=0$.
- But "AAAAA" _as a string_ doesn't have Shannon entropy at all. The string has a _Kolmogorov complexity_ (algorithmic information), which is what your `[[Kolmogorov Complexity]]` link is actually about.

The note slides between source-level entropy ("a perfectly predictable message") and string-level compressibility without flagging the jump. This is _exactly_ the distinction that makes the Kolmogorov link valuable—but the note treats them as the same concept.

#### 2d. LaTeX Formatting is Broken

`$H(X)=−∑p(x)log2p(x)$` has:

- A Unicode minus (−) and Unicode summation (∑) instead of `\sum`.
- An invisible zero-width space () between `log2` and `p(x)`.
- `log2` rendered as inline rather than `\log_2`.

Correct form:

$$
H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)
$$

This matters because Obsidian's MathJax will render this inconsistently and it won't search cleanly.

#### 2e. "Directly contradicts" Is Too Strong

The final sentence says Shannon's definition "directly contradicts" the common-sense notion of information as pattern. It doesn't—it _abstracts away_ from meaning. Shannon explicitly wrote in the 1948 paper that "these semantic aspects of communication are irrelevant to the engineering problem." The two notions measure orthogonal things (syntactic surprisal vs semantic pattern-recognition). They coexist; they don't contradict. The link `[[The Conflict Between Semantic and Shannon Information]]` suggests you know this—so "contradicts" is the wrong verb here.

### 3. Zettelkasten-specific Issues

- Better linking than the previous note—three outbound links, thematically coherent. Good.
- Missing structural links that would sharpen the note:
  - `[[Self-Information vs Entropy]]`—resolves issue 2a.
  - `[[Maximum Entropy Principle]]` (Jaynes)—resolves issue 2b.
  - `[[Redundancy in Communication]]`—the note mentions redundancy but doesn't link it.
  - `[[Channel Capacity]]`—the receiver-centric framing invites this.
- The 💡 emoji adds no information content (apt, given the topic). Fleeting-note vestige.
- Better atomicity than the ambiguity note. This one genuinely defends its title—it doesn't just restate it. The three numbered principles actually work.

### 4. What's Good

- Real engagement with the idea, not just assertion. The numbered principles earn the title.
- Concrete example ("AAAAA")—even though it's slightly misused, it makes the idea tangible.
- Identifies the counterintuitive core explicitly, which is the whole point of a permanent note on a technical concept.
- Outbound links are well-chosen conceptually, even if more could be added.
- "Information as Perceivable Pattern" link is a genuinely useful contrast node to have in the vault.

---

### Concrete next Actions

Pick one.

1. Fix the LaTeX (2 min). Replace the broken formula with:

```
$$H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)$$
```

   Lowest activation energy. Immediate visible win.

2. Weaken "directly contradicts" to "abstracts away from" (1 min). One-word fix that makes the note technically defensible instead of technically wrong.
3. Add a one-line clarification on entropy-vs-string (5 min). After the "AAAAA" sentence, add: _"Note: Shannon entropy is a property of the source distribution, not of individual strings—string-level information content is better captured by [[Kolmogorov Complexity]]."_ This resolves the 2c confusion and earns the existing Kolmogorov link.

If you only do one, do #3—it's the conceptual fix that upgrades the note from "popular-science summary" to "correctly-scoped permanent note," and it activates a link you've already committed to.
