---
title: FITFILE Frontend — Cohort Discovery Architecture
created: 2026-06-08T17:51:40.820Z
source: pieces-ltm
pieces_ids:
  - 8ccc3135-904f-495b-bf2f-e65b41da73d4
  - 2b4ba166-33d9-40c4-b37d-ff0c7e18a333
tags: [raw, pieces]
---

## Asset 1 (Pieces: 8ccc3135-904f-495b-bf2f-e65b41da73d4)

Both outstanding cursors have now returned `sufficient` (one) and a circuit-breaker on the second (indicating no genuinely new content would have been returned). All retrieval is exhausted. Here is the grounded, complete answer from everything retrieved across all pages.

---

## Frontend components defining the cohort discovery screens

The FITFILE frontend is a **Next.js** application (TypeScript, App Router). Based on all evidence retrieved from your memory, the cohort discovery screens are built on these components and routes:

### Route structure (App Router)

The "New Operation" entry point — seen live at `ff-test-a.fitfile.net/fitfile/project/<id>/new-o…` — is the top-level screen that presents the cohort discovery workflow. From your editor captures in the frontend repo (`src/app/`):

- **`src/app/project/[id]/new-operation/`** — the new-operation flow root
  - **`data-extract/[userflowId]/layout.tsx`** — wraps the data extract / cohort discovery userflow; contains `useAppConfig()` / feature-flag checks
  - **`custom-transformations/layout.tsx`** — adjacent layout for custom transformation step
- **`src/app/project/[id]/queryPlan/[queryPlanId]/raw-edit/page.tsx`** — raw query-plan edit screen (gated by `features.updateQueryPlan`)

### Key component files (confirmed from editor captures)

| File | Role |
|---|---|
| `src/components/templates/ToggleDataDisclosureConfirmModals/EnableDataDisclosureConfirmModal.tsx` | Modal that appears when enabling data disclosure for a tenant — surfaces inline in cohort discovery flow |
| `src/lib/networking/useGraphQL.ts` | GraphQL hook used by the frontend; was broken and debugged during a standup (error on line 48) — critical to cohort result fetching |
| `src/lib/networking/AppConfigProvider.tsx` | Provides the app config (feature flags) consumed by `useAppConfig()` in the layout components |
| `src/lib/networking/getAppConfigEnv.ts` | Reads env vars that feed the config provider |
| `src/components/FaroProvider.tsx` | Grafana Faro telemetry wrapper for the frontend app |
| `src/lib/fitfileEnv.ts` | Environment abstraction layer |

### Data shape: `CohortData` type

**Pavlo Kotov** (frontend engineer) defined and used this fixture in wireframing during the 15 Apr 2026 standup:

```typescript
export const n3Fixture: CohortData = {
  total: 66_000,
  sources: [
    { id: 'gp',       label: 'GP Records',         count: 47_000, unique: 18_000 },
    { id: 'nhs',      label: 'NHS Digital',         count: 32_000, unique:  8_000 },
    { id: 'hospital', label: 'Hospital Admissions', count: 28_000, unique:  6_000 },
  ],
  pairs: [
    { leftId: 'gp',  rightId: 'nhs',      pairUnion: 60_000 },
    { leftId: 'gp',  rightId: 'hospital', pairUnion: 58_000 },
    { leftId: 'nhs', rightId: 'hospital', pairUnion: ... },
  ],
};
```

The `pairs` keys follow the convention `0_1` → `A_B` etc. (Oliver Rushton's formulation). This type feeds the cohort breakdown visualisation rendered on the "New Cohort" / cohort results screen.

### Feature flags gating the screens

The frontend checks `features.updateQueryPlan` and `features.updateDataDisclosure` (via `useAppConfig()`) before rendering certain cohort-related screens. These flags are injected through `AppConfigProvider.tsx` / `getAppConfigEnv.ts` and configured per-deployment in ArgoCD / ffnode Helm values.

### Jira work items driving these screens

Active tickets from your sprint boards:

- [**FTFL-494**](https://fitfile.atlassian.net/browse/FTFL-494) — *(De-duplication) Show union counts using entity resolution on Cohort Discovery* — the core sprint ticket driving the intersection/union visualisation on the cohort screen
- **FTFL-501** — *Write Full component for Cohort* — explicitly a frontend component creation task
- **FTFL-502** — *Integrate new cohort artifact components into the OMOP flow*
- **FTFL-496** — *Change disambiguate and count task to produce a new artifact type*
- **FTFL-31** — *Streamline Complex OMOP Query* — parent epic (65% done) that includes all Cohort Discovery child tasks

### Platform context

- The FITFILE platform UI (`FITFILE Platform V3`) showed a live cohort results screen with a `define-cohort-output-name`, `Total study populations`, and a breakdown by node (NNUH / CUH / MKUH) — confirming that the results display component renders per-data-source breakdowns with union intersections
- The **AWSSDE** deployment (eastern SDE: `app.eoe-sde-codisc.privatelink.fitfile.net`) hosts the live cohort discovery workflow, with audit log event types including `CohortDiscoveryUsingFI` (Cohort Discovery Using FITtokens)
- The "Select the type of operation" screen (captured in Teams on 8 Jun 2026) explicitly lists **"Cohort Discovery: Returning aggregate counts of unique records matching defined criteria"** as the first operation type — this is the entry-point screen rendered by the new-operation route

### Collaborators on the frontend cohort screens

- **Pavlo Kotov** — frontend engineer; owns the `CohortData` type and wireframe components
- **Yasir Mansoor** — frontend; visible in standup debugging `useGraphQL.ts` and the Faro SDK setup (`src/components/FaroProvider.tsx`, `src/components/AppConfigProvider.tsx`)
- **Weronika Jastrzebska** — PM; led the deduplication refinement sessions that produced the wireframe requirements
- **Oliver Rushton** — backend/platform; defined the union intersection data format