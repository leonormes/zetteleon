---
title: Knowledge Architecture — Topic Organisation Report
output_type: report
created: 2026-07-27 09:45:00+00:00
wiki_sources: []
tags:
- output
- topic/knowledge-architecture
permalink: llmeon/output/2026-07-27-report-knowledge-architecture-topic-organisation
---

## Scope

Anchor note: [[SoT - Knowledge Architecture (Associative Ontology)]].

Task: audit links, establish a topic tag, connect the cluster with typed edges.

Governance: this run wrote frontmatter `tags` and body prose inside `30_Library/`, which falls **outside** the [[AGENTS.md]] §9.3 exception (typed edges + `axiom:` only). Performed under explicit human instruction per §6. Typed-edge writes were within §9.3.

---

## 1. Link audit

### Fixed

| Note | Was | Now |
|:---|:---|:---|
| SoT - Knowledge Architecture | `[[MOC - Data-Oriented Design]]` | `[[MOC - Data-Oriented Structures & Internals\|Data-Oriented Design]]` |
| SoT - Knowledge Architecture | `[[SoT - Type Theory & Data Structures]]` | `[[MOC - Type Theory\|Type Theory & Data Structures]]` |
| SoT - Knowledge Architecture | `[[SoT - Cognitive Refactoring (Neural Debugging)]]` | `[[SoT - Belief Architecture & Cognitive Spaces\|Cognitive Refactoring (Neural Debugging)]]` |
| SoT - Generative Infrastructure Configuration Framework | `[[SoT - CUE Configuration Logic]]` | `[[SoT - CUE Configuration]]` |
| SoT - Logotherapy and the Will to Meaning | `[[SoT - Identity-Based Habit Formation]]` | `[[SoT - Habit Formation Framework]]` |

### Left broken — UNSURE, needs human judgement

- `[[Victor Frankl]]` — in [[SoT - Logotherapy and the Will to Meaning]], marked "(Archived)". No live note; no obvious substitute. Spelling is also wrong (Viktor).
- `[[Contextual Relationships]]` — in [[SoT - The Philosophy of the Absurd (Camus)]]. Nearest live note is *Contextual Integration of New Ideas*, which is about a different thing. Did not retarget.
- `[[Video - How the Algorithm Hijacked Monkey's Brain]]` — in [[SoT - Active Learning Techniques]]. Source-material link with no corresponding note.

### `SoT - Cognitive Refactoring (Neural Debugging)` — vault-wide dangler

Referenced from three further SoTs, all still broken (out of the audited scope, not touched):

- [[SoT - Belief Architecture & Cognitive Spaces]]
- [[SoT - Personal Agency and Transformation]]
- [[SoT - Mental Models in Software Development]]

Three notes now reference a hub that has never existed. Either author it, or retarget all three.

### Newly in scope after retargeting

Retargeting pulled three notes into the anchor's immediate neighbourhood; they carry their own danglers:

- [[MOC - Data-Oriented Structures & Internals]] → `SoT - Data-Oriented Programming (DOP)`, `SoT - Data-Centric Software Engineering`
- [[MOC - Type Theory]] → `SoT - Parse, Don't Validate`, `SoT - Software Complexity is Conserved Between Control Flow and Representation`
- [[SoT - Belief Architecture & Cognitive Spaces]] → `Beliefs as Defining Spaces`, `Emotional Reasoning`, plus the two above

---

## 2. Topic tag — `topic/knowledge-architecture`

Applied to **50 notes**. Scope chosen: the *meta-layer* — notes making claims about how knowledge is structured — not the six subject domains the anchor surveys.

**Rationale for the narrow scope.** The anchor's stated thesis covers ADHD neurology, Camus, Kubernetes and Rust type theory. Tagging all of that yields a tag co-extensive with the vault, which cannot filter anything. The tag instead bounds the topic the anchor *is about* rather than the topics it *ranges over*.

### Members

**SoT (10)** — Knowledge Architecture (Associative Ontology) · Virtual Knowledge Graph Paradigm · Knowledge Compiler (Argument Graph Spec) · Typed Edge Vocabulary · ProdOS Frontmatter Contract · Order Theory & Lattices · Order Theory · Evolutionary Note System · Structure is Truth is a Unifying Axiom Across Formal Systems · Formal Context (Applied Formal Methods)

**MoC (6)** — Order Theory · Meta MOC - The Core Domains · The Unified Systems Paradigm · From Information to Knowledge · PKM as Process vs Product · Applied Formal Methods

**Claims / atoms (34)** — the flat-vs-hierarchy family (Claim - Flat associative structure beats rigid hierarchy, Practice - Flat linking and tagging, Rhizome Structure, both Folgezettel notes, Alphanumeric IDs Are Addresses Not Categories, Bottom-Up Organization Allows Emergent Structure); the navigation family (Hub Notes, Keyword Index, Structure Notes as Maps of Thought Trails, Visual Containment); the proposition-centred family (both Proposition-Centred notes, PKM should probably be proposition-centred); the note-lifecycle family (Main/Literature/Fleeting Notes, Note Status Lifecycle, Immutability Principle, Deep Processing, Zettelkasten System Essence, Writer Thinking vs Archivist Thinking); the linking family (Creating Meaningful Links, Linking as a Redundancy Reduction Strategy, Key questions when linking notes, Typed Links for Knowledge Context); plus Network Topology of a PKM Vault, Layered Knowledge Architecture, Knowledge Linting, The Ladder of Abstraction, the four PKM-as-X notes, Local-First Obsidian.

### Deliberately excluded

- [[CUE Lattice Model]], [[Configuration Unification]] — genuine instances of §5's lattice/meet claims, but their topic is CUE, not knowledge structure. Adjacent cluster, not this one.
- [[MOC - ADHD and PKM Systems]] — about the human's processing capacity, not the architecture.
- `_link_report_*`, `Main Topics of Interest`, `Reference - Vault Interest Map` — generated index artefacts.

---

## 3. Typed edges

28 edges added across 20 notes. `edge_lint.py --path .` → **0 errors, 0 warnings** (2306 notes, 287 edges in 71 notes).

### The anchor's own thesis, made machine-checkable

The note claims to unify six domains. That claim is now an edge set:

```
SoT - Knowledge Architecture  synthesizes  → PRODOS Core Specification (I)
                                           → ADHD Neurology & Core Concepts (II)
                                           → The Data-Centric Philosophy (III)
                                           → Generative Infrastructure Configuration Framework (IV)
                                           → Logotherapy and the Will to Meaning (V)
                                           → The Universal Speed of Causality (VI)
                              depends_on   → SoT - Order Theory & Lattices   (§5)
```

### Successors pointing back at it

- [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]] `extends` the anchor — this is the rigorous restatement of §4's "Structure determines Behavior", derived from Formal Concept Analysis rather than asserted.
- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] `implements` the anchor — §2's Relationship Matrix (`Informs`/`Extends`/`Catalyses`/`Intersects`) is the direct ancestor of the six-term controlled vocabulary.
- [[MOC - The Unified Systems Paradigm]] `extends` the anchor.

### The flat/associative justification chain

`Claim - Flat associative structure beats rigid hierarchy` now `supports` the anchor and is itself supported by six notes: Rhizome Structure, both Folgezettel notes, Alphanumeric IDs Are Addresses Not Categories, Bottom-Up Organization, Network Topology of a PKM Vault. `Practice - Flat linking and tagging` `implements` it.

### Navigation, ordering, compiler stack

- Hub Notes `depends_on` Rhizome Structure; Keyword Index and Structure Notes both `extend` Hub Notes.
- Knowledge Compiler `depends_on` Typed Edge Vocabulary; Typed Edge Vocabulary `implements` Typed Links for Knowledge Context.
- Formal Context `supports` Structure is Truth; Applied Formal Methods `depends_on` Formal Context.

---

## 4. Tensions surfaced, not resolved

Per §6, these are flagged rather than adjudicated.

1. **The tag itself is contested by the vault.** [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]] and [[PKM should probably be proposition-centred, not topic-centred]] argue that topic-based organisation is epistemically inert. This run just built a topic tag. No `contradicts` edge was written because no note asserts the topic-centred position — the tension is between a claim and a practice, not between two claims.

2. ~~**Two competing unification hubs.**~~ **RESOLVED 2026-07-27 — see §6.** The anchor has been archived and superseded.

3. **Note immutability vs the merge protocol.** [[Immutability Principle - Preserve Original Notes]] says never revise, always append a contradicting note. [[SoT - Evolutionary Note System]] says squash HEAD drafts into SoTs and delete the draft. Arguably compatible (different note types), arguably not. No edge written.

4. **Anchor frontmatter is non-conformant.** `conformant: false`, `non_conformance_reason: "Bulk inferred type. Needs review."`, `last_reviewed: null`, legacy `status`/`updated` keys. Not fixed — that is [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] work, outside this scope.

---

## 5. Validation

- `edge_lint.py --path .` — 0 errors, 0 warnings.
- YAML frontmatter parsed on all 50 tagged notes — 0 failures, no duplicated `tags:`/`modified:` keys, tag applied exactly once each.
- Diffs verified surgical (2–4 lines per note plus the appended edge block).
- `--why "SoT - Knowledge Architecture (Associative Ontology)"` now returns a resolved justification tree bottoming out on 7 leaves. `--impact` still returns none — nothing yet declares a dependency *on* the anchor via `depends_on`.
- Vault audit delta: gaps 21 → 23, bedrock 15 → 22 (two newly load-bearing claims need grounding).

---

## 6. Supersession of the anchor (second pass, 2026-07-27)

### Diagnosis

Not "two competing hubs" — **three jobs in one note**, each done better elsewhere:

| Job | Anchor | Successor | Why the successor wins |
|:---|:---|:---|:---|
| The thesis | §4, four asserted sentences | [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]] | Supplies a mechanism (complexity conservation), three falsification tests (Absence/Drift/Elimination), FCA derivation, and names four of its own gaps |
| Topography | §1 + §3 (six domains, d2 diagram) | [[Meta MOC - The Core Domains]] | Routes via MoCs and triage hubs rather than raw SoTs; no dead links |
| Membership criteria | §5, order theory as illustration | [[MOC - Applied Formal Methods]] | Per-level admission tests with explicit fail signals |
| **Inter-domain dynamics** | **§2 Relationship Matrix** | **nothing existed** | **harvested — see below** |

### Changes made

1. **Harvested** §2 into [[Claim - Domains relate through named relations, not undifferentiated association]] — a conformant `ClaimNote` (proposition, epistemic_status, counter-positions, crux, falsifier). It carries the matrix verbatim plus provenance, and names the lineage from the informal four relations (`Informs`/`Extends`/`Catalyses`/`Intersects`) to the six-term controlled vocabulary.

2. **Declared supersession on the successor**, following the vault's only working precedent ([[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] declares `supersedes: ["[[Typed-Answer-Contract-RAG]]"]`): `supersedes: ["[[SoT - Knowledge Architecture (Associative Ontology)]]"]`. `superseded_by` was *also* populated on the anchor for the benefit of a human reading it — note that the field is otherwise dead in this vault (present on 55 notes, populated on zero).

3. **Archived the anchor in place** — `status: archived`, `prodos.lifecycle: archived`, `prodos.trust: low`, plus a `> [!warning]` banner at the top routing readers to the three successors. The file is **not** deleted, per [[Immutability Principle - Preserve Original Notes]].

4. **Rehomed all five inbound justification edges** so nothing live rests on an archived note:

| Source | Was | Now |
|:---|:---|:---|
| SoT - Structure is Truth | `extends` → anchor | **deleted** — supersession is not an `extends` relation; the vocabulary has no term for it, so it belongs in frontmatter |
| SoT - Typed Edge Vocabulary | `implements` → anchor | `implements` → harvested claim |
| MOC - The Unified Systems Paradigm | `extends` → anchor | `extends` → SoT - Structure is Truth |
| Claim - Flat associative structure | `supports` → anchor | `supports` → SoT - Structure is Truth |
| Network Topology of a PKM Vault | `supports` → anchor | `supports` → SoT - Structure is Truth |

5. **Grounded the harvested claim.** It initially had only `extends` (out) and `implements` (in) — neither is a justification relation, so it was invisible to `--audit`. Added `SoT - Knowledge Compiler (Argument Graph Spec)` `supports` → harvested claim: the compiler's `--why`/`--impact` traversals are only definable over typed edges, which is the claim's own stated evidence.

6. **Harvested claim `extends`** [[Claim - Flat associative structure beats rigid hierarchy]] — flat association is the substrate; typed relations are what make it navigable.

### Verification

- `edge_lint.py --path .` → **0 errors, 0 warnings** (2308 notes, 288 edges in 71 notes).
- `--impact "SoT - Knowledge Architecture (Associative Ontology)"` → no dependents. Nothing rests on the archived note.
- `--why "SoT - Structure is Truth..."` → the seven-leaf justification tree that previously hung off the anchor now hangs off the successor, intact.
- `--why "Claim - Domains relate through named relations..."` → grounded via Knowledge Compiler → Typed Edge Vocabulary.
- Remaining `[[wikilinks]]` to the anchor (7 notes) are prose/navigational, not typed edges. Readers following them land on the archived banner and get redirected.

### What was deliberately not done

- **The anchor's seven outbound edges were kept** (6 × `synthesizes` to the domain SoTs, 1 × `depends_on` → Order Theory & Lattices). They are the historical record of what the note claimed. They make nothing depend *on* the anchor, so they do not pollute the live graph.
- **`conformant: false` left as-is on the anchor.** An archived note should not be re-certified.
- **`[[Protocol - AFM Vault Constitutional Triage]]` is a pre-existing dangler** in [[SoT - Structure is Truth...]], referenced twice. Not introduced by this work; not fixed.

### Reversibility

Every change is a git diff. `git checkout -- 30_Library/` restores the prior state; the harvested note is untracked and can simply be deleted.