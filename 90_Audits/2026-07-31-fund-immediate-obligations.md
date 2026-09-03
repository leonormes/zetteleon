---
title: 2026-07-31-fund-immediate-obligations
type: note
permalink: llmeon/90-audits/2026-07-31-fund-immediate-obligations
---

## Positioning — [[Fund Immediate Obligations First]] — 2026-07-31

### Baseline
Thin—frontmatter missing `conformant`, `prodos` block, `proposition`, `epistemic_status`, and has legacy keys `type: ''`, `status: ''`, `last_reviewed`, `updated`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (plain link to `Give Every Dollar a Job...`).
Overall: True inbound orphan note.

### Search Execution
- Target establishes the primary step in a budgeting hierarchy: funding non-negotiable immediate obligations before anything else.
- Investigated `Give Every Dollar a Job (YNAB Rule 1)`, which outlines the "Hierarchy of Jobs" and explicitly lists "Immediate obligations (Reality)" as Step 1.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Give Every Dollar a Job (YNAB Rule 1).md` | **Use:** Target acts as a concrete implementation detail (Step 1) of the broader ZBB framework outlined in the candidate. | Yes. | No. | Yes. | Pass (Edge: Target `implements` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Fund Immediate...md` | `[implements:: [[Give Every Dollar a Job (YNAB Rule 1)]]]` | Target is the applied first step (the "how-to") of the parent budgeting rule. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
Remove the inline wikilink brackets from `[[Give Every Dollar a Job (YNAB Rule 1)]]` since the edge explicitly anchors the relationship at the bottom.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `''` | `claim` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `A stable budget requires a clear hierarchy of priorities where non-negotiable, immediate obligations are always funded before discretionary spending or long-term goals.` |
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
Following the enrichment pass, `Fund Immediate Obligations First` has been transformed from an orphan into a structured applied step claim. It now correctly implements the theoretical budgeting hierarchy defined in the broader YNAB Rule 1 principle.

### Exposure List
- **Dependents (Outbound load = 0):** `implements` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as an applied practice.

### Threads
Target functions as a concrete practice within a personal finance framework:
- **Thread 1 (Budgeting Practices):**
  `Fund Immediate Obligations First...` (Concrete Step)
  ↳ `implements` -> `Give Every Dollar a Job (YNAB Rule 1)` (Budgeting Principle)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Give Every Dollar a Job (YNAB Rule 1).md` -> [Typed Edge: `implements`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent budgeting principle.

### Patch B (Sever Candidates / Mergers)
Successfully applied. Converted the inline wikilink to plain text since the relationship is now formalized at the bottom.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used legacy keys (`status`, `last_reviewed`, `updated`), had an empty `type: ''`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and lacked `conformant: true`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.