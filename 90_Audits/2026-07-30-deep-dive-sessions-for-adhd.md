---
title: 2026-07-30-deep-dive-sessions-for-adhd
type: note
permalink: llmeon/90-audits/2026-07-30-deep-dive-sessions-for-adhd
---

## Positioning — [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (uses legacy `status` and `updated` without `prodos` object, `type: hypothesis` is not a canonical type).
Existing link count in: 2 (from `Replace -deep Focus marathons- with Repeatable Micro-pipelines` and `The Five-Item To-Do List Reduces Overwhelm`).
Existing link count out: 0.

### Search Execution
- `ADHD Behavioral Strategies for Productivity` -> [No results found / missing note]
- `Flow State` -> [`Flow State is a State of Optimal Dopamine Stimulation`, `MOC - ADHD Functional Neurology & Scaffolding`, `MOC - Project Continuity`]
- `Context Switching` -> [`Task Batching is Grouping Similar Tasks to Reduce Context Switching`, `Context Tags Enable Efficient Batching...`, `Cognitive Firewalls`]
- `Next Actions` -> [`A Next Action Must Be the Absolute Next Physical Visible Activity...`, `Protocol - Action-First GTD`]

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `Replace -deep Focus marathons- with Repeatable Micro-pipelines.md` | **Mention:** "This approach contrasts with unstructured [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]" | Yes—if structured micro-pipelines are correct, unstructured deep dives are incorrect. | No—they are direct, specific counter-proposals to each other. | Yes—validating one decreases confidence in the other. | Pass (Edge) |
| `A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward.md` | **Use:** Target hypothesizes replacing strict granular Next Actions with Deep Dive blocks for ADHD. | Yes—they offer mutually exclusive prescriptions for task size (granular vs blocked). | No. | Yes—if the candidate is universally true, the target is bad advice. | Pass (Edge) |
| `Task Batching is Grouping Similar Tasks to Reduce Context Switching.md` | **Mention:** Target uses reducing "Context Switching" as its core mechanism. | No—Deep Dive blocks are project-batching, not similar-task batching. | Yes—`Context Tags Enable Efficient Batching...` works equally well. | No. | Patch B |
| `MOC - ADHD Experiments & Protocols.md` | **Use:** Target is an active experiment testing an ADHD productivity hypothesis. | N/A | N/A | N/A | Patch B |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Deep Dive Sessions for ADHD (Adapted GTD Next Actions).md` | `[contradicts:: [[Replace -deep Focus marathons- with Repeatable Micro-pipelines]]]` | Direct contrast between unstructured 75m deep dives and structured 25-50m micro-pipelines. | Yes |
| `Deep Dive Sessions for ADHD (Adapted GTD Next Actions).md` | `[contradicts:: [[A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward]]]` | The target explicitly abandons the strict granular next action requirement in favor of blocks. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Deep Dive Sessions for ADHD (Adapted GTD Next Actions).md` | `- [[Task Batching is Grouping Similar Tasks to Reduce Context Switching]] — _Target applies the concept of reducing context switching by batching work by project rather than by task type._` | Under a new `## Related` section at the bottom of the note. |
| `Deep Dive Sessions for ADHD (Adapted GTD Next Actions).md` | `- [[MOC - ADHD Experiments & Protocols]] — _Hub for ADHD hypotheses and active experiments._` | Under a new `## Related` section at the bottom of the note. (Note: The MoC's Dataview query already captures this note dynamically). |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | (missing) | `false` |
| `non_conformance_reason` | (missing) | `"Note is an experiment protocol (type: hypothesis), which is not one of the 5 canonical types."` |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `active` |
| `status` | `active` | (Remove—replaced by `prodos.lifecycle`) |
| `updated` | `null` | (Remove) |

### Claim Stubs Written
None.

### No evidence / needs your call
| Candidate | Why untestable |
|---|---|
| `ADHD Behavioral Strategies for Productivity.md` | Note is missing/does not exist in the vault, despite being linked by inbound backlinks. |

---

## PART 3 — Thread Audit (Target Seed)

### Verdict
The note is an isolated, untested hypothesis/experiment from June 2025. Following the enrichment pass (Part 1/2), it is now structurally positioned as a competing model (contradiction) to both standard GTD granular actions and structured micro-pipelines, but it still lacks any inferential grounding (no `supports` or `depends_on` edges). It carries zero exposure in the justification graph.

### Exposure List
- **Dependents (Inbound load):** 0 (No `supports` edges point to this, and no notes `depends_on` it).
- **Dependencies (Outbound load):** 0.

### Threads
- **Thread 1 (Structural Context):** The note exists in a cluster of task management strategies for ADHD, situated in direct opposition (via `contradicts` edges) to `Replace -deep Focus marathons- with Repeatable Micro-pipelines` and `A Next Action Must Be the Absolute Next Physical Visible Activity...`. It has no inferential chain (root/tip status).

### Traversal Manifest
- **Inbound:**
  - `The Five-Item To-Do List Reduces Overwhelm.md` -> [Mention] Annotated link in `## Related`.
- **Outbound:**
  - `Replace -deep Focus marathons- with Repeatable Micro-pipelines.md` -> [Typed Edge: `contradicts`]
  - `A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward.md` -> [Typed Edge: `contradicts`]
  - `Task Batching is Grouping Similar Tasks to Reduce Context Switching.md` -> [Mention] Annotated link in `## Related`.
  - `MOC - ADHD Experiments & Protocols.md` -> [Hub Termination]

### Patch A (Typings)
None needed beyond what was applied in Part 2. All active connections are either correctly typed edges or explicitly annotated topical links.

### Patch B (Sever Candidates)
None.

### No evidence / untestable
- The Target hypothesis claims replacing Next Actions with Deep Dive blocks works better for ADHD. However, it lacks any empirical evidence or results logged in the `## 4. Results Log`.

### Pathologies Found
1. **Abandoned Experiment:** The note was created over a year ago (2025-06-25), with a 1-week duration protocol, but the results log is entirely empty. It remains `status: active` / `prodos.lifecycle: active` instead of being concluded or rejected.
2. **Epistemic Isolation:** Carries no inferential weight in the system.

### Frontier
- Run the experiment and log the results, or explicitly close it as `rejected` and archive it.

### Next Action
Review the empty Results Log for the experiment and either execute the 1-week protocol to generate evidence, or change `prodos.lifecycle` to `archived` if the experiment is no longer relevant.