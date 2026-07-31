---
title: 2026-07-31-novelty-prompts
type: note
permalink: llmeon/90-audits/2026-07-31-novelty-prompts
---

## Positioning — [[Novelty Prompts Increase Engagement in ADHD Writing]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`type: claim`, `conformant: false`, `non_conformance_reason`, `source`), lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). Contains a wikilink inside the `source` frontmatter field.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 (wikilink in frontmatter to `MOC - Daily Writing for Clarity and ADHD-Friendly Techniques`).
Overall: Inbound orphan.

### Search Execution
- Target is a claim about using novelty to increase writing engagement for ADHD.
- It is an inbound orphan but points outward to a MoC via a frontmatter `source` field.
- I will modernize the frontmatter to the ProdOS claim standard, and move the `source` link into the body of the note.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| N/A | Target is an atomic claim. | N/A | N/A | N/A | Pass (No edge mutations needed) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
None.

### Patch B — Plain Links / MoC Anchors (Leon applies)
Move the `[[MOC - Daily Writing for Clarity and ADHD-Friendly Techniques]]` link from the YAML `source` field into the body text under a `### Related` heading.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `type`, `non_conformance_reason`, `source` | (present) | (Remove) |
| `prodos.kind` | (missing) | `claim` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Using novelty prompts and random selection in writing routines spikes dopamine, increasing engagement for individuals with ADHD.` |
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
Following the enrichment pass, `Novelty Prompts Increase Engagement in ADHD Writing` has been updated to use the standard ProdOS claim schema. It serves as an isolated claim and remains an inbound orphan.

### Exposure List
- **Dependents (Outbound load = 0):** No active load.
- **Dependencies (Inbound load = 0):** This node acts as an isolated claim.

### Threads
Target functions as a writing/ADHD claim:
- **Thread 1 (ADHD / Writing):**
  `Novelty Prompts Increase Engagement in ADHD Writing` (Claim)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `MOC - Daily Writing for Clarity and ADHD-Friendly Techniques.md` -> [Plain Link (Mention)]

### Patch A (Typings)
None required. The note had no typed edges.

### Patch B (Sever Candidates / Mergers)
The `source` wikilink was relocated from the frontmatter to the body as a standard plain link.

### Pathologies Found
- **Orphan:** The note was and remains an inbound orphan.
- **Legacy Frontmatter:** The YAML contained defunct schema fields (`type: claim`, `conformant: false`, `non_conformance_reason`, `source`), and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). This was fully modernised.

### Frontier
- Claim could be linked in the future to ADHD or Writing MoCs. Currently a stable claim.

### Next Action
Mark audit as complete and move to the next target.