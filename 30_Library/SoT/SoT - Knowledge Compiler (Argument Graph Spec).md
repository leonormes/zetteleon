---
aliases: [Knowledge Compiler, Argument Graph, Argument Compiler, Belief Tracing]
created: 2026-07-24T00:00:00+00:00
modified: 2026-07-24T00:00:00+00:00
permalink: llmeon/30-library/so-t/so-t-knowledge-compiler-argument-graph-spec
see_also: ["[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]", "[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]", "[[SoT - PRODOS Core Specification]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]"]
tags: [domain/pkm, prodos/sot, topic/knowledge-graph]
title: SoT - Knowledge Compiler (Argument Graph Spec)
type: sot
conformant: true
prodos:
  kind: sot
  lifecycle: seedling
  trust: working
---

> Canonical status: this note specifies the **semantics and compiler capabilities** of the knowledge graph — what the tool *computes* and *answers*. Its sibling [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] fixes the **syntax** (how edges are written and resolved). The validator is `10_System/scripts/edge_lint.py`; capabilities below extend it. Roadmap in §5 is the source of truth for build order — do one phase, ship it, then reassess.

## Minimum Viable Understanding (MVU)

The vault holds atomic claims. A **typed edge** records *why* one claim stands: `A supports B`, `A contradicts B`, `A depends_on B`. Once enough claims are wired this way, the collection stops being a pile of notes and becomes a **directed argument graph** — and a graph can be interrogated by a computer in ways a human cannot hold in their head. Four questions become mechanical: *Where is my argument unsupported?* (a claim doing work with nothing beneath it). *What are my actual foundations?* (the axioms everything rests on). *Where do I contradict myself?* (conflicting or circular claims). *Why do I believe X, and what falls if X falls?* (trace the justification thread up and down). This is Zettelkasten's atomicity plus a compiler: not a theorem prover and not a truth oracle, but a bookkeeper for your own reasoning that flags the gaps, roots, and contradictions you would otherwise miss. It is opt-in — most notes never join the argument graph, and that is fine.

## 1. Vision & scope

**In scope.** Claims (and claim-blocks) that participate in reasoning, connected by justification edges, plus a compiler that computes epistemic properties of that graph (§3) and reports them — never auto-edits.

**Explicitly out of scope.**

- **Not all content is argumentation.** Reference notes, procedures, journal entries, MoCs — most of the vault — never join the argument graph and are never flagged for "missing support". A note is in the graph *only* if it emits or receives a justification edge.
- **Not a logic engine.** No formal soundness, no proof checking, no truth values. `A supports B` is a bookkeeping assertion *you* made, not a validated inference. The compiler checks graph *shape*, not logical validity.
- **No belief enforcement.** The tool surfaces gaps and conflicts; resolving them is always a human decision.

## 2. The model (minimal)

Three primitives, nothing more:

| Primitive | What it is | How it's written |
|:---|:---|:---|
| **Claim node** | An atomic assertion that can be true or false. | A note `type: claim`, or a `content-block type="claim" id="…"`. |
| **Justification edge** | A directed "reason" relationship between claims. | A typed edge (§4): `%%claim.supports{target}%%` etc. |
| **Axiom marker** | Declares a claim *foundational* — deliberately unsupported, a starting premise. | `axiom: true` in frontmatter (note-level), or `axiom="true"` on the `content-block-start` comment (block-level). |

That is the whole data model. Everything the compiler does (§3) is a graph computation over these three things.

## 3. What the compiler computes (the four capabilities)

Direction convention: **`A supports B` is an edge A → B**, read "A is a reason for B". So B's justification is found by walking edges *backwards into* B. The same holds for `depends_on` (A depends_on B = A → B, "A presupposes B"). Together these two are the **justification edges**; `contradicts` is a symmetric conflict edge.

### C1 — Gap detection (unsupported working claims)

- **Definition:** a claim node that (a) *supports something* (out-degree ≥ 1 on justification edges) but (b) has *no incoming* justification edge and (c) is *not* marked `axiom`.
- **Answers:** *"Where does my argument assert something it never justifies?"*
- **Why this definition:** a claim that supports nothing and is supported by nothing is just an isolated note — not a gap. A gap is a claim *doing load-bearing work* with nothing beneath it and no honest "I take this as given" flag. The fix is a forced, healthy choice: **add support, or declare it an axiom.**

### C2 — Foundation audit (roots & axioms)

- **Definition:** two sets. *Declared axioms* = nodes with `axiom: true`. *Undeclared foundations* = the C1 gap set (unsupported load-bearing claims). 
- **Answers:** *"What does my whole structure actually rest on — and which of those foundations have I consciously chosen versus smuggled in?"*
- **Note:** every undeclared foundation is a decision waiting to be made. Resolving C1 gaps *is* the act of auditing your foundations; the two capabilities are the same computation viewed from opposite ends.

### C3 — Conflict detection

- **Definition (v-first):** (a) any `contradicts` edge = a live conflict; (b) any *cycle* in the `supports`/`depends_on` graph = circular reasoning.
- **Answers:** *"Where do I hold claims that fight each other, or justify a claim using itself?"*
- **Deferred (v-later):** *derived* contradiction — a claim transitively supported by both X and something that contradicts X. Powerful but needs the traversal engine (C4) first.

### C4 — Provenance / thread-pulling

- **Definition:** two traversals from a chosen node X. *Why(X)* = the transitive closure of justification edges *into* X, down to axioms/leaves — the justification tree. *Impact(X)* = the transitive closure *out of* X — everything that would be threatened if X fell.
- **Answers:** *"Why do I believe X, all the way to bedrock?"* and *"If X turns out wrong, what else collapses?"*
- **Output:** an indented tree (text first; visualisation is a later luxury).

## 4. Relationship vocabulary (the argumentation subset)

The full vocabulary lives in [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Of its six relationships, **three are justification/conflict edges** and carry the argument graph:

| Edge | Meaning (A → B) | Role in the graph |
|:---|:---|:---|
| `supports` | A is evidence or a reason **for** B. | justification (inferential) |
| `depends_on` | A **presupposes** B; B is a premise of A. | justification (presuppositional) |
| `contradicts` | A conflicts with B (symmetric). | conflict |

The other three (`extends`, `synthesizes`, `implements`) are **structural**, not argumentative — the compiler ignores them for C1–C3 and may optionally include them in C4 provenance as weak/structural links (flagged as such). No new relationship types are needed for v1; if argumentation reveals a genuine gap (e.g. a distinct `rebuts` vs `undercuts`), it is added *there*, not here.

## 5. Roadmap (iterate slowly — one capability per phase)

| Phase | Capability | Build | Status |
|:---|:---|:---|:---|
| **v0** | Typed edges + resolution | `edge_lint.py` — no danglers, controlled vocab, targets resolve. | **done** |
| **v1** | Gap detection + foundation audit (C1, C2) | Add the `axiom` marker; add `edge_lint.py --audit`: build the justification subgraph, list gaps and declared-vs-undeclared foundations. | next |
| **v2** | Conflict detection (C3) | Report `contradicts` edges; detect cycles in the supports graph. | planned |
| **v3** | Provenance (C4) | `edge_lint.py why <id>` and `impact <id>` — print the justification / impact tree. | planned |
| **v4+** | Derived contradictions, strength-weighted confidence, visualisation, cross-note argument views (Bases) | — | deferred |

Each phase is shippable alone and adds exactly one epistemic answer. Do not build vN+1 until vN has been used on real claims and earned its place.

## 6. Simplicity guards (non-goals)

- **Report-only, always.** The compiler proposes; it never rewrites a note (mirrors `edge_lint.py` and the `UNSURE` discipline in [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]).
- **Opt-in graph.** Silence on a note is the default. Only claims with justification edges are ever assessed.
- **No confidence maths yet.** `strength`/`confidence` attributes stay advisory prioritisation aids, not inputs to a computed truth score, until a real need proves otherwise (see the schema-complexity ceiling in [[SoT - Typed Answer Contract (TAC) for LLM Output]]).
- **One marker, no ontology.** The only new schema element in v1 is the boolean `axiom`. Resist adding node kinds or edge types speculatively.

## 7. Open questions (deferred decisions)

- **Axiom representation.** `axiom: true` (chosen, minimal) vs an `epistemic_status: axiom` enum value vs a `#axiom` tag. Boolean chosen for orthogonality (an axiom can be high- or low-confidence), but revisit if it clutters frontmatter.
- **Do structural edges count in provenance?** C4 could include `extends`/`implements` as weak lineage. Default: exclude from C1–C3, optionally include in C4 with a flag. Decide when C4 is built.
- **Block-level vs note-level claims.** The model supports both, but mixing them raises the block-id-uniqueness question from the Edge Vocabulary SoT §4. Prefer note-level claims until block-level proves necessary for a real argument.
- **Scope of the graph scan.** Whole vault, or a designated `argument/` corpus? Default whole-vault (opt-in via edges means noise is naturally low); reassess if scans get slow or noisy.

## Tensions & Gaps

- **No argument data yet.** As of writing, the only typed edges in the vault are the *structural* container-primitive edges — the justification graph is effectively empty. This spec is forward-looking; v1's value only appears once real `supports`/`depends_on` edges exist. The first task is therefore to *seed* one small real argument, not to build v1 against nothing.
- **Author-asserted, not validated.** Every edge is a claim *you* made about your own reasoning. The compiler can find a gap or a contradiction in the *shape* of what you asserted; it cannot tell you whether an individual `supports` is actually a good reason. It sharpens your thinking; it does not outsource it.
- **Atomicity discipline required.** The graph is only as clean as the claims are atomic. A note bundling three assertions cannot be cleanly supported or contradicted — the Zettelkasten "one claim per node" rule is a hard prerequisite, not a stylistic preference.
