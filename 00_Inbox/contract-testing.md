---
created: 2026-09-18T11:15:47+00:00
modified: 2026-09-18T11:31:30+00:00
permalink: llmeon/00-inbox/contract-testing
title: contract-testing
type: note
---

## Contract Testing: Current Setup

This document describes what contract testing exists in this repo today, how it fits into CI, and

where to look when working on it. It's written as prep material for a workshop on writing contract

tests—see [Contract testing: candidates for new tests](./contract-testing-candidates.md) for

which service boundaries don't have contracts yet.

### What We Mean by "Contract Test" here

We use consumer-driven contract testing via [Pact](https://docs.pact.io/). A consumer (a

service that calls another service) writes tests describing the requests it makes and the

responses it expects. Running those tests produces a pact file—a JSON record of those

request/response pairs. The provider (the service being called) then replays those recorded

requests against a real instance of itself and checks its actual responses still match. This

catches breaking API changes without needing a full end-to-end environment, and without the

provider team having to guess what the consumer actually relies on.

This is different from schema/OpenAPI validation (which checks a response is _shaped_ like the

spec)—Pact checks that a _specific real interaction_ the consumer depends on still works.

### What Exists Today

There is exactly one contract in the system: FitfileFrontend (consumer) → FFCloudGraphQL

(provider), covering the `UpsertQueryPlan_Mutation` GraphQL mutation (`apps/frontend` calling

`apps/ffcloud`'s `/ffcloud/graphql` endpoint). Everything else—including the ~48 other GraphQL

operations the frontend sends to ffcloud, and every other inter-service call in the system—has no

contract test. See the companion doc for the full list of gaps.

Tooling: [`@pact-foundation/pact`](https://github.com/pact-foundation/pact-js) v17, using the

`PactV4` consumer DSL.

#### Consumer Side (`apps/frontend`)

- `apps/frontend/e2e/query-plan/contract/query-plan-contract.pact.test.ts`—the consumer test.
  For each of 4 scenarios (identifiable upsert, multi-query privacy-linkage upsert, validation
  failure, edit-preserving-identity upsert) it declares a provider state (`.given(…)`), the
  exact GraphQL request body, the expected response shape, and then runs a real
  `graphql-request` client against Pact's mock server to assert the frontend code handles that
  response correctly.
- `apps/frontend/e2e/query-plan/contract/matchers.ts`—builds the expected-response matchers
  using Pact's `MatchersV3` (`like`, `atLeastLike`, `eachLike`, `regex`) instead of exact-value
  equality, so the contract asserts on _shape and type_, not incidental example values (an id, a
  timestamp).
- Running it (`yarn workspace @fitfile/frontend test:contract`) deletes any stale pact file and
  regenerates `pacts/FitfileFrontend-FFCloudGraphQL.json` at the repo root.

#### Provider Side (`apps/ffcloud`)

- `apps/ffcloud/src/api-tests/contract/harness.ts`—spins up a real (in-memory HTTP server +
  real Mongo) instance of the ffcloud GraphQL server for verification, with auth and
  authorization (SpiceDB) mocked out and a fixed test user injected into context. Also owns the
  logic for where to source pacts from (see below).
- `apps/ffcloud/src/api-tests/contract/query-plan/query-plan.verify.test.ts`—for each provider
  state name declared by the consumer (`VALID_UPSERT_STATE`, `INVALID_QUERY_PLAN_STATE`,
  `EDIT_UPSERT_STATE`), a state handler resets the contract test data in Mongo, seeds the
  fixtures it needs, and mocks the parts of the domain (query plan validation, SpiceDB
  permission checks) that would otherwise require a full pipeline. Pact's `Verifier` then
  replays each recorded interaction against the live server and diffs the real response against
  the matcher.
- `apps/ffcloud/src/api-tests/contract/query-plan/seeds.ts`—the Mongo fixtures (a project, an
  existing query plan for the edit scenario) used by the state handlers above.

#### Pact Broker vs. Local File

`harness.ts` decides where pacts come from based on `PACT_BROKER_BASE_URL`:

- Not set (local dev, or CI runs where the variable isn't configured): falls back to reading
  the pact file straight off disk (`pacts/FitfileFrontend-FFCloudGraphQL.json`). This is what lets
  a single MR run both the consumer test and the provider verification without any broker.
- Set: verification pulls pacts from the broker instead, using
  [consumer version selectors](https://docs.pact.io/pact_broker/advanced_topics/consumer_version_selectors)
—`mainBranch`, `matchingBranch`, and `deployedOrReleased`—plus `enablePending: true` (so a
  new, not-yet-verified interaction shows up as _pending_ rather than failing the build) and
  `includeWipPactsSince` (currently `2026-09-01`) to pick up WIP pacts from feature branches that
  wouldn't otherwise match a selector.

There's a second verification path, `pactMainBranchSourceOptions()`, used purely to re-verify the

pact currently on the main branch—a safety net so a provider-side change can't silently break

the contract the rest of the team is relying on, even before a broker exists.

Note for the workshop: whether `PACT_BROKER_BASE_URL` is actually set in CI right now (i.e.

whether we have a live PactFlow/broker instance in use, vs. running purely off the file fallback)

isn't something visible from the repo alone—worth confirming with whoever owns CI/CD variables

before presenting this as "we have a broker in production."

### CI Flow

Defined in `deployment/pipeline/verification-pipelines.yml`:

1. `publish_frontend_pact` (runs on `apps/frontend/e2e/query-plan/contract/` changes, or on
   the default branch)—runs `test:contract` to (re)generate the pact file, uploads it as a
   1-day artifact, and—only if `PACT_BROKER_BASE_URL` is set—publishes it to the broker via
   the `pact-broker` CLI, tagged with the commit SHA and branch name.
2. `verify_ffcloud_pact`—depends on `publish_frontend_pact`'s artifact, builds ffcloud, and
   runs `test:contract:verify`, which runs both provider verification tests (against the sourced
   pact, and against the main-branch pact).

Both jobs are path-scoped: they only run when contract-test files, `packages/types`,

`package.json`, or `yarn.lock` change (or unconditionally on the default branch for publishing).

### Running it Locally

```
# Consumer: regenerate the pact file
yarn workspace @fitfile/frontend test:contract

# Provider: verify ffcloud against it
yarn workspace @fitfile/ffcloud test:contract:verify
```

The provider verification needs the same local infra the rest of ffcloud's tests need (Mongo

running). No broker credentials are required for the local file fallback path.

### Key Files, at a Glance

| Concern | File |
|---|---|
| Consumer test | `apps/frontend/e2e/query-plan/contract/query-plan-contract.pact.test.ts` |
| Response matchers | `apps/frontend/e2e/query-plan/contract/matchers.ts` |
| Provider harness + broker source config | `apps/ffcloud/src/api-tests/contract/harness.ts` |
| Provider verification + state handlers | `apps/ffcloud/src/api-tests/contract/query-plan/query-plan.verify.test.ts` |
| Provider test fixtures | `apps/ffcloud/src/api-tests/contract/query-plan/seeds.ts` |
| CI jobs | `deployment/pipeline/verification-pipelines.yml` (`publish_frontend_pact`, `verify_ffcloud_pact`) |
| Generated pact file | `pacts/FitfileFrontend-FFCloudGraphQL.json` (git-ignored, regenerated per run) |
