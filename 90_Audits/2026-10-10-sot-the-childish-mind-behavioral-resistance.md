---
conformant: true
created: 2026-10-10T00:00:00+00:00
modified: 2026-10-22T15:11:05+00:00
non_conformance_reason: ''
permalink: llmeon/90-audits/2026-10-10-sot-the-childish-mind-behavioral-resistance
tags: [audit, domain/pkm]
title: Audit - SoT The Childish Mind Behavioral Resistance
type: link_report
---

## Refresh—[[SoT - The Childish Mind (Behavioral Resistance)]]—2026-10-10

> Prompt: [[Note Refresh & Link Auditor]] (v4). Output Contract (TAC): confidence per section, evidence by wikilink, `UNSURE` where a claim could not be tested. Semantic vault search errored for the whole run, so vault discovery was lexical plus the wikilink graph; coverage claims are downgraded accordingly.

### Why This Prompt

- [[Knowledge Harvesting & Normalization Agent]] was rejected: its execution phase deprecates or deletes fragment notes, which was not asked for, and its tooling section still uses the retired `retrieve_tools` pattern.
- [[Orphan Note Positioning & Thread Audit]] was rejected: the target is an established SoT with 5 inbound links and conformant frontmatter, not an orphan.
- The target's gap was outbound links only, which is the Link Auditor's brief.

### 1. Audit Summary

- Target note: [[SoT - The Childish Mind (Behavioral Resistance)]]
- Protection: no `own_words`, in `30_Library/SoT/`, writable under AGENTS §9.3.
- Baseline: 0 outbound links, 0 typed edges, 5 inbound:
  - [[SoT - Behavioral Architecture]]
  - [[The Mind Movie Fallacy]]
  - [[Motivation, Volition, and Control are Distinct Aspects of the Action Process]]
  - [[The Quit on the Third Urge Rule]]
  - `30_Library/400_indexes/_link_report_thinking_about_knowledge.md` (an index report, not linked back)
- Not in the argument graph: `--why` reported no node found.
- Broken links found: None (there were no links to break).
- New connections discovered: 10 plain links, 2 of them typed (see §3).
- Frontmatter gaps backfilled: None. `title`, `type: sot`, `tags`, `conformant: true` and `non_conformance_reason` were already present, so nothing was touched.

### 2. Search Execution

Core concepts: dual-process mind (Rider and Elephant), immediate gratification, ego depletion, Mind Movie (Babauta), commitment devices and environmental design.

- Wikilink graph, backlinks of the target -> the 5 inbound above.
- Semantic "Rider and Elephant dual-process…" -> tool error, not run.
- Lexical "ego depletion willpower commitment device environmental design path of least resistance" -> [[SoT - Commitment Devices (Ulysses Pacts)]], [[SoT - Behavioral Architecture]], [[Discipline Is a Property of External Structure More Than of Will]], [[Engineering Action and Bypassing Resistance]], [[Timeboxing Combats the Principle of Least Resistance]], [[The War of Art - Resistance and Turning Pro]] (noisy: stopword matches inflated scores)
- Literal `Elephant` -> [[SoT - Behavioral Architecture]], [[SoT - Social Cognition & Self-Perception]], [[Motivation, Volition, and Control are Distinct Aspects of the Action Process]] and 3 unrelated claim notes
- Literal `ego depletion` -> only the target and [[SoT - Behavioral Architecture]] (no note on the replication question)
- Literal `Babauta` -> the target and [[SoT - Intentional Living]] (a one-line attribution, not a Mind Movie treatment)
- Literal `Pleasure Principle` -> the target only
- Literal `replication crisis` / `failed to replicate` -> no matches anywhere in `100_zettelkasten`, `SoT` or `MoC`
- Literal `delay of gratification / marshmallow / hyperbolic discounting / present bias` -> [[Temporal Discounting is the Cognitive Bias Where People Value Immediate Rewards More]], [[Decision making fallacies]]
- Neighbours read before linking: [[SoT - Behavioral Architecture]], [[The Mind Movie Fallacy]], [[The Quit on the Third Urge Rule]], [[SoT - Commitment Devices (Ulysses Pacts)]], [[Discipline Is a Property of External Structure More Than of Will]], [[Engineering Action and Bypassing Resistance]], [[Temporal Discounting is the Cognitive Bias Where People Value Immediate Rewards More]], [[Motivation, Volition, and Control are Distinct Aspects of the Action Process]]. [[SoT - Perfectionism and Analysis Paralysis]] and [[SoT - Prosthetic Executive Function]] were confirmed to exist and read to frontmatter level only; the link annotations for them rest on their titles and aliases, so treat those two as medium confidence.

### 2b. Personal Library Search (ARCHILLES)

Semantic mode, top 6, one hit per book. Relevance is the tool's score; all are labelled medium.

| Query (paraphrased mechanism) | Hit | Relevance | Verdict |
|---|---|---|---|
| Emotional automatic mind as elephant, reasoning mind as rider | The Righteous Mind, "Central Metaphor" | 0.400 | Discarded: the snippet is a heading only, so the sentences that would bear on the claim were not visible |
| same | The Chimp Paradox, ch. 2 p. 2 | 0.382 | Discarded: a related metaphor, but the snippet is about one anecdote and does not bear on the claim |
| Willpower as a limited resource, depletion effect disputed | Indistractable, ch. 8 "Reimagine Your Temperament", p. 46 | 0.306 | Kept. Snippet reads: Dweck concluded that signs of ego depletion were observed only in those who believed willpower was a limited resource. Bears directly on section 2.3. |
| same | The ONE Thing, ch. 7 | 0.286 | Discarded: restates the limited-willpower view, adds no test of it |
| People imagine change as easy and pleasant, then abandon it | Beyond Belief, ch. 11 "Good Beliefs, Bad Beliefs", p. 171 | 0.411 | Kept. Snippet reads: Oettingen's research shows positive fantasies can reduce motivation when rewards are imagined without the effort. Bears on section 3. |
| same | Stumbling on Happiness, ch. 9, p. 180 | 0.417 | Discarded: a study about judgement of an unrelated scenario |

These are semantic-similarity evidence read from a snippet of roughly 200 characters, not confirmed readings of the books. Author for Beyond Belief was not confirmed, so none is cited.

### 3. Typed Edges

Added:

- `[supports:: [[SoT - Behavioral Architecture]], confidence=medium]`
- `[supports:: [[SoT - Commitment Devices (Ulysses Pacts)]], confidence=medium]`

Tests applied:

| Candidate | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|
| [[SoT - Commitment Devices (Ulysses Pacts)]] | Without the Childish Mind taking over later, a pact has nothing to lock out | No other premise is named in that SoT | Retracting this note weakens its rationale | `supports` |
| [[SoT - Behavioral Architecture]] | Its System > Willpower axiom can stand on ego depletion alone | Ego depletion alone could serve | Partial | `supports`, kept at medium confidence and no `strength` |
| [[Discipline Is a Property of External Structure More Than of Will]] | Claim already rests on [[SoT - Behavioral Architecture]] at strength 5 | Yes | Low | Plain link only, to avoid a redundant second path |
| Other eight neighbours | Topical or mechanism-sharing, not inferential | n/a | n/a | Plain links |

UNSURE (proposed, not written):

| Candidate | Why |
|---|---|
| `depends_on` the ego-depletion mechanism | No vault note carries ego depletion as a claim, so there is no target to point an edge at. |
| `contradicts` on the Dweck finding | The finding exists only as a library passage, and an ebook cannot be an edge target. |

Compiler check: `--impact "SoT - The Childish Mind (Behavioral Resistance)"` now lists [[SoT - Commitment Devices (Ulysses Pacts)]] as a dependent and, through [[SoT - Behavioral Architecture]], the Discipline claim chain beneath it. Edges are `supports`, so they feed exposure and provenance.

### 3b. Further Reading Added

- Indistractable—Nir Eyal, ch. 8 "Reimagine Your Temperament", p. 46 (`calibre://view-book/GCcalibreBooks/687/EPUB`)
- Beyond Belief—ch. 11 "Good Beliefs, Bad Beliefs", p. 171 (`calibre://view-book/GCcalibreBooks/1686/EPUB`)

Calibre ids and formats were looked up read-only in `metadata.db` (both books have EPUB and PDF).

### 4. Execution Artifact

One file edited: `30_Library/SoT/SoT - The Childish Mind (Behavioral Resistance).md`. A single append after the last line of section 3; 28 lines inserted, none removed (`git diff --stat`). Existing prose, frontmatter and aliases untouched.

| Section appended | Content |
|---|---|
| `## 4. Related` > Where the Architectural Implication Is Built Out | 5 annotated links, 2 typed edges |
| `## 4. Related` > Where the Characteristics Are Developed | 5 annotated links |
| `### Tensions` | Ego depletion not settled; "Rider and the Elephant" alias unsourced |
| `### Further Reading (Personal Library)` | 2 entries |

### 5. Validation

- FrontmatterContract: PASS. Unchanged and already conformant.
- `edge_lint.py` (whole vault): 4 error(s), 0 warning(s). All 4 existed before this run, in files not touched (each a dangling `Mistaking the Map for the Territory` target). Edge count 1419 -> 1421, matching the two new edges. 0 new errors.
- Fileclass live validation in Obsidian: not checked.
- Confidence: medium. Lexical search only, two link annotations rest on frontmatter-level reading, and library hits are snippet-level.

### No Evidence / Needs Your Call

| Item | Why |
|---|---|
| Ego depletion replication | No vault note covers it; only the Indistractable snippet. A claim note sourced from the book would let the tension carry an edge. |
| Source for "The Rider and the Elephant" | No vault or library source verified. |
| Mind Movie attribution to Babauta | [[SoT - Intentional Living]] mentions him only in passing; no note or passage here confirms the "Mind Movie" term is his. The target states it as fact. |

### Pathologies and Frontier

- [[SoT - Commitment Devices (Ulysses Pacts)]] names the "Childish Mind" in its text but does not link back, so the pair is linked one way only. Same for [[SoT - Behavioral Architecture]] at the typed level: it plain-links here but carries no edge. Worth adding on the other side if you want symmetry; not done, as this run was scoped to the target.
- [[Temporal Discounting is the Cognitive Bias Where People Value Immediate Rewards More]] is `conformant: false` (missing claim fields). Linking to it is fine, but it is a weak anchor until backfilled.
- Section 3 of the target restates [[The Mind Movie Fallacy]], which already carries an `upstream` pointer here. Splitting section 3 out is a candidate for a separate pass.

### Next Action

Run `uv run --with pyyaml python3 10_System/scripts/edge_lint.py --impact "SoT - Behavioral Architecture"` after deciding whether the ego-depletion tension should be mirrored there, since that SoT shares the exposure.
