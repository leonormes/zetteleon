---
source_of_truth: []
aliases: ["Data-Oriented IaC", "DevOps Philosophy", "Infrastructure Strategy", "FitFile Infrastructure Model"]
confidence: "4/5"
created: 2026-01-02T23:30:00Z
epistemic: "strategy"
last_reviewed: "2026-01-02"
modified: 2026-01-03T10:18:48+00:00
purpose: "To define the architectural philosophy for DevOps and IaC, moving from brittle scripting to rigorous data modeling."
review_interval: "6 months"
see_also: ["[[SoT - Data-Oriented Programming (DOP) in Rust]]", "[[SoT - PRODOS (System Architecture)]]"]
status: "stable"
tags: ["devops", "iac", "SoftwareEngineering/Architecture", "strategy", "fitfile"]
title: SoT - DevOps & Infrastructure Architecture Strategy
type: "SoT"
---

## 1. The Core Tension: Complexity vs. Cognition

Current DevOps practices often fail because they exceed human cognitive limits. We build intricate, brittle systems (ArgoCD chains, Helm dependencies) that are impossible to hold in working memory.

* **The Trap:** "Satisficing" (doing just enough to make it work) leads to sub-optimal legacy code that resists change.
* **The Reality:** A distributed system is a complex graph of state, but we try to manage it with linear scripts (IaC).

## 2. The Strategic Pivot: Data-Oriented Infrastructure

We must shift from **Imperative Scripting** (telling the cloud what to do) to **Data-Oriented Modeling** (defining what the cloud *is*).

### 2.1 The Network as Data

Instead of disjointed config files, view the network as a rigorous data model:

* **Resources:** A set of IP addresses (Identity).
* **Reachability:** A map of allowed connections (Public vs. Private).
* **Constraint:** Private IPs have restricted reachability. This should be a **Type Constraint**, not just a firewall rule.

### 2.2 Unifying Identity

Identity concepts are currently scattered across boundaries (Hostname in DNS, Certificate in Vault/Store).

* **The Goal:** Represent the dependency `Hostname <-> Certificate <-> IP` as a single logical unit.
* **The Enforcement:** Make broken configurations (e.g., a Certificate without a matching DNS record) **uncodable** at the schema level.

## 3. FitFile Deployment Context

* **Environment:** Managed K8s (Cloud), Private Networking.
* **Release Strategy:** Unique tags per environment/customer (Multi-tenant).
* **Shared Responsibility:** We must define clear boundaries where our automation ends and the platform begins.

> **Next Action:** Build a "Data-First" object model of the deployment to expose these hidden dependencies.
