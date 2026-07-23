---
title: FITFILE Workflow Architecture — Argo + workflows-api Map
date: 2026-07-23
tags:
- fitfile
- argo-workflows
- workflows-api
- fitconnect
- omop
- architecture
- map
sources:
- /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE
- /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/data-and-analytics
verified-with:
- ast-grep (1MCP)
- lsp-bash (1MCP)
- manual file reads
permalink: llmeon/wiki/projects/fitfile-workflow-architecture-argo-workflows-api-map
---

# FITFILE Workflow Architecture — Argo + workflows-api Map

Full map of the workflow codebase across **InsightFILE** and **data-and-analytics**, produced 2026-07-23. Structural claims (builder→template mappings, template ids, prebaked submission call sites, listener registrations) were re-verified with ast-grep AST queries via 1MCP rather than text grep. Related: [[FITFILE Deployment — ArgoCD + Helm]], [[12 Million Patient Synthetic NHS-OMOP Pipeline]], [[2026-05-29-FTFL-638-argo-workflows-logs-missing-loki]].

## 1. Two-layer model

**(a) Argo layer** — literal `WorkflowTemplate` custom resources, referenced *by name only* from code. **Neither repo contains a single `kind: WorkflowTemplate` manifest** — the YAMLs live in the ArgoCD GitOps repo (app-of-apps pattern, per data-and-analytics `plan.md:273`). This is the biggest traceability gap.

**(b) Internal application concept** — `Operation` → `WorkflowPayload` → Hera `Workflow`:

- **fitconnect** (InsightFILE, TS): business abstraction. `Operation`, persisted `OperationTracking` (correlationId + receipt `{uid, name}`), per-operation **workflow adapters**.
- **workflows-api** (InsightFILE, Python/FastAPI + **Hera**): orchestration abstraction. `TaskTemplate` (catalogue), `AbstractTaskBuilder` (DAG entry → Hera `Task` with `TemplateRef`), `WorkflowBuilder` (assembles + submits).
- **data-and-analytics**: the **worker images** Argo templates run, plus shared model codegen. No orchestration code, no Argo Workflows client — its only "argo" hits are ArgoCD (GitOps).

## 2. Directory map (workflow-related)

```
InsightFILE/
├── apps/workflows-api/workflows_api/          FastAPI service wrapping Argo via Hera
│   ├── config.py                              Argo conn config: ARGO_WORKFLOWS_HOST/TOKEN(_PATH)/NAMESPACE/AUTH_MODE,
│   │                                          image pull secret, TTL (1d/2d), PodGC OnPodCompletion, tolerations
│   └── workflows/
│       ├── workflow.py                        Wraps raw Argo wf dict: status/uid/failure extraction (walks status.nodes)
│       ├── workflow_service.py                Hera WorkflowsService subclass; token re-read on file mtime change
│       ├── workflow_running/
│       │   ├── workflow_submitting.py         submit_any_workflow(): Workflow(workflow_template_ref).create(); 5xx retry (3x, exp backoff)
│       │   └── allowed_workflows.py           name → submit-fn map, ~23 prebaked WorkflowTemplates
│       ├── endpoints/legacy/endpoints.py      GET /workflow_status/{name_uid}; POST /workflow_submit
│       ├── endpoints/new/                     POST /workflows/submit, /workflows/compose/, /workflows/partition/,
│       │                                      /workflows/predict-tenant/, /task-templates/, /dag-templates/, /transformations/*, /health
│       ├── utils/workflow_builder.py          WorkflowBuilder: DAG → Hera Tasks → Workflow; auto-appends Finalize task
│       ├── utils/workflow_composer.py         compose_workflows(): attach SubmitTask to existing payload DAG
│       ├── userflow_translator/               Userflow (e.g. OMOP define-cohort, Atlas JSON) → WorkflowPayload
│       ├── models/                            pydantic models GENERATED (datamodel-codegen) from packages/types JSON schemas
│       └── tasks/
│           ├── __init__.py                    REGISTRY: TASK_TEMPLATES, TASK_BUILDERS, CONSUMES_* lists (static, hard-coded)
│           ├── magic_builder.py               Factory: builder.template() == dag_entry.template_id (linear scan)
│           ├── abstract/abstract_task_builder.py
│           └── <task>/                        21 task dirs: *TaskTemplate + *TaskBuilder each
├── apps/tasks/default-exit-handler/           CLIs invoked by Argo onExit → publish to RabbitMQ
├── apps/tasks/integration-tests/              Consumes workflows.out.* (tests/tools/config/default.ts:26)
├── apps/fitconnect/src/
│   ├── infra/clients/workflowsApi/client.ts   HTTP client for all workflows-api endpoints (axios-retry ×6, not on 500)
│   ├── infra/index.ts:34                      Boot wiring: WorkflowManager + OperationWorkflowManager.subscribeToWorkflowManager()
│   ├── services/workflows/WorkflowManager.ts  Submit + cron polling; emits WorkflowResponse
│   ├── services/operation/                    OperationWorkflowManager + workflow-adapters/* (Operation → WorkflowPayload)
│   ├── domain/operation/OperationTracking.ts  Persisted entity: status, correlationId, receipt, workflow outputs
│   └── routes/workflows-api-proxy/            Allow-listed HTTP proxy to workflows-api
└── packages/types/src/
    ├── tasks/**                               Zod schemas (*TaskUserInput / *TaskWorkflowInput) — THE CONTRACT
    └── registry.ts + generate.ts              zod registry → dist/json-schemas/*.json (input to Python codegen)

data-and-analytics/
├── plan.md, deployment/                       ArgoCD/Helm/GitLab-CI plumbing (no WorkflowTemplates here)
└── services/
    ├── finalize/                              'finalize' task image: temp→permanent S3, gzip, RSA-PSS sign, tag;
    │   │                                      writes metadata JSON to wf output params "read by FITConnect" (README:4)
    │   └── finalize/lib/models/               codegen'd FinalizeArtifact, WorkflowOutputArtifact (from packages/types)
    ├── omop_converter/                        Task image behind convert-to-omop / dataset-to-omop-template
    ├── omop_generator/                        Synthetic OMOP generation — FFAPP-4566 branch runs it on AZURE BATCH, not Argo
    └── pii_analysis/, probabilistic_matching/, integration_test_validator/, common/   further worker code
```

## 3. Task builder inventory (AST-verified, 22/22)

Discovery: **static registry** in `tasks/__init__.py` (`TASK_BUILDERS`, 21 entries + implicit Finalize). Lookup: linear scan `builder.template() == dag_entry.template_id` (magic_builder.py:9, workflow_builder.py:108). Output compatibility via `output_fits_into()` → `CONSUMES_DATASET_TASKS` / `CONSUMES_PICKLED_EMBEDDINGS_TASKS` / `CONSUMES_DIRECTORY_TASKS`.

`TemplateRef(name=argo_workflows_template_name(), template=<name minus '-template'>)`; three builders override the inner name (s3_export → `export-to-s3`, sparse_bf_encoding → `sparse-bf-encoding`, finalize → `finalize`).

| Template id (DAG `template_id`) | Argo WorkflowTemplate | User-input schema |
|---|---|---|
| load-data | load-data-task-template | LoadDataTaskUserInput |
| k-anonymise | k-anonymise-template | KAnonymityTaskUserInput |
| custom-transformations | custom-transformation-template | CustomTransformationTaskUserInput |
| data-profile | data-report-template | EmptyUserInput |
| merge-datasets | merge-multiple-datasets-template-new | MergeDatasetsTaskUserInput |
| concatenate-datasets | concatenate-two-datasets-template | ConcatenateDatasetsTaskUserInput |
| pii-identification-and-treatment | pii-identification-and-treatment-template | PIITreatmentTaskUserInput |
| sparse-bf-encoding | sparse-bf-encoding-task-template | SparseBfEncodingTaskUserInput |
| sparse-bf-comparer | sparse-bf-comparer-template | MergeSparseBfUserInput |
| convert-to-omop | dataset-to-omop-template | OmopConverterTaskUserInput |
| load-data-from-artifacts | load-artifact-task-template | LoadDataFromArtifactsTaskUserInput |
| load-artifact | load-artifact-task-template | LoadArtifactsUserInput |
| load-directory-from-artifacts | load-artifact-task-template | LoadDirectoryFromArtifactsUserInput |
| s3-export | export-to-s3-task-template | ExportToS3TaskUserInput |
| ohdsi-cohort-definition-to-sql-renderer | ohdsi-cohort-definition-sql-renderer-task-template | OhdsiCohortDefinitionSqlRendererTaskUserInput |
| run-sql | run-sql-task-template | RunSqlTaskUserInput |
| ohdsi-query-combiner | ohdsi-query-combiner-template | OhdsiCohortSqlCombinerTaskUserInput |
| omop-tables-reindexer | omop-tables-reindexer-template | OmopLinkageTaskUserInput |
| ude | ude-template | UDETaskUserInput |
| ohdsi-concept-query-builder | ohdsi-concept-query-builder-template | OmopConceptQueryGeneratorTaskUserInput |
| count-set-unions | count-set-unions-v2-template | CountSetUnionsTaskUserInput |
| finalize *(auto-appended, never in user DAGs)* | new-finalize | EmptyUserInput |

Argument mechanics (worked example `MergeTaskBuilder`): `arguments = user_inputs ∪ outputs ∪ additional_arguments()`. Outputs are deterministic S3 keys `{path_prefix}/{dag_entry.id}_dataset.json`; `path_prefix` defaults to the workflow uid — literally `"{{workflow.uid}}"` for Argo substitution. Upstream outputs are wired by re-instantiating the predecessor's builder (magic_builder) and reading its `outputs` — **dataflow is by S3-key convention, not Argo artifact passing**.

## 4. Two submission paths

**A — prebaked** (`POST /workflow_submit`): `allowed_workflows_map[name]` (query, identifiable-query, reidentify-query, validate, query-no-ude, merge, merge-and-k-anonymise, medcat-annotation, load-and-python-script, submit-mesh-request, opt-out-mesh-response, load-and-bloom-filter-encrypt, load-and-probabilistic-intersection, load-and-uniquify-by-primary-key, load-ude-and-uniquify-by-primary-key, load-and-count-set-unions, run-sql-query, concat, concat-and-k-anonymise, specific-transformations, load-and-custom-transformations, nhs-pet-and-privacy-treatment-workflow, move-dataset-workflow) → `submit_any_workflow()` builds Hera `Workflow` with `workflow_template_ref` + flat `Parameter` list → `.create()` (REST to Argo server). `correlation_id` travels as an ordinary workflow parameter. *(21 `submit_any_workflow` call sites AST-verified; `submit_load_ude_and_uniquify_by_primary_key` defined twice.)*

**B — custom DAG** (`POST /workflows/submit`): `WorkflowValidator` → `WorkflowBuilder.build_and_submit_a_workflow()` → Hera `Workflow`+`DAG`, one `Task` per entry, dependencies rewired from `depends_on` ids, Finalize task auto-appended depending on all → `.create()`.

Retry: workflows-api retries only 5xx (3×, exp backoff); fitconnect axios ×6 but never on workflows-api 500s.

## 5. Result flow — polling is primary; RabbitMQ path looks vestigial

**Polling (live path).** `WorkflowManager.startPolling` schedules cron task `workflow-poll-${correlationId}` (`singleton: true` = dedup guard) hitting `GET /workflow_status/{name}` until terminal. Status endpoint falls back to `get_archived_workflow(uid)` on 404 and merges `workflow-failures` (top-down walk of `status.nodes`, last child only of Retry nodes) into `output_parameters`. `OperationWorkflowManager.handleWorkflowResponse` finds `OperationTracking` **by `receipt.uid`** (not correlation id), adapter processes outputs (finalize metadata arrives via wf output params), persists Completed/Failed. On boot, `repollOperationTracking` re-arms polling for all Running operations. Exactly one production listener registration exists (`workflowManager.on('*', …)` — AST-verified).

**Exit handlers (queue path).** Both CLIs only publish one RabbitMQ message (exchange `amq.topic`, routing key `workflows.out.<status>`) — no DB writes, no dataset mutation:
- `exit_handler.py` → status, failures (note **double** `json.loads` — arrives doubly-encoded, consistent with Argo `{{workflow.failures}}` as quoted param), correlation-id, wf id/name.
- `validate_dataset_exit_handler.py` → same + dataset-id, validation-summary-path, and `failed_validation_count` read from a local summary file.

Which Argo variables feed which CLI flags **cannot be confirmed from these repos** — the `onExit` YAML isn't here. By convention: `{{workflow.status}}`→`--workflow-status`, `{{workflow.failures}}`→`--workflow-failures`, `{{workflow.uid}}`→`--workflow-id`, `{{workflow.name}}`→`--workflow-name`, `{{workflow.parameters.correlation-id}}`→`--correlation-id` — *inference, flagged as such*. Only source-visible consumer of `workflows.out.*`: integration tests. fitconnect retains queue config (`responseTopicPattern`) but has **no AMQP consumer** — it moved to HTTP polling.

## 6. Shared contract between repos

Single source of truth: **`InsightFILE/packages/types`**.
1. **TS**: zod schemas `src/tasks/**` consumed by fitconnect adapters via `@fitfile/types`.
2. **JSON Schema**: `generate.ts` serialises the zod registry → `dist/json-schemas/*.json`.
3. **Python (both repos)**: `datamodel-codegen` → pydantic models in `workflows-api/.../models/` and in data-and-analytics task services (e.g. `finalize/lib/models/FinalizeArtifact.py`; manual command in finalize README:34-43).

data-and-analytics shares the *data* contract, not a code dependency.

## 7. End-to-end sequence (representative merge operation)

1. Frontend/GraphQL → fitconnect `OperationWorkflowManager.run()`: fetch schemas, create `OperationTracking` (correlationId from request frame), adapter builds `WorkflowPayload`.
2. `WorkflowManager.startWorkflow()`: input files → temp S3 bucket; POST `/workflow_submit` (named) or `/workflows/submit` (custom DAG).
3. workflows-api validates; resolves via `allowed_workflows_map` or runs `WorkflowBuilder` over the registry, appending Finalize.
4. Hera POSTs to Argo server (`ARGO_WORKFLOWS_HOST`, token from `ARGO_WORKFLOWS_TOKEN_PATH`/`ARGO_WORKFLOWS_TOKEN`); `metadata.uid/name` return as **receipt**, saved on OperationTracking.
5. Argo controller instantiates pods from the referenced WorkflowTemplates (images from data-and-analytics `services/*` and InsightFILE `apps/tasks/*`); tasks exchange data via convention S3 keys.
6. Finalize task (data-and-analytics `services/finalize`) moves kept artifacts to permanent S3, gzips/signs/tags, writes metadata JSON into wf output parameters.
7. Cluster-defined `onExit` runs `default-exit-handler` → RabbitMQ `workflows.out.<status>` (observed consumer: integration tests only).
8. fitconnect cron poller sees terminal status, builds `WorkflowResponse`, finds OperationTracking by `receipt.uid`, adapter registers outputs, marks Completed/Failed.

## 8. Open questions / gaps

1. **No Argo WorkflowTemplate YAMLs in either repo** — every template name is a dangling reference; task→image mapping, `onExit` wiring, and parameter substitution live in the ArgoCD infra repo.
2. **Custom workflows set no exit handler** — `WorkflowBuilder` never sets `on_exit`; Path B relies on polling + Finalize only.
3. **RabbitMQ response path appears abandoned in production** — confirm nothing outside these repos consumes `workflows.out.*` before treating as test-only. (ffcloud, scheduler-service, frontend not audited.)
4. **Fragile inner-template derivation** — `replace('-template','')` yields e.g. `merge-multiple-datasets-new`; unverifiable against YAML.
5. **Three builders share `load-artifact-task-template`**, differing only in arguments.
6. **Code smells**: duplicate abstract `outputs` property in `AbstractTaskBuilder`; `submit_load_ude_and_uniquify_by_primary_key` defined twice; unused `thing` var in `magic_builder`.
7. **Correlation-id is not the lookup key** on the return path (`receipt.uid` is); no submission-side idempotency key exists.
8. **FFAPP-4566 (`omop_generator`) is a third execution universe** — Azure Batch, bypassing Argo and workflows-api entirely; relevant if OMOP generation should ever become a workflows-api task like `omop_converter`.

## Methodology note

- ast-grep (1MCP) structural queries: 22/22 `argo_workflows_template_name` returns; 22/22 `TaskTemplate.id` values; 21 `submit_any_workflow` call sites; single production `workflowManager.on('*')` listener.
- 1MCP LSP find-references/implementations calls failed (`-32603`, language servers not started for these workspaces) — those checks fell back to earlier direct file reads.
- Everything else from direct reads of the cited files (paths + line numbers in the body).