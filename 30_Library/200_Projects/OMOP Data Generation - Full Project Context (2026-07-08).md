---
created: 2026-07-08 00:00:00+00:00
modified: 2026-07-08 08:57:48+00:00
project_category: omop
project_name: OMOP
project_status: active
tags:
- azure-batch
- context-consolidation
- ffapp-4566
- fitfile
- ftfl-475
- ftfl-694
- ftfl-696
- ftfl-721
- omop
- synthea
tickets:
- FTFL-475
- FTFL-476
- FTFL-479
- FTFL-480
- FTFL-488
- FTFL-694
- FTFL-696
- FTFL-721
title: OMOP Data Generation - Full Project Context (2026-07-08)
type: null
permalink: llmeon/30-library/200-projects/omop-data-generation-full-project-context-2026-07-08
---

## Purpose of This Note

Consolidated context for the `omop_generator` codebase (`services/omop_generator` in the `data-and-analytics` repo, branch `feature/FFAPP-4566-OMOP-data-generation`), built by cross-referencing the repo itself, the existing Obsidian notes under `30_Library/200_Projects/`, `jira/`, `Work/`, and the raw Pieces-LTM captures under `raw/`. No live Pieces MCP/LTM tool was reachable in this session—the `raw/*-pieces-*.md` files (Pieces LTM exports saved manually into this vault) were used instead as the closest available substitute.

Related notes: [[OMOP Data Generation - Requirements]] · [[12 Million Patient Synthetic NHS-OMOP Pipeline]] · [[Expanded Analysis OMOP Synthetic Data Generation Project]] · [[Position Statement Clinical Fidelity in Synthetic OMOP Data Generation]] · [[NHS Synthetic Data & OMOP Pipeline Meeting]] · [[FTFL-696 Phase 0b Overlap Validation]] · [[FTFL-721 Phase 0c Cohort Design]]

---

## 1. What This Project is

A standalone CLI (`omop-cli`, console entrypoint `omop`) that generates synthetic OMOP CDM v5.4 patient data at scale, for two purposes:

1. Local dev/test fixtures—small, full-fidelity OMOP exports (10s–1000s of patients) for building ETL and analytics tooling without touching real NHS data.
2. National-scale stress testing—a 12-million-patient, multi-node synthetic dataset used to stress-test the FITFILE platform's cohort federation, linkage, and query performance (the "FFNode Stress Testing Programme", FTFL-694).

Origin ticket: FTFL-475 ("Script to generate OMOP synthetic data"), which pulled in four sibling tickets—FTFL-488 (blob storage), FTFL-479 (DB ingestion), FTFL-476 (multi-DB stress test infra + monitoring), FTFL-480 (stress test permutation runner)—see [[OMOP Data Generation - Requirements]] for the full requirements consolidation and dependency chain.

---

## 2. Architecture (As iMplemented)

Pipeline shape, from `Docs/OMOP_SYNTHETIC_DATA_PLAN.md`:

```
GENERATE  → Synthea (Java) produces Synthea CSVs, no DB required
ETL+EXPORT → Synthea CSVs + Athena vocab → ephemeral local Docker MSSQL
             → ETLSyntheaBuilder (R) → OMOP CDM tables
             → person-ID injection → export CDM to CSV → filter vocab
             → generate concept-distribution stats → tar.gz archive
SEED      → archive → target DB (MSSQL or PostgreSQL), idempotent
```

Key design decision: ETLSyntheaBuilder (R package) needs a _live_ database to transform Synthea output into OMOP CDM—it can't emit CSVs directly. The workaround is a throwaway local Docker MSSQL (Azure SQL Edge on Apple Silicon) used purely as an ETL engine; once ETL finishes, tables are exported to CSV and the container is disposable. This decouples generation from any specific target DB technology.

Implementation is a Python/Typer CLI (`src/omop_cli/`), not the originally-planned Bash scripts—chosen for robust subprocess handling, Pydantic "parse don't validate" config, and native Azure/DB SDKs. Command surface today (`src/omop_cli/commands/`): `generate`, `etl-export`, `seed`, `info`, `silo-split`, `upload`, `vocab`, plus two added on the current branch—`batch-worker` and `batch-merge-validate` (headless distributed generation, see §4).

Service layer (`src/omop_cli/services/`) covers Docker lifecycle, Synthea invocation, ETL patching, archive/manifest handling, atomic CSV writes, Azure upload, ID remapping, NHS post-processing, silo splitting, and vocab filtering—matching the phased plan in `OMOP_SYNTHETIC_DATA_PLAN.md` (Phases 1–7: core decoupling → seeding → cohort/vocab filtering → stats → person-ID injection → sub-cohort injection → Azure blob).

---

## 3. Scale-up: the 12M-patient / 5-node Pipeline

See [[12 Million Patient Synthetic NHS-OMOP Pipeline]] and [[Expanded Analysis OMOP Synthetic Data Generation Project]].

- Engine: `swpc_synthea` (UK fork), NICE guidelines, dm+d codes, GB geography.
- Target: 12M unique patients, ~12B clinical rows, ~60 TiB total footprint (raw FHIR ~26.4 TiB → Parquet ~2 TiB, a 13x reduction).
- Identity linkage: Master Person Service (MPS) logic in `nhs_post_process.py`—Cross-check, Alphanumeric (Soundex), Algorithmic tracing tiers; NDOO opt-out simulation via mock MESH API.
- Node split: data is partitioned into 5 nodes to mirror the real 5-trust SDE architecture, using a synthetic overlap model ("Model C") rather than the originally-discussed "70–85% single-trust" characterisation:

| Nodes per patient | Target % |
|---|---|
| 1 | 40% |
| 2 | 30% |
| 3 | 20% |
| 4 | 7% |
| 5 | 3% |

  Generated by `scripts/azure_batch/generate_subsample_synthea.py`: replicates the 2.7M source patients 5×, assigns each virtual patient to 1–5 nodes per Model C, sets `person_source_value = <uuid>-c{copy_idx}` as the cross-node linking key (since `person_id` is dataset-local), and hash-routes each patient's clinical records to exactly one of their assigned nodes.

- FTFL-696 (Phase 0b, done) validated this empirically: queried all 5 node Parquet files with a duckdb bitmask-signature query over `person_source_value`; all 26 exclusive node-combinations matched Model C targets within 0.03 points (13,549,015 unique virtual persons total). See [[FTFL-696 Phase 0b Overlap Validation]] for the full breakdown and the reusable SQL.
- FTFL-721 (Phase 0c, selected for dev, unassigned) is next: design/create OMOP cohorts for the "C" (cohort size) dimension of the stress-test permutation grid (1k/10k/100k/1M/NodeFull), hard-blocked on Phase 00 (node + DB + ingestion) being complete first.
- Both are sub-tasks of FTFL-694 ("FFNode Stress Testing Programme"), which itself operationalises FTFL-480's 6-variable permutation grid (C × S × E × P × X × L—cohort size, selection scope, extract cap, privacy, S3-export, linkage scenario).

### The Fidelity-vs-speed Tension (Important fRaming, not yet rEsolved in tOoling)

[[Position Statement Clinical Fidelity in Synthetic OMOP Data Generation]] and [[Expanded Analysis OMOP Synthetic Data Generation Project]] capture a real architectural disagreement from the April 2026 planning phase:

- You (documented position) argued for clinically realistic data—messy demographics, missing/superseded NHS numbers, name variation—because the linkage/MPS logic can only be validated against realistic error rates, and skipping this risks Type-1 errors (pipeline works on clean synthetic data, breaks on real data).
- The team's decision (Ollie Rushton et al., 16 Apr meeting) prioritised volume/speed for infrastructure stress-testing: realistic _cohort overlap_ is enough, individual record realism is not required for this phase.
- You committed to the team's decision while flagging it as a tactical win at the expense of strategic robustness. This is still the operating assumption—Model C's overlap engineering (§3 above) is exactly the "realistic overlap, not realistic records" compromise that shipped. Worth re-raising if/when linkage-accuracy validation becomes a stated goal.

---

## 4. Current Branch Work: Azure Batch Distributed Generation (FFAPP-4566)

Branch `feature/FFAPP-4566-OMOP-data-generation`, recent commits:

- `143efe9`—headless `batch-worker` command for distributed OMOP generation
- `06709b0`—`batch-merge-validate` command + Azure Batch config docs
- `da43a0c`—Docker init / Synthea output handling improvements for Batch workers
- `592f00c`—prebaked worker images + local smoke test suite (current HEAD)

This is the execution layer that runs the generation pipeline as parallel Azure Batch tasks instead of one long local run:

- `omop batch-worker`—one worker's headless generation+ETL+export, driven by env vars (`BATCH_INDEX`, `POPULATION`, `VOCAB_BLOB_URL`, `OUTPUT_BLOB_URL`, …).
- `omop batch-merge-validate`—downloads N workers' `cdm-batch-N.tar.gz` outputs and validates the merged result: no PK collisions across batches, key FK relationships hold.
- `scripts/azure_batch/*.sh` / `*.py`—bootstrap, pool/job/task submission, prebaked Docker image build (`build_local_worker_image.sh`), local 1and 2-worker smoke runners that mirror the Batch task locally (see `Docs/local_prebaked_smoke.md`), cleanup, subsample/parquet conversion, refresh-and-resubmit helper (`refresh_batch_tasks.sh`).
- Full step-by-step 2-worker POC is documented in `Docs/azure_batch_poc_runbook.md`, including known gotchas (bootstrap script needs `env` before `apt-get`, tasks need `elevationLevel: admin`, `JOB_ID` must be exported not just set).

### Azure Resources in Use (From raw/2026-06-03-pieces-omop-azure-storage.md)

| Resource | Name | Notes |
|---|---|---|
| Resource group | `omop-synthetic-rg` | UK South, created 2026-04-14, subscription "FITCloud Non-Production" |
| Storage account | `omopstorage12345` | StorageV2, Standard LRS |
| Blob container | `omop-synthetic-data` | Parquet outputs (114 files, ~61.5 GB across 5 nodes at time of capture) |
| Blob container | `omop-reference-data` | Golden vocab archive (`omop-vocab-golden.tar.gz`) |
| Blob container | `omop-code-packages` | Source tarball for Batch workers (`omop_generator-src.tar.gz`) |
| Blob container | `omop-worker-output` | Per-worker `cdm-batch-N.tar.gz` outputs |
| Batch account | `omopbatch12345` |—|
| Container registry | `omopacr0414172753` |—|

### ⚠️ Naming Collision to Be Aware of

A separate, unrelated piece of work—a k8s `rust-chart-manager` Helm-rewriting CLI (Grafana `k8s-monitoring`/Alloy `ImagePullBackOff` investigation, see `Work/FFAPP-4566 k8s-monitoring Alloy ImagePullBackOff Investigation and v4.1.6 Upgrade.md`)—is also tagged FFAPP-4566 in this vault, dated 2026-06-24. It lives in a different repo (`Tools/rust-chart-manager`) and has nothing to do with OMOP generation. Treat that note as a red herring for this project unless it turns out FFAPP-4566 is a shared umbrella ticket spanning both efforts—worth confirming in Jira directly.

---

## 5. Local Dev Workflow (Small-scale)

From the repo `README.md`:

- `uv run omop etl-export --population 10 --vocab-dir <athena> --cdm-out-dir./out/omop-cdm-10`—full local confidence test, needs Docker + Java 17 + R + an Athena vocab download.
- `--reuse-db --reuse-vocab --reset-cdm`—fast iteration: keep vocab loaded, wipe only clinical tables between runs (avoids the "everything piled up" duplicate-person_id problem from stale `--reuse-db` runs).
- Performance notes worth remembering: vocab reload is slow but `--reuse-vocab` doesn't skip ETLSyntheaBuilder's own vocab-map rebuild (`create_source_to_standard_vocab_map` etc.), which is "many minutes" regardless; `insert_drug_era` scales with population; Synthea itself pays a large one-time JVM/module-scan cost per run.
- England mode maintains `.omop-workdir/synthea-id-to-nhs-map.csv` so `person.person_source_value` always resolves to an NHS number even across cohort UUID changes.

---

## 6. Open Items / Risks Worth Tracking

1. FTFL-721 (Phase 0c cohort design)—unassigned, blocked on Phase 00 completion; needed before the Phase 2 stress-test harness can reference concrete cohorts.
2. `omock` R package (mentioned in LTM as "rapid unit testing before the 30 TiB production run")—ownership and scope (schema validation? referential integrity? concept mapping coverage?) was never clarified between FITFILE and The Hyve.
3. Reproducibility/determinism of the seed-offset (1,000,003) scheme across 30 parallel workers—no confirmed answer on whether a crashed worker resumes with the same seed or skips to the next offset. Matters for RAP (Reproducible Analytical Pipeline) compliance.
4. Clinical-fidelity debt—Model C solves overlap realism, not record-level realism (messy demographics, name variants, superseded NHS numbers). If linkage-accuracy validation becomes a requirement, the current dataset likely needs a fidelity pass, per the Position Statement in §3.
5. FFAPP-4566 ticket ambiguity—confirm in Jira whether this ticket number is genuinely shared between the OMOP generation work and the unrelated `rust-chart-manager`/Alloy work, or whether one of the two vault notes has a mis-tagged ticket ID.
6. Working tree currently has several uncommitted/untracked artefacts at the repo root that look like local scratch state rather than intended commits: `.calnotes/notes.db`, `metadata.db`, large `synthea23m/*.csv*`/`.lzo` data files, and worker stdout/stderr logs one directory up. Worth a deliberate `.gitignore` pass before these accidentally get committed.

---

## 7. Source Index

Repo docs read (`services/omop_generator/`): `README.md`, `Docs/Plan.md`, `Docs/OMOP_SYNTHETIC_DATA_PLAN.md`, `Docs/azure_batch_poc_runbook.md`, `Docs/local_prebaked_smoke.md`.

Vault notes read:

- [[OMOP Data Generation - Requirements]]
- [[12 Million Patient Synthetic NHS-OMOP Pipeline]]
- [[Expanded Analysis OMOP Synthetic Data Generation Project]]
- [[Position Statement Clinical Fidelity in Synthetic OMOP Data Generation]]
- [[NHS Synthetic Data & OMOP Pipeline Meeting]]
- [[FTFL-696 Phase 0b Overlap Validation]]
- [[FTFL-721 Phase 0c Cohort Design]]
- `raw/2026-05-08-pieces-omop-ticket-context.md`, `raw/2026-06-03-pieces-omop-azure-storage.md`, `raw/2026-05-14-pieces-omop.md`, `raw/2026-04-28-pieces-omop-stress-testing-plan.md` (raw Pieces LTM exports)
- `Work/FFAPP-4566 k8s-monitoring Alloy ImagePullBackOff Investigation and v4.1.6 Upgrade.md` (unrelated project, same ticket tag—see §4 caveat)
- `30_Library/200_Projects/SoT - Work Open Loops.md` (checked but stale—carried forward from 2026-06-05, doesn't mention FFAPP-4566/FTFL-696/721)

Not available in this session: no live Pieces MCP/LTM tool was connected (only `piecesdb.json` and the manually-saved `raw/*-pieces-*.md` exports exist locally); the in-session `1mcp` memory knowledge graph was empty for all OMOP-related queries.