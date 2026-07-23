---
title: FITFILE Workflow Codebase — Complete Map & Analysis
date: 2026-07-23
tags:
- fitfile
- argo-workflows
- workflows-api
- fitconnect
- architecture
- data-structures
permalink: llmeon/wiki/projects/fitfile-workflow-codebase-complete-map-analysis
---

# FITFILE Workflow Codebase — Complete Map & Analysis

**Last updated:** 2026-07-23  
**Scope:** InsightFILE (workflows-api, fitconnect, packages/types) + data-and-analytics (services) + Deployment (Argo templates)  
**Verification:** ast-grep structural queries + Cursor canvas analysis + direct file reads

## Quick Facts

| Metric | Value |
|--------|-------|
| Active task builders | 22 + auto-appended Finalize |
| Submit paths | 2 (legacy templated, custom DAG) |
| Confirmed template mismatch | 1 (concatenate) |
| Active completion method | HTTP polling |
| WorkflowTemplate YAMLs in these repos | 0 (Deployment/deployment/workflows) |

## Directory Structure

**InsightFILE:**
- `apps/workflows-api/workflows_api/` — FastAPI wrapping Argo via Hera
  - `config.py` — Argo connection config
  - `workflows/workflow.py` — Wraps Argo workflow dict
  - `workflows/workflow_service.py` — Hera WorkflowsService (mtime-refreshing token)
  - `workflows/workflow_running/` — Prebaked template submissions
  - `workflows/endpoints/` — REST API (compose, submit, status, partition, templates)
  - `workflows/utils/workflow_builder.py` — Hera DAG + auto-appends Finalize
  - `workflows/tasks/` — 22 task builders + TaskTemplate registry
- `apps/fitconnect/src/` — Application layer
  - `infra/clients/workflowsApi/client.ts` — HTTP client (axios-retry x6)
  - `services/workflows/WorkflowManager.ts` — Submit + polling
  - `services/operation/OperationWorkflowManager.ts` — Operation→Workflow adapters
  - `domain/operation/OperationTracking.ts` — Persisted tracking entity
- `apps/ffcloud/src/` — Multi-tenant supervisor
- `packages/types/src/` — Zod schemas, JSON Schema, generated pydantic
  - `src/tasks/**` — *TaskUserInput, *TaskWorkflowInput
  - `registry.ts, generate.ts` — Codegen
- `apps/tasks/default-exit-handler/` — RabbitMQ publishers (legacy)

**data-and-analytics:**
- `services/data_and_analytics/` — Transform CLIs (merge, concat, k-anon, etc.)
- `services/finalize/` — Output promotion + metadata
  - `lib/models/` — Codegen FinalizeArtifact, WorkflowOutputArtifact
- `services/omop_converter/` — OMOP + OHDSI SQL
- `services/probabilistic_matching/` — Sparse BF encode/compare
- `services/pii_analysis/` — PII treatment
- `services/common/` — Shared IO, transformationEngine

**Deployment/deployment/workflows:**
- `charts/tasks/templates/` — Task WorkflowTemplates (~50)
- `charts/query/templates/` — Composite named workflows
- `values.yaml` — Image tags, exit-handler config, tolerations

## Task Registry (22+1)

| Builder | template_id | Argo Template | Inner | Input | Outputs | can_start | Match |
|---------|------------|--------------|-------|-------|---------|-----------|-------|
| LoadDataTaskBuilder | load-data | load-data-task-template | load-data-task | LoadDataTaskUserInput | dataset_json_out_key, schema_json_out_key | true | ✓ |
| KAnonymiseTaskBuilder | k-anonymise | k-anonymise-template | k-anonymise | KAnonymityTaskUserInput | dataset/schema/report | false | ✓ |
| CustomTransformationsTaskBuilder | custom-transformations | custom-transformation-template | custom-transformation | CustomTransformationTaskUserInput | dataset_json_out_key, schema_json_out_key | false | ✓ |
| DataProfilerTaskBuilder | data-profile | data-report-template | data-report | EmptyUserInput | summary_json_out_key | false | ✓ |
| MergeTaskBuilder | merge-datasets | merge-multiple-datasets-template-new | merge-multiple-datasets-new | MergeDatasetsTaskUserInput | dataset_output_json_key, schema_output_json_key | false | ✓ |
| ConcatenateTaskBuilder | concatenate-datasets | concatenate-two-datasets-template | concatenate-two-datasets | ConcatenateDatasetsTaskUserInput | dataset_json_out_key, schema_json_out_key | false | ⚠️ MISMATCH |
| PiiTreatmentTaskBuilder | pii-identification-and-treatment | pii-identification-and-treatment-template | pii-identification-and-treatment | PIITreatmentTaskUserInput | dataset/schema/report/summary | false | ✓ |
| SparseBfEncodingTaskBuilder | sparse-bf-encoding | sparse-bf-encoding-task-template | sparse-bf-encoding (override) | SparseBfEncodingTaskUserInput | pickle_df, embedding paths | false | ✓ |
| MergeSparseBfTaskBuilder | sparse-bf-comparer | sparse-bf-comparer-template | sparse-bf-comparer | MergeSparseBfUserInput | output_matching, output_similarities | false | ✓ |
| OmopConverterTaskBuilder | convert-to-omop | dataset-to-omop-template | dataset-to-omop | OmopConverterTaskUserInput | output_directory | false | ✓ |
| LoadDataFromArtifactsTaskBuilder | load-data-from-artifacts | load-artifact-task-template | load-artifact-task | LoadDataFromArtifactsTaskUserInput | dataset_json_out_key, schema_json_out_key | true | ✓ (shared) |
| LoadArtifactTaskBuilder | load-artifact | load-artifact-task-template | load-artifact-task | LoadArtifactsUserInput | dataset_pickle, embedder_pickle | false | ✓ (shared) |
| LoadDirectoryFromArtifactsTaskBuilder | load-directory-from-artifacts | load-artifact-task-template | load-artifact-task | LoadDirectoryFromArtifactsUserInput | output_directory | true | ✓ (shared) |
| S3ExportTaskBuilder | s3-export | export-to-s3-task-template | export-to-s3 (override) | ExportToS3TaskUserInput | {} | true | ✓ |
| OhdsiCohortDefinitionSqlRendererTaskBuilder | ohdsi-cohort-definition-to-sql-renderer | ohdsi-cohort-definition-sql-renderer-task-template | ohdsi-cohort-definition-sql-renderer-task | OhdsiCohortDefinitionSqlRendererTaskUserInput | sql_out_key | true | ✓ |
| RunSqlTaskBuilder | run-sql | run-sql-task-template | run-sql-task | RunSqlTaskUserInput | dataset_json_out_key, schema_json_out_key | true | ✓ |
| OhdsiCohortSqlCombinerTaskBuilder | ohdsi-query-combiner | ohdsi-query-combiner-template | ohdsi-query-combiner | OhdsiCohortSqlCombinerTaskUserInput | sql_out_key | true | ✓ |
| OmopReindexerTaskBuilder | omop-tables-reindexer | omop-tables-reindexer-template | omop-tables-reindexer | OmopLinkageTaskUserInput | output_s3_directory | false | ✓ |
| UdeTaskBuilder | ude | ude-template | ude | UDETaskUserInput | dataset_json_out_key, schema_json_out_key | false | ✓ |
| OmopConceptQueryGeneratorTaskBuilder | ohdsi-concept-query-builder | ohdsi-concept-query-builder-template | ohdsi-concept-query-builder | OmopConceptQueryGeneratorTaskUserInput | sql_out_key | true | ✓ |
| CountSetUnionsTaskBuilder | count-set-unions | count-set-unions-v2-template | count-set-unions-v2 | CountSetUnionsTaskUserInput | cohort_discovery_out_key | false | ✓ |
| FinalizeTaskBuilder | finalize | new-finalize | finalize (override) | EmptyUserInput | {} | false | ✓ (auto-appended) |

**Notes:** Rows 11–13 share load-artifact-task-template. Row 6 (Concatenate) has confirmed mismatch.

## Confirmed Issues

### Q1: Concatenate template name mismatch
Builder targets `concatenate-two-datasets-template`; Deployment is `concatenate-multiple-datasets-template`. TemplateRef mismatch confirmed.

### Q2: Exit-handler Argo wiring not found
CLIs + Rabbit publishers exist. Custom WorkflowBuilder does NOT set onExit. No onExit references in Deployment task/query YAMLs.

### Q3: No workflows.out consumer in FitConnect
Exit handlers publish to amq.topic routing key workflows.out.<status>. FitConnect has stale Rabbit config but no active consumer.

### Q4: LoadArtifactTaskBuilder.output_fits_into() returns None
Method should return a list of consumer tasks, not bare [].

### Q5: Three repos hold workflow pieces
InsightFILE = orchestration API. data-and-analytics = task CLIs. Deployment = WorkflowTemplate YAMLs. fitfile-workflows = Hera authoring (sibling). YAMLs not in the two primary repos.

## Data-Centric Priorities (Linus Torvalds Philosophy)

See separate notes: [[Workflow System — Data-Centric Analysis (Linus Philosophy)]]

**Top refactors:**
1. **R1:** Prebaked workflow table — Replace 23 functions with one YAML data structure
2. **R2:** Task registry consolidation — One keyed record per task, enable CI template validation
3. **R6:** Canonical completion schema — Same field names everywhere, decouple polling from queue
4. **R3:** Discriminated union user_inputs — Type-safe at API boundary
5. **R4/R5:** Reify edges + id-keyed joins — High-impact, requires Argo template coordination

## Related Notes

- [[FITFILE Workflow Architecture — Argo + workflows-api Map]] — Original structural mapping
- [[Workflow System — Data-Centric Analysis (Linus Philosophy)]] — Data design critique + refactoring blueprint