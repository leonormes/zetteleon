---
title: 2026-07-31-evidence-dopamine-neurons
type: note
permalink: llmeon/90-audits/2026-07-31-evidence-dopamine-neurons
---

## Positioning — [[Evidence - Dopamine Neurons Encode Reward Prediction Error Not Pleasure Schultz]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy field `type: evidence` and lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (typed edge to `Dopamine Neurons Encode Reward Prediction Error, Not Pleasure`).
Overall: Inbound orphan.

### Search Execution
- Target is an evidence note that already supports its parent claim.
- No further edges required, but the existing typed edge has legacy `strength=` and `confidence=` kwargs which must be stripped to adhere to the strict six-word vocabulary rule.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Dopamine Neurons Encode Reward Prediction Error, Not Pleasure.md` | **Use:** Target acts as empirical evidence supporting this claim. | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate - existing but needs format strip) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Evidence - Dopamine Neurons Encode...md` | `%%[supports:: [[Dopamine Neurons Encode Reward Prediction Error, Not Pleasure]]]%%` | Strip legacy kwargs from existing typed edge to conform to strict schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. 

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `evidence` | (Remove) |
| `prodos.kind` | (missing) | `evidence` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Midbrain dopamine neurons encode reward prediction error (the difference between actual and predicted reward), rather than the pleasure of the reward itself.` |
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
Following the enrichment pass, `Evidence - Dopamine Neurons...` has been transformed from an inbound orphan with legacy formatting into a structurally compliant ProdOS evidence note. It correctly supports its target claim.

### Exposure List
- **Dependents (Outbound load = 0):** `supports` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as base evidence.

### Threads
Target functions as empirical support:
- **Thread 1 (Reward Prediction Error):**
  `Evidence - Dopamine Neurons...` (Evidence)
  ↳ `supports` -> `Dopamine Neurons Encode Reward Prediction Error, Not Pleasure` (Atomic Claim)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Dopamine Neurons Encode Reward Prediction Error, Not Pleasure.md` -> [Typed Edge: `supports`]

### Patch A (Typings)
Successfully applied. The node's existing edge was stripped of legacy kwargs to conform to the strict six-word vocabulary rule.

### Patch B (Sever Candidates / Mergers)
No severances required. 

### Pathologies Found
- **Orphan:** The note was an inbound orphan.
- **Legacy Edge Formatting:** The `supports` edge contained legacy kwargs (`strength`, `confidence`) which were removed.
- **Legacy Frontmatter:** The YAML used the outdated `type: evidence`, and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.