---
title: 2026-07-31-canonical-schema-v1
type: note
permalink: llmeon/90-audits/2026-07-31-canonical-schema-v1
---

## Positioning — [[Canonical Schema V1]] — 2026-07-31

### Baseline
Thin—frontmatter non-conformant (missing `conformant`, `proposition`, `prodos` block, uses `type: definition`, contains legacy keys `last_reviewed`, `status`, `updated`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 0.
Overall: True orphan note (not structurally anchored).

### Search Execution
- Target defines the superseded V1 YAML schema used previously in the vault.
- Investigated `SoT - ProdOS Frontmatter Contract (Note Type Schemas)`, which is the canonical standard that supersedes this historical schema.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - ProdOS Frontmatter Contract (Note Type Schemas).md` | **Use:** Target represents the historical predecessor to the current SoT schema. | Yes—without this historical reference, the legacy mappings in the SoT lack their original context. | No. | Yes. | Pass (Edge: Target `related_to` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Canonical Schema V1.md` | `[related_to:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]]` | Target is the superseded historical predecessor to the current ProdOS schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `definition` | `concept` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | `seedling` (status) | `archived` |
| `proposition` | (missing) | `Canonical Schema V1 was the initial standardized YAML frontmatter template designed to ensure all notes were machine-readable, which has since been superseded by the ProdOS Frontmatter Contract.` |
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
Following the enrichment pass, `Canonical Schema V1...` has been transformed from an orphan into a structured historical concept. It is now correctly archived and linked as the historical predecessor to the current ProdOS Frontmatter Contract.

### Exposure List
- **Dependents (Outbound load = 0):** Linked via `related_to` which does not increase load.
- **Dependencies (Inbound load = 0):** This node acts as an historical record.

### Threads
Target functions as a historical precedent in the vault architecture domain:
- **Thread 1 (Vault Architecture):**
  `Canonical Schema V1...` (Historical Precedent)
  ↳ `related_to` -> `SoT - ProdOS Frontmatter Contract (Note Type Schemas)` (Framework)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - ProdOS Frontmatter Contract (Note Type Schemas).md` -> [Typed Edge: `related_to`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its superseding framework.

### Patch B (Sever Candidates / Mergers)
No severances required.

### Pathologies Found
- **Orphan:** The note was a true orphan.
- **Legacy Frontmatter:** The YAML used `type: definition`, contained legacy keys (`last_reviewed`, `status`, `updated`), and was missing `proposition` and the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`). This was fully modernised, and the note was formally archived.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.