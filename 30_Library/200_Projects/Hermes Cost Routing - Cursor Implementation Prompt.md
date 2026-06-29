---
created: 2026-06-08 11:35:53+00:00
modified: 2026-06-08 11:49:17+00:00
project_category: hermes_optimisastion
project_name: Hermes Optimisastion
project_status: active
title: Hermes Cost Routing - Cursor Implementation Prompt
type: null
permalink: llmeon/30-library/200-projects/hermes-cost-routing-cursor-implementation-prompt
---

## Hermes Cost Routing Implementation

### Context

You are working in the chezmoi-managed Hermes config directory at `private_dot_hermes/`. The goal is to implement a Gather → Reason → Act cost routing strategy that keeps the free `owl-alpha` model as the workhorse and escalates to paid Claude only for bounded reasoning steps.

### What Already Exists (do not break)

- `private_config.yaml`—Main config. Key relevant values:
  - `model.default: openrouter/owl-alpha`—main model is already free ✓
  - `delegation.model: anthropic/claude-sonnet-4-6` via OpenRouter—paid escalation already wired ✓
  - `delegation.inherit_mcp_toolsets: true`—child agents inherit MCP servers (needs tightening)
  - `approvals.mode: manual`—needs changing to `smart`
  - All `auxiliary.*` models already on `openrouter/owl-alpha` ✓
- `skills/route-task.md`—5-tier routing skill (Tier 0 local → Tier 2 CLI delegation). Currently covers general coding/PKM work. Does NOT have explicit infra debugging protocols or Gather/Reason/Act semantics.
- `skills/premium/claude-code.md`—Uses `claude --print "<prompt>"` via terminal for coding delegation. Good for coding; needs a parallel infra version using Hermes `delegate_task` (not CLI) for bounded reasoning without tool loops.

### Change 1—`private_config.yaml`

Make these targeted changes:

a) Switch approvals to smart mode (line 344):

```yaml
approvals:
  mode: smart          # was: manual
  timeout: 60
  cron_mode: deny
  mcp_reload_confirm: true
  destructive_slash_confirm: true
```

b) Tighten delegation so child Reason agents get no terminal—add `toolsets` restriction to the `delegation` block (around line 300):

```yaml
delegation:
  model: anthropic/claude-sonnet-4-6
  provider: openrouter
  base_url: ''
  api_key: ''
  api_mode: ''
  inherit_mcp_toolsets: false    # was: true — Reason agents must not have MCP/terminal
  toolsets: [file]               # add: Reason agents get file-read only, no terminal
  max_iterations: 20             # was: 50 — Reason agents must stay bounded
  child_timeout_seconds: 120     # was: 600 — Reason calls should be fast
  reasoning_effort: high         # add: we pay for reasoning, use it fully
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true
  subagent_auto_approve: false
```

c) Add a model alias comment block at the bottom of the file (before the final fallback_model comment block) to document the two key models:

```yaml
# ── Model Roles ──────────────────────────────────────────────────────────
# free_main  = openrouter/owl-alpha       (gather, act, monitor, mechanical)
# paid_reason = anthropic/claude-sonnet-4-6  (delegation only, via delegate_task)
# Use paid_reason ONLY via delegate_task with toolsets: [file] restriction above.
```

### Change 2—Rewrite `skills/route-task.md`

Preserve the existing 5-tier table and all tier definitions. ADD a new section called "Infra / Debugging Protocol" between the "Tier 2" section and the "Routing Rules" section. This section describes the Gather → Reason → Act split specifically for infrastructure and debugging tasks:

```markdown
## Infra / Debugging Protocol (Gather → Reason → Act)

For any task involving: kubectl, ArgoCD, Helm, Loki, Prometheus, node debugging, 
Kubernetes config, or any symptom investigation where the root cause is unknown.

### Phase classification

| Phase | Who runs it | What it does |
|-------|-------------|--------------|
| Gather | Tier 1.5 (owl-alpha, free) | Run all diagnostic commands. Read files. Collect output. Build a structured context bundle. |
| Reason | Tier 2 (`delegate_task`) | Receive the context bundle. Return: root cause + exact fix steps + verification commands. No tool use. |
| Act | Tier 1.5 (owl-alpha, free) | Apply the fix. Validate. Monitor. Re-gather if still broken. |

### Gather phase rules

1. Run ALL relevant diagnostic commands before forming any hypothesis.
2. Extract only the signal: error messages, relevant config sections, recent events, diff vs expected state.
3. Self-rate confidence: _"I can identify the root cause from this data: yes / no / uncertain"_
4. If yes and it matches a known playbook pattern → Act immediately (no escalation needed).
5. If no or uncertain → package the suitcase and escalate to Reason.

### Escalation signals (trigger Reason phase)

Escalate to `delegate_task` when ANY of these are true:
- Error message does not match a known pattern in the playbooks below
- A fix was applied but the symptom persists after re-gather
- Root cause requires cross-referencing more than 2 files/resources
- A new schema, operator behaviour, or chart internals must be understood from source
- More than 2 Gather → Act cycles have completed without resolution

### Reason phase — context suitcase schema

When calling `delegate_task`, pass exactly this bundle (no raw command output, distilled only):

```

SYMPTOMS: <bullet list of what is broken and how you know>

ERRORS: <exact error messages, file + line if applicable>

RELEVANT CONFIG: <only the config sections that are suspect, not the whole file>

WHAT I TRIED: <list of fixes attempted and what happened>

WHAT I NEED: root cause + exact fix (file, key, value) + verification command

```

Delegate model: `anthropic/claude-sonnet-4-6` via `delegate_task`.
The child agent has `toolsets: [file]` only — do not ask it to run commands.

### Act phase rules

1. Implement the returned fix exactly as specified.
2. Run the verification command(s) specified by the Reason agent.
3. If verified → done.
4. If not verified → re-gather, note what changed, and escalate again with the updated suitcase.

### Known playbook patterns (no escalation needed)

If the symptom matches one of these exactly, the free model executes the full fix without escalating:

- ArgoCD stuck operation → use skill `argocd-unstick`
- Pod CrashLoopBackOff with known error → use skill `crashloop-triage`
- Helm schema validation error → use skill `helm-validate`
- Loki stream label audit → use skill `loki-label-audit`
```

Also update the existing "Route to Tier 2" rule to add one bullet:

```
- Infra/debugging where Gather phase confidence < 0.7 or escalation signals are present (use delegate_task with infra suitcase schema, not claude --print)
```

### Change 3—Update `skills/premium/claude-code.md`

Add a "When NOT to use this skill" section near the top, after the Purpose section:

```markdown
## When NOT to use this skill

Use `delegate_task` (not `claude --print`) when:
- The task is infrastructure debugging / symptom investigation
- You have a structured suitcase from the Gather phase
- You do NOT want Claude to run tool loops (you want pure reasoning)

Use `claude --print` (this skill) only for:
- Code refactoring, test generation, architecture review
- Tasks where Claude needs to read many source files independently
```

### Change 4—Create 4 New Infra Playbook Skills

Create these files under `skills/custom/infra/`:

#### `skills/custom/infra/argocd-unstick.md`

```markdown
---
name: argocd-unstick
description: "Terminate a stale ArgoCD operation and re-sync to HEAD. Free model executes mechanically."
version: 1.0.0
metadata:
  hermes:
    tags: [infra, argocd, kubernetes, playbook, free-model]
---

# ArgoCD Unstick Playbook

## When to use
ArgoCD app shows `phase=Running` or `phase=Failed` at an old git revision while newer commits exist on the target branch.

## Steps (execute in order, no reasoning required)

1. Check current state
```bash
kubectl --context <ctx> get application <app> -n argocd \
  -o jsonpath='phase={.status.operationState.phase}{"
"}revision={.status.operationState.operation.sync.revision}{"
"}retryCount={.status.operationState.retryCount}{"
"}msg={.status.operationState.message}'
```

1. Get git HEAD

```bash
git -C <repo_path> fetch origin <branch> && git -C <repo_path> rev-parse origin/<branch>
```

2. Decision: if `operationState.phase` is `Running` or `Failed` AND operation revision!= git HEAD → proceed. Otherwise stop.
3. Terminate stuck operation

```bash
kubectl --context <ctx> patch application <app> -n argocd \
  --type json -p '[{"op": "remove", "path": "/operation"}]'
```

If patch returns "invalid request" (no operation to remove), skip to step 5.

4. Force hard refresh

```bash
kubectl --context <ctx> annotate application <app> -n argocd \
  argocd.argoproj.io/refresh=hard --overwrite
```

5. Wait for new operation at HEAD

```bash
until kubectl --context <ctx> get application <app> -n argocd \
  -o jsonpath='{.status.operationState.operation.sync.revision}' \
  | grep -q "<HEAD_REVISION>"; do sleep 5; done
```

6. Report: new operation revision + phase.

### Escalate if

- Step 4 succeeds but no new operation starts within 60s
- New operation starts at HEAD but immediately fails with a non-timeout error
- The same app has been unstuck more than 3 times in this session

```

### `skills/custom/infra/crashloop-triage.md`

```markdown
---
name: crashloop-triage
description: "Gather structured diagnostic bundle for a CrashLoopBackOff pod. Returns context suitcase for escalation or direct fix if pattern matches."
version: 1.0.0
metadata:
  hermes:
    tags: [infra, kubernetes, debugging, crashloop, playbook, free-model]
---

# CrashLoopBackOff Triage Playbook

## When to use
A pod is in `CrashLoopBackOff` status and the root cause is unknown.

## Steps

1. Collect logs (all containers, last 60 lines)
```bash
kubectl --context <ctx> logs <pod> -n <ns> --all-containers --tail=60 2>&1
```

1. Collect pod spec and events

```bash
kubectl --context <ctx> describe pod <pod> -n <ns> 2>&1 | \
  grep -E "State:|Reason:|Message:|Args:|Port:|Host Port:|Image:|hostNetwork:|Limits:|Requests:|Liveness:|Readiness:|Mounts:|Volumes:|Events:" 
```

2. Collect recent namespace events

```bash
kubectl --context <ctx> get events -n <ns> --sort-by='.lastTimestamp' 2>&1 | tail -20
```

3. Pattern match against known causes:

| Pattern in logs | Known fix | Escalate? |
|---|---|---|
| `bind: address already in use` | Check for duplicate port binding (hostNetwork + extraArgs) | No—fix in config |
| `failed to evaluate config` + `component "X" does not exist` | Unquoted string in Alloy/River config | No—quote the value |
| `Error: values don't meet the specifications` | Helm schema violation—check error path | No—fix values |
| `connection refused` to same-pod port | Sidecar not ready, check init order | Possibly |
| Any other error | Build suitcase and escalate | Yes |

1. If escalating: package suitcase using schema from `route-task` infra protocol.

### Output Format

```
POD: <name> | NAMESPACE: <ns> | RESTART_COUNT: <n>
LAST_ERROR: <exact last error line from logs>
PATTERN_MATCH: <matched pattern or "no match">
RECOMMENDATION: <fix or "escalate">
```

```

### `skills/custom/infra/helm-validate.md`

```markdown
---
name: helm-validate
description: "Extract values section and run helm template to catch schema/validation errors before pushing."
version: 1.0.0
metadata:
  hermes:
    tags: [infra, helm, kubernetes, validation, playbook, free-model]
---

# Helm Template Validation Playbook

## When to use
Before committing values.yaml changes to a Helm-managed ArgoCD app, or after a sync fails with a Helm error.

## Steps

1. Extract the relevant values section (the subchart values, not the whole ffnode wrapper):
```bash
awk '/^<top_key>:/{found=1; next} found && /^[^ ]/{found=0} found{sub(/^  /,""); print}' \
  <values_file> | grep -v "^chart:\|vaultSecrets:" > /tmp/chart-test-values.yaml
```

1. Run helm template:

```bash
helm template <release_name> <chart_path> \
  --namespace <namespace> \
  --kube-version <kube_version> \
  --values /tmp/chart-test-values.yaml \
  > /dev/null 2>&1 && echo "CLEAN" || \
helm template <release_name> <chart_path> \
  --namespace <namespace> \
  --kube-version <kube_version> \
  --values /tmp/chart-test-values.yaml \
  2>&1 | grep -A 15 "execution error\|^Error:"
```

2. Pattern match errors:

| Error pattern | Known fix |
|---|---|
| `got array, want object` at `/destinations` | Convert destinations from list to map (remove `- name:`, promote name to key) |
| `At least one collector should be enabled` | Add `collectors:` map with at least one entry |
| `requires Alloy to mount /var/log` | Add `presets: [filesystem-log-reader]` to the logs collector |
| `cluster id should match cluster name` | Add `exporter.defaultClusterId: <cluster_name>` |
| `component "X" does not exist or is out of scope` | Unquoted string value in Alloy River syntax—add quotes |
| Any other execution error | Escalate with the full error + relevant values section |

1. Report: CLEAN or escalate with structured error bundle.

```

### `skills/custom/infra/loki-label-audit.md`

```markdown
---
name: loki-label-audit
description: "Query Loki stream labels for a cluster and report present/missing labels vs expected baseline."
version: 1.0.0
metadata:
  hermes:
    tags: [infra, loki, monitoring, observability, playbook, free-model]
---

# Loki Label Audit Playbook

## When to use
Verifying that expected stream labels are present for a cluster in Loki, or investigating why `{cluster="X", pod="Y"}` queries return no results.

## Expected baseline labels (k8s-monitoring v4.x)

```

cluster, k8s_cluster_name, namespace, container, pod, node,

job, service_name, stream, flags, level, app_kubernetes_io_name

```

## Steps

1. Get all stream label keys for the cluster:
```bash
gcx logs series --context <gcx_context> -d <loki_datasource> \
  --match '{cluster="<cluster_name>"}' -o json 2>&1 | python3 -c "
import sys,json
raw=sys.stdin.read()
lines=[l for l in raw.split('
') if not l.startswith('hint:')]
d=json.loads('
'.join(lines))
streams=d.get('data',[])
all_keys=set()
for s in streams: all_keys.update(s.keys())
pod_count=sum(1 for s in streams if 'pod' in s)
print(f'Streams: {len(streams)}')
print(f'Keys: {sorted(all_keys)}')
print(f'Streams with pod: {pod_count}/{len(streams)}')
"
```

2. Check for recent logs (last 1h):

```bash
gcx logs query --context <gcx_context> -d <loki_datasource> \
  '{cluster="<cluster_name>"}' --limit 1 --from now-1h -o json 2>&1 | \
  python3 -c "
import sys,json
raw=sys.stdin.read()
lines=[l for l in raw.split('
') if not l.startswith('hint:')]
d=json.loads('
'.join(lines))
result=d.get('data',{}).get('result',[])
print('Recent logs found:', len(result) > 0)
if result: print('Sample stream:', result[0].get('stream',{}))
"
```

3. Compare against baseline and report:

```
PRESENT:   <list of expected labels found>
MISSING:   <list of expected labels not found>
EXTRA:     <labels present but not in baseline>
RECENT_LOGS: yes/no
```

4. Known root causes for missing `pod` label:
- v3.x chart: `stage.structured_metadata { "pod" = "pod" }` moves pod to structured metadata. Fix: remove from structuredMetadata or null it.
- v4.x chart: same issue if `podLogsViaLoki.structuredMetadata.pod` is not set to `null`.

1. Known root cause for no recent logs:
- Check alloy-logs pods are Running: `kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-logs`
- Check the secret referenced in the alloy-logs ConfigMap exists in the monitoring namespace.
- Common issue: ConfigMap references `logs_service` secret but actual secret is named `monitoring`.

### Escalate if

- All labels are present but queries still return no results
- Alloy-logs pods are Running but no logs arrive after 10 minutes

```

## Change 5 — MCP server tightening in `private_config.yaml`

In the `mcp_servers` block (around line 433), add explicit tool restrictions:

```yaml
mcp_servers:
  mcp-proxy:
    url: http://127.0.0.1:8000/mcp/
    transport: streamable-http
    connect_timeout: 8
    tools:
      exclude: []          # add explicit allowlist if specific tools should be blocked
  pieces:
    url: http://localhost:39300/model_context_protocol/
    transport: sse
    timeout: 60
    connect_timeout: 8
    tools:
      include:             # allowlist: only the Pieces tools actually used
        - ask_pieces_ltm
        - search_pieces
        - save_to_pieces
```

### Summary of Files to create/modify

| File | Action |
|---|---|
| `private_dot_hermes/private_config.yaml` | Modify: approvals smart, delegation tighten (toolsets/timeout/inherit_mcp), MCP allowlists, add model role comments |
| `private_dot_hermes/skills/route-task.md` | Add: Infra/Debugging Protocol section with Gather/Reason/Act, escalation signals, suitcase schema, playbook reference table |
| `private_dot_hermes/skills/premium/claude-code.md` | Add: "When NOT to use" section directing infra tasks to delegate_task instead |
| `private_dot_hermes/skills/custom/infra/argocd-unstick.md` | Create new |
| `private_dot_hermes/skills/custom/infra/crashloop-triage.md` | Create new |
| `private_dot_hermes/skills/custom/infra/helm-validate.md` | Create new |
| `private_dot_hermes/skills/custom/infra/loki-label-audit.md` | Create new |

### Constraints

- Do not change the existing 5-tier table structure in `route-task.md`—add the infra protocol as an additional section.
- Do not change `delegation.model`—it is correctly set to `anthropic/claude-sonnet-4-6`.
- Do not add a `fallback_model`—the commented-out block at the bottom of config should stay commented.
- The `skills/custom/infra/` directory may not exist yet—create it.
- All config changes are in `private_dot_hermes/` (chezmoi source), not the deployed `~/.hermes/` directory.