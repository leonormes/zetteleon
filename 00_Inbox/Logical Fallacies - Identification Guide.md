---
aliases: [Fallacy Guide]
created: 2026-07-02T00:00:00+00:00
modified: 2026-07-04T10:52:08+00:00
permalink: llmeon/00-inbox/logical-fallacies-identification-guide
status: draft
tags: [argumentation, epistemology, logic]
title: Logical Fallacies - Identification Guide
type: concept
---

> Purpose—identify fallacies in live text and dialogue. The skill is not recalling a list; it is running a four-question diagnostic, then discriminating a genuine fallacy from its legitimate twin. The tables exist only to name what the diagnostic finds.

## 1 · The Diagnostic (Memorise tHis, not the tAbles)

Given any argument:

1. Standardise. State the conclusion in one sentence. List the premises. Strip the rhetoric. Most fallacies survive on presentation; standardisation removes the camouflage.
2. Test the form. Assume every premise true. Does the conclusion follow necessarily (deductive), or become substantially more probable (inductive)? If neither → formal fallacy / non sequitur (§3.1).
3. Test relevance. Do the premises address the _claim_—or the claimant, the audience, or a distorted version of the claim? → relevance fallacy (§3.2).
4. Test the premises. Is a premise doing hidden work—assuming the conclusion, forcing a false choice, or shifting a word's meaning mid-argument? → presumption (§3.3) or ambiguity (§3.4).

And the guard-rail:

> [!warning] The fallacy fallacy
> A fallacious argument does not make its conclusion false. You have defeated _an argument_, not _the claim_. Before updating confidence, construct the repaired (steel-manned) argument—then engage that.

## 2 · Validity and Soundness (Corrected)

|                  | All premises true                    | ≥ 1 premise false                       |
| ---------------- | ------------------------------------ | --------------------------------------- |
| Form valid   | Sound—conclusion guaranteed    | Valid but unsound (the penguin case) |
| Form invalid | Fallacious—conclusion unsettled    | Fallacious—conclusion unsettled        |

This vocabulary is deductive only. Inductive arguments are assessed as _strong/weak_ (form) and _cogent/uncogent_ (form + true premises). Most informal fallacies live on the inductive side—which is why symbolisation alone won't catch them.

> [!note] The Popperian asymmetry, in fallacy terms
> _Modus tollens_ (if T then O; not-O; ∴ not-T) is valid—the logical engine of falsification. _Affirming the consequent_ (if T then O; O; ∴ T) is invalid—the logical shape of naïve confirmation. Popper's asymmetry between falsification and verification _is_ this asymmetry of forms. Two corollaries: no true Scotsman (§3.3) is ad hoc immunisation against a landed modus tollens; Flew's "death by a thousand qualifications" (_Theology and Falsification_) is the same move observed in theology.

## 3 · The Families

### 3.1 Formal—the Structure is Broken

Detect by symbolising: replace content with letters and see whether the skeleton stands.

| Fallacy | The move | Tell | Not a fallacy when |
| --- | --- | --- | --- |
| Affirming the consequent | If P→Q; Q; ∴ P | Evidence _consistent with_ a theory offered as _proof of_ it | Framed as abduction—"P best explains Q"—and held probabilistically |
| Denying the antecedent | If P→Q; not-P; ∴ not-Q | "No P, so no Q" where Q has other routes | The conditional is genuinely biconditional (P iff Q) |
| Undistributed middle | All A are C; all B are C; ∴ all A are B | Shared property read as shared identity |—|

### 3.2 Relevance—the Premises Aim at the Wrong Target

| Fallacy             | The move                                              | Tell                                                | Not a fallacy when                                                             |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Ad hominem          | Attack the arguer, not the argument                   | "Coming from _him_…"                                | The argument rests on testimony or credibility rather than checkable reasoning |
| Tu quoque           | Hypocrisy offered as rebuttal                         | "You do it too"                                     | Assessing the person's sincerity—never the claim's truth                       |
| Straw man           | Refute a distorted version                            | "So what you're really saying is…"                  | Restating to clarify, and the opponent confirms the restatement                |
| Genetic fallacy     | Judge a claim by its origin                           | "That idea comes from X, so…"                       | Origin bears on testimony reliability when the claim can't be checked directly |
| Appeal to authority | Out-of-domain expert, or authority as deductive proof | Credential ≠ field; a lone maverick vs a literature | Relevant expert _consensus_ cited as defeasible inductive evidence             |
| Ad populum          | Popularity as truth                                   | "Everyone knows"                                    | Many _independent_ judgements as weak evidence—and even then, weak             |
| Appeal to emotion   | Feelings as premises for a factual claim              | Vivid anecdote standing in for the missing premise  | Emotion as a reason for _action_, not as evidence of _fact_                    |

### 3.3 Presumption—a Premise Smuggles the Result

| Fallacy | The move | Tell | Not a fallacy when |
| --- | --- | --- | --- |
| Begging the question | Conclusion hidden inside a premise | Rephrase the premise—is it the conclusion in a wig? |—(distinct from the colloquial "raises the question") |
| False dilemma | Two options presented; more exist | "Either… or…" laid over a continuum | Genuine dichotomies (P or not-P) |
| Loaded question | Question presupposes the disputed claim | "Have you stopped…?" | The presupposition is already granted by both parties |
| Slippery slope | Chain to catastrophe asserted, no mechanism | "Next thing you know…" | Mechanism and stepwise probabilities are argued (legal precedent is a real mechanism) |
| False cause (post hoc) | Sequence or correlation read as causation | "After X, therefore because of X" | Correlation flagged as _grounds for investigation_—confounders, reverse causation, coincidence still open |
| Hasty generalisation | Sweeping rule from a tiny or biased sample | Anecdote → "always / never" | Adequate, representative sampling |
| No true Scotsman | Membership redefined to dodge a counterexample | The definition mutates exactly when the counterexample lands | The definition was refined _in advance_ and held fixed |
| Appeal to ignorance | "Not proven false, ∴ true" (or the reverse) | "You can't disprove it" | Absence of _expected_ evidence after a competent search genuinely lowers P(H) |

### 3.4 Ambiguity—the Meaning Moves

| Fallacy | The move | Tell | Not a fallacy when |
| --- | --- | --- | --- |
| Equivocation | A key term changes meaning mid-argument | The argument only works if the word means X in premise 1 and Y in premise 2 | Senses are explicitly distinguished and tracked |
| Motte-and-bailey | Bold claim (bailey) defended as its modest cousin (motte), then re-expanded | Retreat under pressure; re-expansion once pressure lifts | Genuinely conceding to the modest claim—_and staying there_ (Shackel) |
| Composition / division | Parts→whole or whole→parts property transfer | "Every part is light, so the whole is light" | Properties that provably transfer (mass sums; fragility mostly doesn't) |

_Not exhaustive by design—add rows only when a specimen is actually encountered in the wild. Examples are deliberately omitted: the reps log (§5) is where your own specimens accumulate. Generation beats recognition, and recognition is the fluency illusion's home turf._

## 4 · Source audit—Gemini Capture, 2026-07-02

The capture is serviceable but contains one outright error and three structural gaps. Recorded here because this note deliberately diverges from it.

1. Terminological error. Gemini defines valid vs sound correctly, then writes of the penguin syllogism: "the argument as a whole is structurally sound but factually broken." By its own definitions two paragraphs earlier, the argument is _valid but unsound_. Using "sound" for structure is precisely the conflation the passage set out to prevent. Consistent with prior audits: vocabulary-level rigour without practising it.
2. Missing organising principle. Seven informal fallacies are listed and syllogisms explained, but the formal/informal distinction is never named and no formal fallacies are given—despite the syllogism section making them the natural next step.
3. No fallacious/legitimate boundary. The authority, bandwagon and slippery slope entries omit the conditions under which the same move is rational. Misidentification lives exactly on that boundary—hence the "Not a fallacy when" columns above.
4. No identification method. A flat list optimises recognition of textbook cases; live identification needs a procedure (§1).

## 5 · Practice Protocol

One rep (~5 min, interest-triggered, not scheduled):

1. Take one argumentative paragraph already encountered—editorial, HN/Reddit comment, LLM output.
2. Run diagnostic questions 1–4.
3. Name at most one fallacy and one near-miss—something fallacy-shaped that survives via its legitimate twin. The discrimination is the skill; detection alone trains false positives.
4. Log one line below: `date · source · verdict · one-line reason`.

Anti-split rule: this protocol stays inside this note. Promote to a Practice card only after the log holds ≥ 10 entries. (Named failure mode: structure before consolidation.)

## Reps Log

## Links

related_to:: [[Popperian fallibilism]] <!-- repoint to your actual card name -->

related_to:: [[Scandal of deduction]] <!-- §2: validity vs informativeness -->

related_to:: [[LLMs as map-only engines]] <!-- fallacy-shaped text without reasoning; §4 is a specimen -->

related_to:: [[Ontological argument — Kant predicate objection]] <!-- equivocation on "exists" and question-begging both live in this literature -->
