---
title: Audit - Animal Allegory is a Persistent Feature of Fables
type: audit
created: 2026-10-14 00:00:00+00:00
tags:
- audit
- orphan-positioning
permalink: llmeon/90-audits/2026-10-14-animal-allegory-is-a-persistent-feature-of-fables
---

## Positioning — [[Animal Allegory is a Persistent Feature of Fables for Social Commentary]] — 2026-10-14

### Baseline
Thin. Zero outbound links; one inbound (from [[Sequence - Evolution of Fable Storytelling]], which names it as the Key Continuity). Frontmatter `conformant: false`, missing `proposition`, `contradicts`, `evidence_links`, `epistemic_status`. Not protected (no `own_words`). Confidence: high.

### Search Execution
- literal: "fable" and "allegor", "satire" (ripgrep over `30_Library`) -> the fable cluster below, [[MOC - Storytelling Techniques]]
- backlinks query -> the Sequence note only
- Semantic vault search not used this run, so coverage is lexical.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[Aesop's Fables Use Anthropomorphic Allegory]] | Use: the earliest instance of the claimed continuity | Persistence claim loses its starting case | No other note covers it | Retracting it weakens the claim | `depends_on` |
| [[La Fontaines Fables Served as Courtly Education in 17th Century France]] | Use: mid-point instance of allegory as critique | Gap in the continuity | Not substitutable | Moves confidence | `depends_on` |
| [[Fables in Modern Media Range from Cartoons to Political Allegory]] | Use: modern instance, Animal Farm | Claim stops at antiquity | Not substitutable | Moves confidence | `depends_on` |
| [[Sequence - Evolution of Fable Storytelling]] | Mention: names this note | Coherent | n/a | None | Plain link |
| [[Aesop's Fables Originated in Oral Tradition]], [[Phaedrus Adapted Aesop's Fables into Latin Verse]], [[The Versailles Labyrinth Used Fable Installations for Visual Storytelling]] | Mention: same timeline, no allegory content | Coherent | Substitutable | None | Not linked |

### Patch A — Typed Edges
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| This note | `[depends_on:: [[Aesop's Fables Use Anthropomorphic Allegory]]]` | Persistence rests on its instances | Yes |
| This note | `[depends_on:: [[La Fontaines Fables Served as Courtly Education in 17th Century France]]]` | Same | Yes |
| This note | `[depends_on:: [[Fables in Modern Media Range from Cartoons to Political Allegory]]]` | Same | Yes |

### Patch B — Plain Links / MoC Anchors
| File | Proposed line | Where it goes |
|---|---|---|
| This note | 5 annotated links under `## Related` | End of note |
| MOC - Storytelling Techniques.md | `- [[Animal Allegory ...]] rel:: demonstrates` | Under `## Social Functions`, matching the neighbouring line |

### Patch C — Frontmatter Conformance
| Field | Current | Proposed |
|---|---|---|
| proposition, epistemic_status, evidence_links, contradicts | missing | one-sentence claim, medium, empty lists (applied) |
| conformant | false | true, `non_conformance_reason` removed |

### Patch D — Further Reading, Personal Library
Not run this run (ARCHILLES not queried). Reported as unchecked, not as a zero-match.

### Applied (Part 2)
| File | Change | Status |
|---|---|---|
| Animal Allegory is a Persistent Feature of Fables for Social Commentary.md | Frontmatter conformance, `## Related` with 3 typed edges and 5 annotated links | Applied |
| MOC - Storytelling Techniques.md | One line under Social Functions | Applied |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| `[[Political Subversion Through Animal Allegory]]` | Linked from the MoC under Social Functions but no such note exists (confirmed by `ls`). Dangling link; this note or [[Fables in Modern Media Range from Cartoons to Political Allegory]] could be its retarget. |

## Thread Audit (Part 3)

**Verdict:** the Target is a node in the argument graph, resting on three instance claims.
- **Exposure:** 0 dependents (`--impact`: none recorded).
- **Thread:** Target -> three fable-history notes. All three are ungrounded (`conformant: false`, no evidence), so they are the weakest links and bottom out the thread.
- **Cheapest defeater:** a counter-example fable tradition without animal allegory (for example a human-cast moral tale form treated as fable), which the instances do not rule out.
- **Pathologies:** none; no cycle.
- **Frontier:** the three instance notes need `proposition`/`evidence_links`, and the claim has no source for the persistence beyond the vault's own case notes.

### Validation
- `edge_lint.py` (whole vault): 5 errors, the same dangling edges in files not touched this run; none involve the Target or the MoC. 0 warnings.
- `validate_note_shape.py` not run: the note predates 2026-09-26.
- Confidence: medium.

## Next action
Run `uv run --with pyyaml python3 10_System/scripts/edge_lint.py --audit` and check whether the three instance notes appear as new gaps.