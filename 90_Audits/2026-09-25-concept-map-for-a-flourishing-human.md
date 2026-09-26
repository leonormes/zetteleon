---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-concept-map-for-a-flourishing-human
title: 2026-09-25-concept-map-for-a-flourishing-human
type: note
---

## Consolidation — [[A Concept Map for a Flourishing Human]] — 2026-09-25

> Run of [[Knowledge Consolidation Agent]] (v4). You judged this note redundant with the existing MoCs. That is true for three of its four branches; the fourth, plus some framing and source labels, was not held anywhere else, so it was moved first and then the note was deprecated.

### Analysis

Core concept: a child-facing pick-list of 31 skills in four branches, built from the VIA strengths, the English National Curriculum and PSHE, for building a concept map with Bessie at the centre. Epistemic status: a `map` note, not a claim. Tooling tier reached: MCP lexical (`obsidian-llmeon` `wikilinks`) plus `rg` and direct reads. Semantic search was not needed; the overlap was established by reading the candidate notes, so coverage confidence is high for the notes named here and medium for anything beyond them.

### Search Execution (Triad)

Overlap was found from the note's own structure and backlinks, not by open-ended search:

1. Literal: backlinks to the note -> [[MOC - Character and Virtue]] (2 links), and three branch notes (one link each).
2. Abstract: the MoC's §5 "Applied—Character Development for Children" -> lists the parent plus three of four branches.
3. Functional: the MoC's own Tensions section -> states that the "Thinking & Creating Skills" branch "is still only a heading inside" this note.

### Classification

| Note | Class | Evidence | Canonical? |
|---|---|---|---|
| [[MOC - Character and Virtue]] | Related, home map | §2 carries the six virtues and 24 strengths with glosses; §5 already described the child-facing layer | Yes (for the framework and framing) |
| [[Heart & Friendship Skills (Your Kind Heart)]], [[World & Wonder Skills (How You Connect to the World)]] | Duplicate of two branches | Same seven items each, same wording, same source labels | Yes (for their branches) |
| [[Inner Strength & Resilience Skills (Your Strong Spirit)]] | Duplicate of one branch, minus labels | Same seven items and wording; per-item source labels were missing | Yes, after adding them |
| The "Thinking & Creating" branch | **Not held elsewhere** | Named as a gap in the MoC's §5 and Tensions | New note created |

### Actions Applied

| File | Action | One-line diff summary | Status |
|---|---|---|---|
| Thinking & Creating Skills (Your Clever Brain) | create | New sibling note: the eight items verbatim with their source labels, `implements` the MoC, links to the five VIA strength atoms | Done |
| Inner Strength & Resilience Skills | merge | Added a "Curriculum mapping" line restoring the dropped labels; replaced the parent link with a pointer to the MoC §5; removed the `extends` edge to the parent | Done |
| Heart & Friendship Skills; World & Wonder Skills | link | Removed the `extends` edge to the parent (each keeps its `implements` edge to the MoC) | Done |
| MOC - Character and Virtue | merge | §5 gains the concept-map activity framing and a bullet for the new Thinking note; the parent bullet, the gap line and the "Missing sibling note" tension are removed; the parent link is gone from `see_also` | Done |
| A Concept Map for a Flourishing Human | deprecate | `status: superseded`, `superseded_by` (the MoC and the four branch notes), `archive` added to tags, body replaced by the redirect notice; the original text is in git history | Done |

### Conservation Check

| Unique claim in the deprecated note | Where it now lives |
|---|---|
| Thinking & Creating branch: eight skills with descriptions and source labels | [[Thinking & Creating Skills (Your Clever Brain)]] |
| Heart & Friendship branch (seven skills, labels) | [[Heart & Friendship Skills (Your Kind Heart)]], already identical |
| World & Wonder branch (seven skills, labels, PSHE definition) | [[World & Wonder Skills (How You Connect to the World)]], already identical |
| Inner Strength branch (seven skills) | [[Inner Strength & Resilience Skills (Your Strong Spirit)]]; per-item source labels restored by the new "Curriculum mapping" line |
| Six VIA virtues with one-line glosses | [[MOC - Character and Virtue]] §2 (glosses there are worded slightly differently, same content) |
| Concept-map activity: name in the centre, branch to each group, pick what fits; the shift from "things you must do for school" to "all the parts that make up you" | [[MOC - Character and Virtue]] §5 intro |
| Framing that the list combines VIA, the National Curriculum and broader life skills | [[MOC - Character and Virtue]] §5 (already stated) |

### Edges Written

| File | Edge line | Kind | Target verified? |
|---|---|---|---|
| Thinking & Creating Skills | `[implements:: [[MOC - Character and Virtue]], strength=3, confidence=high]` | structural | Yes |

Edges removed: the three `extends:: [[A Concept Map for a Flourishing Human]]` lines on the Inner Strength, Heart & Friendship and World & Wonder notes. All three were structural, so the audit is unaffected.

### Needs your call

| Item | Why it was not done |
|---|---|
| The child-facing intro wording | The parent's opening ("a brilliant, hands-on way to help Bessie visualise her growth") was addressed to a parent and was not carried over; only the activity instruction and the framing sentence were kept. It is in git history if you want it back. |
| Literacy, numeracy and digital literacy | These three come from the National Curriculum and have no atomic notes; the new note says so. |
| Inner Strength branch note sits in `30_Library/MoC/` | Its siblings sit in `100_zettelkasten/`. Left where it is. |

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings (2911 notes, 1415 edges). Every wikilink in the six edited notes resolves, and no note outside the audits still links to the deprecated one.
- `--audit`: 41 gaps, unchanged.
- Confidence: high on conservation (each item compared by reading). UNSURE: whether you want the parent-addressed intro kept; see above.

## Next action

Open `30_Library/MoC/MOC - Character and Virtue.md` at section 5 and check that the concept-map framing reads the way you want.
