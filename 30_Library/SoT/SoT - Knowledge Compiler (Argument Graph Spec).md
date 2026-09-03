---
aliases: [Argument Compiler, Argument Graph, Belief Tracing, Knowledge Compiler]
conformant: true
created: 2026-07-24T00:00:00+00:00
modified: 2026-08-29T09:36:39+00:00
permalink: llmeon/30-library/so-t/so-t-knowledge-compiler-argument-graph-spec
see_also: ["[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]", "[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]"]
tags: [domain/pkm, prodos/sot, topic/knowledge-architecture, topic/knowledge-graph]
title: SoT - Knowledge Compiler (Argument Graph Spec)
type: sot
---

> Open threads: [[HEAD - Is the argument compiler's gap definition measuring anything real?]]

> Canonical status: this note specifies the semantics and compiler capabilities of the knowledge graph—what the tool _computes_ and _answers_. Its sibling [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] fixes the syntax (how edges are written and resolved). The validator is `10_System/scripts/edge_lint.py`; capabilities below extend it. Roadmap in §5 is the source of truth for build order—do one phase, ship it, then reassess.

## Minimum Viable Understanding (MVU)

The vault holds atomic claims. A typed edge records _why_ one claim stands: `A supports B`, `A contradicts B`, `A depends_on B`. Once enough claims are wired this way, the collection stops being a pile of notes and becomes a directed argument graph—and a graph can be interrogated by a computer in ways a human cannot hold in their head. Four questions become mechanical: _Where is my argument unsupported?_ (a claim doing work with nothing beneath it). _What are my actual foundations?_ (the axioms everything rests on). _Where do I contradict myself?_ (conflicting or circular claims). _Why do I believe X, and what falls if X falls?_ (trace the justification thread up and down). This is Zettelkasten's atomicity plus a compiler: not a theorem prover and not a truth oracle, but a bookkeeper for your own reasoning that flags the gaps, roots, and contradictions you would otherwise miss. It is opt-in—most notes never join the argument graph, and that is fine.

## 1. Vision & Scope

In scope. Claims (and claim-blocks) that participate in reasoning, connected by justification edges, plus a compiler that computes epistemic properties of that graph (§3) and reports them—never auto-edits.

Explicitly out of scope.

- Not all content is argumentation. Reference notes, procedures, journal entries, MoCs—most of the vault—never join the argument graph and are never flagged for "missing support". A note is in the graph _only_ if it emits or receives a justification edge.
- Not a logic engine. No formal soundness, no proof checking, no truth values. `A supports B` is a bookkeeping assertion _you_ made, not a validated inference. The compiler checks graph _shape_, not logical validity.
- No belief enforcement. The tool surfaces gaps and conflicts; resolving them is always a human decision.

## 2. The Model (Minimal)

Three primitives, nothing more:

| Primitive | What it is | How it's written |
|:---|:---|:---|
| Claim node | An atomic assertion that can be true or false. | A note `type: claim`, or a `content-block type="claim" id="…"`. |
| Justification edge | A directed "reason" relationship between claims. | A typed edge (§4): `[supports:: [[Target]]]` etc. |
| Axiom marker | Declares a claim _foundational_—deliberately unsupported, a starting premise. | `axiom: true` in frontmatter (note-level), or `axiom="true"` on the `content-block-start` comment (block-level). |

That is the whole data model. Everything the compiler does (§3) is a graph computation over these three things.

## 3. What the Compiler Computes (The fOur cApabilities)

Direction convention: `A supports B` is an edge A → B, read "A is a reason for B". So B's justification is found by walking edges _backwards into_ B. The same holds for `depends_on` (A depends_on B = A → B, "A presupposes B"). Together these two are the justification edges; `contradicts` is a symmetric conflict edge.

### C1—Gap Detection (Unsupported wOrking cLaims)

- Definition: a claim node that (a) _supports something_ (out-degree ≥ 1 on justification edges) but (b) has _no incoming_ justification edge and (c) is _not_ marked `axiom`.
- Answers: _"Where does my argument assert something it never justifies?"_
- Why this definition: a claim that supports nothing and is supported by nothing is just an isolated note—not a gap. A gap is a claim _doing load-bearing work_ with nothing beneath it and no honest "I take this as given" flag. The fix is a forced, healthy choice: add support, or declare it an axiom.

### C2—Foundation Audit (Roots & aXioms)

- Definition: two sets. _Declared axioms_ = nodes with `axiom: true`. _Undeclared foundations_ = the C1 gap set (unsupported load-bearing claims).
- Answers: _"What does my whole structure actually rest on—and which of those foundations have I consciously chosen versus smuggled in?"_
- Note: every undeclared foundation is a decision waiting to be made. Resolving C1 gaps _is_ the act of auditing your foundations; the two capabilities are the same computation viewed from opposite ends.

### C3—Conflict Detection

- Definition (v-first): (a) any `contradicts` edge = a live conflict; (b) any _cycle_ in the `supports`/`depends_on` graph = circular reasoning.
- Answers: _"Where do I hold claims that fight each other, or justify a claim using itself?"_
- Deferred (v-later): _derived_ contradiction—a claim transitively supported by both X and something that contradicts X. Powerful but needs the traversal engine (C4) first.

### C4—Provenance / Thread-pulling

- Definition: two traversals from a chosen node X. _Why(X)_ = the transitive closure of justification edges _into_ X, down to axioms/leaves—the justification tree. _Impact(X)_ = the transitive closure _out of_ X—everything that would be threatened if X fell.
- Answers: _"Why do I believe X, all the way to bedrock?"_ and _"If X turns out wrong, what else collapses?"_
- Output: an indented tree (text first; visualisation is a later luxury).

## 4. Relationship Vocabulary (The aRgumentation sUbset)

The full vocabulary lives in [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Of its six relationships, three are justification/conflict edges and carry the argument graph:

| Edge | Meaning (A → B) | Role in the graph |
|:---|:---|:---|
| `supports` | A is evidence or a reason for B. | justification (inferential) |
| `depends_on` | A presupposes B; B is a premise of A. | justification (presuppositional) |
| `contradicts` | A conflicts with B (symmetric). | conflict |

The other three (`extends`, `synthesizes`, `implements`) are structural, not argumentative—the compiler ignores them for C1–C3 and may optionally include them in C4 provenance as weak/structural links (flagged as such). No new relationship types are needed for v1; if argumentation reveals a genuine gap (e.g. a distinct `rebuts` vs `undercuts`), it is added _there_, not here.

## 5. Roadmap (Iterate slowly—one cApability per pHase)

| Phase | Capability | Build | Status |
|:---|:---|:---|:---|
| v0 | Typed edges + resolution | `edge_lint.py`—no danglers, controlled vocab, targets resolve. | done |
| v1 | Gap detection + foundation audit (C1, C2) | Add the `axiom` marker; add `edge_lint.py --audit`: build the justification subgraph, list gaps and declared-vs-undeclared foundations. | built, unused |
| v2 | Conflict detection (C3) | Report `contradicts` edges; detect cycles in the supports graph. | built, untested—no `contradicts` edge exists yet |
| v3 | Provenance (C4) | `edge_lint.py --why <title>` and `--impact <title>`—print the justification / impact tree. | built, working |
| v4+ | Derived contradictions, strength-weighted confidence, visualisation, cross-note argument views (Bases) |—| deferred |

Each phase is shippable alone and adds exactly one epistemic answer. Do not build vN+1 until vN has been used on real claims and earned its place.

> Status correction (2026-07-25). This table previously read `v1 next / v2 planned / v3 planned`. All three were in fact already implemented in `edge_lint.py`. The build discipline above was therefore not followed—v1–v3 were written in one pass, ahead of the data. The honest current state is that the _code_ runs but only v0 and v3 have been exercised against real edges: v1 returns 12 gaps (below), and v2 has never fired, because the vault contains zero `contradicts` edges. The next task is not more code; it is recording a real contradiction and a real axiom so v1 and v2 can be judged on output rather than assumed correct.

## 6. Simplicity Guards (Non-goals)

- Report-only, always. The compiler proposes; it never rewrites a note (mirrors `edge_lint.py` and the `UNSURE` discipline in [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]).
- Opt-in graph. Silence on a note is the default. Only claims with justification edges are ever assessed.
- No confidence maths yet. `strength`/`confidence` attributes stay advisory prioritisation aids, not inputs to a computed truth score, until a real need proves otherwise (see the schema-complexity ceiling in [[SoT - Typed Answer Contract (TAC) for LLM Output]]).
- One marker, no ontology. The only new schema element in v1 is the boolean `axiom`. Resist adding node kinds or edge types speculatively.

## 7. Open Questions (Deferred dEcisions)

- Axiom representation. `axiom: true` (chosen, minimal) vs an `epistemic_status: axiom` enum value vs a `#axiom` tag. Boolean chosen for orthogonality (an axiom can be highor low-confidence), but revisit if it clutters frontmatter.
- Do structural edges count in provenance? C4 could include `extends`/`implements` as weak lineage. Default: exclude from C1–C3, optionally include in C4 with a flag. Decide when C4 is built.
- Block-level vs note-level claims. The model supports both, but mixing them raises the block-id-uniqueness question from the Edge Vocabulary SoT §4. Prefer note-level claims until block-level proves necessary for a real argument.
- Scope of the graph scan. Whole vault, or a designated `argument/` corpus? Default whole-vault (opt-in via edges means noise is naturally low); reassess if scans get slow or noisy.

## Tensions & Gaps

- ~~No argument data yet.~~ Superseded 2026-07-25. The justification graph is no longer empty: 39 justification edges across 43 nodes, mostly a real ADHD-neurology argument converging on [[The ADHD brain operates on an Interest-Based Nervous System]]. C1 returns 12 genuine gaps—claims that support something with nothing beneath them and no `axiom` flag. What remains empty is the _conflict_ half: 0 `contradicts` edges and 0 `axiom: true` markers vault-wide, so C2's declared-axiom set is empty by construction and C3 has never fired on real data. The seeding task the original tension named is half-done: the support graph exists, the conflict graph does not.
- Every gap is a leaf, which may mean the definition is too generous. All 12 C1 gaps are single-hop leaves feeding one hub claim, and the graph is two levels deep. A shallow star is exactly the shape that makes C1 look productive while telling you little—the "gaps" are simply the outermost ring, and adding support to any of them just moves the ring outward. C1 earns its place only once the graph has depth; until then, read its output as "here is the current frontier", not "here are 12 defects".
- Author-asserted, not validated. Every edge is a claim _you_ made about your own reasoning. The compiler can find a gap or a contradiction in the _shape_ of what you asserted; it cannot tell you whether an individual `supports` is actually a good reason. It sharpens your thinking; it does not outsource it.
- Atomicity discipline required. The graph is only as clean as the claims are atomic. A note bundling three assertions cannot be cleanly supported or contradicted—the Zettelkasten "one claim per node" rule is a hard prerequisite, not a stylistic preference.

[depends_on:: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], strength=5, confidence=high]

[supports:: [[Claim - Domains relate through named relations, not undifferentiated association]], strength=4, confidence=medium]
