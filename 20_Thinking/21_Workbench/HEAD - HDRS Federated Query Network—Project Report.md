---
aliases: []
AoL: Work
candidate_answers: []
closing_condition: false
conformant: true
created: 2026-09-28T15:48:25+00:00
modified: 2026-09-28T15:48:33+00:00
own_words: true
permalink: llmeon/20-thinking/21-workbench/head-2026-09-28-1648
related_claims: []
sources: []
status: open
tags: [prodos/head, state/thinking]
tension: ''
title: HEAD - 2026-09-28 1648
type: question
---

## HDRS Federated Query Network—Project Report

This report consolidates the board's content on the HDRS (Health Data Research Spaces) federated query network. It captures deliverables, evolving architecture, open questions, and risks to guide mid-December and end-of-project milestones.

### Project Overview & Deliverables

Mid-project (mid-December):

- M1: Harmonisation live at two sites. Synthetic CKD dataset mapped to OMOP CDM at EE-SDE and at least one other SDE (target: North West; alternative: West Midlands). OHDSI DQD run at both; publish conformance/completeness against thresholds. Record-level acceptance: 100% structural conformance; defined convention/domain-mapping thresholds; CKD targets ≥95% for normalised creatinine, eGFR, ACR, uACR; ≥90% KDIGO stage derivability.
- M2: Cross-SDE federated query. Execute an OMOP-standard cohort via FITFILE Node routing between the two SDEs; reconcile to known synthetic composition; initial appraisal by AstraZeneca.
- M3: Deployment pattern documentation. Draft sent to all four SDEs and HDRS, aligned to multi-SDE blueprint; completeness checklist (infrastructure prerequisites, harmonisation pipeline, DQ reporting, Node configuration); comment by March 2027.

End-project:

- Connect 3–4 SDEs; run a query on synthetic data from each; deliver finalised outputs above.
- Licensing: Open under Open Government Licence v3.0—multi-SDE deployment pattern documentation, OMOP mapping spec (with The Hyve), DQ scoring methodology and reporting templates (draft at December gateway; full at close).
- Not open: FITFILE Node remains proprietary background IP. HDRS and UK secure environments receive a perpetual, worldwide, royalty-free licence to the open outputs.

### Network Architecture & Topology

- Landscape: Pharma as external consumer; SDEs—West Midlands, Eastern England (Coordinator), North West, South West (provisional). EE has bidirectional links to peers. Open questions: "Who is running the Query?", "Where is prior documentation for WestMids?", "How is data going to be delivered to the Pharma? PRE?"
- Evolved design: Adds a PRE connected to EE. Introduces a "Private FITFILE Network / HSCN" layer with Network Directory and Auto Discovery; designed for deployment in isolated networks. All SDEs connect into this layer.
- Constraint: Queries cannot be fanned out through intermediaries; the query network has only one layer.
- Iteration in progress: Additional placeholder nodes ("D", "SOUTH") indicate ongoing topology design.

### Detailed Layered Architecture

- Data assets layer managed (incl. The Hyve) above FITFILE nodes at SDEs.
- Source processing/source systems layers with FITFILE at each SDE; EE shows an Asset Integration Layer.
- Researcher access via PRE.
- Service provision: "Insights on Linked, Privacy-Treated Data" to partners (e.g., AstraZeneca, a London university).
- FITFILE provides routing/federation across all SDEs.

### Problems & Root Problems

- Problems: P2P topology doesn't scale; heavy Bastion/Firewall layers raise costs; providers can't see results from their node; exponential connection costs; need zero-trust security.
- Root problems: Public networking; multi-tenant infra management doesn't scale; federated authorisation complexity; concern from Leon about scaling data source linking (related to authorisation).

Solutions: To be defined.

### Stakeholder & Governance Elements

- Governance topic flagged: "Privileges."
- Repeated unresolved items: "Who is running the Query?", West Midlands documentation location, data delivery path to Pharma/PRE.
