---
title: 2026-07-31-gleaning-validation
type: note
permalink: llmeon/90-audits/2026-07-31-gleaning-validation
---

## Positioning — [[Gleaning - Secondary Validation to Catch Silent Omissions]] — 2026-07-31

### Baseline
Moderate—frontmatter is missing `prodos.kind`, `prodos.lifecycle`, and `conformant: true`, but has `proposition` and `epistemic_status`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 6 (2 typed edges with invalid parameter bloat, 4 plain links).
Overall: Inbound orphan but structurally anchored outwards via `supports` edges.

### Search Execution
- Target defines a specific LLM verification technique (Gleaning) that catches silent omissions via a secondary prompt.
- It already targets `LLM Pipeline Accuracy Degrades with Document Length and Task Complexity` and `Model Self-Verification as a Secondary Quality Gate`.
- The existing typed edges contain `strength` and `confidence` parameters which clutter the graph and should be stripped to ensure clean six-word vocabulary linting.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `LLM Pipeline Accuracy Degrades...` | **Use:** Target acts as a mitigation technique for this constraint. | Yes. | No. | Yes. | Pass (Retain existing edge, strip params) |
| `Model Self-Verification...` | **Use:** Target provides a specific operator-level implementation of self-verification. | Yes. | No. | Yes. | Pass (Retain existing edge, strip params) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Gleaning - Secondary...md` | `%%[supports:: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]]%%` | Strip parameters for clean linting. | Yes |
| `Gleaning - Secondary...md` | `%%[supports:: [[Model Self-Verification as a Secondary Quality Gate]]]%%` | Strip parameters for clean linting. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
Preserve the plain links under `## Related` and `## See Also`.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Gleaning...` has been cleaned up. It was already targeting broader concepts via `supports` edges, but those edges contained parameter bloat (`strength`, `confidence`) which have now been stripped to ensure clean, six-word vocabulary linting. It now correctly supports constraints around LLM pipeline accuracy and self-verification strategies.

### Exposure List
- **Dependents (Outbound load = 2):** 
  1. `LLM Pipeline Accuracy Degrades...` relies on this node as a concrete mitigation technique.
  2. `Model Self-Verification...` relies on this node as a specific operator-level implementation.
- **Dependencies (Inbound load = 0):** This node acts as an underlying technique.

### Threads
Target functions as a concrete implementation in the Agent/LLM Reliability domain:
- **Thread 1 (LLM Agent Reliability):**
  `Gleaning...` (Mitigation Technique)
  ↳ `supports` -> `LLM Pipeline Accuracy Degrades with Document Length and Task Complexity`
  ↳ `supports` -> `Model Self-Verification as a Secondary Quality Gate`

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `LLM Pipeline Accuracy Degrades with Document Length and Task Complexity.md` -> [Typed Edge: `supports`]
  - `Model Self-Verification as a Secondary Quality Gate.md` -> [Typed Edge: `supports`]
  - `Error Handling and Retry Pipelines for LLM Failures.md` -> [Mention / `## Related`]
  - `DocETL Framework - Declarative Pipelines with Agentic Optimization.md` -> [Mention / `## Related`]
  - `Precision-Recall Trade-offs in LLM Extraction.md` -> [Mention / `## See Also`]

### Patch A (Typings)
Successfully applied. Invalid edge parameters stripped.

### Patch B (Sever Candidates / Mergers)
No severances required. Unresolved related plain links preserved.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`) and `conformant`. The typed edges in the body had parameter bloat (`strength`, `confidence`). This was all fully modernised and cleaned.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.