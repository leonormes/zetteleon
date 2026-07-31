---
title: 2026-07-31-information-organizing-principle
type: note
permalink: llmeon/90-audits/2026-07-31-information-organizing-principle
---

## Positioning — [[Information as an Organizing Principle]] — 2026-07-31

### Baseline
Thin—frontmatter missing `conformant`, `prodos` block, `proposition`, has legacy keys `type: permanent`, `status`, `last_reviewed`, `updated`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (`Information as Foundation of Knowledge` - plain link).
Overall: True inbound orphan note.

### Search Execution
- Target asserts that information is not mere data, but a fundamental organizing force that shapes the material world (analogous to genes).
- Investigated `SoT - The Law of Increasing Functional Information`, which explicitly defines Information as a fundamental physical variable that counters entropy by capturing and preserving order in evolving systems.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - The Law of Increasing Functional Information.md` | **Use:** Target's premise (information as a fundamental physical organizing force) acts as a foundational philosophical claim that underpins and supports the SoT's physical law. | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Information as an Organizing...md` | `%%[supports:: [[SoT - The Law of Increasing Functional Information]]]%%` | Target philosophically aligns with and supports the SoT's physical definition of information as a fundamental structuring force. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain link to `Information as Foundation of Knowledge` will be preserved as a contextual mention.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `permanent` | `claim` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Information functions as a fundamental organizing principle and force that shapes the material world, rather than just abstract data.` |
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
Following the enrichment pass, `Information as an Organizing Principle` has been transformed from an orphan into a structured claim. It now correctly acts as a supporting philosophical premise for the Functional Information framework defined in the SoT.

### Exposure List
- **Dependents (Outbound load = 0):** `supports` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as an observational claim.

### Threads
Target functions as a core justification in the physics of information:
- **Thread 1 (Information Theory / Physics):**
  `Information as an Organizing Principle...` (Philosophical Claim)
  ↳ `supports` -> `SoT - The Law of Increasing Functional Information` (Physical Law)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - The Law of Increasing Functional Information.md` -> [Typed Edge: `supports`]
  - `Information as Foundation of Knowledge.md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual link preserved.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used legacy keys (`status`, `last_reviewed`, `updated`), had an outdated `type: permanent`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and lacked `conformant: true`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.