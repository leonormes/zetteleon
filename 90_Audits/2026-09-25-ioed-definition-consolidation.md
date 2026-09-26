---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-ioed-definition-consolidation
title: 2026-09-25-ioed-definition-consolidation
type: note
---

## Consolidation — [[2026-07-25-ioed-definition-gap-felt-vs-actual-understanding]] — 2026-09-25

> Run of [[Knowledge Consolidation Agent]] (v4). An earlier pass on this note is in [[2026-07-30-ioed-definition]]; this run re-checks it for duplicates and overlaps against today's vault.

### Analysis

Core concept: the Illusion of Explanatory Depth, the gap between how well people think they understand a causal system and how well they can explain it. Epistemic status: claim, `medium`. Tooling tier reached: **MCP lexical** (`obsidian-llmeon` `search_text`, `wikilinks`) plus `rg` for the abstract and functional queries. `search_semantic` errored on two attempts, so "no further duplicates" means none found by keyword. Coverage confidence: medium.

### Search Execution (Triad)

1. Literal: "Illusion of Explanatory Depth" (title, headings, tags) -> the SoT, the older IoED claim note, Knowledge-Related Biases, Illusion of Shared Understanding in Teams, the Sloman and Fernbach Evidence note, Writing in Own Words..., and others.
2. Abstract: metacognition, overconfidence, "illusion of knowing/understanding", "sense of knowing" (`rg`) -> SoT - Metacognitive Calibration, Metacognitive Awareness notes, Illusion of Fluency, the Sloman Evidence note, Evidence - Kahneman... and others.
3. Functional: "understand only until you must explain", "cannot explain", "step-by-step explanation", "recognition versus understanding" (`rg`) -> the SoT, Writing in Own Words..., the input itself, ioed-vs-dunning-kruger.

### Classification

| Note | Class | Evidence | Canonical? |
|---|---|---|---|
| [[SoT - Illusion of Explanatory Depth (IoED)]] | Related, canonical | `type: sot`; its definition callout is the source of this note's Evidence quote; the input already `supports` it | **Yes** (SoT primacy) |
| [[Illusion of Explanatory Depth (IoED)]] | Related, partial overlap | Same headline claim; adds a signals framing and examples; body is pasted chat text; non-conformant | No |
| [[Evidence - Sloman and Fernbach Find the Illusion of Understanding Is Robust Across Topics]] | Related (evidence) | Reports the IoED finding across topics | n/a |
| [[Writing in Own Words Distinguishes Comprehension from the Illusion of Knowledge]] | Related | A test for the same gap from the writing side | n/a |
| [[The Illusion of Shared Understanding in Teams]] | Related (broader, team level) | Same failure mode applied to shared models | n/a |
| [[The Illusion of Fluency is a Cognitive Bias Where Ease of Processing is Mistaken for Deep Learning]], [[Passive Study Habits Foster the Illusion of Fluency]] | Related, distinct construct | Ease of processing versus causal explanation | n/a |
| [[SoT - Metacognitive Calibration]] | Related (already `extends` the SoT) | Wider calibration frame | n/a |

### Actions Applied

| File | Action | One-line diff summary | Status |
|---|---|---|---|
| 2026-07-25-ioed-definition-gap... | link | `evidence_links` set to the Sloman Evidence note; new `## Elsewhere in the Vault` with six annotated links | Done |
| Evidence - Sloman and Fernbach... | link | Second `supports` edge, to the input, plus one sentence saying why | Done |
| Illusion of Explanatory Depth (IoED) | link, conform | Appended `## Consolidation Note` and an `extends` edge to the SoT; frontmatter made conformant (`proposition`, `epistemic_status: low`, `evidence_links`, `contradicts`) | Done |

No merge and no deprecation, for the reasons under Needs your call.

### Conservation Check

No note was deprecated, so nothing was at risk. For the future merge of the older IoED note, its unique claims are recorded here so they cannot be lost:

| Older note | Unique claim | Where it lives now |
|---|---|---|
| Illusion of Explanatory Depth (IoED) | Signals people use beyond recognition: fluency in discussion, exposure to related information, general overconfidence | Only in that note, and named in its new Consolidation Note |
| Illusion of Explanatory Depth (IoED) | Four things a real test would show: explain the mechanism, predict in new situations, identify part interactions, troubleshoot | Only in that note (the SoT covers debugging via familiarity versus comprehension, not the full four) |
| Illusion of Explanatory Depth (IoED) | Worked examples (car, economics, photosynthesis, democracy, bicycle) | Only in that note |

### Edges Written

| File | Edge line | Kind | Target verified? |
|---|---|---|---|
| Evidence - Sloman and Fernbach... | `[supports:: [[2026-07-25-ioed-definition-gap-felt-vs-actual-understanding]], confidence=medium]` | grounding (`supports`) | Yes |
| Illusion of Explanatory Depth (IoED) | `[extends:: [[SoT - Illusion of Explanatory Depth (IoED)]], confidence=medium]` | structural | Yes |

### Needs your call

| Item | Why it was not done |
|---|---|
| **Done in the follow-up below.** Merge [[Illusion of Explanatory Depth (IoED)]] into [[SoT - Illusion of Explanatory Depth (IoED)]] | Overlap is roughly half, below the 80% threshold, and its unique content (table above) is not yet in the SoT. To merge, add its signals list and four-capability test to the SoT's mechanism section, retarget the two links in [[Mind-Reading Fallacy and Projection]], then deprecate it. |
| Deprecate the input into the SoT | The input is a deliberate atom of the SoT, already `supports` it, and five cluster notes point at it. Its Evidence quote is the SoT definition itself. Deprecating would break that chain; I kept it. If you would rather hold the definition only in the SoT, say so. |
| **Done in the follow-up below.** Two cluster notes still carry old-title links | [[2026-07-25-ioed-vs-dunning-kruger-distinction]] and [[2026-07-25-hyperfocus-dopamine-mistaken-for-logical-integrity]] still point to retired titles. Not touched here. |

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings (2911 notes, 1419 edges). Every wikilink in the three edited notes resolves.
- `--why` on the input: it now bottoms out on the Sloman and Fernbach Evidence note, among others. `--audit`: 41 gaps, unchanged.
- Confidence: medium. UNSURE: lexical search only; the "half overlap" figure is my judgement from reading both notes, not a computed measure.

## Follow-up, same day: merge done and cluster links fixed

You approved the merge and the cluster link fix. Result:

| File | Action | Diff summary |
|---|---|---|
| SoT - Illusion of Explanatory Depth (IoED) | merge | New subsection "The Signals We Mistake for Understanding" under section 2, after Familiarity vs. Comprehension |
| Illusion of Explanatory Depth (IoED) | deprecate | Frontmatter: `status: superseded`, `superseded_by: ["[[SoT - Illusion of Explanatory Depth (IoED)]]"]`, `archive` added to tags, `type` and conformance fields kept. Body replaced with the redirect notice; the original text is in git history. The Consolidation Note and `extends` edge from the earlier run went with the old body. |
| Mind-Reading Fallacy and Projection | retarget | Both links to the old note now point to the SoT, keeping the display text |
| 2026-07-25-ioed-definition-gap... | retarget | Its "Elsewhere in the Vault" bullet now points to the SoT and says the older note was merged |
| 2026-07-25-ioed-vs-dunning-kruger-distinction | retarget | Two old-title links (prose and `depends_on` edge) to the definition atom |
| 2026-07-25-hyperfocus-dopamine-mistaken-for-logical-integrity | retarget | Three old-title links (one in the body, one prose, one `extends` edge) to `2026-07-25-externalising-tacit-knowledge-illusion-of-profundity` |

### Conservation Check (final)

| Unique claim in the deprecated note | Where it now lives |
|---|---|
| People judge understanding by signals, not direct assessment | SoT, "The Signals We Mistake for Understanding" (first paragraph) |
| Signals: familiarity, recognition, belief alignment, surface explanation, exposure, fluency, overconfidence | Same section, seven bullets |
| Four-part real test: explain, predict, identify interactions, troubleshoot | Same section, closing paragraph |
| Worked examples: car, financial headlines, photosynthesis terms, democracy terms, bicycle | Same section, inside the bullets |
| Two outgoing links (`Knowledge Aquisition and Zettelkasten.md`, `../notes/2-knowledge_aquisition_and_zettelkasten.md`) | Not carried over: neither target exists in the vault (checked by filename), so no live link was lost |

### Validation

See the closing line of the reply; recorded here as: whole-vault `edge_lint.py` 0 errors, 0 warnings; no broken links in any edited note; gap count unchanged at 41.

## Next action

Skim the new SoT section "The Signals We Mistake for Understanding" and adjust the wording to your own voice if you want it to read less like the original chat text.
