---
created: 2026-09-22T10:52:42+00:00
modified: 2026-09-22T10:59:53+00:00
permalink: llmeon/00-inbox/cue-assessment
title: CUE-ASSESSMENT
type: note
---

## Multi-customer Deployment Review, and an Assessment of CUE

Date: 2026-09-22

Scope: `Deployment/deployment` (charts + ffnodes), `Deployment/Clusters/*` (per-cluster Terraform), and the two existing CUE proof-of-concepts.

Status: Draft for discussion. Numbers below were measured against the working tree on the date above; commands are given so you can re-run them.

---

### 1. How We Deploy to Customers Today

Four layers, each owning part of one customer's configuration:

```
1. Terraform (per cluster)     Clusters/<org>/<env>/<cluster>/locals.tf
                               declares argocd_applications → chart path + value_files
                                                │
2. ArgoCD Application          points at charts/ffnode @ <targetRevision>
                               with -f /ffnodes/<org>/<node>/values.yaml
                                                │
3. ffnode umbrella chart       charts/ffnode/values.yaml (901 lines of defaults)
                               templates/*.yaml emit one child Application per component
                                                │
4. Per-customer overrides      ffnodes/<org>/<node>/*.yaml  (hand-written)
```

Scale, as measured:

|                                 | Count          | Command                                                 |
| ------------------------------- | -------------- | ------------------------------------------------------- |
| Orgs under `ffnodes/`           | 7              | `find ffnodes -mindepth 1 -maxdepth 1 -type d \| wc -l` |
| Node directories                | 31             | `find ffnodes -mindepth 2 -maxdepth 2 -type d \| wc -l` |
| Hand-written per-customer YAML  | 16,408 lines   | `find ffnodes -name '*.yaml' \| xargs cat \| wc -l`     |
| Charts in the umbrella          | 16 (272 files) | `find charts -mindepth 1 -maxdepth 1 -type d \| wc -l`  |
| Customer/cluster Terraform dirs | ~13            | `find Clusters -maxdepth 3 -type d`                     |

Largest single customer file is `ffnodes/eoe/hie-test-34/ohdsi-values.yaml` at 1,152 lines. `hie-prod-34` alone spans five files totalling ~1,750 lines.

#### Release Trains

`argocdApp.targetRevision` is set per node, and there are at least nine distinct trains:

`latest-release`, `eoe-latest-release`, `eoe-test-release`, `cuh-prod-1-latest-release`, `nnuh-prod-1-latest-release`, `mcnft-prod-1-latest-release`, `nwsde-prod-1-latest-release`, `sandbox-testing-1-latest-release`, `master`.

Two nodes (`fitfile/acr-test`, `fitfile/wm-dev-1`) are pinned to a feature branch, `feature/FFAPP-3073-new-ffnode-chart-with-vault-secrets`. That branch is a moving target and nothing prevents it being deleted or rebased underneath a running node.

#### Two Onboarding Paths Exist in Parallel

- The established path—`Clusters/nwsde/scripts/create_customer.sh` does `rsync -av` of a previous customer's directory (`Production/LCA-DP`) and renames. Copy-and-fork.
- The newer path—the CUE POC in `Clusters/eoe/Test/ff-test-1`, where a 64-line `config/customer.yaml` generates everything (§4).

---

### 2. What Actually Hurts, with Evidence

#### 2.1 Nothing Validates a Customer Values file—proven

There is no `values.schema.json` anywhere in `charts/` (`find charts -name values.schema.json` → empty).

Helm therefore accepts any key at all. Tested directly:

```bash
printf 'namespace: t\ndeploymentKey: t\nhost: x.example.net\nmongodb:\n  replicaCnt: 1\nnonsenseTopLevelKey:\n  whatever: true\n' > /tmp/typo.yaml
helm template t charts/ffnode -f /tmp/typo.yaml >/dev/null   # exit 0, no stderr
```

`replicaCnt` (a typo of `replicaCount`) and an entirely invented top-level key both pass silently.

The chart falls back to its default and the node deploys—wrong, but green. This is the single largest correctness gap in the current model, and it is exactly the failure class a type system closes.

#### 2.2 CI Checks Nothing about Customer Config

`.gitlab-ci.yml` has four real jobs: three image builds and `lint_workflows`, which is gated on `changes: workflows//*`. `staging.gitlab-ci.yml` adds kube-config, an ArgoCD sync and integration tests. No job renders or validates `ffnodes/`. A change to a production customer's values file produces a pipeline whose only job is `mr_pipeline_guard`—which, to its credit, says so in its own output: _"this job verifies nothing about the change itself."_

The validation machinery exists (`Makefile` → conftest / kubeconform / kube-score, `scripts/kat-validate.sh`) but it is manual and opt-in. `scripts/VALIDATION.md` even contains a worked GitLab CI snippet that was never wired in. Note also that `scripts/template.sh` iterates `$FFNODE_DIR/values/*/`, a layout only `kch/` and `stg/` still use—it is stale for the other 29 nodes.

#### 2.3 The Escaping Problem

Vault Secrets Operator templates are Go templates, written into YAML, consumed by a Helm chart that runs `tpl` over them—sometimes twice. The result, from `ffnodes/eoe/hie-prod-34/values.yaml`:

```yaml
s3_access_key_id:
  text: '{{"{{`{{get .Secrets \"hie_s3_export_access_key_id\"}}`}}"}}'
```

Three levels of escaping, hand-written, per key, per customer. There are 405 occurrences of `get.Secrets` across `ffnodes/` (`grep -rho 'get \.Secrets' ffnodes | wc -l`) in 18 files, and 37 `secretTransformation:` blocks that each repeat the same `excludes: ['.*']` boilerplate.

This is not theoretical. Git history contains `35123f15 Fix opencost-azure secret escaping causing testing app-of-apps sync failure`.

#### 2.4 Duplication

Across the 29 primary `values.yaml` files, counting only substantive lines (>30 chars, i.e. carrying a value rather than just a key):

- 1,317 substantive lines, 556 distinct → 57.8% are exact duplicates of a line in another file.

The most-repeated lines are precisely the things that should be platform defaults:

| Repeats | Line |
|---|---|
| 32 | `secretName: cloudflare-tls` |
| 18 | `baseURL: "https://fitfile-test.eu.auth0.com"` |
| 18 | `FEATURE_CREATE_QUERY_PLAN: "true"` (and two sibling flags) |
| 16 | `text: '{{"{{`{{get.Secrets \"api_token\"}}`}}"}}'` |
| 14 | `defaultOrganisationAdminUserId: "auth0\|61e6a55e…"` |

#### 2.5 Defaults Are Production-shaped, and Omission is Silent

`charts/ffnode/values.yaml` defaults `global.oauth.baseURL` to `https://fitfile-prod.eu.auth0.com`. Five nodes inherit it. For `ff-a/b/c` and `barts/prod` that is correct; for anything non-production that inherits it, _omitting_ a line selects production. There is no `env: dev | live` discriminator anywhere in the values contract that would make that combination unrepresentable.

#### 2.6 Churn and Correction Rate

Last 12 months, in `deployment/`:

- 1,307 commits total; 337 (26%) touch `ffnodes/`; 465 touch `charts/`.
- Of the 337, 35 (~10%) have corrective subjects (`fix`, `revert`, `hotfix`, `typo`, `wrong`, …), including six consecutive commits titled `Hotfix/grafana perms`.

A tenth of all customer-config commits are repairs to earlier customer-config commits.

---

### 3. What CUE is for

From cuelang.org, the positioning is six use cases: data validation, configuration, boilerplate removal, scripting, code and schema generation, and querying. The site makes no Kubernetes/Helm/Terraform-specific claims—those are community patterns, not product promises.

Two of the six matter here (validation and boilerplate removal), and both rest on one property: Unification. In CUE, types and values are the same thing, and combining two configurations is a commutative, associative, idempotent lattice meet. Concretely:

- Merging is order-independent. There is no "last file wins", so `-f a.yaml -f b.yaml` ordering bugs cannot exist.
- Merging is deep by default. You never write a deep-merge function.
- A conflict is an error, not a silent overwrite. Two layers setting the same field to different concrete values fails the build.
- Closed structs (`#Definition`) reject unknown fields—this is what catches `replicaCnt`.

Verified locally against `cue v0.17.1`:

```
w.mongodb.replicaCnt: field not allowed:
    ./typo.cue:4:11
```

File, line, column, at build time. Compare with Helm's exit 0.

The cost side is equally concrete: CUE is a second language with genuinely unusual semantics (the value/type collapse, `_|_` bottom, definitions vs regular fields, the `|` disjunction/default distinction). It is not "YAML with types". Expect a real learning curve for anyone who has to debug it at 2am.

---

### 4. The POCs You Already Have

#### POC A—`deployment/cue/` (1,333 Lines, Abandoned)

Output-side approach: `cue/schema/values.cue` defines `#Values`, a type for the ffnode chart's values contract; `cue/base/values.cue` holds the 883-line default tree; `cue/instances/ff-a.cue` expresses one real customer against it.

It is unfinished—`ff-a.cue` ends with a literal comment: _"For brevity in this artifact, I am stopping here, but the full migration should include all."_ Most structs are left open with `…`, so it would not catch typos as written.

But the idea is the right one, and it is the cheapest thing on the table. `#Values` is the missing `values.schema.json`. Closing the structs turns it into a CI gate over all 31 nodes with no migration.

#### POC B—`Clusters/eoe/Test/ff-test-1/` (1,065 Lines of CUE + 1,204 Lines of Docs)

Full pipeline. This one works—I ran it:

```bash
cue export ./cue/values.cue ./cue/*.cue -t "infra=$(cat cue/mock_infra.json)" -e values --out yaml
```

…renders valid values. The flow is:

```
config/customer.yaml (64 lines)
  + platform-defaults module (common.yaml, via TF registry)
      → locals.tf (deep merge)
      → generators.tf → terraform output infra_facts (JSON)
      → CUE: #InfraFacts validates, #RenderValues renders
      → generated/values.yaml (461) + thehyve_values.yaml (233) + genjump.tf (454)
```

64 hand-written lines produce ~1,150 generated lines. Against `hie-prod-34`'s ~1,750 hand-written lines, that is the real prize.

What it does well:

- `#InfraFacts` is a genuine typed contract between Terraform and Helm. Missing field → build fails.
- `#VSO.raw` / `.map` / `.doubleMap` in `templates_vault.cue` names the escaping problem and solves it once. The comments are the clearest statement of the problem I found anywhere in the estate: _"Use when the Application template calls tpl on.Values before renderValuesWithVaultSecretInExtraDeploy … AND the destination chart applies another tpl pass."_ That knowledge is currently tacit and re-derived per customer; here it is a named helper with three cases.
- The docs (`CONTRACTS.md`, `CODE_REVIEW_AND_DATA_FLOW.md`, `MIGRATION_PLAYBOOK.md`) are better than most production systems get.

What it does not do—and this matters for §5:

- It does not validate the output. `#InfraFacts` types the _input_. `values:` is an ordinary open struct. A typo in `render_fitfile.cue`—`mongoDb:` for `mongodb:`—renders happily and deploys wrong. The typo class from §2.1 is not closed by POC B as written.
- There is no `cue.mod`. It is a bare file glob invoked via `cue export./cue/*.cue`.
- Its own `CODE_REVIEW_AND_DATA_FLOW.md` audits ~40 hardcoded literals still sitting in `locals.tf`, `render_fitfile.cue` and `jumpbox.tftpl` that the layer-ownership rule says shouldn't be there.

---

### 5. Problems CUE Would Solve for Us

| # | Problem (from §2) | Does CUE fix it? | What it takes |
|---|---|---|---|
| 1 | Typo'd values key deploys silently (§2.1) | Yes, completely | A _closed_ `#Values` schema + `cue vet` in CI. POC A is the start. |
| 2 | CI validates nothing (§2.2) | Yes | One job: `cue vet./ffnodes/…./schema`. Seconds to run, no cluster needed. |
| 3 | Triple-escaped Vault templates (§2.3) | Yes | POC B's `#VSO` helpers. 405 hand-escapes → 3 named functions. |
| 4 | 57.8% duplicated lines (§2.4) | Yes | Defaults live once in a shared package; unification merges them. |
| 5 | Omission silently selects prod (§2.5) | Yes | Model `env` as a disjunction and bind defaults to it; the wrong combination stops being expressible. |
| 6 | Correction-commit rate (§2.6) | Partly | Catches structural/typo/escaping errors. Does not catch "we chose the wrong CIDR". |
| 7 | rsync-fork onboarding (§1) | Yes, if the CUE is a _shared module_ | See §6.4—otherwise it reproduces the fork one layer up. |
| 8 | Nine release trains | No | Orthogonal. CUE can _describe_ rings (POC B has `rollout.ring`), but the sprawl is a process problem. |
| 9 | Feature branches pinned in prod-adjacent nodes | Partly | A schema can constrain `targetRevision` to a pattern. It cannot stop someone widening the pattern. |
| 10 | Terraform ↔ Helm drift | Yes | `#InfraFacts` is exactly this contract, and POC B already has it. |

---

### 6. Where the Complexity Moves

This is the part worth arguing about. CUE does not delete complexity; it relocates it. Four relocations are good, two are bad, and POC B currently has all six.

#### 6.1 Down, into the Type layer—good

Escaping (§2.3) is the clean win. Today the rule _"this string must survive two `tpl` passes"_ lives in 405 hand-written strings and in whoever last debugged it. In CUE it is `#VSO.doubleMap`, defined once, with the reasoning in a comment above it. Getting it wrong becomes impossible rather than merely unlikely.

Same for defaults: `resourcePreset: "standard"` and the 901-line default tree become a typed package that customers unify against, instead of a file that Helm silently merges under them.

#### 6.2 Up, into Terraform HCL—bad, and it Has Already Happened

POC B's `locals.tf` is 512 lines with 59 `merge()` calls and 149 `try()` calls, hand-rolling a deep merge of platform defaults against customer YAML. From its own `CONTRACTS.md`:

> Terraform's built-in `merge()` is shallow (one map level). This repo builds `local.config` in `locals.tf` … with hand-rolled deep merges where partial customer YAML must not wipe platform subtrees.

Then `CONTRACTS.md` needs a two-table section documenting bespoke per-key merge semantics—`vault_secrets` merges three sub-maps; `frontend.env` replaces if present-but-empty; `node_placement.tolerations` replaces but `nodeSelector` merges; `vault_secret_consumers.<app>` replaces only if non-empty.

Deep merging is the one thing CUE does natively, for free, in zero lines, order-independently. POC B does it in HCL—the worst available language for it—and then hands CUE a pre-merged blob. The complexity did not reduce; it moved upstream into a place with no types, no tests, and semantics that need a documentation table to explain.

This is the single most important finding in this report. If you adopt CUE and keep this, you have paid for CUE and not bought the main thing it sells.

#### 6.3 Sideways, into a Hand-rolled interpreter—bad

`cue/vault_secret_dispatch.cue` (111 lines) contains `#_RefString`, `#_RefBool`, `#_ResolveVaultPath` and `#_TemplateValue`: string-keyed dispatch tables that turn `"s3_export.enabled"` into a boolean and `"doubleMap:api_token"` into a template.

```cue
#_TemplateValue: {
    _v: string
    _parts: strings.Split(_v, ":")
    _isDouble: len(_parts) == 2 && _parts[0] == "doubleMap"
    ...
}
```

This exists because the data crosses a JSON boundary (`terraform output -json`), and JSON cannot carry a reference. So a late-binding indirection layer is reimplemented inside CUE, in a language with no first-class support for it. Add a new `template:` helper and you must touch `common.yaml`, `templates_vault.cue`, and the dispatch table, and there is no compile-time check that a string in the YAML matches a key in the table—a typo there yields `_|_` at export time at best, a wrong default at worst.

The root cause is architectural, not a coding error: everything is squeezed through `infra_facts` JSON. Remove that boundary (let CUE read `common.yaml` and `customer.yaml` directly) and this entire file disappears.

#### 6.4 Out, into Module versioning—neutral, but Must Be Managed Deliberately

POC B has no `cue.mod`. It is a directory of files invoked by glob. The predictable consequence has already occurred: the POC exists in two places— `New_Customer/ff-test-1/cue` and `Clusters/eoe/Test/ff-test-1/cue`—and they have diverged:

```
render_fitfile.cue:  58 changed lines (292 vs 290)
schema_infra.cue:     7 changed lines (123 vs 120)
```

Not whitespace. One copy gates the whole Grafana block on `if facts.deploy.monitoring`; the other does not.

A platform rule has already forked between two copies of the platform's own rendering logic.

So: putting CUE in each customer repo reproduces the rsync-fork problem one layer up, and makes it worse, because the forked thing is now logic rather than data.

The fix is available and you have already proven the infrastructure. `cue mod publish` pushes a CUE module to an OCI registry, and `FTFL-1008 Phase 1` in `.gitlab-ci.yml` has already demonstrated that `AZ_CLIENT_ID` can push OCI Helm artefacts to `fitfileregistry.azurecr.io` with immutability enforced. Same registry, same credentials, same pattern.

There is a related cost already visible: POC B's platform defaults ship as a Terraform registry module (`terraform-fitfile-platform-defaults` v1.0.10), so its own docs note that changing a platform default requires _republishing and bumping the module version in every customer repo_. Versioned distribution is right, but it means a one-line default change becomes a fan-out across N repos. Budget for that, or accept floating versions in non-production.

#### 6.5 Nowhere—the Layer CUE Does _not_ Remove

CUE generates `values.yaml`. Everything downstream is unchanged:

- `charts/ffnode/templates/_helpers.tpl` still does `tpl`, `renderValuesWithVaultSecretInExtraDeploy`, and the double-render dance.
- ArgoCD still syncs, app-of-apps still fans out, sync waves still order things.
- Terraform still provisions and still declares `argocd_applications`.

So the Go-template layer—arguably the most error-prone part of the estate—survives untouched. CUE makes its _input_ trustworthy; it does not make the template engine safer. Anyone selling this as "replacing Helm" is overselling it. (A full replacement exists—Timoni, which ships CUE modules as OCI artefacts and skips Helm entirely—but that is a rewrite of 272 chart files, not a config change.)

#### 6.6 New Complexity, Created rather than Moved

Three items, all real:

1. A second language on the critical path. CUE's semantics are unusual and its error messages, while precise about location, can be opaque about cause. Today, diagnosing a bad deploy means reading one YAML file. Afterwards it means reading CUE, knowing which layer supplied a value, and running `cue eval` to find out. `cue eval -e values --out yaml` and the `mock_infra.json` pattern POC B already uses are the mitigations, and they are good ones—but the skill has to exist on the team.
2. Generated files in Git. `generated/values.yaml` is committed so ArgoCD can read it. Reviewers now diff a 461-line generated artefact. Either you review generated output (noise) or you don't (and the generator becomes unreviewed). Rendering in CI and committing from the pipeline is better than `make generate-values` on a laptop, which is where POC B leaves it.
3. Two sources of truth during migration. Every node not yet migrated stays hand-written. With 31 nodes and 9 release trains, a partial migration is the steady state for months. Plan for the mixed period explicitly rather than treating it as a transient.

---

### 7. The Decisive Question: where Does the CUE Boundary Sit?

Three positions, materially different in cost and payoff.

Option A—CUE as a per-repo values generator (what POC B is)

Complexity lands in `locals.tf` (§6.2), in the dispatch interpreter (§6.3), and forks per repo (§6.4). Highest payoff per customer (64 lines → 1,150), highest total cost, and it is the version that has already visibly drifted. _Not recommended as the next step._

Option B—CUE as a shared, published module + thin per-customer data

CUE reads `common.yaml` and `customer.yaml` directly—no `infra_facts` JSON round-trip. Terraform supplies only genuinely dynamic facts (FQDNs, role IDs, generated names). The module is published to ACR with `cue mod publish` and pinned per customer. This deletes §6.2 and §6.3 outright and fixes §6.4 by construction. _This is the right destination._

Option C—CUE as validation only

Keep writing `ffnodes/*/values.yaml` by hand. Add a closed `#Values` schema and run `cue vet` in CI over all 31 nodes. No migration, no generated files, no second source of truth. Closes §2.1 and §2.2—the correctness gap—and none of §2.3–2.5. _Cheapest real improvement available._

---

### 8. Recommendation

Sequence them. Each step is independently valuable and independently abandonable.

Step 0—Validation gate (~1 day, no migration).

Take `deployment/cue/schema/values.cue` from POC A, close the structs that are currently `…`, and add:

```bash
cue vet ./ffnodes/<org>/<node>/values.yaml schema/values.cue -d '#Values'
```

as a CI job over all 31 nodes. Expect it to fail on first run—that is the point; the failures are real findings. Where the chart genuinely accepts free-form keys, keep `…` and say so in a comment.

This closes the biggest gap (§2.1) with zero architectural commitment, and if CUE is later rejected, a `values.schema.json` generated from the same schema keeps most of the benefit.

Step 1—Publish the schema as a CUE module to ACR. `cue mod init`, `cue mod publish` to `fitfileregistry.azurecr.io`. You have already proven OCI push and immutability enforcement in `FTFL-1008 Phase 1`. This is what stops the §6.4 fork before you have 31 copies of it.

Step 2—Move the deep merge out of HCL into CUE. Delete the 59 `merge()` / 149 `try()` block from `locals.tf` and let unification do it. Measurable success criterion: the two merge-semantics tables in `CONTRACTS.md` become unnecessary. Do not skip this step and go straight to generating values—that is Option A, and it is the configuration that has already drifted.

Step 3—Only then, generate values, one non-production node first (`fitfile/testing` is the obvious candidate: 87 commits in 12 months, highest churn in the estate, no patient data). Render in CI, not on a laptop. Diff generated output against the current hand-written file until they match byte-for-byte, then switch the ArgoCD source.

Unrelated to CUE, and worth doing anyway: unpin `acr-test` and `wm-dev-1` from `feature/FFAPP-3073-new-ffnode-chart-with-vault-secrets`; delete the stray `ffnodes/fitfile/gh-pt-1/gh-pt-1/` nesting; fix or remove `scripts/template.sh`, which assumes a layout only two nodes still use.

---

### 9. What Would Make Me Argue against This

Stated plainly, because the case is not one-sided:

- If the team won't learn CUE, Step 0 is still worth it (a schema is readable even if the language isn't), but Steps 2–3 will produce a system one person maintains. That is worse than the status quo.
- If node count is about to shrink rather than grow, the duplication argument weakens considerably. Most of the payoff is amortised over future customers.
- If the real pain is release-train sprawl and ArgoCD sync behaviour rather than config correctness, CUE addresses neither (§5, rows 8–9) and the effort is better spent elsewhere.
- A cheaper 80% exists for §2.1 alone: a hand-written `values.schema.json` in `charts/ffnode/` is enforced by `helm template` natively, needs no new tooling, and no new language. It buys nothing for -2.3–2.5, but it is one file and one afternoon. If Step 0 stalls on tooling objections, do this instead.

---

### 10. Open Questions

1. Is `terraform-fitfile-platform-defaults` intended to stay the canonical source of platform defaults? If yes, Option B needs CUE to read its `common.yaml` directly, not via `infra_facts`.
2. Which of the two `ff-test-1` CUE copies is authoritative, and is the Grafana `deploy.monitoring` gate intended behaviour or an accidental divergence?
3. Are the nine release trains deliberate (per-customer change control) or accreted? That determines whether POC B's ring model is worth carrying forward.
4. Who owns `charts/ffnode`'s values contract? Step 0 requires someone to adjudicate which keys are genuinely open-ended and which are typos.
