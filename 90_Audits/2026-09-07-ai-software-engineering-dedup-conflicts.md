---
tags:
- agent/refresher
- domain/llm
- topic/knowledge-graph
title: 2026-09-07-ai-software-engineering-dedup-conflicts
type: note
permalink: llmeon/90-audits/2026-09-07-ai-software-engineering-dedup-conflicts
---

## Redundancy, Conflict & Currency Audit — MOC - AI Software Engineering — 2026-09-07

> Scope: the cluster rooted at [[MOC - AI Software Engineering]] — ~34 notes spanning the "Cognitive Bridge" family (Macro-Micro Unification, Parochial Code, Dimensions of Code Understanding, Structural Intelligence, Temporal Projection, Atomicity and Loose Coupling, The Architectural Guardian), the Context Rot/Engineering/Engine trio, the Anthropomorphism/Human-vs-AI-Cognition pair, the Human-3.0 task-taxonomy family, Flow Engineering, and the LLM Wiki Pattern family. Tooling: Obsidian MCP for reads/writes, `edge_lint.py` for validation, filesystem grep for cluster-wide tag/link surveys (fast pre-filter, never used as a substitute for reading the actual note before editing it).

### Headline finding: redundancy was the wrong hypothesis

Three separate name-collision candidates were investigated in full before touching anything, on the assumption that similar titles meant duplicate content:

1. **[[SoT - Context Rot]] vs [[SoT - Context Engineering]] vs [[SoT - The Context Engine]]** — read in full. Not duplicates: a genuine three-tier hierarchy — Context Rot (the problem/failure mode) → Context Engineering (the discipline that addresses it) → The Context Engine (a concrete, versioned implementation that `implements` the discipline). Already correctly typed-edged to each other. **No merge.**
2. **The Macro-Micro/Structural-Intelligence family** (7 SoTs) — read in full. Each owns a genuinely distinct layer: the cognitive theory, the resulting anti-pattern, the evaluation framework, the retrieval mechanism, the future-cost metric, the PKM-atom analogue, and the operational prompt. **No merge.**
3. **The LLM Wiki Pattern's four satellite atoms** (LLM Wiki Concept, Layered Knowledge Architecture, Knowledge Linting, Multi-Page Ingestion Impact) — read in full. Each is a distinct atomic facet of one source (definition, structure, one of two core operations, the other core operation) — correct atomic decomposition, not fragmentation. **No merge.**

Conclusion: this cluster's authors already did the deduplication work at write-time. The actual problem was different — see below.

### What was actually wrong: broken links and a missing bridge to the entry point

Six dangling wikilinks were found by verifying every suspicious target actually resolves (per TAC discipline — a note asserted missing must be *confirmed* absent, not assumed):

| File | Was | Fixed to | Verified |
|---|---|---|---|
| [[SoT - Context Rot]] | `[[Context Engineering]]` | `[[SoT - Context Engineering]]` | resolves |
| [[SoT - LLM Codebase Understanding & Hierarchy]] | `[[SoT - Complexity Conservation]]` | `[[SoT - Conservation of Complexity]]` | resolves |
| [[SoT - Macro-Micro Unification]] | `[[Context Engineering]]` (body) | `[[SoT - Context Engineering]]` | resolves |
| [[SoT - Macro-Micro Unification]] | `[[Context Rot]]` (See Also) | `[[SoT - Context Rot]]` | resolves |
| [[SoT - Dimensions of Code Understanding]] | `[[Separation of Concerns]]` | `[[SoT - Atomicity and Loose Coupling\|Separation of Concerns]]` | resolves (matches the exact pattern [[SoT - Parochial Code]] already uses) |
| [[SoT - LLM Codebase Understanding & Hierarchy]] | tag `type/SoT` | `type/sot` | casing fix, matches vault convention |

Two more dangling links were found and **left unresolved rather than guessed**, because no valid target exists and forcing one would be worse than an honest gap:

- [[SoT - Macro-Micro Unification]]: `[[Cognitive Load Theory]]` — no matching note. A note titled [[Cognitive Load]] exists but is about ADHD/personal-productivity working memory, a different domain; redirecting to it would create a false link. Flagged in-note with an explicit callout instead. **Your call**: author a software-engineering-specific Cognitive Load Theory note, or drop the reference.
- [[SoT - Temporal Projection]]: `[[Technical Debt]]` — no matching note anywhere in the vault (checked, including near-titles like "Understanding Debt," which is a different concept). Left as-is, not flagged in-note (lower traffic section) — noting here for visibility.

**The bigger issue**: [[MOC - AI Software Engineering]] itself — the entry point — didn't link to eight notes that are core, well-developed content in its own stated themes: [[SoT - Context Rot]], [[SoT - Context Engineering]], [[SoT - The Context Engine]], [[SoT - Structural Intelligence]], [[SoT - Temporal Projection]], [[SoT - Atomicity and Loose Coupling]], [[The Architectural Guardian]], [[SoT - Human vs AI Cognition]]. The MOC's "Context Rot" and "Perspective Drift" subsections were prose-only with zero wikilinks to the SoTs that actually define those terms. Fixed: the "Core Engineering Concepts" section now links all eight, with a one-line annotation per note explaining what it specifically contributes (not just "see also").

### Genuine duplicate found (handled by linking, not deleting)

[[Intent as High-Level Source Code]] (from a Fowler/Beck source, under [[SoT - AI-Resilient Task Taxonomy (Human 3.0)]]) and [[The Unit of Software Engineering Is Shifting from Code Lines to Intent Expressions]] (from a Karpathy source, in the Agentic AI cluster) assert the same underlying claim — engineering shifts from writing syntax to expressing intent — independently, from two different sources. This is corroboration, not noise: two independent citations for the same claim strengthen it. Rather than deleting either (each carries distinct evidence and sits in a different domain cluster with different implications — DDD/logical-precision framing vs. orchestration/agent-cluster framing), added:

```
[supports:: [[The Unit of Software Engineering Is Shifting from Code Lines to Intent Expressions]]]
```

on [[Intent as High-Level Source Code]]. Validated: 0 new gaps (the source note isn't typed `claim`, so it wasn't C1-checked either way, but the edge itself resolved and lint-passed).

### Conflict identified: not a `contradicts` edge, a live cross-MOC tension

[[SoT - LLM Semantic-Statistical Mismatch]] and [[SoT - Human vs AI Cognition]] both argue, carefully, that an LLM is a statistical predictor, not a cognitive agent — treating it as one ("the model thinks," "the model prefers") is a category error (the Anthropomorphism Trap / Eliza Effect). Meanwhile [[MOC - Agentic AI & LLM Agents]] — the sibling MOC — is built almost entirely on role/autonomy language: "a supervisor agent delegates and escalates," "the Architect enforces," "recursive agent improvement" (an agent "reviews its own logs"). This is not a factual contradiction between two specific claims — the agentic language is functional shorthand for a state machine's control flow, not a literal claim about cognition, and both MOCs would agree on that if asked directly. Per the vault's own conflict-handling convention (preserve both, record the assumption, no `contradicts` edge for a context-dependent tension), this was **documented as prose in both MOCs** rather than forced into a typed edge:

- Added a callout under "5. The Anthropomorphism Trap" in [[MOC - AI Software Engineering]] naming the Agentic AI MOC explicitly.
- Added a matching note beside [[SoT - Agentic Roles]] in [[MOC - Agentic AI & LLM Agents]]'s spine section.

This is the one item under this audit's "identify conflicts" mandate that actually qualified as a conflict rather than a naming coincidence.

### Legacy tag cleanup (consistent with the 2026-09-07 Agentic AI cluster pass)

Two notes flagged but deferred in the prior session's audit — because they weren't part of that session's 42-note "agent"-titled survey — are squarely in this cluster's territory and were normalised now:

| Note | Was | Now |
|---|---|---|
| [[Coherent LLM output signals meaningful processing]] | `[coherence, SoftwareEngineering/AI, TheHuman/Cognition]` | `[domain/llm, topic/llm-behavior, topic/anthropomorphism]` |
| [[Architecture First Approach to AI Development]] | `[ADR, Architecture, Planning, SoftwareEngineering/AI]` | `[domain/llm, topic/agent-architecture, topic/planning]` |

Confirmed via `grep -rl "SoftwareEngineering/AI" 30_Library` — zero remaining hits (the one match this grep also returns is this cluster's own report text naming the tag, not a live tag).

### Flagged for your review — not acted on (judgment calls, not mechanical fixes)

1. **[[SoT - AI-Resilient Task Taxonomy (Human 3.0)]] may be the cluster's stalest note.** Created 2025-12-24 — the oldest note in this cluster by three months — it frames human value via four broad economic/career roles (Problem Definer, Empathy Catalyst, Strategic Narrator, Craft Master) and a "Capital vs. Inspiration Economy" model. Newer notes in the Agentic AI cluster (July 2026) make much more specific, engineering-grounded claims about where humans stay load-bearing — e.g. [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]] and [[A Supervisor Agent Delegates to Repository-Specific Sub-Agents and Escalates Only Ambiguous Architectural Decisions]] (a concrete escalation criterion: ambiguous architectural decisions, not "empathy" or "narrative"). These aren't contradictory — the older note is a broader economic lens, the newer ones are a narrower engineering-workflow lens — but given you said explicitly you don't want to maintain outdated thinking on a fast-moving subject, this is the one note in the cluster I'd ask you to personally judge: still current, or ready for a `supersedes`/`superseded_by` pointer to the newer, more specific claims? I didn't touch it — this is a call about whether your own thinking has moved on, which isn't mine to make.
2. **[[Architecture First Approach to AI Development]] has two more dangling links** (`[[Architectural Decision Records ADRs for AI Agents]]`, `[[AI Agentic Workflows]]`) to notes that don't exist, and predates the atomic-claim template (no `proposition`, no `Evidence` section, legacy `id`/`status: ''`/`type: ''`/`updated: null` frontmatter). It's not orphaned — [[The Unit of Software Engineering Is Shifting from Code Lines to Intent Expressions]] already `extends` it — but it's a candidate for a rewrite into the current atomic template rather than a quick fix, which is beyond this audit's redundancy/conflict scope.
3. **Tag-scheme inconsistency across the whole ~34-note cluster.** Unlike the Agentic AI cluster (which already had a dominant `domain/llm` + `topic/agent-architecture` scheme covering most notes before any cleanup), almost every note in this older cluster (created Jan–Apr 2026, before that convention solidified) carries its own bespoke tag set — `[cognitive-science, mental-model, software-architecture, system-design]`, `[architecture, ast, graph-theory, retrieval, tooling]`, etc. — with no shared vocabulary. This is a much bigger job than the two legacy-tag fixes above (closer to 30 notes, not 2) and wasn't part of what you asked for this round, so I left it alone. Flagging it because it's the same class of problem as the Agentic cluster's tag drift, just larger, and it affects tag-based discoverability of this content.

### Validation

`edge_lint.py --path .`: 15 pre-existing errors before and after this session's edits (all unrelated — journal/project `priority::`/`due::`/`completion::`/`answers::`/`relates_to::` metadata fields from other work, none touching this cluster). 0 new errors introduced.

`edge_lint.py --audit`: 0 gaps before and after (78 bedrock, +1 from the new corroboration edge; 22 contradictions and 5 live tensions unchanged, none in this cluster; 34 cycles unchanged).

Confidence: high on the "no redundancy found" conclusion (three candidate clusters read in full, not sampled). Confidence: high on the six broken-link fixes (each target's existence was verified with `find` before and after). `UNSURE`: none — the two remaining unresolved links and the staleness call are explicitly handed back to you rather than guessed.