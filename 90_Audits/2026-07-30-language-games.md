---
title: 2026-07-30-language-games
type: note
permalink: llmeon/90-audits/2026-07-30-language-games
---

## Positioning — [[Meaning emerges from language games]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block and `proposition`).
Existing link count in: 2 (duplicate mentions in `MOC - The Gap Between Thought and Language`).
Existing link count out: 0 (True outbound orphan).

### Search Execution
- `Conduit Metaphor` / `Mental-to-mental` -> [Found the connection to the core communication SoT and Gap MoC].
- `SoT - Communication & Misunderstanding (The Experiential Filter)` -> [Identified as the structural parent that this claim underpins].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - Communication & Misunderstanding (The Experiential Filter).md` | **Use:** Target provides the philosophical proof (Wittgenstein's language games) for the SoT's core thesis that communication is "coordination, not transmission" and relies on "sufficient functional overlap." | Yes—if meaning required perfect mental correspondence, the SoT's pragmatic framework would fail. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Meaning emerges from language games.md` | `[supports:: [[SoT - Communication & Misunderstanding (The Experiential Filter)]]]` | Target acts as the philosophical grounding for the SoT's model of shared understanding. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Meaning emerges from language games.md` | `- [[MOC - The Gap Between Thought and Language]]` | New `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Meaning is not fixed definitions or mental-to-mental transmission, but emerges from how language is used in practice within shared social activities (language games).` |
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
Following the enrichment pass, `Meaning emerges from language games...` has been correctly repositioned from an outbound orphan to a foundational philosophical proof. It now structurally underpins the core communication SoT.

### Exposure List
- **Dependents (Outbound load = 1):** `SoT - Communication & Misunderstanding (The Experiential Filter)` relies on this node to justify its thesis that communication is functional coordination rather than perfect mental transmission.
- **Dependencies (Inbound load = 0):** This node acts as an independent philosophical premise.

### Threads
Target functions as the foundational mechanism for the pragmatic communication model:
- **Thread 1 (Pragmatic Communication):**
  `Meaning emerges from language games` (Philosophical Mechanism)
  ↳ `supports` -> `SoT - Communication & Misunderstanding (The Experiential Filter)` (Framework)

### Traversal Manifest
- **Inbound:**
  - `MOC - The Gap Between Thought and Language.md` -> [Mention / Hub Link]
- **Outbound:**
  - `SoT - Communication & Misunderstanding (The Experiential Filter).md` -> [Typed Edge: `supports`]
  - `MOC - The Gap Between Thought and Language.md` -> [Mention] Annotated hub link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects Wittgenstein's theory of meaning to the vault's overarching communication framework.

### Patch B (Sever Candidates / Mergers)
No severances required. The hub connection was added to `## Related`. Note: The inbound MoC contains a duplicate legacy `rel::` annotation, but that is outside the scope of mutating the target file.

### Pathologies Found
- **Orphan (Outbound):** The note had zero outbound links in the body. This has been resolved.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.