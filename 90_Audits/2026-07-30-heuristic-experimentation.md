---
title: 2026-07-30-heuristic-experimentation
type: note
permalink: llmeon/90-audits/2026-07-30-heuristic-experimentation
---

## Positioning — [[Heuristic Experimentation Drives Mathematical Insight]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block and `proposition`, uses legacy `status` and `last_reviewed` keys).
Existing link count in: 1 (from `MOC - What is Maths`).
Existing link count out: 0 (True outbound orphan).

### Search Execution
- `Tinkering` / `Mathematical Thinking` -> [Found `SoT - Mathematical Thinking and Problem Solving` and `SoT - Mathematical Thinking Habits`].
- `Mathematical Discovery` -> [Found sibling claim `The Process of Mathematical Discovery is Driven by Pattern Recognition`].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Mathematical Thinking and Problem Solving.md` | **Use:** Target acts as the detailed exploration of the "Deconstruction & Tinkering" and "Embracing Failure" cognitive strategies outlined in the SoT. | Yes—if experimentation didn't drive insight, the SoT's core claim about the necessity of tinkering would fall apart. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Heuristic Experimentation Drives Mathematical Insight.md` | `%%[supports:: [[SoT - Mathematical Thinking and Problem Solving]]]%%` | Target acts as a structural proof point and deep-dive for the specific cognitive strategies advocated by the SoT. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Heuristic Experimentation Drives Mathematical Insight.md` | `- [[MOC - What is Maths]]` | New `## Related` section. |
| `Heuristic Experimentation Drives Mathematical Insight.md` | `- [[The Process of Mathematical Discovery is Driven by Pattern Recognition]] — _A complementary facet of the discovery process._` | New `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Mathematical discovery is driven by heuristic experimentation—tinkering with examples, embracing failure, and testing conjectures to build intuition before seeking formal proof.` |
| `epistemic_status` | (missing) | `high` |
| `status`, `updated`, `last_reviewed` | (present) | (Remove legacy keys) |
| `type` | `strategy` | `claim` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Heuristic Experimentation...` has been transformed from an outbound orphan with legacy YAML into a structurally sound support node. It now properly underpins the cognitive strategies outlined in the mathematics SoT.

### Exposure List
- **Dependents (Outbound load = 1):** `SoT - Mathematical Thinking and Problem Solving` relies on this node as the detailed, actionable implementation of its "Tinkering" and "Embracing Failure" strategies.
- **Dependencies (Inbound load = 0):** This node acts as a base-level methodology, receiving no structural support from other claims.

### Threads
Target functions as the actionable mechanism for the mathematical mindset framework:
- **Thread 1 (Mathematical Tinkering):**
  `Heuristic Experimentation Drives Mathematical Insight` (Actionable Mechanism)
  ↳ `supports` -> `SoT - Mathematical Thinking and Problem Solving` (Framework)

### Traversal Manifest
- **Inbound:**
  - `MOC - What is Maths.md` -> [Mention / Hub Link]
- **Outbound:**
  - `SoT - Mathematical Thinking and Problem Solving.md` -> [Typed Edge: `supports`]
  - `MOC - What is Maths.md` -> [Mention] Annotated hub link in `## Related`.
  - `The Process of Mathematical Discovery is Driven by Pattern Recognition.md` -> [Mention] Annotated sibling link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects the methodology of tinkering to the overarching problem-solving framework.

### Patch B (Sever Candidates / Mergers)
No severances required. The hub connection and the complementary pattern-recognition process were surfaced in a new `## Related` section. Note: The inbound MoC contains a legacy `rel::` annotation, but that is outside the scope of mutating the target file.

### Pathologies Found
- **Orphan (Outbound):** The note had zero outbound links in the body. This has been resolved.
- **Legacy Frontmatter:** The YAML contained deprecated keys (`status`, `last_reviewed`, `updated`) and lacked the mandatory ProdOS block. This was purged and modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.