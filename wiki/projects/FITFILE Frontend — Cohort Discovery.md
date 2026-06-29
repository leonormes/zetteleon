---
title: FITFILE Frontend — Cohort Discovery
wiki_type: dossier
entity_kind: project
created: 2026-06-08 19:22:00+00:00
modified: 2026-06-08 19:22:00+00:00
tags:
- wiki
- dossier
- project
sources:
- raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery
permalink: llmeon/wiki/projects/fitfile-frontend-cohort-discovery
---

## Summary

Frontend workstream on the FITFILE platform covering cohort discovery screens — the user-facing interface for defining patient cohorts across multiple data sources (GP Records, NHS Digital, Hospital Admissions) with intersection/union visualisation. Built as a Next.js (TypeScript, App Router) application with routes under `src/app/project/[id]/new-operation/`, gated by feature flags and served across multiple deployments (testing at `ff-test-a.fitfile.net`, production AWSSDE at `app.eoe-sde-codisc.privatelink.fitfile.net`).

## Key Facts

- **FITFILE frontend is a Next.js application** (TypeScript, App Router). The "New Operation" entry point at `ff-test-a.fitfile.net/fitfile/project/<id>/new-o…` presents the cohort discovery workflow — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **Route structure**: `src/app/project/[id]/new-operation/` is the root, with `data-extract/[userflowId]/layout.tsx` wrapping the cohort discovery userflow and `custom-transformations/layout.tsx` adjacent — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **Key components**: Data disclosure confirmation modal (`EnableDataDisclosureConfirmModal.tsx`), GraphQL networking hook (`useGraphQL.ts`), Faro telemetry provider (`FaroProvider.tsx`), and env abstraction (`fitfileEnv.ts`) — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **`CohortData` TypeScript type** defined by Pavlo Kotov (15 Apr 2026 standup wireframing) including `total`, `sources` (GP, NHS, Hospital), and `pairs` (union intersections following Oliver Rushton's `0_1` → `A_B` convention) — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **Feature flags**: `features.updateQueryPlan` and `features.updateDataDisclosure` gate cohort-related screens, injected via `AppConfigProvider.tsx` / `getAppConfigEnv.ts`, configured per-deployment in ArgoCD / ffnode Helm values — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **Active Jira tickets** driving the work: FTFL-494 (union counts via entity resolution), FTFL-501 (full cohort component), FTFL-502 (integrate into OMOP flow), FTFL-496 (new artifact type), FTFL-31 (parent epic, 65% done) — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

- **Live deployments**: Testing at `ff-test-a.fitfile.net`; production AWSSDE at `app.eoe-sde-codisc.privatelink.fitfile.net` with audit log event type `CohortDiscoveryUsingFI` — [[raw/2026-06-08-pieces-fitfile-frontend-cohort-discovery]] (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

## Timeline

- **2026-04-15** — Pavlo Kotov wireframes the `CohortData` n3Fixture during standup
- **2026-06-08** — Architecture documentation compiled via Pieces LTM recall; "Select the type of operation" screen captured in Teams listing Cohort Discovery as first operation type

## Connections

- [[wiki/projects/FITFILE-Testing-Infrastructure]] (same testing environment `ff-test-a.fitfile.net`)
- [[wiki/projects/FITFILE-Node-Privacy-Architecture]] (sister FITFILE workstream, data governance)
- [[Grafana Alloy Monitoring — FTFL-638]] (monitoring on the same testing cluster)

## Contradictions

*None identified.*

## Open Questions

- What is the current state of FTFL-494 (union counts) — is the visualisation shipped or still in development?
- Has the `useGraphQL.ts` error on line 48 been resolved since the standup debugging session?
- What is the relationship between the AWSSDE deployment and the `ff-test-a` testing environment — are they on the same release cadence?