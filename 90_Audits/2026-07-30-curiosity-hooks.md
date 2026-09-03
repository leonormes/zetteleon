---
title: 2026-07-30-curiosity-hooks
type: note
permalink: llmeon/90-audits/2026-07-30-curiosity-hooks
---

## Positioning — [[Curiosity Hooks are Self-Posed Questions to Rekindle Inspiration]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block and `proposition`).
Existing link count in: 1 (from `MOC - Project Continuity`).
Existing link count out: 0 (True orphan outbound).

### Search Execution
- `Curiosity Hooks` -> [Found the inline link in `MOC - Project Continuity`]
- `Interest-Based Nervous System` -> [Identified the foundational axiom that explains *why* this technique works for ADHD brains].
- `Context Preservation Techniques Maintain Project Novelty and Meaning` -> [Identified the parent category strategy node from the MoC].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `The ADHD brain operates on an Interest-Based Nervous System.md` | **Use:** Target describes a technique to "rekindle inspiration" via "discovery" instead of chores. This is a direct application/hack of the IBNS axiom. | Yes—if the brain operated on importance, curiosity hooks wouldn't be necessary. | No. | Yes—it grounds the technique in neurobiology rather than just "general productivity advice". | Pass (Edge: Target `depends_on` Candidate) |
| `Context Preservation Techniques Maintain Project Novelty and Meaning.md` | **Use:** Target is a specific instance/implementation of this broader category strategy. | Yes—retracting the specific technique weakens the broader strategy's practical application. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Curiosity Hooks are Self-Posed Questions to Rekindle Inspiration.md` | `[depends_on:: [[The ADHD brain operates on an Interest-Based Nervous System]]]` | The technique only works because it specifically targets the triggers (novelty, interest, discovery) of the IBNS to overcome initiation friction. | Yes |
| `Curiosity Hooks are Self-Posed Questions to Rekindle Inspiration.md` | `[supports:: [[Context Preservation Techniques Maintain Project Novelty and Meaning]]]` | Target is a concrete implementation of the broader context preservation strategy. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Curiosity Hooks are Self-Posed Questions to Rekindle Inspiration.md` | `- [[MOC - Project Continuity]]` | New `## Related` section. |
| `Curiosity Hooks are Self-Posed Questions to Rekindle Inspiration.md` | `- [[A Project Story Tracks a Project's Evolving Vision]] — _A complementary context preservation technique._` | New `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Leaving self-posed questions and interesting problems (curiosity hooks) for your future self successfully bypasses task-initiation friction by triggering the interest-based nervous system upon return.` |
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
Following the enrichment pass, `Curiosity Hooks...` has been transformed from an outbound orphan into a structurally anchored implementation node. It correctly derives its mechanism of action from an underlying neurobiological axiom and structurally supports a broader continuity strategy.

### Exposure List
- **Dependents (Outbound load = 1):** `Context Preservation Techniques Maintain Project Novelty and Meaning` relies on this node as a specific, actionable implementation of its strategy.
- **Dependencies (Inbound load = 0):** This node acts as a leaf implementation, receiving no inbound structural support.

### Threads
The node forms a critical bridge connecting high-level strategy to low-level neuroscience:
- **Thread 1 (Continuity via IBNS):**
  `The ADHD brain operates on an Interest-Based Nervous System` (Axiom)
  ↳ `depends_on` <- `Curiosity Hooks are Self-Posed Questions...` (Implementation)
  ↳ `supports` -> `Context Preservation Techniques Maintain Project Novelty and Meaning` (Strategy)

### Traversal Manifest
- **Inbound:**
  - `MOC - Project Continuity.md` -> [Mention / Hub Link]
- **Outbound:**
  - `The ADHD brain operates on an Interest-Based Nervous System.md` -> [Typed Edge: `depends_on`]
  - `Context Preservation Techniques Maintain Project Novelty and Meaning.md` -> [Typed Edge: `supports`]
  - `MOC - Project Continuity.md` -> [Mention] Annotated link in `## Related`.
  - `A Project Story Tracks a Project's Evolving Vision.md` -> [Mention] Annotated sibling link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects the context preservation strategy to the IBNS axiom that makes it effective.

### Patch B (Sever Candidates / Mergers)
No severances required. Relevant hub and sibling connections were added to a new `## Related` section.

### Pathologies Found
- **Orphan (Outbound):** The note had zero outbound links, completely isolated from both the reason it works and the broader category it belongs to. This has been fully resolved.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.