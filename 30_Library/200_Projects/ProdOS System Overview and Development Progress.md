---
created: 2026-04-08T14:02:05+00:00
modified: 2026-10-22T15:11:09+00:00
permalink: llmeon/30-library/200-projects/prod-os-system-overview-and-development-progress
project_category: prodos
project_name: ProdOS
project_status: active
title: ProdOS System Overview and Development Progress
type: project
---

## ProdOS System: Overview and Development Progress

> [!warning] Superseded overview (consolidated 2026-11-09)
> The pre-v5.0 overview that stood here (the Triad framing, "Compass-over-Clock", the "Starting Mindset", `@next_action` and `@now` success indicators, the Clarity Framework commands, the five note types, and the six-stage writing pipeline) is retired. It conflicted with the current specifications. Current sources:
> - Kernel and axioms: [[SoT - PRODOS Core Specification]]
> - Entry map: [[MOC - ProdOS]]
> - Live execution set-up and Todoist taxonomy: [[gtd-action-system]]
> - Note types: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]
> - Writing pipeline: [[SoT - The Unified Writing to Think Process]]
>
> What remains below is the Assurance Layer proposal, which is not implemented and has no other home yet.

### Proposed Assurance Layer (Under Review, 2026-09-14)

A review of the ProdOS architecture (prompted by an external audit document) proposed narrowing an ambitious "agent evaluation framework" pitch into an incremental assurance layer, rather than adopting it wholesale. Not yet implemented—recorded here as the plan update the review itself recommended, pending decision on which parts to build.

> prodOS@LLMeon Assurance Loop: Durable knowledge and agent behaviour are governed through a thin, Git-tracked assurance layer. Domain routing indexes select canonical context, procedures, and restrictions; composable recipes govern repeatable reasoning; gateways control write and authority boundaries; and material corrections are classified by root cause, fixed with the smallest reviewable change, and preserved as regression cases. The system applies these controls proportionately: lightweight for capture and exploration, stronger for canonical knowledge and external action. HEAD contains trusted operational knowledge, STAGING contains validated but unpromoted candidates, and THREAD remains the low-friction space for discovery and provisional thought.

#### What it Would Add (Four Layers, Mapped onto what Already Exists)

| Layer | Already have | Proposed addition |
|:-- |:-- |:-- |
| Knowledge | Canonical notes, source records, maps, typed edges | Declare authority status and scope explicitly |
| Procedure | Prompts, workflows, CRPE, TACs | Convert recurring work into small, composable recipes |
| Assurance | Git, dry runs, structured outputs, review | Gateways, deterministic validation, a small eval suite |
| Learning | Human corrections and note refinement | Treat each significant correction as a classified issue plus a regression case |

#### Two Gateways, not a Policy Maze

- Gateway - Vault Write: required before any durable note creation/modification—explicit write authority, unambiguous target, canonical material retrieved, exact patch prepared, provenance attached, no unresolved conflict, validation attached, change reversible via Git.
- Gateway - Canonical Amendment: all of the above, plus a stated reason an amendment is preferable to a linked supporting note, dependency-impact considered, conflict handling specified, and explicit human approval before promotion from STAGING to HEAD.

#### THREAD/STAGING/HEAD Made Explicit for Agents

| State | Human meaning | Agent permission |
|:-- |:-- |:-- |
| THREAD | Exploration, capture, research, open questions | Read, propose links, create provisional analysis only if authorised |
| STAGING | Candidate knowledge or a proposed change | Create or edit drafts; run validation; never silently promote |
| HEAD | Current trusted operational knowledge | Read freely; amend only through a defined gateway and explicit approval |

#### Epistemic-status Vocabulary for Personal Models (Directly Relevant to the interest/driver Graph)

```yaml
epistemic_status: observation | interpretation | hypothesis | provisional_model | decision | archived
confidence: low | medium | high
review_after: YYYY-MM-DD
```

Distinguishes, e.g.: "practises recurve archery" (observation) → "archery supplies rapid feedback" (interpretation) → "feedback-rich activities may satisfy a drive for competence" (hypothesis). Protects against an agent converting self-reflection into an authoritative psychological conclusion—directly reinforces the existing `proposed`/`supported`/`contested`/`provisional` status discipline already in use in [[A Portable Interest and PKM Knowledge Graph]] and [[A Portable Interest and PKM Knowledge Graph — Interest Seed and Candidate Drivers]]. Also explicitly warns against treating graph centrality as a causal driver score—centrality tells you what to investigate next, not what's generative.

#### Proposed Priority order (Not yet Started)

1. This week: `Gateway - Vault Write`, `Gateway - Canonical Knowledge Amendment`, a routing index for personal productivity/prodOS, an `agent-evals/README.md` with five starter regression cases (canonical-target selection, no-implicit-write, conflict-preservation, minimal-patch, interest-driver epistemic-status).
2. Next fortnight: define the exact THREAD → STAGING → HEAD transition for agent-proposed content; add deterministic validation (frontmatter/schema linting, relative-link resolution, duplicate-title detection); trial on one bounded domain.
3. Later: routing index for platform engineering; evaluation replay for high-value recipes; align Hermes Gateway task orchestration to the same vocabulary.

Traces should stay lightweight—only for a canonical-note/system change, a gateway decision, an external tool request, a material correction, a failure/near-miss, or a HEAD promotion. Not a log of every conversation.
