---
aliases:
- Atomic Note Standard
- Proposition Card
- Zettel Standard
- Note Shape Standard
conformant: true
created: 2026-09-26 00:00:00+00:00
modified: 2026-09-26 00:00:00+00:00
non_conformance_reason: ''
see_also:
- '[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]'
- '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
- '[[The Atomicity Principle - One Idea Per Note]]'
tags:
- domain/pkm
- topic/knowledge-architecture
- topic/zettelkasten
- prodos/sot
title: SoT - Atomic Note Standard (The Proposition Card)
type: sot
permalink: llmeon/30-library/so-t/so-t-atomic-note-standard-the-proposition-card
---

> Canonical status: this note is the authoritative spec for the shape of an atomic note in `30_Library/100_zettelkasten/`. [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] governs the frontmatter fields; this note governs the body, the title, the links and how all of it is enforced. Where the two overlap, this note says which one wins.

## Minimum Viable Understanding (MVU)

A zettel here is a **proposition card**: one idea, stated as a complete sentence in your own words, with its scope, its evidence and its implications written under it, and its connections annotated with the reason for each. Claims are titled with the sentence itself. Everything is checked by a script, and the check applies to new notes only.

## 1. What a zettel is, from this vault's own notes

| Principle | Where it comes from |
|---|---|
| One idea per note, in complete sentences, in your own words | [[Main Notes Are the Essential Building Blocks]], [[Elaboration Through Own Words Deepens Understanding]], [[The Atomicity Principle - One Idea Per Note]] |
| The note is a proposition, something that can be wrong, and a claim is titled by the sentence itself | [[Propositions Are the only Thing that Can Be Wrong]], [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]] |
| One canonical note per idea, linked from everywhere else | [[Linking as a Redundancy Reduction Strategy in Zettelkasten]] |
| A link carries its reason: part of, similar or different, complements or competes | [[Key questions when linking notes in the Zettelkasten method]] |
| The right level of atomicity is personal, so measurable limits are prompts for review and not verdicts; a "but" or a "however" is the usual sign of a second idea | [[Atomic Enough Means the Fewest Pieces Necessary to Be Useful for the Task]], [[The Words But and However Signal That What Follows May Deserve Its Own Note]], [[The Notes of Luhmann Were Atomic-ish, Concise but Not Constrained]] |
| Typed edges only where the logic matters | [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] |
| Capture is temporary; the main note is built from processing it | [[Fleeting Notes Are Temporary Capture Mechanisms]], [[Literature Notes Bridge Source Material and Main Notes]] |
| Hubs and maps are entry points, not the thinking | [[Hub Notes Provide Entry Points to Idea Clusters]], [[Structure Notes as Maps of Thought Trails]] |
| The point is the thinking done while making the note, not the size of the graph | [[Zettelkasten System Essence]], [[Deep Processing is the Core of Zettelkasten]] |

## 2. The card (body)

Applies to notes of `type` `claim`, `concept`, `evidence` and `procedure`. Maps (`map`), SoTs and journals keep their own shapes.

```markdown
## <Title, identical to the filename apart from capitalisation>

<Opening statement: one to three sentences, in your own words. The whole idea, readable cold.>

### Scope & Conditions

<When it applies, the boundaries, the assumptions.>

### Evidence

> "<Verbatim quote from the source>"
> (<Author, work, location>)

### Implications

- <One to three consequences that follow from the source.>

### Related

- [[Other Note]]—<relation>: <why the connection exists>

### Tensions

- [[Other Note]]—tension, not contradiction: <the assumption that differs>

### See Also

- [[Other Note]]

### Further Reading

- [<Book, author, location>](calibre://view-book/Library/id/FORMAT)—_<what it corroborates>_
```

Rules:

1. **No H1.** The title is the H2, and the section headings are H3. The Linter enforces this on save.
2. **Section order is fixed:** Scope & Conditions, Evidence, Implications, then any of Steelman, Related, Tensions, See Also, Further Reading in that order. The first three are required. Omit an optional section rather than leave it empty.
3. **The opening statement is at most three sentences.** If you need a fourth, or a "but", it is probably two notes. The validator warns at four sentences and fails at six.
4. **Evidence is verbatim.** A quotation is copied exactly and its source named. If the claim is your own reasoning, say so in Evidence in a plain sentence instead of inventing a quote.
5. **Links are annotated.** Every bullet under Related and Tensions has a dash and a reason. A bare link is allowed only under See Also.
6. **At most seven links** across Related, Tensions and See Also. Prefer fewer, stronger ones.
7. **Typed edges are optional** and go on their own line, in the closed vocabulary. Never `rel::`.

Evidence notes use a different card: the title, the verbatim quote as a blockquote, then `### What It Supports` and `### What It Does Not Show`.

## 3. Frontmatter

The fields per type are in the Contract §3. This note adds the rules that the Contract left implicit.

- **Required on every atomic note:** `title` (matches the filename), `type`, `tags` (not empty), `conformant`, `created`, `modified`.
- **Required by type:** claim needs `proposition`, `epistemic_status`, `evidence_links`, `contradicts`. Concept needs `definition`, `distinguishes_from`, `used_in_claims`. Evidence needs `source_quote`, `source_reference`, `supports_claims`, `confidence`. Procedure needs `trigger`, `steps`, `verification`.
- **Provenance is optional:** `source_title`, `source_url`, `upstream`, `created_utc`.
- **`prodos.*` is dropped** (decided 2026-09-26). The Obsidian Linter deletes the `prodos` key on save and 87% of notes never carried it, so `type` and `status` carry that information. Do not write it.
- **`confidence` belongs to evidence notes only,** as a number from 0 to 1. On any other type it is an error.
- **No legacy keys:** `uid`, `purpose`, `epistemic`, `updated`, `creation_date`, `last_reviewed`.
- **Types are the Contract's enum.** `atom`, `permanent`, blank and `null` are not types. See the Contract §6 for the migration mapping.
- **Keep string values plain.** Frontmatter strings contain no `: `, apostrophes or double quotes. The Linter's YAML escaping breaks on them (see the checks below). Reword instead: "the experience of each person", not "each person's experience".

## 4. Titles

- A **claim** is titled by its own proposition, as a declarative sentence of at least four words, for example `Pro-Social Punishment Restores Cooperation`. A noun phrase such as `The Methods of Science` is a label, not a claim.
- A **concept** is titled by the term or distinction it defines.
- **Evidence** is titled `Evidence - <who> <verb> <what>`.
- A **question** ends with `?`. A **procedure** starts with `How to`.
- Renaming a note means updating every wikilink to it. Titles are the link targets.

## 5. The ratchet: new notes only

Decided 2026-09-26: the standard is enforced on **new notes only**, and legacy notes are frozen.

- **In scope:** notes in `30_Library/100_zettelkasten/` of type claim, concept, evidence or procedure whose `created` date is on or after **2026-09-26**, and which are not `status: superseded`.
- **Out of scope:** everything older. A legacy note is brought up to standard when someone next thinks it deserves the effort, not by a bulk rewrite.
- **Escape hatch:** a note that cannot yet meet the standard may say so with `conformant: false` and a `non_conformance_reason`. Its violations are then reported as warnings, not errors. This is the Contract's existing rule, not a new one.

## 6. Enforcement

| Layer | What it does |
|---|---|
| `10_System/scripts/validate_note_shape.py` | Checks the frontmatter and body rules above. Default run scans in-scope notes; `--path` checks named files; `--staged` is what the hook uses; `--report` counts legacy shapes without failing. |
| `.git/hooks/pre-commit` | Validates each newly added note's frontmatter, lints edges, then runs the shape check on staged in-scope notes. Legacy notes are not blocked. `SKIP_NOTE_SHAPE=1` skips the shape check for one commit. **Dormant today**: see the note below the table. |
| `10_System/templates/Template - Atomic Zettel` (the claim card), `Template - Concept`, `Template - Evidence`, `Template - Procedure` | Start every new note from the right card. |
| The prompts | The Atomic Signal Extractor names claims as sentences. The Atomic Linker emits the card and runs the validator. The Consolidation Agent and Orphan Note Positioning prompts point here. |
| Obsidian Linter | Formats on save. Its config must agree with this note; it no longer deletes `confidence`, which evidence notes need. |

The validator cannot judge whether a note holds one idea or whether a title reads as a sentence beyond a word count. Those stay review items.

> Status of the hook, 2026-09-26: git's `core.hooksPath` is `~/.config/git/hooks`, a chezmoi-managed hook that only runs a secret scan and never calls `.git/hooks/pre-commit`. The vault's hook has therefore not run since that path was set on 2026-08-03, and vault-backup commits are not gated. Until it is chained (either add a call to the repo hook in the chezmoi-managed global hook, or give this repo its own `core.hooksPath` that runs the secret scan and then this hook), enforcement rests on the prompts, the templates, and running `validate_note_shape.py` by hand or from an agent.

## 7. Decisions

- 2026-09-26: the proposition card is the standard body. It is what 514 existing notes already use and what the Linker produces.
- 2026-09-26: `prodos.*` is not part of an atomic note.
- 2026-09-26: claim titles are full sentences, as the Contract already required.
- 2026-09-26: enforcement applies to new notes only.

## Related

- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—governs the frontmatter fields this note builds on.
- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—governs the edge lines.
- [[Knowledge Consolidation Agent]], [[Atomic Linker → Promote & Connect]] and [[Orphan Note Positioning & Thread Audit]]—the prompts that create notes to this shape.