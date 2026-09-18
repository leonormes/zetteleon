---
permalink: llmeon/00-inbox/contract-testing-candidates
title: contract-testing-candidates
type: note
---
# Contract testing: candidates for new tests

Companion to [Contract testing: current setup](./contract-testing.md). That doc covers the one
contract that exists today (`UpsertQueryPlan_Mutation`, FitfileFrontend → FFCloudGraphQL). This
doc inventories everything else the frontend sends to ffcloud and ranks it as a candidate for the
next contract test(s).

## Inventory

`apps/frontend` sends **89 operations** to ffcloud's GraphQL API in total (47 mutations, 42
queries, 0 subscriptions) — all as `graphql()`-tagged, codegen'd operations under
`apps/frontend/src/**/*.schema.ts(x)`, with one exception (`CreateUserActionAuditEvent`, sent via
a raw inline mutation string in `apps/frontend/src/app/api/auth/[...nextauth]/audit.ts`,
bypassing the usual client). One operation — `UpsertQueryPlan_Mutation` — is covered by a
contract. **88 are not.**

Two of those 88 are dead code with no current caller (`EditS3DataSource_Mutation`,
`CreateUserActionAuditEvent_Mutation`) — listed under Cleanup below, not real gaps.

## Ranking method

No usage telemetry was available for this pass, so ranking is by four signals visible from the
code itself:

1. **Irreversibility** — does a silent contract break let bad data through, or destroy data, with
   no way back? (deletes, disclosure toggles, reidentification)
2. **Reach** — is it on the main dashboard/nav, or gating access across many pages, vs. a
   rarely-hit admin/edge screen?
3. **Shape fragility** — nested/joined response shapes are where a real mismatch already
   happened once (see below); flat scalar responses are lower risk.
4. **Compliance/privacy sensitivity** — this is a health-data platform; PII, data disclosure, and
   reidentification operations carry a different risk class than, say, renaming a data source.

None of these are hard numbers — they're the analyst's judgement, meant to seed workshop
discussion, not a scoring formula to defer to.

## Evidence: this has already happened once

`e488a3d37` / `9e4e0afd4` ("FFAPP-4647 Correctly map dataset refs in query joins") — the frontend
read `join.dataset.ref` for both sides of a query-plan join when ffcloud actually returns
`join.onLeft.datasetRef` / `join.onRight.datasetRef`. The frontend misread the real shape of a
live ffcloud response and silently built wrong cohort-discovery query configurations. This is the
single confirmed frontend↔ffcloud contract-shape bug found in git history (search covered both
repos' full history for graphql/mismatch/breaking/schema/pact/contract terms plus a
per-operation-name sweep; nothing else surfaced, but commit messages are an imperfect proxy —
treat absence elsewhere as "not found," not "didn't happen").

It's also the best teaching example for the workshop: a real bug, in a nested/joined response
shape, in the exact feature area the existing contract test already lives in.

## Tier 1 — next candidates

| Operation | Why |
|---|---|
| `QueryPlanConfiguration_Query` | Same nested join-shape family as the FFAPP-4647 bug — reads the fields that bug touched. Most direct "cover the thing that already broke" pick. |
| `UpsertCohortDiscoveryQueryPlan_Mutation` | Write side of the same join-mapping data; pairs naturally with the query above for a single workshop exercise. |
| `DeleteProjectAndData_Mutation` | Irreversible, destructive, project-wide blast radius. A silently-broken response shape here is the worst-case failure mode in the whole inventory. |
| `TenantPermissions_Query` / `ProjectPermissions_Query` | Used as an access guard across ~21 files and most project-scoped pages. A shape drift here either silently over-grants or locks out — both are security-relevant, not just a broken UI. |

## Tier 2 — soon after

| Operation | Why |
|---|---|
| `Projects_Query`, `Stats_Query` | On the dashboard — the first thing every user sees every session. Low blast radius per-break, but highest raw traffic. |
| `ReidentifyResultWithTokens_Mutation`, `ReidentifyResultWithId_Mutation` | Privacy-critical: reidentification is exactly the kind of operation where "the frontend silently misreads the response" is a compliance incident, not just a bug. |
| `UpdateTenantDataDisclosure_Mutation` (both variants), `UpdateDataAccessRequestStatus_Mutation` | Governance/compliance toggles — a silently-inverted or dropped field changes who can see identifiable data. |
| `DeleteDataSource_Mutation`, `DeleteQueryPlan_Mutation`, `DeleteOrganisationMember_Mutation`, `RemoveDataSourceFromProject_Mutation` / `RemoveDataSourceFromTenant_Mutation` | Same "irreversible delete" class as Tier 1's `DeleteProjectAndData_Mutation`, lower individual blast radius. |
| `CreateUserActionAuditEvent` (the real, called one in `audit.ts`) | Fires on every sign-in/out. Not high business risk if it silently breaks, but it's the audit trail — worth contract-covering for its own sake. It's also currently the one operation that doesn't follow the standard `schema.ts` pattern, worth flagging in the workshop regardless. |

## Tier 3 — everything else

The remaining ~65 operations (data-source CRUD variants for each connector type, org/project
member management, data catalogue/data operations browsing, FITConnect context, scheduler CRUD,
audit logs, validation reports) are mostly single-purpose CRUD against one entity, on
lower-traffic or admin-only screens, with flat response shapes. Not zero-risk, but nothing here
has the combination of reach + irreversibility + shape complexity that would justify jumping the
queue. Revisit once Tier 1/2 are covered and a pattern for reusable state handlers exists.

## Cleanup, not contract candidates

- `EditS3DataSource_Mutation` — defined, no caller. Either wire up an S3 edit page or delete it.
- `CreateUserActionAuditEvent_Mutation` (the `.schema.ts` one, distinct from the inline one
  actually used in `audit.ts`) — orphaned duplicate. Delete it; it's not what fires on login.
- `AddMySQLDataSource_Mutation` duplicate definition in `sqlConnection.schema.ts` (unused) vs.
  `mysql.schema.ts` (used) — same operation defined twice; delete the unused one.
- Two near-duplicate operation pairs worth a naming pass regardless of contract-testing priority:
  `UpdateTenantDataDisclosure` vs `UpdateTenantDataDisclosure_Mutation` (same field, different
  callers), and `Operation_Query` vs `DataOperation_Query` (same field, different flows).
- `UpsertScheduledJob_Mutation`'s wire name is actually `UpsetScheduledJob_Mutation` (typo).
  Cosmetic, but worth knowing if grepping broker/ffcloud logs by name later.

## Caveats

- The 89-operation count is pulled from the codegen'd `apps/frontend/src/gql/gql.ts` source of
  truth, cross-checked against every `*.schema.ts(x)` file — confident in the count itself, not
  verified against ffcloud's live schema for whether every field still resolves.
- Git-history search for past breakage is not exhaustive — see "Evidence" above. One confirmed
  hit; absence elsewhere means "not found in commit messages," not "never happened."
- No usage/traffic telemetry was consulted; "reach" judgements above are from reading call sites
  in code (nav, dashboard, guard hooks), not from actual analytics.
