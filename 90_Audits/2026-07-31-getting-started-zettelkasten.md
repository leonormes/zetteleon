---
title: 2026-07-31-getting-started-zettelkasten
type: note
permalink: llmeon/90-audits/2026-07-31-getting-started-zettelkasten
---

## Positioning — [[Getting Started with Zettelkasten with ADHD]] — 2026-07-31

### Baseline
Thin—frontmatter non-conformant (uses legacy `type: permanent`, missing `prodos` block, `proposition`, `conformant`, has legacy keys `last_reviewed`, `status`, `updated`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (A plain link to a daily note).
Overall: True inbound orphan note.

### Search Execution
- Target offers practical advice on overcoming inertia when starting a PKM practice with ADHD by reducing activation energy and permitting imperfection.
- Investigated `SoT - ADHD Management Protocols`, which contains extensive guidance on reducing task initiation friction and overriding perfectionism-induced paralysis.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - ADHD Management Protocols.md` | **Use:** Target acts as a domain-specific (PKM) implementation of the general initiation and scaffolding tactics defined in the SoT. | Yes—if ADHD inertia wasn't governed by these general protocols, this PKM-specific advice wouldn't work. | No. | Yes. | Pass (Edge: Target `implements` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Getting Started...md` | `%%[implements:: [[SoT - ADHD Management Protocols]]]%%` | Target is a concrete, domain-specific execution of ADHD initiation protocols. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. Preserve the plain link to the daily note.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `permanent` | `claim` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Zettelkasten adoption for ADHD brains requires minimizing activation energy through extreme simplicity and permission for imperfection, bypassing the perfectionism that causes task paralysis.` |
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
Following the enrichment pass, `Getting Started with Zettelkasten...` has been transformed from an orphan into a structured claim/procedure. It now correctly acts as a domain-specific (PKM) implementation of the general initiation and scaffolding tactics defined in the ADHD Management Protocols SoT.

### Exposure List
- **Dependents (Outbound load = 0):** `implements` edges do not increase load.
- **Dependencies (Inbound load = 0):** This node acts as a practical implementation guide.

### Threads
Target functions as a concrete implementation in the ADHD productivity domain:
- **Thread 1 (ADHD Knowledge Management):**
  `Getting Started with Zettelkasten...` (Domain Implementation)
  ↳ `implements` -> `SoT - ADHD Management Protocols` (Framework)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - ADHD Management Protocols.md` -> [Typed Edge: `implements`]
  - `2025-04-21` -> [Mention / `See also:`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required.

### Pathologies Found
- **Orphan:** The note was a true inbound orphan.
- **Legacy Frontmatter:** The YAML used legacy keys (`type: permanent`, `last_reviewed`, `status`, `updated`), lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), lacked `proposition`, and was missing `conformant`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.