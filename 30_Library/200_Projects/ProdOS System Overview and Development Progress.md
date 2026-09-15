---
created: 2026-04-08T14:02:05+00:00
modified: 2026-08-29T09:36:21+00:00
permalink: llmeon/30-library/200-projects/prod-os-system-overview-and-development-progress
project_category: prodos
project_name: ProdOS
project_status: active
title: ProdOS System Overview and Development Progress
type: null
---

## ProdOS System: Overview and Development Progress

ProdOS (Productivity Operating System) is a tool-agnostic, AI-driven system designed to enable stress-free productivity and a "Mind Like Water" state. It integrates principles from the Getting Things Done (GTD) methodology with an ADHD-optimised framework, acting as a sophisticated productivity assistant.

### Core Philosophy and Architecture: The Triad

ProdOS has been streamlined to a core Triad that eliminates infrastructure bloat and focuses on cognitive throughput:

1. Action Engine (Todoist): The repository for all physical, verifiable actions and projects.
2. Knowledge Base (Obsidian): A proposition-centred Zettelkasten for "Computed Truth" and long-term synthesis.
3. AI Chief of Staff (CoS): The reasoning layer that manages context, refines raw input, and maintains system integrity.

The system operates on two fundamental dynamics: Control (Horizontal Management) and Perspective (Vertical Alignment). It transforms AI from a simple tool into a trusted thought partner by enforcing your standards, perspective, and processes. The system embraces a "Capture Now, Structure Later" philosophy to minimise friction during capture and defer detailed organisation to a structured "Clarify" process.

### ADHD-Aware Productivity Strategies

ProdOS is fundamentally designed to be an ADHD-optimised framework, addressing core challenges like task initiation paralysis, executive dysfunction, and dopamine dysregulation.

- Compass-over-Clock Paradigm: Prioritising values and purpose over mere urgency addiction.
- Low Activation Energy: Employing "starter tasks" (<5 min actions) and the "Starting Mindset" (e.g., "work for 15-30 minutes") to overcome inertia.
- Energy Management: Matching tasks to current energy levels and optimal work windows.
- Time-Boxing and Theming: Structured work periods to maintain focus and engagement.
- Success Indicators: Aiming for zero inboxes, every project having a `@next_action`, and a single focus at `@now`.

### The Clarity Framework

The Clarity Framework employs a problem-first approach to strategic prioritisation, ensuring that every project is rooted in a well-defined tension rather than a vague desire.

- Process: Capture problems, analyse them systematically (using Socratic questioning and impact scoring), identify force multipliers, and convert high-impact problems into actionable projects.
- Execution: Problem → Clarity Analysis → GTD Project → Next Actions → AI-Assisted Execution.

### Knowledge Protocol: Proposition-Centred Thinking

ProdOS moves away from generic "topic buckets" to a system of "Computed Truth." The Knowledge Base is structured around five specific note types:

- Claim: A verifiable proposition or belief.
- Concept: A definition or distinction needed for thought.
- Evidence: Grounding for claims (quotes, data, benchmarks).
- Question: An unresolved tension or uncertainty.
- Procedure: Repeatable, binary "know-how" (Protocols).

### The Writing to Think Pipeline

The system enforces a high-fidelity pipeline for moving from raw thought to stable knowledge:

1. Stage 1: Generate (Goldberg Layer): 10-minute raw timed writing to outrun the internal censor.
2. Stage 2: Clarify (Zinsser Layer): Ruthless editing for clarity and strength.
3. Stage 3: Understand (Writing to Learn): Active reflection to discover the "Computed Truth."
4. Stage 4: Connect (Zettelkasten Layer): Deliberate linking to existing knowledge.
5. Stage 5: Synthesise (Outcome Layer): Building structure notes and larger arguments.

### Future Outlook

ProdOS continues to evolve with a focus on:

- Automated background synthesisation.
- Advanced AI decision support based on energy levels.
- Mobile accessibility for frictionless capture.

ProdOS is a continuously evolving system designed to provide a seamless, strategic, and ADHD-optimised productivity experience.


### Proposed Assurance Layer (Under Review, 2026-09-14)

A review of the ProdOS architecture (prompted by an external audit document) proposed narrowing an ambitious "agent evaluation framework" pitch into an incremental assurance layer, rather than adopting it wholesale. Not yet implemented — recorded here as the plan update the review itself recommended, pending decision on which parts to build.

> **prodOS@LLMeon Assurance Loop:** Durable knowledge and agent behaviour are governed through a thin, Git-tracked assurance layer. Domain routing indexes select canonical context, procedures, and restrictions; composable recipes govern repeatable reasoning; gateways control write and authority boundaries; and material corrections are classified by root cause, fixed with the smallest reviewable change, and preserved as regression cases. The system applies these controls proportionately: lightweight for capture and exploration, stronger for canonical knowledge and external action. HEAD contains trusted operational knowledge, STAGING contains validated but unpromoted candidates, and THREAD remains the low-friction space for discovery and provisional thought.

#### What it would add (four layers, mapped onto what already exists)

| Layer | Already have | Proposed addition |
|:-- |:-- |:-- |
| Knowledge | Canonical notes, source records, maps, typed edges | Declare authority status and scope explicitly |
| Procedure | Prompts, workflows, CRPE, TACs | Convert recurring work into small, composable recipes |
| Assurance | Git, dry runs, structured outputs, review | Gateways, deterministic validation, a small eval suite |
| Learning | Human corrections and note refinement | Treat each significant correction as a classified issue plus a regression case |

#### Two gateways, not a policy maze

- **Gateway - Vault Write**: required before any durable note creation/modification — explicit write authority, unambiguous target, canonical material retrieved, exact patch prepared, provenance attached, no unresolved conflict, validation attached, change reversible via Git.
- **Gateway - Canonical Amendment**: all of the above, plus a stated reason an amendment is preferable to a linked supporting note, dependency-impact considered, conflict handling specified, and explicit human approval before promotion from STAGING to HEAD.

#### THREAD/STAGING/HEAD made explicit for agents

| State | Human meaning | Agent permission |
|:-- |:-- |:-- |
| THREAD | Exploration, capture, research, open questions | Read, propose links, create provisional analysis only if authorised |
| STAGING | Candidate knowledge or a proposed change | Create or edit drafts; run validation; never silently promote |
| HEAD | Current trusted operational knowledge | Read freely; amend only through a defined gateway and explicit approval |

#### Epistemic-status vocabulary for personal models (directly relevant to the interest/driver graph)

```yaml
epistemic_status: observation | interpretation | hypothesis | provisional_model | decision | archived
confidence: low | medium | high
review_after: YYYY-MM-DD
```

Distinguishes, e.g.: "practises recurve archery" (observation) → "archery supplies rapid feedback" (interpretation) → "feedback-rich activities may satisfy a drive for competence" (hypothesis). Protects against an agent converting self-reflection into an authoritative psychological conclusion — directly reinforces the existing `proposed`/`supported`/`contested`/`provisional` status discipline already in use in [[A Portable Interest and PKM Knowledge Graph]] and [[A Portable Interest and PKM Knowledge Graph — Interest Seed and Candidate Drivers]]. Also explicitly warns against treating graph centrality as a causal driver score — centrality tells you what to investigate next, not what's generative.

#### Proposed priority order (not yet started)

1. **This week**: `Gateway - Vault Write`, `Gateway - Canonical Knowledge Amendment`, a routing index for personal productivity/prodOS, an `agent-evals/README.md` with five starter regression cases (canonical-target selection, no-implicit-write, conflict-preservation, minimal-patch, interest-driver epistemic-status).
2. **Next fortnight**: define the exact THREAD → STAGING → HEAD transition for agent-proposed content; add deterministic validation (frontmatter/schema linting, relative-link resolution, duplicate-title detection); trial on one bounded domain.
3. **Later**: routing index for platform engineering; evaluation replay for high-value recipes; align Hermes Gateway task orchestration to the same vocabulary.

Traces should stay lightweight — only for a canonical-note/system change, a gateway decision, an external tool request, a material correction, a failure/near-miss, or a HEAD promotion. Not a log of every conversation.