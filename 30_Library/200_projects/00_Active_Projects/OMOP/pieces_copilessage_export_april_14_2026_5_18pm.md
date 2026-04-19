---
Based on your long-term memories from the past ~32 hours, no — the distributed architecture is justified for 12 million patients. The complexity you're dealing with isn't from over-engineering the solution; it's from the inherent difficulty of stabilizing a distributed data pipeline. Let me break down what I found:
created: 2026-04-14T16:18:20+00:00
modified: 2026-04-19T18:30:38+00:00
title: pieces_copilessage_export_april_14_2026_5_18pm
---

## Why Synthea/ETL Takes So Long

From your [Gemini conversation on Azure Batch](https://gemini.google.com/app/2a060af3041f6531) (~9:53 AM yesterday), the core bottlenecks were identified as:

| Bottleneck | Cause |
|------------|-------|
| JVM Overhead | Synthea runs on Java; startup and memory management are slow per-batch |
| Vocabulary Mapping | The R-based `ETLSyntheaBuilder` package performs heavy vocabulary lookups |
| Database I/O | Loading millions of rows into ephemeral MSSQL containers is write-intensive |
| Memory Pressure | Your worker-0 was killed (`exit -9`) during `CONCEPT_RELATIONSHIP.csv` loading due to OOM |

The Gemini analysis explicitly stated:

> "Generating millions of patients (e.g., 10 million) on a single machine is too slow due to JVM overhead, R-based vocabulary mapping, and heavy database I/O."

---

## Your Architecture Is Sound

The blueprint you've designed addresses the real bottlenecks:

1. Golden Vocabulary Archive (Phase A)—Pre-filtering and uploading `omop-vocab-golden.tar.gz` once means workers don't rebuild vocabularies independently. This is a major optimization.
2. ID Remapping via SQL Projection—The `effective_id = original_id + (batch_index × 1,000,000,000)` formula applied during export (not via `UPDATE` statements) is the correct, stateless approach.
3. Azure Batch Fan-Out—For 12 million patients, you'd need ~120 workers at 100K patients each. This is textbook embarrassingly parallel compute—Azure Batch is the right tool.

---

## What's Actually Causing Your Pain

The memories from today show you're in the integration debugging phase, not an architecture problem:

| Time | Issue | Root Cause |
|------|-------|------------|
| ~11:45 AM | `libodbc.so.2` missing | Bootstrap script missing `unixodbc-dev` package |
| ~12:16 PM | Synthea output path mismatch | `batch-worker` wrote to a different dir than `SyntheaService.generate()` expected |
| ~1:30 PM | OOM kill (`exit -9`) | Memory pressure during chunked vocab load |
| ~4:13 PM | `Cannot insert NULL into 'concept_name'` | R's `na.strings` coercing empty strings to SQL `NULL` |

These are all environment and edge-case bugs, not architectural failures.

---

## The Feedback Loop Problem (Your Real Frustration)

At ~4:13 PM today, you wrote:

> "Can't we run tests locally with identical containers before doing the long slow batch jobs? Each run takes 10s of mins to fail. The feedback cycle is too long."

This is the core issue. Your agent responded by creating:

- [local_smoke_worker.sh](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Application/data-and-analytics/services/omop_generator/scripts/azure_batch/local_smoke_worker.sh)—Local preflight harness
- [build_local_worker_image.sh](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Application/data-and-analytics/services/omop_generator/scripts/azure_batch/build_local_worker_image.sh)—Prebaked Docker image builder
- [local_smoke_worker_image.sh](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Application/data-and-analytics/services/omop_generator/scripts/azure_batch/local_smoke_worker_image.sh)—Runs the smoke test against the prebaked image

---

## My Assessment

| Question | Answer |
|----------|--------|
| Is Azure Batch overkill? | No—12M patients is too large for a single machine |
| Is `omop-cli` over-engineered? | No—The ID remapping, golden vocab, and batch-worker subcommand are all justified |
| Why does it feel complicated? | You're debugging environment parity issues, not design flaws |
| What would simplify things? | Get the local smoke test passing before submitting to Azure Batch |

---

## Recommended Next Steps

1. Finish stabilizing the prebaked Docker image—Your agent was building it at ~4:57 PM today. This eliminates dependency drift between local and Azure.
2. Run the 2-worker local simulation—You requested this at ~4:14 PM. This validates the ID offset merge logic without waiting for Azure.
3. Increase worker VM size—Your `Standard_D2s_v3` (8GB RAM) hit OOM during vocab load. Consider `Standard_D4s_v3` (16GB) for headroom.
4. Lock the vocab chunking—The `OMOP_VOCAB_CHUNK_ROWS=50000` setting was introduced to reduce memory footprint. Verify it's wired into the image.

You're not overcomplicating—you're just in the messy middle of making a distributed system reliable.
