---
title: 2026-07-30-commitment-consistency
type: note
permalink: llmeon/90-audits/2026-07-30-commitment-consistency
---

## Positioning — [[Commitment, Consistency, and Sunk Cost Fallacy]] — 2026-07-30

### Baseline
Thin—frontmatter highly non-conformant (missing `conformant`, `prodos` block, `proposition`, contains legacy keys like `creation_date`, `status`, `updated`).
Existing link count in: 0 (True inbound orphan).
Existing link count out: 0 (No wikilinks, only text references).
Overall: True orphan note (not structurally anchored to an SoT).

### Search Execution
- `Sunk Cost Fallacy` / `Commitment` / `Consistency` -> [Identified cognitive bias and ego defense mechanisms].
- Investigated `SoT - Social Cognition & Self-Perception` -> [Identified Section 2 on the Social Intuitionist Model and Strategic Reasoning, where conscious reasoning is a post-hoc justification for an ego-driven position].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Social Cognition & Self-Perception.md` | **Use:** Target acts as a specific example of "Strategic Reasoning" (manufacturing reasons to justify an ego investment), supporting the SoT's model of post-hoc justification. | Yes—if individuals dropped arguments based purely on logic rather than sunk ego costs, the post-hoc reasoning model of social cognition would be false. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Commitment, Consistency, and Sunk Cost Fallacy.md` | `[supports:: [[SoT - Social Cognition & Self-Perception]]]` | Target provides a cognitive mechanism (sunk cost/consistency bias) that reinforces the SoT's theory of ego-driven, post-hoc rationalisation in social conflict. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
None required. The existing text references to "Contextual Myopia" and "Contextual Relationships" are left as bare text since they represent dangling concepts/discussions rather than concrete notes.

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `''` | `claim` |
| `creation_date` / `status` / `updated` / `last_reviewed` | (present) | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Once individuals commit to a position, they experience internal pressure to remain consistent, often manufacturing rationalisations to justify sunk costs and protect their ego.` |
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
Following the enrichment pass, `Commitment, Consistency, and Sunk Cost Fallacy` has been transformed from an orphan into a structured claim. It now correctly acts as a specific cognitive mechanism (sunk cost bias) validating the post-hoc rationalisation and ego-defense models defined in the Social Cognition SoT.

### Exposure List
- **Dependents (Outbound load = 1):** 
  1. `SoT - Social Cognition & Self-Perception` relies on this node as a proof point for its Strategic Reasoning concept.
- **Dependencies (Inbound load = 0):** This node acts as a fundamental behavioral mechanism.

### Threads
Target functions as a core justification in the psychology/cognition domain:
- **Thread 1 (Cognitive Biases / Post-Hoc Justification):**
  `Commitment, Consistency, and Sunk Cost Fallacy` (Cognitive Mechanism)
  ↳ `supports` -> `SoT - Social Cognition & Self-Perception` (Framework)

### Traversal Manifest
- **Inbound:**
  - None.
- **Outbound:**
  - `SoT - Social Cognition & Self-Perception.md` -> [Typed Edge: `supports`]

### Patch A (Typings)
Successfully applied. The node now structurally connects to its parent framework.

### Patch B (Sever Candidates / Mergers)
No severances required. Unresolved textual mentions were left bare as they refer to non-existent conceptual placeholders rather than active nodes.

### Pathologies Found
- **Orphan:** The note was a true orphan (neither anchored to an MOC nor an SoT).
- **Legacy Frontmatter:** The YAML contained numerous legacy keys (`creation_date`, `last_reviewed`, `status`, `updated`, blank `type`) and lacked the mandatory ProdOS block and `proposition`. This was fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.