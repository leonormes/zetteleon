---
title: 2026-07-31-key-questions
type: note
permalink: llmeon/90-audits/2026-07-31-key-questions
---

## Positioning — [[Key questions when linking notes in the Zettelkasten method]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`type: claim`, `conformant: false`, `non_conformance_reason`), lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (plain link to `2 Zettelkasten note`).
Overall: Inbound orphan.

### Search Execution
- Target is a reference note containing a list of heuristic questions for linking notes in a Zettelkasten.
- It is an inbound orphan but points outward contextually to `2 Zettelkasten note`.
- I will modernize the frontmatter to the ProdOS concept stub standard.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| N/A | Target is a concept/reference note, plain mentions serve as context. | N/A | N/A | N/A | Pass (No edge mutations needed) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
None.

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain links are preserved.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `type`, `non_conformance_reason` | (present) | (Remove) |
| `prodos.kind` | (missing) | `concept` |
| `prodos.lifecycle` | (missing) | `stub` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Key questions when linking notes in the Zettelkasten method` has been updated to use the standard ProdOS concept stub schema. It serves as a reference concept note and remains an inbound orphan.

### Exposure List
- **Dependents (Outbound load = 0):** No active load.
- **Dependencies (Inbound load = 0):** This node acts as an isolated concept reference.

### Threads
Target functions as a knowledge architecture concept:
- **Thread 1 (Knowledge Architecture Concept):**
  `Key questions when linking notes in the Zettelkasten method` (Concept Stub)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `2 Zettelkasten note.md` -> [Plain Link (Mention)]

### Patch A (Typings)
None required. The note is a concept stub.

### Patch B (Sever Candidates / Mergers)
No severances required. Contextual links preserved.

### Pathologies Found
- **Orphan:** The note was and remains an inbound orphan.
- **Legacy Frontmatter:** The YAML contained defunct schema fields (`non_conformance_reason`, `type`, `conformant: false`), and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`). This was fully modernised.

### Frontier
- Concept could be linked in the future to PKM/Zettelkasten MoCs. Currently a stable stub.

### Next Action
Mark audit as complete and move to the next target.