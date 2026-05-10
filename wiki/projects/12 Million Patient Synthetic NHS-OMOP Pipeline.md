---
created: 2026-04-28T16:55:00+00:00
entity_kind: project
modified: 2026-05-08T21:15:00+00:00
sources: [raw/2026-04-28-pieces-omop-stress-testing-plan.md, raw/2026-05-08-pieces-omop-ticket-context.md]
tags: [dossier, wiki]
title: 12 Million Patient Synthetic NHS-OMOP Pipeline
wiki_type: dossier
---

## Summary

A FITFILE project to generate and stress-test synthetic NHS OMOP data at scale (up to 12 million patients). The pipeline uses Synthea-style generation, produces five node-level Parquet datasets, and is preparing for infrastructure, algorithmic, and ETL stress tests. Work is tracked across multiple Jira epics (FTFL-475, FTFL-476, FTFL-479, FTFL-480, FTFL-488) and involves integration with The Hyve ETL tooling.

## Key Facts

- Five node datasets are ready for stress testing as Parquet files, one per node.

  > "I produced 5 sets of parque files for 5 nodes" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: 0fe5dae4-33da-4080-b4d1-c99cf0e01a4f)

- Jira tickets framing the work: FTFL-475 (synthetic data generation script), FTFL-476 (stress testing infrastructure + monitoring), FTFL-479 (database ingestion script), FTFL-480 (test userflow script), FTFL-488 (synthetic OMOP data storage).

  > "FTFL-475: Script to generate OMOP synthetic data / FTFL-476: OMOP Stress Testing infra + monitoring / FTFL-480: OMOP Stress Testing - script to create test userflows" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: a09cf70e-29e6-4c79-95ec-5c8023042db8)

- Architectural planning spans ~6 weeks (since early April), with a key meeting block on Thu Apr 16 (~9:28 AM–12:08 PM and 2:00–3:00 PM) that established test dimensions and failure hypotheses.

  > "Your LTM consistently separates stress testing into Infrastructure, Algorithmic/Workflow, and ETL/Hyve pipeline concerns (esp. Apr 16 discussions about 'what aspect are we stress testing?')" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

- Test dimensions cover Infrastructure, Algorithmic/Workflow, and ETL/Hyve pipeline.

  > "Your memories show three distinct test dimensions already established: 1. Infrastructure Stress (FTFL-476) … 2. Algorithmic Stress (FTFL-480 Permutation Testing) … 3. Hyve ETL Stress (from Design Document)" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: 63c8006e-9139-4915-ad68-e29496520114)

- Permutation variables: cohort size, selection scope (tables/fields), privacy treatment (k-anonymity / nullification ON/OFF), extract cap (capped/uncapped), and linkage scenario (single node → two nodes → five nodes).

  > "Cohort size (C): {1k, 10k, 100k, 1M, NodeFull, 5NodeFull} … Privacy (P): {Off, On} … Linkage scenario (L): L1 Single node / L2 Two nodes … / L3 Five nodes" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

- Known failure points include: multi-node federation cliffs, DB reindexer OOM, privacy treatment destroying referential integrity, algorithmic tracing/linkage bottlenecks, vocabulary/concept mapping gaps, and run failure recovery for long jobs.

  > "Multi-node federation cliffs … DB reindexer / heavy maintenance OOM … Privacy treatment destroying referential integrity … Algorithmic tracing / linkage bottlenecks" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

- Monitoring requirements (FTFL-476) must surface: system/container metrics (CPU, memory, disk, network), DB metrics (connections, lock waits, query latencies), and workflow-level stage timings + error taxonomy.

  > "System / container: CPU, Memory, Disk, Network … Database: Active connections, queue depth, query runtime … Workflow / application-level: Run ID, scenario ID, stage timings, error taxonomy" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

- Data quality gates (WhiteRabbit profiling, Achilles distribution checks, DQD) should run before any load tests to avoid "garbage in, garbage out".

  > "Pre-flight quality gates (run before any load): Schema checks + overlap stats + Achilles/WhiteRabbit. Stop condition: any node failing integrity gates blocks load tests until fixed." — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

- Hyve integration remains a critical dependency with open questions on output target (ideally Postgres), throughput at 100k/1M/node-size, feasible schedule (daily/weekly), and governance correctness under load.

  > "What is the output (ideally Postgres)? … How long does OMOP take (daily/weekly/hourly updates)? … Governance correctness under load" — [[raw/2026-04-28-pieces-omop-stress-testing-plan]] (Pieces: dbb82172-1e30-4150-82c5-9f03a378e935)

## Connections

_(none yet—populated as related dossiers and concepts are ingested)_

## Contradictions

_(none flagged)_

## Open Questions

- Overlap engineering: are the 5 node datasets currently disjoint, or do they share engineered Person_IDs for realistic linkage testing?
- What is the concrete query harness for FTFL-480 userflows: FITFILE workflow runner, direct SQL scripts, or Atlas / Achilles-driven queries?
- When will the Hyve ETL pipeline be ready to ingest Parquet/CSV, and what is the agreed SLA for stage runtimes?
- What are the exact resource envelopes (CPU, memory, disk, network) per node for the stress-test environment?
- How will long-run failure recovery be implemented to satisfy RAP/auditability expectations?
