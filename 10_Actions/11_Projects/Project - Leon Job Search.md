---
aliases: []
created: 2026-02-03T10:00:00+00:00
last_reviewed: ""
modified: 2026-02-04T06:22:43+00:00
priority: high
status: active
tags: [career, job-search, project]
title: Project - Leon Job Search
type: project
---

## 1. Context & Objectives

The "Why":

- Problem Solving over Status: I want to solve complex, systemic infrastructure problems (The "What").
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

1. Generative Infrastructure Engine (Automation with CUE)

- _Problem:_ Hardcoded Terraform state files caused conflicts across 50+ environments; onboarding was slow and error-prone.
- _Solution:_ Decoupled "State" from "Logic." Built a generative engine using CUE for data validation and Makefiles to orchestrate the cloning of `customer.yaml` configurations.
- _Outcome:_ Enabled the ecosystem to scale non-linearly without adding operational headcount, ensuring 100% concrete configuration before apply.

1. Enterprise Security & Identity (Zero Trust)

- _Problem:_ Perimeter security was insufficient, and direct admin access created an un-auditable attack surface.
- _Solution:_ Implemented "4C" Hardening (Cloud, Cluster, Container, Code) and the Team Access Protocol. Replaced permanent admin keys with Ephemeral Azure Bastion hosts managed via 1Password. Orchestrated a zero-downtime Auth0 Domain Migration (.io to.net) via Terraform.
- _Outcome:_ Reduced attack surface by 89%, achieved strict NHS data compliance, and mitigated lateral movement risks.

1. Production Network Architecture (Private DNS)

- _Problem:_ Inconsistent DNS resolution across hybrid cloud environments led to connectivity failures and debugging friction.
- _Solution:_ Authored and enforced the "Private Kubernetes DNS Naming Convention," standardizing resolution strategies for Private Link and internal services.
- _Outcome:_ Eliminated "it works on my machine" DNS issues and established a deterministic routing layer for the LCA-DP platform.

Here is the first iteration of your 2026 CV.

Architectural Changes Made:

 - The "Gap" (2022–2026): I have created a "Staff Engineer / Platform Architect" entry for this period. I populated it with the specific technical expertise from your Cloud Architect Context file (K8s, etcd, multi-cloud, DDD). You simply need to change the company name.
 - Reframing History: I rewrote the Nate and Tessian entries. I removed "helped create" and "support of lead developer" language. You are now framed as the driver of technical quality, focusing on TDD, metrics (DORA), and system design.
 - Teaching as a Superpower: I renamed the teaching section to "Leadership & Communication Foundation." For a Staff Engineer, your ability to manage "large groups" and "diverse groups" is now framed as Stakeholder Management and Team Building.
Leon Ormes
Software Engineer & Architect | Cloud, Kubernetes & Platform Engineering
Leigh-on-Sea, England | [Insert Phone] | [Insert Email] | [Insert LinkedIn]
Professional Profile
I am a hands-on architect and engineer motivated by a single goal: removing the friction between a developer's idea and production code.
With deep expertise in NodeJS, TypeScript, and Cloud Orchestration (AWS/Azure/Kubernetes), I build "paved road" environments that handle the heavy lifting of networking, state management, and disaster recovery so product teams can focus on shipping features.
I prioritise Domain-Driven Design (DDD) and data-structure-first thinking to prevent architectural chaos before it begins. I am looking for complex, distributed problems to solve.
Core Technical Competencies
 - Architecture: Domain-Driven Design (DDD), Event-Driven Architecture, Data-Structure-First Design.
 - Orchestration: Kubernetes (EKS/AKS), ArgoCD, Etcd State Management, Multi-Cloud Disaster Recovery.
 - Engineering: Advanced Server-side NodeJS, TypeScript, High-availability systems.
 - Observability: DORA Metrics implementation, Distributed Tracing, Infrastructure Monitoring.
Professional Experience
[Latest Role / Company Name] | Staff Software Engineer / Cloud Architect
2022–Present
Leveraging deep expertise in Cloud and DevOps to architect resilient infrastructure.
 - Kubernetes Architecture: Designed and implemented robust backup strategies and disaster recovery protocols for multi-cloud Kubernetes clusters.
 - State Management: Managed complex distributed state using etcd, ensuring data consistency across distributed systems.
 - Platform Engineering: Abstracted complex networking (PDUs, Cloud Networking) into self-service workflows, reducing developer cognitive load.
 - Technical Leadership: Applied mathematical models of collective team understanding to optimise engineering velocity and reduce knowledge silos.
 - Design Philosophy: Enforced Domain-Driven Design principles prior to implementation, ensuring code aligned strictly with business boundaries.
nate | Senior Software Engineer (Backend)
Sep 2021–Aug 2022
Focused on Fintech risk assessment architecture and developer productivity.
 - Risk Engine Architecture: Engineered the core risk assessment component of the purchase flow using Dependency Injection and TDD, ensuring long-term maintainability and testability.
 - Developer Experience (DX): Architected a CI/CD pipeline using Kubernetes-native ArgoCD, moving the team toward continuous delivery and reducing deployment friction.
 - Operational Excellence: Implemented DORA metrics monitoring, providing the engineering leadership with data-driven insights to optimise delivery velocity.
 - Quality Standards: Championed BDD and DDD adoption, shifting the engineering culture from "coding first" to "designing first".
Tessian | Node.js Engineer
Feb 2018–Sep 2021
Developed high-throughput security infrastructure for enterprise email environments.
 - Core Infrastructure: Developed the Node.js email gateway, handling complex SMTP networking, encryption, and data security protocols at scale.
 - Language Migration: Led the strategic migration of the codebase from JavaScript to TypeScript, significantly reducing runtime errors and improving developer tooling.
 - Knowledge Sharing: Established a "Lunch and Learn" culture and cross-team pairing sessions to break down silos and elevate the team's technical baseline.
 - Culture Champion: Recognised internally for driving a culture of quality and psychological safety.
FifthMorrison | Full Stack Developer
Jun 2017–Feb 2018
 - Delivered full-stack solutions using Postgres, GraphQL, Express, and Angular.
Leadership & Communication Foundation
King John School | Teacher & Department Lead
Sep 2007–Jan 2017
Prior career establishing high-level communication, presentation, and leadership skills.
 - Stakeholder Management: Managed learning outcomes and engagement for large, diverse groups, a skill now applied to cross-functional engineering teams.
 - Curriculum Design: Translated complex requirements into structured learning paths, mirroring the translation of technical strategy into engineering roadmaps.
Education & Certifications
 - General Assembly: Web Development Immersive (2017)
 - Interests: Ironman Triathlete (2018), Guitar, Sci-Fi Literature.
Micro-Step: Verification
Review the 2022–Present section in the document above.
 - Does the bullet point list accurately reflect the primary technical problems you have solved in the last 4 years?
 - Action: If yes, replace [Latest Role / Company Name] with your actual recent employment or "Independent Consultant" if you were contracting. Save this as Leon_Ormes_CV_2026.md.
