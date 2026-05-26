---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:54+00:00
tags: [Literature]
title: Lit! The Many Faces of !Logic!
---

## Lit: The Many Faces of "Logic"

Source: Opus 4.7 [2026-04-25.md](../Journal/2026-04-25.md)

You've spotted something real: "logic" is a polysemous term that spans from rigorous mathematical formalism to dinner-table hand-waving. The unifying thread is the study of valid inference—_what follows from what_—but the rigour varies enormously depending on the domain.

Below, ranked from most to least rigorous.

---

### Tier 1: Formal Logic (Maximum Rigour)

These use precise symbolic languages with explicit syntax, semantics, and rules of inference. Validity is mechanically checkable.

- Mathematical Logic
   - The study of formal systems themselves: proof theory, model theory, set theory, recursion theory, computability.
   - This is logic _as a branch of mathematics_. Think Gödel, Tarski, Church, Turing.
   - Asks meta-questions like "Is this system consistent? Complete? Decidable?"
- Symbolic / Deductive Logic
   - Propositional logic: truth-functional connectives (∧, ∨, ¬, →).
   - First-order predicate logic: quantifiers (∀, ∃), variables, predicates.
   - Higher-order logics: quantification over predicates themselves.
   - Modal logics: necessity/possibility (□, ◇), used for reasoning about time, knowledge, obligation.
   - Validity here is truth-preserving by form alone—if the premises are true, the conclusion _must_ be true.
- Computational Logic
   - Boolean algebra in circuit design, type theory in programming languages, formal verification, SAT solvers, Prolog-style logic programming.
   - Same formal rigour as symbolic logic, applied to machines.

---

### Tier 2: Philosophical Logic

- Studies the _foundations and extensions_ of formal logic.
- Topics: paradoxes (Liar, Russell's), reference, truth, vagueness, conditionals, relevance logic, paraconsistent logic.
- Rigorous, but engages with cases where standard formal logic strains (e.g. "If the moon were made of cheese…").

---

### Tier 3: Non-Deductive Formal Reasoning

Still formalised, but conclusions don't follow with certainty—they follow with _probability_ or _plausibility_.

- Inductive Logic
   - Generalising from particulars: "Every swan I've seen is white, therefore swans are white."
   - Formalised via probability theory and Bayesian inference.
- Abductive Reasoning ("inference to the best explanation")
   - Given evidence, infer the most plausible cause. Used heavily in science, medicine, and detective work.
   - Less formalised than induction, but a recognised mode of inference.

---

### Tier 4: Informal Logic & Critical Thinking

- Analysis of arguments in natural language rather than symbols.
- Fallacy identification (ad hominem, straw man, affirming the consequent).
- Argument mapping, charitable reconstruction.
- Bridges formal logic and everyday reasoning. Rigorous in spirit, but the messiness of natural language means judgement is required.

---

### Tier 5: Argumentation Theory & Rhetoric

- How arguments function in practice: persuasion, dialectic, debate.
- Includes pragma-dialectics, Toulmin's argument model.
- Studies _what makes arguments effective_, not just valid.

---

### Tier 6: Colloquial Uses (Lowest Rigour)

Here "logic" loses its technical edge and becomes a loose synonym for _reasonableness_ or _coherence_.

- "That's logical" → "That makes sense" / "That seems reasonable."
- "The logic of the story" → the internal consistency of a narrative.
- "The logic of war/markets/grief" → the underlying dynamics or causal pattern of a system.
- "Use your logic" → apply common-sense reasoning.

These usages are metaphorical extensions of the technical term. They borrow the prestige of formal logic without the constraints.

---

### The Underlying Principle

What unifies all six tiers is the question: "Given X, what should we conclude about Y, and why?"

- Tiers 1–2 answer this with mathematical certainty.
- Tier 3 answers it with calibrated probability.
- Tiers 4–5 answer it with structured but fallible argument.
- Tier 6 answers it with vibes.

The confusion in everyday discourse is that people often invoke the _authority_ of Tier 1 ("it's just logic!") whilst actually operating in Tier 6.

---

### Next Action

If this taxonomy interests you, pick one of these for a 15-minute deeper dive:

1. Open a terminal and run `man test`—Bash's `[[ ]]` and `test` are pure Tier 1 propositional logic. Read the section on logical operators.
2. Or open Wikipedia's article on "List of fallacies" and skim the formal vs informal split—that's the Tier 1 / Tier 4 boundary in action.

Which tier do you want to drill into next?
