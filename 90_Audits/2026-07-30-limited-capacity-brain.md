---
title: 2026-07-30-limited-capacity-brain
type: note
permalink: llmeon/90-audits/2026-07-30-limited-capacity-brain
---

## Positioning — [[Limited Capacity Brain]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (uses legacy `type: permanent`, `status: null`, no `prodos` object, lacks strict claim fields).
Existing link count in: 0 (True orphan for inbound links).
Existing link count out: 4 (all to SoT notes with legacy/custom annotations like `—elaborates-on—`).

### Search Execution
- `Working Memory` -> [`SoT - Working Memory & Schema Theory`, `Cognitive Offloading Frees Mental Resources...`, `Bessie's Working Memory...`, etc.]
- `not designed for recall` -> [No new results found]
- `jumping to conclusions` -> [`SoT - Illusion of Explanatory Depth (IoED)`, `Judgment is Thinking Things Through...`]
- `Limited Human Information Processing Capacity` -> [Found a near-duplicate note]

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Cognitive Offloading Frees Mental Resources for Decision-Making and Problem-Solving.md` | **Use:** Candidate relies on the brain's short-term capacity being bounded. | Yes—if the brain had infinite capacity, offloading would be unnecessary. | No—this is the specific biological constraint. | Yes—retracting this invalidates the need for offloading. | Pass (Edge: Target `supports` Candidate) |
| `SoT - Working Memory & Schema Theory.md` | **Use:** The SoT relies on the WM bottleneck as a core premise for schema theory. | Yes—if the brain wasn't limited, the SoT's bottleneck premise fails. | No. | Yes. | Pass (Edge: Target `supports` SoT) |
| `SoT - Illusion of Explanatory Depth (IoED).md` | **Use:** Target describes the brain fabricating narratives ("jumping to conclusions") to fill gaps in its limited capacity. | Yes—IoED is the formal phenomenon of this exact mechanism. | No. | Yes. | Pass (Edge: Target `supports` SoT) |
| `SoT - Prosthetic Executive Function.md` | **Use:** Prosthetic EF compensates for the brain's inherent recall limitations. | Yes. | No. | Yes. | Pass (Edge: Target `supports` SoT) |
| `SoT - Learning Mechanisms.md` | **Use:** Already linked as elaborates-on. | Yes. | No. | Yes. | Pass (Edge: Target `supports` SoT) |
| `Limited Human Information Processing Capacity.md` | **Mention:** Claims exactly the same thing: "finite capacity for processing and holding information...". | N/A | Yes—perfect substitute. | N/A | Patch B (Merge Recommendation) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Limited Capacity Brain.md` | `%%[supports:: [[Cognitive Offloading Frees Mental Resources for Decision-Making and Problem-Solving]]]%%` | The limited capacity of the brain is the biological justification for cognitive offloading. | Yes |
| `Limited Capacity Brain.md` | `%%[supports:: [[SoT - Working Memory & Schema Theory]]]%%` | Atomic claim supporting the SoT's section on WM bottlenecks. | Yes |
| `Limited Capacity Brain.md` | `%%[supports:: [[SoT - Illusion of Explanatory Depth (IoED)]]]%%` | Explains the underlying capacity gap that leads to narrative fabrication (IoED). | Yes |
| `Limited Capacity Brain.md` | `%%[supports:: [[SoT - Prosthetic Executive Function]]]%%` | Establishes the necessity for prosthetic/externalized executive function. | Yes |
| `Limited Capacity Brain.md` | `%%[supports:: [[SoT - Learning Mechanisms]]]%%` | Formalizing the existing `elaborates-on` link. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Limited Human Information Processing Capacity.md` | `MERGE RECOMMENDATION` | This note is a near-duplicate of `Limited Capacity Brain.md`. Recommend merging its single sentence into the Target and deleting it to remove fragmentation. |
| `Limited Capacity Brain.md` | (Cleaned up markdown list of the SoT links) | Replace the messy `## Related Concepts` and `## See Also` sections with a unified, cleanly annotated `## Related` list. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `true` |
| `type` | `permanent` | `claim` |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `The human brain has a strictly limited working memory capacity and is not designed for detailed recall, relying instead on narrative fabrication to fill gaps.` |
| `epistemic_status` | (missing) | `high` |
| `status` | `'null'` | (Remove) |
| `updated` | `null` | (Remove) |
| `last_reviewed` | `'null'` | (Remove) |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Limited Capacity Brain` has been structurally repositioned from an isolated "permanent" note to a foundational root claim (`type: claim`, `prodos.kind: atomic`). It now explicitly grounds five higher-order concepts and models across PKM, learning, and cognitive biases. The merger with its near-duplicate resolved a fragmented thread in the graph.

### Exposure List
- **Dependents (Outbound load):** 5 (Target `supports` five higher-level claims/SoTs, making it a high-load foundational premise).
- **Dependencies (Inbound load):** 0 (Target acts as a biological axiom; it has no incoming `supports` or `depends_on` edges).

### Threads
- **Thread 1 (Information Processing & Abstraction):** Target is synthesized by `Myopic Understanding` (inbound edge), which in turn synthesizes `Abstraction as Climbing a Hill`.
- **Thread 2 (Cognitive Productivity):** Target acts as the biological root that `supports` `Cognitive Offloading Frees Mental Resources...` and `SoT - Prosthetic Executive Function`.
- **Thread 3 (Learning & Schema):** Target acts as the biological root that `supports` `SoT - Working Memory & Schema Theory` and `SoT - Learning Mechanisms`.
- **Thread 4 (Bias Formation):** Target `supports` `SoT - Illusion of Explanatory Depth (IoED)`, establishing the mechanism for narrative fabrication.

### Traversal Manifest
- **Inbound:**
  - `Myopic Understanding.md` -> [Typed Edge: `synthesizes`]
  - `Cognitive Offloading Frees Mental Resources for Decision-Making and Problem-Solving.md` -> [Mention] Annotated link in `## See Also`.
- **Outbound:**
  - `Cognitive Offloading Frees Mental Resources for Decision-Making and Problem-Solving.md` -> [Typed Edge: `supports`]
  - `SoT - Working Memory & Schema Theory.md` -> [Typed Edge: `supports`]
  - `SoT - Illusion of Explanatory Depth (IoED).md` -> [Typed Edge: `supports`]
  - `SoT - Prosthetic Executive Function.md` -> [Typed Edge: `supports`]
  - `SoT - Learning Mechanisms.md` -> [Typed Edge: `supports`]
  - `Myopic Understanding.md` -> [Mention] Inline link.

### Patch A (Typings)
Applied successfully in Part 2. Target now functions as a high-leverage supporting node.

### Patch B (Sever Candidates)
Successfully executed. Near-duplicate `Limited Human Information Processing Capacity.md` was merged and deleted. Two broken inbound links pointing to the deleted note were re-routed to the Target.

### Pathologies Found
1. **Unanchored Axiom:** While the claim has 0 dependencies (acting as a root node), it represents established neuroscience/biology. The claim is accepted as true (`epistemic_status: high`), so this lack of internal evidence linking is not a pathology.

### Frontier
- The node is structurally sound and acting efficiently as a multi-domain root. No further action needed.

### Next Action
Mark audit as complete and move to the next target.