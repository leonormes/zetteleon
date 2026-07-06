---
created: 2026-05-29T06:39:00+00:00
modified: 2026-07-04T10:49:48+00:00
permalink: llmeon/raw/2026-05-28-pieces-hermes-config-validation
pieces_ids: [2c964efb-aca8-44ae-80f6-9a9517445ed2, 7b9e7648-7660-4547-82ee-f829cf6a68f1, 86bf2b5e-a70f-41d1-9472-b0a05b8987e7, d7a00c51-b046-4deb-b3a1-cfa991a5a526, e987359e-137c-41e4-9d84-e9b63f7cddd5, eae1f61b-3629-41a3-aba3-3941884f97d1]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-28-pieces-hermes-config-validation
---

## Asset 1—User Request (Pieces: 2c964efb-aca8-44ae-80f6-9a9517445ed2)

Captured: 2026-05-28T14:09:02.610798Z

The user shared Cursor's report on Hermes config changes and asked for validation:

> "I have updated hermes. this is the report cursor gave me."

### Cursor's Config Changes Applied (2026-05-28)

| File | Change | Status (this validation) |
|------|--------|--------------------------|
| `private_dot_hermes/private_config.yaml` | `approvals.mode: smart` (was `manual`) | ✅ |
| | `delegation.inherit_mcp_toolsets: false` | ✅ |
| | `delegation.toolsets: [file]` | ✅ |
| | `delegation.max_iterations: 20` | ✅ |
| | `delegation.child_timeout_seconds: 120` | ✅ |
| | `delegation.reasoning_effort: high` | ✅ |
| | `mcp_servers.mcp-proxy.tools.exclude: []` | ✅ |
| | `mcp_servers.pieces.tools.include: [ask_pieces_ltm, search_pieces, save_to_pieces]` | ✅ |
| | Model Roles comment block (`free_main = owl-alpha / paid_reason = claude-sonnet-4-6`) | ✅ |
| `skills/route-task.md` | "Infra / Debugging Protocol" section added | ✅ |
| | Extra Tier-2 infra/debug bullet (use `delegate_task`, not `claude --print`) | ✅ |
| `skills/premium/claude-code.md` | "When NOT to use" section (infra → `delegate_task`) | ✅ |
| `skills/custom/infra/argocd-unstick.md` | New: 7-step mechanical playbook | ✅ |
| `skills/custom/infra/crashloop-triage.md` | New: CrashLoopBackOff diagnostic bundle | ✅ (exists) |
| `skills/custom/infra/helm-validate.md` | New: Helm template validation | ✅ (exists) |
| `skills/custom/infra/loki-label-audit.md` | New: Loki stream label audit | ✅ (exists) |
| `assets/context/cost-routing-pilot.md` | Phase A (free-only) + Phase B (bounded paid) | ✅ |

Note: `delegation.model` is `anthropic/claude-sonnet-4-6` via OpenRouter—requires OpenRouter credits for paid Reason agent calls.

## Asset 2—Validation Report Detail (Pieces: e987359e-137c-41e4-9d84-e9b63f7cddd5)

Captured: 2026-05-28T14:13:07.719396Z

Full validation produced by Hermes reading all modified files and confirming each change against expected values. All items passed. The validation included a 7-step test plan:

1. Routing smoke test—`/skill route-task` should trigger Tier 1.5 free model
2. `approvals.mode: smart`—low-risk file writes should not prompt `[y/n]`
3. Pieces MCP tool filter—only 3 whitelisted pieces tools exposed
4. Infra playbook Phase A—known pattern (`argocd-unstick`) executed by free owl-alpha, zero paid calls
5. Infra protocol Phase B—ambiguous symptom triggers `delegate_task` with suitcase schema, `toolsets: [file]` only
6. Delegation lockdown guard—child agent with `toolsets: [file]` should NOT be able to run terminal commands
7. Phase A pilot—full free-only session for both coding and infra tasks

## Asset 3—Context Gathering (Pieces: d7a00c51-b046-4deb-b3a1-cfa991a5a526)

Captured: 2026-05-28T14:11:54.499533Z

Additional file reads to complete validation—route-task.md remainder, all infra skill files confirmed present.

## Asset 4—Agent Working Notes (Pieces: 7b9e7648-7660-4547-82ee-f829cf6a68f1)

Captured: 2026-05-28T14:09:10.563345Z

Initial memory search for Hermes config context before validation.
