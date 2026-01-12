---
created: 2026-01-11T17:52:33+00:00
modified: 2026-01-12T09:18:08+00:00
title: Master Refactoring Plan
---

# Master Refactoring Plan

## Cluster 1: Helm Chart Image Inventory

**Status:** **PASS**
**Proposed Structure:** `[[MOC - Helm Chart Image Inventory]]`

**Actions:**
- [ ] Create `[[MOC - Helm Chart Image Inventory]]` as the cluster entry point.
- [ ] **Consolidate** the following atoms into `[[SoT - Helm Chart Image Inventory]]`:
    - `Helm Chart Image Investigation Overview (2025-12-29)`
    - `MongoDB Helm Chart Details (Version 16.5.45)`
    - `MinIO Helm Chart Details (Version 14.7.8)`
    - `PostgreSQL Helm Chart Details (Version 15.5.15)`
    - _Guidance:_ Structure as a table to eliminate repetitive boilerplate (e.g., registry URLs).
    - [ ] Delete original atoms after verification.

## Cluster 2: Centralized MCP Architecture

**Status:** **PASS** (Verify Docker Images)
**Proposed Structure:** `[[MOC - Centralized MCP Architecture]]`

**Actions:**
- [ ] Create `[[MOC - Centralized MCP Architecture]]`.
- [ ] **Merge** architectural definitions into `[[SoT - MCP Gateway Architecture]]`:
    - `Centralised MCP Hub Architecture`
    - `Centralisation via Local Proxy/Gateway`
    - `The MCP-Proxy Router Framework`
    - [ ] Delete original atoms.
- [ ] **Merge** technical configurations into `[[Protocol - Docker MCP Gateway Configuration]]`:
    - `Docker Compose Configuration for MCP Hub`
    - `Implementing an MCP Router with Docker Compose`
    - _Guidance:_ Validate `mcp/memory:latest` and `mcp/filesystem:latest` images (potential hallucination risk).
    - [ ] Delete original atoms.

## Cluster 3: OHDSI Domain Architecture

**Status:** **WARN** (Potential missing content: Section 3.3)
**Proposed Structure:** `[[MOC - OHDSI Domain Architecture]]`

**Actions:**
- [ ] Create `[[MOC - OHDSI Domain Architecture]]`.
- [ ] **Merge** core definitions into `[[SoT - OHDSI Core Domain Model]]`:
    - `Ubiquitous Language - Core Entities`
    - `Bounded Context - Cohort Definition (Core Domain)`
    - [ ] Delete original atoms.
- [ ] **Merge** analytic contexts into `[[SoT - OHDSI Analytic Subdomains]]` (or append to Core Domain Model as a subdomain section):
    - `Ubiquitous Language - Analytic Contexts`
    - `Bounded Context - Analytic Subdomains`
    - [ ] Delete original atoms.

## Cluster 4: Azure Terraform Infrastructure Refactoring

**Status:** **PASS**
**Proposed Structure:** `[[Project - Azure Terraform Infrastructure Refactoring]]`

**Actions:**
- [ ] Create `[[Project - Azure Terraform Infrastructure Refactoring]]`.
- [ ] **Merge** inventory and implementation rules into `[[Protocol - Terraform Implementation Plan]]`:
    - `Target Resource Inventory (State List)`
    - `Final Implementation Plan (Index 5)`
    - [ ] Delete original atoms.
