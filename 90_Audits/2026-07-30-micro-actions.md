---
title: 2026-07-30-micro-actions
type: note
permalink: llmeon/90-audits/2026-07-30-micro-actions
---

## Positioning — [[Master Micro-Actions & Starter Tasks]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (`conformant: false`, missing `prodos` block, missing `proposition`, uses `type: hypothesis` and legacy metadata). Contains a dead outbound link to `[[ADHD Behavioral Strategies for Productivity]]`.
Existing link count in: 0 (True inbound orphan).
Existing link count out: 1 live (`SoT - ADHD Neurology & Core Concepts`), 1 dead.

### Search Execution
- Searched for the dead link `ADHD Behavioral Strategies for Productivity` -> [Not found, confirmed dead link].
- Searched for `Starter Task` -> [Found in `SoT - ADHD Management Protocols` Section 3.1].
- `SoT - ADHD Management Protocols` states it implements `Micro-Stepping Reduces Cognitive Load for Task Initiation`.

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `SoT - ADHD Management Protocols.md` | **Use:** Target provides the experimental hypothesis and tracking structure for the "Starter Task" protocol described in section 3.1 of the SoT. | Yes—if micro-actions didn't work, the SoT's protocol 3.1 would be invalid. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |
| `Micro-Stepping Reduces Cognitive Load for Task Initiation.md` | **Use:** Target is the operationalised experiment (the how-to) of this theoretical claim (the why). | Yes. | No. | Yes. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Master Micro-Actions & Starter Tasks.md` | `%%[supports:: [[SoT - ADHD Management Protocols]]]%%` | Target acts as the experimental proof and implementation of the SoT's Starter Task protocol. | Yes |
| `Master Micro-Actions & Starter Tasks.md` | `%%[supports:: [[Micro-Stepping Reduces Cognitive Load for Task Initiation]]]%%` | Target is the actionable proof-point of the cognitive load claim. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Master Micro-Actions & Starter Tasks.md` | Remove: `Derived from [[ADHD Behavioral Strategies for Productivity]].` | End of file (dead link removal). |
| `Master Micro-Actions & Starter Tasks.md` | `- [[SoT - ADHD Management Protocols]]` | New `## Related` section. |
| `Master Micro-Actions & Starter Tasks.md` | `- [[SoT - ADHD Neurology & Core Concepts]]` | New `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` (implicit) | `true` |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Breaking a daunting task down until the first step is absurdly small (< 2 minutes, purely physical) lowers the activation energy below the threshold of the Wall of Awful, triggering immediate task initiation.` |
| `epistemic_status` | (missing) | `absolute` |
| `status`, `updated`, `last_reviewed` | (present) | (Remove legacy keys) |
| `type` | `hypothesis` | `claim` |
| `tags` | `[..., hypothesis, The, ...]` | Removed rogue `The` and `hypothesis`. |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `Master Micro-Actions...` has been transformed from an inbound/outbound orphan with legacy YAML into a structurally sound experimental protocol node. It now properly underpins both the theoretical cognitive load claim and the broader ADHD management protocols.

### Exposure List
- **Dependents (Outbound load = 2):** `SoT - ADHD Management Protocols` relies on this node as the actionable experiment for its "Starter Task" section. `Micro-Stepping Reduces Cognitive Load for Task Initiation` relies on it as its operationalised proof point.
- **Dependencies (Inbound load = 0):** This node acts as a base-level experiment.

### Threads
Target functions as the actionable, experimental proof for theoretical claims:
- **Thread 1 (ADHD Protocol):**
  `Master Micro-Actions & Starter Tasks` (Experimental Protocol)
  ↳ `supports` -> `SoT - ADHD Management Protocols` (Framework)
- **Thread 2 (Cognitive Theory to Protocol):**
  `Master Micro-Actions & Starter Tasks` (Operationalised Experiment)
  ↳ `supports` -> `Micro-Stepping Reduces Cognitive Load for Task Initiation` (Theoretical Claim)

### Traversal Manifest
- **Inbound:**
  - None. (True inbound orphan).
- **Outbound:**
  - `SoT - ADHD Management Protocols.md` -> [Typed Edge: `supports`] & [Mention in `## Related`]
  - `Micro-Stepping Reduces Cognitive Load for Task Initiation.md` -> [Typed Edge: `supports`]
  - `SoT - ADHD Neurology & Core Concepts.md` -> [Mention] Annotated hub link in `## Related`.

### Patch A (Typings)
Successfully applied. The node now structurally connects the experimental hypothesis to the overarching problem-solving frameworks.

### Patch B (Sever Candidates / Mergers)
The dead link to `ADHD Behavioral Strategies for Productivity` was severed. The surviving core concepts were surfaced in a new `## Related` section.

### Pathologies Found
- **Orphan:** The note was a true orphan with zero inbound links and only one live outbound link hidden in the text.
- **Dead Link:** Contained a reference to a non-existent file.
- **Legacy Frontmatter:** The YAML contained deprecated keys (`status`, `last_reviewed`, `updated`), an incorrect type (`hypothesis`), rogue tags (`The`), and lacked the mandatory ProdOS block. This was purged and modernised.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.