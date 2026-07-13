---
created: 2026-06-08T11:35:53+00:00
isProject: false
modified: 2026-07-13T08:52:22+00:00
name: Hermes daily-driver cost routing
overview: Reconfigure Hermes so a free/cheap model handles gather+mechanical tool
  loops, while Claude is only used for bounded high-value reasoning steps (escalations),
  with strong guardrails, caching, and repeatable debugging patterns for daily coding+infra
  work.
permalink: llmeon/30-library/200-projects/hermes-daily-driver-cost-routing-487849b4.plan
project_category: hermes_optimisastion
project_name: Hermes Optimisastion
project_status: active
title: hermes_daily-driver_cost_routing_487849b4.plan
todos:
- id: audit-current-hermes-config
  content: Audit `private_dot_hermes/private_config.yaml` and identify exact keys
    to change for approvals, aux models, delegation toolset restrictions, and aliases.
  status: pending
- id: implement-gather-reason-act-routing
  content: Update `private_dot_hermes/skills/route-task.md` to enforce Gather/Reason/Act
    classification and escalation to paid Claude only on defined signals.
  status: pending
- id: add-mechanical-playbooks
  content: Add 4 infra playbook skills (ArgoCD unstick, CrashLoop triage, Helm template
    validation, Loki label audit) designed for free-model execution.
  status: pending
- id: tighten-mcp-filters
  content: Add/verify MCP per-server tool allowlists/blacklists and disable unneeded
    MCP utilities to reduce prompt bloat and risk.
  status: pending
- id: pilot-and-tune
  content: Define a 2-phase trial (free-only dry run, then minimum-credit pilot) with
    success criteria and tuning knobs.
  status: pending
type: null
---

## Goal

Make Hermes a daily-driver agent for mixed coding + infra work with 3–5× lower cost by implementing your `Gather → Reason → Act` split: free model runs tool loops + executes known playbooks; paid Claude is invoked only for focused reasoning/diagnosis.

## What You Already Have (Good bAseline)

- Main model is already free-heavy: `openrouter/owl-alpha` in `[private_dot_hermes/private_config.yaml](private_dot_hermes/private_config.yaml)`.
- OpenRouter safety/routing knobs already present (`provider_routing.data_collection: deny`, `require_parameters: true`, response cache enabled).
- Delegation is already configured to a paid Claude model via OpenRouter (`delegation.model: anthropic/claude-sonnet-4-6`).
- You already have a routing skill `[private_dot_hermes/skills/route-task.md](private_dot_hermes/skills/route-task.md)` and a CLI-delegation skill `[private_dot_hermes/skills/premium/claude-code.md](private_dot_hermes/skills/premium/claude-code.md)`.

## Plan (Concrete cHanges)

### Model Routing Architecture

- Keep main model as `openrouter/owl-alpha` (free) to do:
  - terminal/file tool loops (kubectl/helm/git/gcx)
  - structured summarization of outputs
  - mechanical edits when the fix is known
  - monitoring/wait loops
- Use `delegate_task` for "Reason" steps with a paid Claude model via OpenRouter.
  - The child agent runs with no terminal access (or `file`-only) so it can't accidentally spend tokens iterating tool loops.
  - Parent passes a strict context bundle (symptoms + logs + extracted config snippets + "what I tried").
  - Child returns: root cause + exact fix steps + verification commands.
  - Parent executes those steps mechanically.

This design matches Hermes delegation semantics: subagents start with fresh context, so the parent must package a dense "suitcase" (as your existing Tier-0.5 scout pattern requires). See Hermes Delegation docs for the isolation constraint and model override behavior ([Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)).

### Encode Your Escalation Heuristics as a Hermes Skill

Add a new skill (or upgrade an existing one) that:

- Classifies each subtask as Gather / Reason / Act.
- Implements the escalation triggers from your report (unknown error, >2 failed attempts, cross-file causal chain, schema/operator understanding, confidence < 0.7).
- Enforces a hard budget policy: in Gather/Act phases, do not call paid models.

Implementation locations:

- Update `[private_dot_hermes/skills/route-task.md](private_dot_hermes/skills/route-task.md)` to include:
  - explicit "Gather/Reason/Act" classification
  - "delegate to Claude (paid)" only on escalation signals
  - a required "context suitcase" schema
- Add 2–4 playbook skills for the repeated patterns you listed (below).

### Add Playbook Skills for Repeated Infra Loops (Free Model eXecutes)

Create skills that are purely mechanical and return structured outputs, then re-run until stable:

- ArgoCD unstick (operationState phase/revision comparison, terminate op, hard refresh, wait)
- CrashLoopBackOff triage (logs + describe + recent events + minimal bundle)
- Helm render validation (extract relevant values, `helm template`, collect errors)
- Loki label/stream audit (gcx series query, label-key aggregation, missing labels report)

These become deterministic Gather/Act tools; only escalate when the error doesn't match known patterns.

### Tighten OpenRouter Governance + Caching

- Keep (and make explicit) these OpenRouter controls in config:
  - `provider_routing.data_collection: deny` and `require_parameters: true` (supported by Hermes' OpenRouter routing integration) ([Provider Routing](https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing)).
  - `openrouter.response_cache: true` + short TTL for repeated probes (already present).
- Add a small set of model aliases for:
  - `free_main` → `openrouter/owl-alpha`
  - `paid_reason` → `anthropic/claude-sonnet-4-6`
  - optional: `flash_aux` → a cheap fast model for auxiliary tasks (titles, compression, approvals)

OpenRouter also supports a `:free` model variant suffix and a Free Models Router; we'll use that only for _auxiliary_ or _very safe gather_ tasks if you want (per OpenRouter docs index: "Free Variant" and "Free Models Router" in `[OpenRouter llms index](https://openrouter.ai/docs/llms.txt)`).

### Configure Approvals to Reduce Friction Safely

- Switch `approvals.mode` from `manual` to `smart` for local CLI daily-driver use, but keep the always-on hardline blocklist.
- Assign a cheap auxiliary model for `auxiliary.approval` (Hermes recommends this pattern) so approval scoring doesn't burn Claude tokens ([Security](https://hermes-agent.nousresearch.com/docs/user-guide/security), [Configuring Models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)).

### Toolset and MCP Hygiene (Avoid Accidental sPend)

- Ensure default toolsets for the coding profile are limited to what you use daily (`terminal`, `file`, `git`, optional `web`) and keep risky toolsets disabled.
- Review MCP servers in `[private_dot_hermes/private_config.yaml](private_dot_hermes/private_config.yaml)` and:
  - add/confirm per-server `tools.include` allowlists for anything mutating
  - disable resources/prompts utilities where not needed (to reduce prompt bloat)
  - keep `supports_parallel_tool_calls` true only for safe servers

Hermes MCP filtering keys and naming conventions are in ([MCP docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)) and ([MCP Config Reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)).

## Rollout / Validation (Before Buying Many cRedits)

- Dry-run day: run Hermes with `owl-alpha` only, confirm gather loops + playbooks work; track where escalation triggers.
- Small-credit pilot: buy the minimum OpenRouter credit amount, then:
  - run 2–3 "real" mixed sessions
  - verify paid calls happen only on escalation steps
  - confirm provider routing + data collection deny is applied
- Tune thresholds: adjust escalation confidence threshold and "2 failed attempts" guardrail based on your observed failure modes.

## Files Likely to Change

- `[private_dot_hermes/private_config.yaml](private_dot_hermes/private_config.yaml)` (model slots, delegation toolsets, approvals smart mode, aux models, aliases, MCP tool filters)
- `[private_dot_hermes/skills/route-task.md](private_dot_hermes/skills/route-task.md)` (rewrite around Gather/Reason/Act and escalation)
- New skills under `[private_dot_hermes/skills/custom/](private_dot_hermes/skills/custom/)` for the 4 infra playbooks

## Notes / Constraints

- Delegation subagents don't inherit the main model fallback chain; we'll treat paid-Claude as an explicit escalation target, not a fallback. (Hermes docs: [Fallback Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers)).
- Provider routing controls which _underlying_ OpenRouter providers serve a request; it's separate from model selection and separate from Hermes fallback providers.
