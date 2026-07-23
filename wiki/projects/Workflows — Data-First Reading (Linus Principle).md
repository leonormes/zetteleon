---
title: Workflows — Data-First Reading (Linus Torvalds Principle)
date: 2026-07-23
tags:
- fitfile
- workflows-api
- data-structures
- design
- refactoring
- linus-torvalds
related:
- FITFILE Workflow Codebase — Complete Map & Analysis
permalink: llmeon/wiki/projects/workflows-data-first-reading-linus-principle
---

# Workflows — Data-First Reading

**Applied:** Linus Torvalds (2006, on git): "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

Git succeeded not because of clever SCM code, but because of simple, stable object structures (blob/tree/commit/ref) and clear relationships. Code is the easy part once the model is right; the inverse never works.

## Quick metrics

- **5+** overlapping 'workflow' identities ⚠️
- **2** submit data models (legacy vs DAG)
- **2** completion channels (poll vs Rabbit) ⚠️
- **strings** Template↔CLI link type today

---

## 1. The data that actually matters

Ignore Argo pods and Hera builders for a moment. A workflow run is really a **graph of typed artifacts on S3**, plus a small amount of control metadata that says how nodes relate and when the graph is terminal.

| Data | What it is | Where it lives today | Relationships that should be crisp |
|------|-----------|---------------------|-----------------------------------|
| Dataset + schema | Tabular payload + semantic types | S3 temp/output; paths invented per builder | Every transform: (dataset, schema) → (dataset, schema) |
| Artifact | Named file with business_name, tags, attributes | FinalizeArtifact → WorkflowOutputArtifact | keep_artifacts ⊆ task outputs; finalize promotes temp→output |
| Task node | template_id + user_inputs + depends_on + slots | TaskInWorkflowInstance in WorkflowPayload.dag | depends_on = edges; connections = external→slot wiring |
| Workflow run | One execution identity with status + outputs | Split across Argo uid/name, OperationTracking, receipt, sometimes DistributedWorkflowInstance | One primary key; everything else is a foreign key |
| Correlation | Link from app intent → run | Overloaded: operation id, OperationTracking.correlationId, Argo param, per-task UUIDs | Exactly one meaning, stored once, referenced everywhere |
| Template contract | What a task accepts/emits at the Argo boundary | String TemplateRef names + parallel UserInput/WorkflowInput types | Registry row: template_id → CR name → inner template → CLI → I/O schema |
| Completion event | Terminal status + failures + finalize_metadata | Argo status.outputs.parameters (polled); optional Rabbit payload (orphaned) | One event schema; one consumer path |

### Hidden data plane: path conventions

Much of the "graph" is not in the DAG object — it is implicit S3 key templates like `{path_prefix}/{dag_entry_id}_dataset.json`. That is data structure by convention, not by type. When conventions drift (output key `sql_out_key` vs template `output_sql`), the relationship breaks silently.

---

## 2. Where the model is unhealthy

### Identity: Five names for one run

Argo `metadata.uid` / `metadata.name`, FitConnect `OperationTracking.id`, `receipt.uid`, `OperationTracking.correlationId`, FFCloud `DistributedWorkflowInstance.id` + per-partition tracking IDs.

Code papers over this with lookups by uid and dual correlation fields. **Git would have one object id.**

**Symptom:** Poll/repoll use different keys. Custom submit strips correlation_id. Completion lookup searches by uid, not correlation_id.

### Relationship: TemplateRef is a stringly foreign key with no schema

Builder → WorkflowTemplate CR → inner template → container CLI is the most important relationship in the system, and it is **three independent string conventions** across InsightFILE, Deployment YAML, and data-and-analytics.

**Proven break:** `concatenate-two-datasets-template` vs `concatenate-multiple-datasets-template`.

**Code symptom:** MergeTaskBuilder re-instantiates predecessors to read their outputs, re-deriving what should be stored in the DAG.

### Duplication: Two workflow data models in parallel

- **Legacy:** flat `{ workflow_name, parameters }` → whole-pipeline WorkflowTemplate
- **New:** `WorkflowPayload.dag` of composable tasks

Same business outcomes, different shapes, different submit endpoints, different parameter semantics for correlation_id. Code (adapters, WorkflowManager branches) exists to translate between them instead of converging the model.

### Stages: UserInput vs WorkflowInput without a named transform

Types correctly distinguish "what the user configured" from "what the container receives" (paths filled in, upstream artifacts resolved). That is good data thinking — but the transform **lives as imperative builder methods**, not as an explicit, testable function:

```
(TaskNode, resolved upstream outputs) → WorkflowInput
```

Half the tasks also use opaque `Dict[str, Any]` / RootModel, so the boundary is not actually typed.

### Events: Two completion representations, one abandoned

Exit-handler Rabbit payload and `GET /workflow_status` both try to be "run finished". **Polling won; Rabbit config leftovers remain.**

Same fact, two schemas, unclear source of truth — classic symptom of coding paths before fixing the event model.

### Codegen: Shared types exist — but only for some edges

Zod → JSON Schema → pydantic is the right idea (one structure, many languages). It covers compose/submit payloads and finalize artifacts.

**It does NOT cover:**
- Template registry
- S3 path layout
- Completion event

data-and-analytics CLIs still speak argparse flags, not the workflow input types — so the container boundary is outside the shared model.

---

## 3. A Linus-aligned target model

Stabilize a small set of objects and make every layer a thin projection of them — like git's object store.

| Object | Stable fields | Edges |
|--------|--------------|-------|
| **ArtifactRef** | uri, business_name, content_type, digest?, tenant_id | produced_by → TaskRun; consumed_by → TaskRun.slot |
| **TaskSpec** | template_id, user_input (typed), keep_artifacts | template_id → TemplateManifest |
| **TaskRun** | id, spec, status, inputs: ArtifactRef[], outputs: ArtifactRef[] | depends_on → TaskRun[] |
| **WorkflowRun** | id (one UUID), name, status, created_by, tenant/project | contains → TaskRun DAG; optionally partition_of → WorkflowRun |
| **TemplateManifest** | template_id, argo_workflow_template, argo_inner_template, image/cli, input_schema, output_schema | **the only place string names are allowed** |
| **RunTerminalEvent** | workflow_run_id, status, failures[], finalize: ArtifactRef[] | emitted once; poll and (if kept) queue both deserialize this |

**Design rule:** If a relationship cannot be expressed as a field or foreign key on these objects, do not encode it in path-string conventions or parallel code paths. Put it in the data, then write boring code.

---

## 4. Refactors (data first, then delete code)

### P0 — stop the bleeding

**1. TemplateManifest as source of truth**

Single JSON/YAML registry (checked into InsightFILE or generated into Deployment) keyed by `template_id`. Builders read CR names from it; CI asserts Deployment YAML `metadata.name` / inner template / CLI command match.

**Deletes:** concatenate-class name mismatches; guesswork in builders.

**Code becomes:**
```
manifest = REGISTRY[template_id]
TemplateRef(**manifest.argo)
```

**2. One WorkflowRun id**

Pick Argo uid **or** OperationTracking id as primary; store the other as alias. Collapse `correlation_id` to a single documented field (recommend: client-supplied idempotency key, separate from run id).

Fix poll/repoll to use the same key. Remove the strip-on-custom-submit special case by putting the id in the payload schema.

**Deletes:** poll/repoll key divergence; strip-on-submit.

**3. One RunTerminalEvent schema**

Define in `packages/types`. Map Argo status → event in workflows-api; optionally have exit-handler publish the same schema (or delete Rabbit path entirely). FitConnect consumes one type.

**Deletes:** ad-hoc output_parameters parsing; dual interpretation of `workflow-failures` / `finalize_metadata`.

### P1 — make the artifact graph first-class

**4. Explicit ArtifactRef edges instead of path templates**

When composing/submitting, materialize each task's output ArtifactRefs (uri + business_name) on the TaskRun. Downstream tasks receive inputs by ref, not by reconstructing `{prefix}/{id}_dataset.json` in each builder.

`output_fits_into` becomes a type check on ArtifactRef.business_name compatibility — data, not a list of builder classes.

**Deletes:** path-string coupling between tasks.

**5. Named UserInput → WorkflowInput function**

For each template:
```
resolve(spec, upstream: ArtifactRef[]) → WorkflowInput
```

as a pure function next to the Zod/pydantic schema. Builders shrink to "call resolve + attach TemplateRef from manifest". Ban opaque Dict user inputs for new tasks.

**6. Push WorkflowInput to the container boundary**

data-and-analytics CLIs accept one JSON document matching the shared schema (or generate argparse from it). Stops the third dialect (CLI flags) from existing outside the model.

Finalize already did this for artifact metadata — extend the pattern.

### P2 — converge the two worlds

**7. Express legacy pipelines as WorkflowPayload DAGs**

`query-template` et al. become canned DAGs of the same task nodes (or a single composite template still referenced from one registry).

`POST /workflow_submit/` becomes sugar over `POST /workflows/submit`. Deletes `allowed_workflows_map` and half of Operation adapters' special cases — because there is only one run shape.

**8. Partitions as WorkflowRun edges, not a parallel product**

`DistributedWorkflowInstance` should be a graph of WorkflowRun ids with cross-partition ArtifactRefs (load-from-artifacts already implies this). Supervisor polls RunTerminalEvent per child run.

Avoid a second status enum that almost-but-not-quite mirrors Argo/Operation status.

---

## 5. What NOT to refactor first

| Tempting code cleanup | Why it is secondary |
|---------------------|-------------------|
| Rewrite builders / magic_builder elegance | Still keyed off string template ids; prettier code on a broken FK |
| More Hera helpers / less duplication in workflow_submitting.py | Legacy map exists because the data model is forked; merge the model first |
| Revive or polish Rabbit exit handlers | Until RunTerminalEvent is singular, a second transport adds noise |
| Micro-optimizing poll cron | Identity/correlation confusion causes worse operational bugs than poll interval |

---

## 6. Practical order of attack

| Step | Deliverable | Deletes or prevents |
|------|-------------|-------------------|
| 1 | TemplateManifest + CI drift check vs Deployment YAML | concatenate-class name mismatches; guesswork in builders |
| 2 | WorkflowRun identity doc + single correlation field in types | poll/repoll key divergence; strip-on-submit |
| 3 | RunTerminalEvent in packages/types; status endpoint returns it | ad-hoc output_parameters parsing |
| 4 | ArtifactRef on submit payload / finalize | path-string coupling between tasks |
| 5 | Legacy pipelines as DAG presets | dual submit APIs and adapter sprawl |

---

## 7. Litmus test

**After a change, a new engineer should understand a run by reading one schema (WorkflowRun + TaskRun + ArtifactRef + TemplateManifest), not by tracing:**

FitConnect → workflows-api → Hera → YAML → CLI → Rabbit → poll

**If they still need the code path to learn the relationships, the data model is not done.**

---

**Quote:** Linus Torvalds, June 2006, git/library licensing thread (LWN 193245).  
**Based on:** InsightFILE workflows-api / FitConnect / types, data-and-analytics CLIs, Deployment WorkflowTemplates.