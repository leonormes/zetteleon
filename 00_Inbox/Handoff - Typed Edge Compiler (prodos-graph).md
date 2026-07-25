---
title: Handoff — Typed Edge Compiler Build & Validation
purpose: Context transfer to vault-resident LLM PKM assistant (CLI + vault access)
status: ready for implementation
permalink: llmeon/00-inbox/handoff-typed-edge-compiler-prodos-graph
---

# Handoff: Build & Validate the Typed Edge Compiler

You have Obsidian CLI access and can read/write files in this vault. This brief gives you everything decided in a prior design conversation, everything discovered when we tested that design against the real vault, and the concrete next steps. Read this whole document before writing any code — the second half changes the first half's plan.

---

## 1. The idea, in one paragraph

Typed edges are one-line, reading-view-invisible annotations recording a directed, named relationship between two notes or blocks: `%%[relationshipName:: [[target]]]%%`. They upgrade a flat `[[wikilink]]` ("these are related") into a queryable claim ("A **contradicts** B", "A **depends_on** B"). Two independent tools read the same on-disk encoding: **Dataview** for interactive single-hop queries inside Obsidian (works today, zero code), and a **compiler** for everything Dataview structurally cannot do — vocabulary validation, multi-hop traversal, cycle detection, and path audits ("why does A connect to D?").

---

## 2. Decided: the syntax

```
%%[relationshipName:: [[target]]]%%
%%[relationshipName:: [[target]], strength=5, confidence=high]%%
```

- Wrapped in Obsidian's `%% … %%` comment markers → invisible in reading view and Live Preview, but present in the raw markdown.
- The interior is a **Dataview inline field**: `[fieldName:: value]`. This was chosen over a bespoke syntax (`type.rel{target}`) specifically because Dataview already parses it with zero tooling, and it's a documented, stable grammar for a compiler to also parse, rather than one we'd have to invent and maintain a parser for from scratch.
- Target is always a wikilink (`[[Note]]` or `[[Note#^block-id]]`), never an opaque id — this keeps edges rename-safe, since Obsidian's own refactoring rewrites wikilinks automatically.
- Attributes (`strength` 1–5, `confidence` high/medium/low) are optional, comma-separated inline fields. Deliberately only these two — richer metadata (evidence type, temporal scope) belongs in prose, not the edge.

This syntax was **empirically tested and confirmed working**: a `%%[relationshipName:: [[target]]]%%` line is invisible in reading mode and *does* get picked up by a Dataview query on another note (e.g. `LIST WHERE contradicts`).

### Canonical relationship vocabulary (six types)

| Relationship | Meaning (source → target) |
|:---|:---|
| `extends` | Source builds on / specialises the target. |
| `synthesizes` | Source combines several targets into a higher-order idea. |
| `implements` | Source is a concrete realisation of an abstract target. |
| `contradicts` | Source conflicts with / negates the target (symmetric). |
| `supports` | Source provides evidence or argument *for* the target. |
| `depends_on` | Source requires the target to make sense or function. |

Of these six, three (`supports`, `depends_on`, `contradicts`) are *justification/conflict* edges and form an argument subgraph; the other three (`extends`, `synthesizes`, `implements`) are structural and are excluded from argument-graph computations (see §4).

---

## 3. Decided: why a compiler is still needed (don't skip this)

An earlier pass in this design conversation argued Dataview queries alone were sufficient and a compiler was unnecessary ceremony. **That was wrong and was corrected.** Dataview's DQL is a declarative filter over a flat index — no recursion, no schema, no validation. It cannot do:

| Requirement | Dataview | Why not |
|:---|:---|:---|
| Single-hop query ("what contradicts X?") | ✅ | This is exactly what DQL is for. |
| Vocabulary validation | ❌ | Any `fieldName` is stored silently. A typo (`contradicsts`) succeeds at write time and then simply never matches at query time — invisible at both ends. |
| Attribute type checking | ❌ | `strength=9`, `confidence=very-high` are stored happily. |
| Multi-hop / transitive closure | ❌ | No recursion. |
| Path audit ("why does A connect to D?") | ❌ | Requires graph search (BFS), not a filter. |
| Cycle detection | ❌ | A `depends_on` cycle is a real defect; DQL never surfaces it. |

**The vocabulary-typo case alone justifies building this**: it's the one failure mode invisible at both authoring time and query time.

---

## 4. Discovered: a compiler spec already exists — build against it, not from scratch

Before any code is written, a vault search (`obsidian search:context query="contradicts" format=json`) turned up a **pre-existing, more mature spec** that this whole conversation had been unknowingly re-deriving:

📄 `30_Library/SoT/SoT - Knowledge Compiler (Argument Graph Spec).md`

This is the **authoritative target**. It is better-scoped than anything proposed earlier in this conversation:

- **Opt-in graph.** Only notes/blocks with justification edges (`supports`, `depends_on`, `contradicts`) ever join the argument graph. Most of the vault — reference notes, procedures, journal entries, MoCs — is silently excluded. This is a real refinement over "validate every edge in the vault."
- **Four computed capabilities (C1–C4):**
  - **C1 — Gap Detection**: a claim with outgoing justification edges (it supports something) but no incoming edge and no `axiom: true` marker — i.e. load-bearing work resting on nothing.
  - **C2 — Foundation Audit**: declared axioms (`axiom: true`) vs. undeclared foundations (the C1 gap set) — "what am I resting on, chosen vs. smuggled in?"
  - **C3 — Conflict Detection**: `contradicts` edges, plus cycles in the `supports`/`depends_on` graph.
  - **C4 — Provenance**: `why(X)` (transitive closure of justification edges *into* X, down to axioms) and `impact(X)` (transitive closure *out of* X) — this is the `--why` path-audit capability, already named and scoped.
- **Phased roadmap**, explicitly "do one phase, ship it, then reassess":

  | Phase | Capability | Build | Status |
  |:---|:---|:---|:---|
  | v0 | Typed edges + resolution | `edge_lint.py` — no danglers, controlled vocab, targets resolve | **marked `done` — needs verification, see §6** |
  | v1 | Gap + foundation audit (C1, C2) | `axiom` marker + `edge_lint.py --audit` | next |
  | v2 | Conflict detection (C3) | report `contradicts`, detect cycles | planned |
  | v3 | Provenance (C4) | `edge_lint.py why <id>` / `impact <id>` | planned |
  | v4+ | Derived contradictions, confidence maths, visualisation, Bases views | — | deferred |

- **Non-goals stated explicitly**: report-only (never auto-edits notes, mirrors the vault's `UNSURE`/dry-run discipline), no logic engine (checks graph *shape*, not truth), no confidence maths yet.
- **Own tensions already documented**, most importantly: *as of writing, the justification graph is effectively empty — the first real task is seeding one small real argument, not building v1 against nothing.*

**Implication for scope: any new work should extend or complete this spec's `edge_lint.py`, not create a rival tool.** A separately-proposed `prodos-graph` design from earlier in this conversation is now superseded — retire it. The one thing it had that this spec doesn't cover yet is fine-grained syntax validation (unknown relationship names, dangling targets, malformed attributes) — that's a real, still-open gap, but it's a small piece slotting into **v0**, not a new architecture.

---

## 5. Discovered: the vault already has multiple, inconsistent edge encodings live

A plain-text search for `contradicts` across the vault (not scoped to the new syntax) surfaced **at least four different encodings already in use**, which any validator needs to account for or explicitly ignore:

1. **The target syntax** (what this spec defines): `%%[contradicts:: [[Target]]]%%` — confirmed present in the two SoT spec files themselves.
2. **Visible inline Dataview fields, no comment wrapper**: `rel:: contradicts` appearing directly in reading-view text in MoC notes (e.g. `MOC - From Information to Knowledge.md`, `MOC - Divergent Thinking vs Specialization.md`). These are *not* hidden and use a different field name (`rel::` with the relationship as the *value*, rather than the relationship as the *field name*).
3. **Prose annotations under a `## Tensions` heading**: `[[Note Name]]—contradicts: <brief explanation>`, per the convention in `10_System/prompts/Atomic Linker → Promote & Connect.md`. Widely used throughout `30_Library/100_zettelkasten/`.
4. **A frontmatter field**: `contradicts:` already defined as a property in `10_System/fileClasses/claim.md`, expecting a list of wikilinks to Claim notes.
5. There is also a live enforcement prompt — `10_System/prompts/Note Refresh & Link Auditor.md` — that already hardcodes the six-word closed vocabulary and instructs an LLM to reject any other relationship word at write time. This is a *soft*, prompt-level validator that predates any code-level one.

**None of this needs to be "fixed" immediately** — but it means before writing `edge_lint.py`'s ingest step, you should decide (and document in the compiler spec) whether it parses only encoding #1, or whether it needs to normalise across some subset of #1–#4. Silently ignoring #2–#4 while claiming to "validate the vault's typed edges" would give false confidence.

---

## 6. Two anomalies flagged, unresolved — check these first

1. **Possible stray paste.** `30_Library/SoT/SoT - Knowledge Compiler (Argument Graph Spec).md`, line 13, directly under the frontmatter close:
   ```
   contradicts:: [[Earlier Assumption]], strength=4, confidence=high]
   ```
   This is unwrapped (no `%%…%%`, so it's visible in reading view), missing its opening `[`, and matches an example given earlier in this design conversation for testing purposes. It looks like an accidental paste rather than a deliberate edge. **Confirm with the user whether to delete it before it's mistaken for real data by any tooling.**

2. **Roadmap status inconsistency.** The same file's roadmap table marks `v0 | edge_lint.py … | done`. No `edge_lint.py` has been located anywhere in this conversation's vault searches yet. Before building anything:
   ```
   obsidian file path="10_System/scripts/edge_lint.py"
   ```
   - If this resolves → **read the existing file in full** before writing anything; v0 may already be built, and the actual task is extending it toward v1 (C1/C2), not creating it.
   - If it 404s → the roadmap's `done` status is stale and should be corrected to `planned`, and the real starting task is writing v0 itself.

---

## 7. Discovered: Obsidian CLI capabilities usable inside the compiler

The user has the official Obsidian CLI installed (ships with Obsidian 1.12+, `obsidian` command, requires Obsidian desktop app running — no headless/CI story exists for it; `obsidian-headless` is a *different*, sync-only tool and cannot query a vault). Relevant commands, confirmed via docs and live testing:

| Task | Command | Notes |
|:---|:---|:---|
| Extract edge lines with source location | `obsidian search:context query="<text>" format=json` | Returns `path:line:text` — gives you `file:line` provenance for free. **Caveat, confirmed by testing:** Obsidian's search parser treats `word:` as an operator prefix, so a bare query like `contradicts::` errors with `Operator "contradicts" not recognized`. Wrap the query in escaped literal quotes: `query="\"contradicts::\""` — confirmed working and returns real matches including from inside `%%…%%` comments. |
| Full resolved link graph | `obsidian eval code="app.metadataCache.resolvedLinks"` | Gives you Obsidian's own pre-computed link resolution — likely the biggest time-saver, since link resolution (matching `[[Target]]` to an actual file, respecting aliases) is normally the fiddliest part of an ingest step. |
| Dangling/unresolved targets | `obsidian unresolved verbose format=json` | Free "dangling target" check — no custom resolver needed. |
| Frontmatter properties | `obsidian properties`, `obsidian property:read name=<name> file=<name>` | Useful for the "edge duplicates a frontmatter relation" check. |
| Orphans / dead-ends | `obsidian orphans`, `obsidian deadends` | Matches the compiler roadmap's later graph-health ideas, free. |
| One-hop backlinks/outgoing links | `obsidian backlinks file=<name>`, `obsidian links file=<name>` | Single-hop only; multi-hop traversal (C4's `why`/`impact`) still has to be built. |
| Arbitrary Dataview query from the CLI | `obsidian eval code="await app.plugins.plugins.dataview.api.tryQuery('LIST WHERE contradicts')"` | Confirmed as the correct call shape per Dataview's own plugin API docs (`app.plugins.plugins.dataview.api`, method `tryQuery` for exception-based error handling). No dedicated `obsidian dataview` subcommand exists — this `eval` route is the only path in. |
| Native query for the *other* database feature | `obsidian base:query file=<name> view=<name> format=json|csv|tsv|md|paths` | Bases (Obsidian's own DB feature) gets a first-class CLI verb; Dataview doesn't. Not needed now, but worth knowing if the vault ever migrates.|

### The real constraint this creates

**`edge_lint.py` cannot be "headless" in the sense the original design conversation assumed** ("runs in CI, from Neovim, from a cron job, with no Obsidian process alive") if it leans on the CLI, because the CLI requires the Obsidian desktop app to be running. There is no way around this with the current tooling — `obsidian-headless` only does sync/publish, not querying.

**Recommendation carried into this handoff:** build the ingest step behind a single seam — e.g. a `load_edges() -> list[Edge]` function — implemented via the CLI now (fast, ~zero link-resolution code, gets v0/v1 shipped quickly), but isolated enough that a pure-markdown-parsing backend could replace it later if a CI/headless use case ever actually arises. Don't build the standalone parser first; that's the version of this project that stalls on plumbing before producing any output.

---

## 8. What to actually do, in order

1. **Resolve the two anomalies in §6** — confirm/delete the stray paste, confirm/correct the `v0: done` status. Report back what you find before proceeding; don't assume.
2. **Read `10_System/scripts/edge_lint.py` if it exists.** If real, this changes everything below from "build" to "extend" — re-plan from its actual current state.
3. **Decide and document the ingest scope** (§5) — which of the 4+ live encodings `edge_lint.py` parses. Recommendation: parse encoding #1 (`%%[rel:: [[target]]]%%`) as primary/canonical, and at minimum *count and report* (don't silently ignore) instances of #2–#4 so scope decisions are visible, not assumed.
4. **Build v0 first, narrowly**: ingest via `search:context` + `eval`-backed link resolution (§7), validate against the closed six-word vocabulary (§2), flag dangling targets (cross-check against `obsidian unresolved`), flag malformed attributes. Every diagnostic needs `file:line`. Report-only — never auto-edit, per the spec's own stated discipline (§4).
5. **Validate v0 against the real vault** — run it, and expect near-zero real argument edges today (the spec's own Tensions section already predicts this: *"the justification graph is effectively empty"*). The useful output of this first run is a clean list of `file:line` locations using encodings #2–#4, so the user can decide whether/how to migrate them, not a report of C1/C2 gaps (there's nothing to compute yet).
6. **Only then** move to v1 (C1/C2 — gap detection, foundation audit) per the existing roadmap, and only after real `supports`/`depends_on` edges exist to test against, exactly as the spec's own Tensions section recommends.

Do not skip ahead to C3/C4 (conflict detection, provenance/`why`) — the existing roadmap is explicit that each phase should be used on real claims before the next is built, and this handoff should preserve that discipline rather than re-introduce the "build everything at once" instinct the earlier version of this design had.