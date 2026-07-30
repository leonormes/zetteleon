---
created: 2026-07-30T12:05:03+00:00
modified: 2026-07-30T12:05:03+00:00
permalink: llmeon/90-audits/2026-07-30-moc-authority-dynamics-and-adhd
title: 2026-07-30-moc-authority-dynamics-and-adhd
type: note
---

## Positioning — [[MOC - Authority Dynamics and ADHD]] — 2026-07-30

**Scope note before the results:** this target is a MoC, not an atomic claim. Two parts of the standing process don't transfer cleanly, and I'm flagging that rather than forcing them:

- **No Patch A is possible in principle here**, not just this run. Typed edges model justification between claims; MoC→note and MoC→MoC links are navigational by convention and stay untyped even when they're real, well-evidenced connections (per [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] §2 and the Bootstrap Agent's own rule 6). Nothing below is a "missed" typed edge.
- **Part 3 (thread audit) doesn't apply and I'm not running it.** Per [[SoT - Knowledge Compiler (Argument Graph Spec)]] §1: "Reference notes, procedures, journal entries, MoCs—most of the vault—never join the argument graph." Computing an exposure/dependents score for a hub would be inventing a number the compiler itself explicitly declines to produce. If you want this MoC's *content* pressure-tested, that's a different, claim-by-claim job on the atomic notes it links to — not this one.

**Tooling tier: raw filesystem grep/read only**, same downgrade as the last two runs.

### Baseline

Inverted pattern from the last two runs: this is a **leaf hub**, not a sink or a near-orphan. Richly connected *downward* (seven real, prose-embedded outbound links, not a bare list), and completely disconnected *upward* — no MoC or index in the vault points at it.

- Outbound (all genuine prose use, not mention): [[Rejection As Moral Response]], [[Bidirectional Authority Discomfort in ADHD]], [[Rejection Sensitive Dysphoria (RSD)]], [[SoT - ADHD Neurology & Core Concepts#2.1 The Shame-Procrastination Cycle]], [[Defensive Hypervigilance]], [[Shame as Social Regulatory Mechanism]], [[Productive vs Destructive Shame]].
- Inbound: **none.** Confirmed by full-vault search on the exact title — the only hits are the note itself, the four notes it cites (one-way), and yesterday's audit report on [[Bidirectional Authority Discomfort in ADHD]].
- No `Up:` line — several sibling MoCs in this vault (e.g. [[MOC - Social Perception and Self-Awareness]]) open with an `- Up: [[Parent]]` line; this one doesn't have the convention at all.
- Frontmatter: `type: map` is schema-valid, but `status: 'null'` and `last_reviewed: 'null'` are string-literal "null"s rather than real values or absent fields, and there's no `conformant` field either way.

### Search Execution

- Literal anchor "MOC - Authority Dynamics and ADHD" across the vault → 7 hits, all accounted for above; zero from any MoC/index file.
- Read [[MOC - ADHD (The Master Map)]] (the vault's declared "Master Entry Point" for the whole ADHD domain, per [[Meta MOC - The Core Domains]] Domain 2) in full: its "2. The Software: Emotional Regulation & Mindset" section already covers RSD and the Shame-Procrastination Cycle by name — the exact same two mechanisms this MoC discusses — but never links to this MoC itself.
- Read [[Meta MOC - The Core Domains]]: correctly treats the Master Map as the single Domain-2 entry point and doesn't (and shouldn't) enumerate sub-hubs directly — so the fix belongs one level down, at the Master Map, not here.

### Candidate Connections

| Candidate | Evidence | Verdict |
|---|---|---|
| [[MOC - ADHD (The Master Map)]] → this MoC | Master Map's "2. The Software" section already names RSD and the Shame-Procrastination Cycle as its own bullets — this MoC is the fuller treatment of exactly that material, just never linked | **Real gap, not a candidate to test** — MoC-to-MoC placement isn't a Denial/Substitution/Load question, it's a straightforward "does the index cover its own territory" check. It doesn't. |
| An `Up:` line on this MoC itself, pointing at the Master Map | Matches the convention already used elsewhere in the vault (e.g. Social Perception MOC) | Straightforward hygiene addition, not a tested inference |

### Patch A — Typed Edges

None, and none possible for this note type — see scope note above.

### Patch B — Plain Links / MoC Anchors (you'd apply these)

| File | Proposed line | Where it goes |
|---|---|---|
| [[MOC - ADHD (The Master Map)]] | `- The Authority Lens: [[MOC - Authority Dynamics and ADHD]]—_How bidirectional authority discomfort and RSD interact with the shame-procrastination cycle._` | New bullet in "2. The Software: Emotional Regulation & Mindset", alongside the existing Reset/Mindset/Self/Loop bullets |
| [[MOC - Authority Dynamics and ADHD]] | `- Up: [[MOC - ADHD (The Master Map)]]` | New first line, matching the `Up:` convention used by [[MOC - Social Perception and Self-Awareness]] |

### Patch C — Frontmatter Conformance (you'd apply this)

| Field | Current | Proposed |
|---|---|---|
| `status` | `'null'` | Remove, or set a real value (`growing` / `stable` / `evergreen`) — your call which |
| `last_reviewed` | `'null'` | Remove, or set today's date if you're treating this pass as the review |
| `conformant` | (absent) | `true` — `title`/`type`/`tags` are all already valid; nothing here needs a non-conformance flag once the two string-literal nulls above are cleaned up |

### Claim Stubs Written

None — nothing here is a missing atomic concept, it's a missing index entry.

### No evidence / needs your call

None this run — every finding above had direct, checkable evidence (a full-vault title search and a full read of the two candidate index files), not an inference from partial context.

### Validation

- `edge_lint.py`: not applicable — no typed edge proposed or written.
- Confidence: high on all findings — this was a factual connectivity check (does X link to Y), not an inferential judgement call.

---

## Next action

Tell me whether to apply Patch B's two link additions and/or Patch C's frontmatter cleanup — both are single-file, low-risk edits with nothing to lint.
