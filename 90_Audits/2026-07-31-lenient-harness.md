---
title: 2026-07-31-lenient-harness
type: note
permalink: llmeon/90-audits/2026-07-31-lenient-harness
---

## Positioning — [[Lenient Harness Parsing Removes the Negative-Reinforcement Signal for Malformed Tool Output]] — 2026-07-31

### Baseline
Poor—frontmatter has legacy fields (`type: claim`), a malformed `title` wrapping issue, lacks the mandatory ProdOS block (`prodos.kind`, `prodos.lifecycle`, `conformant`). Contains legacy kwargs on the typed edge.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 5 (1 typed edge to `Reinforcement Learning Produces Jagged Intelligence...`, 4 plain links).
Overall: Inbound orphan.

### Search Execution
- Target is an atomic claim about how lenient harness parsing degrades model training signals.
- It depends on the claim about RL producing jagged intelligence.
- I will modernize the frontmatter to the ProdOS claim standard and strip the legacy kwargs from the typed edge.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains` | Target explicitly depends on this claim. | N/A | N/A | N/A | Pass (Edge exists but requires Patch A) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Lenient Harness Parsing...md` | `[depends_on:: [[Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains]]]` | Strip legacy kwargs from existing typed edge to conform to strict schema. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing plain links are preserved.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `claim` | (Remove) |
| `title` | (malformed wrapping) | `Lenient Harness Parsing Removes the Negative-Reinforcement Signal for Malformed Tool Output` |
| `prodos.kind` | (missing) | `claim` |
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
Following the enrichment pass, `Lenient Harness Parsing...` has been transformed from an inbound orphan with legacy formatting into a structurally compliant ProdOS atomic claim. It remains an inbound orphan but correctly depends on its foundational claim.

### Exposure List
- **Dependents (Outbound load = 0):** `depends_on` edges do not increase inbound load on the source note.
- **Dependencies (Inbound load = 0):** This node acts as an isolated claim extending others.

### Threads
Target functions as a dependent claim:
- **Thread 1 (Harness Design & Reinforcement Learning):**
  `Lenient Harness Parsing...` (Atomic Claim)
  ↳ `depends_on` -> `Reinforcement Learning Produces Jagged Intelligence...`

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `Reinforcement Learning Produces Jagged Intelligence...md` -> [Typed Edge: `depends_on`]
  - `Structured Output Enforcement (JSON Schema and Function Calling).md` -> [Plain Link (Mention)]
  - `Grammar-Constrained Decoding Forces Hallucination When JSON Tool-Call Sampling Fails.md` -> [Plain Link (Mention)]
  - `Agent Harness - Wrapping LLMs in Deterministic Software Controls.md` -> [Plain Link (Mention)]
  - `SoT - AI Sycophancy.md` -> [Plain Link (Mention)]

### Patch A (Typings)
Successfully applied. The node's existing edge was stripped of legacy kwargs to conform to the strict six-word vocabulary rule.

### Patch B (Sever Candidates / Mergers)
No severances required. Contextual links preserved.

### Pathologies Found
- **Orphan:** The note was and remains an inbound orphan.
- **Legacy Edge Formatting:** The `depends_on` edge contained legacy kwargs (`strength`, `confidence`) which were removed.
- **Legacy Frontmatter:** The YAML used the outdated `type: claim`, contained a malformed `title`, and lacked the mandatory ProdOS block (`conformant`, `prodos.kind`, `prodos.lifecycle`). This was all fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.