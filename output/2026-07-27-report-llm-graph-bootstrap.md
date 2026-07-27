---
title: 'LLM Graph Bootstrap — First-Pass Survey of the LLM/PKM Cluster'
output_type: report
created: 2026-07-27 00:00:00+00:00
tags:
- output
- knowledge-graph
- typed-edges
- domain/llm
- domain/pkm
permalink: llmeon/output/2026-07-27-report-llm-graph-bootstrap
---

> **Output Contract:** [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]. Confidence stated per section; evidence is a vault path; `UNSURE` items listed in §Validation.
> **Write scope:** proposal-only. No canonical note, conflict note, timeline note, MoC or SoT was authored or edited. No typed edge was written. This file is the entire write footprint (AGENTS.md §2.3).

## Headline

**The LLM/PKM cluster is the largest unwired region of the vault.** `edge_lint.py --audit` reports 288 typed edges across 71 notes, forming a 158-node justification graph — and **not one node in it is an LLM, agent, context-engineering or RAG note.** The graph is entirely ADHD neurology, epistemology, Folgezettel/Zettelkasten theory, Covey, and formal methods.

The single exception is a PKM/LLM *bridge* pair already inside the graph as bedrock:

- `Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines` — supports 1
- `PKM should probably be proposition-centred, not topic-centred` — supports 1
- `Network Topology of a PKM Vault Determines Its Cognitive Properties` — supports 2

So the entry point already exists. What is missing is everything downstream of it.

This is not a thin cluster. It is a **deep, well-written, entirely associative** one: ~223 notes with a mature five-layer structure (MoC → SoT → atom/claim → wiki dossier → raw Pieces capture), a live index note ([[MOC - AI Software Engineering]]) that already narrates the arguments in prose, and several notes that state their own relationships explicitly in body text ("this is a specific instance of…", "the architectural response to…"). Those prose statements are exactly the edges the compiler cannot see.

---

## Search Coverage

**Tooling tier actually reached: 3 — raw filesystem.** This is the weakest tier and the coverage claim below is downgraded accordingly.

| Tier | Status |
|---|---|
| 1. `obsidian-mcp-tools` via 1MCP | **Unavailable.** No `obsidian-mcp-tools_1mcp_*` tool is exposed in this session; only `codemod`, `context7` and `sequential-thinking` are surfaced from the 1MCP bridge. `curl http://127.0.0.1:3050/health` is unreachable — this session's shell is a network-isolated Linux sandbox, not the host, so it cannot see `127.0.0.1:3050` even when 1MCP is running on the Mac. |
| 2. `obsidian` CLI | **Unavailable.** `which obsidian` → not found in the sandbox. |
| 3. Filesystem | **Used.** Vault mounted read/write; `edge_lint.py` runnable (Python 3 + PyYAML present). |

**Consequence:** this survey is **lexical, not semantic**. Every finding below rests on filename patterns, a 1,800-character head-of-body keyword scan, and full reads of ~60 notes. A note phrased entirely in vocabulary I did not guess would be invisible to it. Treat the coverage as *high for anything using the words* `llm / agent / prompt / context / RAG / MCP / retrieval / token / model`, and *unquantified* for anything else.

**Themes searched:** prompt engineering · context engineering · agent orchestration & harness design · coding copilots & pair programming · RAG and retrieval · memory and working-set management · PKM workflows & knowledge-graph construction · evaluation and verification · workflow automation · model choice/routing/trade-offs.

**Query styles used, all three:**

- *Literal anchors* — `LLM`, `PKM`, `prompt engineering`, `agent orchestration`, `MCP`, `RAG`, `context window`.
- *Conceptual variants* — `working set`, `long context`, `multi-agent`, `human in the loop`, `hallucination`, `vibe coding`, `pair programming`, `evaluation harness`.
- *Functional equivalents* — head-of-body keyword density scan over all of `30_Library/`, `20_Thinking/`, `wiki/`, `Claims/`, which caught 55 notes whose filenames contain none of the anchor terms (`Harness Engineering`, `Context Volume Plateau`, `Shift to Verification`, `Work Slop Proliferation`, `Knowledge Linting`, `Framework Cross-Pollination`, …).

**Result:** 223 notes in scope. Full frontmatter + lead-paragraph read on ~60; full-text read on 14.

### Notable gaps

| Gap | Real, or an artefact of lexical search? |
|---|---|
| **Prompt engineering as a live topic** — one note only (`Prompt Architecture Levels`, zero/few-shot/CoT). Everything else treats prompting as the *superseded* practice. | **Real.** Consistent with the timeline shift in §Timeline Shifts. Only 6 files mention "prompt engineering" at all, and 4 of those are defining it in order to reject it. |
| **Memory / working-set management** — thin. `LLM Context Constraints`, `Context Volume Plateau`, `Layered Knowledge Architecture`, `SoT - Agentic AI Design Patterns` §D. No SoT owns it. | **Probably real.** "working set" appears in 4 files, "long context" in 1. |
| **Model choice / routing** — split between two zettels (`Small Models Should Execute Structured Tool Calls…`, `LLMs Exhibit Divergent Strengths…`) and the `wiki/projects/Hermes-*` operational pages. No canonical note. | **Real, and the most cleanly closable gap.** The wiki layer has the operational detail; the claim layer has nothing to attach it to. |
| **Cost** — `Continuous Autonomous Agent Loops Incur Significant API Cost`, `wiki/projects/Token-Usage.md`, `Hermes Cost Optimisation`. Isolated. | Real but low-value to wire. |
| **Evaluation** — well covered (`Evaluation Pipelines Should Distinguish…`, `Objective`/`Subjective Task Validation`, `TDD in Probabilistic Systems`, `Cross-Model Adversarial Auditing`, `Optimal Iteration Count`). Zero edges between any of them. | Not a knowledge gap — a **wiring** gap. |
| Anything outside my keyword set | **Unknown.** This is the honest limit of tier 3. |

Confidence: **high** on what was found; **medium** on completeness.

---

## Candidate Canonical Notes

Recommendations for the human. **No files created.**

| # | Candidate | Why it matters | Evidence found | Confidence |
|---|---|---|---|---|
| 1 | **`SoT - Flow Engineering`** (exists — promote to cluster spine) | It is the only note that names the *mechanism* the whole cluster keeps circling: constraints enforced by a deterministic wrapper, not by prompt text. `MOC - AI Software Engineering` §6 already frames it as "the architectural response to the Anthropomorphism Trap". Everything from MVC gates to TAC to the RPI workflow is an instance of it. | `30_Library/SoT/SoT - Flow Engineering.md` (`source_of_truth: true`) | high |
| 2 | **`SoT - LLM Semantic-Statistical Mismatch`** (exists — the cluster's axiom) | This is the load-bearing premise under most of the cluster: an LLM is a next-token engine, so human-centric instruction is a statistical filter. Nothing in the vault grounds it and nothing declares it. It is the strongest `axiom: true` candidate in the domain. | `30_Library/SoT/SoT - LLM Semantic-Statistical Mismatch.md`; corroborated by `AI as Statistical Interpolation`, `Claims/LLMs_are_map_only_engines.md`, `SoT - Human vs AI Cognition` | high |
| 3 | **A context-engineering canon** — pick **one** of `SoT - Context Engineering` / `SoT - The RPI Workflow (Context Engineering)` / `SoT - The Context Engine` as the parent | Three SoTs, one topic, three different framings (discipline / workflow / architecture-history). `SoT - Context Engineering` is the most abstract and reads as the natural parent; the other two are its implementations. | all three in `30_Library/SoT/`; see Duplicate Cluster A | high |
| 4 | **Model routing / capability trade-offs** — **does not exist**; propose as a claim stub | Confirmed absent by title, alias and path search. The vault has the operational evidence (`wiki/projects/Hermes-Multi-Model-Routing-Strategy.md`, `Hermes Cost Optimisation - Free Model Routing Strategy`) and two orphan claims, but no node to hang them on. | absence verified; see §Verification method | medium |
| 5 | **"Verifiability drives autonomy"** — a real candidate hiding in plain sight | `Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable` and `Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains` are the same underlying mechanism seen from two sides, and they explain *why* `Shift to Verification` and `TDD in Probabilistic Systems` matter. One of the two existing notes should become the canonical statement. | both exist in `100_zettelkasten/` | medium |
| 6 | **`SoT - LLM Wiki Pattern`** (exists — the PKM-side spine) | The one SoT that connects the LLM half of the vault to the PKM half, and the one this vault claims to *be an instance of*. Its ProdOS-isomorphism section is the natural anchor for the whole `wiki/` layer. | `30_Library/SoT/SoT - LLM Wiki Pattern.md` (`source_of_truth: true`) | high |

---

## Duplicate Clusters

| Cluster | Member notes | Merge recommendation |
|---|---|---|
| **A. Context engineering (3 SoTs)** | `SoT - Context Engineering` · `SoT - The RPI Workflow (Context Engineering)` · `SoT - The Context Engine` | **Do not merge — hierarchise.** They are genuinely different objects: a discipline, a workflow, and an architecture post-mortem. Make the first the parent and wire the other two with `implements`. |
| **B. Complexity conservation (2 SoTs, near-identical openers)** | `SoT - Complexity Conservation` · `SoT - Conservation of Complexity` | **Merge — highest priority.** Both open with "Software complexity obeys a conservation law". This is a straight duplicate at SoT level, and it currently blocks a clean `depends_on` target for the LLM corollary. Human decides which title survives. |
| **C. The LLM complexity corollary (2 notes)** | `SoT - LLM Reasoning Obeys the Complexity Conservation Law` · `LLM Reasoning Efficiency is Proportional to Structural Constraint` | **Merge.** Same thesis, same wording ("LLMs fail not because they lack intelligence… procedural entropy instead of structural constraint"). Keep the SoT; fold the zettel in, or demote the SoT to the zettel and keep the atom. |
| **D. RPI workflow (2 notes)** | `SoT - The RPI Workflow (Context Engineering)` · `Research-Plan-Implement Workflow` | **Merge or subordinate.** The zettel is a summary of the SoT with no additional content. |
| **E. Iteration ceiling (2 notes)** | `Automated Optimization Loops Degrade Beyond 15 Iterations` · `Optimal Iteration Count` | **Merge.** Identical claim, identical numbers (5–10 converge, >15 degrades), differing only in whether the cap is stated as 10 or 15. |
| **F. Jevons for code (2 notes)** | `Software Jevons Paradox` · `Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers` | **Merge.** Same claim; the second is the fuller statement. (`Jevons Paradox of Attention` is a *different* claim — keep separate.) |
| **G. The oversight shift (3–5 notes)** | `Shift to Architectural Oversight` · `Shift to High-Level Oversight` · `Shift to Verification` · adjacent: `Commoditization of Manual Coding`, `Agentic Collaboration Shift`, `Intent as High-Level Source Code` | **Merge the first two** (near-identical: value moves from syntax to architecture/curation). **Keep `Shift to Verification` separate** — it is a distinct and sharper claim (the bottleneck moves to *validation*, not to *architecture*). |
| **H. MCP (3 notes)** | `Model Context Protocol (MCP)` [definition] · `Model Context Protocol Standardises the LLM-to-Tool Interface` [claim] · `MCP Architecture Separates Host, Server, and LLM into Distinct Roles` [claim] | **Do not merge.** One definition + two non-overlapping claims (standardisation; role decomposition). Wire, don't fold. |
| **I. LLM wiki (2 notes)** | `SoT - LLM Wiki Pattern` · `LLM Wiki Concept` | **Do not merge.** The zettel is the atomic definition, the SoT is the full pattern. Wire `LLM Wiki Concept` → `SoT - LLM Wiki Pattern`. |
| **J. Eval routing (3 notes)** | `Objective Task Validation` · `Subjective Task Validation` · `Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts` | **Do not merge.** Two heuristics plus the claim that unifies them — a textbook `synthesizes` shape. |
| **K. Minimum viable context (3–4 notes)** | `Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries` · `Context Volume Plateau` · `Context Curation Necessity` · `Low-Context Implementation Execution` | **Do not merge.** One claim (MVC), one constraint (the plateau that motivates it), one heuristic (curate), one procedure (fresh sessions). Clean support chain. |

---

## Conflicts

### Genuine — both cannot hold under the same assumptions

**None found that I am willing to assert as a `contradicts` edge.** Every candidate I tested dissolved into an assumption difference on close reading. Recording the near-misses is more useful than manufacturing an edge:

**Near-miss 1 — `Coherent LLM output signals meaningful processing` vs `AI as Statistical Interpolation` / `Claims/LLMs_are_map_only_engines`.**
The *title* asserts coherence is evidence of meaningful processing, which the rest of the cluster flatly denies. But the *body* says the opposite of its own title: "This coherence signals **to us** that our thoughts have been processed in a meaningful way, **even if that processing is purely algorithmic**." That is a description of the Eliza Effect from the inside — fully compatible with `SoT - Human vs AI Cognition`.
**Recommended treatment: no edge. Retitle the note.** The title is a claim the body does not make, and as long as it stands it will keep reading as a contradiction to anyone (or any agent) skimming titles. Note also has `type: ''` and `status: ''`.

**Near-miss 2 — `Prompt-Injected Non-Functional Requirements` vs `SoT - Flow Engineering`.**
Flow Engineering: constraints in natural-language prompt text are unreliable; enforcement must be structural, making non-compliance *impossible*. The NFR note: reliability/observability/security requirements can be "**durably** encoded" via high-level prompt instruction.
The apparent contradiction dissolves at the NFR note's own Scope & Conditions: "*Requires an agentic harness that consistently applies these global, prompt-level instructions to all agent actions*" — i.e. the harness is the deterministic layer, and the prompt is its payload.
**Recommended treatment: prose tension, not `contradicts`.** The crux worth recording: *is a prompt instruction reliably injected by a harness a structural gate, or still a statistical filter?* Flow Engineering's own logic says the latter; the NFR note assumes the former. Neither note states the assumption, which is why they read as conflicting.

### Context-dependent tensions — prose only, no edge

There is no `context-dependent` relationship in the vocabulary and these are not `contradicts` cases. Each belongs under a `## Tensions` heading in the notes concerned, where the *why* can be written down.

| Tension | Side A | Side B | Assumption difference |
|---|---|---|---|
| **Automated consolidation vs personal-context curation** | `PKM Generates Unique Insights via Personal Context That AI Cannot Replicate` — the irreplaceable value is the human's lived context | `Proposition-Centred Notes Make Superior RAG Chunks…` and `Local-First Obsidian with MCP and RAG…` — the vault's value is as an LLM context substrate | Whether the vault's primary reader is the human or the model. Both are true of *this* vault; it serves both. **This is the most load-bearing unstated tension in the cluster** — the vault's own design sits on top of it. |
| **Cognitive strain as cost vs as mechanism** | `Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence` — strain *is* the learning | `Agent-First Implementation Cycle`, `CLI-AI Automation Can Ingest External Data Streams into Markdown Vaults` — automate the drafting | Whether the task's purpose is the artefact or the author's competence. `Work Slop Proliferation` is evidence for side A; `Desirable Difficulty in Skill Acquisition` and `Eufriction - Productive Friction Strengthens Thinking` (already in the graph) supply the general mechanism. |
| **Long context vs retrieval** | `SoT - Recursive Language Models` — RAG is "brittle for multi-hop reasoning because it relies on semantic similarity rather than logical relationships"; `SoT - LLM Wiki Pattern` — standard RAG is stateless and structurally flawed | `Retrieval-Augmented Generation (RAG)`, `Semantic Search via Embeddings`, the Qdrant notes — RAG as working mechanism | Query complexity. Single-hop factual lookup vs multi-hop reasoning. The RAG notes are *definitional*, not advocacy, so this is a scope tension rather than a disagreement. |
| **Single-agent vs multi-agent** | `Implicit Multi-Agent Coordination via Shared File System` (CORAL), `SoT - Agentic Roles` (the Surgical Team) | `Continuous Autonomous Agent Loops Incur Significant API Cost` — multi-agent runs "exceed hundreds of dollars in a single session"; `Low-Context Implementation Execution` — fresh single sessions are more precise | Cost tolerance and task horizon. Nobody has written the note that states the trade-off. |
| **Rules vs demonstrations** | `Prompt Architecture Levels` — few-shot examples as a level of prompt architecture | `SoT - Context Engineering` — "Domain Manifesto", state the laws of the universe | Not adjudicated anywhere in the vault. Genuinely open. |
| **General assistant vs task-specific agent** | `SoT - AI Agent Skill Architecture` — progressive disclosure keeps one agent lean | `SoT - Agentic Roles` — divide the cognitive load across five specialised roles | Whether context isolation is achieved by *lazy loading* or by *separate processes*. The Skill Architecture note's own Skill/MCP/Subagent table nearly resolves this; nobody has written the resolution down. |

Confidence: **medium-high**. The two near-misses were the only candidates that survived to full-text reading, and both failed on the evidence. If a genuine `contradicts` exists in this cluster, lexical search did not surface it.

---

## Timeline Shifts

**Prose only. No edges.** `supersedes` and `historically_followed_by` are not in the vocabulary, and supersession is a temporal judgement the compiler deliberately does not model.

1. **Prompt engineering → context engineering → flow engineering.** A three-step, not two-step, shift, and the vault records all three stages.
   - *Prompt engineering* survives as one note (`Prompt Architecture Levels`, Jan-era) and is elsewhere referenced only to be rejected.
   - *Context engineering* (Jan 2026, `SoT - Context Engineering`, `SoT - The RPI Workflow`) reframes the problem from wording to information density — compression over accumulation.
   - *Flow engineering* (Apr 2026, `SoT - Flow Engineering`) goes further: even a well-engineered context is still *asking*. Constraints move into a deterministic wrapper. `MVC Enforcement Structural Gates for LLM Agents` (Feb 2026) is the transitional note — it argues for structural gates before the name existed.
   **What changed:** the locus of control moved out of the prompt entirely. Stated most crisply in `SoT - Flow Engineering`: "Prompt Engineering: trying to *talk* the model into following a methodology. Flow Engineering: building a deterministic wrapper that *forces* compliance."

2. **Shadow state → structural intelligence.** Explicitly documented as a failure inside `SoT - The Context Engine`: the "Surgeon" architecture (external bead/inode databases tracking file identity) was tried and marked **FAILED** — "inodes are unstable across containers/git-clones; external databases desynchronize from the code." Replaced by tree-sitter/RepoMap/LSP, derived from the artefacts themselves. **Lesson recorded:** the codebase is the only source of truth; do not build shadow states. This is the vault's best-documented reversal and deserves to survive any merge of the context-engineering cluster.

3. **Stateless RAG → persistent LLM wiki.** `SoT - LLM Wiki Pattern` (Apr 2026) reframes retrieval as an accumulation problem rather than a search problem: knowledge should compound in a maintained wiki rather than be rediscovered per query. The vault's own `wiki/` + `raw/` + `output/` three-layer memory (AGENTS.md §1) is the implementation. `SoT - Recursive Language Models` (Jan 2026) attacks the same weakness from the inference side.

4. **Free prose → typed answer contracts.** `SoT - Typed Answer Contract (TAC) for LLM Output` (17 Jul 2026) generalises a pattern the vault had already invented locally — the `UNSURE` category in `Goal - Orphan Triage Sweep (Daily Cron)` — into a contract applied across the prompt library. The note is honest that the markdown version is "a discipline-plus-structure hybrid rather than a pure structural gate", i.e. it does not yet satisfy its own parent principle.

5. **Associative wikilinks → typed edges.** 24–25 Jul 2026: `SoT - Typed Edge Vocabulary` written, syntax migrated from `%%claim.supports{Target}%%` to the Dataview `%%[rel:: [[Target]]]%%` form across 69 edges in 21 notes, `edge_lint.py` written and put in use. **This shift has not yet reached the LLM cluster** — which is the entire finding of this report. The graph grew where the human was already arguing (ADHD, epistemology) and not where the vault has the most content.

6. **Vault-fixing prompts → vault-using prompts (incomplete).** `20_Thinking/21_Workbench/LLMeon Vault Pattern Report.md` (11 Jul 2026) diagnoses "20+ bespoke AI prompts exist to *fix the vault* rather than notes that *use* it". The typed-edge system is the first infrastructure that makes the vault answer questions rather than reorganise itself. Whether this shift completes is the open question.

---

## Proposed Typed Edges

**None written. All `UNSURE`** — the linter has not been run against them because they do not exist yet.

**Read this before evaluating them:** `edge_lint.py` line 352 sets `JUSTIFICATION = {"supports", "depends_on"}` and `CONFLICT = {"contradicts"}`. **`extends`, `implements` and `synthesizes` are vocabulary-legal but are *not* ingested by the argument audit.** They will pass the linter, appear in Dataview, and do nothing for the C1 gap list or `--why` traversal. Edges 1–4 below are the ones that change what the compiler can answer; 5–9 are navigational structure that happens to be typed.

### Justification edges (compiler-visible)

| # | Source | Edge | Target | Rationale | Validated? |
|---|---|---|---|---|---|
| 1 | `Context Volume Plateau` | `supports` | `Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries` | The plateau note states the empirical mechanism ("performance plateaus or degrades past ~50% capacity… dictates a minimal viable context approach") that the MVC claim asserts as a rule. The source note already draws the conclusion in its own body. `strength=4, confidence=high`. | UNSURE — not written |
| 2 | `Work Slop Proliferation` | `supports` | `Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence` | Work slop is the observed cost the outsourcing claim predicts: low-effort output consuming more total time via clarification cycles. Direct evidence-for. `strength=4, confidence=high`. | UNSURE — not written |
| 3 | `MCP Token Noise` | `supports` | `Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries` | Tool-surface noise degrading reasoning is a second, independent instance of the MVC mechanism (the first being raw context volume). Two independent supports would move MVC from unsupported to grounded. `strength=3, confidence=medium`. | UNSURE — not written |
| 4 | `SoT - Flow Engineering` | `depends_on` | `SoT - LLM Semantic-Statistical Mismatch` | Flow Engineering's entire justification is that the model is not a cognitive agent, so talking to it cannot enforce anything. Remove the Mismatch premise and Flow Engineering has no argument. This is the cluster's spine edge. `strength=5, confidence=high`. **Pair with `axiom: true` on the Mismatch note** (§9.3 permits both), or the audit will immediately list it as a C1 gap. | UNSURE — not written |

### Structural edges (linter-valid, audit-invisible)

| # | Source | Edge | Target | Rationale | Validated? |
|---|---|---|---|---|---|
| 5 | `SoT - The RPI Workflow (Context Engineering)` | `implements` | `SoT - Context Engineering` | The RPI note says so in its own MVU: "the operational framework for applying this discipline." Textbook concrete-realisation-of-abstract. `confidence=high`. | UNSURE — not written |
| 6 | `MVC Enforcement Structural Gates for LLM Agents` | `implements` | `SoT - Flow Engineering` | MVC gates are the context-assembly instance of the deterministic-wrapper principle. `confidence=high`. | UNSURE — not written |
| 7 | `SoT - Typed Answer Contract (TAC) for LLM Output` | `implements` | `SoT - Flow Engineering` | TAC is the output-side instance of the same principle. The TAC note already names MVC as its sibling ("the same idea applied to context assembly rather than output formatting") — so both are `implements` of a shared parent, not `extends` of each other. `confidence=medium`. | UNSURE — not written |
| 8 | `Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts` | `synthesizes` ×2 | `Objective Task Validation`; `Subjective Task Validation` | Two markers, one per target (one edge per marker, per Edge Vocabulary §1). The claim is exactly the union of the two heuristics. `confidence=high`. | UNSURE — not written |
| 9 | `LLM Wiki Concept` | `implements` | `SoT - LLM Wiki Pattern` | Atomic definition as a concrete instance of the full pattern. Weakest of the nine — arguably the atom is the *abstraction* and the SoT the elaboration, in which case leave untyped. `confidence=low`. | UNSURE — not written |

### Relationships I deliberately did NOT type

- `SoT - Context Rot` → `SoT - Parochial Code`: the Context Rot note says rot "is the primary cause of" parochial code. **Causation is not in the vocabulary.** `depends_on` would invert it (parochial code doesn't *require* rot to make sense; other causes exist), and `supports` is an evidential relation, not a causal one. **Leave untyped**, or write it as a prose line. Forcing this one would be the easiest way to corrupt the graph's meaning.
- `Protocol - Typed Answer Contract (TAC) for Vault Agents` → `SoT - Typed Answer Contract (TAC) for LLM Output`: a clean `implements`, but **unwritable under current scope**. The source note lives in `10_System/prompts/`, and §9.3 only licenses typed-edge edits inside existing `30_Library/` notes. The edge must be emitted by the source, so it cannot be written from the SoT side. Flagging as a governance gap rather than working around it.
- The three "shift" notes (`Shift to Architectural Oversight` / `High-Level Oversight` / `Verification`) → anything: resolve Duplicate Cluster G first. Wiring duplicates makes them harder to merge later.
- `Agentic Autonomy Accelerates Fastest…` ↔ `Reinforcement Learning Produces Jagged Intelligence…`: these want `same_as`-ish treatment. **No edge** — that's a merge recommendation for the human, not a relationship.

---

## Unresolved Links Found

Wikilinks in the AI/LLM cluster pointing at notes that do not exist. Each target below was checked against filename, frontmatter `title`, and `aliases`/`alias` across 4,231 indexed names (`.trash` and `99_Archive` excluded). None is a false alarm from a rename.

**Highest value — trivially fixable, currently breaking three canonical SoTs:**

| Missing target | Referenced from | Note |
|---|---|---|
| `Context Engineering` | `SoT - Context Rot` | **`SoT - Context Engineering` exists.** It fails to resolve only because its `aliases` are `[Context Compression, High-Signal Prompting, Information Density, Prompt Optimization]` — the obvious alias is missing. **One-line fix: add `Context Engineering` to that alias list.** |
| `The Architectural Guardian` | `SoT - Agentic Roles`, `SoT - Context Engineering`, `SoT - The Context Engine` | Confirmed absent. Referenced by three SoTs as the meta-context / "Superego" prompt that enforces architectural priors. **The single most load-bearing missing note in the cluster.** |
| `SoT - Cognitive Bridge` | (concept named in `MOC - AI Software Engineering` §1, not linked) | Confirmed absent as a note. The MoC defines the Cognitive Bridge in prose as the cluster's core theme. Candidate for promotion. |

**Also unresolved in the cluster:**

`HEAD - Agentic Engineering and AI Workflow Management` (≥4 sources) · `HEAD The Agent-First Workflow` (≥3) · `HEAD The Failure of Human-Centric Design` (≥4) · `Using Karpathy's Original Framework` (≥4) · `AI Agentic Workflows` · `Architectural Decision Records ADRs for AI Agents` · `Context Quarantine` · `Dynamic Tool Loadout` · `SoT - Semantic Code Graph` · `TDD's Evolution in the LLM Era` · `Targeting LLM Attention via Structural Constraints` (near-miss for the existing `Targeting LLM Attention Requires Encoding Relevance as Structure` — likely a rename that left stale links) · `Typed-Answer-Contract-RAG` (exists **only in `.trash`**) · `Confirmation Bias` · `Separation of Concerns` · `10_System/prompts/Knowledge Consolidation Agent.md` (path-style link; the file exists, the link form is wrong) · `wikilink` (a literal `[[wikilink]]` inside prose in the TAC SoT — documentation artefact, harmless).

The four `HEAD …` targets are consumed-and-deleted working notes (per `SoT - Evolutionary Note System`: "squashing ephemeral thinking (HEAD notes) into durable answers"). Their disappearance is by design; the dangling links are the residue. **Recommend a decision rule** — either the merge protocol rewrites inbound links to the surviving SoT, or HEAD notes are archived rather than deleted. Currently neither happens.

Context: `LLMeon Vault Pattern Report` measured ~1,330 unresolved wikilinks vault-wide (~20% of 6,549). The ~29 above are the AI-cluster share.

---

## First Edits

Ordered. Each is one sitting.

1. **Add `Context Engineering` to the `aliases` of `SoT - Context Engineering`.** One line. Repairs a dangling link from a canonical SoT and makes the note findable by its own name. *Do this one first because it costs nothing and proves the loop.*
2. **Merge Duplicate Cluster B** (`SoT - Complexity Conservation` / `SoT - Conservation of Complexity`). Human action. It blocks edge #4's neighbourhood and is the only *SoT-level* duplicate found — the most damaging kind, because SoTs are what other notes point at.
3. **Set `axiom: true` on `SoT - LLM Semantic-Statistical Mismatch`, then write edge #4** (`SoT - Flow Engineering` `depends_on` it). This is the smallest change that puts the LLM cluster into the justification graph *at all*. Both edits are inside §9.3 scope. Run `edge_lint.py --path` after; it must report 0 errors.
4. **Write edges #1 and #2** (both `supports`, both stated in the source notes' own prose). Two edges, two grounded claims, zero interpretation required.
5. **Retitle `Coherent LLM output signals meaningful processing`** to match its body (it is about *perceived* validation, i.e. the Eliza Effect). Also set its empty `type:`. Human action — this is a proposition edit. Leaving the title as-is guarantees a future agent proposes a spurious `contradicts` edge against it.
6. **Claim stub: model routing / capability trade-offs** → `raw/proposed-claims/2026-07-27-model-routing-capability-tradeoffs.md` (§2.4). The evidence is already in the vault across `wiki/projects/Hermes-*`; the claim node is missing.
7. **Claim stub: the tension between the vault as human sense-making instrument and as LLM context substrate.** This is the unstated premise under `Proposition-Centred Notes…`, `Local-First Obsidian with MCP and RAG…`, `PKM as Sense-Making Engine` and `PKM Generates Unique Insights…` — four notes resting on an assumption none of them names. Highest-value stub in the report.
8. **Then, and only then, the structural edges (#5–#9).** They make the graph readable but change nothing the compiler can check. Doing them first would feel productive and move nothing.

---

## Validation

- **`edge_lint.py --audit`: run, clean.** `python3 10_System/scripts/edge_lint.py --audit` → *"No edge violations found. scanned 2310 notes · 288 edges in 71 notes · 0 error(s), 0 warning(s)."* Argument audit: 177 justification + 5 contradiction edges among 158 nodes; 23 gaps, 11 axioms, 23 bedrock, 1 live tension, 2 cycles. PyYAML present, so title resolution is trustworthy.
- **`edge_lint.py --path` for proposed edges: NOT RUN.** No edges were written, so there is nothing to validate. **Every one of the nine proposed edges is `UNSURE`** and must be linted at 0 errors before being considered done (AGENTS.md §6).
- **Tooling tier: 3 (filesystem).** Lexical search only. Coverage claims downgraded per §Search Coverage.
- **Existence verification:** every note title named in this report was resolved this session against filename, frontmatter `title`, and `aliases`/`alias` across a 4,231-name index built from the live vault (`.trash`, `.git`, `99_Archive` excluded). Three titles are asserted **absent** and were confirmed absent by that same index: `The Architectural Guardian`, `SoT - Cognitive Bridge`, and `Context Engineering` (as a resolvable name — the *note* `SoT - Context Engineering` exists). **Not checked:** `prodos.id`. The field is sparse in this vault and my index keyed on filename/title/alias only. If any of those three exists under a `prodos.id` I did not read, that is where the error would be.
- **Governance:** `AGENTS.md` was **not read in full this session** — a Read call on it was interrupted, and I did not retry. I worked from `CLAUDE.md`'s pointers plus §0/§1/§6 read via shell, and from `SoT - Typed Edge Vocabulary` read in full. Since this pass wrote only to `output/`, the risk is contained, but **any follow-up that writes edges should read §9 in full first.**

**Overall confidence: medium-high.** High on the headline (the compiler is authoritative: zero LLM-domain nodes in the justification graph). High on the duplicate clusters and unresolved links (both mechanically verified). Medium on canonical-note candidates and conflicts, which rest on my reading of ~60 notes out of 223 and on lexical rather than semantic retrieval.

**What would change my view:** running this again through `obsidian-mcp-tools` semantic search. If embedding-based retrieval surfaces a cluster of LLM notes my keyword set missed — particularly around memory/working-set management, where I claim a real gap — the "thin theme" judgements in §Search Coverage would need revising. The headline finding would not change; it comes from the compiler, not from search.
