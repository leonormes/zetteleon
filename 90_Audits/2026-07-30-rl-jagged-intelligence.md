---
title: 2026-07-30-rl-jagged-intelligence
type: note
permalink: llmeon/90-audits/2026-07-30-rl-jagged-intelligence
---

## Positioning — [[Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains]] — 2026-07-30

### Baseline
Thin—frontmatter non-conformant (uses `type: claim`, but `conformant: false` and missing `prodos` block and `proposition`).
Existing link count in: 2 (from `Lenient Harness Parsing...` via `depends_on`, and an index report).
Existing link count out: 3 (one `supports` edge to `Agentic Autonomy Accelerates...`, plus two annotated mentions).

### Search Execution
- `AI and Machine Understanding` -> [Direct candidate via explicit outbound `extends` annotation].
- `SoT - AI Sycophancy` -> [Direct candidate via explicit outbound `extends` annotation].

### Candidate Connections
| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| `AI and Machine Understanding.md` | **Use:** Target's jaggedness mechanism explicitly supports the candidate's claim that models fail to achieve unified human-like understanding. | Yes—if RL improved uniformly, the gap in machine understanding would vanish. | No. | Yes—mechanistic proof. | Pass (Edge: Target `supports` Candidate) |
| `SoT - AI Sycophancy.md` | **Use:** Target explains the root cause (RL's failure on subjective feedback) of the sycophancy failure mode described in the SoT. | Yes—if RL worked perfectly on subjective metrics, it wouldn't default to approval-seeking heuristics. | No. | Yes—mechanistic proof of the SoT's core thesis. | Pass (Edge: Target `supports` Candidate) |

### Patch A — Typed Edges to Write (six-word vocabulary only)
| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| `Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains.md` | `[supports:: [[AI and Machine Understanding]]]` | Target provides the mechanistic explanation for the limitations discussed in the candidate. | Yes |
| `Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains.md` | `[supports:: [[SoT - AI Sycophancy]]]` | Target details the exact RL constraint that causes models to default to sycophancy in subjective tasks. | Yes |

### Patch B — Plain Links / MoC Anchors (Leon applies)
| File | Proposed line | Where it goes |
|---|---|---|
| `Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains.md` | Remove the manual `extends:` prefixes from the `## Related` section and leave the prose context, as the typed edges now structurally define the relationship. | `## Related` section. |

### Patch C — Frontmatter Conformance (Leon applies)
| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred..."` | (Remove) |
| `prodos.kind` | (missing) | `atomic` |
| `prodos.lifecycle` | (missing) | `stable` |
| `proposition` | (missing) | `Reinforcement Learning produces jagged intelligence, excelling in domains with verifiable success signals (like code) while stalling in subjective domains (like humor or writing).` |
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
Following the enrichment pass, `Reinforcement Learning Produces Jagged Intelligence...` has been transformed from an under-structured claim into a high-exposure nexus node. It acts as the core mechanistic explanation linking low-level tool failures (lenient parsing) to high-level cognitive, alignment, and autonomy outcomes.

### Exposure List
- **Dependents (Total load = 4):** 
  - `Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable` (Outbound `supports`)
  - `AI and Machine Understanding` (Outbound `supports`)
  - `SoT - AI Sycophancy` (Outbound `supports`)
  - `Lenient Harness Parsing Removes the Negative-Reinforcement Signal...` (Inbound `depends_on` pointing to Target)
- **Dependencies:** 0 (Target acts as an independent root mechanism).

### Threads
Target acts as a central hub branching into three distinct consequence threads:
- **Thread 1 (Autonomy & Tool Use Limits):**
  `Lenient Harness Parsing...`
  ↳ `depends_on` -> `Reinforcement Learning Produces Jagged Intelligence...`
  ↳ `supports` -> `Agentic Autonomy Accelerates...`
- **Thread 2 (Cognitive Limits):**
  `Reinforcement Learning Produces Jagged Intelligence...`
  ↳ `supports` -> `AI and Machine Understanding`
- **Thread 3 (Alignment Failure):**
  `Reinforcement Learning Produces Jagged Intelligence...`
  ↳ `supports` -> `SoT - AI Sycophancy`

### Traversal Manifest
- **Inbound:**
  - `Lenient Harness Parsing...` -> [Typed Edge: `depends_on` from Candidate to Target]
  - `_link_report_karpathy_interview.md` -> [Mention / Ignored Index]
- **Outbound:**
  - `Agentic Autonomy Accelerates...` -> [Typed Edge: `supports`]
  - `AI and Machine Understanding.md` -> [Typed Edge: `supports`] (Converted from plain link)
  - `SoT - AI Sycophancy.md` -> [Typed Edge: `supports`] (Converted from plain link)

### Patch A (Typings)
Successfully applied. The unstructured `extends` annotations have been formalised into structural `supports` edges.

### Patch B (Sever Candidates / Mergers)
No severances required. Link prose was preserved in `## Related` while the manual relationship tags were dropped in favour of the typed edges.

### Pathologies Found
- **Under-structured Hub:** The note had high intellectual load (explaining multiple failure modes) but weak structural encoding. It is now correctly mapped as a nexus.

### Frontier
- Structurally sound. No further action needed.

### Next Action
Mark audit as complete and move to the next target.