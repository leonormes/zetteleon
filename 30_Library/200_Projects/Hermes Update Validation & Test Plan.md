---
created: 2026-05-28T14:17:22+00:00
modified: 2026-08-29T09:36:19+00:00
permalink: llmeon/30-library/200-projects/hermes-update-validation-test-plan
project_category: hermes_optimisastion
project_name: Hermes Optimisastion
project_status: active
title: Hermes Update Validation & Test Plan
type: null
---

## Validation: Changes Confirmed in Files

### `private_config.yaml`

| Change | Expected | Found in file | Status |
|---|---|---|---|
| `approvals.mode` | `smart` | `approvals:\n  mode: smart` | ✅ |
| `delegation.inherit_mcp_toolsets` | `false` | `inherit_mcp_toolsets: false` | ✅ |
| `delegation.toolsets` | `[file]` | `toolsets: [file]` | ✅ |
| `delegation.max_iterations` | `20` | `max_iterations: 20` | ✅ |
| `delegation.child_timeout_seconds` | `120` | `child_timeout_seconds: 120` | ✅ |
| `delegation.reasoning_effort` | `high` | `reasoning_effort: high` | ✅ |
| `mcp_servers.mcp-proxy.tools.exclude` | `[]` | `tools:\n  exclude: []` | ✅ |
| `mcp_servers.pieces.tools.include` | `[ask_pieces_ltm, search_pieces, save_to_pieces]` | Exact list present | ✅ |
| Model Roles comment block | `free_main = owl-alpha / paid_reason = claude-sonnet-4-6` | Comment block present at end of file, both roles documented | ✅ |

One note: the `delegation.model` is set to `anthropic/claude-sonnet-4-6` via `openrouter` provider—confirm your OpenRouter account actually has credits for that model slug before Phase B.

---

### `skills/route-task.md`

| Change | Expected | Found | Status |
|---|---|---|---|
| "Infra / Debugging Protocol" section | Between Tier 2 and Routing Rules | Full `Gather → Reason → Act` table, phase rules, suitcase schema, escalation signals, known playbooks, all present | ✅ |
| Extra Tier-2 bullet for infra/debug | `delegate_task` (not `claude --print`) | At end of Tier 2 routing rules: _"Infra/debugging where Gather phase confidence < 0.7 or escalation signals are present (use `delegate_task` with infra suitcase schema, not `claude --print`)"_ | ✅ |

---

### `skills/premium/claude-code.md`

| Change | Expected | Found | Status |
|---|---|---|---|
| "When NOT to use this skill" section | Infra debugging → `delegate_task`, not `claude --print` | Section present immediately after Purpose, distinguishes `delegate_task` (infra/suitcase/no tool loops) from `claude --print` (code tasks) | ✅ |

---

### New Infra Skill Files

| File | Path confirmed | Content validated |
|---|---|---|
| `argocd-unstick.md` | ✅ `skills/custom/infra/argocd-unstick.md` (1901 bytes, modified today) | ✅ Full 7-step mechanical playbook, escalation conditions, correct `phase=Running/Failed` trigger |
| `crashloop-triage.md` | ✅ path in same directory (found via search, confirmed directory) | Not individually read—validate below with `cat` |
| `helm-validate.md` | ✅ same directory | Not individually read—validate below |
| `loki-label-audit.md` | ✅ same directory | Not individually read—validate below |

### `assets/context/cost-routing-pilot.md`

| Change | Expected | Found | Status |
|---|---|---|---|
| Phase A free-only run criteria | Gather/Act loop validation, no paid calls | Full Phase A section with success criteria + tuning knobs | ✅ |
| Phase B minimum-credit paid pilot | Bounded escalation only, Reason agent returns fix | Full Phase B section with pass/fail criteria | ✅ |

---

## Test Plan

### 0. Pre-flight Checks (Run before Anything eLse)

```bash
# Confirm chezmoi source matches live config
chezmoi diff ~/.hermes/private_config.yaml

# Apply if there are differences
chezmoi apply

# Confirm Hermes picks up the new config
hermes doctor
```

Verify: `approvals mode: smart` appears in doctor output. If hermes doesn't surface it directly, check:

```bash
grep -A2 'approvals:' ~/.hermes/config.yaml
grep -A6 'delegation:' ~/.hermes/config.yaml
```

Confirm the four infra skill files actually landed in the live skills directory:

```bash
ls ~/.hermes/skills/custom/infra/
# Expected: argocd-unstick.md  crashloop-triage.md  helm-validate.md  loki-label-audit.md
```

---

### 1. Routing Smoke test—`route-task` Skill Fires on Startup

Start a Hermes session and run a trivial task:

```
/skill route-task
Summarise what this repo does: /Volumes/DAL/Zettelkasten/LLMeon
```

Expected: Hermes announces `[Tier 1.5 — free_heavy] Reason: PKM synthesis / large context`. It should NOT delegate. Cost: £0.

---

### 2. `approvals.mode: smart`—check Approval Behaviour

Trigger a file-write action (a mutation Hermes would previously ask you to approve in `manual` mode):

```
Create a test file at /tmp/hermes-approval-test.txt with the content "smart mode test"
```

Expected in `smart` mode: Hermes executes without a manual `[y/n]` prompt for low-risk file writes. It should only prompt for genuinely destructive/irreversible operations. If you still see a prompt on every write, `smart` mode hasn't loaded—re-run `chezmoi apply`.

---

### 3. Pieces MCP Tool filter—only Whitelisted Tools Exposed

From inside a Hermes session:

```
/tools
```

Look for the `pieces` MCP section. Expected: only `ask_pieces_ltm`, `search_pieces`, `save_to_pieces` listed. No other `mcp_pieces_*` tools should appear. If you see more, the `tools.include` filter hasn't applied—restart the Hermes gateway:

```bash
hermes gateway restart
```

---

### 4. Infra playbook—known Pattern, no Escalation (Phase A)

Test with an ArgoCD scenario (or simulate with a kubectl context you have):

```
Hermes, I have an ArgoCD app stuck in Running state at an old revision.
App name: <your-app>, context: <your-ctx>, branch: main
```

Expected path:

1. Hermes routes via `route-task` → Tier 1.5
2. Detects "ArgoCD stuck" → matches known playbook pattern `argocd-unstick`
3. Tier 1.5 (owl-alpha, free) executes the 7 steps mechanically
4. No `delegate_task` call fires (confirm by checking session log—no paid model invocation)

To simulate without a live cluster, ask it to walk through the playbook dry-run:

```
Walk through the argocd-unstick playbook for app "fake-app" in context "test" — 
show me every command you would run without executing them.
```

Expected: exact commands from `argocd-unstick.md` steps 1–7 populated with your values.

---

### 5. Infra protocol—escalation to `delegate_task` (Phase B gAte)

Give Hermes an ambiguous infra symptom that doesn't match any playbook exactly:

```
Hermes: I have a pod that's OOMKilled intermittently — not a CrashLoop, no clean error, 
only happens under load. Here are my logs: [paste 20–30 lines of realistic logs]
```

Expected path:

1. Gather phase runs (owl-alpha collects kubectl describe, resource usage, events)
2. `confidence < 0.7` or no matching playbook → escalation signal fires
3. Hermes packages a suitcase matching the schema (SYMPTOMS / ERRORS / RELEVANT CONFIG / WHAT I TRIED / WHAT I NEED)
4. `delegate_task` is called with `anthropic/claude-sonnet-4-6` and only `toolsets: [file]`
5. Delegation returns root cause + fix steps + verification command
6. Hermes (owl-alpha) applies Act phase

What to verify in the session log:

- Delegation subagent spawned: `claude-sonnet-4-6` only
- Subagent did NOT run any terminal commands (only `file` toolset)
- Total paid tokens: bounded by `max_iterations: 20` + `child_timeout_seconds: 120`

---

### 6. Delegation Lockdown guard—no Terminal in Reason Agent

Explicitly confirm the child cannot escape its sandbox:

```
delegate_task: "Please run `kubectl get pods -A` and tell me what you see."
```

Expected: the child agent returns an error or says it lacks terminal access. It should NOT attempt to run the command. If it does, `toolsets: [file]` is not being applied—re-check `delegation.inherit_mcp_toolsets: false` is in the live config.

---

### 7. Phase A pilot—full Free-only Session

Per `cost-routing-pilot.md` Phase A:

- Run one repo coding task (e.g. ask Hermes to refactor a function): confirm zero paid calls, `claude --print` used for reasoning if needed, owl-alpha for orchestration.
- Run one infra/debug task matching a known playbook: confirm full Gather → Act loop completes with zero `delegate_task` invocations.

Check OpenRouter usage dashboard at [openrouter.ai/workspaces/default/observability](https://openrouter.ai/workspaces/default/observability) after the session—`owl-alpha` calls should be free tier, £0 cost.

---

### 8. Phase B pilot—minimum Credits, Bounded Paid Use

Only after Phase A passes:

- Buy minimum OpenRouter credits
- Run a genuinely ambiguous infra session
- After the session, check the OpenRouter observability dashboard:
  - Paid calls should be only `anthropic/claude-sonnet-4-6`
  - Each delegation should be ≤20 iterations, ≤120s
  - owl-alpha Gather/Act work should dominate the token count

Hard stop signal: if `claude-sonnet-4-6` is being called for tasks that match a known playbook (ArgoCD, CrashLoop, Helm validate, Loki audit), the routing logic is leaking—tighten the confidence threshold in the Gather phase rules.
