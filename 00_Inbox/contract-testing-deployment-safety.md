---
created: 2026-09-18T12:31:15+00:00
modified: 2026-09-21T09:17:35+00:00
permalink: llmeon/00-inbox/contract-testing-deployment-safety
title: contract-testing-deployment-safety
type: note
---

## Contract Testing: Deployment Safety (Can-i-deploy / record-deployment)—design Sketch

Companion to [Contract testing: current setup](./contract-testing.md) and

[Contract testing: candidates for new tests](./contract-testing-candidates.md). Updated twice

after reviewing the `fitfile/deployment` repo directly—first pass corrected a wrong

dev/staging/prod guess with the real ffnode model; this pass corrects the secret-provisioning

recommendation after confirming the Sleuth-hook pattern I originally pointed to is legacy.

### The Real Environment Model

`fitfile/deployment` is a GitOps repo: ArgoCD deploys Helm charts (`charts/`) to a set of

independent ffnodes (`ffnodes/<org>/<node>/values.yaml`)—one per real deployment target.

This is not a three-tier dev/staging/prod ladder. There are ~20+ nodes: internal ones

(`fitfile/development`, `fitfile/testing`, `fitfile/sandbox-testing-{1..5}`) and one per real

customer/hospital deployment (`fitfile/ff-a/b/c`, `barts/prod`, `eoe/cuh-prod-1`,

`eoe/hie-prod-34`, `nwsde/mcnft-prod-1`, etc., each usually paired with a `-test`/`test-34`

counterpart).

The only place a canonical, small environment vocabulary actually exists is Sleuth

(getsleuth.io, the deployment-tracking tool wired into `charts/components/{ffcloud-service,frontend,fitconnect}`):

each real customer/test node sets `sleuth.environment: production` or `sleuth.environment: test`.

`fitfile/development` and `fitfile/testing`—the two internal nodes—have no `sleuth` block

at all; they're not tracked by this mechanism.

### Where the Deploy-success Signal Actually Lives (Two Different Answers)

For the internal `testing` node: there's a real, CI-observable deploy-then-verify cycle,

already running on every relevant MR. `InsightFILE`'s `trigger_integration_tests` job (merge-train

only) triggers this repo's `staging.gitlab-ci.yml` as a child pipeline: `sync_argo_app` forces an

ArgoCD sync of the testing images, then `run_integration_tests` runs the full Argo Workflow

integration suite against it. Both jobs succeeding _is_ a genuine "this version deployed and

works" signal, already gated on merge-train pipelines. This is the best available hook point for

`record-deployment` against a `test`-equivalent environment, if that's ever wanted.

For the internal `development` node: no explicit CI signal exists. ArgoCD auto-syncs

`development` continuously via GitOps whenever `gapv` (InsightFILE's release pipeline) commits a

new image tag to `ffnodes/fitfile/development/values.yaml`—there's no job in this repo that

confirms the sync actually succeeded. `record-deployment` against `development` isn't

straightforward without adding new observability, not because of missing broker access.

For real customer/production nodes: the _shape_ of the answer (a `PostSync` ArgoCD hook Job)

is right, but where I originally sourced the pattern from was wrong—see below.

### Correction: the Sleuth Hook's Secret Pattern is Legacy, Don't Copy it

`charts/components/{ffcloud-service,frontend,fitconnect}/templates/deployment-success-sleuth-hook.yaml`

is a real `PostSync`-hook Job shape (curl Sleuth's `register_deploy` with `environment`+`sha`,

auth from a K8s Secret)—that mechanic is still a good template. But the Secret it reads

(`sleuth-secret`, from `global.sharedSecrets.sleuth.apiKey`) is populated by the `charts/shared-secrets`

chart, which—confirmed by checking where it's actually deployed—is only bootstrapped for

`kch/prod`, `kch/mn4`, and `stg/sandbox`. Those are legacy, decommissioned nodes, not

currently-running clusters. Worse, that chart's secrets are plaintext values committed directly

in `ffnodes/<node>/values/shared-secrets-values.yaml`—fine to leave as historical git content

now that nothing reads them, but not a pattern to extend.

The actual, currently-used mechanism for active nodes (confirmed in `charts/ffnode`, the

umbrella chart real nodes like `fitfile/ff-a` are built from) is HashiCorp Vault Secrets

Operator: each component declares a `vaultSecrets: [{secretName, vaultPath}]` list in

`charts/ffnode/values.yaml` (e.g. `mongodb`, `postgresql`, `ffcloud`, `frontend`, `fitconnect`,

`spicedb` all do this today), which the chart expands into a `VaultDynamicSecret`

(`secrets.hashicorp.com/v1beta1`) resource—VSO then syncs the real secret from Vault

(`admin/deployments/<deploymentKey>/<vaultPath>` by default) into a native K8s Secret, restarting

pods on rotation. This only activates when `global.vault.enabled` is true (see

`charts/ffnode/templates/_helpers.tpl`, `generateVaultDynamicSecrets`).

Notably, no `vaultSecrets` entry for `sleuth` exists in `charts/ffnode/values.yaml` either,

despite `ff-a`'s component values setting `sleuth.enabled: true`—worth a sanity check by whoever

owns this repo on whether Sleuth reporting is actually working for any live node right now. Not

chased further here; out of scope for this design sketch.

### Revised Recommendation: Provision the Pact Broker Credential via `vaultSecrets`, not `sharedSecrets`

Add a `vaultSecrets` entry to `ffcloud`/`frontend`'s block in `charts/ffnode/values.yaml`,

matching the existing pattern:

```yaml
ffcloud:
  vaultSecrets:
    - secretName: "pact-broker"
      vaultPath: '{{ include "applicationVaultPath" . }}'
```

with the actual credential stored in Vault at the resolved path (not in this git repo, plaintext

or otherwise). The `PostSync` hook Job keeps the same shape as the Sleuth one, just reading from

the `pact-broker` Secret VSO creates:

```yaml
{{- if .Values.pactBroker.enabled }}
apiVersion: batch/v1
kind: Job
metadata:
  generateName: pact-broker-record-deployment-
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: pact-record-deployment
          image: curlimages/curl
          command:
            - "curl"
            - "-X"
            - "PUT"
            - "-u"
            - "$(PACT_BROKER_USERNAME):$(PACT_BROKER_PASSWORD)"
            - "{{ .Values.pactBroker.baseUrl }}/pacticipants/{{ .Values.pactBroker.pacticipant }}/versions/{{ .Values.pactBroker.commit.sha }}/deployed-versions/environment/{{ .Values.pactBroker.environment }}"
          env:
            - name: PACT_BROKER_USERNAME
              valueFrom: { secretKeyRef: { name: pact-broker, key: username } }
            - name: PACT_BROKER_PASSWORD
              valueFrom: { secretKeyRef: { name: pact-broker, key: password } }
      restartPolicy: Never
  backoffLimit: 2
{{- end }}
```

(Endpoint shape is still illustrative—confirm the exact REST contract, or use an image with the

`pact-broker` CLI, when this is actually built.)

This still sidesteps the GitLab protected-variable problem from

[FTFL-1101](https://fitfile.atlassian.net/browse/FTFL-1101)—the credential lives in Vault and

reaches the cluster via VSO, never touching a GitLab CI/CD variable—and it's the pattern this

repo actually uses today, not a decommissioned one.

`.Values.pactBroker.commit.sha` would be wired the same way `sleuth.commit.sha` already is: gapv's

`additionalProperties` in `deployment/pipeline/common/gapv-deployment.yaml` (InsightFILE) already

sets `sleuth.commit.sha` from `CI_COMMIT_SHA` on every relevant chart bump—the same pattern adds

a `pactBroker.commit.sha` property for free.

### `can-i-deploy`—still An Open Question, for a Different Reason than before

Unlike `record-deployment`, I didn't find an obvious automated gate to attach `can-i-deploy` to for

_real_ customer-node promotion. `release.sh`/`release-improved.sh` in this repo handle tagging and

GitLab release mechanics for InsightFILE itself, not bumping a specific ffnode's image tag—

promoting a version to e.g. `ff-a` looks like a manual `values.yaml` change/PR, not an automated

step. So there's no single CI job to insert a blocking (or even advisory) `can-i-deploy` call into

for production promotion yet; whoever does that manual promotion would need to run it themselves,

or that promotion step would need to become automated first.

The one place `can-i-deploy` _can_ run today without new infrastructure is the advisory job

already sketched in this note's first version—in InsightFILE's `release.gitlab-ci.yml`, before

the `development`/`testing` auto-promotion, using the existing `PACT_BROKER_*` GitLab CI/CD

variables (unprotected, per the FTFL-1101 decision). Unchanged by this update.

### Bonus Finding: This Team Already Solved the protected-variable-vs-MR-pipeline Problem once

`staging.gitlab-ci.yml`'s `sync_argo_app` job has a comment (referencing FTFL-1061/FTFL-976)

explaining it deliberately uses the AKS kubeconfig via Azure OIDC (`argocd --core`) instead of

logging into the ArgoCD API with `ARGOCD_STAGING_USERNAME`/`PASSWORD`, because that pair is a

protected group variable and "isn't sent to merge-train pipelines"—the exact same

GitLab behaviour documented on FTFL-1101 for `PACT_BROKER_*`. Their fix was swapping a static

protected secret for an OIDC/workload-identity credential, not loosening protection. Worth citing

back on FTFL-1101 as the long-term direction if the team ever wants `PACT_BROKER_*` to be both

protected and available on every MR—not needed for this PoC, but precedent exists in this repo.

### Remaining Open Questions

- Exact Pact Broker REST contract for recording a deployment (or which image ships the
  `pact-broker` CLI)—needed before the hook sketch above is real.
- Whether/how ffnode promotion to a real customer node ever becomes automated enough to host a
  `can-i-deploy` gate—currently looks manual.
- Whether Sleuth deployment tracking is actually functioning for any currently-active node, given
  no `vaultSecrets` entry provisions it—flagged for whoever owns this repo, not pursued further
  here.
