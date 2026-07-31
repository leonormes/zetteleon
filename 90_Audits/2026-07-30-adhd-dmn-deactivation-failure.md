---
title: 2026-07-30-adhd-dmn-deactivation-failure
type: note
permalink: llmeon/90-audits/2026-07-30-adhd-dmn-deactivation-failure
---

## Positioning — [[ADHD DMN Deactivation Failure]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (uses `type: concept`, `conformant: false`, missing `prodos` object and claim fields).
Existing link count in: 4 (from `ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag...`, `MOC - ADHD Functional Neurology...`, `_link_report...`, and `SoT - ADHD Neurology & Core Concepts`).
Existing link count out: 0 (True orphan outbound).

### Search Execution
- `The Glitchy Switch` -> [Direct candidate, identified via MoC consolidation checkbox]
- `daydreaming / mind-wandering` -> [Found `The Glitchy Switch`, `Task-Positive Network (TPN) and Default Mode Network (DMN) Defined`]

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `The Glitchy Switch - TPN and DMN Dysregulation in ADHD.md` | **Use:** Candidate describes "DMN intrusion" as a broad axiom. Target provides the specific fMRI/precuneus evidence for this intrusion. | Yes—if the DMN *did* deactivate normally (Target false), the Glitchy Switch premise of intrusion fails. | No—one is specific anatomical evidence, the other is a broad clinical axiom. | Yes—retracting the fMRI evidence weakens the axiom. | Pass (Edge: Target `supports` Candidate) |
| `ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag, Not Willpower Failure.md` | **Mention:** Both deal with DMN dysregulation, but different mechanisms (deactivation failure vs. maturational lag). | No. | No. | No. | Patch B (Keep as related) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `ADHD DMN Deactivation Failure.md` | `%%[supports:: [[The Glitchy Switch - TPN and DMN Dysregulation in ADHD]]]%%` | Target provides the neuroanatomical fMRI evidence (precuneus deactivation failure) that underpins the Glitchy Switch axiom. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `ADHD DMN Deactivation Failure.md` | `- [[ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag, Not Willpower Failure]] — _A related but distinct DMN dysregulation mechanism (maturational lag vs. deactivation failure)._` | New `## Related` section at the bottom. |
| `ADHD DMN Deactivation Failure.md` | `- [[MOC - ADHD Functional Neurology & Scaffolding]]` | New `## Related` section. |
| `MOC - ADHD Functional Neurology & Scaffolding.md` | Check off the consolidation task | By formalizing the `supports` edge, we've successfully linked the atom to the axiom without needing to destructively merge them. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `type` | `concept` | `claim` |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `ADHD brains fail to progressively deactivate the default mode network (specifically the precuneus) during sustained attention tasks, resulting in mind-wandering and DMN intrusion.` |
| `epistemic_status` | (missing) | `high` |
| `tags` | `[]` | `[adhd, dmn, neuroscience, attention]` |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| None | All targets successfully resolved. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
Following the enrichment pass, `ADHD DMN Deactivation Failure` has been successfully repositioned from a disconnected, poorly-typed `concept` node into a foundational, properly-typed `claim`. It now serves as the specific fMRI/neuroanatomical evidence base (precuneus deactivation failure) that `supports` the broader "Glitchy Switch" axiom.

### Exposure List
- **Dependents (Outbound load):** 1 (`The Glitchy Switch - TPN and DMN Dysregulation in ADHD` relies on this node for its anatomical proof).
- **Dependencies (Inbound load):** 0 (It acts as a root evidence node; the inbound `synthesizes` edge from `SoT - ADHD Neurology & Core Concepts` does not add dependency load).

### Threads
- **Thread 1 (Executive Function Dysregulation):** The node acts as the neuroanatomical root in the following thread:
  `ADHD DMN Deactivation Failure` (Root/Evidence)
  ↳ `supports` -> `The Glitchy Switch - TPN and DMN Dysregulation in ADHD` (Axiom)
  ↳ `supports` -> `Executive Function Challenges are Central to ADHD` (Core Claim)

### Traversal Manifest
- **Inbound:**
  - `ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag, Not Willpower Failure.md` -> [Mention]
  - `MOC - ADHD Functional Neurology & Scaffolding.md` -> [Mention] (Consolidation task now resolved).
  - `SoT - ADHD Neurology & Core Concepts.md` -> [Typed Edge: `synthesizes` from the SoT]
- **Outbound:**
  - `The Glitchy Switch - TPN and DMN Dysregulation in ADHD.md` -> [Typed Edge: `supports`]
  - `ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag, Not Willpower Failure.md` -> [Mention] Annotated link in `## Related`.
  - `MOC - ADHD Functional Neurology & Scaffolding.md` -> [Mention] Inline hub anchor.

### Patch A (Typings)
Successfully applied. Target now explicitly grounds the Glitchy Switch axiom.

### Patch B (Sever Candidates)
No severances required. The "Consolidate" task in the MoC was checked off as resolved via structural linkage instead of destructive merging, preserving the separation between low-level fMRI evidence (this node) and the high-level behavioral axiom (Glitchy Switch).

### Pathologies Found
None remaining. The node was previously an isolated `concept` orphan (outbound), but is now properly anchored in the justification graph.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.