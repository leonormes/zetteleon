---
conformant: true
created: 2026-10-10T00:00:00+00:00
modified: 2026-10-22T15:11:05+00:00
non_conformance_reason: ''
permalink: llmeon/90-audits/2026-10-10-impact-of-set-2-breakthroughs
tags: [audit, domain/pkm]
title: Audit - Impact of Set 2 Breakthroughs
type: link_report
---

## Positioning—[[Impact of Set 2 Breakthroughs]]—2026-10-10

> Output Contract (TAC): confidence stated per section, evidence by wikilink, `UNSURE` or `NO EVIDENCE` where a claim could not be tested. Tooling: Obsidian MCP search (semantic search errored, so lexical plus wikilink graph only; coverage claims are downgraded accordingly), `edge_lint.py`, ARCHILLES CLI.

### Baseline

Thin, not a true orphan.

- Inbound: 1, from [[SoT - Conventional Problem Solving]] (line 96, "How new paradigms become conventional").
- Outbound: 2 bare links, `[[Generative Intelligence]]` and `[[Applicative Intelligence]]`. The second resolves through an alias on [[SoT - Conventional Problem Solving]]. The first does not resolve: [[SoT - Generative Intelligence]] has no `Generative Intelligence` alias, and the wikilink graph reports it unresolved. [[Fundamental Insight Creation]] carries the same dangling link. Resolved after Part 3: the alias `Generative Intelligence` was added to [[SoT - Generative Intelligence]] (see Follow-up fix). Note the wikilink tool does not resolve aliases at all (it also reports the working `Applicative Intelligence` alias as unresolved), so it cannot confirm the fix; check in Obsidian.
- Typed edges: none. `edge_lint.py --why` reports no node found, so it is outside the argument graph.
- Frontmatter: `type: permanent` (non-canonical), no `conformant` or `non_conformance_reason`, legacy `updated: null`, string `last_reviewed: 'null'`.
- Protection: no `own_words`, not in `01_journals/` or `20_Thinking/`. Writable under AGENTS §9.3.

### Search Execution

- "Set 1 Set 2 generative applicative intelligence" (functional equivalent, lexical) -> [[SoT - Generative Intelligence]], [[SoT - Conventional Problem Solving]], [[Fundamental Insight Creation]], [[Kuhn's Four-Stage Model of Paradigm Collapse]], [[Success is Connection Not Mastery]], [[MOC - Theory and Reality (Godfrey-Smith)]]
- Literal "Set 2" / "Set 1" -> only this note and the inbound SoT. The Set 1 / Set 2 labels are not defined anywhere else in the vault.
- Backlinks and outgoing wikilinks (graph) -> as in Baseline.
- Semantic queries ("rare fundamental insights open new fields", "paradigm shift versus normal science") -> tool error, not run. Confidence in "no better sibling exists" is therefore medium.
- MoC membership: only [[MOC - Theory and Reality (Godfrey-Smith)]] lists [[SoT - Generative Intelligence]]; no MoC lists this note or [[Fundamental Insight Creation]].

### Candidate Connections

| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[SoT - Generative Intelligence]] | Use. Defines Set 2 (paradigm creation); the target states a consequence of it. | Without it "Set 2" is undefined | No equal | Moves definition, not confidence | Pass, structural -> `extends` |
| [[Kuhn's Four-Stage Model of Paradigm Collapse]] | Use. Stage 4 (Model Revolution) hands over to Stage 1 (Normal Science) in the new paradigm, which is the "creates new fields for conventional problem-solving" half of the claim. Atom is `axiom: true`. | Denying the cycle removes the mechanism | Weak alternatives only | Retracting it lowers confidence in the target | Pass -> `depends_on`, confidence medium (covers only the structural half) |
| [[SoT - Conventional Problem Solving]] | Use. Set 1; already links back with the same relation. | Set 1 undefined without it | No equal | Low | Topical-logical, but inbound already exists -> plain link |
| [[Fundamental Insight Creation]] | Mention. Describes how a breakthrough is made, not what it does afterwards. | Target survives | Other creation notes would serve | None | Plain link |
| [[Success is Connection Not Mastery]] | Mention. Applies the framework to explorer minds. | Target survives | Yes | None | Skip |
| [[Flawed Mental Models Limit Mastery]] | Mention. The applicative ceiling, not breakthrough impact. | Target survives | Yes | None | Skip |
| [[Paradigm Shifts Complete Through Generational Turnover, Not Persuasion]], [[A Paradigm Only Collapses When a Viable Replacement Exists]] | Mention. About how shifts complete, not their downstream impact. | Target survives | Yes | None | Skip |

Confidence: medium (lexical search only).

### Patch A—Typed Edges (Six-word Vocabulary Only)

| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| Impact of Set 2 Breakthroughs | `[extends:: [[SoT - Generative Intelligence]]]` | Structural: the note elaborates what follows from Set 2. Ignored by C1-C3. | Yes, file exists |
| Impact of Set 2 Breakthroughs | `[depends_on:: [[Kuhn's Four-Stage Model of Paradigm Collapse]], strength=3, confidence=medium]` | Feeds C1 and C4. The Kuhn atom is an axiom, so the dependency is grounded. | Yes, file exists |

### Patch B—Plain Links / MoC Anchors

| File | Proposed line | Where it goes |
|---|---|---|
| Impact of Set 2 Breakthroughs | Annotated links to [[SoT - Conventional Problem Solving]] and [[Fundamental Insight Creation]] | New `## Related` section appended |
| SoT - Generative Intelligence | `- [[Impact of Set 2 Breakthroughs]]—_The consequence side: …_` | One line, end of `### The Kuhnian Framework`, after the Ptolemaic entry. Primary home. |
| MoC | None | No MoC fits both notes; [[MOC - Theory and Reality (Godfrey-Smith)]] lists the SoT, not its satellites. No secondary hub. |

### Patch C—Frontmatter Conformance

| Field | Current | Proposed |
|---|---|---|
| `type` | `permanent` | `claim` |
| `conformant` | absent | `false` |
| `non_conformance_reason` | absent | Title is a topic label, not a declarative sentence; renaming would break the inbound link from SoT - Conventional Problem Solving |
| `proposition` | absent | Fundamental insights are rare but disproportionately impactful because each one opens new fields that conventional problem solving can then explore and develop |
| `epistemic_status` | absent | `medium` |
| `evidence_links`, `contradicts` | absent | `[]` |
| `updated` | `null` | removed (legacy, AGENTS §0) |
| `last_reviewed` | `'null'` (string) | removed (bogus string) |

Title not renamed (flagged). `created`, `tags`, `aliases`, `permalink` unchanged.

### Patch D—Further Reading, Personal Library

| Book—location | Link | What it corroborates | Relevance |
|---|---|---|---|
| Theory and Reality—Godfrey-Smith, 5.3 Normal Science, p. 115 | `calibre://view-book/GCcalibreBooks/1611/EPUB` | The normal scientist uses the tools and concepts the paradigm provides, so a new paradigm supplies the puzzles | 0.419 (medium), snippet read and bears on the claim |
| Flow—Csikszentmihalyi, "The Delights of Science" | `calibre://view-book/GCcalibreBooks/292/EPUB` | A paradigm forces scientists to investigate nature in a detail and depth otherwise unimaginable | 0.413 (medium), snippet read and bears on the claim |

Calibre ids and formats were taken from the existing, already-working links in [[SoT - Generative Intelligence]] (same two books), not looked up fresh. No hit speaks to the _disproportionate_ size of impact.

### Claim Stubs Written

None.

### No Evidence / Needs Your Call

| Candidate | Why untestable |
|---|---|
| "Impact is disproportionately large" | No vault note or read passage supports the magnitude claim. Kuhn supports the structure (revolution -> new normal science), not the proportion. Left as the ungrounded half of the claim. |
| Dangling `[[Generative Intelligence]]` in this note and in [[Fundamental Insight Creation]] | Fixing means editing existing text (target) or adding an alias to a hub; both are outside the append-only scope. Suggested fix: change to `[[SoT - Generative Intelligence\|Generative Intelligence]]`, or add `Generative Intelligence` to that SoT's aliases. Done afterwards: the alias was added (see Follow-up fix). |
| Semantic neighbours | Semantic search errored; a rerun could surface siblings missed by lexical search. |

### Applied (Part 2)

| File | Change | Status |
|---|---|---|
| 30_Library/100_zettelkasten/Impact of Set 2 Breakthroughs.md | Patch C: `type` permanent -> claim; added `conformant: false`, `non_conformance_reason`, `proposition`, `epistemic_status`, `evidence_links`, `contradicts`; removed `updated`, `last_reviewed` | Applied |
| same | Patches A, B, D: appended `## Related` (4 annotated links, `extends` and `depends_on` edges) and `### Further Reading (Personal Library)` (2 entries). Existing prose and the two bare links untouched | Applied |
| 30_Library/SoT/SoT - Generative Intelligence.md | Patch B: one annotated line added at end of `### The Kuhnian Framework` | Applied |

### Validation

- `edge_lint.py` (whole vault): 0 new errors. The 4 errors present are all in files I did not touch, each a dangling `Mistaking the Map for the Territory` target (the note shows as deleted in `git status`). Edge count rose 1417 -> 1419 (the two new edges). 0 warnings.
- Confidence: medium (lexical search only; semantic search errored).

---

## Part 3—Thread Audit Report—seed: [[Impact of Set 2 Breakthroughs]]

### Verdict

The note is now a node in the argument graph, with one grounded dependency and one ungrounded half. The _structural_ half of the claim (a breakthrough creates ground for conventional work) rests on an axiom atom. The _magnitude_ half ("disproportionately large") rests on nothing in the vault.

### Exposure List

- Dependents: 0 (`--impact`: no dependents recorded). Only [[SoT - Generative Intelligence]] and the Conventional Problem Solving SoT link to it, and neither depends on it.
- Exposure: 0. It sits at the tip of a chain, so a defect here moves nothing downstream.

### Threads

| Part | Detail |
|---|---|
| Root | [[Kuhn's Four-Stage Model of Paradigm Collapse]] (`axiom: true`) |
| Chain | Kuhn -> (compiler also reaches) [[Ptolemaic System as a Patched Flawed Model]] -> [[Open Knowledge Systems Prevail Over Closed Systems]] / [[Systems Generate Internal Logic in Isolation]] |
| Tip | [[Impact of Set 2 Breakthroughs]] |
| Weakest link | `Systems are Blind to Their Broader Context`, shown `[?]` (neither axiom nor evidence-backed). It is inherited via the Ptolemaic branch, not introduced by this run. |
| Cheapest defeater | Show a paradigm shift whose follow-on work was _smaller_ than the shift itself, or that normal science did not resume inside the new paradigm. Kuhn's cycle does not rule this out, because it describes stages and not their relative size. |

### Traversal Manifest

- Outbound: [[SoT - Generative Intelligence]] (`extends`, structural), [[Kuhn's Four-Stage Model of Paradigm Collapse]] (`depends_on`), [[SoT - Conventional Problem Solving]] and [[Fundamental Insight Creation]] (plain links, use-vs-mention checked above).
- Inbound: [[SoT - Conventional Problem Solving]] (plain link), [[SoT - Generative Intelligence]] (plain link, new this run).
- Termination: hub ([[SoT - Generative Intelligence]]), axiom ([[Kuhn's Four-Stage Model of Paradigm Collapse]]), depth cap on the Ptolemaic subtree.
- Bare links remaining: `[[Generative Intelligence]]` (was dangling; resolved by the alias added in the follow-up fix) and `[[Applicative Intelligence]]` (alias-resolved, mention-level: they are label links, not inferential edges).

### Patch A—Typings

None further. The two edges above were the only candidates that passed all three tests.

### Patch B—Sever Candidates

None. No edge failed on re-test.

### No Evidence

- Magnitude of impact ("disproportionately large"): no source in vault or library.
- Uniqueness: the claim that Set 2 insights are _rare_ is also unsourced.

### Pathologies Found

- Dangling `[[Generative Intelligence]]` in the target and in [[Fundamental Insight Creation]] (alias missing on the SoT). Fixed in the follow-up below.
- Label coupling: "Set 1 / Set 2" appears only in this note and is defined only here (now stated in `## Related`). It does not appear in either SoT, which use Applicative and Generative.
- Type drift fixed: `permanent` was non-canonical.
- Title is a topic label rather than a claim sentence (flagged, not renamed).
- Inherited: an ungrounded `[?]` premise upstream in the Ptolemaic subtree.

### Frontier

- A sentence-form title such as "Rare Fundamental Insights Open Fields That Conventional Problem Solving Then Develops" would make this a conformant atom, but renaming needs the inbound link in [[SoT - Conventional Problem Solving]] updated in the same step.
- A source for the magnitude claim: [[The Beginning Infinity: Explanations That Transform the World]] (Deutsch, ch. 1) surfaced as a library hit but its snippet did not bear on the claim, so it was discarded unread. It may be worth a targeted ARCHILLES query.

### Next Action

Open `[[Generative Intelligence]]` in this note in Obsidian and confirm it lands on [[SoT - Generative Intelligence]]; revert the alias in that SoT's frontmatter if it does not.

---

## Follow-up fix—2026-10-10

- Change: added `Generative Intelligence` to the `aliases` of [[SoT - Generative Intelligence]]. This resolves the bare `[[Generative Intelligence]]` link in four notes at once: [[Impact of Set 2 Breakthroughs]], [[Fundamental Insight Creation]], [[SoT - Conventional Problem Solving]] and [[SoT - Reframe Your Mindset From Pretender to Explorer]]. No link text was edited. None of the four is own-words protected.
- Why an alias and not four edits: it mirrors how `Applicative Intelligence` already resolves, and leaves existing prose untouched.
- Validation: `edge_lint.py` whole vault still 4 error(s), 0 warning(s), all pre-existing in untouched files. The wikilink tool cannot confirm alias resolution, so verification in Obsidian is still outstanding.
