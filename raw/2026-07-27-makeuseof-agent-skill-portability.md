---
title: Agent skills are portable across Claude, OpenClaw and Hermes runtimes
type: source
created: 2026-07-27T17:03:48+01:00
source_url: https://www.makeuseof.com/claude-openclaw-hermes-skills-deserve-in-toolkit/
source_title: "5 Claude, OpenClaw, and Hermes skills that deserve to be in your toolkit"
source_outlet: MakeUseOf
captured_from: '[[HEAD 5 Claude, OpenClaw, and Hermes skills that deserve to be in your toolkit]]'
corroboration: low
tags: [raw, source, domain/llm, topic/agent-skills, agent-ingested]
permalink: llmeon/raw/2026-07-27-makeuseof-agent-skill-portability
---

## Provenance & trust

**Corroboration: LOW.** Consumer-tech listicle with affiliate-style framing and heavy internal cross-linking. Product recommendations are not corroborated and are **not** extracted below. Only the two structural observations are recorded, because they are checkable against the skill specification rather than resting on the outlet's judgement.

Most of this article's substance is already held in [[SoT - AI Agent Skill Architecture]] under different vocabulary — see the routing report. Recorded here for provenance, not because the source is strong.

## Extracted claims

### 1. Cross-runtime portability (the one genuinely new claim)

- Skills following the common agent-skill specification run across Claude, OpenClaw and Hermes **with only wiring differences** — the difference is which filesystem or storage path each runtime reads, not the skill logic.
- Concrete instance given: Anthropic's `document-skills` set can be installed in Claude Code via `/plugin install`, or copied folder-for-folder into the Hermes or OpenClaw skills directories. *"Since they follow the same agent skill specification, the logic just works."*
- Consequence claimed: dial a skill in once, and it is available in every runtime. Skills become the portable layer; the runtime becomes swappable.
- **Uncorroborated.** The article asserts portability but demonstrates it only for Anthropic's own document skills. Whether third-party skills port cleanly is not evidenced.

### 2. Two-stage approval as an agent write-guardrail

- The `pr-reviewer-skill` generates review files first, lets the human edit or approve them, and only then posts to GitHub.

> "Exactly the kind of guardrail you want when you're letting an agent write on your behalf."

- This is a propose-then-apply structural gate — the same shape as the vault's own `raw/proposed-claims/` stub path (AGENTS.md §2.4) and `edge_lint.py`'s propose-never-auto-edit contract.

### 3. Already held in the vault (recorded, not routed)

- "Layered content architecture so the agent only loads what it needs" — this is progressive disclosure, already documented in [[SoT - AI Agent Skill Architecture]] §2 with more precision (metadata → body → resources, with token costs).
- `skill-creator` as a meta-skill that scaffolds other skills and runs trigger-phrase evaluations — an instance of [[Recursive Agent Improvement]]. The trigger-phrase evaluation detail is a mild refinement of the "Triggering Problem" section already in the Skill Architecture SoT.
- Firecrawl → "LLM-ready markdown chunks + manifest.json" as a persistent knowledge base — an instance of [[SoT - LLM Wiki Pattern]] / [[Layered Knowledge Architecture]], not a new idea.
