---
title: 2026-07-31-evidence-adhd-heterogeneity
type: note
permalink: llmeon/90-audits/2026-07-31-evidence-adhd-heterogeneity
---

## Positioning — [[Evidence - ADHD Heterogeneity Network Analysis 91.8 Percent Unique Patterns]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`source_quote`, `source_reference`, `supports_claims`, `type: evidence`), lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 2 (typed edge to `ADHD is a Heterogeneous Condition with Unique Symptom Patterns`, plain link to `MOC - ADHD (The Master Map)`).
Overall: Inbound orphan.

### Search Execution
- Target is an evidence note that already supports `ADHD is a Heterogeneous Condition with Unique Symptom Patterns`. 
- No further edges required, but the existing typed edge has legacy `strength=` and `confidence=` kwargs which must be stripped to adhere to the strict six-word vocabulary rule.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `ADHD is a Heterogeneous Condition with Unique Symptom Patterns.md` | **Use:** Target acts as empirical evidence supporting this claim. | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate - existing but needs format strip) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Evidence - ADHD Heterogeneity...md` | `[supports:: [[ADHD is a Heterogeneous Condition with Unique Symptom Patterns]]]` | Strip legacy kwargs from existing typed edge to conform to strict schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain link to `MOC - ADHD (The Master Map)` is preserved.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type`, `source_quote`, etc | (present) | (Remove) |
| `prodos.kind` | (missing) | `evidence` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `A network analysis study found that 91.8% of individuals with ADHD had a unique symptom pattern, indicating a one-size-fits-all approach is inappropriate.` |
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
Following the enrichment pass, `Evidence - ADHD Heterogeneity...` has been transformed from an inbound orphan with legacy formatting into a structurally compliant ProdOS evidence note. It correctly supports its target claim.

### Exposure List
- **Dependents (Outbound load = 0):** `supports` edges do not increase inbound load.
- **Dependencies (Inbound load = 0):** This node acts as base evidence.

### Threads
Target functions as empirical support:
- **Thread 1 (ADHD Heterogeneity):**
  `Evidence - ADHD Heterogeneity...` (Evidence)
  ↳ `supports` -> `ADHD is a Heterogeneous Condition with Unique Symptom Patterns` (Atomic Claim)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `ADHD is a Heterogeneous Condition with Unique Symptom Patterns.md` -> [Typed Edge: `supports`]
  - `MOC - ADHD (The Master Map).md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node's existing edge was stripped of legacy kwargs to conform to the strict six-word vocabulary rule.

### Patch B (Sever Candidates / Mergers)
No severances required. Existing contextual links preserved.

### Pathologies Found
- **Orphan:** The note was an inbound orphan.
- **Legacy Edge Formatting:** The `supports` edge contained legacy kwargs (`strength`, `confidence`) which were removed.
- **Legacy Frontmatter:** The YAML used the outdated `type: evidence`, contained defunct schema fields (`source_quote`, `source_reference`, `supports_claims`), and lacked the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `proposition`, `epistemic_status`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.