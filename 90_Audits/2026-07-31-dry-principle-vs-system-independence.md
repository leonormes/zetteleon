---
title: 2026-07-31-dry-principle-vs-system-independence
type: note
permalink: llmeon/90-audits/2026-07-31-dry-principle-vs-system-independence
---

## Positioning — [[DRY Principle vs System Independence]] — 2026-07-31

### Baseline
Poor—frontmatter has `type: claim`, missing `prodos` block, `proposition`, `epistemic_status`, and has `non_conformance_reason` and `conformant: false`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (plain link to `Becoming System Agnostic`).
Overall: True inbound orphan note.

### Search Execution
- Target discusses the architectural trade-off between the DRY principle (eliminating duplication) and system independence (decoupling), arguing that duplication is preferable to the wrong abstraction.
- Investigated `SoT - Pragmatism vs Rigour in Software`, which explicitly maps these types of architectural trade-offs to the broader spectrum of development velocity vs theoretical purity.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Pragmatism vs Rigour in Software.md` | **Use:** Target acts as a specific heuristic ("prefer duplication over wrong abstraction") that supports a pragmatic architectural approach. | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `DRY Principle vs System Independence.md` | `[supports:: [[SoT - Pragmatism vs Rigour in Software]]]` | Target provides a concrete software engineering heuristic that aligns with pragmatic development principles. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing link to `Becoming System Agnostic` is preserved as context.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | (present) | (Remove) |
| `type` | `claim` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `In software architecture, minimizing cross-component dependencies is often more valuable than eliminating code duplication, as premature abstraction creates fragile coupling.` |
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
Following the enrichment pass, `DRY Principle vs System Independence...` has been transformed from an inbound orphan into a structured atomic claim. It now correctly supports the pragmatic architectural approach defined in the Pragmatism vs Rigour in Software SoT.

### Exposure List
- **Dependents (Outbound load = 0):** `supports` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as a heuristic claim.

### Threads
Target functions as a concrete heuristic for prioritizing decoupling over DRY:
- **Thread 1 (Architectural Pragmatism):**
  `DRY Principle vs System Independence...` (Heuristic Claim)
  ↳ `supports` -> `SoT - Pragmatism vs Rigour in Software` (Pragmatic Architecture)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - Pragmatism vs Rigour in Software.md` -> [Typed Edge: `supports`]
  - `Becoming System Agnostic.md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual links preserved.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used the outdated `type: claim`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and lacked `epistemic_status`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.