---
title: 2026-07-30-equal-say-finances
type: note
permalink: llmeon/90-audits/2026-07-30-equal-say-finances
---

## Positioning — [[Partners Should Have Equal Say in Financial Decisions Regardless of Income]] — 2026-07-30

### Baseline
Thin—frontmatter missing `prodos` block and `proposition`.
Existing link count in: 4 (Mentions from `MOC - Family & Finance`, `MOC - Healthy Relationship Expectations and Needs`, `MOC - Relational Dynamics & Family (Triage)`, and `SoT - Family Financial Wellness`).
Existing link count out: 0 (True outbound orphan).

### Search Execution
- `Equal Say in Financial Decisions` -> [Found correctly mapped in multiple Relationship MOCs and anchored in the Family Finance SoT].
- Investigated `SoT - Family Financial Wellness` -> [Identified as the parent framework defining the mechanics of the Relational Architecture: The One-Pot Model].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Family Financial Wellness.md` | **Use:** Target defines the foundational logic (Equal Autonomy) that underpins Section 4.II of the SoT. | Yes—if unequal say was permitted, the "One-Pot Model" architecture would collapse into financial control. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Partners Should Have Equal Say...md` | `%%[supports:: [[SoT - Family Financial Wellness]]]%%` | Target acts as a structural load-bearing pillar for the SoT's relational architecture. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Partners Should Have Equal Say...md` | `- [[Finances in an Unequal-Income Partnership Should Be Treated as Shared Family Money]]` | New `## Related` section (sibling foundation). |
| `Partners Should Have Equal Say...md` | `- [[A Fair Financial System Uses a Shared Pot and Equal Personal Spending Money]]` | New `## Related` section (downstream application). |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `It is reasonable for partners to expect an equal (50/50) say on all major financial decisions and goal-setting, because all money is considered "family money."` |
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
Following the enrichment pass, `Partners Should Have Equal Say...` has been transformed from an outbound orphan into a structurally sound definitional claim. It now correctly underpins `SoT - Family Financial Wellness` by philosophically enabling the "One-Pot Model" relational architecture.

### Exposure List
- **Dependents (Outbound load = 1):** `SoT - Family Financial Wellness` relies on this node as the structural bedrock for its relational protocols (specifically to prevent the model collapsing into unilateral financial control).
- **Dependencies (Inbound load = 0):** This node acts as a fundamental definition.

### Threads
Target functions as the core definitional baseline for the broader financial framework:
- **Thread 1 (Relational Architecture Baseline):**
  `Partners Should Have Equal Say...` (Definitional Baseline)
  ↳ `supports` -> `SoT - Family Financial Wellness` (Framework)

### Traversal Manifest
- **Inbound:**
  - `MOC - Family & Finance.md` -> [Mention]
  - `MOC - Healthy Relationship Expectations and Needs.md` -> [Mention]
  - `MOC - Relational Dynamics & Family (Triage).md` -> [Mention]
  - `SoT - Family Financial Wellness.md` -> [Mention] Annotated in `## Related Claims` section.
- **Outbound:**
  - `SoT - Family Financial Wellness.md` -> [Typed Edge: `supports`]
  - `Finances in an Unequal-Income Partnership Should Be Treated as Shared Family Money.md` -> [Mention] Annotated sibling link in `## Related`.
  - `A Fair Financial System Uses a Shared Pot and Equal Personal Spending Money.md` -> [Mention] Annotated downstream protocol link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects the foundational concept of equality in financial decisions to the overarching Family Financial Wellness framework.

### Patch B (Sever Candidates / Mergers)
No severances required. The related sibling foundations and downstream protocols were surfaced in a new `## Related` section.

### Pathologies Found
- **Orphan:** The note was an outbound orphan.
- **Legacy Frontmatter:** The YAML lacked the mandatory ProdOS block and `proposition`. This was fully modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.