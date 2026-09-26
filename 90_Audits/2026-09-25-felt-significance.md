---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-felt-significance
title: 2026-09-25-felt-significance
type: note
---

## Enrichment — [[Felt significance of thoughts can mislead about their substance]] — 2026-09-25

> Per [[00 - Prompt Library Router]] this is a connected-but-thin claim (310 words, complete claim fields, two `supports` edges, one inbound link), so the single-note refresh applies ([[Note Refresh & Link Auditor]]). Lexical search only (1MCP tools were unavailable).

### Baseline

- **Broken links: none** (resolver: 0 unresolved before and after).
- An `axiom: true`, `epistemic_status: high` claim with **no evidence** and **no outbound prose links**: it lists four causes and four manifestations in plain text, and the notes that hold each of them were not linked. It is the "core insight" of [[MOC - Why Thoughts Feel More Important When Thinking Them]], whose links use the unparsed `rel::` grammar, so the graph had none of that structure.

### Changes

| Area | Change |
|---|---|
| Frontmatter | `evidence_links` → two new Evidence notes. `axiom` and `epistemic_status` left as they are |
| **Where the Causes Live in the Vault** | each of the four causes mapped to its notes (12 links), and three manifestation notes |
| **What to Do About It** | writing, own-words test, Question Master, metacognitive calibration, holding views loosely (9 links) |
| **Tensions** | personal meaning (from the hub map); [[Transition Times Are Valuable Windows for Creative Insight]]; deferring the judgement of substance (Luhmann) |
| **Related, ProdOS, Further Reading** | Stage 2 and 3, the writing-to-think SoT, TAC, HEAD contract, the two link prompts; three books |

### New Evidence (quotes verified verbatim)

| Note | Source | Scope caveat |
|---|---|---|
| [[Evidence - Kahneman Says Confidence Tracks the Quality of the Story Not the Amount of Evidence]] | *Thinking, Fast and Slow* (Calibre 53) | About confidence, not felt importance; supports the general point that metacognitive feelings do not track validity |
| [[Evidence - Sloman and Fernbach Find the Illusion of Understanding Is Robust Across Topics]] | *The Knowledge Illusion* (Calibre 707) | About felt understanding, not felt significance; related by analogy |

### Typed edges: tried, then reverted

I first added `[supports:: [[Felt significance of thoughts can mislead about their substance]]]` on three premise notes ([[Thoughts are bundled with phenomenological qualities]], [[The brain is biased toward its own thoughts in the moment]], [[The Disappointment of Written Thoughts]]). The audit's foundation-gap count rose from 38 to 41, because those notes have no grounds of their own and each became an ungrounded supporter. **I reverted all three.** The connections stay as annotated plain links in the note (the causes and manifestations sections). No new inbound typed edges were kept. If you want them typed later, ground those three notes first.

After the revert the gap count is back to 38.

### Judgement calls

- **Left `axiom: true`.** It is a chosen premise; the Evidence notes corroborate it and say where they stop.
- **The evidence is by analogy.** Both books measure felt confidence or felt understanding, not felt significance. I recorded that on each Evidence note instead of overstating it.
- **Luhmann tension (from *A System for Writing*, Calibre 1491)** is written as prose and reading only; I did not quote it as evidence.

### Left alone

The hub map's `rel::` lines (unparsed grammar). Converting them to typed edges would be a separate pass on that map.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2902 notes, 1409 edges). Resolver: 0 unresolved links in the note and the Evidence notes.
