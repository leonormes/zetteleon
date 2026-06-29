---
title: K8s Cluster Stress Testing with OMOP Data
wiki_type: dossier
entity_kind: project
created: 2026-05-23 12:52:00+00:00
modified: 2026-05-23 12:52:00+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-23-pieces-natural-planning-model.md
permalink: llmeon/wiki/projects/k8s-cluster-stress-testing-with-omop-data
---

## Summary

Summer engineering project to validate stability and resilience of distributed Kubernetes clusters under large OMOP (Observational Medical Outcomes Partnership) clinical data loads. Planned using the GTD Natural Planning Model to overcome initiation difficulty on this high-friction technical work.

## Key Facts

- **Goal:** Validate cluster stability and resilience under large OMOP data loads — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Non-negotiables:** Data privacy compliance, zero disruption to production workloads, compute cost cap — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Success vision:** Comprehensive cluster behaviour report, clearly identified breaking points, tuned cluster configuration — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Required expertise:** DevOps engineers, data scientists familiar with OMOP common data model, network specialists — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Key risks:** Cascading cluster crashes, data corruption during stress test, out-of-memory errors — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Tooling:** Grafana/Prometheus for monitoring, load generation tools, K8s compute node scaling — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Next action identified:** Draft email to DevOps lead to schedule whiteboard session on K8s load testing parameters — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Planning framework:** GTD Natural Planning Model (Purpose & Principles → Vision → Brainstorm → Organise → Next Action) — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 201d6e29-282f-4295-8bf1-44282a6752d3)

## Timeline

- 2026-05-23: Project scoped using Natural Planning Model; next action identified

## Connections

- [[cicd-tooling-validated]] — sister project from same planning session
- [[Azure Entra ID IAM → IaC + PIM Migration]] — sister project from same planning session
- [[12 Million Patient Synthetic NHS-OMOP Pipeline]] — related OMOP data pipeline project

## Contradictions

None identified.

## Open Questions

- Which specific OMOP data distributions should be used for realistic load testing?
- What is the compute cost cap agreed with stakeholders?
- Who is the DevOps lead to contact for the initial whiteboard session?
- What load generation tooling is preferred (e.g. Locust, k6, custom)?