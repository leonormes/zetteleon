---
aliases:
- Atomic Note Standard
- Note Shape Standard
- Proposition Card
- Zettel Standard
conformant: true
created: 2026-09-26T00:00:00+00:00
modified: 2026-11-17T21:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/so-t-atomic-note-standard-the-proposition-card
project_category: prodos
see_also:
- '[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]'
- '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
- '[[The Atomicity Principle - One Idea Per Note]]'
status: evergreen
tags:
- domain/pkm
- prodos/sot
- topic/knowledge-architecture
- topic/zettelkasten
title: SoT - Atomic Note Standard (The Proposition Card)
type: sot
---

> Canonical status: this note is the authoritative spec for the shape of an atomic note in `30_Library/100_zettelkasten/`. [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] governs the frontmatter fields; this note governs the body, the title, the links and how all of it is enforced. Where the two overlap, this note says which one wins.

## Minimum Viable Understanding (MVU)

A zettel here is a proposition card: one idea, stated as a complete sentence in your own words, with its scope, its evidence and its implications written under it, and its connections annotated with the reason for each. Claims are titled with the sentence itself. Everything is checked by a script, and the check applies to new notes only.

## 1. What a Zettel Is, from This Vault's Own Notes

| Principle | Where it comes from |
|---|---|
| One idea per note, in complete sentences, in your own words | [[Main Notes Are the Essential Building Blocks]], [[Elaboration Through Own Words Deepens Understanding]], [[The Atomicity Principle - One Idea Per Note]] |
| The note is a proposition, something that can be wrong, and a claim is titled by the sentence itself | [[Propositions Are the Only Thing That Can Be Wrong]], [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]] |
| One canonical note per idea, linked from everywhere else | [[Linking as a Redundancy Reduction Strategy in Zettelkasten]] |
| A link carries its reason: part of, similar or different, complements or competes | [[Key questions when linking notes in the Zettelkasten method]] |
| The right level of atomicity is personal, so measurable limits are prompts for review and not verdicts; a "but" or a "however" is the usual sign of a second idea | [[Atomic Enough Means the Fewest Pieces Necessary to Be Useful for the Task]], [[The Words But and However Signal That What Follows May Deserve Its Own Note]], [[The Notes of Luhmann Were Atomic-ish, Concise but Not Constrained]] |
| Typed edges only where the logic matters | [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] |
| Capture is temporary; the main note is built from processing it | [[Fleeting Notes Are Temporary Capture Mechanisms]], [[Literature Notes Bridge Source Material and Main Notes]] |
| Hubs and maps are entry points, not the thinking | [[Hub Notes Provide Entry Points to Idea Clusters]], [[Structure Notes as Maps of Thought Trails]] |
| The point is the thinking done while making the note, not the size of the graph | [[Zettelkasten System Essence]], [[Deep Processing is the Core of Zettelkasten]] |

## 2. The Card (Body)

Applies to notes of `type` `claim`, `concept`, `evidence` and `procedure`. Maps (`map`), SoTs and journals keep their own shapes.

```markdown
## <Title, identical to the filename apart from capitalisation>

<Opening statement: one to three sentences, in your own words. The whole idea, readable cold.>

### Scope & Conditions

<When it applies, the boundaries, the assumptions.>

### Evidence

> "<Verbatim quote from the source>"
> <citation line, as printed by verify_quote.py: (Author Year, ch. N, PDF p. M) · [open in Calibre](link)>

### Implications

- <One to three consequences that follow from the source.>

### Falsifier

- <What observation or test would prove the claim wrong.>

### Related

- [[Other Note]]—<relation>: <why the connection exists>

### Tensions

- [[Other Note]]—tension, not contradiction: <the assumption that differs>

### See Also

- [[Other Note]]

### Further Reading

- <Full reference: Author. Year. *Title*. Publisher. [Open in Calibre](calibre://view-book/GCcalibreBooks/<id>/EPUB)>—_<what it corroborates or challenges>_
```

Rules:

1. No H1. The title is the H2, and the section headings are H3. The Linter enforces this on save.
2. Section order is fixed: Scope & Conditions, Evidence, Implications, then any of Falsifier, Steelman, Related, Tensions, See Also, Further Reading in that order. The first three are required on `status: evergreen` (Tier 2) notes, and optional on `status: seed` (Tier 1) claims. Omit an optional section rather than leave it empty.
3. The opening statement is at most three sentences. If you need a fourth, or a "but", it is probably two notes. The validator warns at four sentences and fails at six.
4. Evidence is verbatim. A quotation is copied exactly and its source named. If the claim is your own reasoning, say so in Evidence in a plain sentence instead of inventing a quote. A quotation from a book in the Calibre library is checked with `verify_quote.py` before it is written and cited as in §9.
5. Links are annotated. Every bullet under Related and Tensions has a dash and a reason. A bare link is allowed only under See Also.
6. At most seven links across Related, Tensions and See Also. Prefer fewer, stronger ones.
7. Typed edges are optional and go on their own line, in the closed vocabulary. Never `rel::`.

8. The embed unit is the opening statement. An SoT transcludes a card with `![[Title#^claim]]`, so the SoT carries the proposition only, not the Evidence, Related or Tensions sections. To make a card embeddable, end its opening statement with a space and `^claim` on the same line (a concept card's definition ends with `^def` instead, embedded as `![[Title#^def]]`). Add the marker to any card an SoT embeds; it is optional on the rest. A heading embed (`![[Title#Title]]`) is not a substitute, because Obsidian includes every H3 beneath the heading.

Evidence notes use a different card: the title, the verbatim quote as a blockquote, then `### What It Supports` and `### What It Does Not Show`.

## 3. Frontmatter

The fields per type are in the Contract §3. This note adds the rules that the Contract left implicit.

- Required on every atomic note: `title` (matches the filename), `type`, `tags` (not empty), `conformant`, `created`, `modified`.
- Required by type: `evergreen` (Tier 2) claims need `proposition`, `epistemic_status`, `evidence_links`, `contradicts`; `seed` (Tier 1) claims need only `epistemic_status`. Concept needs `definition`, `distinguishes_from`, `used_in_claims`. Evidence needs `source_quote`, `source_reference`, `supports_claims`, `confidence`. Procedure needs `trigger`, `steps`, `verification`.
- Provenance is optional: `source_title`, `source_url`, `upstream`, `created_utc`.
- `prodos.*` is dropped (decided 2026-09-26). The Obsidian Linter deletes the `prodos` key on save and 87% of notes never carried it, so `type` and `status` carry that information. Do not write it.
- `confidence` belongs to evidence notes only, as a number from 0 to 1. On any other type it is an error.
- No legacy keys: `uid`, `purpose`, `epistemic`, `updated`, `creation_date`, `last_reviewed`.
- Types are the Contract's enum. `atom`, `permanent`, blank and `null` are not types. See the Contract §6 for the migration mapping.
- Keep string values plain. Frontmatter strings contain no `: `, apostrophes or double quotes. The Linter's YAML escaping breaks on them (see the checks below). Reword instead: "the experience of each person", not "each person's experience".

## 4. Titles

- A claim is titled by its own proposition, as a declarative sentence of at least four words, for example `Pro-Social Punishment Restores Cooperation`. A noun phrase such as `The Methods of Science` is a label, not a claim.
- A concept is titled by the term or distinction it defines.
- Evidence is titled `Evidence - <who> <verb> <what>`.
- A question ends with `?`. A procedure starts with `How to`.
- Renaming a note means updating every wikilink to it. Titles are the link targets.

## 5. The Ratchet: New Notes only

Decided 2026-09-26: the standard is enforced on new notes only, and legacy notes are frozen.

- In scope: notes in `30_Library/100_zettelkasten/` of type claim, concept, evidence or procedure whose `created` date is on or after 2026-09-26, and which are not `status: superseded`.
- Out of scope: everything older. A legacy note is brought up to standard when someone next thinks it deserves the effort, not by a bulk rewrite.
- Escape hatch: a note that cannot yet meet the standard may say so with `conformant: false` and a `non_conformance_reason`. Its violations are then reported as warnings, not errors. This is the Contract's existing rule, not a new one.

## 6. Enforcement

| Layer | What it does |
|---|---|
| `10_System/scripts/validate_note_shape.py` | Checks the frontmatter and body rules above (gating Tier 2 card sections on `evergreen`). Default run scans in-scope notes; `--path` checks named files; `--staged` is what the hook uses; `--report` counts legacy shapes without failing. |
| `10_System/scripts/edge_lint.py` | Checks typed edges, unresolved `![[...]]` transclusions, missing `^claim`/`^def` block IDs, and SoTs embedding notes without `synthesizes`/`depends_on` edges. |
| `10_System/scripts/verify_quote.py` | Checks that a quotation appears verbatim in a Calibre book and prints the chapter, PDF page, a paste-ready citation line and a full reference. Run it on every quotation taken from a book (see §9). Exit code 1 means a quote was not found. |
| `.git/hooks/pre-commit` | Validates each newly added note's frontmatter, lints edges, then runs the shape check on staged in-scope notes. Legacy notes are not blocked. `SKIP_NOTE_SHAPE=1` skips the shape check for one commit. Dormant today: see the note below the table. |
| `10_System/templates/Template - Atomic Zettel` (the claim card), `Template - Concept`, `Template - Evidence`, `Template - Procedure`, `Template - SoT` | Start every new note from the right card or compiled SoT skeleton. |
| The prompts | The Atomic Signal Extractor names claims as sentences. The Atomic Linker emits the card and runs the validator. The Consolidation Agent and Orphan Note Positioning prompts point here. |
| Obsidian Linter | Formats on save. Its config must agree with this note; it no longer deletes `confidence`, which evidence notes need. |

The validator cannot judge whether a note holds one idea or whether a title reads as a sentence beyond a word count. Those stay review items.

> Status of the hook, 2026-09-26: git's `core.hooksPath` is `~/.config/git/hooks`, a chezmoi-managed hook that only runs a secret scan and never calls `.git/hooks/pre-commit`. The vault's hook has therefore not run since that path was set on 2026-08-03, and vault-backup commits are not gated. Until it is chained (either add a call to the repo hook in the chezmoi-managed global hook, or give this repo its own `core.hooksPath` that runs the secret scan and then this hook), enforcement rests on the prompts, the templates, and running `validate_note_shape.py` by hand or from an agent.

## 7. Decisions

- 2026-09-26: the proposition card is the standard body. It is what 514 existing notes already use and what the Linker produces.
- 2026-09-26: `prodos.*` is not part of an atomic note.
- 2026-09-26: claim titles are full sentences, as the Contract already required.
- 2026-09-26: enforcement applies to new notes only.
- 2026-11-17: Tier 1 (`status: seed` or `draft`) claims stay lightweight; full Proposition Card fields and sections are gated on Tier 2 (`status: stable` or `evergreen`), and `Falsifier` is an optional section (§2, §3).
- 2026-11-25: `draft` and `stable` retired from `status`. Tier 1 is now `seed` only and Tier 2 is `evergreen` only. Tiers are unchanged: `draft` was already Tier 1 and `stable` already Tier 2, so the migration moves no note between tiers. Note that old `stable` notes became `evergreen` without a fresh review.
- 2026-11-17: SoTs are compiled threads that transclude cards. The embed unit is the opening statement, marked `^claim` on claims and `^def` on concepts (rule 8).
- 2026-11-17: legacy SoTs convert on next substantive edit, and rule-bearing specification SoTs stay prose (§8). Proposed by the agent, pending Leon's confirmation.
- 2026-11-17: a quotation from a Calibre book is verified with `verify_quote.py` and cited author-year with chapter and PDF page, plus a Calibre chapter link (§9). Confirmed on the desktop viewer by Leon.

## 8. SoTs That Embed Cards

An SoT is a compiled thread, not a card, so it keeps its own shape (see `AGENTS.md` §0 and `Template - SoT`).

- Every card an SoT embeds is also indexed in the SoT's Working Knowledge section by a `synthesizes` or `depends_on` edge. `edge_lint.py` warns when an embedded note has no such edge, and when a `#^id` embed points at a block id that is missing.
- Legacy SoTs follow the ratchet. Do not bulk-convert them. Convert one when it is next substantively edited, through the [[Knowledge Consolidation Agent]]: extract each assertion to a card, add `^claim`, then embed.
- Rule-bearing specification SoTs stay as prose. These are the Frontmatter Contract, Typed Edge Vocabulary, Knowledge Compiler, this note, the HEAD Note Contract, the TAC and PRODOS Core Specification. They define rules rather than argue a thesis from claims.
- Legacy cards a converted SoT needs get `^claim` added to their opening statement. That one-line edit is the only change made to them. A card with no clear single opening statement is split first.

## 9. Citing a Book

Applies to any quotation taken from a book in the Calibre library, wherever it appears (Evidence, Steelman, Source notes).

1. **Verify first.** Run `uv run --with pymupdf python3 10_System/scripts/verify_quote.py --id <calibre id> --quote "<text>"`. Write the quotation only if the verdict is `verbatim`, `normalised` or `elided`. On `not_found` fix the quotation, never the check. Never copy a quotation from search-result text, an AI chat or memory without this check.
2. **Cite like a paper.** The line under the quotation is the script's `paste:` line, author-year in plain text, then the chapter and the physical PDF page, then a Calibre link:
   `> (Simler and Hanson 2018, ch. 5, PDF p. 88) · [open in Calibre](calibre://view-book/GCcalibreBooks/1594/EPUB?open_at=toc:5%20Self-Deception)`
   Add `summarising <Name>` inside the brackets when the author is reporting someone else's work. The citation text stands on its own where the link does not work.
3. **Pages.** PDF pages are physical, because these PDFs carry no printed page numbers, so the label says `PDF p.`. An EPUB-only book gets the chapter and no page.
4. **The link.** `open_at=toc:<chapter title>` opens the chapter in the desktop Calibre viewer (confirmed on macOS 2026-11-17). It does not work on a phone. A PDF-only book links to the book without `open_at`.
5. **Further Reading** holds one full reference per book, from the script's `reference:` line: `Author. Year. *Title*. Publisher. [Open in Calibre](calibre://view-book/GCcalibreBooks/<id>/EPUB)`, then a dash and an italic annotation saying whether it corroborates or challenges.
6. **On a phone.** Highlight the passage in BookFusion and let the plugin sync it into `BookFusion/Books/`. Cite the synced highlight note, `[[BookFusion/Books/<book>/<highlight id>|BookFusion highlight]]`, whose `View highlight` link opens at the highlight on desktop and phone (Android opens the BookFusion web reader). Copy the text into the card, still verify it with step 1, and never edit or rename the synced files: the plugin rewrites them.
7. **Say what you don't know.** If the only source for a passage is an AI chat or a secondary summary, say so in a plain sentence in Evidence.

## Related

- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—governs the frontmatter fields this note builds on.
- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—governs the edge lines.
- [[Knowledge Consolidation Agent]], [[Atomic Linker → Promote & Connect]] and [[Orphan Note Positioning & Thread Audit]]—the prompts that create notes to this shape.
