---
tags: [hermes, agent-orchestration, cost-optimization, implementation, done]
date: 2026-05-28
project: hermes-agent-orchestrator
status: implemented — pending pilot
---

# Hermes Cost Routing — Implementation Complete

Cursor completed all changes from [[Hermes Cost Routing - Cursor Implementation Prompt]]. No plan file was modified.

## What Was Applied

### `private_config.yaml`
| Key | Before | After |
|---|---|---|
| `approvals.mode` | `manual` | `smart` |
| `delegation.inherit_mcp_toolsets` | `true` | `false` |
| `delegation.toolsets` | (unset) | `[file]` |
| `delegation.max_iterations` | `50` | `20` |
| `delegation.child_timeout_seconds` | `600` | `120` |
| `delegation.reasoning_effort` | (unset) | `high` |
| `mcp_servers.pieces.tools.include` | (unset) | `[ask_pieces_ltm, search_pieces, save_to_pieces]` |

### Skills Modified
- `skills/route-task.md` — Gather → Reason → Act protocol inserted; infra escalation signals; suitcase schema; playbook reference table; Tier-2 bullet updated to direct infra to `delegate_task` not `claude --print`
- `skills/premium/claude-code.md` — "When NOT to use" section added (infra → delegate_task)

### Skills Created
- `skills/custom/infra/argocd-unstick.md`
- `skills/custom/infra/crashloop-triage.md`
- `skills/custom/infra/helm-validate.md`
- `skills/custom/infra/loki-label-audit.md`

### Added by Cursor (not in original prompt)
- `assets/context/cost-routing-pilot.md` — 2-phase pilot plan (free-only dry run → minimum-credit live test) with success criteria and tuning knobs

---

## Next: Pilot Validation

### Phase 1 — Free-only dry run (before buying OpenRouter credits)
Run 2–3 real sessions using only owl-alpha. Confirm:
- [ ] Gather loops execute cleanly (kubectl/helm/gcx/git)
- [ ] Playbook pattern matching triggers correctly (no false escalations)
- [ ] ArgoCD unstick, crashloop-triage, helm-validate skills are invoked when appropriate
- [ ] Escalation signals are correctly identified and packaged into suitcase format
- [ ] `delegate_task` is NOT called during this phase (no credits needed yet)

### Phase 2 — Minimum-credit live test
Buy minimum OpenRouter credits. Run 2–3 mixed infra+coding sessions. Verify:
- [ ] Paid `delegate_task` calls happen only on genuine escalation steps
- [ ] Each delegation call is bounded to ≤120s and uses `toolsets: [file]` only
- [ ] Root cause returned by Reason agent is actionable (Act phase succeeds)
- [ ] `provider_routing.data_collection: deny` is confirmed active (check OpenRouter dashboard)
- [ ] Total paid calls per session ≤ 10

### Tuning knobs (from `cost-routing-pilot.md`)
- Escalation confidence threshold (currently 0.7) — lower if too many false escalations
- "2 failed attempts" guardrail — adjust based on observed failure modes
- `delegation.max_iterations: 20` — increase if Reason agent hits limit before answering

---

## Key Design Decisions Recorded

**Why `delegate_task` not `claude --print` for infra Reason phase:**
`delegate_task` enforces the `toolsets: [file]` restriction, caps iterations at 20, and times out at 120s. `claude --print` uses the local Claude Code CLI which has its own session and no such guardrails.

**Why `inherit_mcp_toolsets: false`:**
MCP tools (Pieces, mcp-proxy) add significant prompt bloat and risk accidental mutations in child agents. Reason agents need only the context suitcase — no tool access.

**Why `approvals.mode: smart`:**
Manual mode gates every tool call interactively — acceptable for rare Tier-2 invocations, but kills the free-model gather loops that must run unattended. Smart mode applies risk scoring and only prompts for genuinely risky operations.

---

## Related Notes
- [[Hermes Cost Optimisation - Free Model Routing Strategy]]
- [[FTFL-638 Grafana Monitoring Fix - Testing Cluster]]
- [[Hermes Cost Routing - Cursor Implementation Prompt]]