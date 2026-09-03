---
title: 2026-07-30-ioed-definition
type: note
permalink: llmeon/90-audits/2026-07-30-ioed-definition
---

## Positioning — [[2026-07-25-ioed-definition-gap-felt-vs-actual-understanding]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, legacy keys like `evidence_links`, `contradicts`, `non_conformance_reason`, missing `prodos.kind` and `prodos.lifecycle`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (Reference to `SoT - Illusion of Explanatory Depth (IoED)`).
Overall: True orphan note (not structurally anchored with typed edges).

### Search Execution
- Target explicitly references `SoT - Illusion of Explanatory Depth (IoED)` as its source framework, defining the core thesis of the illusion itself.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Illusion of Explanatory Depth (IoED).md` | **Use:** Target acts as the base claim/definition of the illusion detailed in the SoT. | Yes—if the illusion didn't exist or wasn't a gap between felt and actual understanding, the entire SoT would be invalid. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `2026-07-25-ioed-definition-gap-felt-vs-actual-understanding.md` | `[supports:: [[SoT - Illusion of Explanatory Depth (IoED)]]]` | Target is the foundational axiom validating the core premise of the IoED SoT. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain links to sibling claims under `## Related` are left intact.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `contradicts` / `evidence_links` / `non_conformance_reason` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | `People systematically overestimate...` | (Keep unchanged, valid) |
| `epistemic_status` | `medium` | `medium` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `2026-07-25-ioed-definition...` has been transformed from an orphan into a structured claim. It now correctly acts as the base definitional claim supporting the entire IoED SoT framework.

### Exposure List
- **Dependents (Outbound load = 1):** 
  1. `SoT - Illusion of Explanatory Depth (IoED)` relies on this node as its foundational definition.
- **Dependencies (Inbound load = 0):** This node is foundational.

### Threads
Target functions as a core justification in the cognition/learning domain:
- **Thread 1 (IoED Core Premises):**
  `2026-07-25-ioed-definition...` (Base Definition)
  ↳ `supports` -> `SoT - Illusion of Explanatory Depth (IoED)` (Framework)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - Illusion of Explanatory Depth (IoED).md` -> [Typed Edge: `supports`]
  - (Plus multiple plain link mentions under `## Related` pointing to child claims in the cluster).

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Sibling links under `## Related` were preserved.

### Pathologies Found
- **Orphan:** The note was a true orphan (neither anchored to an MOC nor an SoT).
- **Legacy Frontmatter:** The YAML contained the `non_conformance_reason`, `evidence_links`, and `contradicts` keys and lacked the mandatory ProdOS block. This was fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.