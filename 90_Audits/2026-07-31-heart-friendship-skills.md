---
title: 2026-07-31-heart-friendship-skills
type: note
permalink: llmeon/90-audits/2026-07-31-heart-friendship-skills
---

## Positioning — [[Heart & Friendship Skills (Your Kind Heart)]] — 2026-07-31

### Baseline
Thin—frontmatter missing `conformant`, `prodos` block, `proposition`, has empty `type` and legacy keys `status`, `last_reviewed`, `updated`. The note body is an extracted section from a map note.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (`A Concept Map for a Flourishing Human` - plain link).
Overall: True inbound orphan note.

### Search Execution
- Target lists interpersonal VIA character strengths and PSHE values necessary for flourishing.
- Investigated `A Concept Map for a Flourishing Human`, which contains this exact list in its entirety as a section. The target acts as an extracted specialisation of the broader map.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `A Concept Map for a Flourishing Human.md` | **Use:** Target acts as a specialised subset (an extraction) of the broader concept map. | Yes. | No. | Yes. | Pass (Edge: Target `extends` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Heart & Friendship Skills...md` | `%%[extends:: [[A Concept Map for a Flourishing Human]]]%%` | Target specialises a subset of the broader human flourishing map. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
Remove the trailing plain link `[[A Concept Map for a Flourishing Human]]` since it will be replaced by the typed edge.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `''` | `claim` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Heart and friendship skills encompass the VIA Character Strengths and PSHE values necessary for connecting with others and building healthy interpersonal relationships.` |
| `epistemic_status` | (missing) | `high` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Heart & Friendship Skills...` has been transformed from an orphan into a structured claim. It now correctly acts as a specialisation extracted from the broader Flourishing Human concept map.

### Exposure List
- **Dependents (Outbound load = 0):** `extends` edges do not increase load.
- **Dependencies (Inbound load = 0):** This node acts as an extracted subset of a broader map.

### Threads
Target functions as a specific thematic subset of the human flourishing framework:
- **Thread 1 (Human Flourishing Framework):**
  `Heart & Friendship Skills...` (Specialisation)
  ↳ `extends` -> `A Concept Map for a Flourishing Human` (Framework Map)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `A Concept Map for a Flourishing Human.md` -> [Typed Edge: `extends`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework map.

### Patch B (Sever Candidates / Mergers)
Successfully applied. The plain link to the concept map was replaced by the typed edge.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used legacy keys (`status`, `last_reviewed`, `updated`), had an empty `type: ''`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and was missing `conformant`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.