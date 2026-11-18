---
aliases: [Argument Compiler, Argument Graph, Belief Tracing, Knowledge Compiler]
conformant: true
contrasts_with: ["[[The Danger of Perpetual System-Building]]", "[[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]]"]
created: 2026-07-24T00:00:00+00:00
modified: 2026-11-17T21:48:44+00:00
permalink: llmeon/30-library/so-t/so-t-knowledge-compiler-argument-graph-spec
project_category: prodos
see_also: ["[[SoT - Human vs AI Cognition]]", "[[SoT - Typed Answer Contract (TAC) for LLM Output]]", "[[SoT - Unified Writing to Think Process]]"]
status: stable
tags: [domain/pkm, topic/knowledge-architecture, topic/knowledge-graph]
tension: ["[[Cognitive Scaffolds Are Constitutive but Lack Formal Closure]]"]
title: SoT - Knowledge Compiler (Argument Graph Spec)
type: sot
upstream: ["[[SoT - Processing IS the Work]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - The Extended Mind]]"]
---

> Canonical status: this note specifies the semantics, cognitive boundary, and compiler capabilities of the knowledge graph—what the tool _computes_ and _answers_. Its sibling [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] fixes the syntax (how edges are written and resolved). The validator/compiler is `10_System/scripts/edge_lint.py`; alongside Dataview and K-Plex (`.obsidian/plugins/k-plex/`), it forms the vault's three-reader architecture.

## Minimum Viable Understanding (MVU)

The vault holds atomic claims (`type: claim`). A typed edge records _why_ one claim stands (`[supports:: [[Target]]]`, `[depends_on:: [[Target]]]`, `[contradicts:: [[Target]]]`). Once enough claims are wired this way, the collection stops being a pile of notes and becomes a directed argument graph that a computer can interrogate in ways biological working memory cannot hold in RAM:

- _Where is my argument unsupported?_ (C1 gaps: a load-bearing claim with nothing beneath it).
- _What are my actual foundations?_ (C2: declared axioms vs. smuggled assumptions vs. empirical bedrock).
- _Where do I contradict myself?_ (C3: explicit conflicts, live tensions, and circular reasoning).
- _Why do I believe X, and what falls if X falls?_ (C4: provenance and impact trees).
- _What already exists near a new thought?_ (C5: token-overlap routing at ingest so duplicates never silently land).

Three readers share one on-disk edge syntax: `edge_lint.py` compiles the whole argument graph, Dataview answers live single-hop queries, and K-Plex projects relationships onto the interactive Idea Compass, Mind Map, and Facets views. The computer is a strict epistemic bookkeeper, not a truth oracle or surrogate thinker: it surfaces structural blind spots so the human author is forced to think deeper, ground claims, or drop illusions.

---

## 1. Vision, Scope & The Cognitive Division of Labour (ProdOS Alignment)

In scope. Claim notes (and `content-block` blocks) participating in reasoning via justification edges, compiled by `10_System/scripts/edge_lint.py` and surfaced report-only—never auto-edited.

Explicitly out of scope.

- Not all content is argumentation. Procedures, MoCs, journals, and reference notes never get flagged for "missing support" unless they emit or receive justification edges (`not is_claim` leaf nodes with outgoing `supports` count as non-claim bedrock). `SoT` notes (`type: sot`) are composite argument threads built _on_ claims (`[depends_on:: [[Claim]]]` for load-bearing premises and `[synthesizes:: [[Note]]]` for transcluded components), not leaf bedrock.
- Not a logic engine. No formal soundness or truth oracle: `[supports:: [[Target]]]` records a human bookkeeping assertion. The compiler verifies graph _shape_, not logical validity.
- No belief enforcement. The tool exposes structural gaps, cycles, and conflicts; resolving them is always a human decision.

### 1.1 Enhancing Thinking vs. Replacing It (The ProdOS Boundary)

ProdOS enforces a hard boundary between Execution and Learning ([[SoT - PRODOS Core Specification]] §3 & §5, [[SoT - Processing IS the Work]] §6):

- GTD Execution (_Rule of Zero Toil_): Administrative sorting, tagging, and task routing waste ADHD executive function and are safely offloaded to the LLM Chief of Staff ([[Protocol - Action-First GTD (LLM Chief of Staff)]]).
- PKM & Sense-Making (_Productive Friction / Eufriction_): Understanding cannot be outsourced. Cognitive strain is not a cost to eliminate—it is the mechanism that builds mental models and competence ([[Eufriction - Productive Friction Strengthens Thinking]], [[Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence]]). If an agent drafts propositions or stitches ideas silently, the vault grows in file count while human comprehension atrophies ([[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]], [[PKM Generates Unique Insights via Personal Context That AI Cannot Replicate]]).

Therefore, the Knowledge Compiler divides labour cleanly between silicon and mind ([[SoT - The Extended Mind]], [[SoT - Human vs AI Cognition]]):

| Responsibility | Computer (`edge_lint.py` + K-Plex + Agents) | Human Author (Leon) |
|:--- |:--- |:--- |
| Memory & Traversal | Hold 700+ nodes in index; trace multi-hop `--why`/`--impact` chains and DFS cycles beyond working memory ([[Writing Acts as an External Working Memory]]). | Interpret meaning, run causal mental simulations, and judge whether a purported reason actually holds. |
| Epistemic Diagnosis | Flag C1 unsupported load-bearing claims, C3 live tensions, dangling edges, and near-duplicate ingest candidates (`--route`). | Decide whether to research/write support, narrow scope into a `HEAD` tension, set `axiom: true`, or discard the claim. |
| Authorship & Grounding | Enforce report-only TAC discipline ([[SoT - Typed Answer Contract (TAC) for LLM Output]]); never touch `own_words: true` notes (`AGENTS.md` §6). | Author genuine claims in own words ([[SoT - Unified Writing to Think Process]]), supplying lived experience and symbol grounding. |

- Forcing Function Against IoED: By catching load-bearing claims that lack upstream evidence or axiom flags, the compiler breaks the Illusion of Explanatory Depth ([[SoT - Illusion of Explanatory Depth (IoED)]]) and sends the author back into [[SoT - Unified Writing to Think Process]] (Stages 3–5) or a `HEAD - <question>?` workbench note ([[SoT - HEAD Note Contract (The Workbench)]]).
- Formal Closure Limit & Anti-Tinkering Guardrail: Unlike compiler type-checkers or infrastructure state reconciliation engines, cognitive scaffolds lack formal closure against reality ([[Cognitive Scaffolds Are Constitutive but Lack Formal Closure]]). Tooling serves inquiry—expanding compiler complexity without exercising it on real claims violates the anti-tinkering guardrail ([[The Danger of Perpetual System-Building]], [[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]]).

---

## 2. The Model (Minimal)

Three primitives govern the argument graph; note-level YAML conformance and atomic proposition quality are gated alongside it by `10_System/scripts/validate_note_frontmatter.py` ([[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]) and `10_System/scripts/validate_note_shape.py` ([[SoT - Atomic Note Standard (The Proposition Card)]]):

| Primitive | What it is | How it's written |
|:--- |:--- |:--- |
| Claim node | An atomic assertion that can be true or false. | A note `type: claim`, or a `<!--content-block-start type="claim" id="…"-->` block. |
| Justification edge | A directed "reason" or conflict relationship. | An inline typed edge (§4): `[supports:: [[Target]]]`, `[depends_on:: [[Target]]]`, `[contradicts:: [[Target]]]`. |
| Axiom marker | Declares a claim _foundational_—deliberately chosen premise, ungrounded by design. | `axiom: true` in frontmatter (note-level), or `axiom="true"` on the `content-block-start` comment (block-level). |

---

## 3. What the Compiler Computes (Capabilities C1–C5)

Direction convention in `10_System/scripts/edge_lint.py`: `A [supports:: [[B]]]` adds `(A, B)` to the justification graph (`sup_out[A] += 1`, `sup_in[B] += 1`), read _"A is a reason for B"_. `A [depends_on:: [[B]]]` adds `(A, B)` (`dep_out[A] += 1`, `dep_in[B] += 1`), read _"A presupposes B"_.

### C1—Gap Detection (`--audit`)

- Definition: A `type: claim` node that is load-bearing (`sup_out >= 1`, `dep_in >= 1`, or synthesized by an `sot` node) while ungrounded (`sup_in == 0` and not `axiom: true`).
- Answers: _"Where does my argument assert something load-bearing without grounding it?"_
- Why: Isolated claims with no edges stay silent. A claim doing load-bearing work forces an explicit human choice: supply incoming support, or consciously mark `axiom: true`.

### C2—Foundation Audit (`--audit`)

Reports three foundation sets:

1. Declared axioms: participating nodes with `axiom: true`.
2. Undeclared foundations: the C1 gap set (load-bearing claims not yet grounded or marked `axiom: true`).
3. Non-claim bedrock: non-claim, non-axiom, non-SoT leaf nodes (`evidence`, `source`, `journal`, etc.) with `sup_out >= 1`—legitimate external leaves that ground claims without needing support themselves. `SoT` nodes are reported separately as composite argument threads.

### C3—Conflict & Tension Detection (`--audit`)

Checks three conflict shapes in the graph:

1. Explicit contradiction edges: any `[contradicts:: [[Target]]]` edge.
2. Live tensions: `type: claim` nodes that are simultaneously supported (`sup_in >= 1`) and in conflict (`contra >= 1`)—held beliefs you have argued both for and against.
3. Circular reasoning: directed DFS cycles in the combined `supports`/`depends_on` graph.

- Contradiction vs. Scoped Tension Gate ([[Prompt - Vault Ingest Router]] Gate 3): Before adding `[contradicts::]`, apply the assumption probe: _"Can both claims hold if you change one background assumption?"_ If yes, keep both valid and record a scoped tension (`> Open threads:` → `HEAD` note or `tension:` frontmatter). If no (shared assumption violated), emit `[contradicts:: [[Target]]]`.
- Deferred: derived transitive contradictions (`X` supported by `A` and something contradicting `A`).

### C4—Provenance & Impact Thread-Pulling (`--why <TITLE>`, `--impact <TITLE>`)

- `--why <TITLE>`: Traverses incoming `supports`, outgoing `depends_on`, and `sot` `synthesizes` edges down to axioms and bedrock leaves (_"Why do I believe X, down to bedrock?"_). Pass `--include-structural` to also traverse `extends`/`implements` and non-SoT `synthesizes`.
- `--impact <TITLE>`: Traverses outgoing `supports` and incoming `depends_on` (_"If X falls, what else collapses?"_).

### C5—Ingest Routing, Graph Export & Regression (`--route`, `--export-json`, `--regress`)

- `--route "<proposition>"`: Jaccard token-overlap matcher against graph-participating claims (displaying `grounded` / `axiom` / `GAP` status) plus unwired vault claims, used by [[Prompt - Vault Ingest Router]] Gate 1 so new thoughts attach to the existing graph rather than landing as duplicate orphans.
- `--export-json <file>`: Exports resolved nodes and edges as structured JSON.
- `--regress`: Runs deterministic self-contained fixture cases in `10_System/evals/structural/` covering target resolution, syntax masking, and lint warnings.

---

## 4. Relationship Vocabulary & K-Plex Visual Projection

The full controlled vocabulary is defined in [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] (7 closed predicates):

| Edge | Meaning (Source → Target) | Compiler Role (`edge_lint.py`) | K-Plex Idea Compass Axis |
|:--- |:--- |:--- |:--- |
| `supports` | Source is evidence or reason for Target. | Argumentation (`--audit`, `--why`, `--impact`) | West (`supports` ↔ `supported_by`) |
| `depends_on` | Source presupposes Target as a premise. | Argumentation (`--audit`, `--why`, `--impact`) | North (`depends_on` ↔ `prerequisite_of`) |
| `contradicts` | Source conflicts with / negates Target. | Conflict (`--audit`: contradictions, live tensions) | East (`contradicts`, symmetric) |
| `extends` | Source builds on or specialises Target. | Syntactic / resolution validation only | North (`extends` ↔ `extended_by`) |
| `implements` | Source concretises abstract Target. | Syntactic / resolution validation only | North (`implements` ↔ `implemented_by`) |
| `synthesizes` | Hub summarises component Targets. | Syntactic / resolution validation only | South (`synthesizes` ↔ `synthesized_in`) |
| `revises` | Source updates an earlier formulation. | Syntactic / resolution validation only | Sequence (`revises` ↔ `revised_by`) |

- K-Plex Visual Layer: Because `inferAllLinksAsFriends: false` in K-Plex, only typed inline `[…]` edges and configured frontmatter fields render on Compass (`classic`), Mind Map (`mindmap`), and Facets (`wuxing`, grouping nodes by `type` via `prodos-types` and lifecycle `status` via `prodos-status`). Never duplicate an inline typed-edge target in frontmatter `see_also` (`frontmatter-overrides-body-ontology` precedence collapses North/South/East roles into West).

---

## 5. Implementation Status & Live Vault Baseline

| Phase | Capability | Tooling | Status |
|:--- |:--- |:--- |:--- |
| v0 | Controlled vocabulary & wikilink target resolution | `edge_lint.py` | Live |
| v1 | C1 Gap detection & C2 Foundation audit | `edge_lint.py --audit` | Live |
| v2 | C3 Conflict detection (contradictions, live tensions, DFS cycles) | `edge_lint.py --audit` | Live |
| v3 | C4 Justification provenance & impact trees | `edge_lint.py --why` / `--impact` | Live |
| v3.5 | C5 Ingest claim routing, JSON graph export, fixture regression suite, K-Plex Compass/Facets | `--route`, `--export-json`, `--regress`, `k-plex` | Live |
| v4+ | Derived transitive contradictions, strength-weighted propagation |—| Deferred |

- Live Vault Baseline (2026-11-14): `edge_lint.py --audit` indexes 792+ participating nodes, 950+ justification edges, and 52 contradiction edges (`95 gap(s), 98 axiom(s), 113 bedrock, 52 contradiction(s), 10 live tension(s), 44 cycle(s)`).
- Operational Workflows: Maintained via [[Prompt - Vault Ingest Router]] (pre-write routing), [[Note Refresh & Link Auditor]] (note-level wiring), [[Justification Graph Audit & Gap Closure]] (human-approved axiom/support closure), and [[Prompt - Vault Graph Programme (Session Driver)]].

---

## 6. Simplicity Guards (Non-goals)

- Report-only, always. The compiler diagnoses; it never rewrites a note (mirrors `edge_lint.py`, TAC `UNSURE` discipline in [[SoT - Typed Answer Contract (TAC) for LLM Output]], and `own_words: true` protection in `AGENTS.md` §6).
- Opt-in graph. Silence on non-argument notes is by design.
- No computed truth maths. `strength` (1–5) and `confidence` (`high`/`medium`/`low`) stay advisory human markers rather than automated truth weights ([[SoT - Typed Answer Contract (TAC) for LLM Output]]).
- Minimal schema. One boolean (`axiom: true`) and one closed 7-predicate set; add structure only when real reasoning proves it necessary.

---

## 7. Open Questions (Deferred Decisions)

- Block-level vs. note-level claims: Keep preferring atomic note-level claims (`validate_note_shape.py`) until block-level arguments prove essential.
- Structural provenance flag: `--why --include-structural` and `--impact --include-structural` are live in `edge_lint.py` (alongside automatic traversal of `sot` `synthesizes` edges).

---

## 8. Related Architecture & Epistemic Claims

- [[SoT - PRODOS Core Specification]]—_Implements Phase 2 Refinement & Architect Mode graph verification._ [implements:: [[SoT - PRODOS Core Specification]], strength=5, confidence=high]
- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—_Depends on the closed 7-predicate syntax and K-Plex Compass mapping._ [depends_on:: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], strength=5, confidence=high]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Depends on `type: claim`, `status`, and `axiom` metadata schema._ [depends_on:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], strength=4, confidence=high]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Depends on atomic, single-proposition notes so graph edges remain clean and unambiguous._ [depends_on:: [[SoT - Atomic Note Standard (The Proposition Card)]], strength=4, confidence=high]
- [[Claim - Domains relate through named relations, not undifferentiated association]]—_Provides the machine-checkable graph capabilities that make typed relations load-bearing._ [supports:: [[Claim - Domains relate through named relations, not undifferentiated association]], strength=4, confidence=high]
- [[SoT - Processing IS the Work]]—_Operationalises the PKM half of Processing IS the Work by exposing structural gaps for human synthesis rather than automating thinking._ [supports:: [[SoT - Processing IS the Work]], strength=4, confidence=high]
- [[SoT - Illusion of Explanatory Depth (IoED)]]—_Acts as a structural forcing function that exposes ungrounded assumptions hiding behind familiarity._ [supports:: [[SoT - Illusion of Explanatory Depth (IoED)]], strength=4, confidence=high]
- [[Eufriction - Productive Friction Strengthens Thinking]]—_Synthesises desirable cognitive friction into automated gap detection that prompts deeper human elaboration._ [synthesizes:: [[Eufriction - Productive Friction Strengthens Thinking]], strength=4, confidence=high]
- [[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]]—_Synthesises the boundary that digital tools handle storage, retrieval, and graph traversal while understanding stays human._ [synthesizes:: [[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]], strength=4, confidence=high]
- [[PKM Generates Unique Insights via Personal Context That AI Cannot Replicate]]—_Synthesises the principle that human lived context supplies the meaning behind every connection._ [synthesizes:: [[PKM Generates Unique Insights via Personal Context That AI Cannot Replicate]], strength=4, confidence=high]
- [[Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence]]—_Synthesises the rule that propositions and arguments must be authored by the human, never auto-generated._ [synthesizes:: [[Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence]], strength=4, confidence=high]
- [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]]—_Synthesises the closed-vocabulary and contradiction-vs-tension design lessons into the production compiler._ [synthesizes:: [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]], strength=3, confidence=high]
