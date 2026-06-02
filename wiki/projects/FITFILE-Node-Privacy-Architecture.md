---
title: FITFILE Node — Privacy Architecture & Data Processing
wiki_type: dossier
entity_kind: project
created: 2026-06-02T10:51:00+00:00
modified: 2026-06-02T10:51:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-06-02-pieces-fitfile-node-privacy-architecture
---

## Summary

Email chain (June 2026) between FITFILE leadership (Philip Russmeyer, Weronika Jastrzebska), technical staff (Enric, Robin), governance (David Reeves), and the EoE/EaHSN data harmonisation workstream (Laura), discussing FITFILE Node data processing architecture, privacy treatments, and NHS data governance. Triggered by Laura's concern that existing architecture diagrams insufficiently clarify where direct identifiers exist and where privacy treatments are applied. Open technical questions have been escalated to Leon and Ollie regarding data ephemerality during Node processing.

## Key Facts

- **2026-06-02**: Laura (EoE/EaHSN) raised concerns after meetings with CUH and WSH that architecture diagrams don't sufficiently clarify (a) what direct identifiers are present at any point, and (b) where each privacy treatment is applied — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

- **2026-06-02**: Philip reviewed Laura's referenced deck, found issues with FITFILE Node data storage depiction and ambiguous "OMOP and Data Extract" arrows, drafted amendments (Slides 6–13) and a parallel Miro diagram, circulated for feedback ahead of Monday noon deadline — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

### Processing Environments

- **Native Database Environment**: All operations expressible as database queries (column selection, row-level filtering, aggregation, SQL/FQL) execute here with no data movement — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

- **FITFILE Node Compute Environment**: Used only where database-native processing is not reasonably applicable. A transient, ephemeral copy of relevant data is staged to Node local storage for: FITanon/FITtoken generation, privacy treatment (K-anonymity, L-diversity), data profiling, small number suppression — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

- **Federated Deployment Model**: FITFILE deploys within the organisational perimeter, as close to the data source as possible. Node compute environment is physically adjacent to data — no network boundary crossing. Transient copy resides on same physical infrastructure as source database — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

### Governance & Legal Terminology (David Reeves)

- NHS Numbers *are* transferred for NDOO purposes — the claim "no identifiable data stored in FITFILE Nodes" is inaccurate — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

- Correct legal terminology is **pseudonymised / anonymised**, not a blanket "identifiable / not identifiable" binary — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

- Key legal/regulatory concept is *processing*, not *storing*. The "no storage" headline is a useful security control but does not resolve governance questions — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

### NDOO (National Data Opt-Out) — Agreed Position

- Data Controllers expected to perform NDOO before secondary use; FITFILE also performs NDOO as "belts and braces" — **both parties do it** — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

### Philip's Key Unresolved Architectural Question

> "Does a FITFILE Node take a temporary copy of identifiable data into itself in order to e.g. do a count, to execute The Hyve code, or to privacy treat it — **or** are the processing instructions from the Node executed on the dataset *in situ* outside of the Node?"

No answer on record. Not about Project Extract flows (where ephemeral in-flight storage is understood) — about standard query/processing operations — [[raw/2026-06-02-pieces-fitfile-node-privacy-architecture]] (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

## Timeline

- **2026-06-02**: Laura raises architecture diagram concerns with Philip
- **2026-06-02**: Philip drafts amendments (Slides 6–13) and Miro diagram, circulates for feedback
- **2026-06-02**: Robin formalises Enric's technical processing summary for Technical Solution Detail doc
- **2026-06-02**: Open questions escalated to Leon & Ollie (data ephemerality, transient storage details)
- **Deadline: Monday noon** — response to Laura due

## Connections

- [[FITFILE-Testing-Infrastructure]] — FITFILE Azure testing environment infrastructure work
- [[gcx CLI — FITFILE Grafana Stacks]] — FITFILE monitoring infrastructure

## Contradictions

- **NDOO positioning across slides**: Slide 7 shows NDOO before the FITFILE Node; other slides show it within the Node. Philip's position: both are correct (dual-layer), but inconsistency needs to be resolved in diagrams.

- **"No identifiable data" claim**: David Reeves asserts NHS Numbers are transferred for NDOO, directly contradicting the "no identifiable data stored" claim. This is accepted as inaccurate but not yet resolved in the diagrams.

## Open Questions

1. **Where is the transient data copy stored during Node processing?** (MinIO? Encrypted at rest?) — *From Robin, escalated to Leon & Ollie*
2. **Until when is transient data retained?** (Query plan complete? Explicitly deleted? Other?) — *From Robin, escalated to Leon & Ollie*
3. **Is data re-fetched fresh each query run, or can it persist across runs?** — *From Robin*
4. **How transient is "transient"?** Concrete time window or benchmark for external stakeholders? — *From Philip*
5. **How automated is data destruction** after Node processing completes? — *From Philip*
6. **Can Robin's rewrite be updated with current detail?** Enric's original document dates from May 2025 and may be stale — *From Philip*
7. **Why "applicable" vs "possible"** in the Node Compute section? Robin queried this editorial choice — *Unresolved*
8. **Restricted Terms application timing**: OMOP ETL stage or before? — *Directed at Weronika*
9. **SDE Node Query Interface**: Should SDE Data Manager use the SDE Node for PRE queries? — *Philip pushed back, needs clarifying*
10. **Does Node process data in situ or take a temporary copy?** — *Philip's key question, no answer on record*
