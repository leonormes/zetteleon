---
aliases: []
created: 2026-02-03T10:00:00+00:00
last_reviewed: ""
modified: 2026-02-03T14:19:45+00:00
priority: high
status: active
tags: [career, job-search, project]
title: Project - Leon Job Search
type: project
---

## 1. Context & Objectives

The "Why":

- Problem Solving over Status: I want to solve complex, systemic infrastructure problems (The "What"). I am indifferent to the title on the door (The "Label").
- Efficiency: Hierarchies often introduce latency. I want a role where technical decisions are made based on data and architectural fit, not rank.
- Wage: Commensurate with "Staff/Principal" expertise, but applied strictly to technical execution.

## 2. Job Requirements (The Filter)

- Role Focus: Hands-on Architecture, Platform Engineering, "The Fixer."
- Tech Stack: Kubernetes (EKS/AKS), NodeJS/TypeScript, Terraform, AWS/Azure, Rust (Tooling).
- Culture:
    - Flat Structure: Teams that value peer review over managerial approval.
    - Async-First: Documentation as the primary source of truth.
- Anti-Pattern: Avoid roles that conflate "Leadership" with "Management."
- Red Flags:
    - Organisations obsessed with "reporting lines."
    - Environments where "Principal" means "Post-Technical" (i.e., just meetings).

## 3. CV Draft (The Artifact)

### Leon Ormes -- Cloud Architect & Platform Engineer

Summary
A production-hardened engineer obsessed with reducing toil and managing complexity. I reject the notion that infrastructure requires "heroics"; instead, I build systems that are boringly reliable. I specialise in Domain-Driven Design (DDD) and treating infrastructure as a compiled software product. I am not looking to build an empire; I am looking to build systems that work.

Core Philosophy

- Zero Toil: If a human has to do it twice, automate it.
- Data-Structure-First: Define the domain model before writing a single line of implementation.
- Systems Thinking: Optimise the whole, not just the local component.

Key Technical Achievements

1. The "Helm Chart Compiler" (Complexity Reduction)

- _Problem:_ Multi-tenant deployments were fragile due to massive copy-paste YAML and configuration drift.
- _Solution:_ Treated Helm as a compiler target rather than a config file. Created a `fitfile-platform` library that accepts high-level _Intent_ and compiles it into hardened manifests.
- _Outcome:_ Reduced tenant onboarding time by 90% and eliminated "magic number" configurations across the estate.

2. Generative Infrastructure Engine (Automation with CUE)

- _Problem:_ Hardcoded Terraform state files caused conflicts across 50+ environments; onboarding was slow and error-prone.
- _Solution:_ Decoupled "State" from "Logic." Built a generative engine using CUE for data validation and Makefiles to orchestrate the cloning of `customer.yaml` configurations.
- _Outcome:_ Enabled the ecosystem to scale non-linearly without adding operational headcount, ensuring 100% concrete configuration before apply.

3. Enterprise Security & Identity (Zero Trust)

- _Problem:_ Perimeter security was insufficient, and direct admin access created an un-auditable attack surface.
- _Solution:_ Implemented "4C" Hardening (Cloud, Cluster, Container, Code) and the Team Access Protocol. Replaced permanent admin keys with Ephemeral Azure Bastion hosts managed via 1Password. Orchestrated a zero-downtime Auth0 Domain Migration (.io to.net) via Terraform.
- _Outcome:_ Reduced attack surface by 89%, achieved strict NHS data compliance, and mitigated lateral movement risks.

4. Production Network Architecture (Private DNS)

- _Problem:_ Inconsistent DNS resolution across hybrid cloud environments led to connectivity failures and debugging friction.
- _Solution:_ Authored and enforced the "Private Kubernetes DNS Naming Convention," standardizing resolution strategies for Private Link and internal services.
- _Outcome:_ Eliminated "it works on my machine" DNS issues and established a deterministic routing layer for the LCA-DP platform.

## 4. Cover Letter Template (The Pitch)

Subject: Application for [Role Name] - Leon Ormes

The "Why Me" (30 Seconds):

I am an engineer who believes that hierarchy often gets in the way of good architecture.

I am not applying to be a "Staff Engineer" for the badge; I am applying because I have the experience to solve the systemic problems that usually kill velocity at scale. I focus on the "Second Derivative" of productivity: I don't just fix the bug; I build the tool that makes the bug impossible.

My Approach:

1. Complexity Management: I use patterns like "Helm-as-a-Compiler" to abstract complexity, not just document it.
2. Zero Politics: I believe the best idea should win, regardless of who proposes it. I prefer code and documentation over meetings and titles.
3. Data-Centric Design: I apply Domain-Driven Design to infrastructure. Get the data structures right, and the implementation follows naturally.

I am looking for a high-autonomy role where I can apply deep technical rigour to hard problems, without the distraction of ladder-climbing.
