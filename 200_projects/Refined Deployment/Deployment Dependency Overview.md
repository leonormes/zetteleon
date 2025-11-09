---
aliases: []
confidence: 
created: 2025-09-05T10:29:29Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Deployment Dependency Overview
type:
uid: 
updated: 
version:
---

This document outlines the infrastructure deployment process, detailing the relationships between source control, our IaC platform, and the production environment. The goal is to provide a clear understanding of the current workflow to aid in onboarding and future refactoring efforts.

---

## Core Components

The system is comprised of several key components that work together to automate infrastructure provisioning.

- ### Source Control & Artefacts
  - **GitLab**1: This is the central version control system where all infrastructure code is stored. It serves as the single source of truth for our configurations.
  - **Artifactory**2: This repository likely stores built artefacts, provider plugins, or other dependencies required for the Terraform deployments.
- ### Infrastructure as Code (IaC)
  - **TFC Modules**3: This represents a collection of reusable, versioned Terraform modules. Using modules promotes consistency, reduces code duplication, and allows for standardised components across different parts of the infrastructure.
  - **Terraform Infrastructure**4: This is the main repository containing the root Terraform configurations. These configurations call upon the

`TFC Modules` to define the desired state of the overall infrastructure.

- ### Orchestration & State Management
  - **Terraform Cloud**5: This is the managed service used to execute Terraform runs. It securely stores the infrastructure's state file, manages secrets and variables, and provides an audit trail for all changes. It is configured under a specific

**Terraform Cloud Organisation**.

- ### Target Environment
  - **Production**7: This is the live environment where all the resources are provisioned and managed by Terraform. The detailed diagram within this section shows the complex network of deployed resources (e.g., servers, databases, load balancers) and their interdependencies.

---

## Deployment Workflow

The end-to-end process for making an infrastructure change follows these general steps:

1. **Code Change**: A developer makes a change to either a reusable module (`TFC Modules`) or the main configuration (`Terraform Infrastructure`) and pushes the commit to **GitLab**.
2. **Trigger**: This push event automatically triggers a webhook that notifies **Terraform Cloud** of the change.
3. **Plan**: Terraform Cloud clones the relevant repository, pulls the necessary modules, and runs a `terraform plan`. This generates an execution plan showing what resources will be created, modified, or destroyed.
4. **Apply**: After the plan is reviewed and approved by an engineer, the `apply` step is initiated within Terraform Cloud.
5. **Provisioning**: Terraform Cloud executes the apply, interacting with the cloud provider's APIs to bring the **Production** environment to its desired state as defined in the code.

---

## Refactoring & Simplification Suggestions

The diagram highlights a well-structured but complex system. Here are a few suggestions to consider for refactoring:

- **Clarify Production Dependencies**: The most complex part of the diagram is the set of interconnections within the `Production` block. The first step towards simplification would be to clearly document what these resources are and why they are dependent on each other. This can help identify logical groups of resources.
- **Decouple Infrastructure Stacks**: The `Terraform Infrastructure` repository could potentially be broken down into smaller, independent stacks. For example, instead of one large state file for all of production, you could have separate stacks for networking, the database layer, and each application service. This reduces the "blast radius" of a single change and simplifies planning and debugging.
- **Improve Visualisation**: For documentation purposes, consider creating multiple diagrams:
  - A **High-Level Overview** (like the one described above) that shows the main components and data flow.
  - Several **Detailed Diagrams** that zoom in on specific parts, such as the internal architecture of the `Production` environment for a particular service. This makes the overall system much easier to understand for someone new to the project.
