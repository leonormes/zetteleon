---
conformant: true
created: 2026-09-26 00:00:00+01:00
modified: 2026-09-26 00:00:00+01:00
permalink: llmeon/00-inbox/zettelkasten-audit-2026-09-26
status: seed
tags:
- audit
- pkm
- zettelkasten
- allosso
title: Zettelkasten Audit 2026-09-26
type: link_report
---

> [!summary] One-paragraph verdict
> The folder `30_Library/100_zettelkasten/` (1,584 notes) has a **strong connected core and good link reasoning**, but it is a **collection more than a workshop**. Almost no source layer sits under the claims (25 evidence notes against 1,285 point-like notes), a third of the notes hang loose, tags do not work as a keyword index, and nothing shows the reading → thinking → publishing path being walked. Three clusters are close to having an essay in them, and one of them (philosophy of science) already carries its own objections.

Scope: `30_Library/100_zettelkasten/` only. Rubric: *How to Make Notes and Write*, Dan Allosso and S. F. Allosso (2022), Calibre id 708 (`calibre://view-book/GCcalibreBooks/708/EPUB`). Nothing in the vault or Calibre was changed by the audit. Scripts and sample lists are in the session scratchpad.

---

## 1. How the audit was run

1. **Rubric.** I read the book from its EPUB and reduced it to seven testable rules (section 2).
2. **Whole-folder metrics** by script: links, orphans, components, typed edges, frontmatter population, tags, sources, reviews.
3. **Stratified sample of 30 notes** (10 claim, 5 evidence, 5 concept, 5 legacy or untyped, 5 isolated), read by hand. Every qualitative judgement below is **sampled, n=30**, and is my reading, not a measurement.
4. **Cluster scoring** for output-readiness, using tag-based membership. The membership is approximate, so treat cluster sizes as indicative.

> [!warning] Limits
> - `modified` dates are useless: a mass rewrite touched everything on 2026-09-26. Age is judged from `created`.
> - The source layer (highlights, book annotations) may live in Calibre or ARCHILLES, which are out of scope. A shortfall against the book's funnel means "not in this folder", not "does not exist".
> - Fleeting capture lives in `00_Inbox` and `01_journals`, also out of scope, so the book's first stage is **not assessable** here.

---

## 2. Scorecard against the book

| # | Book rule (chapter) | Evidence in the folder | Rating |
|---|---|---|---|
| 1 | **Process funnel**: highlight, then Source Note, then Point Note; about 1 point per 5-10 source notes (ch. 2, 4) | 25 evidence notes against 1,285 point-like notes, about 51:1. 585 notes carry an in-body quoted Evidence block instead. | Weak |
| 2 | **Ownership**: own words, cite the source (ch. 2, 5) | 420 of 1,285 point-like notes (33%) have a real source field. 264 notes have a real `source_url`, 59 of them AI-chat links, plus 13 titled "New chat". | Weak |
| 3 | **Connection**: link at creation, with a reason (ch. 2, 3, 6) | 3,511 internal links, median 1 in and 1 out. 24% have no inbound link, 28% no outbound, 166 (10.5%) neither. But 68% of notes have at least one annotated link, and 1,064 typed edges sit in 537 notes. | Mixed (reasons strong, coverage patchy) |
| 4 | **Keywords and index**, about one keyword per note (ch. 5) | 1,711 distinct tags, 1,012 (59%) used once. Mean 3.7 tags per note, 74 notes untagged. Structure is flat and bottom-up, which the book approves. | Weak |
| 5 | **Review and contradiction-spotting** (ch. 2) | `last_reviewed` set on 46 notes (3%). 30 typed `contradicts` edges. `revises` used 5 times. | Weak |
| 6 | **Output**: thesis, points with sources beneath, strongest objection (ch. 6, 7) | 82 of 900 claims (9%) record a Tensions, Steelman or Objections section. No drafts or outlines in the folder. Three clusters are candidates (section 5). | Partial |
| 7 | **Collector's fallacy** (ch. 5) | 537 notes created in Oct-Nov 2025 and 330 in Sept 2026. 467 notes are `seed`, only 9 `stable` or `evergreen`. 91 of the 166 isolated notes come from one Oct-Dec 2025 batch. | At risk |

Two things the book values that the vault does well: link **reasons** (3,930 annotated link lines against 1,722 bare) and a **flat, tag-based structure** with no forced folder taxonomy.

---

## 3. Findings, ranked

### High

**F1. The source layer is thin, and much of it is AI-derived.**
- Funnel inverted (about 51 point-like notes per evidence note, where the book expects about one point per 5-10 source notes).
- Sampled notes often cite an AI chat, a YouTube transcript, or `UNKNOWN`. Several "Evidence" blocks quote that captured chat, so the note and its evidence come from the same place.
- Why it matters: the book's central claim is that paraphrasing in your own words *is* the ownership step (ch. 2, 5). A note whose paraphrase was written by a model has skipped it.
- Fix: for notes you intend to write from, add a real Source Note from a book or paper, and record where each note came from.

**F2. A long tail of loosely attached notes.**
- 385 notes have no inbound link, 442 no outbound, 166 neither. Of those 166, 91 date from Oct-Dec 2025.
- The sample shows why: textbook stubs (OSI layers, hypervisor types, authentication methods) and video summaries, often single-source and `seed`. Two of the five sampled isolates do link out to SoT notes, so they attach to the SoT layer rather than to each other.
- The book's own warning (ch. 5): unconnected notes "get lost in the box", and it advises discarding what you do not need.

**F3. The output path is not visible.**
- No draft, outline or thesis notes exist in the folder, and only 9% of claims record an objection.
- The book's test for a topic (ch. 7): a non-obvious, arguable thesis, points with sources beneath, and a stated answer to "who would disagree?". Most claims stop at Scope, Evidence and Implications.

### Medium

**F4. Tags are not converging into an index.** 1,012 single-use tags and 3.7 tags per note (the book expects about one) mean tags name notes rather than group them.

**F5. Some link reasons are templated, so 68% "annotated" overstates.** The label "shared mechanism" alone accounts for 477 of the 1,683 labelled annotations (28%), across 328 notes. A reason repeated as a template records that a link exists, not why.

**F6. Review and revision barely happen.** `last_reviewed` on 3% of notes and 5 `revises` edges. `extends` (241) and `upstream` (345 notes) show that "filing behind" a related note is practised, but changing your mind is not.

**F7. Frontmatter hygiene.** 179 notes (11%) have a blank, null or missing `type`, and there are 29 distinct `type` values with case variants (`Fact`/`Factual`, `question`/`Question`). 1,068 notes have no `status`.

### Low

- **F8.** Near-duplicates are few: three title pairs, for example *Rejection Sensitive Dysphoria (RSD)* and *Rejection-Sensitive Dysphoria*.
- **F9.** Size outliers: 132 notes over 500 words and 105 under 60 (median 188). The book asks for one idea per note, readable out of context.

> [!tip] Live tension worth a decision
> [[The Collector's Fallacy Conflates Gathering with Assimilation]] carries a `contradicts` edge to [[Claim - Over-capture plus deferred review is sustainable]]. The book (ch. 5) sides with the first. The vault currently holds both without choosing.

---

## 4. What the 30-note sample showed (my judgement, n=30)

| Stratum | What I found |
|---|---|
| **Claim (10)** | 3 argue their own point ([[Science Is Trustworthy Because Its Structure Corrects for Bias, Not Because Scientists Are Less Biased]], [[Dismissing People Who Disagree Costs You Your Best Error-Detectors]], *Paraphrasing Demonstrates the Independence of Meaning from Language*). 5 restate a source in card form, with a quoted Evidence block. 2 are bare summaries or assertions with no source. |
| **Evidence (5)** | 3 are exemplary (Ahrens, Kahneman, Tracy). Each states **"What it Does not Show"**, and the Tracy note says plainly that it is a popular assertion, not a study. 2 legacy ones have weak provenance (an AI "investigative report", and a MoC cited as the source). |
| **Concept (5)** | 1 is honestly labelled as coming from an AI answer, 1 adds a real critique (*The Mereological Fallacy in Neuroscience*), 2 restate a source, and 1 is a textbook stub from a bulk batch that links to its "same stub batch" siblings. |
| **Legacy or untyped (5)** | Mixed: a 595-word parable with no frontmatter, a summary, a good short note with inline links, a 52-word fragment with one bare link, and a personal-context note with bare links. |
| **Isolated (5)** | Video and chat summaries and a 41-word claim. Two visibly hang off SoT notes. |

Standout practice worth copying: the **"What it Does not Show"** section on the three good evidence notes. It is exactly the book's "who would disagree?" habit, applied to sources.

---

## 5. Output readiness: three candidate clusters

Scored by tag membership. "Density" is internal links per note in the cluster.

| Cluster | Notes | Links (density) | Isolated inside | Objections recorded | Verdict |
|---|---|---|---|---|---|
| **A. Philosophy of science and trust** | 63 | 142 (2.25) | 3 | 8 Tensions, 8 `contradicts` | **Closest to publishable** |
| **B. Agent engineering** | 114 | 376 (3.30) | 2 | 6 Tensions | Dense, thin on sources |
| **C. PKM craft** | 131 | 201 (1.53) | 22 | 10 Tensions, 3 `contradicts` | Promising, weakest sources |

### A. Science earns trust from its structure, not from less biased scientists
- **Thesis:** what makes science trustworthy is falsifiability, a public paper trail and consilience, not the individual objectivity of scientists.
- **Points:** [[Science Is Trustworthy Because Its Structure Corrects for Bias, Not Because Scientists Are Less Biased]] (856 words, already `synthesizes` its two supports), [[Falsifiability Distinguishes Science from Dogma]] (21 inbound links, the highest in the folder), [[The Public Paper Trail of Science Makes Its Self-Correction Verifiable Without Firsthand Observation]], [[Consilience Signals Genuine Scientific Consensus]].
- **Objections already in the vault:** [[Duhem-Quine Holism Complicates Simple Falsification]], [[Godfrey-Smith's Confirmation Objection to Strict Falsificationism]] (has a Tensions section), [[Feyerabend's Epistemological Anarchism Denies Any Fixed Scientific Method]].
- **Gap:** three of the four supporting points come from an AI chat or `UNKNOWN` sources, and nothing yet answers Duhem-Quine.

### B. When code is cheap, human value moves to verification, but review gates fail
- **Thesis:** as agents make code production cheap, human value shifts from writing to verifying and overseeing architecture, yet mandatory human review erodes through approval fatigue.
- **Points:** [[Shift to Verification]], [[Shift to Architectural Oversight]], [[Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers]], [[Resting the Case for Human Value in Software on Being a Quality Gate Is a Losing Argument]].
- **Objection:** [[Mandatory Manual Code Review Before Deployment]] against [[Approval Fatigue Undermines the Safety Value of Human-in-the-Loop Review]]. This is a real internal tension, but no `contradicts` edge links them, and neither note has a source field.
- **Gap:** one evidence note in the whole cluster.

### C. Emergent structure only works if you resist the collector's fallacy
- **Thesis:** bottom-up structure and flat association work only when links carry reasons and gathering is not mistaken for assimilation.
- **Points:** [[Bottom-Up Organization Allows Emergent Structure]], [[Claim - Flat associative structure beats rigid hierarchy]], [[The Collector's Fallacy Conflates Gathering with Assimilation]].
- **Objections:** [[Clusters of Ideas in a Zettelkasten Are Suggestions Not Mandates]] (a real book source, Calibre 1491), [[Network Graph Views Can Induce Apophenia Through Software-Drawn Connections]], and the over-capture claim above.
- **Gap:** 22 isolated notes inside the cluster and the thinnest sourcing. It is also the cluster where your own experience is the best evidence.

**Clusters that fail the test:**
- *ADHD task initiation* (23 notes, 0.52 links per note, 13 of 23 isolated inside the cluster): plenty of content, not connected.
- *Kubernetes control loops* (24 notes): coherent, but drawn largely from one AI essay, with no recorded objections.

---

## 6. The five highest-payoff actions

1. **Decide the collector's-fallacy question, then triage.** Choose between the fallacy note and the over-capture claim. Then work the 91 isolated notes from the Oct-Dec 2025 batch: link, merge or delete.
2. **Build a real source layer for cluster A.** Write 5-10 paraphrased Source Notes from books (Deutsch, Godfrey-Smith, Kuhn are already in Calibre) and cite them. Record where AI-derived notes came from so they can be told apart.
3. **Write one piece from cluster A** using the book's ch. 7 test. Capture new notes as you draft, as the book recommends.
4. **Add the missing objections and edges.** Add Tensions to the claims in cluster A and B, plus `contradicts` edges (start with Mandatory Manual Code Review against Approval Fatigue).
5. **Converge the tags.** Retire single-use tags into about one keyword per note, and start setting `last_reviewed` and using `revises` when you change your mind. Hygiene item: fix the 179 notes with blank `type`.

---

## 7. Appendix A: headline numbers

| Measure | Value |
|---|---|
| Notes | 1,584 (900 claim, 192 concept, 120 atom, 53 permanent, 25 evidence-type, others) |
| Titles as full sentences | 1,045 (66%); 414 short-label titles |
| Internal links / links to outside the folder | 3,511 / 1,911 |
| Median in-degree / out-degree | 1 / 1 (max 21 / 30) |
| No inbound / no outbound / isolated | 385 (24%) / 442 (28%) / 166 (10.5%) |
| Also no inbound link from anywhere in the live vault | 41 of the 166 |
| Connected components | 201; the giant one holds 1,298 notes (82%) |
| Reciprocated links | 1,202 of 3,511 (34%) |
| Typed edges | 1,064 in 537 notes: supports 377, depends_on 244, extends 241, implements 109, synthesizes 58, contradicts 30, revises 5 |
| Annotated link lines / bare | 3,930 / 1,722 |
| Templated label "shared mechanism" | 477 of 1,683 labelled annotations, in 328 notes |
| Tags | 1,711 distinct, 1,012 used once, mean 3.66 per note |
| `last_reviewed` set | 46 |
| Status | seed 467, draft 28, superseded 9, stable 7, stale 3, evergreen 2, none 1,068 |
| Created by month (peaks) | Oct 2025 263, Nov 2025 274, Sept 2026 330 |

---

## 8. Appendix B: what changed in the prompt and why

| Original prompt | Problem | Change |
|---|---|---|
| Names "How to Make Notes and Write" as a vault file | It is a book in Calibre (id 708) | Point to Calibre, and embed the rubric so an agent without Calibre can still run it |
| Fleeting, reference, permanent note typology | That is Ahrens' vocabulary. The book uses highlight, Source Note, Point Note and says the label matters less than the process. | Use the book's terms |
| Alphanumeric IDs must branch | The book advocates them but says "1, 2, 1a" is enough. The point is filing behind a related note. | Judge the function (`extends`, `upstream`, `revises`), not the form |
| "Idea generator" and surprising combinations | The book calls oracle-style emergence "probably exaggerated" | Test where output material concentrates (hot nodes) |
| No scope | The review wandered into 4,000 non-PKM notes | Folder only, other areas as entry-point evidence only |
| No method or evidence rule | An unconstrained model writes a confident narrative | Script the metrics, sample n=30, label judgements |
| Missing checks | The funnel ratio, citations, keyword index, review cadence, thesis test | Added as rules 1-7 |

Additions learned from the real run (not in the earlier draft): count links from a note to SoT or MoC notes as attachment, not isolation; check whether link annotations are templated before crediting them; check whether an "Evidence" quote comes from the cited source or from an AI chat about it; and read the type enum from the frontmatter contract before judging `type`.

### Revised prompt

```markdown
You are auditing a personal Zettelkasten as a code review: read-only, evidence-based, ranked by severity.

## Scope
- Review ONLY `/Volumes/DAL/Zettelkasten/LLMeon/30_Library/100_zettelkasten/`. Ignore `.fuse_hidden*` and `.DS_Store`.
- Out of scope: journals, inbox, work, audits, archive, `30_Library/SoT`. Exceptions: count inbound links from
  `30_Library/MoC/` and `30_Library/400_indexes/` as entry-point evidence, and count a note's links to SoT or MoC
  notes as attachment (report isolation both with and without them).
- Do not modify any file.

## Rubric: "How to Make Notes and Write" (Allosso and Allosso, 2022; Calibre id 708)
Use the book's own terms, not Ahrens' or Luhmann's.
1. Process (ch. 2, 4): highlight <=10% of a text, then Source Note (paraphrase, rarely quote, cite, one keyword), then
   Point Note (own analysis). Funnel: ~100 highlights, ~10 Source Notes, 1-2 Point Notes. Note-type labels matter less
   than the process; source and point notes may sit side by side.
2. Ownership (ch. 2, 5): notes are in the author's own words; paraphrase is the proof of understanding.
3. Connection (ch. 2, 3, 6): every new note is linked to an existing one at creation. Ask of each link: relevant to
   the question? similar or different? agree or disagree? other connections?
4. Keywords and index (ch. 5): about one keyword per note, from the author's interests, feeding an index. IDs and
   "filing behind" a related note let ideas converse over time; judge the FUNCTION, not whether 1a/1a1 is copied.
5. Review (ch. 2): notes are reviewed regularly; old and new notes are compared to surface contradictions.
6. Output (ch. 6, 7): topics emerge from concentrations of notes. Test a cluster: a non-obvious, arguable thesis;
   points, each with source notes beneath; the strongest objection. Output should feed new notes back in.
7. Warning (ch. 5): the collector's fallacy. Gathering is not assimilating.
Exclude ch. 8-11 and the Revision Checklist (they govern drafts). If you cannot access the book, use this rubric and say so.

## Vault conventions (do not penalise)
- Titles act as IDs; typed edges (`supports`, `extends`, `revises`, `contradicts`...) live in note bodies.
- Fleeting capture lives in `00_Inbox` and `01_journals`: report "not assessable", not a failure.
- Standard: `SoT - Atomic Note Standard (The Proposition Card)`; notes from before 2026-09-26 are frozen legacy.
  Treat legacy and current notes as separate cohorts. Read the `type` enum from the frontmatter contract.

## Method
1. Compute whole-folder metrics with a script: counts, link graph, orphans, components, typed edges, frontmatter
   population, tags per note, source-field population. Treat `modified` as unreliable; use `created`.
2. Read a stratified sample of 30 (10 claim, 5 evidence, 5 concept, 5 legacy or untyped, 5 isolated). Label every
   qualitative judgement "sampled, n=30".
3. Separate scaffolding from substance: an empty key or heading is not practice.
4. Flag notes of AI-chat origin (`source_title`, `source_url`). Judge rule 2, and whether an "Evidence" quote comes
   from the cited source or from an AI chat about it.
5. Before crediting link reasons, check whether annotations are templated (repeated label phrases).
6. Say where the source layer might live outside the folder (Calibre, ARCHILLES) before reporting a funnel shortfall.

## Output
- Scorecard: one line per rule 1-7 with metric, rating, chapter reference.
- Findings: severity, evidence (count plus 2-3 example titles), one concrete fix each.
- Output-readiness: 3 candidate clusters, each with thesis, points, source notes and objection, or a stated failure.
- Not assessable / assumptions.
- Verdict: at most 200 words, direct but constructive, ending with the 5 highest-payoff actions.
```