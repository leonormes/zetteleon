---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-tacit-vs-explicit-knowledge
title: 2026-09-24-tacit-vs-explicit-knowledge
type: note
---

## Positioning — [[Tacit vs Explicit Knowledge]] — 2026-09-24

> Prompt: [[Orphan Note Positioning & Thread Audit]] v3, fourth run, single pass with no checkpoint.

### Baseline

**Thin, not orphaned.** It is well linked in (7 inbound files) but nearly closed on the outbound side.

- **Inbound (7):** [[Knowledge Transmission Is Reconstruction, Not Copying]], [[Types of Non-Linguistic Knowledge]] (which also carries a typed `extends` pointing here), [[Satisficing Leads to Sub-optimal Solutions]], [[A PKM Is Personal Because Notes Only Represent Ideas Held in One Head]], [[MOC - From Information to Knowledge]] (a `synthesizes` edge), [[Documenting Mental Models Enables Project Re-entry]], [[The Illusion of Shared Understanding in Teams]].
- **Outbound:** 1 resolving link ([[The Illusion of Shared Understanding in Teams]]) and 1 broken link (`[[Bug in the model]]`, no such note).
- **Frontmatter:** `type: 'null'` (a string), no schema fields, `last_reviewed: 'null'`.
- **Shape:** the note defines a distinction and gives one supporting claim, so I typed it as a `concept` (definition, `distinguishes_from`, `used_in_claims`).

### Search Execution

| Query | Style | Result |
|---|---|---|
| "tacit knowledge versus explicit knowledge; knowing how cannot be fully articulated or written down" | conceptual variant | [[Types of Non-Linguistic Knowledge]], [[Comparison - Knowing vs Understanding]], [[2026-07-25-externalising-tacit-knowledge-illusion-of-profundity]], [[Knowledge Transmission Is Reconstruction, Not Copying]], [[Communicating Depends on Modelling What the Listener Already Knows]], [[MOC - From Information to Knowledge]] |
| Backlink graph | literal anchor | the 7 inbound files above |
| Manual reads of the candidates | literal anchor | confirmed [[Flawed Mental Models Limit Mastery]], [[Semantic Diffusion Creates False Alignment]] exist |

### Candidate Connections

| Candidate | Use / Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[The Illusion of Shared Understanding in Teams]] | **Use.** Its "team model" is a patchwork of "often tacit" models. | **Fails.** Its core claim (same words, different models) survives without the tacit/explicit distinction. | Partly | Retracting the concept does not move it | **Plain link.** I first wrote `depends_on` and reverted it (see below) |
| [[Types of Non-Linguistic Knowledge]] | Use. Tacit is one of its five kinds. | n/a | n/a | n/a | **Plain link** (its existing `extends` edge stays) |
| [[Documenting Mental Models Enables Project Re-entry]] | Use. Documenting is making tacit explicit. | Coherent | Yes | No move | **Plain link**, listed in `used_in_claims` |
| [[2026-07-25-externalising-tacit-knowledge-illusion-of-profundity]] | Use. Its mechanism is exactly the tacit context that vanishes on externalising. | Coherent | Yes | No move | **Plain link**, in `used_in_claims` |
| [[Knowledge Transmission Is Reconstruction, Not Copying]] | Use, weak. Limits how far explicit form transmits knowledge. | Coherent | Yes | No move | **Plain link**, in `used_in_claims` |
| [[Semantic Diffusion Creates False Alignment]], [[Flawed Mental Models Limit Mastery]] | Mention. Both are named in the Illusion note's links. | n/a | n/a | n/a | **Plain link** |
| [[Comparison - Knowing vs Understanding]] | Mention. Different axis. | n/a | n/a | n/a | **Plain link**, in `distinguishes_from` |

**Home hub:** [[MOC - From Information to Knowledge]] already places it (line 25), so no new hub line was added. [[MOC - The Gap Between Thought and Language]] lists the taxonomy but not this note. I did not add it: this note is team-scale and the MoC is about thought and language.

### Patch A — Typed Edges

**None written.** No candidate passed the three tests.

The reverted edge: I first added `[depends_on:: [[Tacit vs Explicit Knowledge]], confidence=medium]` to the Illusion note. Running `--impact` showed it made the concept the root of a tree of 20+ downstream claims (through Habit 5 and its dependents), from one definitional note that has no grounds. That result, plus the failed denial test above, means it over-typed a topical link. It was reverted and the Illusion note's body is unchanged. (Its `modified` timestamp moved to 09:20:45 from Obsidian's own write, not from this run.)

### Patch B — Plain Links

Eight annotated bullets added under a new `## Related` on the Target.

### Patch C — Frontmatter

`type` changed from `'null'` to `concept`; added `definition`, `distinguishes_from` (2 links), `used_in_claims` (3 links), `conformant: true`, empty `non_conformance_reason`; `modified` updated. Existing fields kept, including the junk `last_reviewed: 'null'`. The definition text avoids apostrophes and `: `.

### Patch D — Further Reading

CLI fallback, two queries.

| Book — location | Link | What it corroborates | Relevance |
|---|---|---|---|
| *Learning Digital Identity* — Tacit Knowledge and the Physical World | `calibre://view-book/GCcalibreBooks/1165/EPUB` | "We can know more than we can tell": we use walking and riding a bike without being able to explain the mechanism. | 0.41 |

**Discarded:** DDD books on context maps (visible text is about model boundaries, not making tacit knowledge explicit), Building a Second Brain, First You Write a Sentence, The Problems of Philosophy, The Knowledge Illusion (all off-topic in the visible text).

### Claim Stubs Written

None.

### Applied (Part 2)

| File | Change | Status |
|---|---|---|
| `Tacit vs Explicit Knowledge.md` | Patches B, C and D | Applied |
| `The Illusion of Shared Understanding in Teams.md` | Typed edge added, then reverted | Net no change |
| Hubs | Existing home kept | Skipped |

**Validation:** whole-vault `edge_lint.py` reports `0 error(s), 0 warning(s)` (2837 notes, 1375 edges).

### No evidence / needs your call

- **`[[Bug in the model]]`** is a broken link inside the Target's body. I did not touch the body prose. Retarget it or remove it?
- **The Illusion note has `type: ''`** and reads as several fragments. It is the natural place to state the claim that depends on this concept, but it needs typing and cleaning first.
- **Edge direction:** [[Types of Non-Linguistic Knowledge]] carries `extends` pointing at the Target, while its own annotation calls the Target "the team-scale, applied instance" of that taxonomy. That reads as the reverse direction. Not changed.

---

## Part 3 — Thread Audit Report

### Verdict

**The Target is not a node in the argument graph.** `--why` and `--impact` return "no node found". Only structural edges touch it (`extends` and `synthesizes` inbound). Exposure is 0, with no threads.

The attempted `depends_on` edge showed what typing this note would do. It would become a foundation with a large downstream tree and no grounds. That confirms the decision to leave it untyped.

### Traversal manifest

| Direction | Node | Edge | Termination |
|---|---|---|---|
| In | [[Types of Non-Linguistic Knowledge]] | `extends` | Structural |
| In | [[MOC - From Information to Knowledge]] | `synthesizes` | Structural / hub |
| In | Documenting, Knowledge Transmission, Satisficing, PKM, Illusion | plain | Attribution |
| Out | Related links, plus the broken `Bug in the model` | plain | Depth cap |

### Pathologies found

1. **Broken outbound link** (`Bug in the model`).
2. **Possibly inverted structural edge** (Types of Non-Linguistic Knowledge `extends` this note).
3. **Untyped hub of dependents:** the Illusion note (`type: ''`) sits between this concept and a long chain of claims through Habit 5, which is why any typed edge here has an outsized effect.

### Next action

Decide the `[[Bug in the model]]` link: retarget or remove it in `30_Library/100_zettelkasten/Tacit vs Explicit Knowledge.md`.

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings.
- Confidence: **medium**.

---

## Follow-up — Illusion note typed and cleaned

Leon asked for [[The Illusion of Shared Understanding in Teams]] to be typed and cleaned.

### What changed

- **Type:** `''` → `claim`, with `proposition`, `epistemic_status: medium`, empty `evidence_links` and `contradicts`, `conformant: true`, and tags (previously empty).
- **Body:** the four scattered fragments were merged into Summary, Mechanism, Example and Related. Existing sentences were kept; the duplicate `Links:` line and the stray standalone link were folded into the annotated Related list.
- **Two sentences were completed** because the source text was truncated. Please check them:
  1. "…and the fact that most knowledge is." became "…and by the fact that much of what each member knows is tacit (see Tacit vs Explicit Knowledge)." I used "much of", not "most", to match the note's own "often tacit".
  2. "…the more correct model of (a direction/process)" became "…the more correct model of it as a direction or process."

### Corrections to my earlier report

- **`[[Bug in the model]]` is probably not broken.** [[Flawed Mental Models Limit Mastery]] lists "Bug in the Model" as an alias, differing only in case. The MCP resolver returns no path for it, but I cannot confirm Obsidian's own case handling from here. The same link appears in five other notes, and [[Satisficing Leads to Sub-optimal Solutions]] strikes it through as broken, which may be wrong for the same reason. I did not change any of them.
- I said the Illusion note "reads as several fragments" and should be typed before any claim depends on it. Two notes already do (Habit 5 `depends_on` it, and the software-team claim `extends` it).

### Graph consequences

- The note is now a `claim` node and the audit lists it: `The Illusion of Shared Understanding in Teams (depended-on by 1)`, ungrounded.
- **No typed edge was added.** The only candidate ground is [[Semantic Diffusion Creates False Alignment]], but that note describes the same phenomenon from the vocabulary side, so this reads as a **merge candidate**, not a dependency.

### Needs your call

1. Merge the Illusion note with [[Semantic Diffusion Creates False Alignment]]? (The latter is still `type: 'null'`.)
2. Ground the Illusion claim (an Evidence note) or mark it `axiom: true`? Habit 5 and its downstream tree currently rest on it.
3. Confirm my completion of the two truncated sentences.

---

## Follow-up — merge of Semantic Diffusion into the Illusion note

Leon approved the merge. **Survivor:** [[The Illusion of Shared Understanding in Teams]] (a `claim`, with the dependents: Habit 5 `depends_on` it and the software-team claim `extends` it). **Absorbed:** `Semantic Diffusion Creates False Alignment` (`type: 'null'`, no dependents of its own beyond plain links).

| Step | Change |
|---|---|
| Content | The definition and the Kubernetes "replicas" example moved into a new `### Semantic Diffusion` section of the survivor. The note's own mechanism sentence now points to that section. Nothing else in the absorbed note was unique (its `Links:` and `Bug in the model` lines were pointers back to the survivor and to the alias-resolved link). |
| Aliases | Added `Semantic Diffusion` and `Semantic Diffusion Creates False Alignment` to the survivor, so the old title still resolves. |
| Inbound links | Two repointed with a display alias (`Systems Generate Internal Logic in Isolation`, `Habit 5 - Seek First to Understand, Then to Be Understood`). One removed: my own Related line in `Tacit vs Explicit Knowledge`, which would have duplicated its existing body link to the survivor. |
| Self-links | The two links from the survivor to the absorbed note were rewritten or removed, so it does not link to itself. |
| Deletion | `Semantic Diffusion Creates False Alignment.md` removed. Recoverable from git history or the vault backup commits, and the original text is preserved below. |

**Validation:** whole-vault `edge_lint.py` reports `0 error(s), 0 warning(s)` (2837 notes, 1375 edges). No typed edge pointed at the absorbed note, so no edge was lost.

**Untouched:** the older audit files in this folder still mention the old title. They resolve through the new alias and are historical records, so I did not edit them.

**Still open:** the survivor remains ungrounded (depended on by 1, with a downstream tree through Habit 5). Evidence note or `axiom: true`?

### Original text of the absorbed note (for recovery)

```markdown
---
aliases: []
created: 2025-08-29T15:20:28+00:00
last_reviewed: 'null'
modified: 2026-09-24T09:20:43+00:00
permalink: llmeon/30-library/100-zettelkasten/semantic-diffusion-creates-false-alignment
tags: [communication, language, teams, TheHuman/Cognition/mental-model]
title: Semantic Diffusion Creates False Alignment
type: 'null'
updated: null
---

Semantic diffusion occurs when a team uses the same vocabulary to describe different underlying concepts, creating a false sense of alignment.

For example, team members might all agree to add more "replicas," but one person's mental model is of Kubernetes ReplicaSets, another's is of a read-only database replica with replication lag, and a third's is of a simple backup copy. All parties agree on the term but have a completely different picture of the work, leading to integration failures and mismatched expectations.

Links: [[The Illusion of Shared Understanding in Teams]]

[[Bug in the model]]
```


---

## Follow-up — Evidence notes for the Illusion claim

Leon chose to ground [[The Illusion of Shared Understanding in Teams]] with Evidence notes, not `axiom: true`.

| New note | Source | Confidence |
|---|---|---|
| [[Evidence - Evans DDD Reference Domain Experts and Developers Use Different Languages in the Same Team]] | Evans, *Domain-Driven Design Reference*, Ubiquitous Language section (Calibre id 396) | 0.5 |
| [[Evidence - Evans DDD Meanings of Words Are Slippery Because All Language Rests on a Model]] | Evans, *Domain-Driven Design*, Ubiquitous Language chapter (Calibre id 313) | 0.45 |

**How the quotes were obtained:** the ARCHILLES CLI truncates passages, and the MCP server was disconnected, so I called its search API directly to read full passages. Both quotes are verbatim; the first has whitespace normalised (the PDF text had doubled spaces). Page numbers were not captured by the index, and the notes say so.

**Scope stated in each note:** both support the *divergence* half of the claim (different roles and words carry different models). Neither shows that members *believe* they are aligned, or that the mismatch only surfaces in a crisis. The claim keeps `epistemic_status: medium`.

**Graph result:** the claim's `evidence_links` lists both notes, and each Evidence note carries `supports_claims` plus an inline `supports` edge. `--why` now shows the claim as supported and bottoming out on evidence, and it no longer appears in the `--audit` foundation-gap list. Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2839 notes, 1377 edges).

**Weakest link:** the evidence is two general statements from one author about software design, not a study of team behaviour. A team-cognition source (shared mental models research) would strengthen it.

---

## Follow-up — value check and ProdOS linking for the Illusion note

**Verdict: keep, as a specialisation.** The general theory already exists in [[SoT - Communication & Misunderstanding (The Experiential Filter)]] ("misunderstanding is the default", "Assumption of Divergence", explicit clarification). The Illusion note adds the team-scale case, the vocabulary route (the merged semantic-diffusion material), and now evidence. It carries real weight: [[Habit 5 - Seek First to Understand, Then to Be Understood]] depends on it, the software-team claim extends it, and five other notes link in.

**Where it earns its place in ProdOS**
- [[Protocol - Context Injection]]: its Ubiquitous Language block is the human-to-LLM version of the same problem.
- [[Protocol - Diagnose an Agent Failure]]: the `ambiguous-terminology` and `unclear-user-requirement` classes.

**Linked**
| File | Change |
|---|---|
| The Illusion note | `extends` edge to the Communication SoT (medium), Related bullet, and a `### Where It Applies in ProdOS` section (3 links) |
| Protocol - Context Injection | one annotated bullet under Related Concepts |
| Protocol - Diagnose an Agent Failure | new `## Related` section with one bullet |
| SoT - Communication & Misunderstanding | new `## Related` section |
| SoT - Mental Models in Software Development | one bullet under Related Knowledge |

**Deliberately not linked:** [[Protocol - Vague-to-Action]] and [[Protocol - Weekly Command Centre]] are about personal task initiation, not shared understanding. No typed edge was written from either protocol: the protocols stay coherent if the claim were false, so those links are plain and annotated.

**Not done:** no MoC lists the Illusion note or its claim neighbour; the cluster is anchored through the SoTs above. Adding it to a MoC (e.g. [[MOC - AI Software Engineering]]) is left for you.

**Validation:** whole-vault `edge_lint.py`: 0 errors, 0 warnings (2839 notes, 1378 edges).
