---
created: 2026-05-15T08:23:22+00:00
modified: 2026-05-15T08:48:48+00:00
title: Optimising a Live GitOps Pipeline
---

You

I also have a complex task of optimising our existing deployment pipeline. We have a gitops process but it is not optimal. We need to improve it while it is in use. First should be an investigation into the current setup then planning for improvements. Give me the same natural planning model help Optimising a live delivery pipeline while it is actively serving an engineering team is akin to changing the tyres on a moving car. The Natural Planning Model is an excellent framework for tackling this, ensuring you define the boundaries before diving into the technical weeds of the investigation. Here is a trigger list tailored for investigating and upgrading a live GitOps process: ### Phase 1: Purpose and Principles * **Purpose:** Why are we optimising the pipeline right now? Is the primary driver to reduce lead time for changes, improve deployment frequency, or eliminate manual bottlenecks? * **Executive Issues:** How does a faster or more reliable pipeline support the broader business objectives or product delivery roadmaps? * **Principles:** What are the non-negotiable rules for this project? (e.g., no disruption to the team's ability to ship to production, ensuring small incremental changes rather than a "big bang" pipeline replacement, or adhering strictly to Lean software engineering principles). ### Phase 2: Vision/Outcome * **Ideal Scenario:** What does the optimal state look like? Imagine the deployment process in six months: developers are receiving immediate feedback, the ArgoCD reconciliation loop is seamless and entirely automated, and configuration drift is a thing of the past. * **Measurement:** How will you prove the pipeline is better? What metrics will define success? (e.g., tracking the Four Key Metrics: deployment frequency, lead time, mean time to restore, and change fail percentage). ### Phase 3: Brainstorming * **Current State Investigation:** What is actually happening versus what is documented? Where are the queues and waiting times? (e.g., waiting for tests to run, waiting for environments to provision, or waiting on pull request approvals). * **Technical Architecture:** How is the current GitOps operator configured? Are there long-lived branches causing integration pain, or is the team successfully practicing trunk-based development? How are secrets managed and propagated to k8s? * **Risks & Mitigation:** What happens if an in-flight pipeline change breaks deployment capabilities? How quickly can you roll back the pipeline configuration itself? * **Information Gathering:** Who needs to be consulted? (e.g., gathering candid feedback from the developers who use the pipeline daily to find out what frustrates them the most). ### Phase 4: Organising * **Phasing the Work:** How do you break this down into safe, manageable increments? * *Phase A:* Value stream mapping and metric baseline gathering. * *Phase B:* Optimising the Continuous Integration (CI) feedback loop (e.g., parallelising test suites). * *Phase C:* Refining the Continuous Deployment (CD) sync policies and manifest management. * **Communication:** How will changes to the pipeline be communicated to the team so they aren't surprised by shifting deployment behaviours? * **Tooling:** Do you have the necessary observability tools in place to monitor the health of the deployment pipeline itself? ### Phase 5: Next Actions * **The Next Step:** What is the very next physical, visible action required to start the investigation? * **Process Actions:** Instead of "investigate pipeline," drill down to the atomic action. For example: *"Schedule a 60-minute value stream mapping whiteboard session with the core team to trace a single commit from local workstation to live production."* or *"Run a query to extract the average build times for the last 30 days."*

---

Claude

## Optimising a Live GitOps Pipeline: Scoping & Critique

### 1. The Real Problem (Reframe)

Your instinct—_"investigate first, then plan improvements"_—is correct and ahead of where most engineers start. But it hides an important truth:

> "Investigate the pipeline" and "improve the pipeline" are two different projects, not two phases of one project.

They have different deliverables, different cadences, different success criteria, and different stop conditions. Conflating them produces the classic anti-pattern: investigation bleeds into half-investigation/half-fixing, you can never tell when investigation is _done_, and the improvement project never gets cleanly scoped.

So the work is actually:

- Project I—Pipeline Investigation. Deliverable: a written audit (current state, bottlenecks, evidence-based pain ranking). Done when audit is committed.
- Project O₁..Oₙ—One or more Optimisation projects. Each natural-planned _from the audit_, not from speculation.

You only natural-plan Project I right now. The optimisation projects don't exist yet—they'll be born out of the audit.

Layered onto this is the _real_ constraint: the pipeline is live and multi-tenant. Every change is essentially a production change to multiple customer environments. That's not a footnote—it's a first-class principle that should appear in Phase 1.

---

### 2. Scoping Trigger List

Same format as before. Answer briefly; the goal is to expose ambiguity.

#### A. Which "pipeline", Actually?

You have at least six pipelines stacked on top of each other. Pick one (or rank them):

- A1. Application CI → image build → registry push _(developer-facing)_
- A2. GitOps repo workflow—PR → review → merge → sync trigger
- A3. ArgoCD reconciliation—app-of-apps, sync waves, Helm rendering
- A4. Infrastructure provisioning—Terragrunt → Terraform Cloud → Azure
- A5. Cluster bootstrap—apex chart → Vault → VSO → cert-manager → workloads
- A6. Secret delivery—Vault KV → VSO → Kubernetes Secret → workload

In your recent months, A3, A5, and A6 have produced almost all the pain. That's where the evidence already points.

#### B. Who is the Primary User?

The optimisation target is wildly different per persona:

- Application developers—care about commit-to-prod lead time
- You / platform team—care about bootstrap reproducibility, drift, on-call burden
- Customer admins—care about predictability and change comms
- Compliance / NHS audit—care about traceability and approvals

You cannot optimise for all four simultaneously.

#### C. What Kind of Optimisation?

Different goals = different projects:

- Lead time reduction
- Deployment frequency increase
- Change failure rate reduction
- MTTR improvement
- Cognitive load reduction (for whom—see B)
- Bootstrap reproducibility _(your recurring fire)_
- Drift elimination
- Cost
- Auditability

#### D. Problem source—measured Vs Assumed

- Documented problems from post-incident reviews?
- Pain captured in tickets / Slack threads?
- Your own field notes from the `mkuh-prd-4` debugging marathons?
- Cargo-culted "best practice" gap (be honest)?
- Developer whinge data?

A useful audit weights these sources. Field notes from real incidents beat developer survey responses every time.

#### E. Baseline—what's Instrumented Today?

You cannot improve what you cannot measure. Audit must record:

- Are DORA metrics captured? (Almost certainly _no_ for the infra/cluster pipelines.)
- ArgoCD sync durations per app, per cluster?
- TF apply durations per workspace?
- PR-to-merge time on the GitOps repo?
- Vault token refresh rates, VSO reconcile latencies?
- Bootstrap-from-zero wall time per customer cluster?

If half of these aren't instrumented, the first optimisation project is instrumentation, not the optimisation you think you want.

#### F. Blast Radius & Safety

- How many customer clusters share this pipeline? (You've named `mkuh-prd-4`, `lca-prd-2`—assume more.)
- Change window for pipeline changes?
- Rollback path _for the pipeline itself_—well-defined?
- Can you canary a pipeline change against one customer cluster before broad rollout?

#### G. Deliverable Shape

The investigation deliverable should be specific:

- An ADR-format audit committed to the platform repo?
- A wiki page with embedded Grafana panels?
- A ranked pain-point register with reproduction recipes?
- A value-stream diagram?

I'd recommend: ADR + ranked pain-point register, in the platform repo, reviewable as a PR.

#### H. Time, Focus, Scope

- How much focus time per week? (Be honest—you've also got `omop-cli` and the MKUH cluster bootstrap to stabilise.)
- Solo or with collaborators?
- Hard "no-touch" customer windows?
- Is this self-initiated or backed by a business goal? _(Self-initiated optimisation projects die first when priorities shift.)_

#### I. Definition of done—for the Investigation

Complete this sentence:

> _"The investigation is finished when ___ exists, ___ has been reviewed by ___, and the top three pain points have a documented reproduction recipe."_

If you can fill that in, you have a project. If you cannot, you have a wishlist.

---

### 3. Critique of the LLM Response

It's a fluent template that uses the right vocabulary (DORA, value stream, trunk-based) without engaging with _your_ environment. Specific gaps:

1. No engagement with your actual stack. Doesn't mention ArgoCD app-of-apps, sync waves, Helm/OCI, Terragrunt, Vault/VSO, Terraform Cloud. The pain you've documented over months (double- `tpl` bug, `overwrite: false`, JWT role bootstrap order, ArgoCD auto-sync racing imperative patches) doesn't surface anywhere. A real plan would name names.
2. Conflates investigation and improvement. It frames them as one project. They are not. The audit deliverable scopes the optimisation projects—they have separate natural-planning passes.
3. "Pipeline" is left fatally ambiguous. The plan never asks _which_ pipeline. As above, you have six.
4. DORA without caveats. The Four Key Metrics were defined for application delivery, not platform/infra pipelines. Lead time for an AKS bootstrap is conceptually different from lead time for an application change. Using DORA uncritically here is a category error worth calling out.
5. Risks section is generic. Real risks for your context: pipeline-as-code self-bootstrapping (chicken-and-egg when ArgoCD manages itself), GitOps repo merge conflicts blocking multiple customers simultaneously, OCI chart tag drift, `overwrite: false` causing stealth staleness, double- `tpl` evaluation, multi-tenant blast radius if a "shared" component (cert-manager, VSO operator) is mis-configured.
6. No mention of "strangler fig" or migration patterns. The right architectural pattern for changing a live pipeline is augment-and-deprecate, never rip-and-replace. This is the single most important principle missing.
7. "Brainstorming" suggests trunk-based development as if it's a fix. Trunk-based development is a developer-team practice. It doesn't help if the bottleneck is `argocd-application-controller` saturation or VSO reconcile loops. The LLM doesn't distinguish _developer workflow_ problems from _platform reconciliation_ problems.
8. Tooling section is empty. No mention of `argocd-image-updater`, `argocd-notifications`, `kubent`, `kube-score`, `kubeconform`, OPA/Gatekeeper for pipeline policy, Renovate/Dependabot for chart bumps, or the obvious one: eating your own dog food (pipeline changes go through the pipeline).
9. No multi-tenant framing. Your pipeline is a _product_ serving multiple customer environments. The plan should treat it as such—versioning, deprecation policy, comms cadence.
10. Next Action is again wrong for your role. Scheduling a value-stream mapping session with "the core team" assumes a team-driven process. You're the principal. You drive this; the team contributes.

---

### 4. Over-Advice (Things You Didn't Ask About)

#### 4.1 Strangler Fig is the only Safe Pattern here

Never replace a live pipeline. Instead: build the new path alongside the old, migrate one customer cluster at a time, deprecate the old path explicitly. Every optimisation project should have this shape:

1. New path exists and is exercised by one canary customer
2. New path validated against old over an agreed window
3. Migration plan per customer
4. Old path archived (not deleted) with sunset date

If an optimisation idea can't fit this shape, it's too big—split it.

#### 4.2 Value Stream Mapping—useful, but ADHD-hazardous

VSM is brilliant _if done in one sitting_ and _if the scope is one value stream_. If you start with "map the entire pipeline," you'll be at it for weeks and produce nothing. Constrain it: "map a single config change to `mkuh-prd-4`, commit-to-applied, in one 90-minute session, in `excalidraw` or on paper."

#### 4.3 Instrument before optimising—but Don't Gold-plate

Minimum viable instrumentation:

- ArgoCD app sync duration histogram (Prometheus already emits this)
- TF Cloud run duration via API export
- GitOps repo merge → first sync timestamp (custom)
- VSO reconcile success/failure counts (Prometheus)

Put them on a single Grafana dashboard named `platform-pipeline-health`. That dashboard is itself a deliverable.

#### 4.4 The Pipeline is a Product

You serve multiple customer clusters. The pipeline has:

- Users (devs, customers, you)
- A roadmap (whether explicit or not)
- Breaking changes (whether announced or not)
- Versions (whether tagged or not)

Treat it like one. The audit should include a "pipeline product surface" section—what interfaces are people consuming, and what are your stability guarantees?

#### 4.5 Eat Your Own Dog Food

Pipeline changes should flow _through_ the pipeline. If you're patching ArgoCD config imperatively to fix the pipeline, you've already lost. The audit should specifically check: _"Can a change to the GitOps controller itself be made via a PR to the GitOps repo, merged, and rolled out using the same reconciliation loop?"_ If the answer is no, that's your top optimisation.

#### 4.6 DORA Isn't Quite right—measure the Right Things

For a platform pipeline, consider these instead of (or alongside) DORA:

- Bootstrap time from zero—clean subscription → working cluster (the ultimate end-to-end test)
- Mean time to drift detection
- Mean time to deliver a secret rotation across all customer clusters
- % of customer clusters on the latest pipeline version (fleet currency)
- Operator on-call interventions per week

These map to _your_ pain in a way deployment frequency does not.

#### 4.7 The Audit Should Produce a Ranked Pain Register, not Prose

Output format suggestion:

| Pain | Source (incident/PR/Slack) | Frequency | Blast radius | Cost to fix | Cost to leave | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Double- `tpl` Helm bug | mkuh-prd-4 bootstrap | recurring | per chart | M | H | P1 |
| VSO `overwrite: false` staleness | several | recurring | per secret | S | H | P1 |
| ArgoCD auto-sync racing imperative patches | mkuh-prd-4, EOE | every fix | per app | M | M | P2 |
| Terragrunt `common.yaml` / `override.yaml` merge | multiple | constant friction | code-level | S | M | P2 |

This format forces you to be specific and gives the optimisation phase ready-made tickets.

#### 4.8 Time-box the Audit Hard

- Calendar window: 3 weeks elapsed
- Focus time: 2 hours/day max on this
- Output: one ADR + one register
- If you hit the calendar window without finishing, you publish what you have and stop. Done > perfect.

#### 4.9 ADHD-specific risk

Pipeline-optimisation projects are catnip and quicksand for ADHD brains: novel, technically interesting, infinite depth, no external deadline. Without the time-box and the explicit Investigation/Optimisation split, this project will eat six months and produce only a fascinating tour of your own infrastructure. The constraint is the gift.

---

### 5. Your Next Physical Action

Open your notes app. Create one file: `pipeline-audit/scoping-v0.md`.

Answer only three questions—one or two sentences each:

1. Which pipeline am I auditing first—A1, A2, A3, A4, A5, or A6? _(I'd suggest A5—bootstrap—since that's where the documented pain lives.)_
2. Who is the primary user whose experience I want the audit to inform? _(Likely you / the platform team, given the bootstrap focus.)_
3. What does the audit deliverable look like, concretely? _(Suggested default: an ADR + ranked pain register committed as a PR to the platform repo.)_

That's it. 15-minute time-box. Don't fill in the trigger list yet. Don't start the audit. Don't write the Grafana queries. Just those three answers.

Once `scoping-v0.md` exists with three answers, the _investigation project_ is born. Then—and only then—run the trigger list (§2) against it, then Phase 1 of Natural Planning.

The optimisation projects don't exist yet. They will only exist _after_ the audit is committed. That's a feature, not a bug.

---

You

I have another complex project to improve our azure entra IAM and move it to IAC and pims and tidy up the policies

---

Claude

[[Restructuring Entra ID—Scoping, IaC & PIM]]

[[HEAD Scoping fuzzy projects before natural planning]]
