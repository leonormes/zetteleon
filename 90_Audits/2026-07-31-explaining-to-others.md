---
title: 2026-07-31-explaining-to-others
type: note
permalink: llmeon/90-audits/2026-07-31-explaining-to-others
---

## Positioning — [[Explaining to Others Enhances One's Own Learning]] — 2026-07-31

### Baseline
Moderate—frontmatter missing `prodos` block, `proposition`, `epistemic_status`, and has `non_conformance_reason` and `conformant: false`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 6 (plain links in Related section).
Overall: True inbound orphan note.

### Search Execution
- Target defines the "Protégé Effect" (teaching enhances learning) and lists a number of related concepts including IoED and Active Learning.
- It provides a concrete mechanism/practice for `SoT - Active Learning Techniques`.
- It serves to expose and break the `SoT - Illusion of Explanatory Depth (IoED)`.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Active Learning Techniques.md` | **Use:** Target is a concrete strategy (the Protégé Effect/Feynman Technique) that implements active learning. | Yes. | No. | Yes. | Pass (Edge: Target `implements` Candidate) |
| `SoT - Illusion of Explanatory Depth (IoED).md` | **Use:** Target depends on the mechanism of IoED to provide its benefit (by exposing the depth gaps). | Yes. | No. | Yes. | Pass (Edge: Target `depends_on` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Explaining to Others...md` | `%%[implements:: [[SoT - Active Learning Techniques]]]%%` | Target is an applied technique of the active learning framework. | Yes |
| `Explaining to Others...md` | `%%[depends_on:: [[SoT - Illusion of Explanatory Depth (IoED)]]]%%` | The benefit of explaining depends on exposing the cognitive bias described in IoED. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain links in the "Related" section will be preserved as contextual mentions, except the ones being formalized into typed edges which will be appended with the edges.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `The act of explaining or teaching material to others significantly enhances the explainer's own understanding and knowledge retention.` |
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
Following the enrichment pass, `Explaining to Others...` has been transformed from an orphan into a structured applied strategy claim. It now correctly implements the Active Learning Techniques framework and depends on the IoED cognitive bias concept.

### Exposure List
- **Dependents (Outbound load = 1):** `depends_on` edge adds inbound load to `SoT - Illusion of Explanatory Depth (IoED)`.
- **Dependencies (Inbound load = 0):** This node acts as an applied practice.

### Threads
Target functions as a core practice within the active learning pedagogy:
- **Thread 1 (Active Learning Practices):**
  `Explaining to Others...` (Concrete Strategy)
  ↳ `implements` -> `SoT - Active Learning Techniques` (Framework)
  ↳ `depends_on` -> `SoT - Illusion of Explanatory Depth (IoED)` (Cognitive Bias targeted)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - Active Learning Techniques.md` -> [Typed Edge: `implements`]
  - `SoT - Illusion of Explanatory Depth (IoED).md` -> [Typed Edge: `depends_on`]
  - (Multiple related links) -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework and conceptual dependencies.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual links preserved.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, lacked `epistemic_status`, and had `non_conformance_reason`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.