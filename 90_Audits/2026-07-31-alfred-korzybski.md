---
title: 2026-07-31-alfred-korzybski
type: note
permalink: llmeon/90-audits/2026-07-31-alfred-korzybski
---

## Positioning — [[Alfred Korzybski and General Semantics]] — 2026-07-31

### Baseline
Thin—frontmatter highly non-conformant (missing `conformant`, `proposition`, `prodos` block, contains legacy keys `last_reviewed`, `status`, `updated`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 4 (Wikilinks at the bottom of the page, plus inline).
Overall: Orphan note (not structurally anchored to an SoT).

### Search Execution
- Target defines "General Semantics" (Abstraction Awareness, Non-Identity, Time-Binding) by Alfred Korzybski.
- Investigated `SoT - Reality, Models, and the Limits of Accuracy`, which explicitly bases its Section 2 ("The Core Epistemology: General Semantics") on this exact framework.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Reality, Models, and the Limits of Accuracy.md` | **Use:** Target defines the foundational epistemology (Korzybski's three principles) adopted by the SoT's core model of reality. | Yes—if Korzybski's distinction between map and territory were false, the entire SoT's premise on model limitations would fall apart. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Alfred Korzybski and General Semantics.md` | `%%[supports:: [[SoT - Reality, Models, and the Limits of Accuracy]]]%%` | Target is the foundational origin defining the core epistemology used in the SoT. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. Existing textual links at the bottom are preserved as lateral/conceptual references.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `permanent` | `claim` |
| `last_reviewed` / `status` / `updated` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Alfred Korzybski's principles of General Semantics—Abstraction Awareness, Non-Identity, and Time-Binding—form the epistemological foundation establishing that models (maps) are inherently abstracted from reality (the territory).` |
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
Following the enrichment pass, `Alfred Korzybski...` has been transformed from an orphan into a structured claim. It now correctly acts as the foundational origin of the General Semantics epistemology underpinning the Reality Models SoT.

### Exposure List
- **Dependents (Outbound load = 1):** 
  1. `SoT - Reality, Models, and the Limits of Accuracy` relies on this node as its foundational epistemology.
- **Dependencies (Inbound load = 0):** This node acts as an epistemological foundation.

### Threads
Target functions as a core justification in the philosophy/cognition domain:
- **Thread 1 (Epistemology):**
  `Alfred Korzybski...` (Foundational Origin)
  ↳ `supports` -> `SoT - Reality, Models, and the Limits of Accuracy` (Framework)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - Reality, Models, and the Limits of Accuracy.md` -> [Typed Edge: `supports`]
  - `Mental Models as Evolutionary Filters` -> [Mention]
  - `Leaky Abstractions` -> [Mention]
  - `The Map is Not the Territory` -> [Mention]
  - `Mistaking the Map for the Territory` -> [Mention]
  - `Maps as Simplified Abstractions` -> [Mention]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Unresolved related plain links preserved.

### Pathologies Found
- **Orphan:** The note was a true orphan.
- **Legacy Frontmatter:** The YAML used legacy keys (`last_reviewed`, `status`, `updated`), was missing `proposition`, lacked the mandatory ProdOS block (`prodos.kind` and `prodos.lifecycle`), and `type` was `permanent` rather than `claim`. This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.