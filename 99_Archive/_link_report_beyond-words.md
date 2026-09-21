---
created: 2026-09-21T08:56:03+00:00
created_utc: '2026-09-21T08:56:03+00:00'
modified: 2026-09-21T09:17:36+00:00
permalink: llmeon/00-inbox/link-report-beyond-words
source_atoms: '[[tmp_atoms_beyond-words]]'
status: tmp
title: _link_report_beyond-words
type: link_report
---

## Link Report: beyond Words

### Summary

- Atoms extracted (Step 1): 17
- Atoms processed: 17
- Notes created: 16
- Total links made: 85
- Personal library citations added: 0 (lens 6 not run; see Deviations)
- Unlinked atoms (no connections found): 0
- Not promoted: 1 (Atom 013, duplicate of an existing note)

### Link Map

| Atom | Links | Strongest Connection |
|------|-------|---------------------|
| [[Shared biological architecture enables communication]] | 6 | [[Cross-Cultural Communication Effectiveness]]—extends |
| [[The Symbol Grounding Problem]] | 7 | [[The Chinese Room Argument Contests Whether Symbol Manipulation Alone Constitutes Genuine Understanding]]—shared mechanism |
| [[Language Discretises Continuous Experience]] | 6 | [[Communication is inherently lossy like image compression]]—extends |
| [[Words Are Pointers, Not Containers of Meaning]] | 5 | [[SoT - Communication & Misunderstanding (The Experiential Filter)]]—shared mechanism |
| [[Redundancy Across Channels Corrects Communication Errors]] | 4 | [[Communication requires iterative approximation]]—shared mechanism |
| [[Communicating Depends on Modelling What the Listener Already Knows]] | 4 | [[SoT - Communication & Misunderstanding (The Experiential Filter)]]—shared mechanism |
| [[Gesture Stabilises Ideas That Are Still Forming]] | 6 | [[Pre-Linguistic Thought]]—shared mechanism |
| [[Bodily Feelings Act as Pre-Verbal Cognition]] | 5 | [[Thoughts are bundled with phenomenological qualities]]—shared mechanism |
| [[Image Schemas Ground Abstract Concepts in Bodily Experience]] | 5 | [[Mental representations take multiple forms]]—extends |
| [[Knowledge Transmission Is Reconstruction, Not Copying]] | 6 | [[SoT - Communication & Misunderstanding (The Experiential Filter)]]—extends |
| [[Empathy Is Cognitive Work]] | 4 | [[SoT - Communication & Misunderstanding (The Experiential Filter)]]—extends |
| [[Note Links Connect Representations of Ideas, Not the Ideas Themselves]] | 7 | [[Creating Meaningful Links]]—extends |
| [[Vague Notes Make Links Between Them Tenuous]] | 5 | [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—shared mechanism |
| [[Reviewing Notes and Their Links Forces Re-engagement With the Ideas]] | 3 | [[Note Status Lifecycle]]—shared mechanism |
| [[A PKM Is Personal Because Notes Only Represent Ideas Held in One Head]] | 6 | [[PKM Generates Unique Insights via Personal Context That AI Cannot Replicate]]—shared mechanism |
| [[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]] | 6 | [[Zettelkasten System Essence]]—extends |

### Orphan Atoms (No Links Found)

- None.

### Not Promoted

- Atom 013, "Notes trigger understanding that is processed and integrated in the mind": near-identical to [[Zettelkasten System Essence]], which already states that the Zettelkasten "exists in the mental processes of the individual using it" and that "the notes are a side-effect of understanding, not a substitute for it". Linked to from Atoms 012, 015, 016 and 017 instead of duplicated. It remains recorded in [[tmp_atoms_beyond-words]].

### Overlaps Worth Reviewing

- [[Knowledge Transmission Is Reconstruction, Not Copying]] partly restates a line in [[SoT - Communication & Misunderstanding (The Experiential Filter)]] ("Language transmits Instructions for Reconstruction"). Kept as a separate atom because it makes the knowledge-transfer claim citable on its own.
- [[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]] overlaps the automation point in [[Zettelkasten System Essence]]. Kept because it is scoped to digital tools and carries a distinct tension with [[SoT - The Extended Mind]].
- [[Shared biological architecture enables communication]] is the exact title that [[MOC - The Gap Between Thought and Language]] already links to, so that MOC's dangling link will resolve once this note is filed.

### Deviations From The Prompt

- Vault index: built with targeted title, heading and body searches plus direct reads of every cited note, not by reading all ~2,770 notes. Every link target was then checked against the full filename list for existence and for duplicate names.
- Lens 6 (personal library) was not run. The ARCHILLES MCP disconnected mid-run, and the CLI fallback fails with a LanceDB error ("invalid path … rag_db/Icon"), which appears to be a stray macOS Icon file in the index directory. The suggested fix (`--reset-db`) deletes the whole index and was not attempted.
- Frontmatter follows the current contract, not the prompt's template: top-level `status: seed` is omitted in favour of `prodos.lifecycle: seedling`, and each note carries the claim or concept schema fields (`proposition`, `epistemic_status`, `evidence_links`, `contradicts`, or `definition`, `distinguishes_from`, `used_in_claims`) so that `conformant: true` is valid.
- Extra step: the "Implications" in 13 of the 17 atoms in the first draft of the tmp file were the extractor's own inference; they were rewritten to cite the source before promotion.
- The source note [[beyond words]] was not edited (Step 2 forbids editing existing notes). It has two duplicate `## Related` headings and links to three notes, which is left for you to tidy.
