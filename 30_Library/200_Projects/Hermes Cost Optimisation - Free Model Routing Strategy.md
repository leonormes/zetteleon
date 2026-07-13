---
created: 2026-06-08T11:35:53+00:00
date: 2026-05-28
modified: 2026-07-13T08:44:42+00:00
permalink: llmeon/30-library/200-projects/hermes-cost-optimisation-free-model-routing-strategy
project: hermes-agent-orchestrator
project_category: hermes_optimisastion
project_name: Hermes Optimisastion
project_status: active
status: design-proposal
tags: [agent-orchestration, claude, cost-optimization, hermes, llm-routing, openrouter]
title: Hermes Cost Optimisation - Free Model Routing Strategy
type: null
---

## Hermes Cost Optimisation—Free Model Routing Strategy

### Context

Analysis of a long Claude Code session (FTFL-638—Grafana monitoring fix for testing AKS cluster) to identify which operations could be delegated to a free model in Hermes, reducing token costs while preserving Claude's quality for tasks that require it.

The session covered: ArgoCD deadlock debugging, Alloy config errors, Helm chart migration (v3.x → v4.x), Loki stream label analysis, kubectl/gcx diagnostics, and a staging cluster bug discovery.

---

### The Core Pattern

Every debugging cycle in the session followed three phases:

```
Gather → Reason → Act
```

- Gather—run commands, read files, collect output (~60–70% of operations)
- Reason—understand what the output means, form a hypothesis (~15%)
- Act—write a fix, validate, monitor (~20%)

Phases 1 and 3 are largely mechanical. Phase 2 is where Claude earns its cost.

---

### What a Free Model Could Handle

#### Mechanical Operations (Free Model vIable)

| Task Type | Examples from the Session |
|---|---|
| `kubectl get/describe/logs` | Pod status, events, ArgoCD app state, DaemonSet spec |
| Monitoring loops | `until condition; do sleep; done`—waiting for sync/health/readiness |
| grep through files | Searching values.yaml, chart files, templates for specific keys |
| `git log / diff / show / fetch` | Checking commit contents, comparing revisions |
| `helm template` validation | Running render and checking for `Error:` or `execution error` |
| `gcx` label/series/query calls | Fetching Loki label names, stream counts, metric jobs |
| ArgoCD operation termination | patch + annotate commands once the decision is made |
| Reading known file paths | values.yaml, ConfigMap contents, ArgoCD Application CR |
| Extracting and dumping structured data | kubectl jsonpath + pipe to file for later analysis |

#### Concrete Example—ArgoCD Deadlock Cycle (Repeated 5× in the sEssion)

```
check app status →
read operationState.phase + operationState.revision →
compare revision vs git HEAD →
if stale: terminate operation + hard refresh →
wait for new operation to start at HEAD →
monitor until Synced or Failed
```

Every step here is mechanical. Once Claude established _why_ the deadlock happens and what the fix commands are, a free model could execute this entire cycle on every subsequent recurrence with zero reasoning required.

---

### What Required Claude

| Reasoning Task | Why a Free Model Would Fail |
|---|---|
| Diagnosing `action = keep` as an Alloy River syntax error | Requires knowing Alloy's River language spec—not discoverable from the error message alone |
| Tracing the unquoted `keep` back through Application CR → ffnode chart merge → k8s-monitoring template | Multi-file causal chain across 4 levels of abstraction |
| Identifying the `--web.listen-address` self-conflict (`HOST_IP=0.0.0.0` + `hostNetwork: true` = duplicate bind) | Requires understanding how the chart sets HOST_IP when hostNetwork is enabled |
| Explaining why `stage.structured_metadata` removes `pod` from Loki stream labels | Nuanced Alloy pipeline semantics—not described in any error message |
| Planning the full v3.x → v4.x Helm chart migration | Reading chart source, cross-referencing CHANGELOG, building a mental model of a new architecture |
| Diagnosing the ArgoCD timing race (sync started with stale Application CR values) | Required understanding ArgoCD's operational state machine: last-applied annotation vs. live spec vs. desired state |
| Connecting staging's missing `logs_service` secret to zero logs for 30+ days | Three silent facts: secret doesn't exist + ConfigMap references it + Alloy fails silently |

---

### Hermes Routing Design

#### Principle

> The free model should be a good data collector and a poor diagnostician—it knows the limits of its own pattern matching and escalates cleanly rather than hallucinating a fix.

#### Routing Rules

```
Free model handles:
  - All kubectl / git / helm / gcx commands
  - File reads and grep operations
  - Mechanical edits (change key X to value Y at known location)
  - Monitoring loops and health checks
  - Structured output parsing and summarisation
  - Repeating previously-established fix patterns

Escalate to Claude when:
  - An error message doesn't map to a known fix pattern
  - A previous fix attempt was applied but the symptom persists
  - Multiple files must be cross-referenced to explain one symptom
  - A new configuration schema / operator behaviour must be understood from source
  - The free model has tried more than 2 approaches without resolution
  - An architectural change is needed, not just a value tweak
  - Confidence self-rating falls below threshold after gather phase
```

#### Escalation Signal Heuristics

```python
ESCALATE_SIGNALS = [
    "error in logs does not match any known pattern",
    "fix was applied but symptom persists after N attempts",
    "need to cross-reference more than 2 files to form hypothesis",
    "need to understand chart/operator internals from source",
    "architectural change required (not just config tweak)",
    "self-rated confidence < 0.7 after gather phase",
]

def route(task, free_model_confidence):
    if any(signal_present(task, s) for s in ESCALATE_SIGNALS):
        return "claude"
    if free_model_confidence >= 0.7:
        return "free"
    return "claude"
```

#### Ideal Session Structure

Step 1—Free model runs the diagnostic gather loop:

```
run all kubectl/gcx/git diagnostics →
dump: pod statuses, error messages, relevant config sections, ArgoCD state →
structure into: symptoms / error messages / relevant config →
self-rate confidence on likely cause →
if low confidence: package context and escalate to Claude
```

Step 2—Claude does one focused analysis call (no command running):

```
receive structured context →
reason over it →
produce: "root cause is X, fix is Y, change file Z at line N"
```

Step 3—Free model implements and validates:

```
apply the edit →
run helm template / kubectl apply →
terminate stale ArgoCD ops if needed →
monitor until healthy →
if still broken: re-gather and escalate again
```

---

### Estimated Cost Impact

This session had roughly 40–50 back-and-forth tool call sequences where Claude was both running the command AND interpreting the output.

The actual reasoning that justified Claude's cost happened approximately 10 times (one per genuine root cause). Everything else was context-building that any model can do given the right tools and a clear "gather then report" instruction.

A Hermes split would compress the session to approximately 8–10 Claude calls with the free model handling everything around them—a rough 3–5× cost reduction for sessions of this type.

#### What Drove the Unnecessary Cost

- File reads and greps that returned nothing
- Repeated kubectl status checks to build incremental context
- Waiting/monitoring loops
- Mechanical YAML edits once the fix was known
- Re-running diagnostics after each fix attempt to confirm state

All of these are zero-reasoning operations that any model can execute reliably.

---

### Session-Specific Examples to Implement as Free Model Patterns

These patterns appeared multiple times in the session and are fully automatable:

#### Pattern: ArgoCD Unstick

```
1. check app.status.operationState.phase
2. check app.status.operationState.operation.sync.revision
3. git fetch + compare to HEAD
4. if revision != HEAD AND (phase == Failed OR retryCount >= 5):
     patch /operation remove
     annotate refresh=hard
5. wait for new operation at HEAD revision
```

#### Pattern: Pod CrashLoopBackOff Diagnose

```
1. kubectl logs <pod> --all-containers --tail=50
2. kubectl describe pod <pod> | grep -E "State:|Reason:|Message:|Args:|Port:"
3. kubectl get events -n <ns> --sort-by=lastTimestamp | tail -20
4. package: error_message + pod_spec + recent_events → escalate if no pattern match
```

#### Pattern: Helm Values Validation

```
1. extract relevant section from values.yaml
2. helm template <chart> --values <extracted> 2>&1
3. if "execution error": extract message → escalate
4. if clean: report "renders OK"
```

#### Pattern: Loki Stream Label Check

```
1. gcx logs series --match '{cluster="<name>"}' -o json
2. extract all label keys across streams
3. check for expected labels (pod, namespace, container, node)
4. report: present / missing / count
```

---

### Recommended OpenRouter Free Models for Gather Phase

Models that are reliable for mechanical operations and structured output with no creativity required:

- Gemini 2.0 Flash (free tier)—fast, large context, good at structured data extraction
- Llama 3.1 405B (free via OpenRouter)—strong at following explicit tool-use instructions
- Qwen 2.5 72B (free via OpenRouter)—reliable for grep/parse/summarise loops

Key requirement: the free model must be able to self-rate its own confidence and hand off cleanly rather than attempt reasoning it can't do reliably.

---

### Related Notes

- [[FTFL-638 Grafana Monitoring Fix - Testing Cluster]]
