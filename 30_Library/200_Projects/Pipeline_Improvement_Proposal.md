---
created: 2026-06-16 09:55:31+00:00
modified: 2026-06-16 10:25:59+00:00
title: Pipeline_Improvement_Proposal
project_name: Pipeline
permalink: llmeon/30-library/200-projects/pipeline-improvement-proposal
---

## CI/CD Pipeline Transformation: A Team-Centric, Data-Driven Approach

This document synthesizes our current research, audit findings, and industry best practices into a unified proposal for improving our CI/CD pipeline.

Rather than dictating a new workflow, this document serves as a starting point for the team. It defines a shared understanding of what a pipeline is for, identifies our current blockers, and outlines an evidence-based method for experimenting with improvements.

---

### 1. The Goal and Purpose of the Pipeline (What "Good" Looks Like)

We cannot improve the pipeline if we don't agree on its fundamental purpose. Drawing from modern software engineering principles (like those in _Accelerate_ and _Continuous Delivery_), we propose the following shared understanding:

- A Falsification Mechanism: The pipeline's primary job is _not_ just to build software, but to act as a scientific test to prove that a change is unfit for production. If a release candidate passes all tests, we can trust it is safe to deploy.
- The Only Route to Production: The deployment pipeline defines releasability and must be the exclusive, automated path to production.
- Decoupling Deployment from Release: Deploying code to a server is a technical exercise; releasing a feature to users is a business decision. A healthy pipeline allows us to deploy constantly without necessarily "releasing" half-finished features to customers.

#### Defining "Good" (The DORA Metrics)

To avoid opinion-based debates, we will measure "good" using the industry-standard DORA metrics. A healthy pipeline should lead us toward:

1. Lead Time for Changes: The time it takes to go from a code commit to running in production (Goal: Less than an hour).
2. Deployment Frequency: How often we deploy code (Goal: On-demand / Multiple times a day).
3. Change Failure Rate: The percentage of deployments causing a failure in production (Goal: Near zero, enabled by small batches).
4. Time to Restore Service (MTTR): How long it takes to recover from a failure (Goal: Minutes, enabled by versioned states and automated rollbacks).

---

### 2. Identifying the Real Blockers

Based on our audits and logs, the challenges slowing us down aren't just technical; they are structural.

#### A. The Structural Blocker: "Merge Skew" & Big Batches

The most significant blocker is Merge Skew (the "racing commits" problem), compounded by the team's tendency to work in Big Batches.

- The Conflict: Developers often want to wait until a full feature is complete before merging it. This results in massive, long-lived branches.
- The Impact: When multiple large branches are finally merged into `main`, they conflict or break unexpectedly because the pipeline tested them in isolation against an outdated state. This creates long queues, painful reviews, and high failure rates.

#### B. Process Bottlenecks: Manual Gates & Runner Leaks

- Single-Owner Review Gates: Relying on a single person for approvals creates a massive queue, dragging down Lead Time.
- Manual Pipeline Interventions: We have instances where Terraform plans run _after_ applies, or manual triggers leak runner capacity, blocking subsequent pipelines entirely.

---

### 3. An Evidence-Based, Falsifiable Improvement Process

To ensure this is a team-owned transformation and not a top-down mandate, we will adopt an Experiment-Driven Approach based on the Toyota Improvement Kata:

1. Establish the Baseline: Instrument the pipeline to track our current DORA metrics. We cannot prove an improvement works if we don't know our starting point.
2. Formulate a Hypothesis: E.g., _"If we implement Feature Flags for our next epic, our Lead Time will decrease by X days because developers can merge daily without exposing unfinished work to users."_
3. Run the Experiment: Try the new practice for a single sprint or a single service.
4. Measure and Retro: Look at the data. Did Lead Time improve? Did Change Failure Rate spike? If the data disproves the hypothesis, we discard the change. If it works, we adopt it into our standard workflow.

---

### 4. Options for Improvement (The Roadmap)

Here are the primary options to resolve our blockers, which we can test as team experiments:

#### Option 1: Adopt Feature Flags to Enable Small Commits

- The Idea: To solve the team's concern about "releasing" unfinished work, we introduce Feature Flags (Feature Toggles).
- Why it works: Developers can commit small, safe increments of code daily (solving the Merge Skew/Big Batch problem for the pipeline), but keep the code hidden behind a flag until the business is ready to "release" it.

#### Option 2: Optimize Pipeline Efficiency & YAML Architecture

- The Idea: Move from a rigid "Stage-by-Stage" pipeline to a Directed Acyclic Graph (DAG) using the `needs:` keyword.
- Why it works: Jobs run immediately when their specific dependencies are met, rather than waiting for an entire stage to complete. Combined with "Fail-Fast" linting/testing, this drastically reduces compute minutes and speeds up the feedback loop.

#### Option 3: Transition to Trunk-Based Development

- The Idea: Move away from GitFlow or long-lived feature branches. All developers commit to `main` (trunk) frequently, at least once a day.
- Why it works: It forces small batches, eliminates massive merge conflicts, and ensures continuous integration is actually continuous. (Note: This relies heavily on Option 1 being implemented first).

#### Option 4: Implement Merged Results Pipelines / Merge Trains

- The Idea: Configure GitLab to run pipelines against the _merged_ result of the source and target branch, rather than just the source branch.
- Why it works: It prevents the "Merge Skew" problem by validating exactly what will land in `main`, preventing broken trunks.

---

### 5. Next Steps for the Team

1. Review and Debate: Read through this document. Do we agree on the definition of "Good" (DORA metrics)?
2. Instrument the Baseline: Let's get our tracking in place so we have real data to look at.
3. Choose One Experiment: Pick _one_ option from Section 4 (e.g., Feature flags for the next feature) and try it for two weeks.