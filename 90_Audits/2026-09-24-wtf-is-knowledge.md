---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-wtf-is-knowledge
title: 2026-09-24-wtf-is-knowledge
type: note
---

## Atomisation — [[21-wtf_is_knowledge_anyway]] — 2026-09-24

> Pipeline: [[Atomic Signal Extractor → Write TMP file]] then [[Atomic Linker → Promote & Connect]], run in one pass. 1MCP tools were unavailable, so duplicate checks were lexical (`rg`) plus file reads.

### What the note was

A ~2,500-word raw AI chat: eight questions from Leon and long, generic AI answers with web citations. Type `concept` ("Bulk inferred type. Needs review."). Roughly 20% signal, 80% noise. Most of the AI's content restates notes the vault already has.

### Atoms promoted (7, all in `30_Library/100_zettelkasten/`)

| # | Atom | Type | Confidence |
|---|---|---|---|
| 1 | [[Information Answers Who, What, When and Where Questions While Knowledge Answers Why and How]] | claim | medium |
| 2 | [[Knowledge Supports Prediction and Inference Where Information Alone Does Not]] | claim | medium |
| 3 | [[AI Output Contains No Insight Until a Human Reads and Interprets It]] | claim | medium (Leon's own claim) |
| 4 | [[Knowledge Acquired by Different Routes Keeps Its Factual Content, Verifiability and Practical Application]] | claim | low |
| 5 | [[Knowledge Acquired by Different Routes Differs in Context, Associative Network, Depth, Personal Meaning and Flexibility]] | claim | low |
| 6 | [[An Effective Knowledge Representation Needs Representational Adequacy, Inferential Adequacy and Efficiency, and Acquisitional Efficiency]] | claim | medium |
| 7 | [[Relationships Between Pieces of Knowledge Can Be Logical, Hierarchical, Associative, Contextual or Temporal]] | concept | medium |

Every evidence quote was checked to be verbatim in the original before writing. Each atom links to 2 to 3 existing notes (no phantom links, no self-links), carries `upstream: [[21-wtf_is_knowledge_anyway]]`, and is `conformant: true` with the full claim or concept fields. Atoms 4 and 5 are a deliberate pair (what stays the same, what differs). Obsidian's Linter reformatted their frontmatter on save; that is expected.

### Deliberately not extracted (already in the vault)

- Information versus knowledge (processing, outcome, the "all knowledge is information" relationship): [[Information vs Knowledge]], [[What is information]].
- Data becoming information through context, structure, analysis and purpose, and "meaning is relationship to context": [[What is information]].
- Why knowledge is harder to transfer: [[Knowledge Transmission Is Reconstruction, Not Copying]].
- The AI's list of classical knowledge-representation techniques (ontologies, semantic networks, rules): it answers a different question from how large language models store knowledge, so only the generic criteria (atom 6) were kept.

### What happened to the source note

| Item | Result |
|---|---|
| Original transcript | Preserved unchanged in `99_Archive/21-wtf_is_knowledge_anyway (raw chat).md` |
| [[21-wtf_is_knowledge_anyway]] | Slimmed to a provenance note: Leon's eight questions verbatim, the atom list, a "covered elsewhere" map, a "not extracted" note and the 32 deduplicated URLs the AI cited. `type: journal`, `conformant: true`. The filename is unchanged, so [[Aristotle Distinguished Between Episteme, Techne, and Phronesis]] and older audits still resolve |
| TMP file | Written to `00_Inbox/tmp_atoms_wtf-is-knowledge.md`, then moved to `.trash/` after promotion, matching earlier runs |

### Hub links added

| File | Change |
|---|---|
| MOC - From Information to Knowledge | 4 bullets (atoms 1, 2, 4, 5) at the end of "The Transformation Process" |
| SoT - Human vs AI Cognition | bullet for atom 3 |
| SoT - Virtual Knowledge Graph Paradigm | bullet for atom 6 |

### Judgement calls to check

1. **Atom 3 is your own claim**, quoted from your line in the chat, with the AI's agreement as a second quote. If you would rather have it as a HEAD note or a stronger claim, that is your call.
2. **Atoms 4 and 5 are low confidence**: the AI hedged ("likely", "may differ") and offered no evidence.
3. **Atom 7 is a `concept` but has a sentence title**, following the vault's existing pattern. It is distinguished from the vault's closed six-word edge vocabulary and not linked to it as an edge.
4. **`source_url` is `UNKNOWN`**: the chat's origin was not recorded. The cited URLs are listed on the source note but were not read here.
5. **The source note's type is `journal`**, the closest canonical fit for a captured session; `question` would have needed a title ending in "?" and the Luhmann-style filename.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2854 notes, 1384 edges). No typed edges were written; the atoms are linked with annotated plain links.
