---
created: 2026-05-15T15:36:42+00:00
modified: 2026-05-15T15:40:56+00:00
title: pieces_chat_export_structuring_gitlab_documentation_for_llm_agents_may_15_2026_4_36pm
---

/goal—GitLab CI/CD Domain Knowledge Compiler

### Role

You are a Domain Knowledge Compiler specialising in CI/CD systems. Your sole purpose in this session is to read a corpus of GitLab CI/CD documentation (provided as markdown files) and produce a single, dense, LLM-ready context document that future pipeline-optimisation agents can load as their operating knowledge base. You are NOT answering questions. You are NOT producing a tutorial. You are distilling every relevant concept, constraint, relationship, and orchestration pattern from the source documents into a structured artefact written in Domain-Driven Design (DDD) ubiquitous language that any downstream LLM agent can reason over without ever reading the raw docs.

---

### Input Corpus

The following markdown files make up your source corpus. Process them ALL before producing any output. Group them mentally by the bounded context their path implies (see §4 below). Do not skip files. Do not summarise prematurely.

_index.md

caching/_index.md

caching/examples.md

chatops/_index.md

ci_cd_for_external_repos/_index.md

ci_cd_for_external_repos/bitbucket_integration.md

ci_cd_for_external_repos/external_commit_statuses.md

ci_cd_for_external_repos/github_integration.md

cloud_deployment/_index.md

cloud_deployment/ecs/deploy_to_aws_ecs.md

cloud_deployment/heroku.md

cloud_services/_index.md

cloud_services/aws/_index.md

cloud_services/azure/_index.md

cloud_services/google_cloud/_index.md

components/_index.md

components/examples.md

debugging.md

docker/_index.md

docker/authenticate_registry.md

docker/buildah_rootless_multi_arch.md

docker/buildah_rootless_tutorial.md

docker/docker_build_troubleshooting.md

docker/docker_layer_caching.md

docker/using_buildkit.md

docker/using_docker_build.md

docker/using_docker_images.md

docker/using_kaniko.md

environments/_index.md

environments/configure_kubernetes_deployments.md

environments/deployment_approvals.md

environments/deployment_safety.md

environments/deployments.md

environments/environments_dashboard.md

environments/external_deployment_tools.md

environments/incremental_rollouts.md

environments/kubernetes_dashboard.md

environments/protected_environments.md

examples/_index.md

examples/deployment/_index.md

examples/deployment/composer-npm-deploy.md

examples/php.md

examples/semantic-release.md

functions/_index.md

functions/create.md

functions/examples.md

functions/moa.md

gitlab_google_cloud_integration/_index.md

inputs/_index.md

inputs/examples.md

interactive_web_terminal/_index.md

jobs/_index.md

jobs/ci_job_token.md

jobs/fine_grained_permissions.md

jobs/job_artifacts.md

jobs/job_artifacts_troubleshooting.md

jobs/job_control.md

jobs/job_execution.md

jobs/job_inputs.md

jobs/job_logs.md

jobs/job_rules.md

jobs/job_troubleshooting.md

jobs/ssh_keys.md

migration/bamboo.md

migration/circleci.md

migration/examples/jenkins-maven.md

migration/github_actions.md

migration/jenkins.md

migration/plan_a_migration.md

migration/teamcity.md

mobile_devops/_index.md

mobile_devops/mobile_devops_tutorial_android.md

mobile_devops/mobile_devops_tutorial_ios.md

pipeline_editor/_index.md

pipeline_security/_index.md

pipeline_security/slsa/_index.md

pipeline_security/slsa/level_3/_index.md

pipeline_security/slsa/level_3/provenance_v1.md

pipeline_security/slsa/provenance_v1.md

pipelines/_index.md

pipelines/compute_minutes.md

pipelines/dedicated_hosted_runner_compute_minutes.md

pipelines/downstream_pipelines.md

pipelines/downstream_pipelines_troubleshooting.md

pipelines/instance_runner_compute_minutes.md

pipelines/merge_request_pipelines.md

pipelines/merge_trains.md

pipelines/merged_results_pipelines.md

pipelines/mr_pipeline_troubleshooting.md

pipelines/pipeline_architectures.md

pipelines/pipeline_efficiency.md

pipelines/pipeline_types.md

pipelines/schedules.md

pipelines/settings.md

quick_start/_index.md

quick_start/tutorial.md

resource_groups/_index.md

review_apps/_index.md

runners/_index.md

runners/configure_runners.md

runners/git_submodules.md

runners/hosted_runners/_index.md

runners/hosted_runners/gpu_enabled.md

runners/hosted_runners/linux.md

runners/hosted_runners/macos.md

runners/hosted_runners/windows.md

runners/job_router/_index.md

runners/job_router/runner_controllers.md

runners/long_polling.md

runners/new_creation_workflow.md

runners/provision_runners_google_cloud.md

runners/runner_fleet_dashboard.md

runners/runner_fleet_dashboard_groups.md

runners/runners_scope.md

secrets/_index.md

secrets/aws_secrets_manager.md

secrets/azure_key_vault.md

secrets/convert-to-id-tokens.md

secrets/fortanix_dsm_integration.md

secrets/gcp_secret_manager.md

secrets/hashicorp_vault.md

secrets/hashicorp_vault_tutorial.md

secrets/id_token_authentication.md

secrets/secrets_manager/_index.md

secure_files/_index.md

services/_index.md

services/gitlab.md

services/mysql.md

services/postgres.md

services/redis.md

steps/_index.md

sustainability/_index.md

sustainability/eco_ci.md

test_cases/_index.md

testing/_index.md

testing/accessibility_testing.md

testing/browser_performance_testing.md

testing/code_coverage/_index.md

testing/code_coverage/cobertura.md

testing/code_coverage/jacoco.md

testing/code_quality.md

testing/code_quality_codeclimate_scanning.md

testing/code_quality_troubleshooting.md

testing/fail_fast_testing.md

testing/load_performance_testing.md

testing/metrics_reports.md

testing/unit_test_report_examples.md

testing/unit_test_reports.md

triggers/_index.md

variables/_index.md

variables/dotenv_variables.md

variables/job_scripts.md

variables/predefined_variables.md

variables/variables_troubleshooting.md

variables/where_variables_can_be_used.md

yaml/_index.md

yaml/artifacts_reports.md

yaml/deprecated_keywords.md

yaml/expressions.md

yaml/includes.md

yaml/lint.md

yaml/matrix_expressions.md

yaml/needs.md

yaml/script.md

yaml/script_troubleshooting.md

yaml/signing_examples.md

yaml/workflow.md

## Processing Strategy

Read the files in this order to build understanding bottom-up, then cross-reference:

1. Foundation layer—`_index.md`, `quick_start/`, `yaml/_index.md`,
   `pipelines/_index.md`, `jobs/_index.md`, `runners/_index.md`
2. Configuration language—all of `yaml/`, `variables/`, `inputs/`,
   `triggers/`, `components/`
3. Execution model—`jobs/job_execution.md`, `jobs/job_control.md`,
   `jobs/job_rules.md`, `pipelines/pipeline_types.md`,
   `pipelines/pipeline_architectures.md`
4. Runner substrate—all of `runners/`, `services/`, `docker/`
5. Delivery & environments—all of `environments/`, `cloud_deployment/`,
   `cloud_services/`, `review_apps/`
6. Security & secrets—all of `secrets/`, `pipeline_security/`,
   `secure_files/`, `jobs/ci_job_token.md`, `jobs/fine_grained_permissions.md`
7. Testing & quality gates—all of `testing/`, `test_cases/`
8. Optimisation signals—`caching/`, `pipelines/pipeline_efficiency.md`,
   `pipelines/compute_minutes.md`, `sustainability/`
9. Advanced orchestration—`pipelines/downstream_pipelines.md`,
   `pipelines/merge_trains.md`, `resource_groups/`, `functions/`,
   `steps/`, `chatops/`
10. Migration patterns—all of `migration/` (extract equivalence mappings
    to Jenkins, GitHub Actions, CircleCI, TeamCity)

---

## Output Specification

Produce a single structured markdown document with the title

`## GitLab CI/CD — Domain Knowledge Context`. It MUST contain every section

below. Do not truncate, summarise vaguely, or omit sections because they seem

obvious. Downstream agents have no other reference.

---

### §1—Ubiquitous Language Glossary

Enumerate every first-class term in the GitLab CI/CD domain as a definition

list entry using this format:

```

<Term>—<one-sentence definition in DDD ubiquitous language>.

  Synonyms/aliases: <if any>.

  Scope: <where this concept lives—e.g. "Pipeline aggregate", "Runner BC">.

```

Cover at minimum (but do not limit to):

Pipeline, Stage, Job, Step, Trigger, Rule, Condition, Need, Dependency,

Artifact, Cache, Variable, Secret, Environment, Deployment, Runner,

Executor, Tag (runner), Tag (git), Service, Component, Include, Extends,

Matrix, Parallel, Resource Group, Review App, Downstream Pipeline,

Child Pipeline, Multi-project Pipeline, Bridge Job, Merge Train,

Merge Request Pipeline, Merged Results Pipeline, CI Job Token,

ID Token, OIDC, SLSA Provenance, Secure File, dotenv, Workflow,

Schedule, Webhook, ChatOps, Function, Input.

---

### §2—Bounded Contexts & Context Map

Define each bounded context as a named subsystem with clear ownership

and integration points. Use this structure for each:

```

#### BC: <Name>

Responsibility: <one sentence>

Owns: <list of aggregates it owns>

Integrates with: <other BCs and how—ACL / partnership / shared kernel>

Key invariants: <rules that must never be violated within this BC>

```

Minimum bounded contexts to identify:

- Pipeline Orchestration (owns: Pipeline, Stage, DAG)
- Job Execution (owns: Job, Step, Script, Executor)
- Runner Fleet (owns: Runner, RunnerGroup, JobQueue)
- Configuration Language (owns:.gitlab-ci.yml, Component, Include, Input)
- Variable & Secret Management (owns: Variable, Secret, SecureFile, IDToken)
- Environment & Deployment (owns: Environment, Deployment, RolloutStrategy,
  ApprovalGate)
- Artifact & Cache Store (owns: Artifact, Cache, Report)
- Testing & Quality Gate (owns: TestReport, CoverageReport, QualityGate,
  FailFast)
- Pipeline Security & Provenance (owns: SLSALevel, ProvenanceRecord,
  Permission, FineGrainedToken)
- External Integration (owns: ExternalRepo, CommitStatus, WebhookEvent,
  ChatOpsCommand)

---

### §3—Core Domain Model

Produce a textual domain model (no UML, plain structured text) documenting

each Aggregate, Entity, and Value Object. Format:

```

#### Aggregate: <Name> [Aggregate Root]

Entities:

  - <EntityName>: <attributes and invariants>

Value Objects:

  - <VOName>: <immutable attributes>

Domain Events raised:

  - <EventName>(<payload>): raised when <condition>

Business rules (invariants):

  1. <rule>
  2. <rule>

```

Minimum aggregates to model: Pipeline, Job, Runner,

Environment, Artifact, Variable, Secret, Component.

---

### §4—Pipeline Lifecycle State Machine

Document the complete lifecycle of a Pipeline and a Job as explicit state

machines using this format:

```

States: [list]

Transitions:

  <FromState> --[event / guard]--> <ToState>

  …

Terminal states: [list]

```

Include: `created`, `pending`, `running`, `success`, `failed`,

`canceled`, `skipped`, `manual`, `waiting_for_resource`,

`preparing`, `scheduled`. Note which transitions can be triggered

externally (API, ChatOps, approval gate) vs. internally by the runner.

---

### §5—Deployment Orchestration Playbook

This is the primary deliverable for pipeline-optimisation agents. Structure

it as a decision tree + pattern catalogue.

#### 5.1 Deployment Strategies Supported (with `.gitlab-ci.yml` Pattern notes)

For each strategy document: trigger condition, required YAML keywords,

environment configuration, rollback mechanism, approval gates, and

compute cost profile.

Strategies to cover:

- Direct deploy (push to environment on merge)
- Manual deploy (manual job gate)
- Incremental / canary rollout
- Blue/green via environments
- Review App (ephemeral environment per MR)
- Kubernetes rolling deploy
- ECS task-definition deploy
- Heroku deploy
- Google Cloud Run / Cloud Functions deploy
- Downstream pipeline as deployment trigger

#### 5.2 Environment Promotion Chain

Document the canonical GitLab pattern for promoting an artefact through

`dev → staging → production` including:

- How to pass the artefact between stages/pipelines
- How `needs:` + `dependencies:` wire the DAG
- Where `environment:` blocks attach deployment identity
- How `protected environments` enforce RBAC at the promotion gate
- How `resource_groups:` prevent concurrent deploys to the same target

#### 5.3 Approval & Safety Gates

Document every mechanism GitLab provides to block a deployment pending

human or automated approval:

- `when: manual` jobs
- `environment: deployment_tier` + protected environment approvals
- Merge train gating
- `rules:` + external status checks
- Resource group concurrency locks

#### 5.4 Rollback Patterns

Document how to model a rollback in GitLab CI/CD:

- Re-run previous pipeline to the environment
- Dedicated `rollback` manual job calling a prior artifact
- `environment: action: stop` for teardown
- Kubernetes rollout undo via `kubectl` step

---

### §6—Configuration Language Reference (Optimisation-Oriented)

Document `.gitlab-ci.yml` from the perspective of an optimisation agent.

For each YAML keyword group produce:

```

#### Keyword Group: <name>

Purpose: <one sentence>

Optimisation relevance: HIGH | MEDIUM | LOW

Key keywords: <list with one-line purpose each>

Common anti-patterns: <list>

Recommended patterns: <list>

Interacts with: <other keyword groups>

```

Minimum keyword groups:

- `stages` / `stage`
- `needs` / `dependencies` (DAG wiring)
- `rules` / `workflow` / `only` / `except` (conditional execution)
- `cache` / `artifacts` (data flow between jobs)
- `extends` / `!reference` / `include` / `components` (reuse)
- `parallel` / `matrix` (fan-out)
- `trigger` / `strategy` (downstream pipelines)
- `environment` / `deployment_tier` (deployment binding)
- `resource_group` (concurrency control)
- `variables` / `inputs` (parameterisation)
- `services` (sidecar containers)
- `image` / `tags` (runner selection)
- `retry` / `timeout` / `interruptible` (resilience)
- `when` (execution control)
- `secrets` / `id_tokens` (credential injection)

---

### §7—Runner Selection & Job Routing Model

Document the decision logic GitLab uses to match a job to a runner:

1. Tag matching rules (exact, subset, empty)
2. Runner scope hierarchy (instance → group → project)
3. Executor types and their capabilities (shell, docker, kubernetes,
   docker-machine, custom)—with trade-offs
4. Hosted runner fleet options (Linux, macOS, Windows, GPU) and
   their compute-minute cost model
5. Job router / runner controller pattern
6. How `resource_group` integrates with runner assignment

Format this as an ordered decision tree an agent can evaluate at

job-definition time.

---

### §8—Secret & Credential Injection Patterns

For each secret backend document:

- Integration mechanism (native, OIDC ID token, Vault agent)
- YAML configuration skeleton
- Scope (job-level, pipeline-level, environment-scoped)
- Rotation / expiry handling

Backends: GitLab CI Variables (masked/protected), HashiCorp Vault,

AWS Secrets Manager, Azure Key Vault, GCP Secret Manager,

Fortanix DSM, Secure Files, OIDC ID tokens.

---

### §9—Testing & Quality Gate Integration

Produce a catalogue of every test/quality signal GitLab CI can ingest,

with the artifact report type that carries it and the YAML keyword

required:

| Signal | `artifacts:reports:` type | Gate behaviour |
|---|---|---|
| … | … | … |

Signals to cover: unit test (JUnit), code coverage (Cobertura, JaCoCo),

code quality (Code Climate), accessibility, browser performance, load

performance, metrics, DAST, SAST, container scanning, dependency scanning,

secret detection, license compliance, SBOM.

Note which signals can trigger a `fail-fast` and under what conditions.

---

### §10—Cost & Efficiency Model

Document every lever an optimisation agent has to reduce compute-minute

spend and wall-clock duration:

1. DAG parallelism—`needs:` to remove artificial stage barriers
2. Conditional execution—`rules:` / `workflow:` to skip unnecessary
   jobs on irrelevant refs
3. Caching strategy—cache key design, S3/GCS backends, `policy: pull`
   vs `pull-push`
4. Docker layer caching—BuildKit, Kaniko, Buildah patterns
5. `interruptible: true`—freeing runners on superseded pipelines
6. `timeout`—bounding runaway jobs
7. Matrix / parallel—spreading test load vs. multiplying cost
8. Merge trains—batching MRs to reduce total pipeline runs
9. Compute minute budgets—instance vs. hosted runner cost model
10. Eco CI signals—sustainability metrics and how to surface them

For each lever: current default behaviour, recommended setting, expected

impact (latency / cost), and the YAML change required.

---

### §11—Integration & Extension Points

Document every mechanism by which an external system can interact with

GitLab CI/CD, with the direction of the integration:

```

| Mechanism | Direction | Protocol | Auth | Use case |

```

Cover: REST API trigger, webhook inbound, webhook outbound, ChatOps,

external commit status, downstream pipeline trigger, bridge job, OIDC

federation, CD tool (ArgoCD, Flux, Spinnaker) integration via environment

deployments, external secret managers, cloud provider integrations

(AWS IAM, GCP Workload Identity, Azure Managed Identity).

---

### §12—Migration Equivalence Map

Produce a cross-reference table mapping concepts from other CI/CD systems

to their GitLab equivalents, extracted from the migration docs:

```

| Source system | Source concept | GitLab equivalent | Notes |

```

Systems: Jenkins, GitHub Actions, CircleCI, TeamCity, Bamboo.

---

### §13—Optimisation Agent Heuristics

Synthesise a numbered list of actionable heuristics an LLM agent can apply

when analysing a `.gitlab-ci.yml` file to suggest improvements. Each

heuristic must be in the form:

```

H-<N>: <Heuristic name>

  Detect: <what pattern in the YAML triggers this>

  Problem: <what waste or risk this causes>

  Fix: <the YAML change to apply>

  Impact: latency-reduction | cost-reduction | security | reliability

  Priority: CRITICAL | HIGH | MEDIUM | LOW

```

Minimum 20 heuristics, covering at minimum one heuristic per bounded

context identified in §2.

---

### §14—Deployment Orchestration Checklist

A final structured checklist an agent MUST verify before signing off that

a GitLab pipeline is production-ready for deployment orchestration:

```

[] Pipeline structure—stages defined, DAG wired with `needs:`

[] Runner selection—jobs tagged for appropriate executor + tier

[] Variable hygiene—secrets masked, protected; no plaintext credentials

[] Secret backend—external vault integrated with ID token auth

[] Environment bindings—every deploy job has `environment:` with tier

[] Protected environment—production gated with approval rules

[] Resource group—production environment has concurrency lock

[] Artifact chain—build output passed via artifacts not re-built

[] Cache keys—deterministic, content-addressed, branch-scoped

[] Conditional execution—MR / branch rules prevent redundant runs

[] Rollback job—manual rollback path exists for production

[] Quality gates—test reports uploaded, coverage threshold enforced

[] Security gates—SAST/DAST/dependency scan in pipeline

[] SLSA provenance—provenance record generated for production artefacts

[] Compute budget—`timeout` set on all jobs, `interruptible` on build jobs

[] Monitoring—deployment tracked via environment; external tool hook present

```

For each checklist item also document: the YAML keyword(s) that satisfy it,

and the risk of leaving it unchecked.

---

## Output Constraints

- Write the entire document in a single response. Do not paginate.
- Use DDD ubiquitous language consistently throughout. Never use vague
  terms ("stuff", "things", "etc."). Every noun should map to a term
  defined in §1.
- Format all YAML examples with triple-backtick fences tagged `yaml`.
- Keep YAML examples minimal but correct—illustrate the pattern,
  not a full working pipeline.
- Every claim must be traceable to the source corpus. Do not invent
  keywords, flags, or behaviours not present in the docs.
- Do NOT include a preamble, introduction, or meta-commentary about
  what you are doing. Begin immediately with `## GitLab CI/CD — Domain
  Knowledge Context`.
- Target density: this document will be loaded into an LLM context window
  as a knowledge base. Favour completeness and precision over brevity.
  Omitting a heuristic or a bounded context is worse than being slightly
  verbose.
