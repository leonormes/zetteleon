---
aliases: [Terraform Complexity, Infrastructure Complexity, IaC Abstraction]
created: 2026-02-01T17:05:00+00:00
last_reviewed: 
modified: 2026-02-01T17:05:00+00:00
status: seedling
tags: [devops, terraform, infrastructure, complexity]
title: SoT - Infrastructure Complexity Management
type: SoT
updated: 
---

## The Core Insight

> In Infrastructure as Code (IaC), complexity is conserved. It resides either in the **Graph** (Dependencies) or the **Abstraction** (Modules/Data). To reach the "Complexity Floor," we must move logic out of Resource Blocks (`main.tf`) and into Data Structures (`locals` / `variables`).

## 1. Measuring Terraform Complexity

Since IaC is declarative, we don't measure "loops." We measure **Coupling** and **Blast Radius**.

### A. The "Spaghetti" Test (Dependency Graph)
-   **Metric:** High edge-to-node ratio in the DAG (`terraform graph`).
-   **Symptom:** Everything depends on everything. Changing a Security Group forces a recreation of the EKS Cluster.
-   **Goal:** A clean tree structure with isolated branches.

### B. The Blast Radius (State Size)
-   **Metric:** Number of resources in a single `.tfstate` file.
-   **High Complexity:** 500+ resources. One lock blocks the entire platform.
-   **Low Complexity:** Layered State (Network Layer -> Cluster Layer -> App Layer).

### C. Module Fan-Out
-   **Too Complex:** A module with 40 input variables (Cognitive Overload).
-   **Too Simple:** Hardcoded values inside the module (Hidden Complexity).
-   **The Sweet Spot:** "Opinionated Defaults." The module takes `env = "prod"` and calculates the `cidr_block` internally.

## 2. Reducing Complexity: The "Code to Data" Refactor

**Anti-Pattern (Complexity in Code):**
Manually defining 10 different `aws_s3_bucket` resources with slightly different tags and policies.

**Pattern (Complexity in Data):**
defining a `local.buckets` map (The Data) and using a single `aws_s3_bucket` resource with `for_each` (The Engine).

> "The code becomes a simple engine that processes the data."

## 3. The ArgoCD Abstraction (Separation of Concerns)

A major source of Accidental Complexity is forcing Terraform to manage Kubernetes Workloads.

-   **The Complexity Trap:** Using `helm_release` providers within Terraform to deploy Apps (Prometheus, Grafana). Terraform struggles with K8s eventual consistency, bloating the state file.
-   **The Solution:** Terraform stops at the **API Boundary**.
    1.  **Terraform:** Builds the "Hardware" (VPC, EKS, IAM).
    2.  **ArgoCD:** Manages the "Software" (Helm Charts, Deployments).

By enforcing this split, we reduce the Terraform graph size by 50-80%.

See Also: [[SoT - Conservation of Complexity]], [[SoT - Kubernetes Secrets Management]]
