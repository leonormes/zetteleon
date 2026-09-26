---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-cards-atrocity-paradigm
title: 2026-09-24-cards-atrocity-paradigm
type: note
---

## Positioning — [[Card's Atrocity Paradigm Identifies Evil via Three Necessary Co-conditions]] — 2026-09-24

> Prompt: [[Orphan Note Positioning & Thread Audit]] v3, third run, single pass with no checkpoint.

### Baseline

**Thin (already partly wired), not orphaned.**

- **Outbound:** 2 plain links, [[The Traditional Definition of Knowledge is Justified True Belief]] (an analogy) and [[Evil Harm Is Intolerable Harm That Destroys the Conditions for a Decent Life]]. No typed edges.
- **Inbound (2):** [[SoT - Bonhoeffer's Theory of Functional Stupidity]] (See Also) and an auto-generated link report in `400_indexes/`.
- **Frontmatter:** `type: claim`, `conformant: false`, with 4 missing schema fields.
- **Hub:** none. No MoC or SoT houses the evil-atoms cluster.

### Search Execution

| Query | Style | Result |
|---|---|---|
| "Card atrocity paradigm evil: foreseeable intolerable harm, culpable wrongdoing, inexcusable" | conceptual variant | Six sibling atoms: [[Evil Harm Is Intolerable Harm That Destroys the Conditions for a Decent Life]], [[Evil Requires Both Culpability and Foreseeability — Without These It Is Tragedy]], [[Evil Attacks the Shared Moral Community Itself Not Merely a Norm Within It]], [[Evil Structurally Requires a Radical Power Asymmetry Directed at the Defenceless]], [[Objectification Treats Persons as Instruments and Is a Core Property of Evil]], [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] |
| "Card evil atrocity paradigm" (BM25) | literal anchor | The same cluster plus the link report; the Kuhn "paradigm" notes and the Rust SoT are noise |
| Hub search across `MoC/` and `SoT/` | functional equivalent | [[MOC - Character and Virtue]] §7 (one entry for the cluster), [[SoT - Bonhoeffer's Theory of Functional Stupidity]] |

### Candidate Connections

| Candidate | Use / Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[Evil Requires Both Culpability and Foreseeability — Without These It Is Tragedy]] | **Use.** It unpacks conditions 1 and 2 of the Target. | Target remains coherent | No | The Target is the composite of it and the Harm atom | **PASS as structural.** `synthesizes` |
| [[Evil Harm Is Intolerable Harm That Destroys the Conditions for a Decent Life]] | **Use.** It unpacks condition 3. | Coherent | No | Same | **PASS as structural.** `synthesizes` |
| [[Evil Structurally Requires a Radical Power Asymmetry Directed at the Defenceless]] | Mention. A diagnostic marker, and its own note says it is not a sufficient condition. | Coherent | Yes | No move | **Plain link** |
| [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] | Use (weak). It says foreseeability, not motive, is the deciding variable. | Coherent | Partly | No move | **Plain link** |
| [[Evil Attacks the Shared Moral Community Itself Not Merely a Norm Within It]], [[Objectification Treats Persons as Instruments and Is a Core Property of Evil]] | Mention. Descriptive properties outside the three conditions. | Coherent | Yes | No move | **Plain link** |
| [[SoT - Bonhoeffer's Theory of Functional Stupidity]] | Already links in. Application, not premise. | n/a | n/a | n/a | **Plain link (reciprocal)** |
| [[The Traditional Definition of Knowledge is Justified True Belief]] | Analogy only. Existing link kept. That note is marked `axiom: true`. | n/a | n/a | n/a | **Kept, untyped** |

No `supports`, `depends_on` or `contradicts` candidate passes. In particular, no note contradicts the Target: the power-asymmetry note's claim is compatible if you treat it as a diagnostic rather than a fourth necessary condition.

### Patch A — Typed Edges

Both on the Target file, and both structural only, so the compiler ignores them for C1–C3:

- `[synthesizes:: [[Evil Requires Both Culpability and Foreseeability — Without These It Is Tragedy]], confidence=medium]`
- `[synthesizes:: [[Evil Harm Is Intolerable Harm That Destroys the Conditions for a Decent Life]], confidence=medium]`

### Patch B — Plain Links and Anchors

- Six annotated bullets appended to the Target's existing `### Related`.
- One anchor line in [[MOC - Character and Virtue]] §7, after the [[Evil Attacks the Shared Moral Community Itself Not Merely a Norm Within It]] entry.

### Patch C — Frontmatter

Added `proposition`, `epistemic_status: medium`, empty `evidence_links` and `contradicts`; `conformant: true`; updated `modified`. The `proposition` text avoids apostrophes and `: `. Title unchanged.

### Patch D — Further Reading

**No personal-library matches.** Three CLI queries were run, one with the philosophy tag filter. The results (Nietzsche, Gilbert, Pinker, Locke, the Buddhist dharma book) scored 0.28–0.38, and the visible text did not bear on Card's three conditions. Reported as such rather than forcing a citation.

### Claim Stubs Written

None.

### Applied (Part 2)

| File | Change | Status |
|---|---|---|
| `Card's Atrocity Paradigm Identifies Evil via Three Necessary Co-conditions.md` | Patches A, B and C | Applied |
| `30_Library/MoC/MOC - Character and Virtue.md` | One anchor line in §7 | Applied |
| Patch D | No qualifying hits | Skipped |

**Validation:** whole-vault `edge_lint.py` reports `0 error(s), 0 warning(s)` (2835 notes, 1375 edges).

### No evidence / needs your call

- **The evil cluster has no home hub.** Seven atoms sit under one-off mentions in [[MOC - Character and Virtue]] and a link report. A dedicated MoC would be the proper home. I did not create one.
- **Source verification:** the note's evidence is a secondary paraphrase of Card. I could not check it against the book, which is not in the library index.

---

## Part 3 — Thread Audit Report

### Verdict

**The Target is not a node in the argument graph.** `--why` and `--impact` both return "no node found", and the compiler audit does not list it. Its two new edges are `synthesizes`, which is structural only. Exposure is 0, with no dependents and no threads. As in the first run, this is the correct outcome for a definitional claim, and I did not invent a thread.

### Traversal manifest

| Direction | Node | Edge | Termination |
|---|---|---|---|
| Out | The Culpability and Foreseeability atom, the Intolerable Harm atom | `synthesizes` | Structural (not counted) |
| Out | Power Asymmetry, Malice or Banality, Moral Community, Objectification, Bonhoeffer SoT, JTB | plain | Depth cap / hub |
| In | [[SoT - Bonhoeffer's Theory of Functional Stupidity]], [[MOC - Character and Virtue]] (new), the link report | plain | Hub |

### Use vs mention

The remaining plain links are mention or weak use. Each failed at least two of the three tests in Part 1, so they stay untyped.

### Pathologies found

1. **Hubless cluster:** seven evil-related claims with no dedicated map.
2. **Definitional overlap:** the Culpability atom and the Harm atom partly restate the Target. This is decomposition, and I do not recommend a merge, unlike the previous run's Focus/Continuous pair.
3. **Ungrounded cluster:** none of the evil atoms links to a source-level Evidence note, so the whole cluster is grounded only in a secondary quote.

### Frontier

The Culpability atom and the Harm atom are the next notes to check, since the `synthesizes` edges now point at them.

### Next action

Decide whether the evil atoms warrant their own hub: if yes, create `30_Library/MoC/MOC - Evil and Atrocity.md` listing the seven atoms; otherwise leave them under [[MOC - Character and Virtue]].

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings.
- Confidence: **medium**.

---

## Follow-up — hub created

Leon approved the hub. [[MOC - Evil and Atrocity]] was created with five sections (three conditions, diagnostic features, how ordinary people take part, responding, structural analogy) and a Known Gaps list. [[MOC - Character and Virtue]] §7 gained one line pointing to it. Discovered during the build:

- `Moral Silencing Suppresses Conscience and Enables Evil` is listed in the link report but does not exist as a note.
- `[[Humans Are Social Creatures]]` does not resolve (used by two evil notes).

Neither was linked from the MoC, so no dangling link was added.
