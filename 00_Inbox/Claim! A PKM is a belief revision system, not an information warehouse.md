---
tags:
  - Claim
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-04T10:33:39+00:00
---
# Claim: A PKM is a belief revision system, not an information warehouse

This is a genuinely good definition. It captures something your stated goal ("I am trying to define my thinking... overcome writer's block..
The second is harder. The second is also what makes a PKM worth maintaining for decades.

[Proposition-centred, not proposition-only.md](Proposition-centred,%20not%20proposition-only.md)

[Practice! Capture What Changed My Thinking.md](Practice!%20Capture%20What%20Changed%20My%20Thinking.md)

[Minimal note template with falsifier.md](Minimal%20note%20template%20with%20falsifier.md)

---

## What the Note Gets Wrong (or Oversimplifies)

### 2\. The critique of "topic buckets" is overcorrected

The note says "topic notes should mostly become maps or indexes, not the core content." Mostly true — but it is stated with more confidence than warranted.

There is a legitimate category the note misses: **reference cards**. Not every useful note has to be an arguable claim. Sometimes you genuinely do want a card that says "TCP is connection-oriented, UDP is connectionless" — because you will look it up twice a year and typing it once beats re-Googling.

The correct taxonomy would add:

- **Reference** — a stable definitional card. Not arguable, not a belief. Just a lookup.

Reference cards are fine provided they are (a) clearly labelled as reference, (b) kept few, and (c) not mistaken for thinking. The note's blanket dismissal is too absolute.

### 3\. "A PKM is a belief revision system" is a slogan, not a theorem

It is a *good* slogan. But the note states it with more confidence than it has earned. A PKM can *also* be:

- A scratchpad for writing

- A memory aid for procedural knowledge

- A project management substrate

- A reading log

- A reflection / journal space

These are not beliefs to be revised. The "belief revision system" framing is a useful *emphasis*, not an *exhaustive description*. Treat it as the centre of gravity, not the whole planet.

### 4\. The note does exactly what it warns against

Look at this passage:

> *Packet capture is often the fastest way to collapse uncertainty in network debugging* *Most "network problems" in distributed systems are actually naming, timeout, or policy problems*

These are presented as example *claims you might hold* — but notice how they arrive. They are **asserted with no evidence, no falsifier, no source**. They are the exact "slogans, not beliefs" failure mode the note warns against. The note is modelling bad claim-cards whilst advocating for good claim-cards.

This is not a fatal flaw — they are examples, not claims the note is making. But it is worth noting: *the presentation of a claim is not the same as the claim being rigorous*. A belief-revision PKM has to actually contain the revision structure, not just claim-shaped strings.

[Practice! The Epistemic Status Ladder.md](Practice!%20The%20Epistemic%20Status%20Ladder.md)

### 6\. No mention of the aging problem

The note talks about "how beliefs change over time" but gives no mechanism for tracking that change. This is the single biggest blind spot.

From the JTB card we built: **the dated position field**. Every claim should have a timestamped trail of your position on it. Not just the current confidence — the *diff*. The note misses this entirely.

---

## Reconciling with What We Already Built

Here is the honest reconciliation:

| Element | Pieces' note | Our system | Verdict | 
|---|---|---|---|
| Note types | 5 | 6 | **Ours** (adds Source, Person) | 
| Typed links | Not mentioned | 5 edge types + convention card | **Ours** — this is a gap in the note | 
| Proposition template | Has falsifier field ✓ | Has dated position ✓ | **Merge both** | 
| Steel-man | Not mentioned | Section 1 of Claim cards | **Ours** — IOED defence | 
| Crux / load-bearing disagreement | Not mentioned | Section 6 of Claim cards | **Ours** | 
| Open threads | Implicit | Explicit section | **Ours** | 
| Belief-revision framing | Explicit, strong | Implicit | **Theirs** — adopt this framing | 
| "Capture delta, not summary" | Explicit, strong | Implicit | **Theirs** — adopt this rule | 

**Net:** The note adds two genuinely valuable framings (*belief revision* and *capture delta*) to what we have. It would remove two pieces of structure (Source, Person) that are worth keeping. It misses typed links entirely.

---

## The Honest Meta-Point

This note is a **well-written opinion piece dressed as advice**. It is mostly right, but it is being confidently prescriptive in places where it should be tentative. Specifically:

- It dismisses "wiki-style" notes as obviously inferior. This is a preference, not a proven fact. Some of the world's most productive thinkers (Wikipedia editors, many domain experts) keep wiki-style notes and do fine.

- It implies the belief-revision model is *the* correct model. It is *a* correct model, and probably the right one for you given your stated goals. But the universalist framing obscures that it is a choice.

When you read this note you should feel **validated** in the direction you are heading — because it is consistent with what you have been building — but not **conclusive** that this is the only way. The IOED principle cuts both ways: it applies to advice you are *given* as much as to beliefs you hold.

---

## What to Extract and What to Discard

### Extract and add to your PKM

1. **"Belief revision system, not information warehouse"** — make this a card. It is your PKM's mission statement.

2. **"Capture delta, not summary"** — this becomes a `Practice` card, probably titled something like `Practice: Capture What Changed My Thinking`.

3. **Falsifier field** in the claim template — add this to the JTB card as Section 9: "What would update this?"

4. **The "why am I keeping this?" test** — genuinely useful gatekeeping question. Worth keeping as a `Practice` card.

### Discard or modify

1. The five-type taxonomy → **keep our six**.

2. The blanket dismissal of reference notes → **add a seventh type, Reference, for genuinely stable lookups**.

3. The three-level confidence scale → **use a more granular epistemic-status ladder**.

4. The implicit claim that this is The One True Way → **note it as one defensible model among others**.

---

## Your Immediate Next Action

Fill in only Section 1 (the steel-manned statement). This is a `Claim` card precisely because — and this is the point — the assertion is arguable. It is not obviously true that this is what a PKM *is*. It might be what *your* PKM *should be*. Those are different claims.