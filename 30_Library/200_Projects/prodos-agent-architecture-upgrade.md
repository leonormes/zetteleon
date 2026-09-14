---
created: 2026-09-14T00:00:00+00:00
modified: 2026-09-14T00:00:00+00:00
permalink: llmeon/30-library/200-projects/prodos-agent-architecture-upgrade
project_name: ProdOS Agent Architecture Upgrade
project_category: prodos
project_status: active
prodos:
  kind: project
  lifecycle: stable
  trust: working
related: ["[[AGENTS.md]]", "[[00 - Prompt Library Router]]", "[[SoT - Agentic AI Design Patterns]]", "[[SoT - AI Agent Skill Architecture]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[Protocol - Diagnose an Agent Failure]]", "[[how does this fit with my prodOS@LLMeon protocol?]]"]
tags: [domain/pkm, prodos/project, topic/agent-architecture, topic/knowledge-architecture]
title: prodos-agent-architecture-upgrade
type: project
conformant: true
---

> Upgrading ProdOS's agent-governance stack (knowledge, reasoning, evaluation, self-improvement) toward the four-layer pattern described in Meta's "organizational agents" work, without breaking anything the vault already does well. Live worklist tracked in Todoist project **"ProdOS — Agent Architecture Upgrade"**; this note is the durable spec. **Any LLM picking this up: read this note in full, then check the Todoist project for current task status before doing anything.**
>
> **Status as of 2026-09-14: core upgrade complete.** All 5 original Work Remaining items are done — see Outcome & Successes below and the "Future Work" section for what's deliberately left open.

## Purpose

On 2026-09-14, a comparison was run between:

1. This vault's actual agent-governance config (`AGENTS.md`, `10_System/prompts/`, the TAC notes, `edge_lint.py`),
2. An [InfoQ write-up](https://www.infoq.com/news/2026/09/meta-organizational-agents/) of Meta's internal "organizational agents" architecture — four layers: **knowledge system** (versioned position files + routing/gateway indexes), **reasoning pipeline** (named "recipes," separate from the knowledge they load), **evaluation framework** (automated benchmarks catching drift), and **self-improvement loop** (expert corrections → minimal verified edits → regression-tested → deployed), and
3. A prior, more elaborate "prodOSLLMeon — Vault Knowledge Agent" system prompt that was governing that session — which turned out to already be a near-exact attempt at implementing the Meta four-layer pattern for this vault.

**Provenance, resolved 2026-09-14:** that persona prompt is not vault config at all. It's Perplexity's answer to Leon's own two prompts, captured verbatim in `00_Inbox/how does this fit with my prodOS@LLMeon protocol?.md` — first "how does this fit with my prodOS@LLMeon protocol?" (which produced the Meta-vs-prodOSLLMeon comparison table this whole project is built on), then "give me a full context prompt for my local llm that has access to my vault" (which produced the persona prompt itself, with a suggested save path of `10_System/prompts/prodOSLLMeon Vault Knowledge Agent.md` that was never acted on). Leon pasted that draft into a session as an experiment; it was never adopted into the vault's actual prompt library or reconciled with `AGENTS.md`. Per `AGENTS.md` §0, `00_Inbox/` is a capture entry point, not settled knowledge — this draft has been sitting there untriaged.

This project exists to close the gap between what ProdOS's agent architecture currently *is* and what that comparison showed it's *missing* — and to decide whether/how to formally adopt parts of this draft (see Open Decisions).

## Principles

- **Reuse before building.** `edge_lint.py` is already a working, deterministic validator — the closest thing the vault has to Meta's "automated benchmark" layer. Extend it before writing a parallel eval tool.
- **Smallest safe change, phased.** No big-bang restructure of `AGENTS.md` or the prompt library. Each phase lands as an independent, reviewable change (per the vault's own "Plan a vault change" recipe).
- **Corrections become artefacts, not conversation exhaust.** Right now a correction to agent behaviour lives only in ephemeral session memory. The self-improvement loop this project builds must turn a correction into a stored, regression-tested case tied to the failure it prevents — mirroring Meta's "minimal verified edits."
- **Don't resolve governance conflicts unilaterally.** Where a change would touch permissions, write-gateways, or which document is authoritative, stop and get Leon's decision — don't pick a side and proceed.
- **Root-cause every failure before patching.** Classify a bad output as missing knowledge vs. flawed reasoning vs. genuine ambiguity before editing a prompt in response to it (this taxonomy already exists in the draft persona's "Recipe: Diagnose a failure" — promoting it to a real Protocol note is part of this project).

## Outcome & Successes So Far

**Audit completed 2026-09-14.** Findings:

- ProdOS already has strong, working analogues for 3 of Meta's 4 layers:
  - **Knowledge system** ↔ `AGENTS.md` + `30_Library/SoT/` + `MoC/` taxonomy — solid.
  - **Reasoning pipeline** ↔ `10_System/prompts/` (37 task-specific prompts) + `00 - Prompt Library Router.md` as the gateway/routing index — this is the **strongest existing match** to the Meta pattern; nothing needed here beyond what §"Work Remaining" below lists.
  - **Evaluation framework** ↔ partial. TAC (`SoT - Typed Answer Contract (TAC) for LLM Output`, `Protocol - Typed Answer Contract (TAC) for Vault Agents`) enforces per-response discipline (confidence, evidence, uncertainty-flag), and `edge_lint.py --audit` is a real deterministic structural validator. Neither accumulates into a benchmark that tracks drift over time.
- **Self-improvement loop confirmed absent.** Vault-wide grep for `failure_mode_prevented`, `regression case`, `eval_case` returned zero hits. `SoT - Agentic AI Design Patterns` §2E *names* this pattern as desirable but nothing operationalises it.
- **Skills packaging confirmed unused.** `SoT - AI Agent Skill Architecture` documents the Claude Code Skills pattern (`.claude/skills/`, progressive disclosure) in detail, but `.claude/` in this vault contains only `settings.local.json` (a permissions allowlist) — no `skills/` folder. The prompt-library-router pattern is doing this job instead.
- **Draft-vs-canon conflict identified, provenance now resolved** (see Open Decisions) — the draft persona's write-gateway model (default read-only, 10-condition write gate) contradicts `AGENTS.md`'s explicit full-read-write stance, and `AGENTS.md`'s own claim ("no external spec supersedes this file"). The prompt is just an untriaged Inbox capture, not a competing authority — but Leon has been pasting it into sessions as if it were one, so the vault's real behaviour and its nominal governance have drifted apart in practice. Still needs a human decision (see below), just not an urgent "unknown spec overriding the vault" one.

Full writeup of this audit lives in the conversation that produced this note (2026-09-14 session); the findings above are the durable summary. This note + the Todoist project are now the canonical continuation point — don't re-run the audit from scratch, extend from here.

## Decisions Made

1. **Resolved 2026-09-14 by Leon: keep `AGENTS.md`'s existing full-read-write stance; the draft persona's write-gateway is retired, not adopted.** `00_Inbox/how does this fit with my prodOS@LLMeon protocol?.md` stays in the Inbox as source material for the eval-case and failure-diagnosis work below — not as a competing authority. Vault behaviour and nominal governance no longer disagree.

## Work Remaining — all 5 items done (2026-09-14)

Also tracked in the Todoist project **"ProdOS — Agent Architecture Upgrade"** (all 5 tasks now complete/decided there).

1. ~~Resolve the Open Decision.~~ Done — see Decisions Made above.
2. ~~Build an eval-case store.~~ Done — `10_System/evals/` created, with a two-tier model: `structural/` (self-contained fixture cases, machine-run) and `behavioral/` (documented judgment cases, human-reviewed). Seeded with 3 structural cases (dangling-edge, unknown-relationship, bare-resolved-target — each protecting a real invariant already in `edge_lint.py`) and 2 behavioral cases drawn from *this project's own history*: `behav-001` (the Inbox-authority confusion this project's provenance investigation actually hit) and `behav-002` (the correct escalate-don't-resolve pattern, kept as a positive case to protect). See `10_System/evals/README.md`.
3. ~~Add `--regress` to `edge_lint.py`.~~ Done and verified both ways — it passes all 3 seed cases, and correctly fails (exit 1, reports the missing expectation) against a deliberately-wrong case used to sanity-check the harness itself. Run: `uv run --with pyyaml python3 10_System/scripts/edge_lint.py --regress`.
4. ~~Promote the failure-diagnosis taxonomy.~~ Done — [[Protocol - Diagnose an Agent Failure]], linked from the Router. Points at both new behavioral cases as worked examples of two of its root-cause categories.
5. ~~Decide on Skills adoption.~~ Done — decided **not** to migrate to `.claude/skills/`; documented why in `SoT - AI Agent Skill Architecture` §"Decision: Router Pattern Over Native Skills". The router already does the useful half of progressive disclosure, and Skills solve distribution/autonomous-triggering problems this single-person vault doesn't have.

**Bonus finding, fixed in passing:** while reading `edge_lint.py`'s sibling script, found that `10_System/scripts/validate_note_frontmatter.py` — which `SoT - ProdOS Frontmatter Contract` §9 claimed (as of 2026-07-17) did not exist — actually does exist and is fully runnable, just at a different path (`10_System/scripts/`, not the `gemini-scribe/scripts/` the SoT named). Corrected §9 and the matching "Tensions & Gaps" entry in that SoT. It doesn't have a `--regress` mode yet — flagged as future work below, not built in this pass.

## Future Work (not blocking, not currently tracked in Todoist)

- Wire `edge_lint.py --regress` (and eventually `validate_note_frontmatter.py`) into CI or a pre-commit hook — nothing runs the regression suite automatically yet.
- Give `validate_note_frontmatter.py` its own case-based regression mode, mirroring what `edge_lint.py --regress` now does.
- An actual LLM-judge harness for `behavioral/` cases — right now they're a human-readable checklist, not machine-graded. `behav-001`/`behav-002` would be reasonable first cases to try it against.
- If Leon wants any of these tracked as live work, add them to the Todoist project explicitly — they're recorded here as options, not commitments.

## Context Pointers (for a cold-start agent)

- `AGENTS.md` (vault root) — authoritative agent rulebook.
- `10_System/prompts/00 - Prompt Library Router.md` — routing index for all task prompts.
- `30_Library/SoT/SoT - Agentic AI Design Patterns.md` — names the pattern taxonomy this project is closing gaps against.
- `30_Library/SoT/SoT - AI Agent Skill Architecture.md` — Skills theory, relevant to Work Remaining #5.
- `30_Library/SoT/SoT - PRODOS Core Specification.md` — the *human productivity* ProdOS kernel (PINCH model, MVA) — a related but distinct system from the agent-governance ProdOS this project upgrades. Don't conflate the two.
- `30_Library/SoT/SoT - ProdOS Frontmatter Contract (Note Type Schemas).md` — frontmatter schema this note itself follows.
- `10_System/scripts/edge_lint.py` — the vault's deterministic graph validator; now also runs `10_System/evals/structural/` via `--regress`.
- `10_System/scripts/validate_note_frontmatter.py` — the vault's deterministic frontmatter validator (existence was stale in the SoT contract; corrected 2026-09-14). No `--regress` mode yet.
- `10_System/evals/README.md` — the eval/regression corpus this project built: structural (machine-run) vs behavioral (documented) cases, and their honest limits.
- `30_Library/SoT/Protocol - Diagnose an Agent Failure.md` — the promoted root-cause taxonomy; use it before making any corrective change to a prompt, note, or script.
- `00_Inbox/how does this fit with my prodOS@LLMeon protocol?.md` — the Perplexity-generated source of the draft persona prompt. Stays in the Inbox as source material (see Decisions Made) — not adopted, not deleted.
- Source article: https://www.infoq.com/news/2026/09/meta-organizational-agents/

## Tensions & Gaps

- `SoT - ProdOS Frontmatter Contract` §1 says `type` is strictly required top-level; `AGENTS.md` §0 says new notes should avoid the legacy `type` key in favour of `prodos.kind`. This note carries both, deliberately, pending that contract's own cleanup — not a decision made by this project.
- `validate_note_frontmatter.py` has no regression-case mode; `edge_lint.py` does. Asymmetric on purpose (scope), not an oversight — see Future Work.