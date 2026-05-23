---
title: GitOps Deployment Pipeline Optimisation
wiki_type: dossier
entity_kind: project
created: 2026-05-23T12:52:00+00:00
modified: 2026-05-23T12:52:00+00:00
tags: [wiki, dossier]
sources: [raw/2026-05-23-pieces-natural-planning-model.md]
---

## Summary

Project to investigate and incrementally optimise a live GitOps deployment pipeline while it remains in active use by the engineering team. Changes must be small and incremental — no big-bang replacements. Success measured via the Four Key Metrics (deployment frequency, lead time, MTTR, change fail rate).

## Key Facts

- **Goal:** Investigate current GitOps process, then incrementally optimise without disrupting team delivery — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Non-negotiables:** No disruption to team's ability to ship; small incremental changes only; no big-bang pipeline replacement — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Success vision:** Immediate developer feedback, seamless ArgoCD reconciliation, zero config drift — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Key metrics:** Four Key Metrics — deployment frequency, lead time, mean time to restore, change fail percentage — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Investigation focus:** Current state vs documented state; queues and waiting times (tests, environment provisioning, PR approvals) — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Architecture concerns:** CI/CD architecture review, trunk-based dev vs long-lived branches, secrets management in K8s — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Phasing:** Phase A: Value stream mapping + metric baseline → Phase B: CI feedback loop (parallelise test suites) → Phase C: CD sync policies & manifest management — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Next action identified:** Schedule 60-min value stream mapping session to trace a single commit from workstation to production, OR run query to extract average build times for last 30 days — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)
- **Risk:** A malformed in-flight pipeline change could break deployment capabilities; rollback plan needed — [[raw/2026-05-23-pieces-natural-planning-model]] (Pieces: 201d6e29-282f-4295-8bf1-44282a6752d3)

## Timeline

- 2026-05-23: Project scoped using Natural Planning Model; investigation phase defined

## Connections

- [[wiki/projects/K8s Cluster Stress Testing with OMOP Data]] — sister project from same planning session
- [[Azure Entra ID IAM → IaC + PIM Migration]] — sister project from same planning session
- [[Grafana Alloy Monitoring — FTFL-638]] — observability stack that may inform pipeline monitoring

## Contradictions

None identified.

## Open Questions

- What is the current value stream map of the GitOps pipeline?
- Where are the longest queues/waiting times?
- What test suites can be parallelised in Phase B?
- How will pipeline changes be communicated to the team to avoid surprised developers?
