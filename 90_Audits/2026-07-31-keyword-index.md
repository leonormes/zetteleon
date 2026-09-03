---
title: 2026-07-31-keyword-index
type: note
permalink: llmeon/90-audits/2026-07-31-keyword-index
---

## Positioning — [[Keyword Index Provides Sparse Entry Points]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`type: claim`, `conformant: false`, `non_conformance_reason`), lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). Contains legacy kwargs on the typed edge.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 4 (1 typed edge to `Hub Notes Provide Entry Points to Idea Clusters`, 3 plain links).
Overall: Inbound orphan.

### Search Execution
- Target is an atomic claim about the benefits of sparse indexing in a Zettelkasten.
- It extends another claim `Hub Notes Provide Entry Points to Idea Clusters`.
- I will modernize the frontmatter to the ProdOS claim standard and strip the legacy kwargs from the typed edge.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Hub Notes Provide Entry Points to Idea Clusters` | Target explicitly extends this claim. | N/A | N/A | N/A | Pass (Edge exists but requires Patch A) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Keyword Index Provides Sparse Entry Points.md` | `[extends:: [[Hub Notes Provide Entry Points to Idea Clusters]]]` | Strip legacy kwargs from existing typed edge to conform to strict schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain links are preserved.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `type`, `non_conformance_reason` | (present) | (Remove) |
| `prodos.kind` | (missing) | `claim` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `A sparse keyword index that links to only a few entry points induces productive serendipity by forcing navigation through the network rather than relying on comprehensive retrieval.` |
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
Following the enrichment pass, `Keyword Index Provides Sparse Entry Points` has been transformed from an inbound orphan with legacy formatting into a structurally compliant ProdOS atomic claim. It remains an inbound orphan but correctly extends its parent claim.

### Exposure List
- **Dependents (Outbound load = 0):** `extends` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as an isolated base claim.

### Threads
Target functions as an extension claim:
- **Thread 1 (Zettelkasten Navigation):**
  `Keyword Index Provides Sparse Entry Points` (Atomic Claim)
  ↳ `extends` -> `Hub Notes Provide Entry Points to Idea Clusters`

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Hub Notes Provide Entry Points to Idea Clusters.md` -> [Typed Edge: `extends`] (Also plain link)
  - `Rhizome Structure - Non-Hierarchical Network.md` -> [Plain Link (Mention)]
  - `Concept-Orientation Enables Cross-Domain Discovery.md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node's existing edge was stripped of legacy kwargs to conform to the strict six-word vocabulary rule.

### Patch B (Sever Candidates / Mergers)
No severances required. Contextual links preserved.

### Pathologies Found
- **Orphan:** The note was and remains an inbound orphan.
- **Legacy Edge Formatting:** The `extends` edge contained legacy kwargs (`strength`, `confidence`) which were removed.
- **Legacy Frontmatter:** The YAML used the outdated `type: claim`, contained defunct schema fields (`non_conformance_reason`, `conformant: false`), and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.