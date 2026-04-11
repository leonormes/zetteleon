*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Saturday Apr 11, 2026 - 9:38 AM*
---
From your long-term memories — especially the consolidation into [MASTER_REMEDIATION_PLAN.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MASTER_REMEDIATION_PLAN.md), the state-driven framing in [TERRAFORM_STATE_AS_SOURCE_OF_TRUTH.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/TERRAFORM_STATE_AS_SOURCE_OF_TRUTH.md), the target shape in [CUSTOMER_DEPLOYMENT_MODULE_INTERFACE.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/CUSTOMER_DEPLOYMENT_MODULE_INTERFACE.md), and the process work in [MIGRATION_PLAYBOOK.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MIGRATION_PLAYBOOK.md) — plus the fact that your recent audit corrected several stale assumptions around 5:07 PM on Thursday and then restructured the plan again around 12:43 PM–12:54 PM on Friday — yes: I’d add several things.

The IDE plan is directionally right, but it still misses some hard-won lessons from your last month of work.

## Short version

I’d add **10 things**:

1. **A Phase 0 for live bug fixes before module extraction**
2. **A strict post-handoff rule: downstream reads only from `terraform output -json infra_facts`**
3. **A single-writer rule for every shared resource**
4. **A three-phase operational model, not just bootstrap vs steady-state**
5. **A clearer definition of what `infra_facts` actually is**
6. **Mandatory CI validation, not optional**
7. **A formal sunset plan for Gen 1 / Gen 2 patterns**
8. **A contract-fidelity rule for [mock_infra.json](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/cue/mock_infra.json)**
9. **A specific TheHyve remediation dependency chain**
10. **A “do not extract known defects into the shared module” gate**

## What I’d add to the plan

### 1) Add a new Phase 0: fix live correctness risks before extraction

This is the biggest missing thing.

Your plan jumps to “extract the fat customer stack,” but over the last month you found multiple issues that should be patched **before** they get baked into a shared module.

Based on your audit work documented around 2:04 PM and then consolidated around 5:07 PM on Thursday, I would explicitly add:

- **VaultAuth split-brain** must be resolved before extraction
- **Node pool label mismatch** (`workflow` vs `workflows`) must be resolved before extraction
- **TheHyve bypass path** must be brought under the normal pipeline before extraction
- **Stale generated customer artifacts** must be purged from template/demo repos before extraction
- **Known fallback mismatches** like `enable_grafana` in [locals.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/locals.tf) must be corrected first

Why: a shared module amplifies both good patterns and bad ones. If you extract first, you turn local bugs into platform bugs.

### 2) Add the post-handoff rule as a first-class architecture law

This came through strongly in your Friday notes around 12:43 PM and 12:54 PM.

I’d add this verbatim as a principle:

> **After bootstrap / handoff, all non-sensitive downstream configuration must read from `terraform output -json infra_facts` only.**

That means:

- CUE reads `infra_facts`, not [config/customer.yaml](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/config/customer.yaml)
- scripts read `infra_facts`, not re-derived formulas
- jumpbox rendering reads `infra_facts`
- Helm gets rendered values from CUE, not side-channel config

This is the cleanest way to prevent split-brain between “desired config YAML” and “actual realised TF state”.

### 3) Add a single-writer rule

This is the governance rule the IDE plan implies but doesn’t state.

I’d add a section to [CONTRACTS.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/CONTRACTS.md) like:

| Resource / Concept | Single Writer | Readers |
|---|---|---|
| Infra resources | Terraform | CUE / scripts / docs |
| Helm values | CUE | ArgoCD / Helm |
| Secrets values | Vault/VSO path | apps |
| App catalog | platform defaults + customer overrides | Terraform / CUE |
| Generated artifacts | pipeline only | ArgoCD / jumpbox |

And the rule:

> If a thing is rendered in both Terraform templates and CUE/Helm, that is a bug until proven otherwise.

This directly addresses the class of issues you found around VaultAuth and other duplicated ownership.

### 4) Change the operating model from “2-mode” to “3-phase runtime reality”

Strategically, bootstrap vs managed still makes sense.

Operationally, your own correction around 12:50 PM on Friday is important: the private-cluster reality means this is not just a neat two-step pipeline.

I’d preserve both views:

#### Strategic model
- Bootstrap
- Managed

#### Runtime execution model
1. **Phase A — Local bootstrap**
2. **Phase B — TFC private infra**
3. **Phase C — Jumpbox in-network cluster bootstrap/render/apply**

That correction matters because otherwise people will keep writing docs that imply “TFC apply => done”, which you already disproved.

I’d make this explicit in [MIGRATION_PLAYBOOK.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MIGRATION_PLAYBOOK.md), [README.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/README.md), and [MASTER_REMEDIATION_PLAN.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MASTER_REMEDIATION_PLAN.md).

### 5) Define what `infra_facts` actually is

A big thing from your state-as-truth work around 9:19 PM on Thursday:

`infra_facts` currently mixes:
- merged config
- deterministic computed values
- a small number of real live Terraform outputs

So I’d add a design decision. Choose one of these and document it:

#### Option A — Keep one `infra_facts`, but document subdomains
```hcl
infra_facts = {
  customer         = ...
  platform         = ...
  infrastructure   = ...
  central_services = ...
  computed         = ...
}
```

#### Option B — Split conceptually
- `infra_config`: merged/derived config
- `infra_state`: live resource outputs
- rendered together into one contract for CUE

I’d slightly prefer **Option A** for practicality, but with clear field provenance in docs.

The key is: stop pretending every field in `infra_facts` is “live state”. Your own audit found that most of it is not. That’s okay, but it must be made explicit.

### 6) Make CI validation mandatory

The IDE plan says optional validation of customer YAML. I would upgrade that to mandatory.

You’ve already spent too much time debugging silent drift for this to stay optional.

## Minimum CI gates I’d add

### Gate 1 — customer config validation
Validate [config/customer.yaml](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/config/customer.yaml) before plan.

Success:
- schema-valid
- mergeable with defaults
- no forbidden keys / shape drift

### Gate 2 — Terraform/CUE contract validation
Validate actual `infra_facts` against [schema_infra.cue](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/cue/schema_infra.cue).

Success:
- `cue vet` exits 0
- no missing fields
- no stale schema

### Gate 3 — generated artifact identity check
Your Friday work around 12:50 PM makes this critical.

Add `make verify-generated` and ensure:
- deployment key in generated values matches current customer
- repo URL / namespace / FQDN don’t belong to a copied old customer
- no stale `mkuh-prd-4` artefacts survive in new-customer repos

### Gate 4 — optional-but-useful Helm dry render
Good for catching nils and missing keys before jumpbox apply.

### Gate 5 — mock fidelity check
Keep [mock_infra.json](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/cue/mock_infra.json) structurally aligned with real output.

### Commands section
I’d standardise the verification section around:

```bash
terraform fmt -check
terraform validate
terraform plan -out=plan.tfplan

make validate-cue
make validate-cue-mock

INFRA_JSON=$(terraform output -json infra_facts | jq -c '.value // .')
cue vet ./cue/*.cue -t "infra=$INFRA_JSON"

make generate-values
make verify-generated

cd helm_chart_deployment
helm template ffnode charts/ffnode -f ../ff-test-1/generated/values.yaml --dry-run
```

### What success looks like
- No contract mismatches
- No stale identity leakage
- No Helm nils
- No accidental generation against old customer data

### What failure means
- Contract drift
- stale copied artefacts
- schema lag
- parallel ownership bug
- missing live outputs in the pipe

### 7) Add a Gen 1 / Gen 2 sunset plan

Your [MASTER_REMEDIATION_PLAN.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MASTER_REMEDIATION_PLAN.md) already talks about three generations in one codebase. The IDE plan doesn’t say how they die.

I’d add a section:

## Legacy pattern deprecation map

| Legacy Pattern | Current Location | Status | Exit Plan |
|---|---|---|---|
| bootstrap-era provider handling | customer repos | transitional | keep for Phase A only |
| old central-services assumptions | legacy repo/docs | reference-only | freeze + document |
| hardcoded jumpbox app blocks | templates | active debt | move to app catalog |
| per-customer fat locals | customer repos | active debt | replace with shared module |
| direct template bypasses | special-case components | active debt | route through CUE/shared module |

This keeps the migration honest. Otherwise “new model” docs accumulate while old mechanisms remain active forever.

### 8) Add a contract-fidelity rule for the mock

This is smaller, but it matters.

You identified around 1:28 PM and 4:45 PM on Thursday that mock data was blind to real VSO paths until updated. That’s exactly the kind of thing that silently rots.

I’d add:

> `cue/mock_infra.json` is not example data; it is a contract fixture.

Rules:
- update it whenever `infra_facts` shape changes
- generate or refresh it from a known-good real environment where possible
- CI fails if real `infra_facts` contains keys absent from the mock contract fixture

### 9) Add a specific TheHyve remediation dependency

TheHyve should not just be “one of many apps in the catalog”. It has an outstanding architectural exception.

I’d add a tracked sequence:

1. move TheHyve rendering into CUE
2. move TheHyve literals into policy/defaults
3. route secret wiring through shared dispatch
4. only then delete raw template bypasses
5. only then include it in the extracted shared customer module

That dependency should be explicit in the roadmap, otherwise you risk preserving the bypass inside the new module architecture.

### 10) Add a “bad extraction” prevention checklist

Before moving anything from [locals.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/locals.tf) into a shared module, require this checklist:

- Is there already a single writer?
- Is the source of truth documented?
- Is the field in `infra_facts` because CUE actually needs it?
- Is the merge rule stable enough to centralise?
- Does the mock cover it?
- Is there a CI gate for regression?
- Are we extracting behaviour, or extracting a bug?

That would stop a lot of “clean-looking but premature” abstraction.

---

## What I would change in your current directions A–E

## A. Extract fat customer stack into shared module
Add:
- **Do this incrementally**
- Extract merge helpers first
- Extract catalogs second
- Extract `generators/` third
- Only collapse customer repo after the edge cases are normalised

Also add a prerequisite:
- no unresolved split-brain ownership issues may enter the shared module

## B. Replace imperative lists with platform catalogs
Strongly agree, but add:
- catalog entries need **schema + versioning**
- conditions should use stable predicates, not ad hoc string expressions everywhere
- app catalog must define **owner**, **value file path**, **enablement flag**, **bootstrap mode**, and **deployment mode**

A useful target shape would be something like:

```yaml
argocd_catalog:
  ffnode:
    enabled_when: deploy.ffnode
    chart: charts/ffnode
    values_file: generated/values.yaml
    owner: cue
  thehyve:
    enabled_when: deploy.thehyve
    chart: charts/integrations/thehyve
    values_file: generated/thehyve_values.yaml
    owner: cue
```

## C. Tighten the “add a field” workflow
Upgrade “optional validate in CI” to **mandatory**.

Also add a triage question at the top:
> Does this field belong in customer intent, platform defaults, Terraform-computed facts, Vault, or generated values?

That one question will prevent half the churn.

## D. Align ArgoCD app-of-apps across repos
Agree. I’d add:
- don’t just unify representation — unify **source ownership**
- pick one catalog that both jumpbox generation and any app-of-apps model consume
- legacy repo patterns should be explicitly marked “legacy only / no new customers”

## E. Secrets stay data-driven
Agree. I’d add one stronger principle:
- sensitive values stay out of `infra_facts`
- secret references, consumers, mount paths, and non-sensitive metadata can be in `infra_facts`
- secret *values* remain Vault/VSO only

That boundary needs to be written down clearly.

---

## A better success criteria section

I’d extend your “what success looks like” with measurable outcomes.

| Metric | Current smell | Target |
|---|---|---|
| Customer repo local logic | fat [locals.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/locals.tf) | thin wrapper / passthrough |
| Add new app | multiple code edits across repos | catalog entry + chart wiring |
| Add new secret consumer | new HCL/CUE special cases | data-only extension |
| Add new field | repeated layer edits with guesswork | documented contract path |
| Generated artifact safety | stale copied files possible | `verify-generated` gate |
| Ownership clarity | duplicated writers possible | one owner per resource |
| Real/mocked contract parity | can drift silently | enforced in CI |
| Legacy model bleed | Gen 1/2/3 overlap | documented migration + deprecation |

---

## Recommended execution order

This is the sequencing I’d use, based on your audit history:

1. **Patch live bugs and stale assumptions**
   - ownership conflicts
   - scheduling mismatch
   - stale generated artefacts
   - fallback mismatches

2. **Write the architecture laws**
   - post-handoff rule
   - single-writer rule
   - sensitive vs non-sensitive flow rule

3. **Add mandatory CI gates**
   - customer YAML validation
   - contract validation
   - verify-generated
   - mock fidelity

4. **Move imperative lists to catalogs**
   - namespaces
   - app catalog
   - app enablement rules

5. **Normalise special-case integrations**
   - especially TheHyve

6. **Extract shared module incrementally**
   - merge helpers
   - derivation logic
   - `generators/`
   - thin customer repo

7. **Deprecate Gen 1 / Gen 2 artefacts**
   - docs
   - scripts
   - patterns
   - compatibility notes

---

## Bottom line

Yes — your IDE plan is good, but based on the last month of work I’d add three major upgrades:

1. **More sequencing discipline**
   - patch correctness first, extract second

2. **Stronger architecture laws**
   - post-handoff rule
   - single-writer rule
   - three-phase runtime reality

3. **Enforcement, not aspiration**
   - mandatory CI
   - contract fixture fidelity
   - generated-artifact identity checks

If you want, I can turn this into a **merge-ready addendum** for [MASTER_REMEDIATION_PLAN.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/MASTER_REMEDIATION_PLAN.md) and [CONTRACTS.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/New_Customer/ff-test-1/docs/CONTRACTS.md), or rewrite your IDE plan into a cleaner **Phase 0 / A / B / C roadmap**.