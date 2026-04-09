---
created: 2026-04-02T11:05:00+01:00
last-synthesis: 2026-04-02
modified: 2026-04-09T08:11:00+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [automation, gitops, iac, terraform, type/SoT, vault]
title: SoT - Vault Infrastructure Automation
trust-level: stable
---

## Minimum Viable Understanding (MVU)

Vault Infrastructure Automation replaces manual, error-prone configuration with an idempotent, manifest-driven Terraform pipeline. It centralizes all Vault primitives (Auth methods, Secrets Engines, Namespaces, and Policies) into a single YAML configuration file, which Terraform renders into API calls. This ensures consistency across environments and eliminates "tribal knowledge" regarding secret access.

## Working Knowledge

### 1. The Unified Manifest Pattern

The core of this automation is a `manifest.yaml` that serves as the single source of truth for the Vault environment.

- Auth Backends: Defines types (Kubernetes, AppRole, JWT) and paths.
- Secrets Engines: Configures KV-v2, PKI, or Database engines.
- Policies: Maps HCL policy files to Vault names.
- Roles: Binds Kubernetes ServiceAccounts or TFC Workspaces to specific policies and TTLs.

### 2. Idempotency & Stable Keys

To ensure predictable runs, Terraform must use stable keys for `for_each` loops:

- Vault: Uses `path` or `name` as the primary key.
- TFC Integration: Uses OIDC (Workload Identity) to authenticate Terraform Cloud runs to Vault, eliminating static `VAULT_TOKEN` environment variables.

### 3. Bootstrap & Lifecycle

- Initial Setup: A one-time manual token is used to create the TFC JWT auth method and role. All subsequent runs are self-authenticated.
- Deletion Protection: Stateful resources (like `vault_mount`) should use `lifecycle { prevent_destroy = true }` to avoid accidental data loss during manifest refactoring.

## Current Understanding

### GitOps Flow for Secrets

1. Change: Engineer updates `manifest.yaml` (e.g., adding a new Kubernetes role).
2. Validate: CI validates the YAML schema against a JSON schema definition.
3. Plan: Terraform calculates the diff (e.g., "Add 1 new role").
4. Apply: On merge, Terraform updates Vault. VSO then automatically reconciles the new role in the cluster.

## Related Knowledge

- Operator Integration: [[SoT - Vault Secrets Operator (VSO)]] (`rel:: broader`)
- Infrastructure Theory: [[SoT - Infrastructure Complexity Management]] (`rel:: supports`)
- TFC Best Practices: [[SoT - Terraform Cloud Best Practices]]
