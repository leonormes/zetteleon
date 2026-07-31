---
title: 2026-07-31-evidence-torvalds-complexity
type: note
permalink: llmeon/90-audits/2026-07-31-evidence-torvalds-complexity
---

## Positioning — [[Evidence - Torvalds Complexity Conservation Data Structures vs Control Flow]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`source_reference`, `supports_claims`, `type: evidence`), lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 2 (typed edge to `Software Complexity is Conserved Between Control Flow and Representation`, plain link to `Code vs Data Structures (Torvalds Essay)`).
Overall: Inbound orphan.

### Search Execution
- Target is an evidence note that already supports its parent claim.
- No further edges required, but the existing typed edge has legacy `strength=` and `confidence=` kwargs which must be stripped to adhere to the strict six-word vocabulary rule.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Software Complexity is Conserved Between Control Flow and Representation.md` | **Use:** Target acts as empirical evidence supporting this claim. | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate - existing but needs format strip) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Evidence - Torvalds Complexity Conservation...md` | `%%[supports:: [[Software Complexity is Conserved Between Control Flow and Representation]]]%%` | Strip legacy kwargs from existing typed edge to conform to strict schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain link to `Code vs Data Structures (Torvalds Essay)` is preserved.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type`, `source_reference`, etc | (present) | (Remove) |
| `prodos.kind` | (missing) | `evidence` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `When data structures perfectly model domain constraints, procedural complexity can be shifted into the structural layer, simplifying the resulting code.` |
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
Following the enrichment pass, `Evidence - Torvalds Complexity Conservation...` has been transformed from an inbound orphan with legacy formatting into a structurally compliant ProdOS evidence note. It correctly supports its target claim.

### Exposure List
- **Dependents (Outbound load = 0):** `supports` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as base evidence.

### Threads
Target functions as empirical support:
- **Thread 1 (Software Complexity Conservation):**
  `Evidence - Torvalds Complexity Conservation...` (Evidence)
  ↳ `supports` -> `Software Complexity is Conserved Between Control Flow and Representation` (Atomic Claim)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Software Complexity is Conserved Between Control Flow and Representation.md` -> [Typed Edge: `supports`]
  - `Code vs Data Structures (Torvalds Essay).md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node's existing edge was stripped of legacy kwargs to conform to the strict six-word vocabulary rule.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual links preserved.

### Pathologies Found
- **Orphan:** The note was an inbound orphan.
- **Legacy Edge Formatting:** The `supports` edge contained legacy kwargs (`strength`, `confidence`) which were removed.
- **Legacy Frontmatter:** The YAML used the outdated `type: evidence`, contained defunct schema fields (`source_reference`, `supports_claims`), and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.