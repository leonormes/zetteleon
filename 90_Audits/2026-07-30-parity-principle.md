---
title: 2026-07-30-parity-principle
type: note
permalink: llmeon/90-audits/2026-07-30-parity-principle
---

## Positioning — [[The Parity Principle - Functional Equivalence in Cognition]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block and `proposition`). Contains a malformed outbound link (`[[SoT - The Extended Mind Thesis|EMT]]`).
Existing link count in: 1 (`SoT - The Extended Mind`).
Existing link count out: 1 (broken/malformed).

### Search Execution
- `Parity Principle` -> [Found correctly placed in `SoT - The Extended Mind` as the core philosophical criteria for functional equivalence].
- Investigated `SoT - The Extended Mind Thesis` -> [Confirmed the file is actually named `SoT - The Extended Mind`].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - The Extended Mind.md` | **Use:** Target defines the "Parity Principle," which the SoT explicitly relies on in Section 2 (Active Externalism) to philosophically justify the entire thesis. | Yes—if the parity principle is false, the Extended Mind Thesis loses its core logical mechanism. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `The Parity Principle...md` | `[supports:: [[SoT - The Extended Mind]]]` | Target acts as the logical proof point and philosophical definition for the broader framework. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `The Parity Principle...md` | `The Parity Principle is the philosophical heart of the [[SoT - The Extended Mind\|EMT]].` | Line 13 (Fixing the malformed link). |
| `The Parity Principle...md` | `- [[Natural-Born Cyborgs - Human Plasticity and Tool Merger]]` | New `## Related` section (sibling concept under the EMT). |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `If an external process functions in a way that we would unhesitatingly accept as cognitive were it occurring inside the head, then we should treat that external process as part of the cognitive system.` |
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
Following the enrichment pass, `The Parity Principle...` has been transformed from an isolated node with a broken outbound link into a structurally sound definitional claim. It now correctly underpins Active Externalism, the core argument of the Extended Mind framework.

### Exposure List
- **Dependents (Outbound load = 1):** `SoT - The Extended Mind` relies on this node as the logical and philosophical proof point for its entire framework (Section 2: Active Externalism).
- **Dependencies (Inbound load = 0):** This node acts as a fundamental definition.

### Threads
Target functions as the core mechanical definition for the broader framework:
- **Thread 1 (Philosophical Mechanism):**
  `The Parity Principle...` (Logical Proof Point)
  ↳ `supports` -> `SoT - The Extended Mind` (Framework)

### Traversal Manifest
- **Inbound:**
  - `SoT - The Extended Mind.md` -> [Mention] Annotated in the SoT's Active Externalism section.
- **Outbound:**
  - `SoT - The Extended Mind.md` -> [Typed Edge: `supports`] & [Mention] Inline definition.
  - `Natural-Born Cyborgs - Human Plasticity and Tool Merger.md` -> [Mention] Annotated sibling link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects the foundational philosophical logic of parity to the overarching extended mind framework.

### Patch B (Sever Candidates / Mergers)
The broken inline link (`[[SoT - The Extended Mind Thesis|EMT]]`) was corrected. A related sibling concept (`Natural-Born Cyborgs`) was surfaced in a new `## Related` section.

### Pathologies Found
- **Malformed Link:** The sole outbound link was broken due to an incorrect filename reference (`Thesis` was added erroneously).
- **Legacy Frontmatter:** The YAML contained the `non_conformance_reason` key and lacked the mandatory ProdOS block and `proposition`. This was fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.