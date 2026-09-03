---
title: 2026-07-30-ltd-habit-breaking
type: note
permalink: llmeon/90-audits/2026-07-30-ltd-habit-breaking
---

## Positioning — [[Long-Term Depression is a Mechanism for Breaking Habits]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block and `proposition`). Contains an invalid `source` key pointing to an internal MoC.
Existing link count in: 1 (from `MOC - The Science of Making and Breaking Habits`).
Existing link count out: 0 (True orphan outbound in the body text).

### Search Execution
- `Long-Term Potentiation` / `neurons that fire together` -> [Found the counterpart note `Long-Term Potentiation (LTP)...`]
- `Neuroplasticity` -> [Found the parent claim `Neuroplasticity is the Foundation for Habit Change`].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Neuroplasticity is the Foundation for Habit Change.md` | **Use:** Target explains the exact physical mechanism (LTD / unwiring) that allows neuroplasticity to *break* habits, supporting the broad claim. | Yes—if LTD didn't exist, neuroplasticity could only explain habit *formation*, not breaking. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Long-Term Depression is a Mechanism for Breaking Habits.md` | `[supports:: [[Neuroplasticity is the Foundation for Habit Change]]]` | Target provides the neurobiological unwiring mechanism that proves neuroplasticity enables habit breaking. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Long-Term Depression is a Mechanism for Breaking Habits.md` | `- [[MOC - The Science of Making and Breaking Habits]]` | New `## Related` section (migrated from the invalid frontmatter `source` key). |
| `Long-Term Depression is a Mechanism for Breaking Habits.md` | `- [[Long-Term Potentiation (LTP) is a Key Cellular Mechanism for Learning]] — _The counterpart mechanism (neurons that fire together, wire together)._` | New `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Long-Term Depression (LTD) is the neuroscientific mechanism for breaking habits, weakening neural pathways when a trigger is intentionally dissociated from its habitual response.` |
| `epistemic_status` | (missing) | `absolute` |
| `source` | `'[[MOC...]]'` | (Remove—internal links belong in the body) |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Long-Term Depression...` has been correctly repositioned from an outbound orphan to a supporting mechanism node. It now structurally underpins the broader claim that neuroplasticity enables habit change.

### Exposure List
- **Dependents (Outbound load = 1):** `Neuroplasticity is the Foundation for Habit Change` relies on this node to explain the physical unwiring process necessary for breaking habits.
- **Dependencies (Inbound load = 0):** This node acts as a fundamental biological mechanism, receiving no structural support from other claims.

### Threads
Target functions as a core biological proof-point for neuroplasticity:
- **Thread 1 (Habit Unwiring):**
  `Long-Term Depression is a Mechanism for Breaking Habits` (Mechanism)
  ↳ `supports` -> `Neuroplasticity is the Foundation for Habit Change` (Axiom)

### Traversal Manifest
- **Inbound:**
  - `MOC - The Science of Making and Breaking Habits.md` -> [Mention / Hub Link]
- **Outbound:**
  - `Neuroplasticity is the Foundation for Habit Change.md` -> [Typed Edge: `supports`]
  - `Long-Term Potentiation (LTP) is a Key Cellular Mechanism for Learning.md` -> [Mention] Annotated counterpart link in `## Related`.
  - `MOC - The Science of Making and Breaking Habits.md` -> [Mention] Migrated to `## Related` from invalid YAML key.

### Patch A (Typings)
Successfully applied. The node now structurally connects the physical LTD unwiring mechanism to the habit change axiom it proves.

### Patch B (Sever Candidates / Mergers)
No severances required. The invalid frontmatter source link was correctly migrated to the body as a hub link, and the LTP counterpart was surfaced.

### Pathologies Found
- **Orphan (Outbound):** The note had zero outbound links in the body. This has been resolved.
- **Invalid Frontmatter Schema:** The YAML contained an internal wikilink within a `source` key, violating the ProdOS frontmatter contract. This was removed.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.