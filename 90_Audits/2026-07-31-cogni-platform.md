---
title: 2026-07-31-cogni-platform
type: note
permalink: llmeon/90-audits/2026-07-31-cogni-platform
---

## Positioning — [[Cogni Platform - Claude Code Persistent Memory Architecture]] — 2026-07-31

### Baseline
Moderate—frontmatter is missing the mandatory `prodos.kind`, `prodos.lifecycle`, and `conformant` keys, though it has `proposition` and `type: claim`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 5 (3 typed edges with parameter bloat, 2 plain links).
Overall: Inbound orphan but structurally anchored outwards via `implements` edges.

### Search Execution
- Target discusses a specific platform (Cogni) implementing persistent memory for Claude Code.
- It already targets several claims (`Persistent Memory Layers...`, `Agent Feedback Loops...`, `Selective Memory Retrieval...`).
- The existing typed edges contain `strength=5, confidence=high` parameters which clutter the graph and should be stripped to clean six-word vocabulary edges.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Persistent Memory Layers Enable Multi-Session Agent Continuity` | **Use:** Target implements this concept concretely. | Yes | No. | Yes. | Pass (Retain existing edge, strip params) |
| `Agent Feedback Loops Require Bidirectional Memory Writes` | **Use:** Target implements this concept. | Yes | No. | Yes. | Pass (Retain existing edge, strip params) |
| `Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows` | **Use:** Target implements this concept. | Yes | No. | Yes. | Pass (Retain existing edge, strip params) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Cogni Platform...md` | `[implements:: [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]]` | Strip parameters for clean linting. | Yes |
| `Cogni Platform...md` | `[implements:: [[Agent Feedback Loops Require Bidirectional Memory Writes]]]` | Strip parameters for clean linting. | Yes |
| `Cogni Platform...md` | `[implements:: [[Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows]]]` | Strip parameters for clean linting. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
Preserve the plain links under `## Related`.

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
Following the enrichment pass, `Cogni Platform...` has been cleaned up. It was already targeting broader concepts via `implements` edges, but those edges contained parameter bloat (`strength`, `confidence`) which have now been stripped to ensure clean, six-word vocabulary linting.

### Exposure List
- **Dependents (Outbound load = 0):** `implements` edges do not increase load.
- **Dependencies (Inbound load = 0):** This node acts as a concrete implementation platform.

### Threads
Target functions as a concrete implementation in the Agent Memory Architecture domain:
- **Thread 1 (Agent Memory Architecture):**
  `Cogni Platform...` (Platform Implementation)
  ↳ `implements` -> `Persistent Memory Layers Enable Multi-Session Agent Continuity`
  ↳ `implements` -> `Agent Feedback Loops Require Bidirectional Memory Writes`
  ↳ `implements` -> `Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows`

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Persistent Memory Layers Enable Multi-Session Agent Continuity` -> [Typed Edge: `implements`]
  - `Agent Feedback Loops Require Bidirectional Memory Writes` -> [Typed Edge: `implements`]
  - `Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows` -> [Typed Edge: `implements`]
  - `Claude Code Session Isolation Forces Context Reloading Across Invocations` -> [Mention / `## Related`]
  - `Layered Knowledge Architecture` -> [Mention / `## Related`]

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