---
aliases: [Configuration Generator Pattern, Generative Config, GIC Framework]
confidence: 5/5
created: 2025-12-13T00:00:00Z
epistemic: 
last-synthesis: 2025-12-13
last_reviewed: 2025-12-13
modified: 2025-12-13T14:08:09Z
purpose: To define the Generative Infrastructure Configuration (GIC) Framework, a pattern for treating configuration as a generated output to maximize robustness and consistency.
related-soTs: ["[[SoT - PRODOS (System Architecture)]]", "[[SoT - Software Configuration Management Patterns]]"]
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: [architecture, configuration_management, devops, infrastructure_as_code, terraform]
title: SoT - Generative Infrastructure Configuration Framework
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Generative Infrastructure Configuration (GIC)
> GIC is an infrastructure management framework that treats configuration as a **generated output** rather than a manual input.
>
> **Core Principle:** By defining a minimal, declarative **Configuration Kernel** (intent) and processing it through a validated **Configuration Generator** (code), the system automatically derives complex, error-prone values (protocols), ensuring consistency, reducing cognitive load, and making changes explicitly evident.

---

## 2. Working Knowledge (The Framework)

### The Core Problem

Manual configuration in modern distributed systems is fragile. Reliance on vast, explicit `.tfvars` files leads to:

-   **Error-Prone Deployments:** Typos in hostnames or ARNs cause failures.
-   **Inconsistency:** Naming conventions drift across environments.
-   **High Cognitive Load:** Developers must manage dozens of unique identifiers.
-   **Opaque Changes:** The impact of variable changes is often unclear.

### The Solution Architecture

GIC shifts the source of truth from fragile inputs to robust code.

#### 1. The Configuration Kernel (The Intent)

A minimal set of human-defined inputs describing *what* is being deployed, not *how*.

-   **Example Inputs:** `app_name`, `environment`, `base_domain`, `aws_region`, `cost_centre`.
-   **Characteristic:** Small surface area, high robustness.

#### 2. The Configuration Generator (The Protocol)

A version-controlled module (e.g., Terraform module) that ingests the Kernel and applies codified rules to producing a deterministic output.

-   **Function:** `Kernel -> Generator -> Full Configuration Manifest`
-   **Characteristic:** Tested, peer-reviewed, "pure function" logic.

#### 3. The Generated Manifest (The Output)

The complex, derived values used by infrastructure resources.

-   **Examples:**
    -   DNS Hostnames: `user-service.prod.my-company.co.uk`
    -   S3 Buckets: `my-company-prod-user-service-assets`
    -   Secret Paths: `/prod/user-service/db_creds`
    -   Tags: `{ Application="user-service", Env="prod", ... }`

---

## 3. Current Understanding (Implementation Patterns)

### Terraform & Helm Integration

GIC is particularly powerful when chaining tools. Terraform acts as the "Root Generator," producing values that are then passed downstream.

**The Workflow:**
1.  **Kernel:** Developer commits a minimal `.tfvars` file.
2.  **Generator:** Terraform GIC module derives all names, tags, and paths.
3.  **Infrastructure:** Terraform provisions cloud resources using these derived values.
4.  **Application:** Terraform renders values for Helm charts (or other app configs) using the *same* generated data, ensuring the application layer and infrastructure layer are perfectly synchronized.

### Benefits
-   **Resilience:** Typos are caught in code review of the Generator, not in ad-hoc config files.
-   **Consistency:** Naming conventions are enforced by code.
-   **Agility:** Spinning up new environments requires only a minimal Kernel file.
-   **Change Evidence:** Changes to the Generator are code changes; changes to the Kernel are explicit data changes.

---

## 4. Minimum Viable Understanding (MVU)

1.  **Input Minimal Intent:** Only define what distinguishes this deployment (Name, Env).
2.  **Generate Complexity:** Use code to derive names, paths, and tags based on strict protocols.
3.  **Consolidate Config:** Use the generated outputs to drive both Infrastructure (Terraform) and Application (Helm) configuration.
4.  **Fail Fast:** Validate the Generator code, so individual deployments are safe by default.

---

## 5. Sources and Links
-   Original Proposal: "RFC-001: Generative Infrastructure Configuration (GIC) Framework" (Archived)
-   [[SoT - Software Configuration Management Patterns]] (Foundational discipline)
