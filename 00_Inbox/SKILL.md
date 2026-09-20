---
created: 2026-09-18T11:22:15+00:00
description: "Write or extend a Pact contract test between two services in this repo — a consumer test, a provider verification, or both. Use when asked to add a contract test, pact test, consumer-driven contract, or provider verification for any service pair here (frontend, ffcloud, fitconnect, scheduler-service, workflows-api, etc)."
modified: 2026-09-18T11:31:30+00:00
name: write-contract-test
permalink: llmeon/00-inbox/skill
title: SKILL
---

## Write a Contract Test

One working pair exists already: `frontend` (consumer) → `ffcloud`'s `FFCloudGraphQL` (provider),

covering `UpsertQueryPlan_Mutation`. Read it before writing a new one—it's the template every

step below points back to:

- Consumer test: `apps/frontend/e2e/query-plan/contract/query-plan-contract.pact.test.ts`
- Matchers: `apps/frontend/e2e/query-plan/contract/matchers.ts`
- Provider harness: `apps/ffcloud/src/api-tests/contract/harness.ts`
- Provider verification + state handlers: `apps/ffcloud/src/api-tests/contract/query-plan/query-plan.verify.test.ts`
- Provider fixtures: `apps/ffcloud/src/api-tests/contract/query-plan/seeds.ts`
- CI: `deployment/pipeline/verification-pipelines.yml`, jobs `publish_frontend_pact` / `verify_ffcloud_pact`

Full narrative of how those pieces fit together: `docs/contract-testing.md`. Known gaps and which

pair to pick if none was specified: `docs/contract-testing-candidates.md`. Don't restate either—

point back to them.

### Steps

#### 1. Confirm the Pair Isn't Already Covered

Grep for the consumer/provider names under `apps/*/e2e//contract` and

`apps/*/src//contract`. If it's genuinely new, check `docs/contract-testing-candidates.md` for

context on why that pair matters before writing anything.

#### 2. Write the Consumer Test

In the consumer app, alongside its existing tests (`e2e/<feature>/contract/` for a Jest+Playwright

app like `frontend`; the provider-app equivalent otherwise):

- `new PactV4({ consumer, provider, dir: pactDir })`, one `describe` per endpoint/operation.
- One `.addInteraction()` per scenario: `.given(<provider state string>)` →
  `.uponReceiving(<description>)` → `.withRequest(…)` → `.willRespondWith(…)` →
  `.executeTest(async (mockServer) => { /* real consumer code call, real assertions */ })`.
- Response bodies use `MatchersV3` (`like`, `atLeastLike`, `eachLike`, `regex`)—assert shape,
  not value. An id, a timestamp, a count that isn't the point of the scenario: `like(…)`, never
  a hardcoded literal. Hardcoding one makes the contract brittle against unrelated provider
  changes and defeats the point of a contract test.
- Delete any stale pact file before the suite runs (see the top of the template file) so re-runs
  don't append.

Each `.given(…)` string is a contract in itself—the provider side must implement a handler with

that exact string.

#### 3. Write the Provider Verification

In the provider app:

- Reuse or write a harness that boots a real instance of the provider—real database, mocked
  auth/authz and other cross-cutting infra—and returns its base URL. `harness.ts` is the
  template; if the provider isn't `ffcloud`, adapt it rather than inventing a different shape.
- One state handler per `.given(…)` string the consumer declared. Each handler resets and seeds
  _only_ the data that scenario needs—see `seeds.ts`. Missing or wrong seeding here is the most
  common way a "passing" verification hides a real contract break.
- Run `Verifier` twice: once against the sourced pact (`pactSourceOptions()`—broker if
  `PACT_BROKER_BASE_URL` is set, else the local pact file), and once against
  `pactMainBranchSourceOptions()`. The second run is what stops a provider change from silently
  breaking the contract already relied on, even before every consumer has re-verified.
- If the provider isn't a Jest/TS app (e.g. `workflows-api`, which is Python)—there is no
  existing example of this in the repo yet. Use Pact's verifier for that language; don't force a
  Jest harness onto a non-JS service.

#### 4. Wire CI

Add a publish job (consumer side) and a verify job (provider side) to

`deployment/pipeline/verification-pipelines.yml`, mirroring `publish_frontend_pact` /

`verify_ffcloud_pact`. Path-scope both to the new contract test files so they only run when

relevant.

#### 5. Close the Loop in the Docs

Move the pair from "Not covered" to "Covered" in `docs/contract-testing-candidates.md`, and add it

to the table in `docs/contract-testing.md`. These two files are the single source of truth for

"what's covered"—don't leave a second, divergent list anywhere else.

### Done when

Consumer suite passes and produces a pact file; provider verification passes against both the

sourced pact and the main-branch pact; CI jobs exist and are path-scoped; both docs reflect the new

pair.
