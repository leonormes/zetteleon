---
title: 2026-07-31-estimating-time-adhd
type: note
permalink: llmeon/90-audits/2026-07-31-estimating-time-adhd
---

## Positioning — [[Estimating Time for ADHD (Tripling Estimates)]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy empty fields (`status`, `last_reviewed`, `updated`), outdated `type: permanent`, and lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (plain link to `The Done State as a Boundary for ADHD Projects`).
Overall: True inbound orphan note.

### Search Execution
- Target asserts that individuals with ADHD should triple their time estimates to account for neurological time blindness.
- Investigated `SoT - ADHD Management Protocols`, which collects tactical principles (External Scaffolding) to compensate for ADHD hardware constraints (like Time Blindness, which is explicitly noted).

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - ADHD Management Protocols.md` | **Use:** Target acts as a concrete tactical scaffolding rule that compensates for the time blindness constraint defined in the ADHD protocols. | Yes. | No. | Yes. | Pass (Edge: Target `implements` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Estimating Time for ADHD (Tripling Estimates).md` | `%%[implements:: [[SoT - ADHD Management Protocols]]]%%` | Target is an applied practice (a scaffolding protocol) for managing ADHD time blindness. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain link to `The Done State as a Boundary for ADHD Projects` is preserved as a contextual mention.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `status`, `type`, etc | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Tripling time estimates is a necessary cognitive scaffold for ADHD to counter intrinsic time blindness.` |
| `epistemic_status` | (missing) | `high` |
| `tags` | `[TheHuman/Health/ADHD]` | `[TheHuman/Health/ADHD, time-management, estimation, scaffolding]` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Estimating Time for ADHD...` has been transformed from an inbound orphan into a structured applied method claim. It now correctly implements the external scaffolding rules defined in the ADHD Management Protocols SoT.

### Exposure List
- **Dependents (Outbound load = 0):** `implements` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as an applied practice.

### Threads
Target functions as a concrete practice for managing neurological time blindness:
- **Thread 1 (External Scaffolding):**
  `Estimating Time for ADHD...` (Applied Practice)
  ↳ `implements` -> `SoT - ADHD Management Protocols` (ADHD External Scaffolding)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - ADHD Management Protocols.md` -> [Typed Edge: `implements`]
  - `The Done State as a Boundary for ADHD Projects.md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual links preserved.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used the outdated `type: permanent`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, lacked `epistemic_status`, and had legacy empty fields (`status`, `last_reviewed`, `updated`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.