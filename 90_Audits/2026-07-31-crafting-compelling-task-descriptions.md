---
title: 2026-07-31-crafting-compelling-task-descriptions
type: note
permalink: llmeon/90-audits/2026-07-31-crafting-compelling-task-descriptions
---

## Positioning — [[Crafting Compelling Task Descriptions and Sustaining Motivation]] — 2026-07-31

### Baseline
Poor—frontmatter is legacy, missing `prodos` block, `proposition`, `epistemic_status`, and has empty fields `status: ''`, `type: ''`, `last_reviewed: ''`, `updated: null`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 0 (True outbound orphan).
Overall: True totally disconnected orphan note.

### Search Execution
- Target provides tactical advice on writing task descriptions (action verbs, specific binary steps) and anchoring them to a motivational "Why".
- Investigated `SoT - PRODOS Core Specification`, which defines the Minimal Viable Action (MVA) and the Dopamine Engine (PINCH model) as core execution mechanisms.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - PRODOS Core Specification.md` | **Use:** Target acts as a concrete implementation guide for defining MVAs (Section 3.2) and anchoring motivation (Section 2). | Yes. | No. | Yes. | Pass (Edge: Target `implements` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Crafting Compelling Task Descriptions...md` | `%%[implements:: [[SoT - PRODOS Core Specification]]]%%` | Target is an applied technique for defining tasks in alignment with PRODOS execution requirements. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. Note had zero outgoing links initially.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `status`, `type`, etc | (present, empty) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Effective task execution requires defining the physical next action with specificity while simultaneously anchoring it to a motivational 'Why'.` |
| `epistemic_status` | (missing) | `high` |
| `tags` | `[]` | `[task-management, motivation, execution, prodos]` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Crafting Compelling Task Descriptions...` has been transformed from an orphan into a structured applied method claim. It now correctly implements the Minimal Viable Action (MVA) definition and motivation mechanics outlined in the PRODOS Core Specification.

### Exposure List
- **Dependents (Outbound load = 0):** `implements` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as an applied technique.

### Threads
Target functions as a concrete practice for defining executable tasks:
- **Thread 1 (Task Definition & Motivation):**
  `Crafting Compelling Task Descriptions...` (Applied Technique)
  ↳ `implements` -> `SoT - PRODOS Core Specification` (Execution Engine & MVA definition)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - PRODOS Core Specification.md` -> [Typed Edge: `implements`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Note had zero outgoing links initially.

### Pathologies Found
- **Orphan:** The note was a true inbound and outbound orphan.
- **Legacy Frontmatter:** The YAML was entirely legacy, containing empty `status`, `type`, `last_reviewed`, and `updated` fields, and lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and lacked `epistemic_status`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.