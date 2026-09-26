---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-compare-oneself-to-yesterdays-self
title: 2026-09-24-compare-oneself-to-yesterdays-self
type: note
---

## Positioning — [[Compare Oneself to Yesterday's Self Not Others]] — 2026-09-24

> Prompt: [[Orphan Note Positioning & Thread Audit]], Part 1 only. Nothing in `30_Library/` has been edited. Part 2 and Part 3 are pending your go-ahead.
>
> Output Contract: [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]. Confidence is stated per section, and evidence is cited by `[[wikilink]]`.

### Baseline

**Thin, not a true orphan.**

- **Outbound:** 0 (`wikilinks outgoing` returned nothing). There are no typed edges either.
- **Inbound:** 1, from [[MOC - Divergent Thinking vs Specialization]] line 40, under `### Personal Development`.
  - That MoC's `rel::` grammar is not parsed by `edge_lint.py` (per [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] §5.1), so the link carries no graph weight.
  - The fit is incidental: the note appears as a side-item in a MoC about generalism.
- **Frontmatter:** `type: claim`, `conformant: false`. It is missing `proposition`, `contradicts`, `evidence_links` and `epistemic_status`.
  - The title is a topic-style phrase, not "a single declarative sentence" as [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.1 requires.
- **Body:** two paragraphs (Summary and Details). The Details paragraph names "an iterative learning philosophy" without linking it.

### Search Execution

Tooling was `obsidian-llmeon` (semantic, BM25 text and wikilink graph) plus direct file reads of candidates. `edge_lint.py --path` reported "scanned 0 notes" for both the Target and the MoC, so that run confirms nothing.

| Query | Style | Result |
|---|---|---|
| "comparing yourself to others is demotivating; measure progress against your past self" | conceptual variant | [[Habit Change Must Align With Personal Values Not External Expectations]], [[Progress is Built From Small Boring Repeated Actions]], [[Externalizing Progress Makes it Tangible and Motivational]], [[Sociometer Theory Treats Self-Esteem as a Monitor of Perceived Social Acceptance]], [[Self-Esteem and Identity]] |
| "incremental improvement, iterative learning, small daily gains, growth mindset" | functional equivalent | [[Continuous Iterative Learning Mindset is Essential]], [[Celebrate Small Successes to Build Routine Momentum]], [[Systems Drive Progress Through the Compounding Effect of Atomic Habits]], [[Consistency and Momentum]] |
| "social comparison envy status anxiety" | literal anchor (BM25) | [[SoT - Social Cognition & Self-Perception]] §F, [[MOC - Social Perception and Self-Awareness]], [[Mental Models as Social Status Signals]] (the rest was noise on "social") |
| Manual follow-up | literal anchor | [[SoT - ADHD Self-Compassion & Strengths]] §2.1 "Unwinnable Game of Comparison" (found by reading, not by search) |

**Existence checks**
- Confirmed present by file read: [[MOC - How to Build Discipline]], [[MOC - The Science of Making and Breaking Habits]], [[Process Over Outcome Mindset]], [[SoT - The Evolutionary Biology of Status]], [[SoT - Personal Agency and Transformation]].
- No atomic note on **social comparison** exists. Only [[SoT - Social Cognition & Self-Perception]] §F (three lines) covers it, and the MoC above also lists it as a gap.

### Candidate Connections

| Candidate | Use / Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[Habit Change Must Align With Personal Values Not External Expectations]] | **Use.** Its "growth aligned with external standards is fragile" is the general principle. The Target is the specific case where the external standard is another person. | Target stays coherent | Partly substitutable | Retracting it weakens the Target's mechanism | **PASS (weak).** `extends` (specialisation), confidence=medium |
| [[Continuous Iterative Learning Mindset is Essential]] | **Use.** The Target's own Details text says it aligns "with an iterative learning philosophy." | Coherent | Yes | No move | **FAIL tests, topically real.** Plain link |
| [[Progress is Built From Small Boring Repeated Actions]] | Mention. Shares "incremental gains" vocabulary. | Coherent | Yes | No move | **Plain link** |
| [[Externalizing Progress Makes it Tangible and Motivational]] | Use, but conditional. A "yesterday" baseline needs a persisted record, and this note supplies the mechanism for that. | Coherent | Partly | The Target does not currently assert this dependency | **Plain link** (a `depends_on` would put an unstated premise in the Target) |
| [[SoT - Social Cognition & Self-Perception]] §F | **Use.** Automatic status comparison is the mechanism behind "comparison to others" being the default. | Coherent | Yes (see also [[SoT - The Evolutionary Biology of Status]]) | No move | **Plain link** to the mechanism section |
| [[SoT - ADHD Self-Compassion & Strengths]] §2.1 | **Use.** The SoT documents the failure mode the Target warns against. | Coherent | Partly | Retracting the Target would move the SoT's §2.1 support | **Direction inverts.** If typed, the edge belongs on the SoT side (`supports` → Target). Your call, see below |
| [[Sociometer Theory Treats Self-Esteem as a Monitor of Perceived Social Acceptance]], [[Self-Esteem and Identity]] | Mention. About acceptance, not comparison. | n/a | n/a | n/a | **Not proposed** |
| [[Mental Models as Social Status Signals]] | Mention. | n/a | n/a | n/a | **Not proposed** |

**Homes considered**

| Hub | Fit |
|---|---|
| [[MOC - Divergent Thinking vs Specialization]] (current) | Poor. It is off-topic for the note's claim. |
| [[MOC - How to Build Discipline]] | Moderate. It already houses [[Progress is Built From Small Boring Repeated Actions]]. |
| [[MOC - The Science of Making and Breaking Habits]] | Unread beyond existence. Fit unverified. |
| [[MOC - Social Perception and Self-Awareness]] | Moderate. It has a Systematic Biases section, and its `### Meta-Awareness and Calibration` section is closest. |

Confidence: **medium**. The homes were not read in full.

### Patch A — Typed Edges to Write (six-word vocabulary only)

| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `30_Library/100_zettelkasten/Compare Oneself to Yesterday's Self Not Others.md` | `[extends:: [[Habit Change Must Align With Personal Values Not External Expectations]], confidence=medium]` | The Target specialises the general external-standards principle. This is structural only, so the compiler ignores it for C1–C3 and it will not move any exposure score. | Yes (file read) |

**Not proposed, and why:**
- I found no `supports` or `depends_on` candidate that passes all three tests.
- Do not treat that as a defect in the note. It is a short prescriptive claim with no `evidence_links`, and the evidence side is Patch D below.

### Patch B — Plain Links / MoC Anchors (Leon applies)

**Related section to add to the Target** (per the Annotated Link Rule):

| File | Proposed line | Where it goes |
|---|---|---|
| Target | `- [[Continuous Iterative Learning Mindset is Essential]]—_The "iterative learning philosophy" the Details paragraph invokes but does not link._` | New `### Related` |
| Target | `- [[Progress is Built From Small Boring Repeated Actions]]—_The incremental-gains mechanism that makes yesterday a meaningful baseline._` | `### Related` |
| Target | `- [[Externalizing Progress Makes it Tangible and Motivational]]—_A comparison with yesterday needs a persisted record of yesterday._` | `### Related` |
| Target | `- [[SoT - Social Cognition & Self-Perception]]—_§F Social Comparison: why comparing with others is automatic and hard to switch off._` | `### Related` |
| Target | `- [[SoT - ADHD Self-Compassion & Strengths]]—_§2.1: the "Unwinnable Game of Comparison" as a worked failure mode._` | `### Related` |

**MoC anchoring (options for you to choose)**

| File | Proposed line | Where it goes |
|---|---|---|
| [[MOC - How to Build Discipline]] | `- [[Compare Oneself to Yesterday's Self Not Others]]—_Judge progress against your own earlier baseline, not against other people._` | Next to the [[Progress is Built From Small Boring Repeated Actions]] entry (line 24), matching that entry's pattern |
| [[MOC - Social Perception and Self-Awareness]] | Same line | `### Meta-Awareness and Calibration` |

Keep the existing [[MOC - Divergent Thinking vs Specialization]] entry, or move it. That is your call.

**Reverse-direction plain link** (optional): add [[Compare Oneself to Yesterday's Self Not Others]] to §2.1 of [[SoT - ADHD Self-Compassion & Strengths]].

### Patch C — Frontmatter Conformance (Leon applies)

| Field | Current | Proposed |
|---|---|---|
| `proposition` | missing | "Comparing your current self with your own previous baseline sustains motivation better than comparing yourself with prodigies or other people." |
| `epistemic_status` | missing | `medium` (plausible, with corroborating book passages but no linked Evidence notes yet) |
| `evidence_links` | missing | `[]` for now. See Patch D. |
| `contradicts` | missing | `[]` |
| `conformant` / `non_conformance_reason` | `false` / 4 missing fields | Re-evaluate to `true` after the fields above are added |
| `title` | topic-style phrase | **Do not rename now.** The contract wants a declarative sentence, but a rename touches the one MoC backlink. A candidate: "Comparing Yourself to Your Yesterday Self Sustains Motivation Better Than Comparing to Others." |

`tags` is fine as is.

### Patch D — Further Reading, Personal Library (Leon applies)

Two ARCHILLES queries ran in semantic mode, with the mechanism paraphrased. Relevance was ≳0.30 in each case, but the passages were read in full, and only the following bear on the claim.

| Book — location | Link | What it corroborates | Relevance |
|---|---|---|---|
| Scott Young, *Ultralearning* — ch. 14, "Be Careful with Competition" (p. 1379 in index) | `calibre://view-book/GCcalibreBooks/710/EPUB` | The reference group you compare yourself to changes motivation. Believing you will always be behind everyone else "robs you of the motivation to work hard." | 0.40 |
| James Clear, *Atomic Habits* — ch. 20, p. 200 | `calibre://view-book/GCcalibreBooks/690/EPUB` | Without reflection "we have no process for determining whether we are performing better or worse compared to yesterday." The closest textual match to the Target's framing. | 0.38 |
| Paul Gilbert, *The Compassionate Mind* — ch. 5 "Social pressures and comparisons" | `calibre://view-book/GCcalibreBooks/120/EPUB` | Comparison with others feeds the threat system and anxiety, and competitive comparison leaves people "feel[ing] like failures." | 0.42 |

These are semantic-similarity hits, not confirmed on-topic readings of the whole book.

**Discarded**
- Dweck's *Mindset*, Syed's *Black Box Thinking*, Davis and Daniels' *Effective DevOps*, Marquet's *Leadership Is Language*, Kahneman's *Thinking, Fast and Slow*, Laloux and Schein: keyword or theme overlap on growth mindset, with no comparison-to-others content.
- Syed's *Bounce* (stereotypes and race in sport) also surfaced and does not bear on the claim.

### Claim Stubs Written

**None.** `raw/proposed-claims/` and the §2.4 stub route referenced in the prompt do not exist in the current `AGENTS.md`. The prompt appears out of date on this point.

### No evidence / needs your call

| Candidate | Why untestable |
|---|---|
| Atomic note on **social comparison** as a mechanism (Festinger-style) | Absent from `100_zettelkasten`. Only the SoT §F stub exists. It would be the natural `supports` target for this claim. Do you want a new note drafted, or should the SoT section suffice? |
| [[SoT - ADHD Self-Compassion & Strengths]] §2.1 as an edge | The relationship is real but sits inside an SoT section, not a note. Typing it means a `supports` line in the SoT pointing at this Target. Decide whether that hub should carry the edge. |
| Whether [[Process Over Outcome Mindset]] belongs | Existence confirmed, but I did not read it. Unrated. |

### Divergences found (for your attention)

1. **Write-scope conflict in the prompt.** `AGENTS.md` §9.3 now lets agents write freely in `30_Library/100_zettelkasten/`, `SoT/`, `MoC/` and `200_Projects/`, including body content. [[Orphan Note Positioning & Thread Audit]] still applies the stricter "propose, don't write" reading. I followed the prompt for Part 1. Say whether Part 2 should apply Patches B and C directly or leave them to you.
2. **`edge_lint.py --path`** reported "scanned 0 notes" for single-file paths. Validate against the vault root before trusting a "0 errors" result.

### Validation

- `edge_lint.py`: not yet meaningful. Nothing has been written, and the single-file run scanned 0 notes.
- Confidence: **medium**.
  - The candidates that passed were read in full.
  - The home MoCs were not read in full.
  - Patch A is deliberately thin.

---

## Applied (Part 2)

Authorised by Leon: "continue with all patches/changes". Applied under `AGENTS.md` §9.3.

| File | Change | Status |
|---|---|---|
| `30_Library/100_zettelkasten/Compare Oneself to Yesterday's Self Not Others.md` | Patch A: `[extends:: [[Habit Change Must Align With Personal Values Not External Expectations]], confidence=medium]` appended | Applied |
| Same | Patch B: `### Related` with 6 annotated links | Applied |
| Same | Patch C: added `proposition`, `epistemic_status: medium`, `evidence_links: []`, `contradicts: []`; `conformant: true`, empty `non_conformance_reason`; `modified` updated. Title unchanged | Applied |
| Same | Patch D: `### Further Reading (Personal Library)` with 3 `calibre://view-book/GCcalibreBooks/<id>/EPUB` links (710, 690, 120) | Applied |
| `30_Library/MoC/MOC - How to Build Discipline.md` | One anchor line after the `Progress is Built From Small Boring Repeated Actions` entry | Applied |
| `30_Library/MoC/MOC - Social Perception and Self-Awareness.md` | One anchor line at the end of `### Meta-Awareness and Calibration` list | Applied |
| `30_Library/SoT/SoT - ADHD Self-Compassion & Strengths.md` | One `See also` sub-bullet under §2.1 | Applied (plain link only, no typed edge) |
| `MOC - Divergent Thinking vs Specialization` | Existing entry kept | Untouched |
| New social-comparison atomic note | Not created (needs your call, see above) | Skipped |

**Judgement calls made without asking you**
- Both MoCs were used as homes (one primary, one secondary).
- The SoT §2.1 reverse link is a plain `See also`, not a `supports` edge.

**Validation:** `edge_lint.py` over the whole vault reports `0 error(s), 0 warning(s)` (2834 notes, 1372 edges).

---

## Part 3 — Thread Audit Report

### Verdict

**The Target is not a node in the argument graph.** `--why` and `--impact` both return "no node found". Its only typed edge is `extends`, which the compiler ignores for C1–C3. Exposure is 0, it has no dependents and no threads.

That is the correct outcome for this note. It is a short prescriptive claim whose only structural relation is a specialisation, so I have not invented a thread for it.

### Exposure list

None. Nothing in the vault rests on the Target through `supports` or `depends_on`.

### Threads

None to extract (no root, chain or tip).

### Traversal manifest

| Direction | Node | Edge / link | Termination |
|---|---|---|---|
| Out | [[Habit Change Must Align With Personal Values Not External Expectations]] | typed `extends` | Depth cap. It is `type: principle` and not part of the claim graph. |
| Out | [[Continuous Iterative Learning Mindset is Essential]], [[Progress is Built From Small Boring Repeated Actions]], [[Externalizing Progress Makes it Tangible and Motivational]] | plain | Attribution (sibling atoms) |
| Out | [[SoT - Social Cognition & Self-Perception]], [[SoT - ADHD Self-Compassion & Strengths]] | plain | Hub |
| In | [[MOC - Divergent Thinking vs Specialization]], [[MOC - How to Build Discipline]], [[MOC - Social Perception and Self-Awareness]], [[SoT - ADHD Self-Compassion & Strengths]] | plain (one `rel::` line, unparsed) | Hub |

### Use vs mention on the bare links

All five Related links are **mention or weak use**. Each failed denial, substitution and load in Part 1. They are correctly left untyped.

### Patch A (typings) / Patch B (sever candidates)

- **Typings:** none new. The two candidate promotions are held back because they need evidence notes that do not yet exist:
  - `supports` from the Target to a future social-comparison note.
  - `supports` from SoT §2.1 to the Target.
- **Sever candidates:** none.

### No evidence

- The claim's empirical support exists only as three book passages. They sit in Further Reading and are not `[[Evidence]]` notes, so `evidence_links` is `[]`. The note is schema-conformant but **ungrounded in the graph's terms**.

### Pathologies found

1. **Unparsed grammar:** the only pre-existing inbound link sits in a line using `rel::`. `edge_lint.py` ignores that grammar, so the previous link never counted toward the graph.
2. **Conformant but ungrounded:** `conformant: true` with `evidence_links: []` and `epistemic_status: medium`. That is allowed by the schema, but the epistemic status rests on the reader's trust in Further Reading, not on graph evidence.
3. **Title is topic-shaped,** not a declarative sentence. Left unchanged to avoid breaking backlinks.

### Frontier

Nearest unexplored neighbours are [[Process Over Outcome Mindset]] (unread) and any future social-comparison note.

### Next action

Create three Evidence notes from the Young, Clear and Gilbert passages and list them in this note's `evidence_links`: `uv run --with pyyaml python3 10_System/scripts/edge_lint.py --route "Comparing yourself with your own past baseline sustains motivation better than comparing with others"` to check for duplicates first.

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings.
- Confidence: **medium** (the two MoC homes were only read around the insertion point).
