---
aliases:
- Modularity by Information Hiding
- Parnas Information Hiding
created: 2025-12-12 00:00:00+00:00
modified: 2026-07-04 10:50:56+00:00
permalink: llmeon/30-library/so-t/so-t-information-hiding-parnas
see_also: []
superseded_by: ''
supersedes: ''
tags:
- design-principles
- modularity
- SoftwareEngineering
- SoftwareEngineering/Architecture
title: SoT - Information Hiding (Parnas)
prodos:
  kind: sot
  lifecycle: stable
  review:
    last_reviewed: '2025-12-12'
---


## 2. Core Principles

Parnas's approach contrasts with decomposition based on functional flowcharts. Instead, he proposed:

- Decision-Based Decomposition: Modules should be organized around design decisions, not steps in processing.
- Encapsulation of Change: Modules should hide decisions that are likely to change (e.g., file formats, hardware devices, complex algorithms).
- Abstract Interfaces: Modules communicate through well-defined, stable interfaces that expose _what_ the module does, but not _how_ it does it.

---

## 3. Goals and Benefits

The primary goals of Information Hiding are to manage complexity and enable system evolution.

### A. Improved Maintainability & Flexibility

- Reduced Impact of Changes: Changes to a hidden design decision (e.g., switching database technology) are localized within a single module.
- Independent Development: Teams can develop modules concurrently without needing to know each other's internal implementations.

### B. Enhanced Comprehensibility

- Reduced Cognitive Load: Developers can understand a module's function without grasping its internal intricacies.
- Clearer Abstractions: Forces designers to create clean, well-defined boundaries.

### C. Promotes Modularity

- Supports the creation of loosely coupled components that interact through stable interfaces.

---

## 4. ProdOS Integration

Information Hiding principles are vital for managing knowledge complexity in ProdOS:

- SoT as Modules: Each SoT (Source of Truth) note acts as a module. It presents a definitive statement and core concepts (the "abstract interface"), while hiding the "implementation details" (the dozens of original Zettelkasten notes that were synthesized).
- Readability & Re-entry: This allows for frictionless re-entry into complex topics; you only need the SoT's interface to understand the concept, reducing cognitive load.
- Managing Change: When underlying details change (e.g., new research), only the relevant SoT needs to be updated, not every note that references the concept.
