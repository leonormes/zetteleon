---
created: 2026-06-06T00:00:00+00:00
modified: 2026-06-06T08:04:33+00:00
related: ["[[ffnode-templating-analysis]]", "[[ffnode-templating-complexity-metrics]]"]
tags: [1, 2, config, cue, cuelang, deployment, ffnode, helm, kubernetes, multi-cluster, type-safety, validation]
ticket: FTFL-673
title: ffnode-cue-evaluation-and-stage1-schema
type: project
project_category: refined_deployment
project_status: active
project_name: "Refined Deployment"
---

> Evaluation of [CUE](https://cuelang.org/) for the `ffnode` deployment config, plus a working, fleet-tested Stage-1 validation schema.
> Companion to [[ffnode-templating-analysis]] and [[ffnode-templating-complexity-metrics]].

## Verdict

Yes—but as a validation/generation layer in front of the Helm + ArgoCD you keep, adopted in stages. Not as a Helm/ArgoCD replacement.

The CUE-native package manager (Timoni) integrates with Flux, not ArgoCD—and your App-of-Apps-on-ArgoCD architecture is the part that already scores 4/5. So the move is to bolt CUE on as a safety net, not to re-platform.

Stage 1 (validation only) is almost pure upside and supersedes the `values.schema.json` recommendation from [[ffnode-templating-complexity-metrics]]—same goal, far more expressive. Stages 2–3 carry real bus-factor risk and should be gated on the team actually wanting to learn CUE.

---

## How CUE Maps onto the Weak Scorecard Metrics

| Metric (current) | What CUE does |
|---|---|
| C1 Schema enforcement (1) | CUE's core. Types _are_ constraints. `if enabled { ingress: host: string & =~"^faro" }` makes the empty-host case unrepresentable. Can `import` k8s OpenAPI/CRD schemas to validate against the real API contract. |
| A4 Convention count (2) | CUE _unifies_: one way to express a constraint; conflicts are compile errors, not last-write-wins. The "3 secret-transform modes + 2 escaping styles" sprawl collapses. |
| B1 Value fan-out (2) | `ingress.host` becomes one field that the ingress, cert `dnsNames`, and frontend `FARO_COLLECTOR_URL` all _reference_—drift becomes structurally impossible. |
| B4 Blast-radius (2) | A base change that violates any cluster's constraints fails `cue vet` for that cluster before shipping. |
| C4 Feedback latency (1) | `cue vet` runs in ms in CI/pre-commit—failure moves left from ArgoCD-sync/runtime to the editor. |
| D3 Drift visibility (2) | Every cluster is a CUE value of one schema → a "cluster → version" table is a trivial `cue export`. |

Six of the seven lowest scores. CUE is unusually well-aimed at this problem.

## What CUE Does NOT Fix (be honest)

- The VSO `tpl`-escaping problem (A3) survives if CUE only generates `values.yaml` and Helm still `tpl`s them—the double-eval is a _Helm_ artifact. CUE only retires it if CUE generates the final `VaultStaticSecret` manifest directly, bypassing Helm `tpl` (that's Stage 3, the most invasive).
- No native ArgoCD integration—Timoni→ArgoCD doesn't exist. Use ArgoCD CMP to run `cue export` at render time, or (simpler) run CUE in CI to _generate/validate_ the `ffnodes/*` overlays Helm already consumes.
- Learning curve / bus-factor. CUE's unification model is genuinely different (not "YAML with types"). The stated problem is _"only Ollie understands the templating"_—adopt CUE carelessly and you trade it for _"only one person understands CUE."_ Biggest risk; gate the rollout on it.
- Alternative if CUE feels too alien: KCL (more imperative/Python-ish, gentler curve).

---

## Staged Adoption (ArgoCD untouched)

1. CUE as validator only (1–2 wks, lowest risk)—schema for `ffnodes/*` overlays, `cue vet` in CI. Everything else unchanged. Done below—it works.
2. CUE generates the overlays (1–2 mo)—cluster config as small CUE files; `cue export` renders `values.yaml`. Enforces B1/B2/D3 by construction.
3. (Optional) CUE generates the risky manifests directly—move just the VSO secrets out of Helm `tpl`. Only thing that retires A3. Do last, only if Stage 2 sticks.

---

## Stage-1 schema—written and Tested against the Real Fleet

File committed to the repo at `ffnodes/schema/cluster_values.cue`. Scope is deliberately narrow: validate the high-value, drift-/bug-prone fields; leave every sub-chart block open (`…`) so existing overlays pass unmodified.

```cue
// Package ffnodes — Stage-1 validation for ffnodes/<hub>/<cluster>/values.yaml.
package ffnodes

#Hostname: =~"^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$"

#ClusterValues: {
	// Identity — required on every cluster-root overlay
	namespace:     #Hostname
	deploymentKey: #Hostname
	host?:         #Hostname

	// Feature toggles: every listed flag must be a bool (catches `"true"` / `ture`)
	deploy?: {
		certManager?: bool
		monitoring?:  bool
		frontend?:    bool
		fitconnect?:  bool
		spicedb?:     bool
		workflowsApi?: bool
		persistence?: bool
		coordinatingStation?: bool
		initialiseCluster?:   bool
		messageBroker?:       bool
		mssql?:               bool
		seedData?:            bool
		mutatingProxyWebhook?: bool
		workflowsIntegrationTests?: bool
		blobCsiDriver?: bool
		mongodbNext?:   bool
		...
	}

	argocdApp?: {targetRevision: string & !="", ...}

	proxy?: {
		enabled: bool | *false
		if enabled {proxyUrl: string & =~"^https?://"}
		...
	}

	// Grafana Alloy / Faro — the block that produced the FTFL-673 bugs
	grafanaAlloy?: {
		frontendObservability?: {
			enabled: bool | *false
			// KEY CONSTRAINT: a non-empty faro host is REQUIRED when enabled.
			// This is exactly the guard the Helm template missed.
			if enabled {ingress: host: #Hostname & =~"^faro"}
			environment?: string
			tls?: {createCertificate?: bool | *true, existingSecret?: string, ...}
			...
		}
		...
	}
	...  // all other sub-chart blocks: allowed, unchecked in Stage 1
}
```

### Proven Results (`cue v0.16.1`, Run 2026-06-06)

- 24 / 25 cluster-root overlays PASS unmodified.
- The 1 "failure" is `stg/sandbox`—not a bug: it has its own `Chart.yaml` + `templates/` (a divergent layout) with no top-level `namespace`/`deploymentKey`. The schema usefully surfaced that 24 of 25 clusters share one shape and one doesn't—exactly the fleet-heterogeneity you want flagged. Exclude chart-style dirs from the vet glob.
- Negative tests both correctly REJECTED:
  - `frontendObservability.enabled: true` + empty `ingress.host` →
    `invalid value "" (out of bound =~"^faro")` ✅ (this is the FTFL-673 Bug 1 class)
  - `deploy.monitoring: "true"` (string) →
    `conflicting values "true" and bool (mismatched types string and bool)` ✅

So the schema accepts every real cluster, rejects the exact bugs that shipped, and flags structural drift—with readable error messages pointing at file:line.

---

## CI Snippet (GitLab `validate` stage)

Drop this next to `lint_workflows`. Targets the homogeneous cluster-root overlays and skips chart-style dirs (those with a sibling `Chart.yaml`).

```yaml
vet_ffnodes:
  stage: validate
  image: cuelang/cue:0.16.1   # or install cue in your existing image
  script:
    - |
      fail=0
      for f in $(find ffnodes -mindepth 3 -maxdepth 4 -name values.yaml | grep -vE '/values/'); do
        dir=$(dirname "$f")
        # skip self-contained chart dirs (e.g. stg/sandbox) — different shape
        [ -f "$dir/Chart.yaml" ] && continue
        if ! cue vet -d '#ClusterValues' ffnodes/schema/cluster_values.cue "$f"; then
          echo "SCHEMA FAIL: $f"; fail=1
        fi
      done
      exit $fail
  rules:
    - changes: ["ffnodes//*", "ffnodes/schema/*.cue"]
```

### Next Refinements (cheap, High value)

- Tighten `deploymentKey` to equal the directory name (catches copy-paste clusters).
- Add a cross-field rule: if `proxy.enabled` then `argocdApp.globalIgnoreDifferences` must include the HTTP_PROXY excludes (CUH pattern).
- Stage-1.5: a CUE check on the _base chart_ `values.yaml` asserting every `faro-*` / `*-bearer-token` key produced is consumed by a template—this is what catches the `fargo-bearer-token` typo (Bug 2), which lives in the base chart, not the overlays.

---

## Bottom line for the Two Goals

- Keeping clusters aligned: CUE turns "aligned by review" into "aligned by construction"—every overlay must satisfy one schema. Stage 1 already enforces this for the bug-prone fields.
- Maintaining versions as you scale: Stage 2 (`cue export` overlays) makes a fleet-wide version table and staged rollouts a query, not a grep. The architecture that makes this work (App-of-Apps, pinned `targetRevision`) is already in place.

Sources: [Timoni](https://github.com/stefanprodan/timoni) · [Timoni comparison](https://timoni.sh/comparison/) · [CUE→k8s manifests](https://devops-db.com/cue-lang-from-strict-validation-to-dynamic-kubernetes-manifests/) · [CUE + ArgoCD discussion](https://github.com/argoproj/argo-cd/discussions/14472)
