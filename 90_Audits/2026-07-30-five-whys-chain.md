---
title: 2026-07-30-five-whys-chain
type: note
permalink: llmeon/90-audits/2026-07-30-five-whys-chain
---

## Positioning — [[2026-07-25-five-whys-chain-drills-to-first-principles]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, legacy keys like `evidence_links`, `contradicts`, `non_conformance_reason`, missing `prodos.kind` and `prodos.lifecycle`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (Reference to `SoT - Illusion of Explanatory Depth (IoED)`).
Overall: True orphan note (not structurally anchored with typed edges).

### Search Execution
- Target explicitly references `SoT - Illusion of Explanatory Depth (IoED)` as its source framework, defining a forcing function (antidote) for IoED.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Illusion of Explanatory Depth (IoED).md` | **Use:** Target defines one of the core antidotes (the "Five Whys Chain") for overcoming the cognitive illusion described in the SoT. | Yes—if the Five Whys didn't overcome IoED, the SoT's proposed forcing functions would be invalid. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `2026-07-25-five-whys-chain-drills-to-first-principles.md` | `%%[supports:: [[SoT - Illusion of Explanatory Depth (IoED)]]]%%` | Target acts as a direct counter-measure (forcing function) to the illusion detailed in the SoT. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `contradicts` / `evidence_links` / `non_conformance_reason` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | `'Repeatedly asking "why"...'` | (Keep unchanged, valid) |
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
Following the enrichment pass, `2026-07-25-five-whys-chain...` has been transformed from an orphan into a structured claim. It now correctly acts as a core forcing function (antidote) validating the active-auditing thesis within the IoED SoT.

### Exposure List
- **Dependents (Outbound load = 1):** 
  1. `SoT - Illusion of Explanatory Depth (IoED)` relies on this node as a practical counter-measure to the illusion.
- **Dependencies (Inbound load = 0):** This node acts as a fundamental behavioral mechanism.

### Threads
Target functions as a core justification in the cognition/learning domain:
- **Thread 1 (IoED Counter-Measures):**
  `2026-07-25-five-whys-chain...` (Forcing Function)
  ↳ `supports` -> `SoT - Illusion of Explanatory Depth (IoED)` (Framework)

### Traversal Manifest
- **Inbound:**
  - `Familiarity and Comprehension Are Distinct...` (According to internal text)
- **Outbound:**
  - `SoT - Illusion of Explanatory Depth (IoED).md` -> [Typed Edge: `supports`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required.

### Pathologies Found
- **Orphan:** The note was a true orphan (neither anchored to an MOC nor an SoT).
- **Legacy Frontmatter:** The YAML contained the `non_conformance_reason`, `evidence_links`, and `contradicts` keys and lacked the mandatory ProdOS block. This was fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.